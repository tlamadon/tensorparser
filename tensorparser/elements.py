
class Tensor:
  """ this stores a reference to a tensor, a name and its dimensions
  """

  def __init__(self,name,dim):
    self.dim   = dim
    self.name  = name
  def __eq__(self, other):
    return self.name==other.name
  def __hash__(self):
    ord3 = lambda x : '%.3d' % ord(x)
    return int(''.join(map(ord3, self.name)))
  def __str__(self):
    return self.name+ '[' + str(self.dim) + ']'
  def __lt__(self,other):
    return self.name < other.name

class Scalar:
  def __init__(self,name):
    self.name = name
  def __str__(self):
    self.name


class IndexLocation:
  """ this stores a reference to an index, a name and its dimensions
  """
  def __init__(self,tname,iname,dim):
    self.tname = tname
    self.iname = iname
    self.dim  = dim
  def __eq__(self, other):
    return (self.iname==other.iname) & (self.dim==self.dim) & (self.tname==self.tname)
  def __hash__(self):
    ord3 = lambda x : '%.3d' % ord(x)
    return int(''.join(map(ord3, self.iname + self.tname +  str(self.dim))))
  def __str__(self):
    return self.iname + ' : ' + str(self.dim) + ']'
  def __lt__(self,other):
    if (self.name == other.name):
      return self.dim < other.dim
    return self.name < other.name

