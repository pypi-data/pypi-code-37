from __future__ import print_function 
from __future__ import absolute_import 

import tensorflow as tf
import numpy as np 

from scipy.special import erfinv as ierf 
from scipy.linalg  import sqrtm

try: 
  from FixedBinInterpolator import FixedBinInterpolator 
except: 
  from .FixedBinInterpolator import FixedBinInterpolator 


class FastQuantileLayer ( tf.keras.layers.Layer ) :
  """
    Creates a keras layer to emulate the behaviour of 
    scikit-learn QuantileTransformer.
  """

  def __init__ (self, 
      n_quantiles = 50, 
      n_samples   = 200, 
      output_distribution='uniform', 
      default_to_inverse = False, 
      numpy_dtype = np.float32, 
      verbose = False,
      decorrelate = False, 
      **kwargs
    ):
    """
      n_quantiles : int (default: 100)
        Number of quantiles to be computed. It corresponds to 
        the number of landmarks used to discretize the cumulative 
        density function.

      n_sample : int (default: 5000)
        Number of points used to sample the transforms.
        Larger values will result in slower evaluation but more 
        accurate function representation and inversion. 

      output_distribution : string (default: 'uniform')
        Marginal distribution for the transformed data. 
        The choices are 'uniform' (default) or 'normal'.
        The normal distribution is truncated. 

      dtype : numpy data type (default: np.float32)
        Data type of the expected input 

      default_to_inverse : bool
        If default_to_inverse is True, and inverse is explicitely specified
        when applying the layer. 
    """

    self._Nbins             = n_quantiles
    self._Nsamples          = n_samples
    self._outDist           = output_distribution
    self.default_to_inverse = default_to_inverse
    self.numpy_dtype        = numpy_dtype 
    self.verbose            = verbose 

    self.mean_transformed     = np.array([])
    self.covariance_matrix    = np.array([])
    self.inverse_covmat       = np.array([])       

    tf.keras.layers.Layer.__init__ ( self, kwargs ) 


  def _fit_transform ( self, X): 
    """
      Internal. Creates the interpolator for a single variable 
    """
    y  = np.linspace ( 0, 1, self._Nbins ) 
    xq = np.quantile ( X, y )
    if  self._outDist == 'normal' :
      y = ierf ( np.clip(2.*y - 1.,-0.99999, 0.99999)) * np.sqrt(2)

    yq = np.interp(np.linspace(xq[0], xq[-1], self._Nsamples), xq, y ) 

    return xq[0], xq[-1], yq 



  def fit ( self, X, y = None ): 
    """
      Creates the tensorflow interpolator used to transform the 
      distribution to either a uniform or normal distribution.  
    """
    rank = len(X.shape) 
    if rank == 1:   # single variable  
      X = X[None] 

    x_values = list(); y_values = list() 
    for iCol in range ( X.shape[1] ): 
      xmin_, xmax_, yvalues_ = self._fit_transform ( X[:,iCol] ) 
      x_values . append ((xmin_, xmax_))
      y_values . append ( yvalues_ ) 

    self._transforms_X = self.add_weight (
        name = 'fwd_transform_X',
        shape = np.array(x_values).shape,
        initializer = tf.keras.initializers.Constant(value=np.array(x_values)),
        trainable = False
      )


    self._transforms_Y = self.add_weight (
        name = 'fwd_transform_Y',
        shape = np.array(y_values).shape,
        initializer = tf.keras.initializers.Constant(value=np.array(y_values)),
        trainable = False
      )

    self.build ( X.shape[1:] ) 

    return self 


  def build ( self, input_shape ):
    tf.keras.layers.Layer.build ( self, input_shape ) 
  


  def transform ( self, X ) : 
    """
      Apply the tensorflow graph 
    """
    rank = len(X.shape) 
    if rank == 1:   # single variable  
      X = X[None] 

    if not hasattr(self, "_transforms_X"):
      raise RuntimeError ( "QuantileTransformTF was not initialized. Run qtf.fit(numpy_dataset)." ) 

    ret = [] 
    for iColumn in range(X.shape[1]): 
      ret.append ( 
          self._transform_column ( X[:,iColumn],
            self._transforms_X[iColumn],
            self._transforms_Y[iColumn]
          )
        )

    return tf.transpose(tf.stack(ret))



  def _transform_column ( self, X, x_boundaries, y_values ):
    """ Apply the interpolation graph:
        X: x-values for which to compute the corresponding y through interpolation
        x_boundaries: 1D tensor
        y_values: points used to interpolate 

      Returns:
        y_values : 1D tensor of the same length as x_values
    """

    ## Prune the x_values of values larger than the maximum and 
    ## smaller than the minimum for which interpolation would be illdefined 
    ones = tf.ones_like ( X ) 

    ## Find the bin 
    N    = int(y_values.shape[0])
    R    = (x_boundaries[1]-x_boundaries[0])
    x_id = (X/R - x_boundaries[0]/R) * (N-1) 
    x_0f = tf.floor ( x_id )
    x_0 = tf.cast ( x_0f , tf.int64 ) 

    x_0 = tf.clip_by_value ( x_0, 0, N-2 )
    x_1 = x_0 + 1 

    y_0 = tf.gather ( y_values, tf.cast(x_0, tf.int64) ) 
    y_1 = tf.gather ( y_values, tf.cast(x_1, tf.int64) ) 

    y = y_0 + tf.clip_by_value(x_id - x_0f,0,1) * (y_1 - y_0)

    return tf.identity ( y, 'interpolated' ) 
      

  def call ( self, X ):
    """
      Service function to call transform 
    """
    return self.transform ( X, self.default_to_inverse ) 

  
  def get_inverse ( self ):
    """
      Return a clone of this layer. 
    """
    new_layer = self.from_config ( self . get_config() ) 

    if not hasattr(self, "_transforms_X"):
      raise RuntimeError ( "QuantileTransformTF was not initialized. Run qtf.fit(numpy_dataset)." ) 

    nVars = self._transforms_X.shape[0]

    x_boundaries = list()
    y_values     = list() 

    for iVar in range(nVars): 
      x_boundaries.append (( 
          self._transforms_Y.initial_value[iVar,0], 
          self._transforms_Y.initial_value[iVar,-1] 
        ))

    print (x_boundaries)



    return new_layer 


  def get_config ( self ):
    """
      Returns the configuration dictionary.
    """
    cfg = tf.keras.layers.Layer.get_config ( self )
    cfg . update ( dict(
        _Nbins             = int(self._Nbins)           ,   
        _Nsamples          = int(self._Nsamples )       , 
        _outDist           = str(self._outDist)         , 
        numpy_dtype        = str(np.dtype(self.numpy_dtype).name) , 
    ))
    return cfg 

  
  @classmethod
  def from_config ( cls, cfg ):
    """
      Returns the configuration dictionary.
    """
    newLayer = FastQuantileLayer() 
    newLayer._Nbins               = cfg [ '_Nbins' ] 
    newLayer._Nsamples            = cfg [ '_Nsamples' ] 
    newLayer.numpy_dtype          = cfg [ 'numpy_dtype'] 

    return newLayer

    
