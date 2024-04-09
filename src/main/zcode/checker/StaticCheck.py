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
    FUNC_DECLR = 0
    FUNC_DEFIN = 1
    
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
        return f"FunctionType: {self.name} - {self.params} - {self.return_type} - {self.declare_type}"

class ArrayType(Type):
    def __init__(self, eleType:Type, eleLength:float):
        super(ArrayType, self).__init__()
        self.eleType = eleType
        self.eleLength = eleLength

    def __eq__(self, other):
        if super(ArrayType, self).__eq__(other):
            return self.eleType == other.eleType and \
                (self.eleLength == other.eleLength if self.eleLength is not None and other.eleLength is not None else True)
        else:
            return False
    
    def __str__(self):
        return f"ArrayType: {self.eleLength} --> {str(self.eleType)}"

class Utils():
    def InferType(name:str, inferType:type, genEnv: list[(int, dict)]):
        for _, env in genEnv:
            if name in env:
                if type(env[name]) is not FunctionType:
                    env[name] = inferType
                else:
                    env[name].return_type = inferType
                return inferType
        else:
            raise Exception(f"Variable {name} not found in general environment")

FOR_ENV = 1
FUNC_ENV = 2
NONE_ENV = 3

class StaticChecker(BaseVisitor, Utils):
    def visitProgram(self, ast, param):
        param = [(NONE_ENV, {})]

        for i in ast.decl:
            self.visit(i, param)

        _, var_dict = param[0]
        
        # Ưu tiên No Definition for a Function. PROVE
        fnDeclaration = list(filter(lambda x: type(x) is FunctionType and x.declare_type == FunctionType.FUNC_DECLR, var_dict.values()))
        if len(fnDeclaration) > 0: raise NoDefinition(fnDeclaration[0].name)

        if not ('main' in var_dict): 
            raise NoEntryPoint()
        else:
            mainInfo = var_dict['main'] 
            if not(mainInfo == FunctionType("main", [], VoidType(), FunctionType.FUNC_DEFIN)):
                raise NoEntryPoint()

    def visitVarDecl(self, ast, param):
        _, cur_env = param[0]
        try:
            id_instance = self.visit(ast.name, [param[0]])
        except Undeclared as e:
            id_instance = None
        
        id_name = ast.name.name
        if id_instance is not None:
            raise Redeclared(Variable(), ast.name)
        else:
            cur_env[id_name] = NoneType()
            valueType = self.visit(ast.varInit, param) if ast.varInit else NoneType()
            
            if ast.varType:
                varType = self.visit(ast.varType, param)
                
                if type(valueType) is NoneType and ast.varInit: # Infer type for NoneType of right hand side variable of the declaration 
                    valueType = Utils.InferType(ast.varInit.name if type(ast.varInit) is Id else ast.varInit.name.name,
                                                varType, param)
                
                if type(valueType) is not NoneType and \
                    ((varType != valueType) or (varType != cur_env[id_name] and type(cur_env[id_name]) is not NoneType)):
                    raise TypeMismatchInStatement(ast)
                else:
                    cur_env[id_name] = varType
            else:
                # Do not need to check the valueType is not Array because we permit in this. PROVE
                # Incase 'var' type này thì assignment trước đã luôn đảm bảo là var sẽ có expression => valueType != NONETYPE
                cur_env[id_name] = valueType

        return VoidType()

    def visitFuncDecl(self, ast, param):
        _, cur_env = param[0]       
        try:
            fn_instance = self.visit(ast.name, [param[0]])
        except Undeclared as e:
            fn_instance = None
            
        new_env = (FUNC_ENV, {})
        try:
            for i in ast.param: self.visit(i, [new_env])
        except Redeclared as e:
            raise Redeclared(kind=Parameter(), name=ast.name)
        
        if fn_instance is None:
            # Because we haven't declare this function name => Create it and append into cur_env            
            fn_instance = FunctionType(id=ast.name.name, 
                                       params=[new_env[1][p.name.name] for p in ast.param], 
                                       return_type=NoneType(), 
                                       declare_type=FunctionType.FUNC_DECLR)
            cur_env[ast.name.name] = fn_instance
        else:
            if type(fn_instance) is not FunctionType:
                raise Redeclared(kind=Function(), name=ast.name)
            else:
                if fn_instance.declare_type == FunctionType.FUNC_DEFIN or ast.body is None:
                    # Incase the function had body but now define again
                    # Or case: the function declared twices
                    raise Redeclared(kind=Function(), name=ast.name)

        # fn_instance.declare_type == FUNC_DECLR and ast.body != None
        if ast.body is not None:
            body_type = self.visit(ast.body, [new_env] + param)
            fn_type = fn_instance.return_type
            
            if type(fn_type) is NoneType:
                fn_instance.return_type = body_type
            elif fn_type != body_type:
                raise TypeMismatchInStatement(ast)
            fn_instance.declare_type = FunctionType.FUNC_DEFIN
                        
        return VoidType()

