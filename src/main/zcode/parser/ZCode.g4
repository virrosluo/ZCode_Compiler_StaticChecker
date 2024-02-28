// 2153379
grammar ZCode;

@lexer::header {
from lexererr import *
}

options {
	language=Python3;
}

program: nl_nullable_list decl_list EOF;
decl_list: declaration decl_list | declaration ;

// ----------------------------------------------------------------- LEXER -------------------------------------------------------------------------

NUM_KEYWORD: 'number';
BOOL_KEYWORD: 'bool';
STRING_KEYWORD: 'string';

RETURN_KEYWORD: 'return';

VAR_KEYWORD: 'var';
DYNAMIC_KEYWORD: 'dynamic';
FUNC_KEYWORD: 'func';

FOR_KEYWORD: 'for';
UNTIL_KEYWORD: 'until';
BY_KEYWORD: 'by';

BREAK_KEYWORD: 'break';
CONTINUE_KEYWORD: 'continue';

IF_KEYWORD: 'if';
ELSE_KEYWORD: 'else';
ELIF_KEYWORD: 'elif';

BEGIN_KEYWORD: 'begin';
END_KEYWORD: 'end';

BOOL_LIT: 'true' | 'false';

ASSIGN_OP: '<-';
ADD_OP: '+';
SUB_OP: '-';
MUL_OP: '*';
DIV_OP: '/';
MOD_OP: '%';
NOT_OP: 'not';
AND_OP: 'and';
OR_OP: 'or';
EQUAL_OP: '=';
INEQUAL_OP: '!=';
LESS_OP: '<';
LESSEQUAL_OP: '<=';
LARGE_OP: '>';
LARGEEQUAL_OP: '>=';
CONCAT_OP: '...';
EQUAL_STR_OP: '==';

ID : [a-zA-Z_]+[a-zA-Z0-9_]*;

LEFT_PARENTHESIS : '(';
RIGHT_PARENTHESIS : ')';

LEFT_BRACKET: '[';
RIGHT_BRACKET: ']';

SEPARATOR_KEYWORD: ',';

REAL_LIT: INTPART | INTPART DECPART | INTPART DECPART? EXPPART;
fragment INTPART: [0-9]+;
fragment DECPART: [.][0-9]*;
fragment EXPPART: [eE] [+-]? [0-9]+;

NL1: '\r\r\n' {self.text = "\n"} ;	// Because if "input = \r\n" go to here, it will be: \r \r\n
NL2: '\r' {self.text = "\n"};		// Because if "input = \r" go to here, it will be: \r
NL3: '\r\n' {self.text = "\n"};		// Because if "input = \n" go to here, it will be: \r\n
NL4: '\n' {self.text = "\n"};	// In case of testing on other OSs, input will be \n only

WS : [ \t\b\f]+ -> skip ;
COMMENT_LINE: '##' ~[\r\n]* -> skip;	// Nếu bỏ đi \r thì có thể catch đc col+1 dòng với 1 các testcase lỗi xuống dòng

UNCLOSE_STRING: '"' ( ~["\\'\r\n] | ('\\' [bfrnt\\']) | ('\'' ["]?) )* {raise UncloseString(self.text[1:])};

STRING_LIT: '"' ( ~["\\'\r\n] | ('\\' [bfrnt\\']) | ('\'' ["]?) )* '"' {self.text = self.text[1:-1]};

NEWLINE_STRING: '"' ( ~["\\'\r\n] | '\\' [bfrnt\\'] | ('\'' ["]?) )*? ('\r\n' | '\n' | '\r') {raise UncloseString(self.text[1:].replace('\r', '').replace('\n',''))} ;

ILLEGAL_ESCAPE: '"' ( ~["\\'\r\n] | ('\'' ["]?) | ('\\' [bfrnt\\']))*? ('\\' ~[bfrnt\\']) {raise IllegalEscape(self.text[1:])};

ERROR_TOKEN: . {raise ErrorToken(self.text)};

// ----------------------------------------------------------------- PARSER -------------------------------------------------------------------------

nl_type: NL1 | NL2 | NL3 | NL4;

// nullable list of newlines
nl_nullable_list: nl_type nl_nullable_list |;

// not null list of newlines
nl_list: nl_type nl_list | nl_type;

declaration
		: variable_stat
		| function_stat ;

variable_stat
		: explicit_declare nl_list
		| implicit_declare nl_list;

dtype: NUM_KEYWORD | BOOL_KEYWORD | STRING_KEYWORD;
primitiveDtype: dtype ID ;
arrayDtype: dtype ID LEFT_BRACKET numlit_list RIGHT_BRACKET;

explicit_declare: array_declare		// Hoàn toàn có thể gán là number | array như array_declaration
		| primitive_declare;

primitive_declare: primitiveDtype (ASSIGN_OP expression | );

