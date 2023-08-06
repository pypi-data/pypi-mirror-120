# PyCommandApp
tool to create a commandline application easily


# usage
`python3 -m pip install commandapp` (not implemented yes)
```python
from commandapp import CommandApp

app = CommandApp()


@app.register
def hello(name: str):
    print("Hello {}".format(name))


@app.register(name="print")
def cmd_print(text: str):
    print(text)


app.run()
```
