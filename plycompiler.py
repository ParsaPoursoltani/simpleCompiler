import ply.lex as lex
import ply.yacc as yacc

# List of token names
tokens = (
    'INT', 'STR', 'PRINT',
    'NUMBER', 'IDENTIFIER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS'
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='

# Define a rule for identifiers
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z_0-9]*'


# Define a rule for number literals
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule for string literals
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove the quotes
    return t


# Define a rule for newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Define keywords
keywords = {
    'int': 'INT',
    'str': 'STR',
    'print': 'PRINT'
}


# Define a rule for identifying keywords
def t_KEYWORD(t):
    r'\b(?:int|str|print)\b'
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t


# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Parsing rules

# Dictionary to store variables
variables = {}


def p_statement_list(p):
    '''statement_list : statement
                      | statement statement_list'''


def p_statement_decl(p):
    '''statement : INT IDENTIFIER EQUALS expression
                 | STR IDENTIFIER EQUALS STRING'''
    if p[1] == 'int':
        variables[p[2]] = p[4]
    elif p[1] == 'str':
        variables[p[2]] = p[4]


def p_statement_assign(p):
    '''statement : IDENTIFIER EQUALS expression'''
    if p[1] in variables:
        variables[p[1]] = p[3]
    else:
        print(f"Undefined variable '{p[1]}'")


def p_statement_print(p):
    '''statement : PRINT expression'''
    print(p[2])


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_group(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]


def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]


def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    if p[1] in variables:
        p[0] = variables[p[1]]
    else:
        print(f"Undefined variable '{p[1]}'")
        p[0] = 0


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")


# Build the parser
parser = yacc.yacc()

# Example usage
if __name__ == '__main__':
    with open(input("Enter the filename: "), 'r') as file:
        data = file.read()

    # Parse the data
    parser.parse(data)
