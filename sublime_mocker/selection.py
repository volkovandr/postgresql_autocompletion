'''Mocker for Sublime's Selection class'''


class Selection():
    '''Represents Sublimes Selection class'''
    a = 0
    b = 0

    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b

    def begin(self):
        if self.a < self.b:
            return self.a
        else:
            return self.b

    def end(self):
        if self.b > self.a:
            return self.b
        else:
            return self.a
