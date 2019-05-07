####################################################################################################
# neuropythy/graphics/core.py
# Core implementation of the neuropythy graphics library for plotting cortical surfaces

import numpy               as np
import numpy.linalg        as npla
import scipy               as sp
import scipy.sparse        as sps
import scipy.spatial       as spspace
import neuropythy.geometry as geo
import neuropythy.mri      as mri
import neuropythy.io       as nyio
import os, sys, six, itertools, atexit, shutil, tempfile, warnings, pimms

from ..util            import (times, zdivide, plus, minus, to_hemi_str)
from ..vision          import (visual_area_names, visual_area_numbers)

# 2D Graphics ######################################################################################

# Below are various graphics-related functions; some are wrapped in a try block in case matplotlib
# is not installed.
def _matplotlib_load_error(*args, **kwargs):
    raise RuntimeError('load failure: the requested object could not be loaded, probably because ' +
                       'you do not have matplotlib installed correctly')
cmap_curvature = _matplotlib_load_error
cmap_polar_angle_sym = _matplotlib_load_error
cmap_polar_angle_lh = _matplotlib_load_error
cmap_polar_angle_rh = _matplotlib_load_error
cmap_polar_angle = _matplotlib_load_error
cmap_theta_sym = _matplotlib_load_error
cmap_theta_lh = _matplotlib_load_error
cmap_theta_rh = _matplotlib_load_error
cmap_theta = _matplotlib_load_error
cmap_eccentricity = _matplotlib_load_error
cmap_log_eccentricity = _matplotlib_load_error
cmap_radius = _matplotlib_load_error
cmap_log_radius = _matplotlib_load_error
cmap_log_cmag = _matplotlib_load_error

