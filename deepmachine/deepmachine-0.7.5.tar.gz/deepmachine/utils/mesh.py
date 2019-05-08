import sklearn.metrics
import sklearn.neighbors
import matplotlib.pyplot as plt
import scipy.sparse
import scipy.sparse.linalg
import scipy.spatial.distance
import numpy as np
import menpo3d.io as m3io

from scipy.stats import norm
from mpl_toolkits.mplot3d import Axes3D
from menpo3d.rasterize import rasterize_mesh
from menpo3d.rasterize import rasterize_barycentric_coordinate_images
from itwmm.visualize import lambertian_shading
from menpo.transform import Homogeneous
from menpo.shape import ColouredTriMesh, TriMesh


from .np import rotation_matrix
    

def grid(m, dtype=np.float32):
    """Return the embedding of a grid graph."""
    M = m**2
    x = np.linspace(0, 1, m, dtype=dtype)
    y = np.linspace(0, 1, m, dtype=dtype)
    xx, yy = np.meshgrid(x, y)
    z = np.empty((M, 2), dtype)
    z[:, 0] = xx.reshape(M)
    z[:, 1] = yy.reshape(M)
    return z


def distance_scipy_spatial(z, k=4, metric='euclidean'):
    """Compute exact pairwise distances."""
    d = scipy.spatial.distance.pdist(z, metric)
    d = scipy.spatial.distance.squareform(d)
    # k-NN graph.
    idx = np.argsort(d)[:, 1:k+1]
    d.sort()
    d = d[:, 1:k+1]
    return d, idx


def distance_sklearn_metrics(z, k=4, metric='euclidean'):
    """Compute exact pairwise distances."""
    d = sklearn.metrics.pairwise.pairwise_distances(
            z, metric=metric, n_jobs=-2)
    # k-NN graph.
    idx = np.argsort(d)[:, 1:k+1]
    d.sort()
    d = d[:, 1:k+1]
    return d, idx


def distance_lshforest(z, k=4, metric='cosine'):
    """Return an approximation of the k-nearest cosine distances."""
    assert metric is 'cosine'
    lshf = sklearn.neighbors.LSHForest()
    lshf.fit(z)
    dist, idx = lshf.kneighbors(z, n_neighbors=k+1)
    assert dist.min() < 1e-10
    dist[dist < 0] = 0
    return dist, idx

# TODO: other ANNs s.a. NMSLIB, EFANNA, FLANN, Annoy, sklearn neighbors, PANN


def adjacency(dist, idx):
    """Return the adjacency matrix of a kNN graph."""
    M, k = dist.shape
    assert M, k == idx.shape
    assert dist.min() >= 0

    # Weights.
    sigma2 = np.mean(dist[:, -1])**2
    dist = np.exp(- dist**2 / sigma2)

    # Weight matrix.
    I = np.arange(0, M).repeat(k)
    J = idx.reshape(M*k)
    V = dist.reshape(M*k)
    W = scipy.sparse.coo_matrix((V, (I, J)), shape=(M, M))

    # No self-connections.
    W.setdiag(0)

    # Non-directed graph.
    bigger = W.T > W
    W = W - W.multiply(bigger) + W.T.multiply(bigger)

    assert W.nnz % 2 == 0
    assert np.abs(W - W.T).mean() < 1e-10
    assert type(W) is scipy.sparse.csr.csr_matrix
    return W