// LEFT_BRACKET (number list) RIGHT_BRACKET 
// Hoàn toàn có thể gán là number | array
array_declare: arrayDtype (ASSIGN_OP expression | );
numlit_list: REAL_LIT numlit_tail | REAL_LIT;
numlit_tail: SEPARATOR_KEYWORD REAL_LIT numlit_tail | ;

implicit_declare: VAR_KEYWORD ID ASSIGN_OP expression
		| DYNAMIC_KEYWORD ID (ASSIGN_OP expression | );

		// ----------------------------------------------------------------

function_stat: function_definition
		| function_declaration ;

function_definition: FUNC_KEYWORD ID LEFT_PARENTHESIS param_list RIGHT_PARENTHESIS nl_nullable_list (block_stat | return_stat);
function_declaration: FUNC_KEYWORD ID LEFT_PARENTHESIS param_list RIGHT_PARENTHESIS nl_list;

param_list: parameter param_list_tail |;
param_list_tail: SEPARATOR_KEYWORD parameter param_list_tail | ;
parameter 
		: primitiveDtype 
		| arrayDtype ;


		// ----------------------------------------------------------------

// Đảm bảo rằng các statement này đều có dấu xuống dòng ở cuối dòng
statement: control_stat 
		| loop_stat
		| variable_stat
		| block_stat
		| function_call
		| assignment
		| return_stat
		| break_stat
		| continue_stat ;

		// ----------------------------------------------------------------

statement_list: statement statement_list | ;

	// ---------------------------------------------------------------- RETURN BREAK CONTINUE FUNCCALL STATEMENT
return_stat: RETURN_KEYWORD (expression | ) nl_list ;
break_stat: BREAK_KEYWORD nl_list ;
continue_stat: CONTINUE_KEYWORD nl_list ;
block_stat: BEGIN_KEYWORD nl_list statement_list END_KEYWORD nl_list;
function_call: function_expr nl_list;

	// ---------------------------------------------------------------- COMMENT_LINE_STRUCTURE
comment: COMMENT_LINE nl_list;
		
	// ---------------------------------------------------------------- EXPRESSION

// Concat operator
expression
		: relational_expr CONCAT_OP relational_expr
		| relational_expr ;

relation_operation: EQUAL_OP | EQUAL_STR_OP | INEQUAL_OP | LESS_OP | LARGE_OP | LESSEQUAL_OP | LARGEEQUAL_OP;
relational_expr: logical_expr relation_operation logical_expr
		| logical_expr;

logical_expr: logical_expr (AND_OP | OR_OP) adding_expr
		| adding_expr;

adding_expr: adding_expr (ADD_OP | SUB_OP) multiplying_expr
		| multiplying_expr ;
multiplying_expr: multiplying_expr (MUL_OP | DIV_OP | MOD_OP) not_logical
		| not_logical ;

not_logical: NOT_OP not_logical
		| sign_expr ;

sign_expr: SUB_OP sign_expr
		| index_expr;

index_expr: (ID | function_expr) LEFT_BRACKET expression_nonempty_list RIGHT_BRACKET	// Chỉ có thể là ID hoặc function_call ở LEFT_BRACKET
		| parenthesis_expr ;

parenthesis_expr: LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
		| term ;

term
		: REAL_LIT 
		| BOOL_LIT
		| STRING_LIT
		| ID
		| function_expr
		| array_expr ;

// Có tính là 1 expression
// array_expr: Không thể là array rỗng (Theo Khang Phùng)
array_expr : LEFT_BRACKET expression_nonempty_list RIGHT_BRACKET;
function_expr: ID LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS ;

expression_list: expression expression_list_tail | ;
expression_list_tail: SEPARATOR_KEYWORD expression expression_list_tail | ;

expression_nonempty_list: expression expression_nonempty_tail;
expression_nonempty_tail: SEPARATOR_KEYWORD expression expression_nonempty_tail | ;

	// ---------------------------------------------------------------- CONTROL STATEMENT (MAYBE HAVE ERROR)

control_stat: IF_KEYWORD ifst_component elif_stmt_list (ELSE_KEYWORD nl_nullable_list statement | ) ;

elif_stmt_list: ELIF_KEYWORD ifst_component elif_stmt_list | ;
ifst_component: LEFT_PARENTHESIS expression RIGHT_PARENTHESIS nl_nullable_list (statement | );

	// ---------------------------------------------------------------- LOOP STATEMENT

loop_stat: FOR_KEYWORD ID UNTIL_KEYWORD expression BY_KEYWORD expression nl_nullable_list statement ;

	// ----------------------------------------------------------------

// Assignment thì expression phía trước ASSIGN_OP không thể là 1 cái array_expr được mà nó phải là 
assignment: <assoc=right> (ID | ID LEFT_BRACKET expression_nonempty_list RIGHT_BRACKET) ASSIGN_OP expression nl_list;