try:
    import matplotlib, matplotlib.pyplot, matplotlib.tri, matplotlib.colors
    # we use this below
    blend_cmap = matplotlib.colors.LinearSegmentedColormap.from_list
    
    cmap_curvature = matplotlib.colors.LinearSegmentedColormap(
        'curv',
        {name: ((0.0, 0.0, 0.5), (0.5, 0.5, 0.2), (1.0, 0.2, 0.0))
         for name in ['red', 'green', 'blue']})
    cmap_curvature.__doc__ = '''
    cmap_curvature is a colormap for plotting the curvature of a vertex; note that this colormap
    assumes FreeSurfer's standard way of storing curvature where negative values indicate gyri and
    positive values indicate sulci.
    Values passed to cmap_curvature should be scaled such that (-1,1) -> (0,1).
    '''
    
    cmap_polar_angle_sym = blend_cmap(
        'polar_angle_sym',
        [(0.5,0,0), (1,1,0), (0,0.5,0), (0,1,1), (0,0,0.5), (0,1,1), (0,0.5,0), (1,1,0), (0.5,0,0)])
    cmap_polar_angle_sym.__doc__ = '''
    cmap_polar_angle_sym is a colormap for plotting the pRF polar angle of a vertex.
    Values passed to cmap_polar_angle_sym should be scaled such that (-180,180 deg) -> (0,1).

    cmap_polar_angle_sym is a circular colormap that is left-right symmetric with green representing
    the horizontal meridian, blue representing the upper vertical meridian, and red representing the
    lower vertical meridian.
    '''
    cmap_polar_angle_lh = blend_cmap(
        'polar_angle_lh',
        [(0.5,0,0), (0.75,0,0.5), (1,0,1), (0.5,0,0.75), (0,0,0.5), (0,1,1), (0,0.5,0), (1,1,0),
         (0.5,0,0)])
    cmap_polar_angle_lh.__doc__ = '''
    cmap_polar_angle_lh is a colormap for plotting the pRF polar angle of a vertex.
    Values passed to cmap_polar_angle_lh should be scaled such that (-180,180 deg) -> (0,1).

    cmap_polar_angle_lh is a circular colormap that emphasizes colors in the right visual field; the
    left visual field appears mostly magenta.
    '''
    cmap_polar_angle_rh = blend_cmap(
        'polar_angle_rh',
        [(0.5,0,0), (1,1,0), (0,0.5,0), (0,1,1), (0,0,0.5), (0.5,0,0.75), (1,0,1), (0.75,0,0.5),
         (0.5,0,0)])
    cmap_polar_angle_rh.__doc__ = '''
    cmap_polar_angle_rh is a colormap for plotting the pRF polar angle of a vertex.
    Values passed to cmap_polar_angle_rh should be scaled such that (-180,180 deg) -> (0,1).

    cmap_polar_angle_rh is a circular colormap that emphasizes colors in the left visual field; the
    right visual field appears mostly magenta.
    '''
    cmap_polar_angle = blend_cmap(
        'polar_angle',
         [(0.5,0,0), (1,0,1), (0,0,0.5), (0,1,1), (0,0.5,0), (1,1,0), (0.5,0,0)])
    cmap_polar_angle.__doc__ = '''
    cmap_polar_angle is a colormap for plotting the pRF polar angle of a vertex.
    Values passed to cmap_polar_angle should be scaled such that (-180,180 deg) -> (0,1).

    cmap_polar_angle is a 6-pronged circular colormap; note that it does not have dark or bright
    values at the horizontal meridia as cmap_polar_angle_sym, cmap_polar_angle_lh, and
    cmap_polar_angle_rh do.
    '''
    cmap_theta_sym = blend_cmap(
        'theta_sym',
        [(0.5,0,0), (1,1,0), (0,0.5,0), (0,1,1), (0,0,0.5), (0,1,1), (0,0.5,0), (1,1,0), (0.5,0,0)])
    cmap_theta_sym.__doc__ = '''
    cmap_theta_sym is a colormap for plotting the pRF theta of a vertex.
    Values passed to cmap_theta_sym should be scaled such that (-pi,pi rad) -> (0,1). Note that 0 is
    the right right horizontal meridian and positive is the counter-clockwise direction.

    cmap_theta_sym is a circular colormap that is left-right symmetric with green representing
    the horizontal meridian, blue representing the upper vertical meridian, and red representing the
    lower vertical meridian.
    '''
    cmap_theta_lh = blend_cmap(
        'theta_lh',
        [(0.5,0,0), (1,1,0), (0,0.5,0), (0,1,1), (0,0,0.5),
         (0.5,0,0.75), (1,0,1), (0.75,0,0.5), (0.5,0,0)])
    cmap_theta_lh.__doc__ = '''
    cmap_theta_lh is a colormap for plotting the pRF theta of a vertex.
    Values passed to cmap_theta_lh should be scaled such that (-pi,pi rad) -> (0,1). Note that 0 is
    the right right horizontal meridian and positive is the counter-clockwise direction.

    cmap_theta_lh is a circular colormap that emphasizes colors in the right visual field; the
    left visual field appears mostly magenta.
    '''
    cmap_theta_rh = blend_cmap(
        'theta_rh',
        [(0.5,0,0), (0.75,0,0.5), (0.5,0,0.75), (1,0,1),
         (0,0,0.5), (0,1,1), (0,0.5,0), (1,1,0), (0.5,0,0)])
    cmap_theta_rh.__doc__ = '''
    cmap_theta_rh is a colormap for plotting the pRF theta of a vertex.
    Values passed to cmap_theta_rh should be scaled such that (-pi,pi rad) -> (0,1). Note that 0 is
    the right right horizontal meridian and positive is the counter-clockwise direction.

    cmap_theta_rh is a circular colormap that emphasizes colors in the left visual field; the
    right visual field appears mostly magenta.
    '''
    cmap_theta = blend_cmap(
        'theta',
        [(0,       cmap_polar_angle(0.25)),
         ( 1.0/12, (  1,  0,  1)),
         ( 3.0/12, (0.5,  0,  0)),
         ( 5.0/12, (  1,  1,  0)),
         ( 7.0/12, (  0,0.5,  0)),
         ( 9.0/12, (  0,  1,  1)),
         (11.0/12, (  0,  0,0.5)),
         (1,       cmap_polar_angle(0.25))])
    cmap_theta.__doc__ = '''
    cmap_theta is a colormap for plotting the pRF theta of a vertex.
    Values passed to cmap_theta should be scaled such that (-pi,pi rad) -> (0,1). Note that 0 is the
    right right horizontal meridian and positive is the counter-clockwise direction.

    cmap_theta is a 6-pronged circular colormap; note that it does not have dark or bright
    values at the horizontal meridia as cmap_theta_sym, cmap_theta_lh, and
    cmap_theta_rh do.
    '''
    cmap_eccentricity = blend_cmap(
        'eccentricity',
        [(0,       (  0,  0,  0)),
         (1.25/90, (  0,  0,0.5)),
         (2.5/90,  (  1,  0,  1)),
         (5.0/90,  (0.5,  0,  0)),
         (10.0/90, (  1,  1,  0)),
         (20.0/90, (  0,0.5,  0)),
         (40.0/90, (  0,  1,  1)),
         (1,       (  1,  1,  1))])
    cmap_eccentricity.__doc__ = '''
    cmap_eccentricity is a colormap for plotting the pRF eccentricity of a vertex.
    Values passed to cmap_eccentricity should be scaled such that (0,90 deg) -> (0,1).
    '''
    cmap_log_eccentricity = blend_cmap(
        'log_eccentricity',
        [(0,     (  0,  0,  0)),
         (1.0/7, (  0,  0,0.5)),
         (2.0/7, (  1,  0,  1)),
         (3.0/7, (0.5,  0,  0)),
         (4.0/7, (  1,  1,  0)),
         (5.0/7, (  0,0.5,  0)),
         (6.0/7, (  0,  1,  1)),
         (1,     (  1,  1,  1))])
    cmap_log_eccentricity.__doc__ = '''
    cmap_log_eccentricity is a colormap for plotting the log of eccentricity.
    Values passed to cmap_log_cmag should be scaled however desired, but note that the colormap
    itself runs linearly from 0 to 1, so eccentricity data should be log-transformed
    then scaled before being passed.
    '''
    cmap_radius = blend_cmap(
        'radius',
        [(0,       (  0,  0,  0)),
         (1.25/30, (  0,  0,0.5)),
         (2.5/30,  (  1,  0,  1)),
         (5.0/30,  (0.5,  0,  0)),
         (10.0/30, (  1,  1,  0)),
         (20.0/30, (  0,0.5,  0)),
         (40.0/30, (  0,  1,  1)),
         (1,       (  1,  1,  1))])
    cmap_radius.__doc__ = '''
    cmap_radius is a colormap for plotting the pRF radius (sigma) of a vertex.
    Values passed to cmap_radius should be scaled such that (0,30 deg) -> (0,1).
    '''
    cmap_log_radius = blend_cmap(
        'log_radius',
        [(0,     (  0,  0,  0)),
         (1.0/7, (  0,  0,0.5)),
         (2.0/7, (  1,  0,  1)),
         (3.0/7, (0.5,  0,  0)),
         (4.0/7, (  1,  1,  0)),
         (5.0/7, (  0,0.5,  0)),
         (6.0/7, (  0,  1,  1)),
         (1,     (  1,  1,  1))])
    cmap_log_radius.__doc__ = '''
    cmap_log_radius is a colormap for plotting the log of radius.
    Values passed to cmap_log_cmag should be scaled however desired, but note that the colormap
    itself runs linearly from 0 to 1, so radius data should be log-transformed then scaled before
    being passed.
    '''
    cmap_log_cmag = blend_cmap(
        'log_cmag',
        [(0,     (  0,  0,  0)),
         (1.0/7, (  0,  0,0.5)),
         (2.0/7, (  1,  0,  1)),
         (3.0/7, (0.5,  0,  0)),
         (4.0/7, (  1,  1,  0)),
         (5.0/7, (  0,0.5,  0)),
         (6.0/7, (  0,  1,  1)),
         (1,     (  1,  1,  1))])
    cmap_log_cmag.__doc__ = '''
    cmap_log_cmag is a colormap for plotting the log of cortical magnification.
    Values passed to cmap_log_cmag should be scaled however desired, but note that the colormap
    itself runs linearly from 0 to 1, so cortical magnification data should be log-transformed
    then scaled before being passed.
    '''

    colormaps = {
        'curvature':        (cmap_curvature,        (-1,1)),
        'polar_angle_sym':  (cmap_polar_angle_sym,  (-180,180)),
        'polar_angle_lh':   (cmap_polar_angle_lh,   (-180,180)),
        'polar_angle_rh':   (cmap_polar_angle_rh,   (-180,180)),
        'polar_angle':      (cmap_polar_angle,      (-180,180)),
        'theta_sym':        (cmap_theta_sym,        (-np.pi,np.pi)),
        'theta_lh':         (cmap_theta_lh,         (-np.pi,np.pi)),
        'theta_rh':         (cmap_theta_rh,         (-np.pi,np.pi)),
        'theta':            (cmap_theta,            (-np.pi,np.pi)),
        'eccentricity':     (cmap_eccentricity,     (0,90)),
        'log_eccentricity': (cmap_log_eccentricity, (np.log(0.5), np.log(90.0))),
        'radius':           (cmap_radius,           (0, 40)), 
        'log_radius':       (cmap_log_radius,       (np.log(0.25), np.log(40.0))),
        'log_cmag':         (cmap_log_cmag,         (np.log(0.5), np.log(32.0)))}
    for (k,(cmap,_)) in six.iteritems(colormaps): matplotlib.cm.register_cmap(k, cmap)
except Exception: pass

def to_rgba(val):
    '''
    to_rgba(val) is identical to matplotlib.colors.to_rgba(val) except that it operates over lists
      as well as individual elements to yield matrices of rgba values. In addition, it always yields
      numpy vectors or matrices.
    '''
    if pimms.is_npmatrix(val) and val.shape[1] == 4: return val
    try: return np.asarray(matplotlib.colors.to_rgba(val))
    except Exception: return np.asarray([matplotlib.colors.to_rgba(u) for u in val])
def color_overlap(color1, *args):
    '''
    color_overlap(color1, color2...) yields the rgba value associated with overlaying color2 on top
      of color1 followed by any additional colors (overlaid left to right). This respects alpha
      values when calculating the results.
    Note that colors may be lists of colors, in which case a matrix of RGBA values is yielded.
    '''
    args = list(args)
    args.insert(0, color1)
    rgba = np.asarray([0.5,0.5,0.5,0])
    for c in args:
        c = to_rgba(c)
        a = c[...,3]
        a0 = rgba[...,3]
        if   np.isclose(a0, 0).all(): rgba = np.ones(rgba.shape) * c
        elif np.isclose(a,  0).all(): continue
        else:                         rgba = times(a, c) + times(1-a, rgba)
    return rgba

_vertex_angle_empirical_prefixes = ['prf_', 'measured_', 'empiirical_']
_vertex_angle_model_prefixes = ['model_', 'predicted_', 'inferred_', 'template_', 'atlas_',
                                'benson14_', 'benson17_']
