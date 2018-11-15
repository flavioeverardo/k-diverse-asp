# k-diverse-asp
Variations of clasp-nk to calculate k-similar/diverse answer sets

## Description

Extending clasp by means of custom propagators developed in Python, we present three ways to get n answer sets which are k similar/diverse. This work is based on clasp-nk by [Eiter et al. 2009].</br>
Let the distance (k) between two answer sets be the Hamming distance, defined as the number of atoms that differs from one answer to another.</br>
Two answer sets are adjacent if their Hamming distance is one; in other words, they are adjacent if only one atom differs.

The three approaches to get a set n of answer sets which respect a k-similarity/diversity are:</br>
Propagator_k_distance. Get answer sets with distance k during propagation. </br>
Fixpoint_check_k_distance. Get answer sets with distance k when fixpoints are reached.</br>
Total_check_k_distance. Get answer sets with distance k on total assignments.</br>

## Table of Contents

- [Requirements](#requirements)
- [Usage](#usage)
- [Example](#example)
- [Test](#test)
- [License](#license)

## Requirements
Tested with Python 2.7 on MacOS 10.13.2 High Sierra 64-bits. 

## Usage
Any propagator uses a standard clingo call. Please use the full command to enable the random heuristic.
```bash
$ clingo example.lp propagator_k_distance.py -c n=7 -c k=2 0 -c v=true [--sign-def=rnd --sign-fix --rand-freq=1 --seed=$RANDOM --enum-mode=record]
```

## Example
```bash
$ cat example.lp 
#const n=5.
{ p(1..n) }.
p(3).
p(4).
:- p(2).
:- p(1), p(4).

$ clingo example.lp propagator_k_distance.py -c n=7 -c k=2 -c v=true 0
clingo version 5.3.0
Reading from example.lp ...
number of unassigned literals: 3
Solving...
Answer: 1
p(3) p(4)
Answer: 2
p(3) p(4) p(6) p(7)
Answer: 3
p(3) p(4) p(5) p(7)
Answer: 4
p(3) p(4) p(5) p(6)

Max distance between two answer sets: 3

Distance between [p(3), p(4)] and [p(3), p(4), p(6), p(7)] = 2
Distance between [p(3), p(4)] and [p(3), p(4), p(5), p(7)] = 2
Distance between [p(3), p(4)] and [p(3), p(4), p(5), p(6)] = 2
Distance between [p(3), p(4), p(6), p(7)] and [p(3), p(4), p(5), p(7)] = 2
Distance between [p(3), p(4), p(6), p(7)] and [p(3), p(4), p(5), p(6)] = 2
Distance between [p(3), p(4), p(5), p(7)] and [p(3), p(4), p(5), p(6)] = 2
Total distance: 12
SATISFIABLE

Models       : 4
Calls        : 1
Time         : 0.071s (Solving: 0.02s 1st Model: 0.02s Unsat: 0.00s)
CPU Time     : 0.035s
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
Eiter, Thomas, et al. "Finding similar or diverse solutions in answer set programming." International Conference on Logic Programming. Springer, Berlin, Heidelberg, 2009.
