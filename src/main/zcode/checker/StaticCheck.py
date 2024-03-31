from AST import *
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce

class Type(ABC):
    def __eq__(self, other):
        return type(self) == type(other)

class NumType(Type):
    def __str__(self):
        return "NumType"
        
class StringType(Type): 
    def __str__(self):
        return "StringType"
        
class BoolType(Type): 
    def __str__(self):
        return "BoolType"
        
class NoneType(Type): 
    def __str__(self):
        return "NoneType"

class VoidType(Type): 
    def __str__(self):
        return "VoidType"

class FunctionType(Type):
    def __init__(self, id:str, params:list[type], return_type:Type, declare_type:int):
        super(FunctionType, self).__init__()
        self.name = id
        self.params = params
        self.return_type = return_type
        self.declare_type = declare_type
        
    def __eq__(self, other):
        if super(FunctionType, self).__eq__(other):
            return self.return_type == other.return_type
        
    def __str__(self):
        return "FunctionType"

class ArrayType(Type):
    def __init__(self, eleType:Type):
        super(ArrayType, self).__init__()
        self.eleType = eleType

    def __eq__(self, other):
        if super(ArrayType, self).__eq__(other):
            return self.eleType == other.eleType
        else:
            return False
    
    def __str__(self):
        return f"ArrayType: {str(self.eleType)}"

class Utils():
    def InferType(name:str, inferType:type, genEnv: list[dict]):
        for env in genEnv:
            if name in env:
                env[name] = inferType
                return inferType
        else:
            raise Exception(f"Variable {name} not found in general environment")

FUNC_DEFINITION = 5
FUNC_DECLARATION = 6

FOR_ENV = 1
FUNC_ENV = 2
NONE_ENV = 3

class StaticChecker(BaseVisitor, Utils):
    def visitProgram(self, ast, param):
        param = [(NONE_ENV, {})]

        for i in ast.decl:
            self.visit(i, param)

        _, var_dict = param[0]
        if not ('main' in var_dict): raise NoEntryPoint()

        fnDeclaration = list(filter(lambda x: type(x) is FunctionType and x.declare_type == FUNC_DECLARATION, var_dict.values()))
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
            valueType = self.visit(ast.varInit, param) if ast.varInit else NoneType()
            if ast.varType: 
                varType = self.visit(ast.varType, param)

                if (type(valueType) is not NoneType) and varType != valueType:
                    raise TypeMismatchInStatement(ast)
                else:
                    cur_env[id_name] = varType
            else: 
                if type(valueType) is ArrayType:
                    raise TypeMismatchInStatement(ast)
                
                # Incase 'var' type này thì assignment trước đã luôn đảm bảo là var sẽ có expression => valueType != NONETYPE
                cur_env[id_name] = valueType

        return VoidType()

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
            if type(fn_instance) is FunctionType:
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
        fn_instance = FunctionType(fn_name, 
                                        [self.visit(i.name, [new_env]) for i in ast.param], 
                                        fn_type, 
                                        decl_type)
        cur_env[fn_name] = fn_instance

        return VoidType()

