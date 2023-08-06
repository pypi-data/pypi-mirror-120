# ExtensionConvertor

## Install
`pip install ExtensionConvertor`


## How to use
```python
from ExtensionConvertor import ExtensionConvertor

conv = ExtensionConvertor("hoge.jpg")
conv.replace_extension("pdf")
# >>> hoge.pdf
conv.replace_extension("pdf, "_hoge")
# >>> hoge_hoge.pdf
```