_vertex_angle_prefixes = ([''] + _vertex_angle_model_prefixes + _vertex_angle_model_prefixes)

def vertex_curvature_color(m):
    return [0.2,0.2,0.2,1.0] if m['curvature'] > -0.025 else [0.7,0.7,0.7,1.0]
def vertex_prop(m, property=None):
    if property is None or property is Ellipsis: return None
    elif pimms.is_vector(property): return property
    elif pimms.is_number(property): return property
    elif not pimms.is_str(property): raise ValueError('argument is not property-like: %s'%property)
    elif property in m: return m[property]
    else: return None
def vertex_weight(m, property=None):
    p = vertex_prop(m, property)
    if p is None:
        return next((m[k]
                     for name in ['weight', 'variance_explained']
                     for pref in ([''] + _vertex_angle_empirical_prefixes)
                     for k in [pref + name]
                     if k in m),
                    1.0)
    return p
def vertex_angle(m, property=None):
    p = vertex_prop(m, property)
    if p is None:
        ang0 = next((m[kk] for k in _vertex_angle_prefixes for kk in [k+'polar_angle'] if kk in m),
                    None)
        if ang0 is not None: return ang0
        ang0 = next((m[kk]
                     for name in ['angle', 'theta']
                     for k in _vertex_angle_prefixes for kk in [k + name]
                     if kk in m),
                    None)
        if ang0 is not None:
            return np.mod(90.0 - 180.0/np.pi*ang0 + 180, 360) - 180
        return None
    return p
def vertex_eccen(m, property=None):
    p = vertex_prop(m, property)
    if p is None:
        ecc0 = next((m[k]
                     for kk in _vertex_angle_prefixes
                     for k in [kk + 'eccentricity']
                     if k in m),
                    None)
        if ecc0 is not None: return ecc0
        ecc0 = next((m[k]
                     for kk in _vertex_angle_prefixes
                     for k in [kk + 'rho']
                     if k in m),
                    None)
        if ecc0 is not None:
            return 180.0/np.pi*ecc0
        return None
    return p
def vertex_sigma(m, property=None):
    p = vertex_prop(m, property)
    if p is not None: return p
    return next((m[k]
                 for kk in _vertex_angle_prefixes
                 for nm in ['sigma', 'radius', 'size']
                 for k in [kk + nm]
                 if k in m),
                None)
def vertex_varea(m, property=None):
    p = vertex_prop(m, property)
    if p is not None: return p
    return next((m[k]
                 for kk in _vertex_angle_prefixes
                 for nm in ['visual_area', 'varea', 'label']
                 for k in [kk + nm]
                 if k in m),
                None)
def vertex_angle_color(m, weight_min=0.2, weighted=True, hemi=None, property=Ellipsis,
                       weight=Ellipsis, null_color='curvature'):
    if m is Ellipsis:
        kw0 = {'weight_min':weight_min, 'weighted':weighted, 'hemi':hemi,
               'property':property, 'weight':weight, 'null_color':null_color}
        def _pass_fn(x, **kwargs):
            return vertex_angle_color(x, **{k:(kwargs[k] if k in kwargs else kw0[k])
                                            for k in list(set(kwargs.keys() + kw0.keys()))})
        return _pass_fn
    if isinstance(null_color, basestring):
        null_color = null_color.lower()
        if null_color == 'curvature' or null_color == 'curv':
            nullColor = np.asarray(vertex_curvature_color(m))
        else:
            raise ValueError('bad null color: %s' % null_color)
    else:
        nullColor = np.asarray(null_color)
    ang = vertex_angle(m, property)
    if ang is None: return nullColor
    if isinstance(hemi, basestring):
        hemi = hemi.lower()
        if hemi == 'lh' or hemi == 'left':
            ang = ang
        elif hemi == 'rh' or hemi == 'right':
            ang = -ang
        elif hemi == 'abs':
            ang = np.abs(ang)
        else: raise ValueError('bad hemi argument: %s' % hemi)
    w = vertex_weight(m, property=weight) if weighted else None
    if weighted and (not pimms.is_number(w) or w < weight_min):
        return nullColor
    angColor = np.asarray(cmap_polar_angle_sym((ang + 180.0) / 360.0))
    if weighted:
        return angColor*w + nullColor*(1-w)
    else:
        return angColor
def vertex_eccen_color(m, weight_min=0.1, weighted=True, hemi=None,
                       property=Ellipsis, null_color='curvature', weight=Ellipsis):
    if m is Ellipsis:
        kw0 = {'weight_min':weight_min, 'weighted':weighted, 'hemi':hemi,
               'property':property, 'weight':weight, 'null_color':null_color}
        def _pass_fn(x, **kwargs):
            return vertex_eccen_color(x, **{k:(kwargs[k] if k in kwargs else kw0[k])
                                            for k in list(set(kwargs.keys() + kw0.keys()))})
        return _pass_fn
    if isinstance(null_color, basestring):
        null_color = null_color.lower()
        if null_color == 'curvature' or null_color == 'curv':
            nullColor = np.asarray(vertex_curvature_color(m))
        else:
            raise ValueError('bad null color: %s' % null_color)
    else:
        nullColor = np.asarray(null_color)
    ecc = vertex_eccen(m, property)
    if ecc is None: return nullColor
    w = vertex_weight(m, property=weight) if weighted else None
    if weighted and (not pimms.is_number(w) or w < weight_min):
        return nullColor
    eccColor = np.asarray(cmap_eccentricity((ecc if 0 < ecc < 90 else 0 if ecc < 0 else 90)/90.0))
    if weighted:
        return eccColor*w + nullColor*(1-w)
    else:
        return eccColor
def vertex_sigma_color(m, weight_min=0.1, weighted=True, hemi=None,
                       property=Ellipsis, null_color='curvature', weight=Ellipsis):
    if m is Ellipsis:
        kw0 = {'weight_min':weight_min, 'weighted':weighted, 'hemi':hemi,
               'property':property, 'weight':weight, 'null_color':null_color}
        def _pass_fn(x, **kwargs):
            return vertex_sigma_color(x, **{k:(kwargs[k] if k in kwargs else kw0[k])
                                            for k in list(set(kwargs.keys() + kw0.keys()))})
        return _pass_fn
    if isinstance(null_color, basestring):
        null_color = null_color.lower()
        if null_color == 'curvature' or null_color == 'curv':
            nullColor = np.asarray(vertex_curvature_color(m))
        else:
            raise ValueError('bad null color: %s' % null_color)
    else:
        nullColor = np.asarray(null_color)
    sig = vertex_sigma(m, property)
    if sig is None: return nullColor
    w = vertex_weight(m, property=weight) if weighted else None
    if weighted and (not pimms.is_number(w) or w < weight_min):
        return nullColor
    sigColor = np.asarray(cmap_radius(sig/30.0))
    if weighted:
        return sigColor*w + nullColor*(1-w)
    else:
        return sigColor
_varea_colors = {'V1': (1,0,0), 'V2': (0,1,0),    'V3': (0,0,1),
                 'hV4':(0,1,1), 'VO1':(0,0.5,1), 'VO2':(0,1,0.5),
                 'LO1':(1,0,1), 'LO2':(0.5,0,1), 'TO1':(1,0,0.5), 'TO2':(0.5,0,0.5),
                 'V3a':(1,1,0), 'V3a':(0.5,1,0)}