# ---------------------------------------------------------------- BIN / UNI OPERATION

    def visitBinaryOp(self, ast, param):
        def on_check(inferType:Type):
            typeOperand_1 = self.visit(ast.left, param)
            typeOperand_2 = self.visit(ast.right, param)
            
            if (type(typeOperand_1) is inferType) and (type(typeOperand_2) is inferType):
                return typeOperand_1
            else:
                if type(typeOperand_1) is NoneType:
                    typeOperand_1 = Utils.InferType(ast.left.name, inferType(), param)
                if type(typeOperand_2) is NoneType:
                    typeOperand_2 = Utils.InferType(ast.right.name, inferType(), param)
                if not ((type(typeOperand_1) is inferType) and (type(typeOperand_2) is inferType)):
                    raise TypeMismatchInExpression(ast)
                else:
                    return typeOperand_1

        if ast.op in ['+', '-', '*', '/', '%']:
            return on_check(NumType)

        elif ast.op in ['and', 'or']:
            return on_check(BoolType)

        elif ast.op in ['...']:
            return on_check(StringType)

        elif ast.op in ['=', '!=', '<', '>', '<=', '>=']:
            return on_check(NumType)

        elif ast.op in ['==']:
            return on_check(StringType)

    def visitUnaryOp(self, ast, param):
        def on_check(correctType):
            typeOperand = self.visit(ast.operand, param)
            
            if type(typeOperand) is correctType:
                return typeOperand
            elif type(typeOperand) is NoneType:
                return Utils.InferType(ast.operand.name, correctType())
            else:
                raise TypeMismatchInExpression(ast)

        if ast.op == 'not':
            on_check(BoolType)
        
        elif ast.op == '-':
            on_check(NumType)

# ---------------------------------------------ast)--------------- Statements

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
            if type(i) is not VoidType:
                return i
        return VoidType()


    def visitIf(self, ast, param):
        cur_env_name, _ = param[0]
        new_env = (cur_env_name, {})

        ifExprType = type(self.visit(ast.expr, param)) is BoolType
        stmt_type = [self.visit(ast.thenStmt, [new_env] + param)]

        elif_stmt_type, elifExprType = [], []
        for expr, stmt in ast.elifStmt:
            elifExprType.append(type(self.visit(expr, param)) is BoolType)
            elif_stmt_type.append(self.visit(stmt, [new_env] + param))

        if ifExprType and all(elifExprType): 
            raise TypeMismatchInStatement(ast)

        else_stmt_type = [self.visit(ast.elseStmt, [new_env] + param)] if ast.elseStmt else []

        # In this set, all element must be the same type (VoidType or other Type) -> Cannot have multiple return type
        return_type_list = [i for i in stmt_type + elif_stmt_type + else_stmt_type if type(i) is not VoidType]
        if len(return_type_list) == 0:
            return VoidType()
        elif len(return_type_list) == 1: 
            return return_type_list[0]
        else: 
            raise TypeCannotBeInferred(ast)

    def visitFor(self, ast, param):
        new_env = (FOR_ENV, {})

        condType = self.visit(ast.condExpr, param)
        idType = self.visit(ast.name, param)

        if (type(condType) is not BoolType) or (type(idType) is not NumType): 
            raise TypeMismatchInStatement(ast)

        return self.visit(ast.body, [new_env] + param)

    def visitContinue(self, ast, param):
        cur_env_type, _ = param[0]
        if cur_env_type != FOR_ENV: 
            raise MustInLoop(ast)
        else: 
            return VoidType()

    def visitBreak(self, ast, param):
        cur_env_type, _ = param[0]
        if cur_env_type != FOR_ENV: 
            raise MustInLoop(ast)
        else:
            return VoidType()

    def visitReturn(self, ast, param):
        if ast.expr: 
            return self.visit(ast.expr, param)
        else: 
            return VoidType()

    def visitAssign(self, ast, param):
        left_type = self.visit(ast.lhs, param)
        right_type = self.visit(ast.rhs, param)

        if (type(left_type) is NoneType) and (type(right_type) is NoneType): 
            raise TypeCannotBeInferred(ast)
        elif type(left_type) is NoneType: # => Inferred to the left type
            Utils.InferType(ast.lhs.name, right_type, param)
        elif type(right_type) is NoneType: # => Inferred to the right type
            Utils.InferType(ast.rhs.name, left_type, param)
        else:
            if type(left_type) != type(right_type): raise TypeMismatchInStatement(ast)
        
        return VoidType()

    # Check the input param type ?
    def visitCallStmt(self, ast, param):
        try: 
            fn_instance = self.visit(ast.name, param)
        except Undeclared as e: 
            raise Undeclared(kind=Function(), name=e.name)
        
        if type(fn_instance) is FunctionType:
            if (type(fn_instance.return_type) is not VoidType) or len(fn_instance.params) != len(ast.args):
                raise TypeMismatchInExpression(ast)
            else: 
                for in_param, fn_param in zip(ast.args, fn_instance.params):
                    in_type = self.visit(in_param, param)
                    if type(in_type) is NoneType: 
                        raise TypeCannotBeInferred(ast)
                    else:
                        if in_type != fn_param: 
                            raise TypeCannotBeInferred(ast)

                return fn_instance.return_type
        else: # What will return when call a varable is as function
            raise Unname("Cannot call a non-function type id")
        
    # Incase use a variable as a callee (number a; a()) ???
    def visitCallExpr(self, ast, param):
        try:
            fn_instance = self.visit(ast.name, param)
        except Undeclared as e:
            raise Undeclared(kind=Function(), name=e.name)

        if type(fn_instance) is FunctionType:
            if (type(fn_instance.return_type) is VoidType) or len(fn_instance.params) != len(ast.args):
                raise TypeMismatchInExpression(ast)
            else: 
                for in_param, fn_param in zip(ast.args, fn_instance.params):
                    in_type = self.visit(in_param, param)
                    if type(in_type) is NoneType:
                        raise TypeCannotBeInferred(ast)
                    else:
                        if in_type != fn_param: 
                            raise TypeCannotBeInferred(ast)
                        
                return fn_instance.return_type
        else: # What will return when call a varable as function
            raise Unname("Cannot call a non-function type id")

