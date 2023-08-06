# ATUS Transformer package

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This package contains two functions. One of them transforms the original ATUS activity codes into 11 broad categories: 
1. Sleep
2. Personal Care
3. Housework
4. Child Care
5. Adult Care
6. Work and Education
7. Shopping
8. TV Watching
9. Eating
10. Leisure
11. Travel and Other

The second function recodes transformed activity codes into string names.

## Installation

```
pip install ATUS-Transformer
```

## Usage

- There is (for now) 2 functions:
  - activityDictionary(). The arguments is a string containing ATUS original activity code.
  - activityNumberToString(). The argument is a number between 1 and 11.

## Example: activityDictionary

```
import atus_transformer
atus_transformer.activityDictionary("10101")
```
**Output**

```
1
```

## Note

- Contributions are welcome. Contact: kamilakolpashnikova@gmail.com

## Author

Kamila Kolpashnikova 2021