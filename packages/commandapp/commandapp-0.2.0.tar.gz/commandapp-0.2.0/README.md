# <img width=auto height="30" src="https://raw.githubusercontent.com/PlayerG9/PyCommandApp/master/README.assets/pycmdicon.png" alt="Pillow logo"> PyCommandApp
library to create a commandline application easily

<!--
<p align="center">
    <img width=auto height="100" src="https://raw.githubusercontent.com/PlayerG9/PyCommandApp/master/README.assets/pycmdicon.png" alt="pycmd logo">
</p>
--->

# Index
- [Installation](#installation)
- [Usage](#usage)
- [Tips](#tips)
    - [Keyword-Parameter](#keyword-parameter)


# Installation
`python3 -m pip install commandapp`  
[View on pypi.org](https://pypi.org/project/commandapp/)

# Usage
### Code
```python
from commandapp import CommandApp

app = CommandApp()


@app.register
def hello(name: str):
    r"""
    prints hello `name`
    """
    print("Hello {}".format(name))


@app.register(name="print")
def cmd_print(text: str):
    r"""
    print what he should say
    """
    print(text)


app.run()
```
### Console
```commandline
>> py myapp.py
usage: -c [-h] {hello,print} ...
>> py myapp.py -h
usage: -c [-h] {hello,print} ...

optional arguments:
  -h, --help     show this help message and exit

command:
  {hello,print}  available commands
    hello        prints hello `name`
    print        print what he should say
>> py myapp.py hello
usage: -c hello [-h] name
hello: error: the following arguments are required: name
>> py myapp.py hello "python"
Hello python
>> py myapp.py print "This package is awesome"
This package is awesome
```


# Tips
## Keyword-Parameter
### Code
```python
from commandapp import CommandApp

app = CommandApp()

@app.register
def a(param: str):
    print([param])

@app.register
def b(*, param: str):
    print([param])

app.run()
```
### Console
```commandline
>> py myapp.py a "Value"
["Value"]
>> py myapp.py b "Value"
b: error: the following arguments are required: --param
>> py myapp.py b --param "Value"
["Value"]
```