def vertex_varea_color(m, property=Ellipsis, null_color='curvature', hemi=None,
                       weight=Ellipsis, weight_min=0.1, weighted=False):
    if m is Ellipsis:
        kw0 = {'weight_min':weight_min, 'weighted':weighted, 'hemi':hemi,
               'property':property, 'weight':weight, 'null_color':null_color}
        def _pass_fn(x, **kwargs):
            return vertex_varea_color(x, **{k:(kwargs[k] if k in kwargs else kw0[k])
                                            for k in list(set(kwargs.keys() + kw0.keys()))})
        return _pass_fn
    if isinstance(null_color, basestring):
        null_color = null_color.lower()
        if null_color == 'curvature' or null_color == 'curv':
            nullColor = np.asarray(vertex_curvature_color(m))
        else:
            raise ValueError('bad null color: %s' % null_color)
    else:
        nullColor = np.asarray(null_color)
    lbl = vertex_varea(m, property)
    if lbl is None or lbl == 0: return nullColor
    w = vertex_weight(m, property=weight) if weighted else None
    if weighted and (not pimms.is_number(w) or w < weight_min):
        return nullColor
    if not pimms.is_str(lbl):
        lbl = None if lbl is None or lbl < 0 or lbl > len(visual_area_names) else \
              visual_area_names[lbl]
    lblColor = np.asarray(_varea_colors.get(lbl, None))
    if lblColor is None: return nullColor
    if weighted: return lblColor*w + nullColor*(1-w)
    else:        return lblColor
def curvature_colors(m):
    '''
    curvature_colors(m) yields an array of curvature colors for the vertices of the given
      property-bearing object m.
    '''
    return np.asarray(m.map(vertex_curvature_color))
def retino_colors(vcolorfn, *args, **kwargs):
    'See eccen_colors, angle_colors, sigma_colors, and varea_colors.'
    if len(args) == 0:
        def _retino_color_pass(*args, **new_kwargs):
            return retino_colors(vcolorfn, *args,
                                 **{k:(new_kwargs[k] if k in new_kwargs else kwargs[k])
                                    for k in set(kwargs.keys() + new_kwargs.keys())})
        return _retino_color_pass
    elif len(args) > 1:
        raise ValueError('retinotopy color functions accepts at most one argument')
    m = args[0]
    # we need to handle the arguments
    if isinstance(m, (geo.VertexSet, pimms.ITable)):
        tbl = m.properties if isinstance(m, geo.VertexSet) else m
        n = tbl.row_count
        # if the weight or property arguments are lists, we need to thread these along
        if 'property' in kwargs:
            props = kwargs['property']
            del kwargs['property']
            if not (pimms.is_vector(props) or pimms.is_matrix(props)):
                props = [props for _ in range(n)]
        else: props = None
        if 'weight' in kwargs:
            ws = kwargs['weight']
            del kwargs['weight']
            if not pimms.is_vector(ws) and not pimms.is_matrix(ws): ws = [ws for _ in range(n)]
        else: ws = None
        vcolorfn0 = vcolorfn(Ellipsis, **kwargs) if len(kwargs) > 0 else vcolorfn
        if props is None and ws is None: vcfn = lambda m,k:vcolorfn0(m)
        elif props is None:              vcfn = lambda m,k:vcolorfn0(m, weight=ws[k])
        elif ws is None:                 vcfn = lambda m,k:vcolorfn0(m, property=props[k])
        else: vcfn = lambda m,k:vcolorfn0(m, property=props[k], weight=ws[k])
        return np.asarray([vcfn(r,kk) for (kk,r) in enumerate(tbl.rows)])
    else:
        return vcolorfn(m, **kwargs)
def angle_colors(*args, **kwargs):
    '''
    angle_colors(obj) yields an array of colors for the polar angle map of the given
      property-bearing object (cortex, tesselation, mesh).
    angle_colors(dict) yields an array of the color for the particular vertex property
      mapping that is given as dict.
    angle_colors() yields a functor version of angle_colors that can be called with one of the
      above arguments; note that this is useful precisely because the returned function
      preserves the arguments passed; e.g. angle_colors(weighted=False)(mesh) is equivalent to
      angle_colors(mesh, weighted=False).

    The following options are accepted:
      * weighted (True) specifies whether to use weight as opacity.
      * weight_min (0.2) specifies that below this weight value, the curvature (or null color)
        should be plotted.
      * property (Ellipsis) specifies the specific property that should be used as the
        eccentricity value; if Ellipsis, will attempt to auto-detect this value.
      * weight (Ellipsis) specifies  the specific property that should be used as the weight value.
      * null_color ('curvature') specifies a color that should be used as the background.
    '''
    return retino_colors(vertex_angle_color, *args, **kwargs)
def eccen_colors(*args, **kwargs):
    '''
    eccen_colors(obj) yields an array of colors for the eccentricity map of the given
      property-bearing object (cortex, tesselation, mesh).
    eccen_colors(dict) yields an array of the color for the particular vertex property mapping
      that is given as dict.
    eccen_colors() yields a functor version of eccen_colors that can be called with one of the
      above arguments; note that this is useful precisely because the returned function
      preserves the arguments passed; e.g. eccen_colors(weighted=False)(mesh) is equivalent to
      eccen_colors(mesh, weighted=False).

    The following options are accepted:
      * weighted (True) specifies whether to use weight as opacity.
      * weight_min (0.2) specifies that below this weight value, the curvature (or null color)
        should be plotted.
      * property (Ellipsis) specifies the specific property that should be used as the
        eccentricity value; if Ellipsis, will attempt to auto-detect this value.
      * weight (Ellipsis) specifies  the specific property that should be used as the weight value.
      * null_color ('curvature') specifies a color that should be used as the background.
    '''
    return retino_colors(vertex_eccen_color, *args, **kwargs)
def sigma_colors(*args, **kwargs):
    '''
    sigma_colors(obj) yields an array of colors for the pRF-radius map of the given
      property-bearing object (cortex, tesselation, mesh).
    sigma_colors(dict) yields an array of the color for the particular vertex property mapping
      that is given as dict.
    sigma_colors() yields a functor version of sigma_colors that can be called with one of the
      above arguments; note that this is useful precisely because the returned function
      preserves the arguments passed; e.g. sigma_colors(weighted=False)(mesh) is equivalent to
      sigma_colors(mesh, weighted=False).

    The following options are accepted:
      * weighted (True) specifies whether to use weight as opacity.
      * weight_min (0.2) specifies that below this weight value, the curvature (or null color)
        should be plotted.
      * property (Ellipsis) specifies the specific property that should be used as the
        eccentricity value; if Ellipsis, will attempt to auto-detect this value.
      * weight (Ellipsis) specifies  the specific property that should be used as the weight value.
      * null_color ('curvature') specifies a color that should be used as the background.
    '''
    return retino_colors(vertex_sigma_color, *args, **kwargs)
def varea_colors(*args, **kwargs):
    '''
    varea_colors(obj) yields an array of colors for the visual area map of the given
      property-bearing object (cortex, tesselation, mesh).
    varea_colors(dict) yields an array of the color for the particular vertex property mapping
      that is given as dict.
    varea_colors() yields a functor version of varea_colors that can be called with one of the
      above arguments; note that this is useful precisely because the returned function
      preserves the arguments passed; e.g. varea_colors(weighted=False)(mesh) is equivalent to
      varea_colors(mesh, weighted=False).

    The following options are accepted:
      * weighted (True) specifies whether to use weight as opacity.
      * weight_min (0.2) specifies that below this weight value, the curvature (or null color)
        should be plotted.
      * property (Ellipsis) specifies the specific property that should be used as the
        eccentricity value; if Ellipsis, will attempt to auto-detect this value.
      * weight (Ellipsis) specifies  the specific property that should be used as the weight value.
      * null_color ('curvature') specifies a color that should be used as the background.
    '''
    return retino_colors(vertex_varea_color, *args, **kwargs)
