from errors import error
import sly

class Lexer(sly.Lexer):

    keywords = {'if', 'else', 'for', 'do', 'while', 'return', 'break', 'not', 'int', 'char', 'delete', 'void', 'float', 'size', 'bool', 'true', 'false',
    'const'}

    tokens = {
        * { kw.upper() for kw in keywords},
        LE, GE, EQ, NE, LT, GT, OR, AND, NOT, IDENT, INT_LIT, FLOAT_LIT, BOOL_LIT, CHAR_LIT, STRING_LIT, INC, DEC, ADDEQ, SUBEQ, MULEQ, DIVEQ, MULTILINE_COMMENT, MODEQ
    }
    
    literals = {'(', ')', '{', '}', ';', ',', '.', '+', '-', '*', '/', '%', '<', '>', '=', '!', '[', ']', ' '}

    ignore = '\t'

    ignore_multiline_comment = r'\/\*[.]*\*\/'
    ignore_line_comment = r'\/\/.*'

    FLOAT_LIT = r'[-]?[0-9]+[.][0-9]+'

    @_(r'0[bB][01]+', r'[1-9][0-9]*', r'0[xX][0-9a-fA-F]+')
    def INT_LIT(self, t):
        if '0b' in t.value or '0B' in t.value:
            t.value = int(t.value, 2)
        elif '0x' in t.value or '0X' in t.value:
            t.value = int(t.value, 16)
        else:
            t.value = int(t.value, 10);

    @_(r'0[1-7][0-7]*')
    def INT_LIT(self, t):
        t.value = int(t.value, 8)

    NOT = r'not'
    
    CHAR_LIT = r'[\'\"].[\'\"]'

    STRING_LIT = r'[\"\'].*[\"\']'

    IDENT = r'[a-zA-Z]+[a-zA-Z0-9]*'


    
def main():
    import sys
    text = 'hola=-9656.75;mychar="a";mystring="hello world"//Te amo/*You are the best'
    lexer = Lexer()
    for tok in lexer.tokenize(text):
        print(tok)

if __name__ == '__main__':
    main()