# ---------------------------------------------------------------- BIN / UNI OPERATION

    def visitBinaryOp(self, ast, param):
        def on_check(inferType:Type):
            typeOperand_1 = self.visit(ast.left, param)
            if type(typeOperand_1) is NoneType:
                typeOperand_1 = Utils.InferType(ast.left.name if type(ast.left) is Id else ast.left.name.name,
                                                inferType(), param)
                
            typeOperand_2 = self.visit(ast.right, param)
            if type(typeOperand_2) is NoneType:
                typeOperand_2 = Utils.InferType(ast.right.name if type(ast.right) is Id else ast.right.name.name,
                                                inferType(), param)
            
            if (type(typeOperand_1) is inferType) and (type(typeOperand_2) is inferType):
                return typeOperand_1
            else:
                raise TypeMismatchInExpression(ast)

        if ast.op in ['+', '-', '*', '/', '%']:
            return on_check(NumType)

        elif ast.op in ['and', 'or']:
            return on_check(BoolType)

        elif ast.op in ['...']:
            return on_check(StringType)

        elif ast.op in ['=', '!=', '<', '>', '<=', '>=']:
            on_check(NumType)
            return BoolType()

        elif ast.op in ['==']:
            return on_check(StringType)

    def visitUnaryOp(self, ast, param):
        def on_check(correctType):
            typeOperand = self.visit(ast.operand, param)
            
            if type(typeOperand) is correctType:
                return typeOperand
            elif type(typeOperand) is NoneType:
                return Utils.InferType(ast.operand.name if type(ast.operand) is Id else ast.operand.name.name,
                                       correctType())
            else:
                raise TypeMismatchInExpression(ast)

        if ast.op == 'not':
            on_check(BoolType)
        
        elif ast.op == '-':
            on_check(NumType)

