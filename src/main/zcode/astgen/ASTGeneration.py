from ZCodeVisitor import ZCodeVisitor
from ZCodeParser import ZCodeParser
from AST import *

class ASTGeneration(ZCodeVisitor):

    def visitProgram(self,ctx:ZCodeParser.ProgramContext):
        decl_list = ctx.decl_list().accept(self)    
        return Program(decl_list)
    
    def visitDecl_list(self, ctx: ZCodeParser.Decl_listContext):
        if ctx.getChildCount() == 1:
            return [ctx.declaration().accept(self)]
        else:
            return [ctx.declaration().accept(self)] + ctx.decl_list().accept(self)
        
    def visitDeclaration(self, ctx: ZCodeParser.DeclarationContext):
        return ctx.variable_stat().accept(self) if ctx.variable_stat() else ctx.function_stat().accept(self)

# ---------------------------------------------------------------- Function Declaration and Definition

    def visitFunction_stat(self, ctx:ZCodeParser.Function_statContext):
        funcComponents = ctx.getChild(0)
        funcID = self.visitID(funcComponents.ID())
        
        # In case we have list/tail => this code should be clearer
        paramArray = funcComponents.param_list().accept(self)

        # If the ctx is function declaration, then it will not have body
        # Otherwise, we can get the body of the function (block statement or return statement)
        if ctx.function_declaration():
            funcBody = None
        elif ctx.function_definition():
            funcBody = funcComponents.block_stat().accept(self) if funcComponents.block_stat() else funcComponents.return_stat().accept(self)
        return FuncDecl(funcID, paramArray, funcBody)
    
    def visitParam_list(self, ctx:ZCodeParser.Param_listContext):
        param_list = []
        current_param = ctx
        while current_param.getChildCount() > 0:
            param_list.append(current_param.parameter().accept(self))
            current_param = current_param.param_list_tail()
        
        return param_list

    def visitParameter(self, ctx: ZCodeParser.ParameterContext):
        if ctx.primitiveDtype():
            dtype, id = ctx.primitiveDtype().accept(self)
        elif ctx.arrayDtype():
            dtype, id = ctx.arrayDtype().accept(self)
        
        modifier = None
        varInit = None
        
        return VarDecl(id, dtype, modifier, varInit)

# ---------------------------------------------------------------- Block Statement

    def visitBlock_stat(self, ctx: ZCodeParser.Block_statContext):
        stmt_list = ctx.statement_list().accept(self)
        return Block(
            stmt=stmt_list
        )
    
    def visitStatement_list(self, ctx: ZCodeParser.Statement_listContext):
        if ctx.getChildCount() == 0:
            return []
        else:
            return [ctx.statement().accept(self)] + ctx.statement_list().accept(self)
        
    def visitStatement(self, ctx: ZCodeParser.StatementContext):
        if ctx.control_stat():
            return ctx.control_stat().accept(self)
        elif ctx.loop_stat():
            return ctx.loop_stat().accept(self)
        elif ctx.variable_stat():
            return ctx.variable_stat().accept(self)
        elif ctx.block_stat():
            return ctx.block_stat().accept(self)
        elif ctx.function_call():
            return ctx.function_call().accept(self)
        elif ctx.assignment():
            return ctx.assignment().accept(self)
        elif ctx.return_stat():
            return ctx.return_stat().accept(self)
        elif ctx.break_stat():
            return ctx.break_stat().accept(self)
        else:
            return ctx.continue_stat().accept(self)
    
# ---------------------------------------------------------------- Function Call Statement

    def visitFunction_call(self, ctx: ZCodeParser.Function_callContext):
        funcExpr = ctx.function_expr()
        id = self.visitID(funcExpr.ID())
        expr_list = funcExpr.expression_list().accept(self)
        return CallStmt(
            name=id,
            args=expr_list
        )

    def visitExpression_list(self, ctx: ZCodeParser.Expression_listContext):
        expr_list = []
        current_expr = ctx
        while current_expr.getChildCount() > 0:
            expr_list.append(current_expr.expression().accept(self))
            current_expr = current_expr.expression_list_tail()

        return expr_list
    
