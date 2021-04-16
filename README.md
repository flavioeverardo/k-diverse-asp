[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/flavioeverardo/k-diverse-asp)
[![Build Status](https://travis-ci.com/flavioeverardo/k-diverse-asp.svg?branch=master)](https://travis-ci.com/flavioeverardo/k-diverse-asp)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)

# k-diverse-asp
Variations of *clasp-nk* to calculate *k*-similar/diverse answer sets.

## Description

We present different means of calculating *n* similar/diverse answer sets by extending *clasp* with custom propagators in Python. This work is based on *clasp-nk* by [Eiter et al. 2009](https://arxiv.org/abs/1108.3260)[1].</br>

Let the distance (*k*) between two answer sets be the Hamming distance, defined as the number of atoms that differs from one answer set to another. Two answer sets are adjacent if their Hamming distance is one; in other words, they are adjacent if only one atom differs. </br>

Currently, we have three approaches to get a set of *n* answer sets with a separation of at least *k* among answer sets. 
They share the same idea departing from the first answer set.</br>
From there, the upcoming candidate answer set must respect the separation of at least *k*, otherwise, the candidate answer set is added as a learned nogood. Their difference lies in which part of the search we perform the distance measurement, and they are:</br>

- Propagator_k_distance: get answer sets with distance *k* during propagation. </br>
- Fixpoint_k_distance: get answer sets with distance *k* when fixpoints are reached.</br>
- Total_k_distance: get answer sets with distance *k* on total assignments.</br>

Plus, there is a prototye of an incremental version of the Total_k_distance propagator where the *k* value increments in one unit for each new solving call
Incremental_k_distance. Incrementally, search for *k* distant answer sets until no such separation holds.</br>

## Table of Contents

- [Requirements](#requirements)
- [Usage](#usage)
- [Example](#example)
- [Test](#test)
- [License](#license)

## Requirements
`k-diverse-asp` works with `clingo` version 5.4
and is tested under Unix systems using Travis CI for Linux with Python 2.7 and 3.9. </br>
The easiest way to obtain Python enabled clingo packages is using Anaconda.
Packages are available in the Potassco channel.
First install either Anaconda or Miniconda and then run: `conda install -c potassco clingo`.

## Usage
Example command line call using the propagator_k_distance. Please use the full command to enable the random heuristic of *clasp*.
```bash
$ clingo example.lp fixpoint_k_distance.py 4 -c k=3 [--sign-def=rnd --sign-fix --rand-freq=1 --seed=$RANDOM --enum-mode=record]
```
Another example call using the incremental approach asking for 4 answer sets starting with a distance of at least 3 and *clasp's* random heuristic.
```
clingo example.lp incremental_k_distance.py 4 -c k=3 --sign-def=rnd --sign-fix --rand-freq=1 --seed=$RANDOM --enum-mode=record
```

## Example

A couple of examples asking for four answer sets with a separation of at least two and three.
```bash
$ cat example.lp 
#const n=5.
{ p(1..n) }.
p(3).
p(4).
:- p(2).
:- p(1), p(4).

$ clingo example.lp fixpoint_k_distance.py 4 -c k=3 --sign-def=rnd --sign-fix --rand-freq=1 --seed=$RANDOM --enum-mode=record                                  [1:54:05]
clingo version 5.4.0
Reading from example.lp ...
number of unassigned literals: 8
Solving...
Answer: 1
p(3) p(4) p(6) p(8) p(11)
Answer: 2
p(3) p(4) p(6) p(8) p(10) p(12)
Answer: 3
p(3) p(4) p(6) p(7) p(8) p(9) p(11) p(12)
Answer: 4
p(3) p(4) p(6) p(7) p(8) p(9) p(10)

Distance between answer sets 1 and 2 = 3
Distance between answer sets 1 and 3 = 3
Distance between answer sets 1 and 4 = 4
Distance between answer sets 2 and 3 = 4
Distance between answer sets 2 and 4 = 3
Distance between answer sets 3 and 4 = 3
Total distance: 20
Max distance between two answer sets: 4
SATISFIABLE

Models       : 4+
Calls        : 1
Time         : 0.012s (Solving: 0.00s 1st Model: 0.00s Unsat: 0.00s)
CPU Time     : 0.012s

```

```
$ clingo example.lp fixpoint_k_distance.py 4 -c k=3
clingo version 5.4.0
Reading from example.lp ...
number of unassigned literals: 4
Solving...
Answer: 1
p(3) p(4)
Answer: 2
p(3) p(4) p(6) p(7) p(8)

Max distance between two answer sets: 4

Distance between [p(3), p(4)] and [p(3), p(4), p(6), p(7), p(8)] = 3
Total distance: 3
SATISFIABLE

Models       : 2
Calls        : 1
Time         : 0.065s (Solving: 0.04s 1st Model: 0.00s Unsat: 0.04s)
CPU Time     : 0.029s
```

Example of the incremental solving
```
$ clingo example.lp incremental_k_distance.py 4 -c k=3 --sign-def=rnd --sign-fix --rand-freq=1 --seed=$RANDOM --enum-mode=record                               [2:03:49]
clingo version 5.4.0
Reading from example.lp ...

k: 3
Solving...
Answer: 1
p(3) p(4) p(6) p(8) p(10)
Answer: 2
p(3) p(4) p(6) p(12)
Answer: 3
p(3) p(4) p(6) p(7) p(8) p(11)
Answer: 4
p(3) p(4) p(6) p(7) p(10) p(11) p(12)

Distance between answer sets 1 and 2 = 3
Distance between answer sets 1 and 3 = 3
Distance between answer sets 1 and 4 = 4
Distance between answer sets 2 and 3 = 4
Distance between answer sets 2 and 4 = 3
Distance between answer sets 3 and 4 = 3
Total distance: 20
Max distance between two answer sets: 4

k: 4
Solving...
Answer: 1
p(3) p(4) p(6) p(8) p(10)
Answer: 2
p(3) p(4) p(5) p(6) p(7) p(8) p(12)
Answer: 3
p(3) p(4) p(8) p(11) p(12)
Answer: 4
p(3) p(4) p(5) p(7) p(8) p(10) p(11)

Distance between answer sets 1 and 2 = 4
Distance between answer sets 1 and 3 = 4
Distance between answer sets 1 and 4 = 4
Distance between answer sets 2 and 3 = 4
Distance between answer sets 2 and 4 = 4
Distance between answer sets 3 and 4 = 4
Total distance: 24
Max distance between two answer sets: 4

k: 5
Solving...
Answer: 1
p(3) p(4) p(6) p(8) p(10)

Total distance: 0
Max distance between two answer sets: 0
------------------------------------------------------------------------------------
Optimum
Answer: 1
p(3) p(4) p(6) p(8) p(10)
Answer: 2
p(3) p(4) p(5) p(6) p(7) p(8) p(12)
Answer: 3
p(3) p(4) p(8) p(11) p(12)
Answer: 4
p(3) p(4) p(5) p(7) p(8) p(10) p(11)

Distance between answer sets 1 and 2 = 4
Distance between answer sets 1 and 3 = 4
Distance between answer sets 1 and 4 = 4
Distance between answer sets 2 and 3 = 4
Distance between answer sets 2 and 4 = 4
Distance between answer sets 3 and 4 = 4
Total distance: 24
Max distance between two answer sets: 4

SATISFIABLE

Models       : 9
Calls        : 3
Time         : 0.041s (Solving: 0.01s 1st Model: 0.00s Unsat: 0.01s)
CPU Time     : 0.041s

```

## Test

To run the tests, go into the test directory. Normalize the results from a given program (file_name.lp) with the command:
```
python run.py -c clingo normalize file_name.lp > file_name.sol
```
Next, run the tests with the command:
```
python run.py -c clingo run
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## References
*Eiter, T., Erdem, E., Erdogan, H., & Fink, M. (2013). Finding similar/diverse solutions in answer set programming. Theory and Practice of Logic Programming, 13(3), 303-359.*</br>
