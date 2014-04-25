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
    self.INDEX_LINEARISE = 0 # 0 for multidimensional, 1 for linear starting at 0, 2 for starting at 1
    self.tp = None
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
    """ generates the multi-dimensional array, it would a good idea
        to allow to generate a linear index x1 + nx*( y2 - 1)
    """
    IS = [e.id for e in node.elts]
    if (self.INDEX_LINEARISE==0):
      self.content += ",".join(IS)
    else:
      prev= ""
      for e in reversed(IS):
        if (prev==""):
          EE = e
        else:
          EE = e + " + " + self.tp.getIndexName(e) + " * (" + EE + "-1)"
        prev = e
      self.content += EE


  def visit_Call(self,node):
    if (node.func.id=='I'):
      for l in node.args: self.visit_Indicator(l)
    elif (node.func.id in self.CALL2):
      self.content += self.CALL2[node.func.id] + '('
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
      if (nn in ["Add","Sub"]):
        self.content += '('
      self.visit_wrap(node.left)
      self.content += self.BinOpMid[nn]
      self.visit_wrap(node.right)
      if (nn in ["Add","Sub"]):
        self.content += ')'

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

  def declareExtractIndexRange(self,iname,tname,dim):
    return "int " + iname + " = dim(" + tname + ")[" + str(dim) + "]"

  def declareFunction(self,tp):
    """
    generate the full function
    """

    self.tp = tp

    # extract sizes
    sizes = tp.getSizesSet()
    sp = lambda x: "".join([ " " for i in range(0,x)]) # function that indents

    # get result
    self.LHS = self.RES_NAME + self.SUBSCRIPT_L + ",".join(tp.index_out) + self.SUBSCRIPT_R

    s = ""
    s += self.func_header(tp) + self.CR

    # add a commenter with the formula
    s += self.addComment( "Generated tensor:") + self.CR
    s += self.addComment( tp.name + " " + tp.Eraw + " | " + tp.Vraw ) + self.CR
    if ("desc" in tp.tdesc.keys()):
      s += self.addComment(tp.tdesc["desc"]) + self.CR
    # print function signature
    s += self.declareCall(tp,sizes) + self.CR

    for t in tp.index_out:
      s += self.declareIndex(t)
    for t in tp.index_rest:
      s += self.declareIndex(t)
    for t in tp.tensors :
      s += self.declareTensor(t)
    for t in tp.scalars:
      s += self.declareScalar(t)

    # declare result
    s += self.declareResult(tp,[tp.getIndexName(i) for i in tp.index_out]) + self.CR

    # create loops or out indexes
    indent = 0
    for i in tp.index_out:
      s += sp(indent) + self.declareLoopIn(i,tp.getIndexName(i)) + self.CR
      indent+=1

    # initialing the result to 0
    s += sp(indent) + self.declareSetResultTozero() + self.CR

    for i in tp.index_rest:
      s += sp(indent) + self.declareLoopIn(i,tp.getIndexName(i)) + self.CR
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
    return self.LHS + " =  " + self.LHS + self.BinOpMid["Add"] + et_str

  def declareLoopIn(self,i,size):
    return "for " + i + " = 1:" +  self.getIndexName(i)
  def declareLoopOut(self,i):
    return "end"
  def declareSetResultTozero(self):
    return self.LHS + "= 0"
  def addComment(self,s):
    return self.COMMENT + ' ' + s
  def getFileExtension(self):
    return "." + self.FILE_EXTENSION
  def declareModuleHeader(self,name,tensors):
    return "Module file header"
  def declareModuleFooter(self,name):
    return "Module file footer"

  def func_header(self,tp):
      return ""

  def func_footer(self,tp):
    return "" + self.CR
