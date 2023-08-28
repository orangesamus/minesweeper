class Square(object):
    def __init__(self, bomb, number, flag):
        self.bomb = bomb
        self.number = number
        self.flag = flag

    def getBomb(self):
        return self.bomb

    def getNumber(self):
        return self.number

    def __str__(self):
        return "has a bomb? %s, number is a %i" % (self.bomb, self.number)