# ---------------------------------------------------------------- Array Expression
    
    def visitArray_expr(self, ctx: ZCodeParser.Array_exprContext):
        expr_list = ctx.expression_nonempty_list().accept(self)
        return ArrayLiteral(expr_list)
    
# ---------------------------------------------------------------- Return Statement

    def visitReturn_stat(self, ctx: ZCodeParser.Return_statContext):
        expr = ctx.expression().accept(self) if ctx.expression() else None # NEED FIX
        return Return(expr)

# ---------------------------------------------------------------- Continue/Break Statement

    def visitContinue_stat(self, ctx: ZCodeParser.Continue_statContext):
        return Continue()
    
    def visitBreak_stat(self, ctx: ZCodeParser.Break_statContext):
        return Break()
    
# ---------------------------------------------------------------- For Statement
    
    def visitLoop_stat(self, ctx: ZCodeParser.Loop_statContext):
        id = self.visitID(ctx.ID())
        cond = ctx.expression(0).accept(self)
        increaseUnit = ctx.expression(1).accept(self)
        body = ctx.statement().accept(self)
        return For(
            name=id,
            condExpr=cond,
            updExpr=increaseUnit,
            body=body
        )
    
# ---------------------------------------------------------------- Control Statement

    def visitControl_stat(self, ctx: ZCodeParser.Control_statContext):
        cond, stmt = ctx.ifst_component().accept(self)
        elif_list = ctx.elif_stmt_list().accept(self)
        else_stmt = ctx.statement().accept(self) if ctx.statement() else None
        return If(
            expr=cond,
            thenStmt=stmt,
            elifStmt=elif_list,
            elseStmt=else_stmt
        )


    def visitIfst_component(self, ctx: ZCodeParser.Ifst_componentContext):
        expr = ctx.expression().accept(self)
        statement = ctx.statement().accept(self)
        return (expr, statement)
    
    def visitElif_stmt_list(self, ctx: ZCodeParser.Elif_stmt_listContext):
        if ctx.getChildCount() == 0:
            return []
        else:
            return [ctx.ifst_component().accept(self)] + ctx.elif_stmt_list().accept(self)

# ---------------------------------------------------------------- Assign Statement
        
    def visitAssignment(self, ctx: ZCodeParser.AssignmentContext):
        rhs = ctx.expression().accept(self)

        if ctx.expression_nonempty_list():
            expr_list = ctx.expression_nonempty_list().accept(self)
            lhs = ArrayCell(
                arr=self.visitID(ctx.ID()),
                idx=expr_list
            )
        else:
            lhs = self.visitID(ctx.ID())

        return Assign(
            lhs=lhs,
            rhs=rhs
        )
    
    def visitExpression_nonempty_list(self, ctx: ZCodeParser.Expression_nonempty_listContext):
        expr_list = []
        current_expr = ctx
        while current_expr.getChildCount() > 0:
            expr_list.append(current_expr.expression().accept(self))
            current_expr = current_expr.expression_nonempty_tail()

        return expr_list

