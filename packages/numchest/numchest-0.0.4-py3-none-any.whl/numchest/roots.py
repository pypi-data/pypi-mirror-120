import numpy as np
import math


def findZeros(values, axis=None, start=0, end=-1):
  """Find zeros in a one dimensional numpy array

  The algorithm checks for zero crossings and then performs a linear 
  interpolation to determine an approximate value for the zero crossing.

  Parameters
  ----------
  values: numpy array
    The array containeng the function values
  axis: numpy array, optional
    An array containing the x-axis values. These will be used to determine
    the zero crossings. Requires axis.size = values.size.
    If not supplied, the indices of the values array will be used to calculate
    the zero crossings
  start: int, optional
    A starting index to look for zero crossings. Negative values indicate offsets
    from the end of the array. (default = 0)
  end: int, optional
    An end index to look for zero crossings. Negative values indicate offsets
    from the end of the array. (default = -1)
  """
  def getX(index):
    if (axis is None):
      return index
    lo = math.floor(index)
    alpha = index - lo
    if (alpha == 0.0):
      return axis[lo]
    else:
      return (1-alpha)*axis[lo] + alpha*axis[lo+1]

  n = values.size
  if (end<0):
    end = n + end
  if (start<0):
    start = n + start
  
  lastval = values[start]
  result = []

  for i in range(start+1, end+1):
    nextval = values[i]
    if (nextval==0.0):
      result.append(getX(i))
    elif (lastval*nextval < 0.0):
      result.append(getX( i - nextval/(nextval-lastval) ))
    lastval = nextval
  
  return np.array(result)

