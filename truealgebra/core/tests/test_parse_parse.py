""" Test Parse parse methods
"""

from truealgebra.core.parse import Parse
from truealgebra.core.expression import (
    Number, Container, Symbol, CommAssoc, null, end
)
from collections import namedtuple
import pytest


# TEST init_parse method - Done
@pytest.fixture
def create_parse_init(settings):
    """ Fixture Used in testing init_parse methods
    """

    class PyTestParse(Parse):
        def init_tokenizer(self, delim):
            return self.init_tokenizer_out

        def two_parse(self, left, delims):
            return left

    def create_parse(init_tokenizer_out):
        parse = PyTestParse(settings)
        parse.init_tokenizer_out = init_tokenizer_out
        return parse

    return create_parse


def test_init_parse_0(create_parse_init):
    parse = create_parse_init(init_tokenizer_out=Container('-', (), 251, 252))

    out = parse.init_parse(('end',))

    assert out == Container('-', (), 0, 999)


def test_init_parse_1(create_parse_init):
    tok_out = Container('f', ())
    parse = create_parse_init(init_tokenizer_out=tok_out)

    out = parse.init_parse(('end',))

    assert out is tok_out


@pytest.mark.parametrize(
    'tok_out, msg',
    [
        (end, "Null content not allowed before delimiter in: ('end',)"),
        (
            Container('***', (), 251, 250),
            "token ***() has unbound left binding power"),
    ]
)
def test_init_parse_error(tok_out, msg, create_parse_init, capsys):
    parse = create_parse_init(init_tokenizer_out=tok_out)

    out = parse.init_parse(('end',))
    output = capsys.readouterr()

    assert out == null
    assert msg in output.out


# TEST two_parse method - Done
@pytest.fixture
def create_parse_two(settings):
    """ Fixture Used in testing two_parse method
    """

    LeftMid = namedtuple('LeftMid', ('left', 'mid'))

    class PyTestParse(Parse):
        def init_tokenizer(self, delim):
            return next(self.gen)

        def two_parse_end(self, left):
            return left

        def three_parse(self, left, mid, delims):
            return LeftMid(left, mid)

        def make_generator(self, token_tup):
            self.gen = iter(token_tup)

        gen = iter(())

    def create_parse(token_tup):
        parse = PyTestParse(settings)
        parse.make_generator(token_tup)
        return parse

    return create_parse


# case 2-1
def test_two_parse_1(create_parse_two):
    token_tup = (end,)
    left = Number(3)
    parse = create_parse_two(token_tup)

    out = parse.two_parse(left, ('end',))

    assert out == left


# case 2-2
def test_two_parse_2(create_parse_two):
    left = Symbol('x')
    token_tup = (
        Container('!', (), 2000, 0),
        Container('!', (), 2000, 0),
        end,
    )
    parse = create_parse_two(token_tup)

    out = parse.two_parse(left, ('end',))

    assert out == (Container('!', (Container('!', (Symbol('x'),)),)))


# case 2-3
def test_two_parse_3(create_parse_two):
    left = Container('@', (), 0, 3000)
    token_tup = (Symbol('y'),)
    parse = create_parse_two(token_tup)

    out = parse.two_parse(left, ('end',))

    assert out.left == left
    assert out.left.lbp == 0
    assert out.left.rbp == 3000
    assert out.mid == Symbol('y')
    assert out.mid.lbp == 0
    assert out.mid.rbp == 0


# case 2-4
def test_two_parse_4(create_parse_two):
    left = Container('D', (Symbol('x'),), 0, 481)
    token_tup = (Container('-', (), 251, 252),)
    parse = create_parse_two(token_tup)

    out = parse.two_parse(left, ('end',))

    assert out.left == left
    assert out.mid == token_tup[0]
    assert out.mid.lbp == 0
    assert out.mid.rbp == 999


@pytest.mark.parametrize(
    'left, token_tup, msg',
    [
        (  # case 2-5
            Container('@', (), 0, 3000),
            (Container('!', (), 2000, 0),),
            'adjacent binding tokens @() and !()'
        ),
        (  # case2-6
            Symbol('x'),
            (Symbol('y'),),
            'adjacent nonbinding tokens x and y'
        ),
    ]
)
def test_two_parse_error(left, token_tup, msg, create_parse_two, capsys):
    parse = create_parse_two(token_tup)

    out = parse.two_parse(left, ('end',))
    output = capsys.readouterr()

    assert out == null
    assert msg in output.out


# TEST two_parse_end method - Done
def test_two_parse_end(settings):
    parse = Parse(settings)

    out = parse.two_parse_end(Symbol('x'))

    assert out == Symbol('x')