# ------------------------------------------------------------ Statements

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

        ifExprType = type(self.visit(ast.expr, param)) is BoolType
        stmt_type = [self.visit(ast.thenStmt, [(cur_env_name, {})] + param)]
        
        elif_stmt_type, elifExprType = [], []
        for expr, stmt in ast.elifStmt:
            elifExprType.append(type(self.visit(expr, param)) is BoolType)
            elif_stmt_type.append(self.visit(stmt, [(cur_env_name, {})] + param))

        if not (ifExprType and all(elifExprType)):
            raise TypeMismatchInStatement(ast)

        else_stmt_type = [self.visit(ast.elseStmt, [(cur_env_name, {})] + param)] if ast.elseStmt else []
        
        # Incase of all ifelse also have return => Get the first return type 
        return_type_list = stmt_type + elif_stmt_type + else_stmt_type
        return return_type_list[0]

    def visitFor(self, ast, param):
        new_env = (FOR_ENV, {})

        idType = self.visit(ast.name, param)
        if type(idType) is NoneType:
            idType = Utils.InferType(ast.name.name, 
                                     NumType(), param)

        condType = self.visit(ast.condExpr, param)
        if type(condType) is NoneType:
            condType = Utils.InferType(ast.condExpr.name if type(ast.condExpr) is Id else ast.condExpr.name.name,
                                       BoolType(), param)
            
        updType = self.visit(ast.updExpr, param)
        if type(updType) is NoneType:
            updType = Utils.InferType(ast.updExpr.name if type(ast.updExpr) is Id else ast.updExpr.name.name,
                                      NumType(), param)

        if (type(condType) is not BoolType) or (type(idType) is not NumType) or (type(updType) is not NumType): 
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
            exprType = self.visit(ast.expr, param)
            if type(exprType) is NoneType: 
                raise TypeCannotBeInferred(ast)
            else:
                return exprType
        else: 
            return VoidType()

    def visitAssign(self, ast, param):
        right_type = self.visit(ast.rhs, param)
        left_type = self.visit(ast.lhs, param)

        if (type(left_type) is NoneType) and (type(right_type) is NoneType): 
            raise TypeCannotBeInferred(ast)
        elif type(left_type) is NoneType: # => Inferred to the left type
            Utils.InferType(ast.lhs.name if type(ast.lhs) is Id else ast.lhs.name.name,
                            right_type, param)
        elif type(right_type) is NoneType: # => Inferred to the right type
            Utils.InferType(ast.rhs.name if type(ast.rhs) is Id else ast.rhs.name.name,
                            left_type, param)
        else:
            if left_type != right_type: raise TypeMismatchInStatement(ast)
        
        return VoidType()


    def visitCallStmt(self, ast, param):
        try: 
            fn_instance = self.visit(ast.name, param)
        except Undeclared as e: 
            raise Undeclared(kind=Function(), name=e.name)
        
        if type(fn_instance) is FunctionType:
            if type(fn_instance.return_type) is NoneType:
                Utils.InferType(fn_instance.name, VoidType(), param)
                
            if (type(fn_instance.return_type) is not VoidType) or len(fn_instance.params) != len(ast.args):
                raise TypeMismatchInExpression(ast)
            else: 
                for in_param, fn_param in zip(ast.args, fn_instance.params):
                    in_type = self.visit(in_param, param)
                    if type(in_type) is NoneType:
                        in_type = Utils.InferType(in_param.name if type(in_param) is Id else in_param.name.name,
                                                  fn_param, param)
                    if in_type != fn_param: 
                        raise TypeCannotBeInferred(ast)

                return fn_instance.return_type
        else: 
            raise Undeclared(kind=Function(), name=ast.name)
        
        
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
                        in_type = Utils.InferType(in_param.name if type(in_param) is Id else in_param.name.name,
                                                  fn_param, param)
                    if in_type != fn_param:
                        raise TypeCannotBeInferred(ast)
                        
                return fn_instance.return_type
        else:
            raise Undeclared(kind=Function(), name=ast.name)

# ---------------------------------------------------------------- Literal Identification

    def visitId(self, ast, param):
        instance = [env[ast.name] for _, env in param if ast.name in env]
        if len(instance) == 0: 
            raise Undeclared(kind=Identifier(), name=ast.name)
        else: 
            return instance[0]

    def visitArrayCell(self, ast, param):                   
        numTypeIdx = True
        for index in ast.idx:
            idxType = self.visit(index, param)
            if type(idxType) is NoneType:
                idxType = Utils.InferType(index.name if type(index) is Id else index.name.name,
                                          NumType(), param)
            numTypeIdx = (type(idxType) is NumType) and numTypeIdx 
            
        arrType = self.visit(ast.arr, param)
        if type(arrType) is NoneType:
            raise TypeCannotBeInferred(ast)

        if (numTypeIdx == True) and (type(arrType) is ArrayType):
            try: 
                eleType = reduce(lambda acc, _: acc.eleType, range(len(ast.idx)), arrType)
                if type(eleType) is ArrayType: 
                    raise Exception()
                else:
                    return eleType
            except: 
                raise TypeMismatchInExpression(ast)
        else: 
            raise TypeMismatchInExpression(ast)

    def visitNumberLiteral(self, ast, param):
        return NumType()

    def visitBooleanLiteral(self, ast, param):
        return BoolType()

    def visitStringLiteral(self, ast, param):
        return StringType()

    def visitArrayLiteral(self, ast, param):
        
        elementsType = []
        for x in ast.value:
            eleType = self.visit(x, param)
            if type(eleType) is NoneType: raise TypeCannotBeInferred(ast)
            else: elementsType.append(eleType)
            
        isIdenticalType = all([x == elementsType[0] for x in elementsType[1:]])

        if isIdenticalType: 
            return ArrayType(elementsType[0], float(len(elementsType)))
        else:
            raise TypeMismatchInExpression(ast)
    
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
            if len(num_lit) == 0: 
                return self.visit(ast.eleType, param)
            else:
                if type(num_lit[0]) is not float:
                    raise TypeMismatchInStatement(ast)
                return ArrayType(arrayTypeRecursive(num_lit[1:]), num_lit[0])
        
        return arrayTypeRecursive(ast.size)