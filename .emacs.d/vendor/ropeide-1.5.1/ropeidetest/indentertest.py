import unittest

from rope.base import codeanalyze
from ropeide.indenter import (PythonCodeIndenter, NormalIndenter,
                              _StatementRangeFinder)
from ropeidetest.mockeditortest import MockEditorFactory


class PythonCodeIndenterTest(unittest.TestCase):

    __factory = MockEditorFactory()

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.editor = self.__factory.create()
        self.indenter = PythonCodeIndenter(self.editor)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_python_indenter(self):
        self.editor.set_text('print "hello"\n')
        self.indenter.correct_indentation(0)
        self.assertEquals('print "hello"\n', self.editor.get_text())

    def test_indenting_lines_with_indented_previous_line(self):
        self.editor.set_text('def f():\n    g()\nh()\n')
        self.indenter.correct_indentation(3)
        self.assertEquals('def f():\n    g()\n    h()\n', self.editor.get_text())

    def test_indenting_lines_with_indented_previous_line(self):
        self.editor.set_text('def f():\n    g()\nh()\n')
        self.indenter.correct_indentation(3)
        self.assertEquals('def f():\n    g()\n    h()\n', self.editor.get_text())

    def test_indenting_lines_when_prev_line_ends_with_a_colon(self):
        self.editor.set_text('def f():\ng()')
        self.indenter.correct_indentation(2)
        self.assertEquals('def f():\n    g()', self.editor.get_text())

    def test_empty_prev_line(self):
        self.editor.set_text('    \nprint "hello"\n')
        self.indenter.correct_indentation(2)
        self.assertEquals('    \nprint "hello"\n', self.editor.get_text())

    def test_indenting_lines_with_indented_previous_line_with_empty_line(self):
        self.editor.set_text('def f():\n    g()\n\nh()\n')
        self.indenter.correct_indentation(4)
        self.assertEquals('def f():\n    g()\n\n    h()\n', self.editor.get_text())

    def test_indenting_lines_when_prev_line_ends_with_a_colon_with_empty_line(self):
        self.editor.set_text('def f():\n\ng()')
        self.indenter.correct_indentation(3)
        self.assertEquals('def f():\n\n    g()', self.editor.get_text())

    def test_indenting_lines_at_start(self):
        self.editor.set_text('    g()\n')
        self.indenter.correct_indentation(1)
        self.assertEquals('g()\n', self.editor.get_text())

    def test_indenting_lines_with_start_previous_line(self):
        self.editor.set_text('\n    g()\n')
        self.indenter.correct_indentation(2)
        self.assertEquals('\ng()\n', self.editor.get_text())

    def test_deindenting_after_pass(self):
        self.editor.set_text('def f():\n    pass\n    f()')
        self.indenter.correct_indentation(3)
        self.assertEquals('def f():\n    pass\nf()', self.editor.get_text())

    def test_explicit_line_continuation(self):
        self.editor.set_text('c = a + \\\nb')
        self.indenter.correct_indentation(2)
        self.assertEquals('c = a + \\\n    b', self.editor.get_text())

    def test_returning_after_backslashes(self):
        self.editor.set_text('c = \\\n    b\\\n+ a')
        self.indenter.correct_indentation(3)
        self.assertEquals('c = \\\n    b\\\n    + a', self.editor.get_text())

    def test_returning_after_backslashes2(self):
        self.editor.set_text('c = \\\n    b\na')
        self.indenter.correct_indentation(3)
        self.assertEquals('c = \\\n    b\na', self.editor.get_text())

    def test_backslash_should_indent_relative_to_the_first_word(self):
        self.editor.set_text('print a, \\\nb')
        self.indenter.correct_indentation(2)
        self.assertEquals('print a, \\\n      b', self.editor.get_text())

    def test_backslash_indenting_on_indented_blocks(self):
        self.editor.set_text('def f():\n    c = a + \\\nb')
        self.indenter.correct_indentation(3)
        self.assertEquals('def f():\n    c = a + \\\n        b', self.editor.get_text())

    def test_backslash_indenting_on_indented_blocks2(self):
        self.editor.set_text('def f():\n    print a, \\\nb')
        self.indenter.correct_indentation(3)
        self.assertEquals('def f():\n    print a, \\\n          b', self.editor.get_text())

    def test_deindenting_when_encountering_else(self):
        self.editor.set_text('if True:\n    print "hello"\n    else:')
        self.indenter.correct_indentation(3)
        self.assertEquals('if True:\n    print "hello"\nelse:', self.editor.get_text())

    def test_deindenting_when_encountering_elif(self):
        self.editor.set_text('if True:\n    print "hello"\n    elif False:')
        self.indenter.correct_indentation(3)
        self.assertEquals('if True:\n    print "hello"\nelif False:', self.editor.get_text())

    def test_deindenting_when_encountering_except(self):
        self.editor.set_text('try:\n    print "hello"\n    except Exception:')
        self.indenter.correct_indentation(3)
        self.assertEquals('try:\n    print "hello"\nexcept Exception:', self.editor.get_text())

    def test_deindenting_when_encountering_finally(self):
        self.editor.set_text('try:\n    print "hello"\n    finally:')
        self.indenter.correct_indentation(3)
        self.assertEquals('try:\n    print "hello"\nfinally:', self.editor.get_text())

    def test_deindenting_after_return(self):
        self.editor.set_text('def f():\n    return "hello"\n    b\n')
        self.indenter.correct_indentation(3)
        self.assertEquals('def f():\n    return "hello"\nb\n', self.editor.get_text())

    def test_deindenting_after_raise(self):
        self.editor.set_text('def f():\n    raise Exception()\n    b\n')
        self.indenter.correct_indentation(3)
        self.assertEquals('def f():\n    raise Exception()\nb\n', self.editor.get_text())

    def test_multiple_indents(self):
        self.editor.set_text('def f():\n')
        self.indenter.correct_indentation(2)
        self.indenter.correct_indentation(2)
        self.assertEquals('def f():\n    ', self.editor.get_text())

    def test_implicit_continuation(self):
        self.editor.set_text('def f(a,\nb):')
        self.indenter.correct_indentation(2)
        self.assertEquals('def f(a,\n      b):', self.editor.get_text())

    def test_double_parens(self):
        self.editor.set_text('def f(a, (c, b),\ne):')
        self.indenter.correct_indentation(2)
        self.assertEquals('def f(a, (c, b),\n      e):', self.editor.get_text())

    def test_double_parens(self):
        self.editor.set_text('def f(a, (c, \nb), e):')
        self.indenter.correct_indentation(2)
        self.assertEquals('def f(a, (c, \n          b), e):', self.editor.get_text())

    def test_implicit_continuation2(self):
        self.editor.set_text('d = {"age" : 20, \n"name" : "Ali"}')
        self.indenter.correct_indentation(2)
        self.assertEquals('d = {"age" : 20, \n     "name" : "Ali"}', self.editor.get_text())

    def test_deindents_after_implicit_continuation(self):
        self.editor.set_text('f(a,\n      b)\na = 10')
        self.indenter.correct_indentation(3)
        self.assertEquals('f(a,\n      b)\na = 10', self.editor.get_text())

    def test_deindents_after_implicit_continuation_after_double_parens(self):
        self.editor.set_text('def f(a, (c, \nb), e):\na=b')
        self.indenter.correct_indentation(2)
        self.indenter.correct_indentation(3)
        self.assertEquals('def f(a, (c, \n          b), e):\n    a=b', self.editor.get_text())

    def test_implicit_continuation_after_return(self):
        self.editor.set_text('def f():\n    return (2,\n3)')
        self.indenter.correct_indentation(3)
        self.assertEquals('def f():\n    return (2,\n            3)', self.editor.get_text())

    def test_implicit_continuation_after_dots(self):
        self.editor.set_text('a_var.an_attr.\\\na_method()')
        self.indenter.correct_indentation(2)
        self.assertEquals('a_var.an_attr.\\\n      a_method()', self.editor.get_text())

    def test_deindenting_empty_lines(self):
        self.editor.set_text('\n')
        self.indenter.deindent(2)
        self.assertEquals('\n', self.editor.get_text())

    def test_deindenting_four_spaces(self):
        self.editor.set_text('    print "hello"\n')
        self.indenter.deindent(1)
        self.assertEquals('print "hello"\n', self.editor.get_text())

    def test_deindenting(self):
        self.editor.set_text('def f()\n    print "hello"\n    def g():\n')
        self.indenter.deindent(3)
        self.assertEquals('def f()\n    print "hello"\ndef g():\n', self.editor.get_text())

    def test_normal_indenter_indenting(self):
        self.editor.set_text('a sample text')
        indenter = NormalIndenter(self.editor)
        indenter.indent(1)
        self.assertEquals('    a sample text', self.editor.get_text())

    def test_normal_indenter_deindenting(self):
        self.editor.set_text('a sample \n        text')
        indenter = NormalIndenter(self.editor)
        indenter.deindent(2)
        self.assertEquals('a sample \n    text', self.editor.get_text())

    def test_indenting(self):
        self.editor.set_text('print "a"')
        self.indenter.indent(1)
        self.assertEquals('    print "a"', self.editor.get_text())

    def test_not_doing_anything_in_noraml_indenters_correct_indentation(self):
        self.editor.set_text('a sample \ntext')
        indenter = NormalIndenter(self.editor)
        indenter.correct_indentation(2)
        self.assertEquals('a sample \ntext', self.editor.get_text())

    def test_inserting_tab(self):
        self.editor.set_text('print "a"')
        self.indenter.insert_tab(self.editor.get_end())
        self.assertEquals('print "a"    ', self.editor.get_text())

    def test_ignoring_parens_in_strings(self):
        self.editor.set_text('print "("\na = 10')
        self.indenter.correct_indentation(2)
        self.assertEquals('print "("\na = 10', self.editor.get_text())

    def test_ignoring_parens_in_comments(self):
        self.editor.set_text('# hello ( \na = 10')
        self.indenter.correct_indentation(2)
        self.assertEquals('# hello ( \na = 10', self.editor.get_text())

    def test_deindenting_after_implicit_continuation_after_return(self):
        self.editor.set_text('def f():\n    return (2,\n            3)\na = 10')
        self.indenter.correct_indentation(4)
        self.assertEquals('def f():\n    return (2,\n            3)\na = 10',
                          self.editor.get_text())

    def test_ignoring_back_slash_in_comments(self):
        self.editor.set_text('# hello \\\na = 10')
        self.indenter.correct_indentation(2)
        self.assertEquals('# hello \\\na = 10', self.editor.get_text())

    def test_entering_a_new_line(self):
        self.editor.set_text('\n')
        self.indenter.entering_new_line(0)
        self.assertEquals('\n', self.editor.get_text())

    def test_entering_a_new_line(self):
        self.editor.set_text('def f():\n')
        self.indenter.entering_new_line(2)
        self.assertEquals('def f():\n    ', self.editor.get_text())

    def test_entering_a_new_line2(self):
        self.editor.set_text('def f():\n    print "hey"\n\n')
        self.indenter.entering_new_line(4)
        self.assertEquals('def f():\n    print "hey"\n\n', self.editor.get_text())

    def test_line_breaks_after_open_parens(self):
        self.editor.set_text('a_func(\narg)\n')
        self.indenter.correct_indentation(2)
        self.assertEquals('a_func(\n    arg)\n', self.editor.get_text())

    def test_line_breaks_after_equals(self):
        self.editor.set_text('a_var = \\\nNone\n')
        self.indenter.correct_indentation(2)
        self.assertEquals('a_var = \\\n    None\n', self.editor.get_text())

    def test_indenting_a_line_like_the_previous_line(self):
        self.editor.set_text('    line1\nline2')
        indenter = NormalIndenter(self.editor)
        indenter.correct_indentation(2)
        self.assertEquals('    line1\n    line2', self.editor.get_text())

    def test_indenting_the_first_line(self):
        self.editor.set_text('    line1\n')
        indenter = NormalIndenter(self.editor)
        indenter.correct_indentation(1)
        self.assertEquals('line1\n', self.editor.get_text())

    # TODO: More work on the effects of current and previous lines
    def xxx_test_else_after_break(self):
        self.editor.set_text('for i in range(1):\n' +
                             '    if True:\n' +
                             '        break\n' +
                             '    else:\n')
        self.indenter.correct_indentation(4)
        self.assertEquals('for i in range(1):\n' +
                          '    if True:\n' +
                          '        break\n' +
                          '    else:\n',
                          self.editor.get_text())

    def test_line_break_after_inner_parens(self):
        self.editor.set_text('a_func(a_func(\na_var)')
        self.indenter.correct_indentation(2)
        self.assertEquals('a_func(a_func(\n       a_var)',
                          self.editor.get_text())

    def test_comments_after_colon(self):
        self.editor.set_text('if False: # comments\npass')
        self.indenter.correct_indentation(2)
        self.assertEquals('if False: # comments\n    pass',
                          self.editor.get_text())

    def test_returns_with_no_args(self):
        self.editor.set_text('def f():\n    return\n    var = 1\n')
        self.indenter.correct_indentation(3)
        self.assertEquals('def f():\n    return\nvar = 1\n',
                          self.editor.get_text())

    def get_range_finder(self, code, line):
        result = _StatementRangeFinder(
            codeanalyze.ArrayLinesAdapter(code.split('\n')), line)
        return result

    def test_simple_statement_finding(self):
        finder = self.get_range_finder('a = 10', 1)
        self.assertEquals(1,  finder.get_statement_start())

    def test_get_start(self):
        finder = self.get_range_finder('a = 10\nb = 12\nc = 14', 1)
        self.assertEquals(1,  finder.get_statement_start())

    def test_get_last_open_parens(self):
        finder = self.get_range_finder('a = 10', 1)
        self.assertTrue(finder.last_open_parens() is None)

    def test_get_last_open_parens2(self):
        finder = self.get_range_finder('a = (10 +', 1)
        self.assertEquals((1, 4), finder.last_open_parens())

    def test_is_line_continued(self):
        finder = self.get_range_finder('a = 10', 1)
        self.assertFalse(finder.is_line_continued())

    def test_is_line_continued2(self):
        finder = self.get_range_finder('a = (10 +', 1)
        self.assertTrue(finder.is_line_continued())

    def test_is_line_continued2(self):
        finder = self.get_range_finder('a = (10 +', 1)
        self.assertTrue(finder.is_line_continued())


if __name__ == '__main__':
    unittest.main()

