#!/usr/bin/python
class Cell:
    def __init__(self, name, value, position, parents, formula):
            self.name = name
            self.value = value
            self.position = position
            self.parents = parents
            self.formula = formula
            self.children = []

            for parent in parents:
                parent.children.append(self)
    def __repr___(self):
        return self.name

    def displayCell(self):
        print "Value of ", self.name, ": ", self.value
        print "Position: ", self.position

    def set_value(self, new_value):
        self.value = new_value
        #update value of children
        for child in self.children:
            child.recompute()

    def recompute(self):
        #takes into account value of parents and calculates the new value of the current cell
        #prepare the argument/ get individual values as list
        parent_values = []
        for parent in self.parents:
            parent_values.append(parent.value)
        #call formula
        self.value = self.formula(parent_values)

        #recursive call on all cells below it
        for child in self.children:
            child.recompute()

class Formula:
    def __init__(self, formula):
        self.formula = formula

    def __str__(self):
        return self.__repr__();
# $A1
class Var(Formula):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Var(%s)" % self.name

# formula + formula
class Add(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "Add(%s, %s)" % (self.left, self.right)

class Mult(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return "Mult(%s, %s)" % (self.left, self.right)

def parser(tokens):
    #while token not empty do
    #put variable on variable_stack and other on operation_stack
    #if the operation is * AND no ( follows, compute
    #else continue
    var_stack = []
    op_stack = []

    while len(tokens) != 0:
        cur_token = tokens.pop(0)
        #Error if we have two consecutive operations or variables
        if len(tokens) != 0 and cur_token[0] == "$" and tokens[0][0] == "$":
            print "ERROR, Formula is incorrect, we cannot have two consecutive var"
            return
        elif len(tokens) != 0 and cur_token[0] != "$"  and tokens[0][0] != "$" and cur_token[0] != "(" and cur_token[0] != ")" and tokens[0][0] != "(" and tokens[0][0] != ")":
            print "ERROR, Formula is incorrect, we cannot have two consecutive op"
            return
        if cur_token[0] == "$": #checks if it is a variable
            var_stack.append(cur_token)
        elif cur_token == "+" or cur_token == "(":
            op_stack.append(cur_token)
        elif cur_token == "*" and tokens[0] == "(":
            op_stack.append(cur_token)
        elif cur_token == "*":
            #compute right away and push onto stack
            if len(var_stack) < 1 or len(tokens) == 0 or tokens[0][0] != "$":
                print "Error, not enough variables"
                return
            var1 = var_stack.pop()
            var2 = tokens.pop(0)
            var_stack.append(Mult(var1, var2))
        elif cur_token == ")":
            cur_op = op_stack.pop()
            while cur_op != "(":
                if cur_op == "+":
                    if len(var_stack) < 2:
                        print "Error, not enough variables"
                        return
                    var2 = var_stack.pop()
                    var1 = var_stack.pop()
                    var_stack.append(Add(var1, var2))
                cur_op = op_stack.pop()
        else:
            print "ERROR, incorrect formula, %s is not a valid token" % cur_token
            return

    while len(op_stack) != 0:
        cur_op = op_stack.pop()
        if cur_op == "+":
            if len(var_stack) < 2:
                print "Error, not enough variables"
                return
            var2 = var_stack.pop()
            var1 = var_stack.pop()
            var_stack.append(Add(var1, var2))
        if cur_op == "*":
            if len(var_stack) < 2:
                print "Error, not enough variables"
                return
            var2 = var_stack.pop()
            var1 = var_stack.pop()
            var_stack.append(Mult(var1, var2))
    return var_stack

while True:
    text = raw_input("> ")
    print parser(text.split(" "))
