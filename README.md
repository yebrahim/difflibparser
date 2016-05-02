# Python difflibparser
A simple parser for the python difflib ndiff that returns objects representing diff between two files

Usage
-----

left file:

    line1
    lineTwo
    lineThrees
    line4
    line6
    
right file:
    
    line1
    xlineTw0
    lineThree
    line4
    line66

difflib-parser is a simple module that parses the output of difflib.ndiff. It takes two strings and exposes a getNextLine() method that returns a dictionary that represents the next line in the diff. The return type always has a 'code' key that contains one of the following values:

    class DiffCode:
        SIMILAR = 0         # line hasn't changed between the files, its diff starts with '  '
        RIGHTONLY = 1       # line exists in the right file only, its diff starts with '+ '
        LEFTONLY = 2        # line exists in the left file only, its diff starts with '- '
        CHANGED = 3         # line has incremental changes on the left file, the diff is represented as three of four lines
                                in the order ('-', '+', '?'), ('-', '?', '+') or ('-', '?', '+', '?')

If the returned code is DiffCode.CHANGED, the result will also contain 'rightchanges' and 'rightchanges' keys, each is a list of indices that have changed on the left and right side respectively. One of these two can be None but not both.

For the two files above, these are the returned results when calling getNextLine() repetitively:

    {'code': 0, 'line': 'line1'}
    {'rightchanges': [0, 7], 'code': 3, 'newline': 'xlineTw0', 'leftchanges': [6], 'line': 'lineTwo'}
    {'rightchanges': None, 'code': 3, 'newline': 'lineThree', 'leftchanges': [9], 'line': 'lineThrees'}
    {'code': 0, 'line': 'line4'}
    {'rightchanges': [5], 'code': 3, 'newline': 'line66', 'leftchanges': None, 'line': 'line6'}

Which matches the output of difflib.ndiff:

    line1
    - lineTwo
    ?       ^
    + xlineTw0
    ? +      ^
    - lineThrees
    ?          -
    + lineThree
      line4
    - line6
    + line66
    ?      +
