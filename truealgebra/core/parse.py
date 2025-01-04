from truealgebra.core.err import ta_logger
from truealgebra.core.expressions import Container, Number, Symbol, null, end
from truealgebra.core.settings import settings
from truealgebra.core.constants import (
    OPERATORS, DIGITS, WHITE_SPACE, LETTERS, META_DELIMITERS
)


def parse_logger(msg):
    ta_logger.log('Parse Error\n' + msg)


class Parse:
    """ As a rule, do not call nex_char before calling a tokenizer

    Tokenizer methods
    =================
    The init_tokenizer is the only tokenizer method that gets called by
    a parse method. The init_tokenizer sets self.buf to the empty string,
    then removes white space from self.char. It acts upon the first
    non-white-space in self.char. It will call other tokenizer methods.

    Tokenizer methods, other than the init_tokenizer, only append string
    characters to self.buf. The purpose of a tokenizer methodis to build
    self.buf so that it can be used to create a token.

    Tokenizer methods will call other tokenizer
    methods. But there are no circular chain of calls; for example the
    integer tokenizer method can call the real tokenizer method, but the real
    tokenizer method cannot cause the integer tokenizer method being called
    again.

    Before a tokenizer method is called, the calling method does not
    call self.next_char to replace self.char.

    Tokenizer methods call factory methods when they are done forming the
    self.buf attribute. The token returned by the factory method, will be
    also returned by the preceding chain of tokenizer methods leading to
    the factory method.

    Factory Methods
    ===============
    factory methods use self.buf to create tokens which are TrueAlgebra
    expressions. Factory methods return TrueAlgebra expressions.
    """

    def __init__(self,  postrule=None):
        self.buf = ''
        self.char = None
        self.string = ''
        self.string_iterator = None
        self.postrule = postrule  # UNTESTED CHANGE

    def next_char(self):
        self.char = next(self.string_iterator, 'end')

    def __call__(self, strn):
        self.string = strn
