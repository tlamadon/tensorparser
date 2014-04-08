tensorparser
============

python command line tool that generates tensor for code from tensor expression for several languages

## What is this?

`tensorparser` is a small command line utility ( and a python library ) that generates code for tensor expression 
written in simple and intuitive way. The notation is based on Einstein tensor notation. 

A simple tensor is just a multidimensional array, and a a tensor expression is an operation on those arrays. In a tensor expression, 
incidices not present on the left handside and automatically summed. So if for instance you have a matrix $a_{ij}$


## install

Install using pip or easy_install

    pip install tensorparser
    
    
## usage

Create a json file that describes a module that will include a list of tensors. Then run tensorparser,
and the file will be generated. Here is an example of a file called `mytensors.json`:

        {
         "module_name":"atensor",
         "tensors": {
            "T_hire" : {
                "expr" : "I(S[x,y2] - Z[z1] >= 0 ) * G[z1] * V[y2]",
                "args" : "x"
            },
            "T_fire" : {
             "expr" : "I(S[x,y2] - Z[z1] >= 0 ) * G[z1] * V[y2]",
             "args" : "x"
            }
          }
        }

finally generate julia code using `-f jl` or Fortran code with `-f f90`. More format are to come.

     tensorparser -f jl mytensors.json

which generates

