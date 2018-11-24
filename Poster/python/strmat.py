import re


class strmat(object):
    """
    Convert `str' to `mat'.
    """
    # ------- INIT -------
    def __init__(self, string:str, SPLIT:str="\n", ELE:list=None, NUM_RE:str=None):
        # CONSTANT
        self.SPLIT = SPLIT    # 051     ┌─┐
        if ELE:               # 646 <=> | | <=> Unit
            self.ELE = ELE    # 352     └─┘
        else:
            self.ELE = [s for s in "┌┐┘└ ─|"]
        if NUM_RE:
            self.NUM_RE = NUM_RE
        else:
            self.NUM_RE = "[0-9a-zA-Z]"
        self.PARTNUM = 0
        # VARIABLE
        self.str   = string
        self.mat   = string.split(self.SPLIT)
        self.shape = (self.mat.__len__(), self.mat[0].__len__())
        self.part  = dict()
        # Pre-process
        self.__arrange()

    # ------- CONSTRUCTOR -------
    def __getitem__(self, idx):
        return self.mat[idx[0]][idx[-1]]

    def __str__(self):
        return self.SPLIT.join(self.mat)

    # ------- FUNCTIONS -------
    # ----- PUBLIC -----
    def get_box_index(self, coor, expand=None):
        """
        Get box index by coordinate.
        """
        if expand!=None: return self.get_box_index([coor,expand])
        for i in range(self.PARTNUM):
            s,e = self.part[i+1]
            if all([s[i]<=coor[i]<=e[i] for i in [0,-1]]):
                return i+1

    def get_box_shape(self, idx):
        """
        Get box shape by index.
        """
        return self.__box_shape(idx)

    def get_position(self, idx):
        """
        Get box position.
        """
        """
        start,_ = self.part[idx]
        row,col = 0,0
        _       = dict()
        for i in range(start[0]+1):
            _[self.get_box_index([i, start[-1]])] = None
        row = _.keys().__len__()
        _.clear()
        for i in range(start[-1]+1):
            _[self.get_box_index([start[0], i])] = None
        col = _.keys().__len__()
        return row-1,col-1
        """

    def is_aligned(self, idx_a, idx_b):
        """
        [up, left, down, right]
        """
        a0,a1 = self.part[idx_a]
        b0,b1 = self.part[idx_b]
        key = ["up", "left", "down", "right"]
        val = [i==j for i,j in zip(a0+a1,b0+b1)]
        return dict(zip(key, val))

    def convert_to_roman(self, num):
        """
        Convert arabic number to roman.
        """
        return self.__arabic_to_roman(num)

    def convert_to_arabic(self, char):
        """
        Convert character to arabic number.
        """
        return self.__numalpha_to_num(char)

    def convert_to_alpha(self, num):
        """
        Convert num to alphabet.
        """
        return self.__num_to_numalpha(num)

    # ----- PRIVATE -----
    def __numalpha_to_num(self, char):
        """
        123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
        str: "1-9", "a-z",  "A-Z"
        ord: 49-57, 97-122, 65-90
        num: 1-9,   10-35,  36-61
        """
        o = ord(char)
        if o in range(49, 57+1):
            return o - 48
        elif o in range(97, 122+1):
            return o - 87
        elif o in range(65, 90+1):
            return o - 29

    def __num_to_numalpha(self, num):
        """
        pass
        """
        if num in range(1, 9+1):
            return chr( num+48 )
        elif num in range(10, 35+1):
            return chr( num+87 )
        elif num in range(36, 61+1):
            return chr( num+29 )

    def __arabic_to_roman(self, num):
        """
        eg: 23 -> XXIII
        """
        numL = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        strL = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        result = ""
        for i in range(len(numL)):
             while num >= numL[i]:
                 num    -= numL[i]
                 result += strL[i]
        return result

    def __index_convert(self, num):
        """
        eg: 10 -> 0,10
        """
        row,col = self.shape
        col    += 1    # all rows have "\n".
        return num//col, (num+1)%col-1

    def __around_cuboid(self, idx):
        """
        ┌ ─˃ ┐
             |
             ˅
          <- ┘
        """
        def dct_idx(key):
            num = re.findall(self.NUM_RE, self[row,col])
            if num: key = self.__numalpha_to_num(num[0])
            return key
        # start -> end
        row,col = self.__index_convert(idx)
        start = (row,col)
        key   = 0
        while self[row,col] != self.ELE[1]:
            col += 1
        while self[row,col] != self.ELE[2]:
            row += 1
        end   = (row,col)
        while self[row,col] != self.ELE[3]:
            col -= 1
            key = dct_idx(key)
        self.part[key] = (start, end)

    def __box_shape(self, idx):
        """
        Return the shape of the box.
        len `┌' = 0.5
        len `┐' = 0.5
        len `┘' = 0.5
        len `└' = 0.5
        """
        return tuple(j-i for i,j in zip(*self.part[idx]))

    def __arrange(self):
        self.PARTNUM = re.findall(self.NUM_RE, self.str).__len__()
        idx = -1
        for i in range(self.PARTNUM):
            idx = self.str.index(self.ELE[0], idx+1)
            self.__around_cuboid(idx)



debug = False

if debug:
    from pprint import pprint

    test = """
    ┌─┐┌─┐┌───┐
    └1┘└2┘|   |
    ┌─┐┌─┐└─3─┘
    | || |┌───┐
    └4┘└5┘└─6─┘
    ┌─┐┌───┐┌─┐
    └7┘└─8─┘└9┘
    """

    obj = strmat(test.strip())
    print(obj[-1,-1])
    print(obj)
    pprint(obj.part)
    print(obj.get_box_shape(3))
    print(obj.get_box_index([2,5]))
    print(obj.is_aligned(3,4))
    print(obj.convert_to_roman(23))

    for i in "123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        tmp1 = obj._strmat__numalpha_to_num(i)
        tmp2 = obj._strmat__arabic_to_roman(tmp1)
        print(tmp1, tmp2)

    for i in "123465789":
        idx = str(obj).index(i)
        idx = obj._strmat__index_convert(idx)
        print(obj[idx])
