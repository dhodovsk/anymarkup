# -*- coding: utf-8 -*-
import io
import os

import pytest
import six

from anymarkup import *

from test import *

class TestParse(object):
    fixtures = os.path.join(os.path.dirname(__file__), 'fixtures')

    def assert_unicode(self, struct):
        if isinstance(struct, dict):
            for k, v in struct.items():
                self.assert_unicode(k)
                self.assert_unicode(v)
        elif isinstance(struct, list):
            for i in struct:
                self.assert_unicode(i)
        elif isinstance(struct, (six.string_types, type(None), type(True))):
            pass
        else:
            raise AssertionError('Unexpected type {0} in parsed structure'.format(type(struct)))

    @pytest.mark.parametrize('str, expected', [
        ('', {}),
        ('{}', {}),
        ('[]', []),
        (example_ini, example_ini_as_struct),
        (example_json, example_as_struct),
        (example_xml, example_as_struct),
        (example_yaml, example_as_struct),
    ])
    def test_parse_basic(self, str, expected):
        parsed = parse(str)
        assert parsed == expected
        self.assert_unicode(parsed)

    @pytest.mark.parametrize('str, expected', [
        ('# comment', {}),
        ('# comment\n', {}),
        ('# comment\n' + example_ini, example_ini_as_struct),
        ('# comment\n' + example_json, example_as_struct),
        ('# comment\n' + example_yaml, example_as_struct),
    ])
    def test_parse_recognizes_comments_in_ini_json_yaml(self, str, expected):
        parsed = parse(str)
        assert parsed == expected
        self.assert_unicode(parsed)

    def test_parse_works_with_bytes_yielding_file(self):
        f = open(os.path.join(self.fixtures, 'empty.ini'), 'rb')
        parsed = parse(f)
        assert parsed == {}

    def test_parse_works_with_unicode_yielding_file(self):
        # on Python 2, this can only be simulated with io.open
        f = io.open(os.path.join(self.fixtures, 'empty.ini'), encoding='utf-8')
        parsed = parse(f)
        assert parsed == {}

    def test_parse_fails_on_wrong_format(self):
        with pytest.raises(AnyMarkupError):
            parse('foo: bar', format='xml')

    @pytest.mark.parametrize('file, expected', [
        # TODO: some parsers allow empty files, others don't - this should be made consistent
        ('empty.ini', {}),
        ('empty.json', AnyMarkupError),
        ('empty.xml', AnyMarkupError),
        ('empty.yaml', {}),
        ('example.ini', example_ini_as_struct),
        ('example.json', example_as_struct),
        ('example.xml', example_as_struct),
        ('example.yaml', example_as_struct),
    ])
    def test_parse_file_basic(self, file, expected):
        f = os.path.join(self.fixtures, file)
        if expected == AnyMarkupError:
            with pytest.raises(AnyMarkupError):
                parse_file(f)
        else:
            parsed = parse_file(f)
            assert parsed == expected
            self.assert_unicode(parsed)

    def test_parse_file_noextension(self):
        parsed = parse_file(os.path.join(self.fixtures, 'without_extension'))
        assert parsed == example_ini_as_struct
        self.assert_unicode(parsed)

    def test_parse_file_fails_on_bad_extension(self):
        with pytest.raises(AnyMarkupError):
            parse_file(os.path.join(self.fixtures, 'bad_extension.xml'))
