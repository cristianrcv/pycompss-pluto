<!-- Automatic builds status -->
<!-- [![Build Status](https://travis-ci.org/XX)](https://travis-ci.org/XX) -->

<!-- Codacy -->
<!-- [![codacy_coverage](https://api.codacy.com/project/badge/Coverage/d9a02acdf3ad4213b4932b5441201101)](https://www.codacy.com/app/cristianrcv/pycompss-pluto?utm_source=github.com&utm_medium=referral&utm_content=cristianrcv/pycompss-pluto&utm_campaign=Badge_Coverage) -->

[![codacy_grade](https://api.codacy.com/project/badge/Grade/d9a02acdf3ad4213b4932b5441201101)](https://www.codacy.com/app/cristianrcv/pycompss-pluto?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=cristianrcv/pycompss-pluto&amp;utm_campaign=Badge_Grade)

<!-- Codecov -->
[![codecov](https://codecov.io/gh/cristianrcv/pycompss-pluto/branch/master/graph/badge.svg)](https://codecov.io/gh/cristianrcv/pycompss-pluto)

<!-- Maven central packages version -->
<!-- [![Maven Central](https://maven-badges.herokuapp.com/maven-central/XX)](https://maven-badges.herokuapp.com/maven-central/XX) -->

<!-- Dependencies update status -->
<!-- [![Dependency Status](https://www.versioneye.com/user/projects/59f6fd4c0fb24f1f1f38c653/badge.svg?style=flat-square)](https://www.versioneye.com/user/projects/59f6fd4c0fb24f1f1f38c653) -->

<!-- Java DOC status -->
<!-- [![Javadocs](http://javadoc.io/badge/XX.svg)](http://javadoc.io/doc/XX) -->

<!-- Main Repository language -->
[![Language](https://img.shields.io/badge/language-python-brightgreen.svg)](https://img.shields.io/badge/language-python-brightgreen.svg)

<!-- Repository License -->
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/cristianrcv/pycompss-pluto/blob/master/LICENSE)


# PyCOMPSs AutoParallel

The PyCOMPSs AutoParallel module.

The implementation includes:
* The `@parallel()` decorator for Python to run applications with [PyCOMPSs][compss]
* Different Translator modules to automatically generate parallel Python code
    * Py2Scop Translator: Translation of Python code into [OpenScop][openscop] format 
    * Scop2PScop2Py Translator: Integration with the [PLUTO][pluto] tool to generate
    possible parallelizations of the given code. The output is written in Python
    (by means of a [CLooG][cloog] extension) with parallel annotations following an
    OMP fashion. 
    * Py2PyCOMPSs Translator: Translation of parallel annotated Python code into
    PyCOMPSs task definitions. 
 * A Code Replacer module to replace the user code by autogenerated code.

---

## Table of Contents

* [Dependencies](#dependencies)
    * [Software Dependencies](#software-dependencies)
    * [Included Dependencies inside PLUTO](#included-dependencies-inside-pluto)
    * [Python Module Dependencies](#python-module-dependencies)
    * [Extra Dependencies](#extra-dependencies)
* [Commands](#commands)
    * [Examples](#examples)
    * [Test](#test)
    * [Coverage](#coverage)
    * [Style](#style)
    * [Clean](#clean)
* [Contributing](#contributing)
* [Author](#author)
* [Disclaimer](#disclaimer)
* [License](#license)

---

## Dependencies

### Software Dependencies

[COMPSs][compss]: The COMP Superscalar (COMPSs) framework is mainly compose of a
programming model which aims to ease the development of applications for distributed
infrastructures, such as Clusters, Grids and Clouds and a runtime system that exploits
the inherent parallelism of applications at execution time. The framework is
complemented by a set of tools for facilitating the development, execution monitoring
and post-mortem performance analysis. It natively supports Java but has bindings for
Python, C and C++. 

[PLUTO][pluto]: PLUTO is an automatic parallelization tool based on the polyhedral
model. The polyhedral model for compiler optimization provides an abstraction to
perform high-level transformations such as loop-nest optimization and parallelization
on affine loop nests. Pluto transforms C programs from source to source for 
coarse-grained parallelism and data locality simultaneously. The core transformation
framework mainly works by finding affine transformations for efficient tiling. OpenMP
parallel code for multicores can be automatically generated from sequential C program
sections. Outer (communication-free), inner, or pipelined parallelization is achieved
purely with OpenMP parallel for pragrams.


### Included Dependencies inside PLUTO

[OpenSCOP][openscop]: OpenScop is an open specification defining a file format and a set
of data structures to represent a static control part (SCoP for short), i.e., a program
part that can be represented in the polyhedral model. The goal of OpenScop is to 
provide a common interface to various polyhedral compilation tools in order to 
simplify their interaction. The OpenScop aim is to provide a stable, unified format
that offers a durable guarantee that a tool can use an output or provide an input 
to another tool without breaking a tool chain because of some internal changes in one
element of the chain. The other promise of OpenScop is the ability to assemble or
replace the basic blocks of a polyhedral compilation framework at no, or at least
low engineering cost.

[CLooG][cloog]: CLooG is a free software and library to generate code for scanning
Z-polyhedra. That is, it finds a code (e.g. in C, FORTRAN...) that reaches each
integral point of one or more parameterized polyhedra. CLooG has been originally
written to solve the code generation problem for optimizing compilers based on the
polytope model. Nevertheless it is used now in various area e.g. to build control
automata for high-level synthesis or to find the best polynomial approximation of
a function. CLooG may help in any situation where scanning polyhedra matters. While
the user has full control on generated code quality, CLooG is designed to avoid
control overhead and to produce a very effective code.


### Python Module Dependencies

- [Inspect][inspect] Python module
- [AST][ast] Python module
- [AST Observe/Rewrite (ASTOR)][astor] Python module
- Uses the [subprocess][subprocess] Python module (`scop2pscop2py` translator)
- [Logging][logging] Python module
- [UnitTest][unittest] Python module


### Extra Dependencies

- To run all tests you require the [Nose][nose] Python module
- To add code coverage you require [coverage][coverage] and/or
[codacy-coverage][codacy] Python modules


## Commands

### Examples

The `examples/` folder contains a folder per example application. 

Each example contains a `README.md` file (describing the application and the generated
task graphs), and two versions: the `userparallel` and the `autoparallel`. Each
version contains its own `run.sh` script to run it locally using 4 cores.

The `examples/` folder contains a `run.sh` script to run all the available 
applications locally using 4 cores.  


### Test

With debug mode enabled:

```
export PYTHONPATH=${git_base_dir}
cd pycompss
python nose_tests.py -s
```

With debug mode disabled:

```
export PYTHONPATH=${git_base_dir}
cd pycompss
python -O nose_tests.py
```


### Coverage

Run coverage:

```
./coverage_run.sh
```

Upload coverage:

```
echo "YOUR_TOKEN" > .CODACY_PROJECT_TOKEN
echo "YOUR_TOKEN" > .CODECOV_PROJECT_TOKEN

./coverage_upload.sh
```


### Style

This project follows the [PyCodeStyle guide][pycodestyle] (formerly called pep8).

This project tolerates the following relaxations:
* `E501 line too long` : Code lines can be up to 120 characters

You can verify the code style by running:

```
pycodestyle . --max-line-length=120
```


### Clean

```
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
```

## Contributing

All kinds of contributions are welcome. Please do not hesitate to open a new issue,
submit a pull request or contact the author if necessary. 
 

## Author

Cristián Ramón-Cortés Vilarrodona <cristian.ramoncortes(at)bsc.es> ([Personal WebPage][cristian])

This work is supervised by:
- Rosa M. Badia ([BSC][bsc])
- Philippe Clauss ([INRIA][inria])
- Jorge Ejarque ([BSC][bsc])


## Disclaimer

This is part of a collaboration between the [CAMUS Team][camus] at [INRIA][inria] and
the [Workflows and Distributed Computing Team][wdc-bsc] at [BSC][bsc] and is still
under development. 


## License

Licensed under the [Apache 2.0 License][apache-2]


[compss]: http://compss.bsc.es
[pluto]: http://pluto-compiler.sourceforge.net/
[openscop]: http://icps.u-strasbg.fr/people/bastoul/public_html/development/openscop/
[cloog]: http://www.cloog.org/

[inspect]: https://docs.python.org/2/library/inspect.html
[ast]: https://docs.python.org/2/library/ast.html
[astor]: http://astor.readthedocs.io/en/latest/
[subprocess]: https://docs.python.org/2/library/subprocess.html
[logging]: https://docs.python.org/2/library/logging.html
[unittest]: https://docs.python.org/2/library/unittest.html

[nose]: https://nose.readthedocs.io/en/latest/
[coverage]: https://coverage.readthedocs.io/en/coverage-4.4.2/
[codacy]: https://github.com/codacy/python-codacy-coverage
[pycodestyle]: https://pypi.python.org/pypi/pycodestyle

[camus]: https://www.inria.fr/en/teams/camus
[inria]: https://www.inria.fr/
[wdc-bsc]: https://www.bsc.es/discover-bsc/organisation/scientific-structure/workflows-and-distributed-computing
[bsc]: https://www.bsc.es/
[cristian]: https://cristianrcv.netlify.com/

[apache-2]: http://www.apache.org/licenses/LICENSE-2.0
