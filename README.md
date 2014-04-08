tensorparser
============

python command line tool that generates tensor for code from tensor expression for several languages

## What is this?

`tensorparser` is a small command line utility ( and a python library ) that generates code for tensor expression 
written in simple and intuitive way. The notation is based on Einstein tensor notation. 

A simple tensor is just a multidimensional array, and a a tensor expression is an operation on those arrays. In a tensor expression, 
indices not present on the left hand side and automatically summed.


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

    module atensor
    export T_fire,T_hire
    # Generated tensor:
    # T_fire I(S[x,y2] - Z[z1] >= 0 ) * G[z1] * V[y2] | x
    function T_fire(G,S,V,Z)
    nx = size(S)[1]
    ny = size(S)[2]
    nz = size(G)[1]
    @inbounds begin
    Res = zeros(nx)
    for x in 1:nx
     Res[x]= 0
     for y2 in 1:ny
      for z1 in 1:nz
       Res[x] =  Res[x].+(S[x + nx * (y2-1)].-Z[z1].>=0).*G[z1].*V[y2]
      end
     end
    end
    end
    return Res
    end

    # Generated tensor:
    # T_hire I(S[x,y2] - Z[z1] >= 0 ) * G[z1] * V[y2] | x
    function T_hire(G,S,V,Z)
    nx = size(S)[1]
    ny = size(S)[2]
    nz = size(G)[1]
    @inbounds begin
    Res = zeros(nx)
    for x in 1:nx
     Res[x]= 0
     for y2 in 1:ny
      for z1 in 1:nz
       Res[x] =  Res[x].+(S[x + nx * (y2-1)].-Z[z1].>=0).*G[z1].*V[y2]
      end
     end
    end
    end
    return Res
    end

    end

