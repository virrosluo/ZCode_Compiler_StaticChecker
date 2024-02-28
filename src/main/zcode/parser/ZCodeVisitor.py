# Generated from main/zcode/parser/ZCode.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ZCodeParser import ZCodeParser
else:
    from ZCodeParser import ZCodeParser

# This class defines a complete generic visitor for a parse tree produced by ZCodeParser.

class ZCodeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ZCodeParser#program.
    def visitProgram(self, ctx:ZCodeParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#decl_list.
    def visitDecl_list(self, ctx:ZCodeParser.Decl_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#nl_type.
    def visitNl_type(self, ctx:ZCodeParser.Nl_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#nl_nullable_list.
    def visitNl_nullable_list(self, ctx:ZCodeParser.Nl_nullable_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#nl_list.
    def visitNl_list(self, ctx:ZCodeParser.Nl_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#declaration.
    def visitDeclaration(self, ctx:ZCodeParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#variable_stat.
    def visitVariable_stat(self, ctx:ZCodeParser.Variable_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#dtype.
    def visitDtype(self, ctx:ZCodeParser.DtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#primitiveDtype.
    def visitPrimitiveDtype(self, ctx:ZCodeParser.PrimitiveDtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#arrayDtype.
    def visitArrayDtype(self, ctx:ZCodeParser.ArrayDtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#explicit_declare.
    def visitExplicit_declare(self, ctx:ZCodeParser.Explicit_declareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#primitive_declare.
    def visitPrimitive_declare(self, ctx:ZCodeParser.Primitive_declareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#array_declare.
    def visitArray_declare(self, ctx:ZCodeParser.Array_declareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#numlit_list.
    def visitNumlit_list(self, ctx:ZCodeParser.Numlit_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#numlit_tail.
    def visitNumlit_tail(self, ctx:ZCodeParser.Numlit_tailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#implicit_declare.
    def visitImplicit_declare(self, ctx:ZCodeParser.Implicit_declareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#function_stat.
    def visitFunction_stat(self, ctx:ZCodeParser.Function_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#function_definition.
    def visitFunction_definition(self, ctx:ZCodeParser.Function_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#function_declaration.
    def visitFunction_declaration(self, ctx:ZCodeParser.Function_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#param_list.
    def visitParam_list(self, ctx:ZCodeParser.Param_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#param_list_tail.
    def visitParam_list_tail(self, ctx:ZCodeParser.Param_list_tailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#parameter.
    def visitParameter(self, ctx:ZCodeParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#statement.
    def visitStatement(self, ctx:ZCodeParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#statement_list.
    def visitStatement_list(self, ctx:ZCodeParser.Statement_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#return_stat.
    def visitReturn_stat(self, ctx:ZCodeParser.Return_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#break_stat.
    def visitBreak_stat(self, ctx:ZCodeParser.Break_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#continue_stat.
    def visitContinue_stat(self, ctx:ZCodeParser.Continue_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#block_stat.
    def visitBlock_stat(self, ctx:ZCodeParser.Block_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#function_call.
    def visitFunction_call(self, ctx:ZCodeParser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#comment.
    def visitComment(self, ctx:ZCodeParser.CommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#expression.
    def visitExpression(self, ctx:ZCodeParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#relation_operation.
    def visitRelation_operation(self, ctx:ZCodeParser.Relation_operationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#relational_expr.
    def visitRelational_expr(self, ctx:ZCodeParser.Relational_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#logical_expr.
    def visitLogical_expr(self, ctx:ZCodeParser.Logical_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#adding_expr.
    def visitAdding_expr(self, ctx:ZCodeParser.Adding_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#multiplying_expr.
    def visitMultiplying_expr(self, ctx:ZCodeParser.Multiplying_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#not_logical.
    def visitNot_logical(self, ctx:ZCodeParser.Not_logicalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#sign_expr.
    def visitSign_expr(self, ctx:ZCodeParser.Sign_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#index_expr.
    def visitIndex_expr(self, ctx:ZCodeParser.Index_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#parenthesis_expr.
    def visitParenthesis_expr(self, ctx:ZCodeParser.Parenthesis_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#term.
    def visitTerm(self, ctx:ZCodeParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#array_expr.
    def visitArray_expr(self, ctx:ZCodeParser.Array_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#function_expr.
    def visitFunction_expr(self, ctx:ZCodeParser.Function_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#expression_list.
    def visitExpression_list(self, ctx:ZCodeParser.Expression_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#expression_list_tail.
    def visitExpression_list_tail(self, ctx:ZCodeParser.Expression_list_tailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#expression_nonempty_list.
    def visitExpression_nonempty_list(self, ctx:ZCodeParser.Expression_nonempty_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#expression_nonempty_tail.
    def visitExpression_nonempty_tail(self, ctx:ZCodeParser.Expression_nonempty_tailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#control_stat.
    def visitControl_stat(self, ctx:ZCodeParser.Control_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#elif_stmt_list.
    def visitElif_stmt_list(self, ctx:ZCodeParser.Elif_stmt_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#ifst_component.
    def visitIfst_component(self, ctx:ZCodeParser.Ifst_componentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#loop_stat.
    def visitLoop_stat(self, ctx:ZCodeParser.Loop_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZCodeParser#assignment.
    def visitAssignment(self, ctx:ZCodeParser.AssignmentContext):
        return self.visitChildren(ctx)



del ZCodeParser