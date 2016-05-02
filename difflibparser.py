import difflib

class DiffCode:
    SIMILAR = 0         # starts with '  '
    RIGHTONLY = 1       # starts with '+ '
    LEFTONLY = 2        # starts with '- '
    CHANGEDLEFT = 3     # two lines, first starts with '+ ' or '- ' and second with '? '
    CHANGEDRIGHT = 4    # two lines, first starts with '+ ' or '- ' and second with '? '

class DifflibParser:
    def __init__(self, text1, text2):
        self.__text1 = text1
        self.__text2 = text2
        self.__diff = list(difflib.ndiff(text1.splitlines(), text2.splitlines()))
        self.__currentLineno = 0

    def getNextLine(self):
        result = {}
        if self.__currentLineno >= len(self.__diff):
            return None
        currentLine = self.__diff[self.__currentLineno]
        code = currentLine[:2]
        line = currentLine[2:]
        result['line'] = line
        if code == '  ':
            result['code'] = DiffCode.SIMILAR
        elif code == '- ':
            # check if next line indicates an incremental change
            nextLine = self.__diff[self.__currentLineno + 1] if self.__currentLineno + 1 < len(self.__diff) else None
            if nextLine and nextLine[:2] == '? ':
                result['code'] = DiffCode.CHANGEDLEFT
                self.__currentLineno += 1
                minusIndices = [i for (i,c) in enumerate(nextLine[2:]) if c in ['-', '^']]
                result['changedIndices'] = minusIndices
            else:
                result['code'] = DiffCode.LEFTONLY
        elif code == '+ ':
            # check if next line indicates an incremental change
            nextLine = self.__diff[self.__currentLineno + 1] if self.__currentLineno + 1 < len(self.__diff) else None
            if nextLine and nextLine[:2] == '? ':
                result['code'] = DiffCode.CHANGEDRIGHT
                self.__currentLineno += 1
                plusIndices = [i for (i,c) in enumerate(nextLine[2:]) if c in ['+', '^']]
                result['changedIndices'] = plusIndices
            else:
                result['code'] = DiffCode.RIGHTONLY
        self.__currentLineno += 1
        return result
