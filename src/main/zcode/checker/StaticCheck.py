from AST import *
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce

VOIDTYPE = 0
NONETYPE = 1
NUMTYPE = 2
STRINGTYPE = 3
BOOLTYPE = 4
FUNC_DEFINITION = 5
FUNC_DECLARATION = 6

FOR_ENV = 1
FUNC_ENV = 2
NONE_ENV = 3

class FunctionStructure():
    def __init__(self, name, params, return_type, declare_type):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.declare_type = declare_type

class ArrayStructure():
    def __init__(self, eleType):
        self.eleType = eleType

    def __eq__(self, other):
        if isinstance(other, ArrayStructure):
            return self.eleType == other.eleType
        else:
            return False
        
    def __hash__(self):
        return hash(self.eleType)
    
    def __str__(self):
        return f"ArrayStructure: {str(self.eleType)}"

class StaticChecker(BaseVisitor, Utils):
    def visitProgram(self, ast, param):
        param = [(NONE_ENV, {})]

        for i in ast.decl:
            self.visit(i, param)

        _, var_dict = param[0]
        if not ('main' in var_dict): raise NoEntryPoint()

        fnDeclaration = list(filter(lambda x: isinstance(x, FunctionStructure) and x.declare_type == FUNC_DECLARATION, var_dict.values()))
        if len(fnDeclaration) > 0: raise NoDefinition(fnDeclaration[0].name)

    # How can VarDecl know that the current declaration is param, function or variable
    def visitVarDecl(self, ast, param):
        _, cur_env = param[0]
        try:
            id_instance = self.visit(ast.name, [param[0]])
        except Undeclared as e:
            id_instance = None
        
        id_name = ast.name.name
        if id_instance != None:
            raise Redeclared(Variable(), id_name)
        else:
            valueType = self.visit(ast.varInit, param) if ast.varInit else NONETYPE
            if ast.varType: 
                varType = self.visit(ast.varType, param)

                if valueType != NONETYPE and varType != valueType: 
                    raise TypeMismatchInStatement(ast)
                else:
                    cur_env[id_name] = varType
            else: 
                if isinstance(valueType, ArrayStructure):
                    raise TypeMismatchInStatement(ast)
                
                # Incase 'var' type này thì assignment trước đã luôn đảm bảo là var sẽ có expression => valueType != NONETYPE
                cur_env[id_name] = valueType

        return VOIDTYPE

    # Do we have case: func a(number x)
            # func a(number x, number y) ?

    # Do we have case: number a
            # func a()

    # Do we have case: func a(number x)
            # func a(number x, number y) return 1
    def visitFuncDecl(self, ast, param):
        _, cur_env = param[0]

        new_env = (FUNC_ENV, {})
        if ast.body is None:
            decl_type = FUNC_DECLARATION 
            fn_type = None
        else:
            decl_type = FUNC_DEFINITION
            fn_type = self.visit(ast.body, [new_env] + param)

        try:
            fn_instance = self.visit(ast.name, [param[0]])
        except Undeclared as e:
            fn_instance = None

        if fn_instance is not None:
            # Incase the function name is in the envir, we need to check many conditions
            if isinstance(fn_instance, FunctionStructure):
                # Incase the exist function name is declaration
                if fn_instance.declare_type == FUNC_DECLARATION:
                    # Incase declare the function name again => Raise Error. 
                    # If the decl_type is FUNCTION_DEFINITION then we will remake the instance FunctionStructure
                    if decl_type == FUNC_DECLARATION: 
                        raise Unname("function being redeclared")
                # Incase the exist function name is definition
                else: 
                    raise Redeclared(kind=Function(), name=fn_instance.name)
            else:
                raise Unname("Declare the function name with the same identifier name")

        # Construct the FunctionStructure Instance
        try:
            for i in ast.param: 
                self.visit(i, [new_env])
        except Redeclared as e: 
            raise Redeclared(kind=Parameter(), name=e.name)
        
        fn_name = ast.name.name
        fn_instance = FunctionStructure(fn_name, 
                                        [self.visit(i.name, [new_env]) for i in ast.param], 
                                        fn_type, 
                                        decl_type)
        cur_env[fn_name] = fn_instance

        return VOIDTYPE

