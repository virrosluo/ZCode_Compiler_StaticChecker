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
    
    def __init__(self, id:str, params:list, return_type:Type, declare_type:int):
        super(FunctionType, self).__init__()
        self.name = id
        self.params = params
        self.return_type = return_type
        self.declare_type = declare_type
        
    def __eq__(self, other):
        if super(FunctionType, self).__eq__(other):
            return all([
                self.return_type == other.return_type,
                len(self.params) == len(other.params),
                all([i == j for i,j in zip(self.params, other.params)])
            ])
        
    def __str__(self):
        return f"FunctionType: {self.name} - {[str(i) for i in self.params]} - {str(self.return_type)} - {self.declare_type}"

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

class Symbol():
    def __init__(self, name:str, idType: Type):
        self.name = name
        self.idType = idType
    def assignType(self, newType: Type):
        if type(self.idType) is FunctionType:
            self.idType.return_type = newType
        else:
            self.idType = newType

class StaticChecker(BaseVisitor, Utils):
    pass

class Utils():
    def InferType(id, inferType:Type, genEnv: list, checker:StaticChecker) -> Type:
        if type(id) is ArrayLiteral:
            if type(inferType) is not ArrayType:
                raise Exception()
            Utils.InferArray(id, inferType, genEnv, checker)
            return inferType
        else:
            if type(id) is Id:
                name = id.name
                isVariable = True
            else:
                name = id.name.name
                isVariable = False

            for _, env in genEnv:
                filtered_id = list(filter(lambda x: all([x.name == name, 
                                                        (isVariable and type(x.idType) is not FunctionType) or (not(isVariable) and type(x.idType) is FunctionType)]), 
                                        env))
                if len(filtered_id) > 0:
                    filtered_id[0].assignType(inferType)
                    return inferType
        
    def InferArray(expr:Expr, inferType:Type, genEnv, checker:StaticChecker) -> Type:
        if type(expr) is not ArrayLiteral:
            if type(checker.getExprType(expr, genEnv, Identifier)) is NoneType: 
                Utils.InferType(expr, inferType, genEnv, checker)
        else:
            if len(expr.value) != inferType.eleLength:
                raise Exception()
            for val in expr.value: 
                Utils.InferArray(val, inferType.eleType, genEnv, checker)

FOR_ENV = 1
FUNC_ENV = 2
NONE_ENV = 3

