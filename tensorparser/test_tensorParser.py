from unittest import TestCase
from tensorparser import TensorParser
from tensorparser.elements import IndexLocation

__author__ = 'thibautlamadon'

class TestTensorParser(TestCase):

  def  test_extract_index(self):
    tp = TensorParser("T_hire      " , "I(S[x,y2] - Z[z1] >= 0 ) * G[z1] * V[y2]","x")
    self.assertEqual(tp.index_out, ['x'])
    self.assertTrue("y2" in tp.index_rest)
    self.assertTrue("z1" in tp.index_rest)
    self.assertTrue("nz" in tp.getSizesSet())
    self.assertTrue("nx" in tp.getSizesSet())
    self.assertTrue("ny" in tp.getSizesSet())

  def  test_extract_index(self):
    """

    """
    tp = TensorParser("T_hire      " , "I(S[x,y2] - Z[z1] >= 0 ) * G[z1] * V[y2]","x")
    tname,dim = tp.getIndexSize('z1')
    testbool  = ((tname=="S") & (dim==1)) | ((tname=="G") & (dim==0))
    self.assertTrue(testbool)

  def test_index(self):
    i1 = IndexLocation('T','x',1)
    self.assertTrue(i1.iname=='x')



