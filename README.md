# QualitativeModelFitting
[![Build Status](https://travis-ci.org/CiaranWelsh/QualitativeModelFitting.svg?branch=master)](https://travis-ci.org/CiaranWelsh/QualitativeModelFitting)
[![Docs](https://readthedocs.org/projects/qualitativemodelfitting/badge/?version=latest)]
[!Coverage](coverage.svg)]

A package for fine tuning `sbml` models in accordance with qualitative observations derived from literature and data. 

[Documentation here](https://qualitativemodelfitting.readthedocs.io/en/latest/)
-------------------------------------------------------------------------------

Installation
------------

Create a python 3.6 environment:
```
$ conda create --name py36 python=3.6
```
switch to environment:
```
$ conda activate py36
```
then:
```
$pip install QualitativeModelFitting
```
Due to problems with the `tellurium` and `roadrunner` dependencies, you must use python 3.6. 

Quickstart
----------

Make an model using [antimony](http://tellurium.analogmachine.org/antimony-tutorial/). 

antimony_string = '''
model SimpleFeedback()
compartment Cell = 1;
var A in Cell;
var B in Cell;
var C in Cell;
const S;
const I;
A = 0;
B = 0;
C = 0;
S = 0;
I = 0;
BI = 0;
k1 = 0.1;
k2 = 0.1;
k3 = 0.1;
k4 = 0.1;
k5 = 10;
k6 = 0.1;
k7 = 0.1;
k8 = 0.1;
R1: => A            ; Cell * k1*S;
R2: A =>            ; Cell * k2*A*C;
R3: => B            ; Cell * k3*A;
R4: B =>            ; Cell * k4*B;
R5: B + I => BI     ; Cell * k5*B*I;
R6: BI => B + I     ; Cell * k6*BI;
R7: => C            ; Cell * k7*B;
R8: C =>            ; Cell * k8*C;
end
'''
```
Define an input string 
```
input_string='''
timeseries None { S=0, I=0 } 0, 100, 101
timeseries S { S=1, I=0 } 0, 100, 101
timeseries I { S=0, I=1 } 0, 100, 101
timeseries SI { S=1, I=1 } 0, 100, 101
observation
Obs_basics1:    A[None]@t=0             >  A[None]@t=10
Obs_basics2:    A[S]@t=10               >  A[S]@t=0
Obs_basics3:    A[S]@t=25               >  A[SI]@t=25
Obs_mean:       mean(B[S]@t=(0, 100))   >  mean(B[SI]@t=(0, 100))
Obs_max:        max(B[SI]@t=(0, 100))   >  max(B[S]@t=(0, 100))
Obs_min:        min(B[SI]@t=(0, 100))   == 0
Obs_any:        any(B[SI]@t=(0, 100)    >  3)
Obs_all:        all(B[S]@t=(0, 100)     <  1)'''
```

Run the `Runner`
```
Runner(antimony_string, input_string).run()
          name            observation  evaluation
0  Obs_basics1                  0 > 0       False
1  Obs_basics2             0.9779 > 0        True
2  Obs_basics3        1.5713 > 2.4536       False
3     Obs_mean        0.9376 > 0.1644        True
4      Obs_max        0.3675 > 1.3467       False
5      Obs_min                 0 == 0       False
6      Obs_any  any(TimeInterval > 3)       False
7      Obs_all  all(TimeInterval < 1)       False










