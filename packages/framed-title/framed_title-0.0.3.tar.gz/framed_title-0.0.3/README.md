## Framed Title

[![PyPI](https://img.shields.io/pypi/v/framed_title)](https://pypi.org/project/framed_title/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/framed_title)]((https://pypi.org/project/framed_title/))
[![GitHub](https://img.shields.io/github/license/xelorabb/framed_title)](https://github.com/xelorabb/framed_title/blob/master/LICENSE)

Prints a framed title

#### Install
`pip install framed_title`

#### Examples

* ##### Example 1
  ```python
  a = FramedTitle(['Framed Title', 'Longer subtitle in the 2nd row'])
  a.show()
  ```
  ![example_01](https://raw.githubusercontent.com/xelorabb/framed_title/master/examples/example_01.png)

* ##### Example 2
  ```python
  b = FramedTitle(
    ['Framed Title', 'Longer subtitle in the 2nd row'],
    'double_stroke',
    ['green', 'dark'],
    'black',
    bg_color='yellow')
  b.show()
  ```
  ![example_02](https://raw.githubusercontent.com/xelorabb/framed_title/master/examples/example_02.png)

* ##### Example 3
  ```python
  c = FramedTitle(
    ['Framed Title', 'Longer subtitle in the 2nd row'],
    'stroke',
    'red',
    text_align='right',
    padding=0)
  c.show()
  ```
  ![example_03](https://raw.githubusercontent.com/xelorabb/framed_title/master/examples/example_03.png)

* ##### Example 4
  ```python
  d = FramedTitle(
    ['Framed Title', 'Longer subtitle in the 2nd row'],
    'simple',
    ['cyan', 'dark'],
    ['blue', 'dark'],
    'left',
    'gray')
  d.set_margin(2,4,2,4)
  d.set_padding(2,4)
  d.show()

  # OR #################################
  d = FramedTitle(
    ['Framed Title', 'Longer subtitle in the 2nd row'],
    'simple',
    ['cyan', 'dark'],
    ['blue', 'dark'],
    'left',
    'gray',
    [2, 4, 2, 4],
    [2, 4])
  d.show()
  ```
  ![example_04](https://raw.githubusercontent.com/xelorabb/framed_title/master/examples/example_04.png)

#### Constructor Arguments
```python
def __init__(self,
  titles,
  frame_type = 'hash',
  frame_color = 'white',
  text_color = 'white',
  text_align = 'center',
  bg_color = None,
  margin = 0,
  padding = 1
):
```

###### Argument Values
* `frame_type`: [ _stroke_ | _double_stroke_ | _simple_ | _hash_ ]
* `text_align`: [ _left_ | _center_ | _right_ ]
* See [here](https://github.com/xelorabb/yatts#color-palette) for color values
