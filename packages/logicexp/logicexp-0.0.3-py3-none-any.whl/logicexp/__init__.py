def Or(input1,input2):
    """
    Logic for OR operation

    Parameters
    ----------

    input1 (Required) : First input value. Should be 0 or 1.
    input2 (Required) : Second input value. Should be 0 or 1.
    """
    return f"( {input1} | {input2} )"

def And(input1,input2):
    """
    Logic for AND operation

    Parameters
    ----------

    input1 (Required) : First input value. Should be 0 or 1.
    input2 (Required) : Second input value. Should be 0 or 1.
    """
    return f"( {input1} & {input2} )"

def Not(input):
    """
    Logic for NOT operation

    Parameters
    ----------

    input (Required) : Input value. Should be 0 or 1.
    """
    return "( not {} )".format(str(input))

def Xor(input1,input2):
    """
    Logic for XOR operation

    Parameters
    ----------

    input1 (Required) : First input value. Should be 0 or 1.
    input2 (Required) : Second input value. Should be 0 or 1.
    """
    return str(input1) + "^" + str(input2)

def Nand(input,input2):
    """
    Logic for NAND operation

    Parameters
    ----------

    input1 (Required) : First input value. Should be 0 or 1.
    input2 (Required) : Second input value. Should be 0 or 1.
    """
    return Not(And(input,input2))

def Nor(input,input2):
    """
    Logic for NOR operation

    Parameters
    ----------

    input1 (Required) : First input value. Should be 0 or 1.
    input2 (Required) : Second input value. Should be 0 or 1.
    """
    return Not(Or(input,input2))

def Calculate(expression):
    """
    Calculates the result of logical expression

    Parameters
    ----------

    expression (Required) : Logical expression
    """
    try:
        result = eval(expression)
        if result == True:
            return 1
        else:
            return 0
    except:
        print("Error: Invalid logical expression")
        return None