class StaticChecker(BaseVisitor, Utils):
    def __init__(self, ast):
        self.ast = ast
        
    def check(self):
        return self.visit(self.ast, [])
    
    def getExprType(self, expr:Expr, curEnv, errorKind) -> Type:
        returnType = self.visit(expr, curEnv)
        if type(expr) is Id:
            returnType = returnType[0]
            if returnType is None:
                raise Undeclared(kind=errorKind(), name=expr.name)
        return returnType
    
    def visitProgram(self, ast, param):        
        param = [( NONE_ENV, [Symbol(name="readNumber", idType=FunctionType(id="readNum", params=[], return_type=NumType(), declare_type=FunctionType.FUNC_DEFIN)),
                              Symbol(name="writeNumber", idType=FunctionType(id="writeNum", params=[NumType()], return_type=VoidType(), declare_type=FunctionType.FUNC_DEFIN)),
                              Symbol(name="readBool", idType=FunctionType(id="readBool", params=[], return_type=BoolType(), declare_type=FunctionType.FUNC_DEFIN)),
                              Symbol(name="writeBool", idType=FunctionType(id="writeBool", params=[BoolType()], return_type=VoidType(), declare_type=FunctionType.FUNC_DEFIN)),
                              Symbol(name="readString", idType=FunctionType(id="readString", params=[], return_type=StringType(), declare_type=FunctionType.FUNC_DEFIN)),
                              Symbol(name="writeString", idType=FunctionType(id="writeString", params=[StringType()], return_type=VoidType(), declare_type=FunctionType.FUNC_DEFIN))] )]

        for i in ast.decl:
            self.visit(i, param)

        _, var_dict = param[0]
        
        # Ưu tiên No Definition for a Function. PROVE
        fnDeclaration = list(filter(lambda x: type(x.idType) is FunctionType and x.idType.declare_type == FunctionType.FUNC_DECLR, var_dict))
        if len(fnDeclaration) > 0: raise NoDefinition(fnDeclaration[0].name)

        for var in var_dict:
            if var.name == 'main':
                if (var.idType == FunctionType("main", [], VoidType(), FunctionType.FUNC_DEFIN)):
                    break
        else:
            raise NoEntryPoint()

    def visitVarDecl(self, ast, param) -> list:
        _, cur_env = param[0]
        id_instance, _ = self.visit(ast.name, [param[0]])

        if id_instance is not None:
            raise Redeclared(Variable(), ast.name)
        else:
            varSymbol = Symbol(ast.name.name, NoneType())
            cur_env.append(varSymbol)
            
            if ast.varType:
                if ast.varInit:
                    try:
                        valueType = self.getExprType(ast.varInit, param, Identifier)
                    except TypeCannotBeInferred as _:
                        raise TypeCannotBeInferred(ast)
                else: 
                    valueType = NoneType()
                varType = self.visit(ast.varType, param)
                
                if type(valueType) is NoneType and ast.varInit: # Infer type for NoneType of right hand side variable of the declaration 
                    try: valueType = Utils.InferType(ast.varInit, varType, param, self)
                    except: raise TypeMismatchInStatement(ast)
                
                if type(valueType) is not NoneType and \
                    ((varType != valueType) or (varType != varSymbol.idType and type(varSymbol.idType) is not NoneType)):
                    raise TypeMismatchInStatement(ast)
                else:
                    varSymbol.assignType(varType)
            else:
                # Do not need to check the valueType is not Array because we permit in this. PROVE
                if ast.varInit:
                    # Incase we have variableInit. If the RHS is NoneType but LHS also NoneType => Raise TypeCannotBeInferred
                    try:
                        valueType = self.getExprType(ast.varInit, param, Identifier)
                    except TypeCannotBeInferred as _:
                        raise TypeCannotBeInferred(ast)
                    if type(valueType) is NoneType: raise TypeCannotBeInferred(ast)
                else:
                    # Incase we dont have variableInit. The LHS Type can assign to NoneType
                    valueType = NoneType()
                
                varSymbol.assignType(valueType)

        return [None]

    def visitFuncDecl(self, ast, param):
        _, cur_env = param[0]       
        _, fn_instance = self.visit(ast.name, [param[0]])
            
        new_env = (FUNC_ENV, list())
        try:
            for i in ast.param: self.visit(i, [new_env])
        except Redeclared as e:
            raise Redeclared(kind=Parameter(), name=ast.name)

        if fn_instance is None:
            # Because we haven't declare this function name => Create it and append into cur_env
            fn_instance = FunctionType(id=ast.name.name, 
                                       params=[var.idType for var in new_env[1]], 
                                       return_type=NoneType(),
                                       declare_type=FunctionType.FUNC_DECLR)
            cur_env.append(Symbol(ast.name.name, fn_instance))
        else:
            if len(new_env[1]) == len(fn_instance.params):
                sameParams = all([fn_params == new_params.idType for fn_params, new_params in zip(fn_instance.params, new_env[1])])
            else:
                sameParams = False
                
            if fn_instance.declare_type == FunctionType.FUNC_DECLR and ast.body is None or not(sameParams) or fn_instance.declare_type == FunctionType.FUNC_DEFIN:
                # Incase the function had body but now define again
                # Or case: the function declared twices
                # Or the same name with the different num params or different param type => Considers as a new function
                raise Redeclared(kind=Function(), name=ast.name.name)

        # fn_instance.declare_type == FUNC_DECLR and ast.body != None
        if ast.body is not None:
            body_type = list(filter(lambda x: x is not None, self.visit(ast.body, [new_env] + param))) # body_type: List[Tuple(statement return, returnType) or None]
            fn_type = fn_instance.return_type

            if len(body_type) == 0:
                body_type = [(None, VoidType())]

            # Assign type for Function Return
            if type(fn_type) is NoneType:
                fn_instance.return_type = body_type[0][1]
            else:
                for returnStmt, returnType in body_type:
                    if fn_type != returnType:
                        raise TypeMismatchInStatement(returnStmt)
            fn_instance.declare_type = FunctionType.FUNC_DEFIN
        return None

