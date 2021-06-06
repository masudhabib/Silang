from rply.token import BaseBox
from errors import *


class Program(BaseBox):
    def __init__(self, statement):
        self.statements = []
        self.statements.append(statement)

    def add_statement(self, statement):
        self.statements.insert(0, statement)

    def evaluate(self, env):
        # print "count: %s" % len(self.statements)
        result = None
        for statement in self.statements:
            result = statement.evaluate(env)
            # print result.to_string()
        return result

    def get_statements(self):
        return self.statements


class Null(BaseBox):
    def evaluate(self, env):
        return self

    def to_string(self):
        return 'null'


class Boolean(BaseBox):
    def __init__(self, value):
        self.value = bool(value)

    def evaluate(self, env):
        return self.value

    def to_string(self):
        if self.value:
            return "true"
        else:
            return "false"


class Integer(BaseBox):
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value

    def to_string(self):
        if self.value % 1 == 0:
            return str(int(self.value))
        elif self.value % 1 == 0:
            return str(int(self.value))


class String(BaseBox):
    def __init__(self, value):
        self.value = str(value)

    def evaluate(self, env):
        return self

    def to_string(self):
        return f'{self.value}'


class Variable(BaseBox):
    def __init__(self, name):
        self.name = str(name)
        self.value = None

    def getname(self):
        return str(self.name)

    def evaluate(self, env):
        if env.variables.get(self.name, None) is not None:
            self.value = env.variables[self.name].evaluate(env)
            return self.value
        raise LogicError("Not yet defined")

    def to_string(self):
        return str(self.name)


class If(BaseBox):
    def __init__(self, condition, body, else_body=Null()):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def evaluate(self, env):
        # print("self.condition.evaluate(env)", self.condition.evaluate(env))
        condition = self.condition.evaluate(env)
        if condition:
            # print("should not come here")
            return Boolean(self.body.evaluate(env))
        else:
            if type(self.else_body) is not Null:
                # print("should come here")
                return Boolean(self.else_body.evaluate(env))
        return Null()


class While(BaseBox):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def evaluate(self, env):
        condition = self.condition.evaluate(env)
        while condition:
            self.body.evaluate(env)
            condition = self.condition.evaluate(env)
        return


class For(BaseBox):
    def __init__(self, item, sequence, body):
        self.item = item
        self.sequence = sequence
        self.body = body

    def evaluate(self, env):
        if isinstance(self.item, Variable):
            # if env.variables.get(self.left.getname(), None) is None:
            #     env.variables[self.left.getname()] = self.right
            #     return self.right.evaluate(env)
            # otherwise raise error
            # raise WrongVarError(self.left.getname())
            list = self.sequence.to_list()
            for i in list:
                # print(i.value)
                env.variables[self.item.getname()] = i
                # print(self.body)
                self.body.evaluate(env)
            return
        else:
            raise LogicError("Error: Cannot assign, is not an instance")


class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_string(self):
        return 'BinaryOp'


class Equal(BinaryOp):
    def evaluate(self, env):
        # print(self.left.evaluate(env), self.right.evaluate(env))
        # print(self.left.evaluate(env) == self.right.evaluate(env))
        # print(Boolean(self.left.evaluate(env) == self.right.evaluate(env)).value)
        return Boolean(self.left.evaluate(env) == self.right.evaluate(env))


class NotEqual(BinaryOp):
    def evaluate(self, env):
        result = self.left.evaluate(env) == self.right.evaluate(env)
        result = not result
        return result


class Add(BinaryOp):
    def evaluate(self, env):
        return Integer(self.left.evaluate(env) + self.right.evaluate(env))


class Sub(BinaryOp):
    def evaluate(self, env):
        return Integer(self.left.evaluate(env) - self.right.evaluate(env))


class Mul(BinaryOp):
    def evaluate(self, env):
        return Integer(self.left.evaluate(env) * self.right.evaluate(env))


class Div(BinaryOp):
    def evaluate(self, env):
        return Integer(self.left.evaluate(env) / self.right.evaluate(env))


class Assignment(BinaryOp):
    def evaluate(self, env):
        if isinstance(self.left, Variable):
            # if env.variables.get(self.left.getname(), None) is None:
            #     env.variables[self.left.getname()] = self.right
            #     return self.right.evaluate(env)
            # # otherwise raise error
            # raise ImmutableError(self.left.getname())
            env.variables[self.left.getname()] = self.right
            return self.right.evaluate(env)
        else:
            raise LogicError("Error: Cannot assign, is not an instance")


class List(BaseBox):
    def map(self, fun, ls):
        nls = []
        for l in ls:
            nls.append(fun(l))
        return nls

    def __init__(self, statements):
        self.values = [statements]
        # if statements:
        #     self.statements = statements

    # def get_statements(self):
    #     return self.statements

    def push(self, statement):
        self.values.insert(0, statement)

    def append(self, statement):
        self.values.append(statement)

    def index(self, i):
        if type(i) is Integer:
            return self.values[i.value]
        raise LogicError("Cannot index with that value")

    def to_list(self):
        return self.values

    def evaluate(self, env):
        if len(self.values) == 0:
            # print("self.statements", type(self.values))
            self.values += self.values
        return self

    def to_string(self):
        return '[%s]' % (", ".join(self.map(lambda x: x.to_string(), self.values)))


class Index(BinaryOp):
    def evaluate(self, env):

        left = self.left.evaluate(env)
        if type(left) is List:
            return left.index(self.right.evaluate(env))

        raise LogicError("Cannot index this")


class Print(BaseBox):
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        if hasattr(self.value.evaluate(env), 'to_string'):
            print(self.value.evaluate(env).to_string())
            return self.value.evaluate(env).to_string()
        else:
            print(str(self.value.evaluate(env)))
            return self.value.evaluate(env)


class Addition(BaseBox):
    def __init__(self, item):
        self.item = item

    def evaluate(self, env):
        if isinstance(self.item, Variable):
            env.variables[self.item.getname()].value = env.variables[self.item.getname()].value + 1
            # print(env.variables[self.item.getname()].value)
            return
        else:
            raise LogicError("Error: Cannot assign, is not an identifier")