# ---------------------------------------------------------------- BIN / UNI OPERATION

    def visitBinaryOp(self, ast, param):
        typeOperand_1 = self.visit(ast.left, param)
        typeOperand_2 = self.visit(ast.right, param)

        if typeOperand_1 == NONETYPE or typeOperand_2 == NONETYPE: raise TypeCannotBeInferred(ast)

        if ast.op in ['+', '-', '*', '/', '%']:
            if not (typeOperand_1 == NUMTYPE and typeOperand_2 == NUMTYPE): raise TypeMismatchInExpression(ast)
            else: return NUMTYPE

        elif ast.op in ['and', 'or']:
            if not (typeOperand_1 == BOOLTYPE and typeOperand_2 == BOOLTYPE): raise TypeMismatchInExpression(ast)
            else: return BOOLTYPE

        elif ast.op in ['...']:
            if not (typeOperand_1 == STRINGTYPE and typeOperand_2 == STRINGTYPE): raise TypeMismatchInExpression(ast)
            else: return STRINGTYPE

        elif ast.op in ['=', '!=', '<', '>', '<=', '>=']:
            if not (typeOperand_1 == NUMTYPE and typeOperand_2 == NUMTYPE): raise TypeMismatchInExpression(ast)
            else: return NUMTYPE

        elif ast.op in ['==']:
            if not (typeOperand_1 == STRINGTYPE and typeOperand_2 == STRINGTYPE): raise TypeMismatchInExpression(ast)
            else: return STRINGTYPE

    def visitUnaryOp(self, ast, param):
        typeOperand = self.visit(ast.operand, param)

        if typeOperand == NONETYPE: raise TypeCannotBeInferred(ast)

        if typeOperand == 'not':
            if typeOperand != BOOLTYPE: raise TypeMismatchInExpression(ast)
            else: return BOOLTYPE
        
        elif ast.op == '-':
            if typeOperand != NUMTYPE: raise TypeMismatchInExpression(ast)
            else: return NUMTYPE

# ---------------------------------------------------------------- Statements

    # Incase: {'if else':'NUMTYPE', 'if else': 'BOOLTYPE'} . How can we check and sure about this ???
    # Incase: {'return NUMTYPE', 'return BOOLTYPE'} . How can we check and sure about this ???
    def visitBlock(self, ast, param):
        cur_env_name, _ = param[0]
        new_env = (cur_env_name, {})

        return_type = list(map(
            lambda stmt: self.visit(stmt, [new_env] + param), 
            ast.stmt))
        
        # Getting the return type for the block statement (Incase block statement have multiple return statements) => Get the first return statement
        for i in return_type:
            if i != VOIDTYPE: return i
        return VOIDTYPE


    def visitIf(self, ast, param):
        cur_env_name, _ = param[0]
        new_env = (cur_env_name, {})

        ifExprType = self.visit(ast.expr, param) == BOOLTYPE
        stmt_type = [self.visit(ast.thenStmt, [new_env] + param)]

        elif_stmt_type, elifExprType = [], []
        for expr, stmt in ast.elifStmt:
            elifExprType.append(self.visit(expr, param) == BOOLTYPE)
            elif_stmt_type.append(self.visit(stmt, [new_env] + param))

        if ifExprType and all(elifExprType): raise TypeMismatchInStatement(ast)

        else_stmt_type = [self.visit(ast.elseStmt, [new_env] + param)] if ast.elseStmt else []

        # In this set, all element must be the same type (VOIDTYPE or other TYPE) -> Cannot have multiple return type
        return_type = set(stmt_type + elif_stmt_type + else_stmt_type)
        if len(return_type) == 1: 
            return return_type.pop()
        else: 
            raise TypeCannotBeInferred(ast)

    def visitFor(self, ast, param):
        new_env = (FOR_ENV, {})

        condType = self.visit(ast.condExpr, param)
        idType = self.visit(ast.name, param)

        if condType != BOOLTYPE or idType != NUMTYPE: raise TypeMismatchInStatement(ast)

        return_type = self.visit(ast.body, [new_env] + param)
        return return_type

    def visitContinue(self, ast, param):
        cur_env_type, _ = param[0]
        if cur_env_type != FOR_ENV: 
            raise MustInLoop(ast)
        else: 
            return VOIDTYPE

    def visitBreak(self, ast, param):
        cur_env_type, _ = param[0]
        if cur_env_type != FOR_ENV: 
            raise MustInLoop(ast)
        else:
            return VOIDTYPE

    def visitReturn(self, ast, param):
        if ast.expr: 
            return self.visit(ast.expr, param)
        else: 
            return VOIDTYPE

    def visitAssign(self, ast, param):
        left_type = self.visit(ast.lhs, param)
        right_type = self.visit(ast.rhs, param)

        if left_type == NONETYPE and right_type == NONETYPE: raise TypeCannotBeInferred(ast)
        elif left_type == NONETYPE: # => Inferred to the left type
            pass
        else:
            if left_type != right_type: raise TypeMismatchInStatement(ast)
            else: return VOIDTYPE

    def InferredType(self, ast, param, inferred_type):
        ...

    # Check the input param type ?
    def visitCallStmt(self, ast, param):
        try: 
            fn_instance = self.visit(ast.name, param)
        except Undeclared as e: 
            raise Undeclared(kind=Function(), name=e.name)
        
        if isinstance(fn_instance, FunctionStructure):
            if fn_instance.return_type != VOIDTYPE or len(fn_instance.params) != len(ast.args):
                raise TypeMismatchInExpression(ast)
            else: 
                for in_param, fn_param in zip(ast.args, fn_instance.params):
                    in_type = self.visit(in_param, param)
                    if in_type == NONETYPE: 
                        raise TypeCannotBeInferred(ast)
                    else:
                        if in_type != fn_param: 
                            raise TypeCannotBeInferred(ast)
                        
                return VOIDTYPE
        else: # What will return when call a varable is as function
            raise Unname("Cannot call a non-function type id")
        
    # Incase use a variable as a callee (number a; a()) ???
    def visitCallExpr(self, ast, param):
        try:
            fn_instance = self.visit(ast.name, param)
        except Undeclared as e:
            raise Undeclared(kind=Function(), name=e.name)

        if isinstance(fn_instance, FunctionStructure):
            if fn_instance.return_type == VOIDTYPE or len(fn_instance.params) != len(ast.args):
                raise TypeMismatchInExpression(ast)
            else: 
                for in_param, fn_param in zip(ast.args, fn_instance.params):
                    in_type = self.visit(in_param, param)
                    if in_type == NONETYPE: 
                        raise TypeCannotBeInferred(ast)
                    else:
                        if in_type != fn_param: 
                            raise TypeCannotBeInferred(ast)
                        
                return fn_instance.return_type
        else: # What will return when call a varable is as function
            raise Unname("Cannot call a non-function type id")