def colors_to_cmap(colors):
    colors = np.asarray(colors)
    if len(colors.shape) == 1: return colors_to_cmap([colors])[0]
    if colors.shape[1] == 3:
        colors = np.hstack((colors, np.ones((len(colors),1))))
    steps = (0.5 + np.asarray(range(len(colors)-1), dtype=np.float))/(len(colors) - 1)
    return matplotlib.colors.LinearSegmentedColormap(
        'auto_cmap',
        {clrname: ([(0, col[0], col[0])] +
                   [(step, c0, c1) for (step,c0,c1) in zip(steps, col[:-1], col[1:])] +
                   [(1, col[-1], col[-1])])
         for (clridx,clrname) in enumerate(['red', 'green', 'blue', 'alpha'])
         for col in [colors[:,clridx]]},
        N=(len(colors)))
def guess_cortex_cmap(pname):
    '''
    guess_cortex_cmap(proptery_name) yields a tuple (cmap, (vmin, vmax)) of a cortical color map
      appropriate to the given property name and the suggested value scaling for the cmap. If the
      given property is not a string or is not recognized then the log_eccentricity axis is used
      and the suggested vmin and vmax are None.
    '''
    if not pimms.is_str(pname): return (log_eccentricity, None, None)
    if pname in colormaps: return colormaps[pname]
    # check each manually
    for (k,v) in six.iteritems(colormaps):
        if pname.endswith(k): return v
    for (k,v) in six.iteritems(colormaps):
        if pname.startswith(k): return v
    return (log_eccentricity, None, None)
def apply_cmap(zs, cmap, vmin=None, vmax=None):
    '''
    apply_cmap(z, cmap) applies the given cmap to the values in z; if vmin and/or vmad are passed,
      they are used to scale z.
    '''
    if vmin is None: vmin = np.min(zs)
    if vmax is None: vmax = np.max(zs)
    if pimms.is_str(cmap): cmap = matplotlib.cm.get_cmap(cmap)
    return cmap((zs - vmin) / (vmax - vmin))

def cortex_cmap_plot_2D(the_map, zs, cmap, vmin=None, vmax=None, axes=None, triangulation=None):
    '''
    cortex_cmap_plot_2D(map, zs, cmap, axes) plots the given cortical map values zs on the given
      axes using the given given color map and yields the resulting polygon collection object.
    cortex_cmap_plot_2D(map, zs, cmap) uses matplotlib.pyplot.gca() for the axes.

    The following options may be passed:
      * triangulation (None) may specify the triangularion object for the mesh if it has already
        been created; otherwise it is generated fresh.
      * axes (None) specify the axes on which to plot; if None, then matplotlib.pyplot.gca() is
        used. If Ellipsis, then a tuple (triangulation, z, cmap) is returned; to recreate the plot,
        one would call:
          axes.tripcolor(triangulation, z, cmap, shading='gouraud', vmin=vmin, vmax=vmax)
      * vmin (default: None) specifies the minimum value for scaling the property when one is passed
        as the color option. None means to use the min value of the property.
      * vmax (default: None) specifies the maximum value for scaling the property when one is passed
        as the color option. None means to use the max value of the property.
    '''
    if triangulation is None:
        triangulation = matplotlib.tri.Triangulation(the_map.coordinates[0], the_map.coordinates[1],
                                                     triangles=the_map.tess.indexed_faces.T)
    if axes is Ellipsis: return (triangulation, zs, cmap)
    return axes.tripcolor(triangulation, zs, cmap=cmap, shading='gouraud', vmin=vmin, vmax=vmax)
def cortex_rgba_plot_2D(the_map, rgba, axes=None, triangulation=None):
    '''
    cortex_rgba_plot_2D(map, rgba, axes) plots the given cortical map on the given axes using the
      given (n x 4) matrix of vertex colors and yields the resulting polygon collection object.
    cortex_rgba_plot_2D(map, rgba) uses matplotlib.pyplot.gca() for the axes.

    The option triangulation may also be passed if the triangularion object has already been
    created; otherwise it is generated fresh.
    '''
    cmap = colors_to_cmap(rgba)
    zs = np.linspace(0.0, 1.0, the_map.vertex_count)
    return cortex_cmap_plot_2D(the_map, zs, cmap, axes=axes, triangulation=triangulation)
def cortex_plot_colors(the_map,
                       color=None, cmap=None, vmin=None, vmax=None, alpha=None,
                       underlay='curvature', mask=None):
    '''
    cortex_plot_colors(mesh, opts...) yields the cortex colors as a matrix of RGBA rows for the
      given mesh and options. 

    The following options are accepted:
      * color (default: None) specifies the color to plot for each vertex; this argument may take a
        number of forms:
          * None, do not plot a color over the underlay (the default)
          * a matrix of RGB or RGBA values, one per vertex
          * a property vector or a string naming a property, in which case the cmap, vmin, and vmax
            arguments are used to generate colors
          * a function that, when passed a single argument, a dict of the properties of a single
            vertex, yields an RGB or RGBA list for that vertex.
      * cmap (default: 'log_eccentricity') specifies the colormap to use in plotting if the color
        argument provided is a property.
      * vmin (default: None) specifies the minimum value for scaling the property when one is passed
        as the color option. None means to use the min value of the property.
      * vmax (default: None) specifies the maximum value for scaling the property when one is passed
        as the color option. None means to use the max value of the property.
      * underlay (default: 'curvature') specifies the default underlay color to plot for the
        cortical surface; it may be None, 'curvature', or a color.
      * alpha (default None) specifies the alpha values to use for the color plot. If None, then
        leaves the alpha values from color unchanged. If a single number, then all alpha values in
        color are multiplied by that value. If a list of values, one per vertex, then this vector
        is multiplied by the alpha values. Finally, any negative value is set instead of multiplied.
        So, for example, if there were 3 vertices with:
          * color = ((0,0,0,1), (0,0,1,0.5), (0,0,0.75,0,8))
          * alpha = (-0.5, 1, 0.5)
        then the resulting colors plotted will be ((0,0,0,0.5), (0,0,1,0.5), (0,0,0.75,0,4)).
      * mask (default: None) specifies a mask to use for the mesh; this is passed through to_mask()
        to figure out the masking. Those vertices not in the mask are not plotted (but they will be
        plotted in the underlay if it is not None).
    '''
    # okay, let's interpret the color
    if color is None:
        color = np.full((the_map.vertex_count, 4), 0.5)
        color[:,3] = 0
    try:
        clr = matplotlib.colors.to_rgba(color)
        # This is an rgb color to plot...
        color = np.ones((the_map.vertex_count,4)) * matplotlib.colors.to_rgba(clr)
    except Exception: pass
    if pimms.is_vector(color) or pimms.is_str(color):
        # it's a property that gets interpreted via the colormap
        p = the_map.property(color)
        # if the colormap is none, we can try to guess it
        if cmap is None:
            (cmap,(vmn,vmx)) = guess_cortex_cmap(color)
            if vmin is None: vmin = vmn
            if vmax is None: vmax = vmx
        color = apply_cmap(p, cmap, vmin=vmin, vmax=vmax)
    if not pimms.is_matrix(color):
        # must be a function; let's try it...
        color = to_rgba(the_map.map(color))
    color = np.array(color)
    if color.shape[1] != 4: color = np.hstack([color, np.ones([color.shape[0], 1])])
    # okay, and the underlay...
    if underlay is not None:
        if pimms.is_str(underlay) and underlay.lower() in ['curvature', 'curv']:
            underlay = apply_cmap(the_map.prop('curvature'), cmap_curvature, vmin=-1, vmax=1)
        else:
            try: underlay = np.ones((the_map.vertex_count, 4)) * to_rgba(underlay)
            except Exception: raise ValueError('plot underlay failed: must be a color or curvature')
    # okay, let's check on alpha...
    if alpha is not None:
        if pimms.is_number(alpha): alpha = np.full(color.shape[0], alpha)
        else: alpha = the_map.property(alpha)
        color[:,3] *= alpha
        neg = (alpha < 0)
        color[neg,3] = -alpha[neg]
    alpha = color[:,3]
    # and the mask...
    if mask is not None:
        ii = the_map.mask(mask, indices=True)
        tmp = np.zeros(len(color))
        tmp[ii] = color[ii,3]
        color[:,3] = tmp
    # then, blend with the underlay if need be
    if underlay is not None:
        color = color_overlap(underlay, color)
    return color

