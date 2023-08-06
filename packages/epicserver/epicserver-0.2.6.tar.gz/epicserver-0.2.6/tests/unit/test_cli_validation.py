#!/usr/bin/env python3

from epicman.server.utils import single_address, port_or_addr, comma_seperated

from ipaddress import IPv4Address, IPv6Address

from argparse import ArgumentTypeError

import fuzzing
import pytest

### comma_seperated ###
@pytest.mark.parametrize('value,result', 
    [('1',           [1]),
     ('1,1',         [1,1]),
     ('1,1,1,1,1,1', [1,1,1,1,1,1]),
     (' 1',          [1]),
     ('1 ',          [1]),
     (' 1,1',        [1,1]),
     ('1 ,1',        [1,1]),
     ('1, 1',        [1,1]),
     ('1,1 ',        [1,1]),
     ('2,2 ',        [2,2]), # make sure 1 is not special cased
    ])
def test_comma_seperated(value, result):
    conv = comma_seperated(int)
    assert conv(value) == result

@pytest.mark.parametrize('value,error', 
    [('',                ValueError),
     (',',               ValueError),
     ('Not a number',    ValueError),
     ('1.3',             ValueError),
     ('1,Not a number',  ValueError),
     ('Not a number,1',  ValueError),
     ('Not a number ,1', ValueError),  # spaces
    ])
def test_comma_error(value, error):
    conv = comma_seperated(int)
    with pytest.raises(error):
        conv(value)

### single_address ###
@pytest.mark.parametrize('value,result', 
    [('example.com:80',          ('example.com', 80)),
     ('example.com:http',        ('example.com', 80)),
     ('127.0.0.1:80',            (IPv6Address('::FFFF:127.0.0.1'), 80)),
     ('127.0.0.1:http',          (IPv6Address('::FFFF:127.0.0.1'), 80)),
     ('::1:80',                  (IPv6Address('::1'), 80)),
     ('::1:http',                (IPv6Address('::1'), 80)),
     # https://en.wikipedia.org/wiki/IDN_Test_TLDs
     ('إختبار:80',               ('xn--kgbechtv', 80)),
     ('إختبار:http',             ('xn--kgbechtv', 80)),
     ('آزمایشی:80',              ('xn--hgbk6aj7f53bba', 80)),
     ('آزمایشی:http',            ('xn--hgbk6aj7f53bba', 80)),
     ('测试:80',                 ('xn--0zwm56d', 80)),
     ('测试:http',               ('xn--0zwm56d', 80)),
     ('測試:80',                 ('xn--g6w251d', 80)),
     ('測試:http',               ('xn--g6w251d', 80)),
     ('испытание:80',            ('xn--80akhbyknj4f', 80)),
     ('испытание:http',          ('xn--80akhbyknj4f', 80)),
     ('परीक्षा:80',               ('xn--11b5bs3a9aj6g', 80)),
     ('परीक्षा:http',             ('xn--11b5bs3a9aj6g', 80)),
     ('δοκιμή:80',               ('xn--jxalpdlp', 80)),
     ('δοκιμή:http',             ('xn--jxalpdlp', 80)),
     ('테스트:80',               ('xn--9t4b11yi5a', 80)),
     ('테스트:http',             ('xn--9t4b11yi5a', 80)),
     ('טעסט:80',                 ('xn--deba0ad', 80)),
     ('טעסט:http',               ('xn--deba0ad', 80)),
     ('テスト:80',               ('xn--zckzah', 80)),
     ('テスト:http',             ('xn--zckzah', 80)),
     ('பரிட்சை:80',               ('xn--hlcj6aya9esc7a', 80)),
     ('பரிட்சை:http',             ('xn--hlcj6aya9esc7a', 80)),
     # confirm that an idn being rencoded produces the same output
     ('xn--hlcj6aya9esc7a:80',   ('xn--hlcj6aya9esc7a', 80)),
     ('xn--hlcj6aya9esc7a:http', ('xn--hlcj6aya9esc7a', 80)),
    ])
def test_single_address(value, result):
    assert single_address(value) == result

@pytest.mark.parametrize('value', 
    ['',
     'missing_port',
     'has spaces',
     '  has_spaces',
     'has_spaces  ',
     'invalid_port:-1',
     'invalid_port:0',
     'invalid_port:70000',
     'invalid_port:34b',
     'invalid_port:b34',
     'invalid_port:not-a-valid-service',
     '11111.11111.1111.111:8755', # bad ip
     'bad domain name:8755',
     '\x02non_printable_chars.com:8755',
    ])
def test_single_address_error(value):
    with pytest.raises(ArgumentTypeError):
        single_address(value)

# Negative (fail) cases are tested via single_address
# see implementaiton (its the catch all)
@pytest.mark.parametrize('value,result', 
    [(':80',          ('', 80)),
     (':http',        ('', 80)),
     ('80',           ('', 80)),
#### ('http',        ('', 80)), # this is invalid as we cant tell if domain name or port name
    ])
def test_port_or_addr(value, result):
    assert port_or_addr(value) == result


@pytest.mark.parametrize('func,err,seed',
    [(port_or_addr,         ArgumentTypeError, ':80'),
     (port_or_addr,         ArgumentTypeError, '80'),
     (port_or_addr,         ArgumentTypeError, 'http'),
     (port_or_addr,         ArgumentTypeError, ':http'),
     (single_address,       ArgumentTypeError, '127.0.0.1:80'),
     (single_address,       ArgumentTypeError, '127.0.0.1:http'),
     (single_address,       ArgumentTypeError, '::1:80'),
     (single_address,       ArgumentTypeError, '::1:http'),
     (single_address,       ArgumentTypeError, '[::1]:80'),
     (single_address,       ArgumentTypeError, '[::1]:http'),
     (single_address,       ArgumentTypeError, 'missing_port'),
     (single_address,       ArgumentTypeError, 'has spaces'),
     (single_address,       ArgumentTypeError, '  has_spaces'),
     (single_address,       ArgumentTypeError, 'has_spaces  '),
     (single_address,       ArgumentTypeError, 'invalid_port:-1'),
     (single_address,       ArgumentTypeError, 'invalid_port:0'),
     (single_address,       ArgumentTypeError, 'invalid_port:70000'),
     (single_address,       ArgumentTypeError, 'invalid_port:34b'),
     (single_address,       ArgumentTypeError, 'invalid_port:b34'),
     (single_address,       ArgumentTypeError, 'invalid_port:not-a-valid-service'),
     (single_address,       ArgumentTypeError, '11111.11111.1111.111:8755'),
     (single_address,       ArgumentTypeError, 'bad domain name:8755'),
     (single_address,       ArgumentTypeError, '\x02non_printable_chars.com:8755'),
     (comma_seperated(int), ValueError,        '0,0'),
    ])
def test_fuzz_func(func,err,seed):
    ROUNDS = 25
    VARIATION = 2
    for value in fuzzing.fuzz_string(seed, ROUNDS, VARIATION):
        try:
            func(value)
        except err:
            pass  # this is OK