#       if not isinstance(self.string, str):
#           raise ParsingError('parse input must be string')
        self.string_iterator = iter(self.string)
        self.next_char()
        out = self.init_parse()
        if self.postrule is not None:
            out = self.postrule(out)  # UNTESTED CHANGE
        self.buf = ""
        return out

    def init_parse(self, delims=('end',)):
        left = self.init_tokenizer(delims)
        if left is end:  # 0-0
            parse_logger(
                'Null content '
                'not allowed before delimiter in: {}'.format(delims)
            )
            return null
        elif left.lbp and left.name in settings.infixprefix:  # 0-1a
            left.lbp = 0
            left.rbp = settings.infixprefix[left.name]
        elif left.lbp:  # 0-1b
            parse_logger(
                'token {} has unbound left binding power'.format(left)
            )
            return null
        return self.two_parse(left, delims)

    def two_parse(self, left, delims):
        mid = self.init_tokenizer(delims)
        while True:
            if mid is end:  # case 2-1
                return self.two_parse_end(left)

            elif not left.rbp and mid.lbp:  # case 2-2
                mid._bind_left(left)
                left = mid
                mid = self.init_tokenizer(delims)

            elif left.rbp and not mid.lbp:  # case 2-3
                return self.three_parse(left, mid, delims)

            elif (  # case 2-4
                left.rbp and mid.lbp
                and mid.name in settings.infixprefix
            ):
                mid.lbp = 0
                mid.rbp = settings.infixprefix[mid.name]

            elif left.rbp and mid.lbp:  # case 2-5
                parse_logger(
                   'adjacent binding tokens {} and {}'.format(left, mid)
                )
                return null
            elif not left.rbp and not mid.lbp:  # case 2-6
                parse_logger(
                   'adjacent nonbinding tokens {} and {}' .format(left, mid)
                )
                return null

    def two_parse_end(self, left):
        if not left.rbp:  # case 2e-1
            return left
        else:  # case 2e-2
            parse_logger(
                'token {} has unbound right binding power'.format(left)
            )
            return null

    def three_parse(self, left, mid, delims):
        """ Parse a sequence of three or more tokens.

        This method is the heart of the parsing precess.

        farleft list
            Every item in farleft is a token with ``lbp == 0`` and ``rbp > 0``.
            It is case 3-6 that appends the left token to farleft.
            Case 3-6 is the only case that appends tokens to farleft.

            Case 3-6 is executed when ``mid.rbp > 0`` and ``mid.lbp == 0``.
            The left.rbp must be positive. The left token is appended to
            farleft. Therefore all tokens in farleft have a positive rbp.

            The lbp is 0 for all tokens in farleft, because they at one
            time had beeni left tokens.

        left token
            The left token lbp is always 0. the two_parse method assures
            this is true with the inital left token. It is true for all
            other left tokens becuse they are either the first token
            on the left or are adjacent on the left to a token in farleft
            with a positive rbp.

            The rbp of a left token can be zero or positive.

        mid token
            The original mid token came from the two-parse method.
            All other mid tokens had been right tokens.

            The values of mid token lbp and rbp are crucial
            in cases 3.5 to 3.8.

        right token
            The right tken is crated by the init_tokenizer method.
            Cases 3-3 and 3-4 outputs a null expression and an error message
            when there is a parsing error.
        """
        right = self.init_tokenizer(delims)
        farleft = list()
        # case = 'initial'

        while True:
            if right is end:  # case 3-1
                return self.three_parse_end(farleft, left, mid)

            elif (  # case 3-2
                right.name in settings.infixprefix
                and mid.rbp
                and right.lbp
            ):
                right.lbp = 0
                right.rbp = settings.infixprefix[right.name]
                # case = '3-2'

            elif mid.rbp and right.lbp:  # case 3-3
                parse_logger(
                    'adjacent binding tokens {} and {}'.format(mid, right)
                )
                return null

            elif not mid.rbp and not right.lbp:  # case 3-4
                parse_logger(
                    'adjacent nonbinding tokens {} and {}'.format(mid, right)
                )
                return null

            # case 3-5
            elif mid.lbp and farleft and farleft[-1].rbp >= mid.lbp:
                lefty = farleft.pop()
                lefty._bind_right(left)
                left = lefty
                # case = '3-5'

            elif mid.lbp:  # case 3-6
                mid._bind_left(left)
                left = mid
                mid = right
                right = self.init_tokenizer(delims)
                # case = '3-6'

            elif (  # case 3-7
                mid.rbp
                # and not mid.lbp
            ):
                farleft.append(left)
                left = mid
                mid = right
                right = self.init_tokenizer(delims)
                # case = '3-7'

            elif (  # case 3-8
                left.rbp >= right.lbp
                # and not mid.lbp and not mid.rbp
            ):
                left._bind_right(mid)
                mid = right
                right = self.init_tokenizer(delims)
                # case = '3-8'

            elif (  # case 3-9
                left.rbp < right.lbp
                # and not mid.lbp and not mid.rbp
            ):
                right._bind_left(mid)
                mid = right
                right = self.init_tokenizer(delims)
                # case = '3-9'

    def three_parse_end(self, farleft, left, mid):
        if mid.rbp:  # case 3e-1
            parse_logger(
                'token {} has unbound right binding power'.format(mid)
            )
            return null

        elif left.rbp:  # case 3e-2
            left._bind_right(mid)
            while farleft:
                lefty = farleft.pop()
                lefty._bind_right(left)
                left = lefty
            return left

        # case 3e-3
        while farleft and farleft[-1].rbp > mid.lbp:
            lefty = farleft.pop()
            lefty._bind_right(left)
            left = lefty
        mid._bind_left(left)
        left = mid
        while farleft:
            lefty = farleft.pop()
            lefty._bind_right(left)
            left = lefty
        return left

# tokenizer methods
    def init_tokenizer(self, delims):
        self.buf = ""
        while self.char in WHITE_SPACE:
            self.next_char()
        if self.char in delims:
            return end
        elif self.char in DIGITS:
            return self.integer_tokenizer()
        elif self.char in LETTERS:
            return self.symbol_tokenizer()
        elif self.char == '.':
            return self.real_tokenizer()
        elif self.char in OPERATORS:
            return self.oper_tokenizer()
        elif self.char == '(':
            return self.parenthesis_tokenizer()
        else:
            parse_logger('unrecognized character: {}'.format(self.char))
            return null

    def symbol_tokenizer(self):
        while self.char in LETTERS or self.char in DIGITS:
            self.buf += self.char
            self.next_char()
#       if self.buf == settings.sqrtneg1:
#           return self.complex_factory()
#       elif self.buf in settings.symbol_operators:
        if self.buf in settings.symbol_operators:
            return self.symbol_operator_factory()
        elif self.char == '(':
            return self.function_form_tokenizer()
        else:
            return self.symbol_factory()

    def sform_tokenizer(self):
        """ Develope Scientific form tokens for numbers."""
        self.buf += self.char
        self.next_char()
        if self.char in ('+', '-'):
            self.buf += self.char
            self.next_char()
        if self.char not in DIGITS:
            parse_logger(
                'scientific notation requires a digit after the e or E'
            )
            return null
        while self.char in DIGITS:
            self.buf += self.char
            self.next_char()
        if self.char == settings.sqrtneg1:
            self.next_char()
