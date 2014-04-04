__author__ = 'thibautlamadon'

"""
 Mother class to generate output of the tensor.
 Language specific implementation should extend that class.

"""

import ast
import re

class Formatter(ast.NodeVisitor):

  def __init__(self):
    self.CR = "\n"
    self.content = ""
    self.BinOpMid = { "Mult":"*", "Add":"+", "Div":"/", "Sub":"-" }
    self.CALL2 = { "max":"max"}
    self.Functions = { "log":"log" }
    self.Compare = { "Gt":">","GtE":">=","Lt":"<","LtE":"<=" }
    self.SUBSCRIPT_L = '['
    self.SUBSCRIPT_R = ']'
    self.POW = '^'
    self.RES_NAME = 'R'
    self.LHS = 'R'
    self.indexAsSizes = False
    self.COMMENT = "//"
    self.FILE_EXTENSION = "txt"
    pass

  def visit_wrap(self,n):
    self.generic_visit(ast.Tuple(elts=[n]))

  def visit_Module(self, node):
    """ Called on the beginning of the visit
    """
    self.content = ""
    self.generic_visit(node)

  def generic_visit(self, node):
    ast.NodeVisitor.generic_visit(self, node)

  def visit_Name(self, node):
    self.content += node.id

  def visit_Subscript(self, node):
    AA = node.value.id
    if (AA=='R'): AA = self.RES_NAME
    self.content +=  AA + self.SUBSCRIPT_L
    ast.NodeVisitor.generic_visit(self, node.slice)
    self.content += self.SUBSCRIPT_R

  def visit_Tuple(self,node):
    IS = [e.id for e in node.elts]
    self.content += ",".join(IS)

  def visit_Call(self,node):
    if (node.func.id=='I'):
      for l in node.args: self.visit_Indicator(l)
    elif (node.func.id in self.CALL2):
      self.content += node.func.id + '('
      self.visit_wrap(node.args[0])
      self.content +=  ','
      self.visit_wrap(node.args[1])
      self.content +=  ')'
    else:
      self.content += node.func.id + '('
      for l in node.args: self.visit_wrap(l)
      self.content +=  ')'


  def visit_BinOp(self,node):
    nn = node.op.__class__.__name__

    if (nn=='Pow'):
      self.visit_Pow(node.left,node.right)
    elif (nn in self.BinOpMid.keys()):
      self.visit_wrap(node.left)
      self.content += self.BinOpMid[nn]
      self.visit_wrap(node.right)

  def visit_Compare(self,node):
    self.visit_wrap(node.left)

    nn = node.ops[0].__class__.__name__
    if (nn in self.Compare.keys()):
      self.content += self.Compare[nn]
    else:
      self.content += nn

    self.visit_wrap(node.comparators[0])

  def visit_Indicator(self,node):
    self.content += '1['
    self.visit(node)
    self.content += ']'

  def formatTensor(self,tp):
    self.content = ""
    self.generic_visit(tp.Et)
    print self.content

  def visit_Num(self,node):
    self.content += str(node.n)

  def visit_Pow(self,x1,x2):
    self.content += '('
    self.visit_wrap(x1)
    self.content += ')'+self.POW + '('
    self.visit_wrap(x2)
    self.content += ')'

  def declareFunction(self,tp):
    """
    generate the full function
    """

    # extract sizes
    sizes = set([self.getIndexBound(ii) for ii in (tp.index_rest| set(tp.index_out) )])

    sp = lambda x: "".join([ " " for i in range(0,x)])

    # get result
    self.LHS = self.RES_NAME + self.SUBSCRIPT_L + ",".join(tp.index_out) + self.SUBSCRIPT_R

    s = ""
    s += self.func_header(tp) + self.CR

    # add a commenter with the formula
    s += self.addComment( "Generated tensor:") + self.CR
    s += self.addComment( tp.name + " " + tp.Eraw + " | " + tp.Vraw ) + self.CR
    # print function signature
    s += self.declareCall(tp,sizes) + self.CR

    # print objects declarations
    for t in sizes:
      s += self.declareIndex(t)
    for t in tp.index_out:
      s += self.declareIndex(t)
    for t in tp.index_rest:
      s += self.declareIndex(t)
    for t in tp.tensors :
      s += self.declareTensor(t)
    for t in tp.scalars:
      s += self.declareScalar(t)

    # declare result
    s += self.declareResult(tp,[self.getIndexBound(i) for i in tp.index_out]) + self.CR

    # create loops or out indexes
    indent = 0
    for i in tp.index_out:
      s += sp(indent) + self.declareLoopIn(i) + self.CR
      indent+=1

    # initialing the result to 0
    s += sp(indent) + self.declareSetResultTozero() + self.CR

    for i in tp.index_rest:
      s += sp(indent) + self.declareLoopIn(i) + self.CR
      indent+=1

    # append formula
    s += sp(indent) + self.declareFormula(tp) + self.CR

    for i in tp.index_out:
      indent-=1
      s += sp(indent) + self.declareLoopOut(i)+ self.CR

    for i in tp.index_rest:
      indent-=1
      s += sp(indent) + self.declareLoopOut(i) + self.CR

    s += self.func_footer(tp)
    return s

  def declareTensor(self,t):
    return ""

  def declareResult(self,n):
    return ""

  def declareScalar(self,t):
    return ""

  def declareFormula(self,tp):
    self.visit(tp.Et)
    et_str = self.content
    return self.LHS + " =  " + self.LHS + "+" + et_str

  def getIndexBound(self,index):
    """
    if index is x1, returns nx,
    in other words, remove the numbers at the end

    """
    return "n" + re.search("(.*[a-zA-Z])[0-9]*$", index).group(1)

  def declareLoopIn(self,i):
    return "for " + i + " = 1:" +  self.getIndexBound(i)
  def declareLoopOut(self,i):
    return "end"
  def declareSetResultTozero(self):
    return self.LHS + "= 0"
  def addComment(self,s):
    return self.COMMENT + ' ' + s
  def getFileExtension(self):
    return "." + self.FILE_EXTENSION
  def declareModuleHeader(self,name):
    return "Module file header"
  def declareModuleFooter(self,name):
    return "Module file footer"