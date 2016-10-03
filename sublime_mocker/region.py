'''Mocker for Sublime's Region class'''


class Region():
    '''Represents Sublimes Region class'''

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

    def __eq__(self, other):
        if self.a == other.a and \
                self.b == other.b:
            return True
        return False

    def __ne__(self, other):
        if self.a != other.a:
            return True
        if self.b != other.b:
            return True
        return False

    def __str__(self):
        return str((self.a, self.b))
