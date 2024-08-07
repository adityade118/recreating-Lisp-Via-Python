Memory = {}

fncnDefined = {}

stack = []


def convertToList(operator_String):
    input_str_list = []
    string = ""
    input_evaluable = operator_String[1:-1]
    input_evaluable += " "
    i = 0
    while i < len(input_evaluable):
        ch = input_evaluable[i]
        if ch == "(":
            braceOpen: int = -1  # just to know when we invoke the while loop, else double count the first brace
            while braceOpen != 0:
                if braceOpen == -1:
                    braceOpen = 0  # to start the while loop with braceOpen = 0
                ch = input_evaluable[i]
                string += ch
                if ch == "(":
                    braceOpen += 1
                elif ch == ")":
                    braceOpen -= 1
                i += 1

        elif ch == " ":
            input_str_list.append(string)
            string = ""
            i += 1

        else:
            string += ch
            i += 1

    return input_str_list


class Operation:
    def __init__(self, string):
        self.string = string

    def eval(self):
        operation_List = convertToList(self.string)
        operator = operation_List[0]
        # arithmetic operations
        if operator == "+":
            out: int = 0
            for i in range(1, len(operation_List)):
                out += Value(operation_List[i]).value
            return out
        if operator == "*":
            out = 1
            for i in range(1, len(operation_List)):
                out *= Value(operation_List[i]).value
            return out

        # logical operations
        if operator == "=":
            return Value(operation_List[1]).value == Value(operation_List[2]).value
        if operator == "<":
            return Value(operation_List[1]).value < Value(operation_List[2]).value
        if operator == "and":
            return Value(operation_List[1]).value and Value(operation_List[2]).value
        if operator == "or":
            return Value(operation_List[1]).value or Value(operation_List[2]).value

        # memory operations
        if operator == "set":
            Memory[operation_List[1]] = Value(operation_List[2]).value
            return Memory[operation_List[1]]  # issue 3 solved

        # conditional operations
        if operator == "if":
            if len(operation_List) == 3:
                if Value(operation_List[1]).value:
                    return Value(operation_List[2]).value
                else:
                    return None
            else:
                if Value(operation_List[1]).value:
                    return Value(operation_List[2]).value
                else:
                    return Value(operation_List[3]).value

        # while loop
        '''
        > (set a 1)
        1
        > (set b 1)
        1
        > (while (< a 9) (set b (* b a)) (set a (+ 1 a)))
        0
       '''
        if operator == "while":
            while True:
                if Value(operation_List[1]).value:
                    for i in range(2, len(operation_List)):
                        Operation(operation_List[i]).eval()
                else:
                    break
            return 0

        # function

        # function definition
        if operator == "defun":
            funcsName = operation_List[1]
            arg = operation_List[2]
            i = 3
            fnc_body = []
            while i < len(operation_List):
                fnc_body += [operation_List[i]]
                i += 1
            fncnDefined[funcsName] = [arg, fnc_body]
            return fncnDefined[funcsName]

        # function call
        if operator in fncnDefined.keys():
            stack.append(Memory.copy())
            parameters = convertToList(fncnDefined[operator][0])
            for i in range(len(parameters)):
                Memory[parameters[i]] = Value(operation_List[i + 1]).value

            for i in range(len(fncnDefined[operator][1]) - 1):
                Operation(fncnDefined[operator][1][i]).eval()

            out = Operation(fncnDefined[operator][1][-1]).eval()
            Memory.clear()
            Mem = stack.pop()
            Memory.update(Mem)
            return out


class Value:
    def __init__(self, string):
        if string[0] == "(" and string[-1] == ")":
            string = Operation(string)
            self.value = string.eval()
        elif string in Memory.keys():
            self.value = Memory[string]
        else:
            self.value = int(string)


while True:
    command = input("> ")
    if command == "exit":
        break
    print(Operation(command).eval())