def test_two_parse_end_error(settings, capsys):
    parse = Parse(settings)

    out = parse.two_parse_end(Container('@', (), 0, 3000))
    output = capsys.readouterr()

    assert out == null
    assert 'token @() has unbound right binding power' in output.out


# TEST three_parse method -Done
@pytest.fixture
def create_parse_three(settings):
    """ Fixture Used in testing three_parse method
    """

    farleftmid = namedtuple('farleftmid', ('farleft', 'left', 'mid'))

    class PytestParse(Parse):
        def init_tokenizer(self, delim):
            return next(self.gen)

        def three_parse_end(self, farleft, left, mid):
            return farleftmid(farleft, left, mid)

        def make_generator(self, token_tup):
            self.gen = iter(token_tup)

        gen = iter(())

    def create_parse(token_tup):
        parse = PytestParse(settings)
        parse.make_generator(token_tup)
        return parse

    return create_parse


Co = Container
CA = CommAssoc
Sy = Symbol
Nu = Number


# Test three_parse_method
# See truealgebra.core.tests.ipython_three_parse for a
# script to be imported into ipython for debugging
@pytest.mark.parametrize(
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
def test_three_parse(
    left, mid, token_tup, outfarleft, outleft, outmid, create_parse_three
):
    parse = create_parse_three(token_tup)

    out = parse.three_parse(left, mid, ('end'))

    for idx, tok in enumerate(out.farleft):
        ofl = outfarleft[idx]
        assert tok == ofl
        assert tok.lbp == ofl.lbp
        assert tok.rbp == ofl.rbp
    out.left == outleft
    out.left.lbp == outleft.lbp
    out.left.rbp == outleft.rbp
    out.mid == outmid
    out.mid.lbp == outmid.lbp
    out.mid.rbp == outmid.rbp


@pytest.fixture
def create_parse_three_error(settings):
    """ Fixture Used in testing three_parse method with error
    """

    class PytestParse(Parse):
        def init_tokenizer(self, delim):
            return next(self.gen)

        def make_generator(self, token_tup):
            self.gen = iter(token_tup)

        gen = iter(())

    def create_parse(token_tup):
        parse = PytestParse(settings)
        parse.make_generator(token_tup)
        return parse

    return create_parse


@pytest.mark.parametrize(
    'left, mid, token_tup, msg',
    [
        (
            Co('%', (), 0, 10),
            Co('@', (), 0, 3000),
            (Co('!', (), 2000, 0),),
            'adjacent binding tokens @() and !()',
        ),
        (
            Co('@', (), 0, 3000),
            Sy('x'),
            (Sy('y'),),
            'adjacent nonbinding tokens x and y',
        ),
    ]
)
def test_three_parse_error(
    left, mid, token_tup, msg, create_parse_three_error, capsys,
):
    parse = create_parse_three_error(token_tup)

    out = parse.three_parse(left, mid, ('end'))
    output = capsys.readouterr()

    assert out == null
    assert msg in output.out


@pytest.mark.parametrize(
    'farleft, left, mid, correct',
    [
        (  # case3e-2
            [],
            Co('**', (Sy('a'),), 0, 1250),
            Co('!', (Nu(3),), 0, 0),
            Co('**', (Sy('a'),Co('!', (Nu(3),)))),
        ),
        (  # case 3e-2
            [Co('%', (), 0, 10), Co('%', (), 0, 10)],
            Co('**', (Sy('a'),), 0, 1250),
            Co('!', (Nu(3),), 0, 0),
            Co('%', (Co('%', (
                Co('**', (Sy('a'),Co('!', (Nu(3),)))),
            )),))
        ),
        (  # case 3e-3
            [
                Co('%', (), 0, 10),
                Co('@', (), 0, 3000),
                Co('@', (), 0, 3000),
            ],
            Co('!', (Co('@', (Sy('y'),)),), 0, 0),
            Co('!', (), 2000, 0),
            Co('%', (
                Co('!', (
                    Co('@', (Co('@', (
                        Co('!', (Co('@', (Sy('y'),)),))
                    ,)),))
                ,))
            ,))
        ),
    ]
)
def test_three_parse_end(farleft, left, mid, correct, settings):
    parse = Parse(settings)

    out = parse.three_parse_end(farleft, left, mid)

    assert out == correct


def test_three_parse_end_error(settings, capsys):
    parse = Parse(settings)

    out = parse.three_parse_end([], Sy('a'), CA('*', (), 1000, 999))
    output = capsys.readouterr()

    assert out == null
    assert 'token *() has unbound right binding power' in output.out