# ---------------------------------------------------------------- Expression Statement
    
    def visitExpression(self, ctx: ZCodeParser.ExpressionContext):
        if ctx.getChildCount() > 1:
            return BinaryOp(
                op=ctx.CONCAT_OP().getText(),
                left = ctx.relational_expr(0).accept(self),
                right = ctx.relational_expr(1).accept(self)
            )
        else:
            return ctx.relational_expr(0).accept(self)
        
    def visitRelation_operation(self, ctx: ZCodeParser.Relation_operationContext):
        if ctx.EQUAL_OP(): return ctx.EQUAL_OP().getText()
        elif ctx.EQUAL_STR_OP(): return ctx.EQUAL_STR_OP().getText()
        elif ctx.INEQUAL_OP(): return ctx.INEQUAL_OP().getText()
        elif ctx.LESS_OP(): return ctx.LESS_OP().getText()
        elif ctx.LARGE_OP(): return ctx.LARGE_OP().getText()
        elif ctx.LESSEQUAL_OP(): return ctx.LESSEQUAL_OP().getText()
        else: return ctx.LARGEEQUAL_OP().getText()
    
    def visitRelational_expr(self, ctx: ZCodeParser.Relational_exprContext):
        if ctx.getChildCount() > 1:
            return BinaryOp(
                op = ctx.relation_operation().accept(self),
                left = ctx.logical_expr(0).accept(self),
                right = ctx.logical_expr(1).accept(self)
            )
        else:
            return ctx.logical_expr(0).accept(self)
        
    def visitLogical_expr(self, ctx: ZCodeParser.Logical_exprContext):
        if ctx.getChildCount() > 1:
            return BinaryOp(
                op = ctx.AND_OP().getText() if ctx.AND_OP() else ctx.OR_OP().getText(),
                left = ctx.logical_expr().accept(self),
                right = ctx.adding_expr().accept(self)
            )
        else:
            return ctx.adding_expr().accept(self)
        
    def visitAdding_expr(self, ctx: ZCodeParser.Adding_exprContext):
        if ctx.getChildCount() > 1:
            return BinaryOp(
                op = ctx.ADD_OP().getText() if ctx.ADD_OP() else ctx.SUB_OP().getText(),
                left = ctx.adding_expr().accept(self),
                right = ctx.multiplying_expr().accept(self)
            )
        else:
            return ctx.multiplying_expr().accept(self)
        
    def visitMultiplying_expr(self, ctx: ZCodeParser.Multiplying_exprContext):
        if ctx.getChildCount() > 1:
            if ctx.MUL_OP(): op = ctx.MUL_OP().getText()
            elif ctx.DIV_OP(): op = ctx.DIV_OP().getText()
            else: op = ctx.MOD_OP().getText()

            return BinaryOp(
                op = op,
                left = ctx.multiplying_expr().accept(self),
                right = ctx.not_logical().accept(self)
            )
        else:
            return ctx.not_logical().accept(self)
    
    def visitNot_logical(self, ctx: ZCodeParser.Not_logicalContext):
        if ctx.getChildCount() > 1:
            return UnaryOp(ctx.NOT_OP().getText(),
                           (ctx.not_logical()).accept(self))
        else:
            return ctx.sign_expr().accept(self)
    
    def visitSign_expr(self, ctx: ZCodeParser.Sign_exprContext):
        if ctx.getChildCount() > 1:
            return UnaryOp(ctx.SUB_OP().getText(),
                           ctx.sign_expr().accept(self))
        else:
            return ctx.index_expr().accept(self)
        
    def visitIndex_expr(self, ctx: ZCodeParser.Index_exprContext):
        if ctx.getChildCount() > 1:
            id = ctx.function_expr().accept(self) if ctx.function_expr() else self.visitID(ctx.ID())

            expr_list = ctx.expression_nonempty_list().accept(self)

            return ArrayCell(
                arr=id,
                idx=expr_list
            )
        else:
            return ctx.parenthesis_expr().accept(self)
    
    def visitParenthesis_expr(self, ctx: ZCodeParser.Parenthesis_exprContext):
        if ctx.getChildCount() > 1:
            return ctx.expression().accept(self)
        else:
            return ctx.term().accept(self)
        
    def visitTerm(self, ctx: ZCodeParser.TermContext):
        if ctx.REAL_LIT():
            return self.visitNumberLiteral(ctx.REAL_LIT())
        elif ctx.STRING_LIT():
            return self.visitStringLiteral(ctx.STRING_LIT())
        elif ctx.BOOL_LIT():
            return self.visitBooleanLiteral(ctx.BOOL_LIT())
        elif ctx.ID():
            return self.visitID(ctx.ID())
        elif ctx.function_expr():
            return ctx.function_expr().accept(self)
        elif ctx.array_expr():
            return ctx.array_expr().accept(self)
        
    def visitFunction_expr(self, ctx: ZCodeParser.Function_exprContext):
        id = self.visitID(ctx.ID())
        expr_list = ctx.expression_list().accept(self)
        return CallExpr(
            name=id,
            args=expr_list
        )
    