# ---------------------------------------------------------------- BIN / UNI OPERATION

    def visitBinaryOp(self, ast, param):
        def on_check(correctType:Type):
            typeOperand_1 = self.getExprType(ast.left, param, Identifier)
            if type(typeOperand_1) is NoneType:
                try: typeOperand_1 = Utils.InferType(ast.left, correctType(), param, self)
                except: raise TypeMismatchInExpression(ast)
                
            typeOperand_2 = self.getExprType(ast.right, param, Identifier)
            if type(typeOperand_2) is NoneType:
                try: typeOperand_2 = Utils.InferType(ast.right, correctType(), param, self)
                except: raise TypeMismatchInExpression(ast)

            if (type(typeOperand_1) is correctType) and (type(typeOperand_2) is correctType):
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
            on_check(StringType)
            return BoolType()

    def visitUnaryOp(self, ast, param):
        def on_check(correctType):
            typeOperand = self.getExprType(ast.operand, param, Identifier)
            
            if type(typeOperand) is correctType:
                return typeOperand
            elif type(typeOperand) is NoneType:
                try: return Utils.InferType(ast.operand, correctType(), param, self)
                except: raise TypeMismatchInExpression(ast)
            else:
                raise TypeMismatchInExpression(ast)

        if ast.op == 'not':
            return on_check(BoolType)
        
        elif ast.op == '-':
            return on_check(NumType)

# ------------------------------------------------------------ Statements

    # Incase: {'if else':'NUMTYPE', 'if else': 'BOOLTYPE'} . How can we check and sure about this ???
    # Incase: {'return NUMTYPE', 'return BOOLTYPE'} . How can we check and sure about this ???
    def visitBlock(self, ast, param) -> list:
        cur_env_name, _ = param[0]
        new_env = (cur_env_name, list())

        return_type = reduce(lambda acc, ele: acc + self.visit(ele, [new_env] + param), ast.stmt, [])
        return_type = list(filter(lambda x: x is not None, return_type))
        
        # Getting the return type for the block statement (Incase block statement have multiple return statements) => Get the first return statement
        return return_type if len(return_type) > 0 else [None]

    def visitIf(self, ast, param) -> list:
        cur_env_name, _ = param[0]

        ifExprType = type(self.getExprType(ast.expr, param, Identifier)) is BoolType
        stmt_type = self.visit(ast.thenStmt, [(cur_env_name, [])] + param)
        
        elif_stmt_type, elifExprType = [], []
        for expr, stmt in ast.elifStmt:
            elifExprType.append(type(self.getExprType(expr, param, Identifier)) is BoolType)
            elif_stmt_type += self.visit(stmt, [(cur_env_name, [])] + param)

        if not (ifExprType and all(elifExprType)):
            raise TypeMismatchInStatement(ast)

        else_stmt_type = self.visit(ast.elseStmt, [(cur_env_name, [])] + param) if ast.elseStmt else []
        
        # Incase of all ifelse also have return => Get the first return type 
        return_type_list = [i for i in stmt_type + elif_stmt_type + else_stmt_type if i is not None]
        return return_type_list if len(return_type_list) > 0 else [None]

    def visitFor(self, ast, param) -> list:
        new_env = (FOR_ENV, list())

        idType = self.getExprType(ast.name, param, Identifier)
        if type(idType) is NoneType:
            try: idType = Utils.InferType(ast.name, NumType(), param, self)
            except: raise TypeMismatchInStatement(ast)

        condType = self.getExprType(ast.condExpr, param, Identifier)
        if type(condType) is NoneType:
            try: condType = Utils.InferType(ast.condExpr, BoolType(), param, self)
            except: raise TypeMismatchInStatement(ast)
            
        updType = self.getExprType(ast.updExpr, param, Identifier)
        if type(updType) is NoneType:
            try: updType = Utils.InferType(ast.updExpr, NumType(), param, self)
            except: raise TypeMismatchInStatement(ast)

        if (type(condType) is not BoolType) or (type(idType) is not NumType) or (type(updType) is not NumType): 
            raise TypeMismatchInStatement(ast)
        
        return self.visit(ast.body, [new_env] + param)

    def visitContinue(self, ast, param) -> list:
        cur_env_type, _ = param[0]
        if cur_env_type != FOR_ENV: 
            raise MustInLoop(ast)
        else: 
            return [None]

    def visitBreak(self, ast, param) -> list:
        cur_env_type, _ = param[0]
        if cur_env_type != FOR_ENV: 
            raise MustInLoop(ast)
        else:
            return [None]

    # Return Tuple(currentStmt and returnType)
    def visitReturn(self, ast, param) -> list:
        if ast.expr: 
            exprType = self.getExprType(ast.expr, param, Identifier)

            if exprType is None: 
                raise Undeclared(kind=Identifier(), name=ast.expr.name)
            
            if type(exprType) is NoneType:
                raise TypeCannotBeInferred(ast)
            else:
                return [(ast, exprType)]
        else: 
            return [(ast, VoidType())]

    def visitAssign(self, ast, param) -> list:
        try:
            right_type = self.getExprType(ast.rhs, param, Identifier)
            left_type = self.getExprType(ast.lhs, param, Identifier)
        except TypeCannotBeInferred as _:
            raise TypeCannotBeInferred(ast)

        if (type(left_type) is NoneType) and (type(right_type) is NoneType): 
            raise TypeCannotBeInferred(ast)
        elif type(left_type) is NoneType: # => Inferred to the left type
            try: Utils.InferType(ast.lhs, right_type, param, self)
            except: raise TypeMismatchInStatement(ast)
        elif type(right_type) is NoneType: # => Inferred to the right type
            try: Utils.InferType(ast.rhs, left_type, param, self)
            except: raise TypeMismatchInStatement(ast)
        else:
            if left_type != right_type: raise TypeMismatchInStatement(ast)
        return [None]


    def visitCallStmt(self, ast, param) -> list:
        _, fn_instance = self.visit(ast.name, param)
        if fn_instance is None:
            raise Undeclared(kind=Function(), name=ast.name.name)
        
        if type(fn_instance.return_type) is NoneType:
            try: Utils.InferType(ast, VoidType(), param, self)
            except: raise TypeMismatchInStatement(ast)
            
        if (type(fn_instance.return_type) is not VoidType) or len(fn_instance.params) != len(ast.args):
            raise TypeMismatchInStatement(ast)
        else: 
            for in_param, fn_param in zip(ast.args, fn_instance.params):
                in_type = self.getExprType(in_param, param, Identifier)
                if type(in_type) is NoneType:
                    in_type = Utils.InferType(in_param, fn_param, param, self)
                if in_type != fn_param: 
                    raise TypeMismatchInExpression(ast)

            return [None]
                
    def visitCallExpr(self, ast, param):
        _, fn_instance = self.visit(ast.name, param)
        if fn_instance is None:
            raise Undeclared(kind=Function(), name=ast.name.name)

        if (type(fn_instance.return_type) is VoidType) or len(fn_instance.params) != len(ast.args):
            raise TypeMismatchInExpression(ast)
        else: 
            for in_param, fn_param in zip(ast.args, fn_instance.params):
                in_type = self.getExprType(in_param, param, Identifier)
                if type(in_type) is NoneType:
                    try: in_type = Utils.InferType(in_param, fn_param, param, self)
                    except: raise TypeMismatchInExpression(ast)
                if in_type != fn_param:
                    raise TypeMismatchInExpression(ast)
                    
            return fn_instance.return_type

