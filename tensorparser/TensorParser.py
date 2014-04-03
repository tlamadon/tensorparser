import ast
from elements import *

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
  def __init__(self):
    ast.NodeVisitor.__init__(self)
    self.indexes = []
  def generic_visit(self, node):
    ast.NodeVisitor.generic_visit(self, node)
  def visit_Name(self, node):
    self.indexes.append(node.id)

class IndexFinder(ast.NodeVisitor):
  '''
  Extracts the different indexes present in the tensor expression
  '''

  def __init__(self):
    ast.NodeVisitor.__init__(self)
    self.tensors = set()
    self.indexes = set()
    self.scalars = set()

  def visit_Module(self, node):
    """ Called on the beginning of the visit
    """
    self.tensors = set()
    self.indexes = set()
    self.scalars = set()
    self.generic_visit(node)

  def generic_visit(self, node):
    ast.NodeVisitor.generic_visit(self, node)

  def visit_Subscript(self,node):
    """
    when we find an Array, we need
      - name
      - dimension
      - list of indexes
    """
    cc = IndexCollector()
    ast.NodeVisitor.generic_visit(cc, node.slice)
    self.tensors.add(Tensor(node.value.id,len(cc.indexes)))
    self.indexes = set(cc.indexes) | set(self.indexes)

  def visit_Name(self, node):
    self.scalars.add(node.id)

  def visit_Call(self,node):
    for l in node.args: ast.NodeVisitor.generic_visit(self, ast.Tuple(elts=[l]))

class TensorParser:

  def __init__(self,name,E,vars):
    self.Eraw = E
    self.Vraw = vars
    self.expr = E
    self.Et = ast.parse(E)
    self.vars = vars.split(',')
    self.name = name.strip()

    self.index_out  = vars.split(',')

    # extract the other indexes
    index_finder   = IndexFinder()
    index_finder.visit(self.Et)
    self.index_rest = index_finder.indexes - set(self.index_out)

    # extract tensors and scalars
    self.tensors = index_finder.tensors
    self.scalars = index_finder.scalars

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

