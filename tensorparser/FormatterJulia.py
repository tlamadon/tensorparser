__author__ = 'thibautlamadon'

import Formatter
import ast

class JuliaFormat(Formatter.Formatter):

  def __init__(self):
    Formatter.Formatter.__init__(self)
    self.SUBSCRIPT_L = '['
    self.SUBSCRIPT_R = ']'
    self.POW = '^'
    self.COMMENT ="#"
    self.FILE_EXTENSION="jl"

  def func_header(self,tp):
    return ""

  def func_footer(self,tp):
    return "end"

  def declareTensor(self,t):
    return ""

  def declareResult(self,tp,sizes):
    return tp.name + " = zeros("+ ",".join(sizes) + ")"

  def declareIndex(self,t):
    return ""

  def declareCall(self,tp,sizes):
    args = [t.name for t in tp.tensors]
    args.sort()
    s = "function " + tp.name + "(" +",".join(args)
    if len(tp.scalars)>0:
      s += "," + ",".join(tp.scalars)
    s += ")"
    return s

  def getResName(self,tp):
    return tp.name

  def declareFunction(self,tp):
    self.RES_NAME = tp.name
    return Formatter.Formatter.declareFunction(self,tp)

  def declareLoopIn(self,i):
    return "for " + i + " in 1:" +  self.getIndexBound(i)

  def declareLoopOut(self,i):
    return "end"

  def visit_Indicator(self,node):
    self.content += '('
    self.visit(node)
    self.content += ')'

  def func_footer(self,tp):
    return tp.name + self.CR+ "end" + self.CR

  def declareModuleHeader(self,name):
    return "module " + name +self.CR

  def declareModuleFooter(self,name):
    return self.CR + "end"+ self.CR