def cortex_plot_2D(the_map,
                   color=None, cmap=None, vmin=None, vmax=None, alpha=None,
                   underlay='curvature', mask=None, axes=None, triangulation=None):
    '''
    cortex_plot_2D(map) yields a plot of the given 2D cortical mesh, map.

    The following options are accepted:
      * color (default: None) specifies the color to plot for each vertex; this argument may take a
        number of forms:
          * None, do not plot a color over the underlay (the default)
          * a matrix of RGB or RGBA values, one per vertex
          * a property vector or a string naming a property, in which case the cmap, vmin, and vmax
            arguments are used to generate colors
          * a function that, when passed a single argument, a dict of the properties of a single
            vertex, yields an RGB or RGBA list for that vertex.
      * cmap (default: 'log_eccentricity') specifies the colormap to use in plotting if the color
        argument provided is a property.
      * vmin (default: None) specifies the minimum value for scaling the property when one is passed
        as the color option. None means to use the min value of the property.
      * vmax (default: None) specifies the maximum value for scaling the property when one is passed
        as the color option. None means to use the max value of the property.
      * underlay (default: 'curvature') specifies the default underlay color to plot for the
        cortical surface; it may be None, 'curvature', or a color.
      * alpha (default None) specifies the alpha values to use for the color plot. If None, then
        leaves the alpha values from color unchanged. If a single number, then all alpha values in
        color are multiplied by that value. If a list of values, one per vertex, then this vector
        is multiplied by the alpha values. Finally, any negative value is set instead of multiplied.
        So, for example, if there were 3 vertices with:
          * color = ((0,0,0,1), (0,0,1,0.5), (0,0,0.75,0,8))
          * alpha = (-0.5, 1, 0.5)
        then the resulting colors plotted will be ((0,0,0,0.5), (0,0,1,0.5), (0,0,0.75,0,4)).
      * mask (default: None) specifies a mask to use for the mesh; thi sis passed through map.mask()
        to figure out the masking. Those vertices not in the mask are not plotted (but they will be
        plotted in the underlay if it is not None).
      * axes (default: None) specifies a particular set of matplotlib pyplot axes that should be
        used. If axes is Ellipsis, then instead of attempting to render the plot, a tuple of
        (tri, zs, cmap) is returned; in this case, tri is a matplotlib.tri.Triangulation
        object for the given map and zs and cmap are an array and colormap (respectively) that
        will produce the correct colors. Without axes equal to Ellipsis, these would instead
        be rendered as axes.tripcolor(tri, zs, cmap, shading='gouraud'). If axes is None, then
        uses the current axes.
      * triangulation (default: None) specifies the matplotlib triangulation object to use, if one
        already exists; otherwise a new one is made.
    '''
    # parse the axes
    if axes is None: axes = matplotlib.pyplot.gca()
    # process the colors
    color = cortex_plot_colors(the_map, color=color, cmap=cmap, vmin=vmin, vmax=vmax, alpha=alpha,
                               underlay=underlay, mask=mask)
    # finally, we can make the plot!
    return cortex_rgba_plot_2D(the_map, color, axes=axes, triangulation=triangulation)


# 3D Graphics ######################################################################################

# If we're using Python 2, we're compatible with pysurfer:
def _ipyvolume_load_error(*args, **kwargs):
    raise RuntimeError('load failure: the requested object could not be loaded, probably ' +
                       'because you do not have ipyvolume installed correctly')