def replace_random_edges(A, noise_level):
    """Replace randomly chosen edges by random edges."""
    M, M = A.shape
    n = int(noise_level * A.nnz // 2)

    indices = np.random.permutation(A.nnz//2)[:n]
    rows = np.random.randint(0, M, n)
    cols = np.random.randint(0, M, n)
    vals = np.random.uniform(0, 1, n)
    assert len(indices) == len(rows) == len(cols) == len(vals)

    A_coo = scipy.sparse.triu(A, format='coo')
    assert A_coo.nnz == A.nnz // 2
    assert A_coo.nnz >= n
    A = A.tolil()

    for idx, row, col, val in zip(indices, rows, cols, vals):
        old_row = A_coo.row[idx]
        old_col = A_coo.col[idx]

        A[old_row, old_col] = 0
        A[old_col, old_row] = 0
        A[row, col] = 1
        A[col, row] = 1

    A.setdiag(0)
    A = A.tocsr()
    A.eliminate_zeros()
    return A


def laplacian(W, normalized=True):
    """Return the Laplacian of the weigth matrix."""

    # Degree matrix.
    d = W.sum(axis=0)

    # Laplacian matrix.
    if not normalized:
        D = scipy.sparse.diags(d.A.squeeze(), 0)
        L = D - W
    else:
        d += np.spacing(np.array(0, W.dtype))
        d = 1 / np.sqrt(d)
        D = scipy.sparse.diags(d.A.squeeze(), 0)
        I = scipy.sparse.identity(d.size, dtype=W.dtype)
        L = I - D * W * D

    # assert np.abs(L - L.T).mean() < 1e-9
    assert type(L) is scipy.sparse.csr.csr_matrix
    return L


def lmax(L, normalized=True):
    """Upper-bound on the spectrum."""
    if normalized:
        return 2
    else:
        return scipy.sparse.linalg.eigsh(
                L, k=1, which='LM', return_eigenvectors=False)[0]


def fourier(L, algo='eigh', k=1):
    """Return the Fourier basis, i.e. the EVD of the Laplacian."""

    def sort(lamb, U):
        idx = lamb.argsort()
        return lamb[idx], U[:, idx]

    if algo is 'eig':
        lamb, U = np.linalg.eig(L.toarray())
        lamb, U = sort(lamb, U)
    elif algo is 'eigh':
        lamb, U = np.linalg.eigh(L.toarray())
    elif algo is 'eigs':
        lamb, U = scipy.sparse.linalg.eigs(L, k=k, which='SM')
        lamb, U = sort(lamb, U)
    elif algo is 'eigsh':
        lamb, U = scipy.sparse.linalg.eigsh(L, k=k, which='SM')

    return lamb, U


def plot_spectrum(L, algo='eig'):
    """Plot the spectrum of a list of multi-scale Laplacians L."""
    # Algo is eig to be sure to get all eigenvalues.
    plt.figure(figsize=(17, 5))
    for i, lap in enumerate(L):
        lamb, U = fourier(lap, algo)
        step = 2**i
        x = range(step//2, L[0].shape[0], step)
        lb = 'L_{} spectrum in [{:1.2e}, {:1.2e}]'.format(i, lamb[0], lamb[-1])
        plt.plot(x, lamb, '.', label=lb)
    plt.legend(loc='best')
    plt.xlim(0, L[0].shape[0])
    plt.ylim(ymin=0)


def lanczos(L, X, K):
    """
    Given the graph Laplacian and a data matrix, return a data matrix which can
    be multiplied by the filter coefficients to filter X using the Lanczos
    polynomial approximation.
    """
    M, N = X.shape
    assert L.dtype == X.dtype

    def basis(L, X, K):
        """
        Lanczos algorithm which computes the orthogonal matrix V and the
        tri-diagonal matrix H.
        """
        a = np.empty((K, N), L.dtype)
        b = np.zeros((K, N), L.dtype)
        V = np.empty((K, M, N), L.dtype)
        V[0, ...] = X / np.linalg.norm(X, axis=0)
        for k in range(K-1):
            W = L.dot(V[k, ...])
            a[k, :] = np.sum(W * V[k, ...], axis=0)
            W = W - a[k, :] * V[k, ...] - (
                    b[k, :] * V[k-1, ...] if k > 0 else 0)
            b[k+1, :] = np.linalg.norm(W, axis=0)
            V[k+1, ...] = W / b[k+1, :]
        a[K-1, :] = np.sum(L.dot(V[K-1, ...]) * V[K-1, ...], axis=0)
        return V, a, b

    def diag_H(a, b, K):
        """Diagonalize the tri-diagonal H matrix."""
        H = np.zeros((K*K, N), a.dtype)
        H[:K**2:K+1, :] = a
        H[1:(K-1)*K:K+1, :] = b[1:, :]
        H.shape = (K, K, N)
        Q = np.linalg.eigh(H.T, UPLO='L')[1]
        Q = np.swapaxes(Q, 1, 2).T
        return Q

    V, a, b = basis(L, X, K)
    Q = diag_H(a, b, K)
    Xt = np.empty((K, M, N), L.dtype)
    for n in range(N):
        Xt[..., n] = Q[..., n].T.dot(V[..., n])
    Xt *= Q[0, :, np.newaxis, :]
    Xt *= np.linalg.norm(X, axis=0)
    return Xt  # Q[0, ...]


def rescale_L(L, lmax=2):
    """Rescale the Laplacian eigenvalues in [-1,1]."""
    M, M = L.shape
    I = scipy.sparse.identity(M, format='csr', dtype=L.dtype)
    L /= lmax / 2
    L -= I
    return L


def chebyshev(L, X, K):
    """Return T_k X where T_k are the Chebyshev polynomials of order up to K.
    Complexity is O(KMN)."""
    M, N = X.shape
    assert L.dtype == X.dtype

    # L = rescale_L(L, lmax)
    # Xt = T @ X: MxM @ MxN.
    Xt = np.empty((K, M, N), L.dtype)
    # Xt_0 = T_0 X = I X = X.
    Xt[0, ...] = X
    # Xt_1 = T_1 X = L X.
    if K > 1:
        Xt[1, ...] = L.dot(X)
    # Xt_k = 2 L Xt_k-1 - Xt_k-2.
    for k in range(2, K):
        Xt[k, ...] = 2 * L.dot(Xt[k-1, ...]) - Xt[k-2, ...]
    return Xt


def shape_mask(mesh):
    bcoords_img_inst, tri_index_img_inst = rasterize_barycentric_coordinate_images(mesh, [256,256])
    TI_inst = tri_index_img_inst.as_vector()
    BC_inst = bcoords_img_inst.as_vector(keep_channels=True).T
    sample_index = tri_index_img_inst.as_unmasked().sample(mesh.with_dims([0,1])).squeeze()
    shape_mask_idx = np.unique(mesh.trilist[sample_index].flatten())
    
    shape_mask_arr = np.zeros([mesh.n_points])
    shape_mask_arr[shape_mask_idx] += 1
    
    return shape_mask_arr > 0


def render_mesh(sample_mesh, trilist=None, scale=128, offset=128, shape=[256, 256], store_path=None, return_image=True, **kwargs):

        if isinstance(sample_mesh, ColouredTriMesh):
            sample_mesh = sample_mesh
        elif isinstance(sample_mesh, TriMesh):
            sample_mesh = ColouredTriMesh(
                sample_mesh.points,
                trilist=sample_mesh.trilist
            )
            sample_mesh = lambertian_shading(sample_mesh, **kwargs)
        else:
            if sample_mesh.shape[-1] != 3:
                sample_colours = sample_mesh[...,3:]
            else:
                sample_colours = np.ones_like(sample_mesh) * [0, 0, 1]

            sample_mesh = sample_mesh[...,:3]

            sample_mesh = ColouredTriMesh(
                sample_mesh * scale + offset,
                trilist=trilist,
                colours=sample_colours
            )

            sample_mesh = lambertian_shading(sample_mesh, **kwargs)

        mesh_img = rasterize_mesh(
            sample_mesh,
            shape
        )
        # mesh_img = mesh_img.rotate_ccw_about_centre(180)

        if store_path:
            if not store_path.exists():
                store_path.mkdir()

            m3io.export_mesh(sample_mesh, store_path/'{}.obj'.format(time.time()))

        if return_image:
            return mesh_img

        return mesh_img.pixels_with_channels_at_back()


def render_meshes(sample_meshes, trilist, **kwargs):

    return np.array([render_mesh(m, trilist, **kwargs) for m in sample_meshes])


def render_cmesh_cloud(cmesh, figsize=[14,14], oritation=[0,0,0], normalise=True, ax=None):
    if isinstance(cmesh, ColouredTriMesh):
        points = cmesh.points
        colours = cmesh.colours
    else:
        points = cmesh[...,:3]
        colours = cmesh[...,3:]
        
    colours = np.clip(colours, 0, 1)
    
    # normalise to unit sphere
    if normalise:
        points -= points.mean(axis=0)
        points /= points.max()
    
    zori = Homogeneous(rotation_matrix(np.deg2rad(oritation[2]), [0,0,1]))
    yori = Homogeneous(rotation_matrix(np.deg2rad(oritation[1]), [0,1,0]))
    xori = Homogeneous(rotation_matrix(np.deg2rad(oritation[0]), [1,0,0]))
    
    
    points = zori.apply(points)
    points = yori.apply(points)
    points = xori.apply(points)
    
    if not ax:
        plt.close()
        f = plt.figure(figsize=figsize)
        ax = f.add_subplot(111, projection='3d')
        
    ax.view_init(0, 0)
    # make the panes transparent
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # make the grid lines transparent
    ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

    ax.set_xlim3d(-1,1)
    ax.set_ylim3d(-1,1)
    ax.set_zlim3d(-1,1)

    ax.scatter3D(
        points[:,0],
        points[:,1], 
        points[:,2], 
        c=colours, 
        s=1
    )
    ax.axis('off')


def rotate_mesh(mesh, angle, axis=0):
    rot_v = [0 ,0 ,0]
    rot_v[axis] = 1
    
    mesh = mesh.copy()
    mesh_t = mesh.centre_of_bounds()
    mesh.points -= mesh_t
    mesh = Homogeneous(rotation_matrix(np.deg2rad(angle), rot_v)).apply(mesh)
    mesh.points += mesh_t
    
    return mesh


def recover_mesh_from_uvxyz(uvxyz, img, template_mask, trilist=None):
    mu = np.mean(uvxyz[template_mask],axis=0)
    std = np.std(uvxyz[template_mask],axis=0)
    nd = norm(mu, std)
    nd_mask = (nd.cdf(uvxyz[template_mask]) < [0.05, 0.05, 0.01]).any(axis=-1)
    plan_points = np.stack(np.meshgrid(*map(range, [256, 256])) + [np.zeros([256, 256])], axis=-1)[template_mask][~nd_mask]
    if trilist is not None:
        plan_trilist = trilist
    else:
        plan_trilist = TriMesh(plan_points[:,:2]).trilist
    masked_points = uvxyz[template_mask][~nd_mask].clip(0,1) * 256
    color_sampling = masked_points[:,:2].astype(np.uint8)
    rec_shape = ColouredTriMesh(
        masked_points * [1,1,-1], 
        trilist=plan_trilist, 
        colours=img.pixels_with_channels_at_back()[color_sampling[:,0],color_sampling[:,1],:] # np.ones_like(masked_points) * [0,0,1] #
    )
    return rec_shape