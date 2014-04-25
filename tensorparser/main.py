"""
This is relatively basic stuff
you write an expression of the sort

A[x1,x2] * B[x2]

I collect the indexes, here x1,x2
I generate the code to wrap the operation as a sum.

can generate fortran, c++, or anything else that can be useful

"""


import ast
import tensorparser.FormatterJulia
format = tensorparser.FormatterJulia.JuliaFormat()
tp = tensorparser.TensorParser("T_hire      " , "I(S[x,y2] - Z[z1] >= 0 ) * G[z1] * V[y2]","x",)
print format.declareFunction(tp)


#process("T_P0_1     " , "max(0,S[x1,y] - S[x1,y1]-Z[z1]) * G[z1] * H[x1,y1]","y")
#process("T_P0_0     " , "max(0,S[x1,y]-Z[z1]) * G[z1] * U[x1]","y")
#process("T_W0       " , "max(0,S[x,y1]-Z[z1]) * G[z1] * V[y1] ","x")
#process("T_H_j2j    " , "I(S[x,y] -Z[z1]  > S[x,y2]       ) * G[z1] * H[x,y2] * V[y]","x,y")
#process("T_H_j2j_out" , "I(S[x,y]        < S[x,y2] -Z[z1] ) * G[z1] * V[y2]","x,y")
#process("T_H_u2e    " , "I(S[x,y] -Z[z1] >=0) * G[z1] * U[x] * V[y]","x,y")
#process("T_V        " , "H[x,y]","y")
#process("T_U        " , "H[x,y]","x")
#process("T_pr0_0    " , "I(S[x,y] -Z[z1]  >0 ) * G[z1] * U[x] ","y")
#process("T_pr0_1    " , "I(S[x,y] -Z[z1]  > S[x,y2]       ) * G[z1] * H[x,y2] ","y")
#process("T_pr1      " , "I(S[x,y]        < S[x,y2] -Z[z1] ) * G[z1] * V[y2]","y")

#process("T_hire      " , "I(S[x,y2] - Z[z1] >= 0 ) * G[z1] * V[y2]","x")
#
#
#
#
#process("T_sep      " , "I(S[x,y2] < 0 ) * H[x,y2]","x")
#
#process("T_fill0      " , "I(S[x2,y] - Z[z1] >= 0 ) * G[z1] * U[x2]","y")
#process("T_fill1      " , "I(S[x2,y] - Z[z1] >= S[x2,y2] ) * G[z1] * H[x2,y2]","y")
#process("T_leave      " , "I(S[x,y2] - Z[z1] > S[x,y] )   * V[y2] * G[z1] * H[x,y]","y")
