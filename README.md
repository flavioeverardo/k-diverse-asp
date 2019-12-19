[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/flavioeverardo/k-diverse-asp)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)

# nk-diverse-asp
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
Tested with Python 2.7 on MacOS 10.13.2 High Sierra 64-bits. Travis CI testing coming soon.

## Usage
Example command line call using the propagator_k_distance. Please use the full command to enable the random heuristic of *clasp*.
```bash
$ clingo example.lp fixpoint_k_distance.py 4 -c k=3 [--sign-def=rnd --sign-fix --rand-freq=1 --seed=$RANDOM --enum-mode=record]
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

clingo example.lp fixpoint_k_distance.py 4 -c k=2
clingo version 5.4.0
Reading from example.lp ...
number of unassigned literals: 4
Solving...
Answer: 1
p(3) p(4)
Answer: 2
p(3) p(4) p(6) p(7)
Answer: 3
p(3) p(4) p(6) p(8)
Answer: 4
p(3) p(4) p(7) p(8)

Max distance between two answer sets: 3

Distance between [p(3), p(4)] and [p(3), p(4), p(6), p(7)] = 2
Distance between [p(3), p(4)] and [p(3), p(4), p(6), p(8)] = 2
Distance between [p(3), p(4)] and [p(3), p(4), p(7), p(8)] = 2
Distance between [p(3), p(4), p(6), p(7)] and [p(3), p(4), p(6), p(8)] = 2
Distance between [p(3), p(4), p(6), p(7)] and [p(3), p(4), p(7), p(8)] = 2
Distance between [p(3), p(4), p(6), p(8)] and [p(3), p(4), p(7), p(8)] = 2
Total distance: 12
SATISFIABLE

Models       : 4+
Calls        : 1
Time         : 0.047s (Solving: 0.00s 1st Model: 0.00s Unsat: 0.00s)
CPU Time     : 0.028s
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
