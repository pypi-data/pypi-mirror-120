from mpmath import *
from bisect import bisect_left
from functools import reduce

class TabularInterpolator:
  def __init__(self, Tx = lambda x: x, TxInv = lambda x: x, Ty = lambda x: x, TyInv = lambda x: x):
    self.Tx = Tx
    self.Ty = Ty
    self.TxInv = TxInv
    self.TyInv = TyInv

  def interpolate(self, x, x_orig, y_orig):
    def _basis(j):
        p = [(x - x_values[m])/(x_values[j] - x_values[m]) for m in range(k) if m != j]
        return reduce(lambda s, v: s*v, p)

    # print(x, x_orig)
    k = len(x_orig)
    x_values = [self.Tx(x) for x in x_orig]
    y_values = [self.Ty(y) for y in y_orig]
    return self.TyInv(sum(_basis(j)*y_values[j] for j in range(k)))

def LogYInterpolator():
  return TabularInterpolator(Ty = lambda y: log(y), TyInv = lambda y: exp(y))

def LogLogInterpolator():
  return TabularInterpolator(Tx = lambda x: log(x), TxInv = lambda x: exp(x), Ty = lambda y: log(y), TyInv = lambda y: exp(y))

class Tabular:
  def __init__(self, func, interp = [TabularInterpolator()], regions = [], x = [], eps = mp.mpf('1e-4'), limit=mp.mpf('1e10')):
    self.func = func;
    self.x = x;
    self.y = [func(s) for s in x];
    self.checked = [ False ] * len(x);
    self.interp = interp
    self.regions = regions
    self.eps = eps
    self.limit = limit
    
  def __insertLow(self):
    intp = self.interp[bisect_left(self.regions, self.x[0])]
    xnew = intp.TxInv(3*intp.Tx(self.x[0]) - 2*intp.Tx(self.x[1]))
    ynew = self.func(xnew)
    self.x.insert(0, xnew)
    self.y.insert(0, ynew)
    self.checked.insert(0, False)

  def __insertHigh(self):
    l = len(self.x)
    intp = self.interp[bisect_left(self.regions, self.x[l-1])]
    xnew = intp.TxInv(3*intp.Tx(self.x[l-1]) - 2*intp.Tx(self.x[l-2]))
    ynew = self.func(xnew)
    self.x.insert(l, xnew)
    self.y.insert(l, ynew)
    self.checked.insert(l, False)

  def __findLargestInterval(self, xval, ind):
    intp = self.interp[bisect_left(self.regions, xval)]
    intsz = [(intp.Tx(self.x[ind-1+i]) - intp.Tx(self.x[ind-2+i])) for i in range(3)]
    return ind - 1 + intsz.index(max(intsz))


  def __intervalCenter(self, ind):
    intp = self.interp[bisect_left(self.regions, self.x[ind])]
    xl = intp.Tx(self.x[ind - 1])
    xh = intp.Tx(self.x[ind])
    xm = intp.TxInv(0.5*(xl+xh))
    ym = self.func(xm)
    return (xm, ym, intp)

  def __splitInterval(self, ind):
    xm, ym, intp = self.__intervalCenter(ind)
    self.x.insert(ind, xm)
    self.y.insert(ind, ym)
    self.checked.insert(ind, False)

  def __checkPrecision(self, ind, xval):
    intp = self.interp[bisect_left(self.regions, xval)]
    intsz = [(intp.Tx(self.x[ind-1+i]) - intp.Tx(self.x[ind-2+i])) for i in range(3)]
    return (max(intsz) < self.eps)
    # xm, ym, intp = self.__intervalCenter(ind)
    # yapp = intp.interpolate(xm, self.x[ind-2:ind+2], self.y[ind-2:ind+2])
    # return mp.fabs((ym-yapp)/ym) < self.eps

  def __refinedInterpolate(self, xval):
    while (xval<=self.x[1]):
      self.__insertLow()

    while (xval>=self.x[len(self.x)-2]):
      self.__insertHigh()

    ind = bisect_left(self.x, xval)
    self.checked[ind] = self.__checkPrecision(ind, xval)
    while (not self.checked[ind]):
      insInd = self.__findLargestInterval(xval, ind)
      self.__splitInterval(insInd)
      ind = bisect_left(self.x, xval)
      self.checked[ind] = self.__checkPrecision(ind, xval)
    
    interpolator = self.interp[bisect_left(self.regions, xval)]
    return interpolator.interpolate(xval, self.x[ind-2:ind+2], self.y[ind-2:ind+2])

  def load(self, filename):
    with open(filename) as f:
      table = [[x for x in line.split()] for line in f]
    
    self.x = [mp.mpf(entry[0]) for entry in table]
    self.y = [mp.mpf(entry[1]) for entry in table]

    self.checked = [len(entry) > 2 and entry[2] for entry in table]

  def save(self, filename):
    xlast = mp.mpf('-1e500')
    with open(filename, 'w') as f:
      for i in range(len(self.x)):
        if (self.x[i] > xlast):
          f.write('%s %s %r\n' % (self.x[i], self.y[i], self.checked[i]))
          xlast = self.x[i]

  def lock(self):
    self.checked = [True for x in self.x]

  def eval(self, xval):
    ind = bisect_left(self.x, xval)
  
    if (self.checked[ind]):
      interpolator = self.interp[bisect_left(self.regions, xval)]
      return interpolator.interpolate(xval, self.x[ind-2:ind+2], self.y[ind-2:ind+2])
    else:
      return self.__refinedInterpolate(xval)


class Tabulated:
  def __init__(self, filename, interp = [TabularInterpolator()], regions = []):
    self.interp = interp
    self.regions = regions

    with open(filename) as f:
      table = [[x for x in line.split()] for line in f]

    self.x = [mp.mpf(entry[0]) for entry in table]
    self.y = [mp.mpf(entry[1]) for entry in table]
    self.N = len(self.x) - 2
    
  def eval(self, xval):
    ind = bisect_left(self.x, xval)
  
    if (ind < 2):
      interpolator = self.interp[0]
      return interpolator.interpolate(xval, self.x[0:2], self.y[0:2])
    if (ind > self.N):
      interpolator = self.interp[len(self.interp) - 1]
      return interpolator.interpolate(xval, self.x[self.N:(self.N+2)], self.y[self.N:(self.N+2)])
    else:
      interpolator = self.interp[bisect_left(self.regions, xval)]
      return interpolator.interpolate(xval, self.x[ind-2:ind+2], self.y[ind-2:ind+2])