# ---------------------------------------------------------------- Literal Identification

    def visitId(self, ast, param):
        instance = [env[ast.name] for _, env in param if ast.name in env]
        if len(instance) == 0: 
            raise Undeclared(kind=Variable(), name=ast.name)
        else: 
            return instance[0]

    # If no error occurs, return NUMTYPE, BOOLTYPE, STRINTYPE, or ArrayStructure (in case [[1,2,3], [4,5,6]])
    # Incase a[1,2,3] if a is 3D array -> it will not out of boundary. Otherwise, what error will we raise ?
    def visitArrayCell(self, ast, param):            
        arrType = self.visit(ast.arr, param)
        numTypeIdx = all([self.visit(index, param) == NUMTYPE for index in ast.idx])

        if numTypeIdx == True and isinstance(arrType, ArrayStructure):
            try: 
                eleType = reduce(lambda acc, _: acc.eleType, range(len(ast.idx)), arrType)
                return eleType
            except: 
                raise Unname("Indexing out of boundary")
        else: 
            raise TypeMismatchInExpression(ast)

    def visitNumberLiteral(self, ast, param):
        return NUMTYPE

    def visitBooleanLiteral(self, ast, param):
        return BOOLTYPE

    def visitStringLiteral(self, ast, param):
        return STRINGTYPE

    # What will we return if Element in array is not same type ?
    def visitArrayLiteral(self, ast, param):
        elementsType = set(list(map(lambda x: self.visit(x, param), ast.value)))

        if len(elementsType) > 1: 
            raise Unname("Element in array is not same type")
        else:
            return ArrayStructure(elementsType.pop())
    
# ---------------------------------------------------------------- Type Identification

    def visitNumberType(self, ast, param):
        return NUMTYPE

    def visitBoolType(self, ast, param):
        return BOOLTYPE

    def visitStringType(self, ast, param):
        return STRINGTYPE
    
    def visitVoidType(self, ast, param):
        return VOIDTYPE

    def visitArrayType(self, ast, param):
        def arrayTypeRecursive(num_lit):
            if len(num_lit) == 0: return self.visit(ast.eleType, param)
            else:
                if not isinstance(num_lit[0], float):
                    raise TypeMismatchInStatement(ast)                                
                return ArrayStructure(arrayTypeRecursive(num_lit[1:]))
        
        return arrayTypeRecursive(ast.size)