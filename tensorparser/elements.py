
class Tensor:

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