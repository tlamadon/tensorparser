import ast
from elements import *
import re

"""
I need to extract:
 - the Arrays and their dimensions
 - the scalars
 - the list of output indexes
 - the list of all indexes
 - the common indexes so that dimension can be passed to the routine

 help: http://greentreesnakes.readthedocs.org/en/latest/nodes.html#control-flow
"""

class IndexCollector(ast.NodeVisitor):
  ''' parses expressions like a[x,y,z] and extracts
      the list of indexes x,y,z. We also get the
      order
  '''
  def __init__(self):
    ast.NodeVisitor.__init__(self)
    self.indexes = []

  def generic_visit(self, node):
    ast.NodeVisitor.generic_visit(self, node)

  def visit_Name(self, node):
    self.indexes.append(node.id)

class IndexFinder(ast.NodeVisitor):
  '''
  Extracts the different indexes present in the tensor expression,
  as well as where they appear
  '''

  def __init__(self):
    ast.NodeVisitor.__init__(self)
    self.tensors = set()
    self.indexes = set()
    self.index_loc = dict()
    self.scalars = set()

  def visit_Module(self, node):
    """ Called on the beginning of the visit
    """
    self.tensors = set()
    self.indexes = set()
    self.scalars = set()
    self.index_loc = set()
    self.generic_visit(node)

  def generic_visit(self, node):
    ast.NodeVisitor.generic_visit(self, node)

  def visit_Subscript(self,node):
    """
    when we find an Array, we need
      - name
      - dimension
      - list of indexes and their locations
    """
    cc = IndexCollector()
    ast.NodeVisitor.generic_visit(cc, node.slice)

    # store the tensor
    self.tensors.add(Tensor(node.value.id,len(cc.indexes)))
    # store the indexes
    self.indexes = set(cc.indexes) | set(self.indexes)

    # store each location
    i = 0
    for ii in cc.indexes:
      self.index_loc.add(IndexLocation(node.value.id,ii,i))
      i+=1


  def visit_Name(self, node):
    self.scalars.add(node.id)

  def visit_Call(self,node):
    for l in node.args: ast.NodeVisitor.generic_visit(self, ast.Tuple(elts=[l]))

class TensorParser:
  """
   very important class that extracts information from the tensor expression.
   From this class, the formatter should be able to generate the code for the module.
  """

  def __init__(self,name,E,vars,tdesc):
    self.Eraw = E
    self.Vraw = vars
    self.expr = E
    self.Et = ast.parse(E)
    self.vars = vars.split(',')
    self.name = name.strip()
    self.tdesc = tdesc

    self.index_out   = vars.split(',')

    # extract the other indexes
    index_finder   = IndexFinder()
    index_finder.visit(self.Et)
    self.index_rest = index_finder.indexes - set(self.index_out)

    # extract tensors and scalars
    self.tensors = index_finder.tensors
    self.scalars = index_finder.scalars
    self.index_loc = index_finder.index_loc

    # extract unique indexes
    # we need to remove the number at the end of each index

  def __str__(self):
    s = 'I(' + ','.join(self.index_rest) + '|' + ','.join(self.index_out) + ')'
    s += ',T(' + ','.join([ str(t) for t in self.tensors]) + ')'
    s += ',S(' + ','.join([ str(t) for t in self.scalars]) + ')'
    return s
#    print "index others: ",self.index_rest
#    print "index tensors:",self.tensors
#    print "index scalars:",self.scalars

  def getIndexSize(self,iname):
    for ii in self.index_loc:
      if ( iname == self.getIndexName(ii.iname) ):
        return ii.tname,ii.dim
    raise Exception(iname + " not in location list!")


  def getIndexName(self,index):
    """
    if index is x1, returns nx,
    in other words, remove the numbers at the end

    """
    return "n" + re.search("(.*[a-zA-Z])[0-9]*$", index).group(1)

  def getSizesSet(self , withn=False):
    if (withn):
      return set([self.getIndexName(ii) for ii in (self.index_rest| set(self.index_out) )])
    else:
      return set([self.getIndexName(ii) for ii in (self.index_rest| set(self.index_out) )])