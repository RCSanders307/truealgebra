"""
Ipython Evalute three_parse module of Parse
===========================================

Procedure
---------
In truealgebra.core.parse do the following:

    # Search for ``# from IPython import embed``. Uncomment the line
    # Search for ``# embed`` and uncomment. Mind the indention.
    # Search for ``# case =`` and replace with ``case =``

Install ipython, if not installed.
Open a terminal and start a session of ipython

.. code-block:: python

    # if needed set the  path
    import sys
    sys.path.append('<path to truealgebra>')

    from truealgebra.core.testing.ipython_three_parse import *

    # run tester where <n> is an integer indicating the index of the
    # data list in the maker Var instance representing a test.
    out = tester(<n>)

    # The embed()) inside the three_parse method while loop halts
    # execution once at the beginning of the while loop cycle.
    # At each halt in the execution, intergate to see wat has happened::

    # find the name of the case executed in the previous while loop cycle.
    case

    # tokens assigned to farleft, left, mid, and right
    (farleft, left, mid, right)

    # right and left binding powers of tokens: left mid, and right
    (left.lbp, left.rbp,  mid.lbp, mid.rbp, right.lbp, right.rbp)

    # proceed with while loop execution
    exit

    # duplicate pytest testing in test_parse_parse.py:
    ex = maker(<n>)
    assert out.left == ex.outleft
    assert out.left.lbp == ex.outleft.lbp
    assert out.left.rbp == ex.outleft.rbp
    # and so on

Cleanup
-------
In truealgebra.core.parse do the following:

    # Search for ``from IPython import embed``. Comment the line out
    # Search for ``embed()`` and comment the line out.
    # Search for ``case =`` and replace with ``# case =``
"""

from truealgebra.core.rule import (RuleBase, Rules, RulesBU, JustOne,
    JustOneBU, NaturalRule, HalfNaturalRule
)
from truealgebra.core.expression import (
    ExprBase, Symbol, Number, Container,Restricted, Assign, Null, End,
    CommAssoc, true, false, null, any__, end
)
from truealgebra.core.settings import Settings, DIGITS, OPERATORS
from truealgebra.core.parse import Parse
from collections import namedtuple


settings = Settings()
settings.set_default_bp(251, 252)
settings.set_custom_bp('!', 2000, 0)
settings.set_custom_bp('!!!', 3000, 0)
settings.set_custom_bp('/', 1100, 1100)
settings.set_custom_bp('**', 1251, 1250)
settings.set_custom_bp('*', 1000, 999)
settings.set_custom_bp('+', 500, 500)
settings.set_custom_bp("@", 0, 3000)
settings.set_custom_bp("%", 0, 10)
settings.set_custom_bp("!**", 1000, 1000)
settings.set_custom_bp("!*", 999, 999)

settings.set_bodied_functions('D', 481)
settings.set_symbol_operators("and", 75, 75)
settings.set_symbol_operators("E")
settings.set_symbol_operators("jj")
settings.set_infixprefix("-", 999)
settings.set_container_subclass('+', CommAssoc)
settings.set_container_subclass('*', CommAssoc)
settings.set_container_subclass(':=', Assign)
settings.set_container_subclass('Rule', Restricted)

settings.set_sqrtneg1('j')
settings.set_complement('star', '*')
settings.set_complement('!!', '+')


class Vars:
    vars = 'a'
    args = [(1,)]

    def __init__(self, ndx):
        vlist = self.__class__.vars.split(', ')
        arg = self.__class__.args[ndx]
        for i, v in enumerate(vlist):
            exec('self.' + v + ' = arg[' + str(i) + ']')


def unmark(vars, aargs):

    class NewVars(Vars):
        pass

    NewVars.vars = vars
    NewVars.args = aargs

    def maker(i):
        vvar = NewVars(i)
        return vvar

    return maker

Co = Container
CA = CommAssoc
Sy = Symbol
Nu = Number

NR = NaturalRule
HNR = HalfNaturalRule

