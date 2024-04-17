from StaticCheck import *
                    

class StaticInference():
    checkerModule = StaticChecker()
    
    def visitCallStmt(self, ast, param, inferType:FunctionType):
        pass        

    def visitBlock(self, ast, param, inferType):
        pass

    def visitIf(self, ast, param, inferType):
        pass

    def visitFor(self, ast, param, inferType):
        pass

    def visitContinue(self, ast, param, inferType):
        pass

    def visitBreak(self, ast, param, inferType):
        pass

    def visitReturn(self, ast, param, inferType):
        pass

    def visitAssign(self, ast, param, inferType):
        pass
    
    def visitCallExpr(self, ast, param, inferType):
        for _, env in param:
            idSymbol = list(filter(lambda x: x.name == ast.name and type(x.idType) is FunctionType, env))
            if len(idSymbol) > 0:
                idSymbol = idSymbol[0]
                if type(idSymbol.idType.return_type) is NoneType:
                    idSymbol.idType = inferType
                elif type(idSymbol.idType) is not type(inferType):
                    raise TypeMismatchInExpression(ast)
                return inferType

    def visitArrayLiteral(self, ast, param, inferType:ArrayType):
        for i in ast.value:
            currentInfer = inferType.eleType
            try:
                self.visit(i, param, currentInfer)
            except TypeMismatchInExpression as e:
                raise TypeMismatchInExpression(ast)
        return inferType
        
    def visitId(self, ast, param, inferType):
        for _, env in param:
            idSymbol = list(filter(lambda x: x.name == ast.name and type(x.idType) is not FunctionType, env))
            if len(idSymbol) > 0:
                idSymbol = idSymbol[0]
                if type(idSymbol.idType) is NoneType:
                    idSymbol.idType = inferType
                elif type(idSymbol.idType) is not type(inferType):
                    raise TypeMismatchInExpression(ast)
                return inferType
    
# DO NOT USE:
    def visitArrayCell(self, ast, param, inferType):
        pass
    
    def visitBinaryOp(self, ast, param, inferType):
        pass

    def visitUnaryOp(self, ast, param, inferType):
        pass
    
    def visitProgram(self, ast, param, inferType):
        pass

    def visitVarDecl(self, ast, param, inferType):
        pass

    def visitFuncDecl(self, ast, param, inferType):
        pass

    def visitNumberType(self, ast, param, inferType):
        pass

    def visitBoolType(self, ast, param, inferType):
        pass

    def visitStringType(self, ast, param, inferType):
        pass

    def visitArrayType(self, ast, param, inferType):
        pass
    
    def visitNumberLiteral(self, ast, param, inferType):
        pass

    def visitBooleanLiteral(self, ast, param, inferType):
        pass

    def visitStringLiteral(self, ast, param, inferType):
        pass
    
    def visit(self, ast, param, inferType:Type) -> Type:
        return ast.accept(self, param, inferType)