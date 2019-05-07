def LU(mat,z,copy,obj):
    """
    Returns L and U matrices of the matrix
    ***KNOWN ISSUE:Doesn't always work if determinant is 0 | linear system is inconsistant***
    ***STILL NEEDS CLEAN UP***
    """
    if not mat.isSquare:
        return (None,None,None)

    from MatricesM.C_funcs.linalg import CLU
    calcs = CLU(mat.dim,z,copy,mat._cMat)
    
    return (obj(mat.dim,calcs[0],dtype=mat.dtype),calcs[1],obj(mat.dim,calcs[2],dtype=mat.dtype))