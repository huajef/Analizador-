import ply.lex as lex
import os
import re
from flask import Flask, render_template, request

# initializations
app = Flask(__name__)


# routes

@app.route('/')
def home():

    return render_template('index.html')


@app.route('/validador', methods=['POST'])
def valida():
    error = False
    if request.method == 'POST':
        expresion = request.form['message']
        
        # return 'hello'

        reservadas = ['BEGIN', 'END', 'IF', 'THEN', 'WHILE', 'DO', 'CALL', 'CONST',
                      'VAR', 'PROCEDURE', 'OUT', 'IN', 'ELSE'
                      ]
        tokens = reservadas+['ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
                             'ODD', 'ASSIGN', 'NE', 'LT', 'LTE', 'GT', 'GTE',
                             'LPARENT', 'RPARENT', 'COMMA', 'SEMMICOLOM',
                             'DOT', 'UPDATE'
                             ]

        precedence = (
            ('right','ID','CALL','BEGIN','IF','WHILE'),
            ('right','PROCEDURE'),
            ('right','VAR'),
            ('right', 'ASSIGN'),
            ('right','UPDATE'),
            ('left','NE'),
            ('left','LT','LTE','GT','GTE'),
            ('left','PLUS','MINUS'),
            ('left','TIMES','DIVIDE'),
            ('right','ODD'),
            ('left','LPARENT','RPARENT'),
        )

        t_ignore = '\t '
        t_PLUS = r'\+'
        t_MINUS = r'\-'
        t_TIMES = r'\*'
        t_DIVIDE = r'/'
        t_ODD = r'ODD'
        t_ASSIGN = r'='
        t_NE = r' \r'
        t_LT = r'<'
        t_LTE = r'<='
        t_GT = r'>'
        t_GTE = r'>='
        t_LPARENT = r'\('
        t_RPARENT = r'\)'
        t_COMMA = r','
        # t_SEMMICOLOM = r';'
        t_DOT = r'\.'
        t_UPDATE = r':='

        def t_ID(t):
            r'[a-zA-Z_][a-zA-Z0-9_]*'
            if t.value.upper() in reservadas:
                t.value = t.value.upper()
                # reservadas.get(t.value,'ID')
                t.type = t.value

            return t

        def t_newline(t):
            r'\n+'
            t.lexer.lineno += len(t.value)

        # t_ignore = ' \n'

        def t_COMMENT(t):
            r'\#.*'
            pass

        def t_NUMBER(t):
            r'\d+'
            t.value = int(t.value)
            return t

        def t_error(t):
            # print("caracter ilegal '%s'") % t.value[0]
            t.lexer.skip(1)
            return 'error'   


        def p_program(p):
            '''program : block'''
            print "program"
            #p[0] = program(p[1],"program")

        def p_block(p):
            '''block : constDecl varDecl procDecl statement'''
            print "block"

        def p_constDecl(p):
            '''constDecl : CONST constAssignmentList SEMMICOLOM'''
            #p[0] = constDecl(p[2])
            print "constDecl"

        def p_constDeclEmpty(p):
            '''constDecl : empty'''
            #p[0] = Null()
            print "nulo"

        def p_constAssignmentList1(p):
            '''constAssignmentList : ID ASSIGN NUMBER'''
            print "constAssignmentList 1"

        def p_constAssignmentList2(p):
            '''constAssignmentList : constAssignmentList COMMA ID ASSIGN NUMBER'''
            print "constAssignmentList 2"

        def p_varDecl1(p):
            '''varDecl : VAR identList SEMMICOLOM'''
            print "varDecl 1"

        def p_varDeclEmpty(p):
            '''varDecl : empty'''
            print "nulo"

        def p_identList1(p):
            '''identList : ID'''
            print "identList 1"

        def p_identList2(p):
            '''identList : identList COMMA ID'''
            print "identList 2"

        def p_procDecl1(p):
            '''procDecl : procDecl PROCEDURE ID SEMMICOLOM block SEMMICOLOM'''
            print "procDecl 1"

        def p_procDeclEmpty(p):
            '''procDecl : empty'''
            print "nulo"

        def p_statement1(p):
            '''statement : ID UPDATE expression'''
            print "statement 1"

        def p_statement2(p):
            '''statement : CALL ID'''
            print "statement 2"

        def p_statement3(p):
            '''statement : BEGIN statementList END'''
            print "statement 3"

        def p_statement4(p):
            '''statement : IF condition THEN statement'''
            print "statement 4"

        def p_statement5(p):
            '''statement : WHILE condition DO statement'''
            print "statement 5"

        def p_statementEmpty(p):
            '''statement : empty'''
            print "nulo"

        def p_statementList1(p):
            '''statementList : statement'''
            print "statementList 1"

        def p_statementList2(p):
            '''statementList : statementList SEMMICOLOM statement'''
            print "statementList 2"

        def p_condition1(p):
            '''condition : ODD expression'''
            print "condition 1"

        def p_condition2(p):
            '''condition : expression relation expression'''
            print "condition 2"

        def p_relation1(p):
            '''relation : ASSIGN'''
            print "relation 1"

        def p_relation2(p):
            '''relation : NE'''
            print "relation 2"

        def p_relation3(p):
            '''relation : LT'''
            print "relation 3"

        def p_relation4(p):
            '''relation : GT'''
            print "relation 4"

        def p_relation5(p):
            '''relation : LTE'''
            print "relation 5"

        def p_relation6(p):
            '''relation : GTE'''
            print "relation 6"

        def p_expression1(p):
            '''expression : term'''
            print "expresion 1"

        def p_expression2(p):
            '''expression : addingOperator term'''
            print "expresion 2"

        def p_expression3(p):
            '''expression : expression addingOperator term'''
            print "expresion 3"

        def p_addingOperator1(p):
            '''addingOperator : PLUS'''
            print "addingOperator 1"

        def p_addingOperator2(p):
            '''addingOperator : MINUS'''
            print "addingOperator 1"

        def p_term1(p):
            '''term : factor'''
            print "term 1"

        def p_term2(p):
            '''term : term multiplyingOperator factor'''
            print "term 1"

        def p_multiplyingOperator1(p):
            '''multiplyingOperator : TIMES'''
            print "multiplyingOperator 1"

        def p_multiplyingOperator2(p):
            '''multiplyingOperator : DIVIDE'''
            print "multiplyingOperator 2"

        def p_factor1(p):
            '''factor : ID'''
            print "factor 1"

        def p_factor2(p):
            '''factor : NUMBER'''
            print "factor 1"

        def p_factor3(p):
            '''factor : LPARENT expression RPARENT'''
            print "factor 1"

        def p_empty(p):
            '''empty :'''
            pass

        def p_error(p):
            print "Error de sintaxis ", p
            

        cadena = expresion
        analizador = lex.lex()
        analizador.input(cadena)       

        while True:
            tok = analizador.token()
            if not tok : break
            tok = str(tok)
            print(tok)

            if tok.find('error') > -1 :
                error = True           

            
    message = ''
    if (error):
        message = 'incorrecto.html'
    else:
        message = 'correcto.html'
        
    return render_template(message)

if __name__ == '__main__':
    app.run(debug=True)
