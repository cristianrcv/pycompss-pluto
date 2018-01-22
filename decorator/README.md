Parallel Decorator
=============================

Implementation of the parallel decorator.


### Dependencies


### Test with debug

```
python nose_tests.py
```


### Test without debug                                                                                                                                                                                                                                                         

```
python -O nose_tests.py
```


### Run

```
import CodeReplacer
func = <func instance>
new_code = <path_to_file_containing_new_code>
new_func = CodeReplacer.replace(func, new_code)
```


### Clean

```
find . -name "*.pyc" -delete
```


### Run coverage

```
coverage run --omit="/usr/lib/*" nose_tests.py
coverage report -m
coverage xml
export CODACY_PROJECT_TOKEN=%Project_Token%
python-codacy-coverage -r coverage.xml
rm -f coverage.xml
```