##    for iColumn, transform in enumerate(cfg [ 'direct_transforms' ]):
##      tf_y = newLayer.add_weight ( 
##          name = 'y%d' % iColumn, 
##          shape = (transform['n_samples'],), 
##          trainable = False 
##        )
##          
##      newLayer.fwdTransforms_ . append ( 
##          FixedBinInterpolator ( transform['x_min'], transform['x_max'], tf_y ) 
##        )
##
##    for iColumn, transform in enumerate(cfg [ 'inverse_transforms' ]):
##      tf_xq = newLayer.add_weight ( 
##          name = 'xq%d' % iColumn, 
##          shape = (transform['n_samples'],), 
##          trainable = False 
##        )
##
##      newLayer.bwdTransforms_ . append ( 
##          FixedBinInterpolator ( transform['x_min'], transform['x_max'], tf_xq )
##        )
#
#    return newLayer
#
#
#  def compute_output_shape ( self, input_shape ):
#    return input_shape
#
#

if __name__ == '__main__':
  dataset = np.c_[
    np.random.uniform ( 0., 1., 1000) , 
    np.random.uniform ( -5., 50., 1000) , 
  ]
  th = np.pi / 5. 
  rotmat = np.array([[np.cos(th),np.sin(th)],[-np.sin(th),np.cos(th)]])
  dataset = np.matmul ( dataset, rotmat ) 

  transformer = FastQuantileLayer (output_distribution='normal', decorrelate=False)
  transformer . fit ( dataset ) 


  #transformer . from_config ( transformer.get_config() ) 

  test_dataset = tf.constant(
    np.matmul ( np.c_[
      np.random.uniform ( 0., 1., 10000) , 
      np.random.uniform ( -5, 50., 10000) , 
    ],rotmat), dtype = tf.float32)

  t = transformer . transform ( test_dataset ) 

  bkwd = transformer . get_inverse() . transform ( t )

  with tf.Session() as session: 
    session.run (tf.global_variables_initializer())
    print ("###### Original dataset ####### " ) 
    print ("Mean: ", np.mean ( test_dataset.eval() , axis= 0) ) 
    print ("Std: ",  np.std  ( test_dataset.eval() , axis= 0) ) 
    print () 
    print ("###### Forward transform ####### " ) 
    print ("Mean:", np.mean((t.eval()), axis= 0))
    print ("Std: ", np.std ((t.eval()), axis= 0))
    print ("CovMat: ", np.cov ( t.eval(), rowvar = False ) )
    print () 
#    print ("###### Backward transform ####### " ) 
#    print ("Mean: ", np.mean ( bkwd.eval() , axis= 0) ) 
#    print ("Std: ",  np.std  ( bkwd.eval() , axis= 0) ) 
#    print () 
#    print ("Average squared error: ", np.sqrt(np.mean ( np.square ( test_dataset.eval() - bkwd.eval() ) ))) 
#    print ("Max.    squared error: ", np.sqrt(np.max  ( np.square ( test_dataset.eval() - bkwd.eval() ) ))) 
#    cmpr = np.c_[test_dataset.eval(), t.eval(),  bkwd.eval()] 
#    error = np.abs(cmpr[:,0]-cmpr[:,4]) 
#
#    print ( "Largest errors: " ) 
#    print (cmpr [np.argsort(-error)][:10] ) 
#    

    
  
  