cortex_plot_3D = _ipyvolume_load_error
try:
    import ipyvolume as ipv

    def cortex_plot_3D(obj,
                       color=None, cmap=None, vmin=None, vmax=None, alpha=None,
                       underlay='curvature', mask=None, hemi=None, surface='inflated',
                       figure=Ellipsis, width=600, height=600,
                       view=None, camera_distance=100, camera_fov=None, camera_up=None):
        '''
    cortex_plot_3D(hemi) plots the inflated surface of the given cortex object hemi and returns the
      ipyvolume figure object.
    cortex_plot_3D(mesh) plots the given mesh.
    cortex_plot_3D((hemi1, hemi2...)) plots all the given hemispheres or meshes.
    cortex_plot_3D(mesh) yields a PySurfer Brain object for the given 3D cortical mesh.
    cortex_plot_3D(subject) is equivalent to cortex_plot_3D((subject.lh, subject.rh)).

    The following options are accepted:
      * color (default: None) specifies the color to plot for each vertex; this argument may take a
        number of forms:
          * None, do not plot a color over the underlay (the default)
          * a matrix of RGB or RGBA values, one per vertex
          * a property vector or a string naming a property, in which case the cmap, vmin, and vmax
            arguments are used to generate colors
          * a function that, when passed a single argument, a dict of the properties of a single
            vertex, yields an RGB or RGBA list for that vertex.
      * cmap (default: 'log_eccentricity') specifies the colormap to use in plotting if the color
        argument provided is a property.
      * vmin (default: None) specifies the minimum value for scaling the property when one is passed
        as the color option. None means to use the min value of the property.
      * vmax (default: None) specifies the maximum value for scaling the property when one is passed
        as the color option. None means to use the max value of the property.
      * underlay (default: 'curvature') specifies the default underlay color to plot for the
        cortical surface; it may be None, 'curvature', or a color.
      * alpha (default None) specifies the alpha values to use for the color plot. If None, then
        leaves the alpha values from color unchanged. If a single number, then all alpha values in
        color are multiplied by that value. If a list of values, one per vertex, then this vector
        is multiplied by the alpha values. Finally, any negative value is set instead of multiplied.
        So, for example, if there were 3 vertices with:
          * color = ((0,0,0,1), (0,0,1,0.5), (0,0,0.75,0,8))
          * alpha = (-0.5, 1, 0.5)
        then the resulting colors plotted will be ((0,0,0,0.5), (0,0,1,0.5), (0,0,0.75,0,4)).
      * mask (default: None) specifies a mask to use for the mesh; this is passed through to_mask()
        to figure out the masking. Those vertices not in the mask are not plotted (but they will be
        plotted in the underlay if it is not None).
      * hemi (defaut: None) specifies the hemisphere to use. If the passed mesh object is actually a
        subject or mesh pair then this specifies which hemisphere to use. If the passed object is a
        mesh, then this overrides its chirality, if specified in meta_data. If two hemispheres are
        given, then this may be 'both' or 'split' in accordinace with PySurfer's Brain() class.
      * surface (default: 'white') specifies the surface to use if the mesh object passed is in fact
        either a cortex or subject object.
      * axes (default: None) specifies the ipyvolume axes that should be used; if None, then the
        current axes are used.
      * stylize (default: True) specifies whether or not neuropythy should apply additional standard
        stylings to the ipyvolume figure; these include making sure that the plot range is
        appropriate, that the axes and box are not plotted, and that the camera is in an
        orthographic position looking at the mesh.
    '''
        # First, see if we've been passed a cortex or subject object...
        mesh = []
        for arg in (obj if pimms.is_vector(obj) else [obj]):
            if   geo.is_mesh(arg): mesh.append(arg)
            elif geo.is_topo(arg): mesh.append(to_mesh((mesh, surface)))
            elif mri.is_subject(arg):
                for h in (hemi if pimms.is_vector(hemi) else [hemi]):
                    if geo.is_topo(h) or geo.is_mesh(h): hh = [h]
                    elif h in arg.hemis: hh = [arg.hemis[h]]
                    else:
                        h = to_hemi_str(h)
                        hh = [arg.lh, arg.rh] if h == 'lr' else [arg.hemis[h]]
                    for hh in h: mesh.append(to_mesh((hh, surface)))
        # process the colors
        rgba = np.concatenate(
            [cortex_plot_colors(m, color=color, cmap=cmap, vmin=vmin, vmax=vmax,
                                alpha=alpha, underlay=underlay, mask=mask)
             for m in mesh])
        n = len(rgba)
        # Okay, setup the ipyv figure...
        mns = np.full(3, np.inf)
        mxs = np.full(3, -np.inf)
        ms = ()
        if figure is None: f = ipv.gcf()
        elif figure is Ellipsis: f = ipv.figure(width=width, height=height)
        else: f = figure
        for (m,i0) in zip(mesh,[0] if len(mesh) == 1 else [0,mesh[0].vertex_count]):
            (x,y,z) = m.coordinates
            ii = slice(i0, i0 + m.vertex_count)
            ipvm = ipv.plot_trisurf(x,y,z, m.tess.faces.T, color=rgba[ii,:3])
            mns = np.min([mns, np.min([x,y,z], axis=1)], axis=0)
            mxs = np.max([mxs, np.max([x,y,z], axis=1)], axis=0)
            ms = ms + (ipvm,)
        # Figure out the bounding box...
        szs = mxs - mns
        mid = 0.5*(mxs + mns)
        bsz = np.max(szs)
        # okay, set the plot limits
        mxs = mid + 0.5*bsz
        mns = mid - 0.5*bsz
        ipv.pylab.xlim(mns[0],mxs[0])
        ipv.pylab.ylim(mns[1],mxs[1])
        ipv.pylab.zlim(mns[2],mxs[2])
        # few other styling things
        ipv.pylab.xlabel('')
        ipv.pylab.ylabel('')
        ipv.pylab.zlabel('')
        ipv.style.box_off()
        ipv.style.axes_off()
        # figure out the view
        d = camera_distance
        up = None
        if view is None: view = 'back'
        if pimms.is_str(view):
            if camera_distance is None: d = 10
            view = view.lower()
            (view, up) = (((0,-d,0), (0,0, 1)) if view in ['back','rear','posterior','p','-y'] else
                          ((0, d,0), (0,0, 1)) if view in ['front','anterior','a','+y','y']    else
                          ((0,0, d), (0, 1,0)) if view in ['top','superior','s','+z','z']      else
                          ((0,0,-d), (0,-1,0)) if view in ['bottom','inferior','i','-z']       else
                          (( d,0,0), (0,0, 1)) if view in ['right','r','x','+x']               else
                          ((-d,0,0), (0,0, 1)) if view in ['left','l','-x']                    else
                          (view, None))
            if pimms.is_str(view): raise ValueError('Unknown view: %s' % view)
        if camera_up is not None: up = camera_up
        if d is None: d = np.sqrt(np.sum(np.asarray(d)**2))
        fov = camera_fov
        if fov is None: fov = 180.0/np.pi * 2 * np.arctan(1.125/(2*d))
        f.camera.position = tuple(view)
        f.camera.up = tuple(up)
        f.camera.fov = fov
        f.camera.lookAt(tuple(mid))
        warnings.warn('neuropythy: NOTE: due to a bug in ipyvolume, camera views cannot currently' +
                      ' be set by neuropythy; however, if you click the reset (home) button in' +
                      ' the upper-left corner of the figure, the requested view will be fixed.')
        return f
except Exception: pass

def cortex_plot(mesh, *args, **opts):
    '''
    cortex_plot(mesh) calls either cortex_plot_2D or cortex_plot_3D depending on the dimensionality
      of the given mesh, and yields the resulting graphics object. All optional arguments supported
      by each is supported by cortex plot.

    The following options are accepted:
      * color (default: None) specifies the color to plot for each vertex; this argument may take a
        number of forms:
          * None, do not plot a color over the underlay (the default)
          * a matrix of RGB or RGBA values, one per vertex
          * a property vector or a string naming a property, in which case the cmap, vmin, and vmax
            arguments are used to generate colors
          * a function that, when passed a single argument, a dict of the properties of a single
            vertex, yields an RGB or RGBA list for that vertex.
      * cmap (default: 'log_eccentricity') specifies the colormap to use in plotting if the color
        argument provided is a property.
      * vmin (default: None) specifies the minimum value for scaling the property when one is passed
        as the color option. None means to use the min value of the property.
      * vmax (default: None) specifies the maximum value for scaling the property when one is passed
        as the color option. None means to use the max value of the property.
      * underlay (default: 'curvature') specifies the default underlay color to plot for the
        cortical surface; it may be None, 'curvature', or a color.
      * alpha (default None) specifies the alpha values to use for the color plot. If None, then
        leaves the alpha values from color unchanged. If a single number, then all alpha values in
        color are multiplied by that value. If a list of values, one per vertex, then this vector
        is multiplied by the alpha values. Finally, any negative value is set instead of multiplied.
        So, for example, if there were 3 vertices with:
          * color = ((0,0,0,1), (0,0,1,0.5), (0,0,0.75,0,8))
          * alpha = (-0.5, 1, 0.5)
        then the resulting colors plotted will be ((0,0,0,0.5), (0,0,1,0.5), (0,0,0.75,0,4)).
      * mask (default: None) specifies a mask to use for the mesh; thi sis passed through map.mask()
        to figure out the masking. Those vertices not in the mask are not plotted (but they will be
        plotted in the underlay if it is not None).
      * hemi (defaut: None) specifies the hemisphere to use. If the passed mesh object is actually a
        subject or mesh pair then this specifies which hemisphere to use. If the passed object is a
        mesh, then this overrides its chirality, if specified in meta_data. If two hemispheres are
        given, then this may be 'both' or 'split' in accordinace with PySurfer's Brain() class.
      * surface (default: 'white') specifies the surface to use if the mesh object passed is in fact
        either a cortex or subject object.
      * axes (default: None) specifies a particular set of matplotlib pyplot axes that should be
        used. If axes is Ellipsis, then instead of attempting to render the plot, a tuple of
        (tri, zs, cmap) is returned; in this case, tri is a matplotlib.tri.Triangulation
        object for the given map and zs and cmap are an array and colormap (respectively) that
        will produce the correct colors. Without axes equal to Ellipsis, these would instead
        be rendered as axes.tripcolor(tri, zs, cmap, shading='gouraud'). If axes is None, then
        uses the current axes.
      * triangulation (default: None) specifies the matplotlib triangulation object to use, if one
        already exists; otherwise a new one is made.
    '''
    if not isinstance(mesh, geo.Mesh) or mesh.coordinates.shape[0] > 2:
        # must be a 3D call
        return cortex_plot_3D(mesh, *args, **opts)
    else:
        return cortex_plot_2D(mesh, *args, **opts)

