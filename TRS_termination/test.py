from termination import check_termination

def test():
    assert check_termination('tests/test0.txt') == (True, 'g > f')
    assert check_termination('tests/test1.txt') == (False, None)
    assert check_termination('tests/test2.txt') == (False, None)
    assert check_termination('tests/test3.txt') == (True, 'g > f > h')
    assert check_termination('tests/test4.txt') == (True, 'n > a > o')
    assert check_termination('tests/test5.txt') == (True, 'a > s')
    assert check_termination('tests/test6.txt') == (False, None)
    assert check_termination('tests/test7.txt') == (True, 'm > a > s')
    assert check_termination('tests/test8.txt') == (True, 'f > h')
    assert check_termination('tests/test9.txt') == (False, None)
    assert check_termination('tests/test10.txt') == (True, 'f > g')

test()
