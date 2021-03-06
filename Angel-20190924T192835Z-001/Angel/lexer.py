from errors import error
import sly

class Lexer(sly.Lexer):

    keywords = {'if', 'else', 'for', 'do', 'while', 'return', 'break', 'not', 'int', 'char', 'delete', 'void',
    'float', 'size', 'bool', 'true', 'false', 'const', 'new', 'sub', 'add', 'mde', 'te', 'de', 'pe', 'me'}

    tokens = {
        * { kw.upper() for kw in keywords},LE, GE, EQ, NE, LT, GT, OR, AND, NOT,
        INT_LIT, FLOAT_LIT, IDENT, BOOL_LIT, CHAR_LIT, STRING_LIT, INC, DEC,
        ADDEQ, SUBEQ, MULEQ, DIVEQ, MODEQ}

    literals = {'(', ')', '{', '}', ';', ',', '.', '+', '-', '*', '/', '%', '<', '>', '=', '!', '[', ']'}

    ignore = '\t\n\ \;\(\)\{\}\='

    LE = r'<='

    GE = r'>='

    EQ = r'=='

    LT = r'<'

    GT = r'>'

    OR = r'\|\|'

    AND = r'\&\&'

    INC = r'\+\+'

    DEC = r'\-\-'

    ADDEQ = r'\+\='

    SUBEQ = r'\-\='

    MULEQ = r'\*\='

    DIVEQ = r'\/\='

    MODEQ = r'\%\='

    INT = r'int'

    IF = r'if'

    ELSE = r'else'

    FOR = r'for'

    DO = r'do'

    WHILE = r'while'

    RETURN = r'return'

    BREAK = r'break'

    CHAR = r'char'

    DELETE = r'delete'

    VOID = r'void'

    FLOAT = r'float'

    SIZE = r'size'

    BOOL = r'bool'

    TRUE = r'true'

    FALSE = r'false'

    CONST = r'const'

    ignore_multiline_comment = r'\/\*.*\*\/'
    ignore_line_comment = r'\/\/.*\n'

    @_(r'\/\*.*')
    def multilineCommentNotClosedError(self, t):
        error(self.lineno, 'Comentario no cerrado')
        self.index += 1


    @_(r'[-]?[0-9]+[.][0-9]*')
    def FLOAT_LIT(self, t):
        t.value = float(t.value)


    @_(r'0[bB][01]+', r'[1-9][0-9]*', r'0[xX][0-9a-fA-F]+')
    def INT_LIT(self, t):
        if '0b' in t.value or '0B' in t.value:
            t.value = int(t.value, 2)
        elif '0x' in t.value or '0X' in t.value:
            t.value = int(t.value, 16)
        else:
            t.value = int(t.value, 10);


    NOT = r'not'

    CHAR_LIT = r'[\'\"].[\'\"]'

    STRING_LIT = r'[\"\'].*[\"\']'

    IDENT = r'[a-zA-Z]+[a-zA-Z0-9]*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
        return t
    @_(r'\r')
    def scapeCodError(self,t):
        error(self.lineno, 'En la línea Cadena de código de escape invalido')
        self.endex +=1

    def error(self, t):
        error(self.lineno, 'En la línea se encuentra un caracter ilegal %r' % t.value[0])
        self.index += 1


def main():
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write('Uso: python3 lexer.py filename\n')
        raise SystemExit(1)
    f = open(sys.argv[1], "r")
    text = f.read()
    lexer = Lexer()
    for tok in lexer.tokenize(text):
        print(tok)

if __name__ == '__main__':
    main()