# ---------------------------------------------------------------- Literal Identification

    def visitId(self, ast, param):
        varInstance, funcInstance = None, None
        for _, env in param:
            for var in env:
                if var.name == ast.name and type(var.idType) is not FunctionType and varInstance is None:
                    varInstance = var.idType
                elif var.name == ast.name and type(var.idType) is FunctionType and funcInstance is None:
                    funcInstance = var.idType
            if varInstance is not None and funcInstance is not None:
                break
        
        return varInstance, funcInstance

    def visitArrayCell(self, ast, param):                   
        numTypeIdx = True
        for index in ast.idx:
            idxType = self.getExprType(index, param, Identifier)
            if type(idxType) is NoneType:
                try: idxType = Utils.InferType(index, NumType(), param, self)
                except: raise TypeMismatchInExpression(ast)
            numTypeIdx = (type(idxType) is NumType) and numTypeIdx 
            
        arrType = self.getExprType(ast.arr, param, Identifier)
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
            eleType = self.getExprType(x, param, Identifier)
            elementsType.append(eleType)
            
        validTypeList = [i for i in elementsType if type(i) is not NoneType]
        isIdenticalType = all([x == validTypeList[0] for x in validTypeList[1:]])
        
        if not isIdenticalType:
            raise TypeMismatchInExpression(ast)
        else:
            if len(validTypeList) > 0:
                for expr, exprType in zip(ast.value, elementsType):
                    if type(exprType) is NoneType: 
                        try: Utils.InferType(expr, validTypeList[0], param, self)
                        except: raise TypeMismatchInExpression(ast)
                return ArrayType(validTypeList[0], float(len(elementsType)))
            else:
                return NoneType()
    
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