# The following line is an old artifact that should be reoved.
# It ia a bug.
            return self.complex_real_factory()
        else:
            return self.real_factory()

    def function_form_tokenizer(self):
        token = self.function_form_factory()

        self.next_char()   # at this point self.char = '('

        while self.char in WHITE_SPACE:  # remove white space
            self.next_char()
        if self.char == ')':
            self.next_char()
            return token

        while True:
            item = self.init_parse(delims=(')', ',', 'end'))
            if self.char == ')':
                token._append_item(item)
                self.next_char()
                return token
            elif self.char == 'end':
                parse_logger('Missing right parenthesis: )')
                return null
            token._append_item(item)
            self.next_char()

    def real_tokenizer(self):
        """ Develope tokens for real numbers"""
        self.buf += self.char  # self.char will be '.'
        self.next_char()
        while self.char in DIGITS:
            self.buf += self.char
            self.next_char()
        if self.buf == '.':
            parse_logger('real number with "." requires a digit')
            return null
        elif self.char in ('e', 'E'):
            return self.sform_tokenizer()
#       elif self.char == settings.sqrtneg1:
#           self.next_char()
#           return self.complex_real_factory()
        else:
            return self.real_factory()

    def oper_tokenizer(self):
        while self.char in OPERATORS:
            self.buf += self.char
            self.next_char()
        return self.operator_factory()

    def integer_tokenizer(self):
        while self.char in DIGITS:
            self.buf += self.char
            self.next_char()
        if self.char == '.':
            return self.real_tokenizer()
#       elif self.char == settings.sqrtneg1:
#           self.next_char()
#           return self.complex_int_factory()
        elif self.char in ('e', 'E'):
            return self.sform_tokenizer()
        else:
            return self.integer_factory()

    def parenthesis_tokenizer(self):
        """Create token between right and left parenthesis.

        self.buf is empty string and not used
        """
        self.next_char()   # at this point self.char = "("
        out = self.init_parse(delims=(")", "end"))
        if self.char == ")":
            self.next_char()
            return out
        else:  # self.char = 'end'
            parse_logger('Missing right parenthesis: )')
            return null

# factory methods
    def integer_factory(self):
        return Number(int(self.buf))

#   def complex_real_factory(self):
#       return Number(complex(0, float(self.buf)))

#   def complex_int_factory(self):
#       return Number(complex(0, int(self.buf)))

#   def complex_factory(self):
#       """ symbol_tokenizer has sqrtneg1 in self.buf"""
#       return Number(complex(0, 1))

    def real_factory(self):
        return Number(float(self.buf))

    def make_container_instance(self):
        name = settings.complement.get(self.buf, self.buf)
        cls_ = settings.container_subclass.get(name, Container)
        return cls_(name)

    def function_form_factory(self):
        token = self.make_container_instance()
        if self.buf in settings.bodied_functions:
            token.rbp = settings.bodied_functions[self.buf]
        return token

    def symbol_operator_factory(self):
        token = self.make_container_instance()
        token.lbp, token.rbp = settings.symbol_operators[self.buf]
        return token

    def operator_factory(self):
        token = self.make_container_instance()

        token.lbp, token.rbp = settings.custom_bp.get(
            self.buf,
            settings.default_bp
        )
        return token

    def symbol_factory(self):
        return Symbol(self.buf)


# used to parse strings with newline "\n" characters and ";"
def meta_parser(strn):
    """ This function has not been unit tested.
    It most likely will be changed significantly.
    Some of the changes could (or not) be:

        # The name 'Multi', will be used instead of 'meta'. For example,
        the name meta_parser would be multi_parser. multi means many.

        # The output would not be a generator, but a list or an object with
        a list attribute. e.g. MultExpression with a list exprs attribute.

        #The objects will be created in the parser by using '\t' and ';' as
        delimiters in the delims parameters.

        # a MultiExpression instance can not be inside of any other Expression
        instance including another MultExpression instance.
    """
    while strn:
        indx = -1
        for delim in META_DELIMITERS:
            tmp = strn.find(delim)
            if indx == -1:
                indx = tmp
            elif tmp > -1 and tmp < indx:
                indx = tmp
        if indx == -1:
            # the statement below be in a try block
            result = settings.parse(strn)
            strn = ""
        else:
            # the statement below be in a try block
            result = settings.parse(strn[:indx])
            strn = strn[indx+1:]
        yield result


parse = Parse()
