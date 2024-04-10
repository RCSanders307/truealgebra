from truealgebra.core.parse import Parse


def test_next_char(conftest_settings):
    parse = Parse()
    parse.string = 'abc'
    parse.string_iterator = iter(parse.string)

    parse.next_char()
    a = parse.char
    parse.next_char()
    b = parse.char
    parse.next_char()
    c = parse.char
    parse.next_char()
    end = parse.char

    assert a == 'a'
    assert b == 'b'
    assert c == 'c'
    assert end == 'end'