# ---------------------------------------------------------------- Literal Identification

    def visitId(self, ast, param):
        instance = [env[ast.name] for _, env in param if ast.name in env]
        if len(instance) == 0: 
            raise Undeclared(kind=Variable(), name=ast.name)
        else: 
            return instance[0]

    # If no error occurs, return NumType, BoolType, StringType, or ArrayType (in case [[1,2,3], [4,5,6]])
    # Incase a[1,2,3] if a is 3D array -> it will not out of boundary. Otherwise, what error will we raise ?
    def visitArrayCell(self, ast, param):            
        arrType = self.visit(ast.arr, param)
        numTypeIdx = all([
            type(self.visit(index, param)) is NumType 
            for index in ast.idx])

        if (numTypeIdx == True) and (type(arrType) is ArrayType):
            try: 
                eleType = reduce(lambda acc, _: acc.eleType, range(len(ast.idx)), arrType)
                return eleType
            except: 
                raise Unname("Indexing out of boundary")
        else: 
            raise TypeMismatchInExpression(ast)

    def visitNumberLiteral(self, ast, param):
        return NumType()

    def visitBooleanLiteral(self, ast, param):
        return BoolType()

    def visitStringLiteral(self, ast, param):
        return StringType()

    # What will we return if Element in array is not same type ?
    def visitArrayLiteral(self, ast, param):
        elementsType = list(map(lambda x: self.visit(x, param), ast.value))
        isIdenticalType = all([type(x) == type(elementsType[0]) for x in elementsType[1:]])

        if isIdenticalType: 
            return ArrayType(elementsType[0])
        else:
            raise Unname("Element in array is not same type")
    
# ---------------------------------------------------------------- Type Identification

    def visitNumberType(self, ast, param):
        return NumType()

    def visitBoolType(self, ast, param):
        return BoolType()

    def visitStringType(self, ast, param):
        return StringType()
    
    def visitVoidType(self, ast, param):
        return VoidType()

    def visitArrayType(self, ast, param):
        def arrayTypeRecursive(num_lit):
            if len(num_lit) == 0: return self.visit(ast.eleType, param)
            else:
                if type(num_lit[0]) is not float:
                    raise TypeMismatchInStatement(ast)
                return ArrayType(arrayTypeRecursive(num_lit[1:]))
        
        return arrayTypeRecursive(ast.size)