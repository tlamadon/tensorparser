__author__ = 'thibautlamadon'

import Formatter
import ast

class FortranFormat(Formatter.Formatter):

  def __init__(self):
    Formatter.Formatter.__init__(self)
    self.SUBSCRIPT_L = '('
    self.SUBSCRIPT_R = ')'
    self.POW = '**'
    self.COMMENT ="!"
    self.FILE_EXTENSION="f90"


  def declareTensor(self,t):
    return "double precision " + t.name + "(" + ",".join([ ":" for i in range(0,t.dim)]) + ")" +self.CR

  def declareResult(self,tp,sizes):
    return "double precision " + tp.name   + "("+ ",".join(sizes) + ")"

  def declareScalar(self,t):
    return "double precision " + t +self.CR

  def declareIndex(self,t):
    return "integer " + t +self.CR

  def visit_Num(self,node):
    self.content += str(node.n) +'D0'

  def declareCall(self,tp,sizes):
    args = [t.name for t in tp.tensors]
    args.sort()
    s = "function " + tp.name + "(" +",".join(args)
    if len(tp.scalars)>0:
      s += "," + ",".join(tp.scalars)
    s +=  "," + ",".join(sizes)

    s += ")" + self.CR + "implicit none"
    return s

  def getResName(self,tp):
    return tp.name

  def declareFunction(self,tp):
    self.RES_NAME = tp.name
    return Formatter.Formatter.declareFunction(self,tp)

  def declareSetResultTozero(self):
    return self.LHS + "= 0D0"

  def declareLoopIn(self,i,s):
    return "do " + i + " = 1," +  s
  def declareLoopOut(self,i):
    return "end do"
  def visit_Indicator(self,node):
    self.content += 'MERGE(1D0,0D0,'
    self.visit(node)
    self.content += ')'

  def declareModuleHeader(self,name,tensors):
    return "module " + name +self.CR + "contains" + self.CR

  def declareModuleFooter(self,name):
    return "end module "+ self.CR

  def func_footer(self,tp):
    return "end function" + self.CR
