from rply.token import BaseBox


class Number(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()


class Sub(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()


class Mul(BinaryOp):
    def eval(self):
        return self.left.eval() * self.right.eval()


class Div(BinaryOp):
    def eval(self):
        return self.left.eval() / self.right.eval()

class Pow(BinaryOp):
    def eval(self):
        return self.left.eval() ** self.right.eval()


class Boolean(BaseBox):
    def init(self, value):
        self.value = bool(value)

    def eval(self, env):
        return self

    def to_string(self):
        return str(self.value).lower()



