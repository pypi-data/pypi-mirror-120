# UsefulDecorators
## What is this?
UsefulDecorators is for checking file extension of function's arguments.

## How to install
You can install UsefulDecorators by pip

`pip install UsefulDecorators`


## How to use
### FileExtensionChecker
FileExtensionChecker checks the file name's extension of arguments.

```python
from UsefulDecorators.FileNameChecker import extension_checker

@extension_checker(filename1="xml")
def hoge(filename1):
    print(filename1)

hoge("hoge.xml")
# hoge.xml
hoge(filename1="hoge.xml")
# hoge.xml
hoge("hoge.pdf")
# AssertionError: filename1 requires extension xml. You specified the argument as hoge.pdf
```

### FunctionAnnotationChecker
FunctionAnnotationChecker checks the arguments' data type.
```python
from UsefulDecorators.FunctionAnnotationChecker import annotation_checker

@annotation_checker
def hoge(x: int, y: float, z: str) -> int:
    return x

hoge(1, 2.0, "3.0")
```

- FunctionAnnotationChecker can also check return value. You can check any data type and typing.Union keyword.
