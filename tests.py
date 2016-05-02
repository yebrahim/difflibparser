from difflibparser import *

file1 = '''
line1
lineTwo
lineThrees
line4
line6
'''

file2 = '''
line1
xlineTw0
lineThree
line4
line66
'''

diff = difflib.ndiff(file1.splitlines(), file2.splitlines())
for line in diff:
    print(line)

print('---------\n')

differ = DifflibParser(file1.splitlines(), file2.splitlines())

for line in differ:
    print(line)