# ---------------------------------------------------------------- Variable Declaration

    def visitVariable_stat(self, ctx:ZCodeParser.Variable_statContext):
        if ctx.explicit_declare():
            explicitDecl = ctx.getChild(0)
            return explicitDecl.accept(self)
        else:
            implicitDecl = ctx.getChild(0)
            return implicitDecl.accept(self)

    def visitExplicit_declare(self, ctx:ZCodeParser.Explicit_declareContext):
        '''Exploit the content of the explicit declaration
        return: VarDecl object
        '''
        if ctx.primitive_declare():
            primitiveDecl = ctx.primitive_declare()
            dtype, id = primitiveDecl.primitiveDtype().accept(self)
            modifier = None
            initVal = primitiveDecl.expression().accept(self) if primitiveDecl.expression() else None
            return VarDecl(name=id, varType=dtype, modifier=modifier, varInit=initVal)
        
        elif ctx.array_declare():
            arrayDecl = ctx.array_declare()
            dtype, id = arrayDecl.arrayDtype().accept(self)
            modifier = None
            initVal = arrayDecl.expression().accept(self) if arrayDecl.expression() else None
            return VarDecl(name=id, varType=dtype, modifier=modifier, varInit=initVal)

    def visitPrimitiveDtype(self, ctx: ZCodeParser.PrimitiveDtypeContext):
        dtype = ctx.dtype().accept(self)
        id = self.visitID(ctx.ID())
        return (dtype, id)

    # def visitArrayDtype(self, ctx: ZCodeParser.ArrayDtypeContext):
    #     dtype = ctx.dtype().accept(self)
    #     id = self.visitID(ctx.ID())
    #     return (dtype, id)


    def visitImplicit_declare(self, ctx:ZCodeParser.Implicit_declareContext):
        '''Exploit the content of the implicit declaration
        return: VarDecl object
        '''
        id = self.visitID(ctx.ID())
        dtype = None
        modifier = ctx.VAR_KEYWORD().getText() if ctx.VAR_KEYWORD() else ctx.DYNAMIC_KEYWORD().getText()
        initVal = ctx.expression().accept(self) if ctx.expression() else None

        return VarDecl(id, dtype, modifier, initVal)
    
# ---------------------------------------------------------------- VALUE LITERAL

    def visitID(self, ctx: ZCodeParser.ID):
        return Id(ctx.getText())
    
    def visitBooleanLiteral(self, ctx: ZCodeParser.BOOL_LIT):
        return BooleanLiteral(ctx.getText() == 'true')
    
    def visitStringLiteral(self, ctx: ZCodeParser.STRING_LIT):
        return StringLiteral(ctx.getText())
    
    def visitNumberLiteral(self, ctx: ZCodeParser.REAL_LIT):
        return NumberLiteral(float(ctx.getText()))
    
# ---------------------------------------------------------------- DATA TYPE
    
    def visitArrayDtype(self, ctx: ZCodeParser.ArrayDtypeContext):
        dtype = ctx.dtype().accept(self)
        dim_list = ctx.numlit_list().accept(self)
        id = self.visitID(ctx.ID())
        return ArrayType(dim_list, dtype), id
    
    def visitNumlit_list(self, ctx: ZCodeParser.Numlit_listContext):
        '''Return a list of real number for visitArrayType
        Return [float, float, float]
        '''
        num_list = []
        current_num = ctx
        while current_num.getChildCount() > 0:
            num_list.append(float(current_num.REAL_LIT().getText()))
            current_num = current_num.numlit_tail()

        return num_list


    def visitDtype(self, ctx: ZCodeParser.DtypeContext):
        if ctx.NUM_KEYWORD():
            return NumberType()
        elif ctx.STRING_KEYWORD():
            return StringType()
        elif ctx.BOOL_KEYWORD():
            return BoolType()
        