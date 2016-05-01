# Python difflibparser
A simple parser for the python difflib ndiff that returns objects representing diff between two files

Usage
-----

left file:

    line1
    line2
    line3
    line4
    
right file:
    
    line1
    line3
    line444
    line5

difflib-parser is a simple module that parses the output of difflib.ndiff. It takes two strings and exposes a getNextLine() method that returns a dictionary that represents the next line in the diff. The return type always has a 'code' key that contains one of the following values:

    class DiffCode:
        SIMILAR = 0         # line hasn't changed between the files, its diff starts with '  '
        RIGHTONLY = 1       # line exists in the right file only, its diff starts with '+ '
        LEFTONLY = 2        # line exists in the left file only, its diff starts with '- '
        CHANGEDLEFT = 3     # line has incremental changes on the left file, the diff is represented as two lines
                                first starts with '- ' and second with '? ' and contains '-' or '^' marks
        CHANGEDRIGHT = 4    # line has incremental changes on the right file, the diff is represented as two lines
                                first starts with '+ ' and second with '? ' and contains '+' or '^' marks

If the code is CHANGEDLEFT or CHANGEDRIGHT, the result will also contain a 'changedIndices' key that's a list of marked indices for change. For a line with code CHANGEDLEFT, these marks indicate the corresponding indices have been removed (left file only), and vice versa for CHANGEDRIGHT.

For the two files above, these are the returned results when calling getNextLine() repetitively:

    {'code': 0, 'line': 'line1'}
    {'code': 2, 'line': 'line2'}
    {'code': 0, 'line': 'line3'}
    {'code': 2, 'line': 'line4'}
    {'code': 4, 'line': 'line444', 'changedIndices': [5, 6]}
    {'code': 1, 'line': 'line5'}

Which matches the output of difflib.ndiff:

      line1
    - line2
      line3
    - line4
    + line444
    ?      ++\n
    + line5
