__author__ = 'thibautlamadon'

import Formatter
import ast

class JuliaFormat(Formatter.Formatter):

  def __init__(self):
    Formatter.Formatter.__init__(self)
    self.SUBSCRIPT_L = '['
    self.SUBSCRIPT_R = ']'
    self.POW = '.^'
    self.COMMENT ="#"
    self.FILE_EXTENSION="jl"
    self.BinOpMid = { "Mult":".*", "Add":".+", "Div":"./", "Sub":".-" }
    self.Compare = { "Gt":".>","GtE":".>=","Lt":".<","LtE":".<=" }
    self.INDEX_LINEARISE =1
    self.CALL2 = { "max":"max", "min":"min"}


  def func_header(self,tp):
    return ""

  def func_footer(self,tp):
    return "end"

  def declareTensor(self,t):
    return ""

  def declareResult(self,tp,sizes):
    return self.RES_NAME + " = zeros("+ ",".join(sizes) + ")"

  def declareIndex(self,t):
    return ""

  def declareCall(self,tp,sizes):
    args = [t.name for t in tp.tensors]
    args.sort()
    s = "function " + tp.name + "(" +",".join(args)
    if len(tp.scalars)>0:
      s += "," + ",".join(tp.scalars)
    s += ")"

    s += self.CR

    # extract sizes from inputs
    for ss in sizes :
      tname,dim = tp.getIndexSize(ss)
      s += ss + " = size(" + tname + ")[" + str(dim+1) + "]" + self.CR

    s += "@inbounds begin"

    return s

  def getResName(self,tp):
    return tp.name

  def declareFunction(self,tp):
    self.RES_NAME = "Res" #tp.name
    return Formatter.Formatter.declareFunction(self,tp)

  def declareLoopIn(self,i,size):
    return "for " + i + " = 1:" +  size

  def declareLoopOut(self,i):
    return "end"

  def visit_Indicator(self,node):
    self.content += '('
    self.visit(node)
    self.content += ')'

  def func_footer(self,tp):
    s = "end" + self.CR
    s += "return " + self.RES_NAME + self.CR+ "end" + self.CR
    return s

  def declareModuleHeader(self,name,tensors):
    rr = "module " + name +self.CR
    rr += "export " + ",".join(tensors)
    return rr


  def declareModuleFooter(self,name):
    return self.CR + "end"+ self.CR