class ROIDrawer:
    '''
    ROIDrawer(axes, mproj) creates a new ROIDrawer class that interacts with the plot on
      the given axes to save the lines drawn on the plot as a neuropythy path trace, which
      is available from the roiDrawer object as roiDrawer.trace once the user is finished.
    ROIDrawer(axes, fmap) extracts the map projection from the meta-data in the given
      flatmap; note that if the projection is not encoded in the flatmap's meta-data, an
      error will be raised.
    
    All arguments and keyword arguments following the first two are passed verbatim to the
    axes.plot() function, which is used for plotting the drawn lines.
    '''
    def __init__(self, axes, mp, closed=True, event_handlers=None, plot_list=None, *args, **kw):
        from neuropythy import (to_map_projection, is_map_projection, is_vset)
        # Assumption: the axes have already been plotted, so there's no need to do any
        # plotting here, aside from the lines we're about to draw
        self.axes = axes
        # get the map projection
        if is_vset(mp) and 'projection' in mp.meta_data: mp = mp.meta_data['projection']
        elif not is_map_projection(mp): mp = to_map_projection(mp)
        self.map_projection = mp
        # draw the initial lines
        if len(args) == 0 and len(kw) == 0: args = ['k.-']
        self.line = axes.plot([], [], *args, **kw)[0]
        self.xs = list(self.line.get_xdata())
        self.ys = list(self.line.get_ydata())
        self.connections = [
            self.line.figure.canvas.mpl_connect('button_press_event', self.on_button),
            self.line.figure.canvas.mpl_connect('key_press_event', self.on_key),
            self.line.figure.canvas.mpl_connect('close_event', self.on_close)]
        # get rid of the mesh for path traces (because we don't want to export meshes on accident)
        if mp.mesh is not None: mp = mp.copy(mesh=None)
        self.trace = geo.PathTrace(mp, np.zeros((2,0)), closed=closed,
                                   meta_data={'roi_drawer':self})
        self.closed = closed
        self.event_handlers = event_handlers
        self.plot_list = plot_list
        if plot_list is not None and len(plot_list) > 0:
            for p in plot_list[1:]: p.set_visible(False)
            plot_list[0].set_visible(True)
        self.current_plot = 0
    def end(self, success=True):
        from neuropythy import path_trace
        # we've finished; clean up and make the line
        if success:
            if len(self.xs) < 1: raise ValueError('Drawn line has no points')
            pts = np.transpose([self.xs, self.ys])
            # remove us from the trace meta-data if we're in it
            rd = self.trace.meta_data.get('roi_drawer')
            if rd is self: self.trace.meta_data = self.trace.meta_data.discard('roi_drawer')
            self.trace.persist()
        else: self.trace = None
        for conn in self.connections:
            self.line.figure.canvas.mpl_disconnect(conn)
        # redraw the final version:
        if self.closed:
            self.xs.append(self.xs[0])
            self.ys.append(self.ys[0])
            self.line.set_data(self.xs, self.ys)
            self.line.figure.canvas.draw()
        plt.close(self.line.figure)
        # clear everything
        self.connection = None
        self.line = None
        self.xs = None
        self.ys = None
    def on_close(self, event):
        self.end(success=False)
    def on_key(self, event):
        import matplotlib.collections
        if event.inaxes != self.line.axes: return
        if event.key == 'tab':
            # we go to the next plot...
            if not self.plot_list: return
            self.plot_list[self.current_plot].set_visible(False)
            tmp = self.current_plot
            self.current_plot = (self.current_plot + 1) % len(self.plot_list)
            a = self.plot_list[self.current_plot]
            if isinstance(a, matplotlib.collections.TriMesh): a.set_visible(True)
            else: self.plot_list[self.current_plot] = a(self.axes)
            a.figure.canvas.draw()
    def on_button(self, event):
        endkeys = ['shift+control', 'shift+ctrl', 'control+shift', 'ctrl+shift']
        if self.line is None: return
        if event.inaxes != self.line.axes: return
        # if shift is down, we delete the last point
        if event.key == 'shift':
            if len(self.xs) == 0: return
            self.xs = self.xs[:-1]
            self.ys = self.ys[:-1]
        elif event.key in endkeys:
            # we abort!
            self.end(success=False)
            return
        elif (event.key is not None and self.event_handlers is not None and
              event.key in self.event_handlers):
            self.event_handlers[event.key](self, event)
            return
        else: # add the points
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
        # redraw the line regardless
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()
        # and update the trace
        self.trace.points = np.asarray([self.xs, self.ys])
        if event.dblclick or event.key in ['control', 'ctrl']:
            self.end(success=True)

def trace_roi(hemi, map_proj, axes, closed=True, event_handlers=None, plot_list=None, **kw):
    '''
    trace_roi(hemi, map_proj, axes) creates an ROIDrawer object that controls the tracing of lines
      around an ROI in a 2D matplotlib plot and returns a not-yet-persistent immutable PathTrace
      object with the ROIDrawer in its meta_data. The path trace is persisted as soon as the user
      finished drawing their line; if the line is canceled, then the trace is never persisted.

    ROI tracing is very simple: any point in the plot is appended to the path as it is clicked; in
    order to eliminate the previous point, hold shift while clicking. To end the path, hold control
    while clicking. To abort the path, hold both shift and control while clicking. (Double-clicking
    should be equivalent to control-clicking, but this does not work in all setups.) In order to use
    the ROI tracing, `%matplotlib notebook` is recommended.

    The trace_roi() function accepts all options that can be passed to cortex_plot() as well as the
    following options:
      * closed (default: True) specifies whether the path-trace that is constructed should be closed
        (True) or open (False).
      * event_handlers (default: None) specifies additional event handlers (named by key) for the
        ROIDrawer().
      * plot_list (default: None) specifies a list of alternate TriMesh objects that can be plotted
        cyclically when the user presses tab. TriMesh objects can be created by pyplot.triplot and
        pyplot.tripcolor, which are used by the neuropythy cortex_plot function as well. If the
        plot_list is not empty, then the first item of the list is immediately plotted on the axes.
        Unlike in the ROIDrawer function itself, the plot_list may contain maps whose keys are
        the various arguments (aside from the initial mesh argument) to cortex_plot.
    '''
    # okay, first off, if the plot_list has maps in it, we convert them using cortex_plot:
    if plot_list is not None:
        if geo.is_flatmap(hemi):                  fmap = hemi
        elif geo.is_flatmap(map_proj):            fmap = map_proj
        elif not geo.is_map_projection(map_proj): fmap = geo.to_map_projection(map_proj)(hemi)
        else:                                     fmap = map_proj(hemi)
        plot_list = [cortex_plot(fmap, axes=axes, **p) if pimms.is_map(p) else p
                     for p in plot_list]
    # next, make the roi drawer
    rd = ROIDrawer(axes, map_proj, closed=closed,
                   event_handlers=event_handlers, plot_list=plot_list)
    return rd.trace

        