# Below is the same as the parametrize fixture for test_three_parse
# in truealgebra.core.testing.test_parse_parse.
maker = unmark(
    'left, mid, token_tup, outfarleft, outleft, outmid',
    [
        (   # case 3-1,  0
            Co('@', (), 0, 3000),
            Sy('x'),
            (end,),
            [],
            Co('@', (), 0, 3000),
            Sy('x'),
        ),
        (   # case 3-2, 3-6, 3-7, 1
            Sy('x'),
            Co('-', (), 251, 252),
            (
                Co('-', (), 251, 252),
                Nu(1),
                end,
            ),
            [Co('-', (Sy('x'),), 0, 252)],
            Co('-', (), 0, 999),
            Nu(1),
        ),
        (   # case 3-7, 3-8, 3-5, 3-6  2
            # Covers case 3-5 of farleft[-1].rbp == mid.lbp
            Co('@', (), 0, 3000),
            Co('@', (), 0, 3000),
            (
                Sy('y'),
                Co('!', (), 2000, 0),
                Co('!', (), 2000, 0),
                end,
            ),
            [],
            Co('!', (Co('@', (Co('@', (Sy('y'),)),)),)),
            Co('!', (), 2000, 0),
        ),
        (   # case 3-7, 3-8, 3-5, 3-6, 3
            # Covers case 3-5 of farleft[-1].rbp == mid.lbp
            Co('@', (), 0, 3000),
            Co('@', (), 0, 3000),
            (
                Sy('y'),
                Co('!!!', (), 3000, 0),
                Co('!', (), 2000, 0),
                end,
            ),
            [],
            Co('!!!', (Co('@', (Co('@', (Sy('y'),)),)),)),
            Co('!', (), 2000, 0),
        ),
        (   # case 3-8, 3-8, 3-6, 4
            # covers case 3-6 with farleft empty
            Co('@', (), 0, 3000),
            Sy('x'),
            (
                CA('+', (), 1000, 999),
                Sy('y'),
                end,
            ),
            [],
            CA('+', (Co('@', (Sy('x'),)),), 0, 999),
            Sy('y'),
        ),
        (   # case 3-7, 3-8, 3-6, 5
            # covers 3-6 with farleft(-1].rbp < mid.lbp
            Co('%', (), 0, 10),
            Co('@', (), 0, 3000),
            (
                Sy('y'),
                Co('!', (), 2000, 0),
                Co('!', (), 2000, 0),
                end,
            ),
            [Co('%', (), 0, 10)],
            Co('!', (Co('@', (Sy('y'),)),), 0, 0),
            Co('!', (), 2000, 0),
        ),
        (  # case 3-9, 3-7, 6
            CA('+', (Nu(3),), 0, 500),
            Nu(8),
            (
                CA('*', (), 1000, 999),
                Nu(9),
                end,
            ),
            [CA('+', (Nu(3),), 0, 500),],
            CA('*', (Nu(8),), 0, 999),
            Nu(9),
        ),
        (  # case 3-8, 3-6, 7
            # tests case 3-8 when left.rbp > rigt.lbp, the rbp prevails.
            CA('*', (Nu(3),), 0, 999),
            Nu(8),
            (
                CA('+', (), 500, 500),
                Nu(9),
                end,
            ),
            [],
            CA('+', (CA('*', (Nu(3), Nu(8)), 0, 0),), 0, 500),
            Nu(9),
        ),
        (  # case 3-8, 3-6,  8
            # tests case 3-8 when left.rbp == rigt.lbp, the rbp prevails.
            # the left token binds the mid token
            CA('+', (Nu(3),), 0, 500),
            Nu(8),
            (
                CA('+', (), 500, 500),
                Nu(9),
                end,
            ),
            [],
            CA('+', (CA('+', (Nu(3), Nu(8)), 0, 0),), 0, 500),
            Nu(9),
        ),
    ]
)



def create_create_parse_three(settings=settings):
    """ Fixture Used in testing three_parse method
    """

    FarLeftMid = namedtuple('FarLeftMid', ('farleft', 'left', 'mid'))

    class PyTestParse(Parse):
        def init_tokenizer(self, delim):
            return next(self.gen)

        def three_parse_end(self, farleft, left, mid):
            return FarLeftMid(farleft, left, mid)

        def make_generator(self, token_tup):
            self.gen = iter(token_tup + (end,))

        gen = iter(())

    def create_parse(token_tup):
        parse = PyTestParse(settings)
        parse.make_generator(token_tup)
        return parse

    return create_parse


def tester(n):
    """ A minor bug. Cannot use the same n twice.
    Need to start over to repeat an n (example: use 3 twice)
    """
    ex = maker(n)
    create_parse = create_create_parse_three()
    parse = create_parse(ex.token_tup)
    return parse.three_parse(ex.left, ex.mid, ('end'))

