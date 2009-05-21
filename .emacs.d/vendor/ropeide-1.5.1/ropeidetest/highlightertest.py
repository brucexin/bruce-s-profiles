import unittest

from ropeide.highlighter import (PythonHighlighting, HighlightingStyle,
                                 ReSTHighlighting, NoHighlighting)
class HighlightTest(unittest.TestCase):

    def setUp(self):
        self.highlighting = PythonHighlighting()
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def _assertOutcomesEquals(self, text, expected, not_expected=[], start=None, end=None):
        if start is None:
            start = 0
        if end is None:
            end = len(text)
        highlights = []
        for result in self.highlighting.highlights(text, start, end):
            highlights.append(result)
        for highlight in expected:
            self.assertTrue(highlight in highlights)
        for highlight in not_expected:
            self.assertTrue(highlight not in highlights)

    def testKeywordHighlighting(self):
        text = 'def sample_function():\n    pass\n'
        highs = [(0, 3, 'defkeyword'), (27, 31, 'keyword')]
        self._assertOutcomesEquals(text, highs)

    def testKeywordHighlighting2(self):
        text = 'import re\nclass Test(object):\n    def f(self):\npass\n'
        highs = [(0, 6, 'keyword'), (10, 15, 'defkeyword'),
                 (34, 37, 'defkeyword'), (47, 51, 'keyword')]
        self._assertOutcomesEquals(text, highs)

    def testKeywordHighlighting3(self):
        text = '   for x in range(10):'
        highs = [(3, 6, 'keyword'), (9, 11, 'keyword')]
        self._assertOutcomesEquals(text, highs)

    def test_not_highlighting_keywords_when_partof_other_words(self):
        text = 'class_'
        not_highs = [(0, 5, 'keyword')]
        self._assertOutcomesEquals(text, [], not_highs)

    def test_not_highlighting_keywords_when_partof_other_words2(self):
        text = 'in_for_class = def3 + _def + def_ + def_while'
        not_highs = [(0, 2, 'keyword'), (3, 6, 'keyword'), (7, 12, 'keyword'),
                     (0, 2, 'keyword'), (15, 18, 'keyword'), (29, 32, 'keyword'),
                     (36, 39, 'keyword'), (40, 45, 'keyword')]
        self._assertOutcomesEquals(text, [], not_highs)

    def test_no_highlighting(self):
        noHigh = NoHighlighting()
        text = 'def sample_function():\n    pass\n'
        expected = []
        for result in noHigh.highlights(text, None, None):
            self.assertEquals(expected[0], result)
            del expected[0]
        self.assertFalse(expected)

    def test_get_styles(self):
        self.assertEquals(True, 'keyword' in self.highlighting.get_styles())
        self.assertTrue(isinstance(self.highlighting.get_styles()['keyword'], HighlightingStyle))

    def test_following_keywords(self):
        text = 'if not'
        highs = [(0, 2, 'keyword'), (3, 6, 'keyword')]
        self._assertOutcomesEquals(text, highs)

    def test_keywords_in_strings(self):
        text = 's = " def "'
        not_highs = [(6, 9, 'keyword')]
        self._assertOutcomesEquals(text, [], not_highs)

    def test_function_definition(self):
        text = 'def func(args):'
        highs = [(0, 3, 'defkeyword'), (4, 8, 'definition')]
        self._assertOutcomesEquals(text, highs)

    def test_class_definition(self):
        self.assertTrue('definition' in self.highlighting.get_styles())
        text = 'class Sample(object):'
        highs = [(0, 5, 'defkeyword'), (6, 12, 'definition')]
        self._assertOutcomesEquals(text, highs)

    def test_comments(self):
        self.assertTrue('comment' in self.highlighting.get_styles())
        text = 'a = 2 # Hello world\ntest = 12'
        highs = [(6, 19, 'comment')]
        self._assertOutcomesEquals(text, highs)

    def test_long_strings(self):
        self.assertTrue('string' in self.highlighting.get_styles())
        text = "a = '''2 # multiline \n comments'''\nb = 2"
        highs = [(4, 34, 'string')]
        self._assertOutcomesEquals(text, highs)

    def test_highlighting_a_part_of_editor(self):
        text = 'print a\nprint b\nprint c'
        highs = [(8, 13, 'keyword')]
        not_highs = [(0, 5, 'keyword'), (16, 21, 'keyword')]
        self._assertOutcomesEquals(text, highs, not_highs, start=8, end=15)

    def test_highlighting_builtins(self):
        self.assertTrue('builtin' in self.highlighting.get_styles())
        text = 'a = None'
        highs = [(4, 8, 'builtin')]
        self._assertOutcomesEquals(text, highs)

    def test_suspected_region_for_triples(self):
        text = '"""\nhello\n"""'
        suspected = self.highlighting.get_suspected_region_after_change(text, 11, 12)
        self.assertEquals((0, len(text)), suspected)

    def test_suspected_region_for_triples2(self):
        text = '"""\nhello\n"""'
        suspected = self.highlighting.get_suspected_region_after_change(text, 2, 3)
        self.assertEquals((0, len(text)), suspected)


class ReSTHighlightTest(unittest.TestCase):

    def setUp(self):
        self.highlighting = ReSTHighlighting()
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def in_highlights(self, text, expected):
        highlights = []
        for result in self.highlighting.highlights(text, 0, len(text)):
            highlights.append(result)
        return expected in highlights

    def test_highlighting_section_titles(self):
        self.assertTrue('title' in self.highlighting.get_styles())
        self.assertTrue(self.in_highlights('My Title\n========\n', (0, 8, 'title')))

    def test_highlighting_section_titles2(self):
        self.assertTrue(self.in_highlights('========\nMy Title\n========\n', (9, 17, 'title')))

    def test_highlighting_section_titles3(self):
        self.assertTrue(self.in_highlights('\nMy Title\n========\n', (1, 9, 'title')))

    def test_list_signs(self):
        self.assertTrue('listsign' in self.highlighting.get_styles())
        self.assertTrue(self.in_highlights('* item # 1\n', (0, 1, 'listsign')))

    def test_list_signs2(self):
        self.assertTrue(self.in_highlights('- item # 1\n', (0, 1, 'listsign')))

    def test_ordered_lists(self):
        self.assertTrue(self.in_highlights('1. item # 1\n', (0, 2, 'listsign')))

    def test_directives(self):
        self.assertTrue('directive' in self.highlighting.get_styles())
        self.assertTrue(self.in_highlights('.. note:: This is a note\n', (0, 9, 'directive')))

    def test_emphasis(self):
        self.assertTrue('emphasis' in self.highlighting.get_styles())
        self.assertTrue(self.in_highlights('*important*', (0, 11, 'emphasis')))

    def test_strong_emphasis(self):
        self.assertTrue('strongemphasis' in self.highlighting.get_styles())
        self.assertTrue(self.in_highlights('**important**', (0, 13, 'strongemphasis')))

    def test_strong_emphasis(self):
        self.assertTrue('literal' in self.highlighting.get_styles())
        self.assertTrue(self.in_highlights('``rope``', (0, 8, 'literal')))

    def test_interpreted(self):
        self.assertTrue('interpreted' in self.highlighting.get_styles())
        self.assertTrue(self.in_highlights('`rope`', (0, 6, 'interpreted')))

    def test_pre_role(self):
        self.assertTrue('pre_role' in self.highlighting.get_styles())
        self.assertTrue(self.in_highlights(':emphasis:`rope`', (0, 10, 'pre_role')))

    def test_post_role(self):
        self.assertTrue('post_role' in self.highlighting.get_styles())
        self.assertTrue(self.in_highlights('`rope`:emphasis:', (6, 16, 'post_role')))

    def test_hyperlink_target(self):
        self.assertTrue('hyperlink_target' in self.highlighting.get_styles())
        self.assertTrue(self.in_highlights('http://rope.sf.net/index.html',
                                           (0, 29, 'hyperlink_target')))

    def test_hyperlink(self):
        self.assertTrue('hyperlink' in self.highlighting.get_styles())
        self.assertTrue(self.in_highlights('rope_', (0, 5, 'hyperlink')))

    def test_hyperlink2(self):
        self.assertTrue(self.in_highlights('`rope homepage`_', (0, 16, 'hyperlink')))

    def test_hyperlink3(self):
        self.assertFalse(self.in_highlights('rope_homepage', (0, 5, 'hyperlink')))

    def test_hyperlink4(self):
        self.assertTrue(self.in_highlights('rope_homepage_', (0, 14, 'hyperlink')))

    def test_hyperlink_in_multilines(self):
        self.assertTrue(self.in_highlights('`rope\nhomepage`_', (0, 16, 'hyperlink')))

    def test_hyperlink_definition(self):
        self.assertTrue('hyperlink_definition' in self.highlighting.get_styles())
        self.assertTrue(self.in_highlights('.. _rope: http://rope.sf.net\n',
                                           (0, 9, 'hyperlink_definition')))

    def test_hyperlink_definition2(self):
        self.assertTrue(self.in_highlights('.. _rope homepage: http://rope.sf.net\n',
                                           (0, 18, 'hyperlink_definition')))

    def test_highlights_in_lists(self):
        self.assertTrue(self.in_highlights('* rope_\n', (2, 7, 'hyperlink')))

    def test_highlights_in_lists2(self):
        self.assertTrue(self.in_highlights('- `rope homepage`_::\n', (2, 18, 'hyperlink')))

    def test_not_highlighting_hyperlinks_in_inline_literals(self):
        self.assertFalse(self.in_highlights('``rope_``', (2, 7, 'hyperlink')))

    def test_highlighting_fields(self):
        self.assertTrue('field' in self.highlighting.get_styles())
        self.assertTrue(self.in_highlights(':Age: 3 months', (0, 5, 'field')))

    def test_escaping(self):
        self.assertFalse(self.in_highlights('\\`Age\\` 3 months', (1, 7, 'interpreted')))

    def test_back_quotes_inside_literals(self):
        self.assertTrue(self.in_highlights('``a`b``', (0, 7, 'literal')))

    def test_following_literals(self):
        self.assertTrue(self.in_highlights('``a````b``', (0, 5, 'literal')))
        self.assertTrue(self.in_highlights('``a````b``', (5, 10, 'literal')))

    def test_suspected_region_for_quotes(self):
        text = '=====\ntitle\n====='
        suspected = self.highlighting.get_suspected_region_after_change(text, 15, 16)
        self.assertEquals((0, len(text)), suspected)

    def test_anonymous_hyperlinks(self):
        self.assertTrue('anonymous_hyperlink' in self.highlighting.get_styles())
        self.assertFalse(self.in_highlights('rope__', (0, 6, 'hyperlink')))
        self.assertTrue(self.in_highlights('rope__', (0, 6, 'anonymous_hyperlink')))

    def test_literals_in_titles(self):
        self.assertTrue(self.in_highlights('``rope``\n--------', (0, 8, 'title')))

    def test_dots_in_hyperlinks(self):
        self.assertTrue(self.in_highlights('rope.rope_', (0, 10, 'hyperlink')))

    def test_hyperlink_definition(self):
        self.assertTrue('literal_block' in self.highlighting.get_styles())
        code = 'here ::\n  line1\n    line2\nnormal\n'
        self.assertTrue(self.in_highlights(code, (code.index('::'), code.index('normal'),
                                                  'literal_block')))

    def test_comments(self):
        self.assertTrue('comment' in self.highlighting.get_styles())
        code = '.. this is a comment\nnormal\n'
        self.assertTrue(self.in_highlights(code, (0, code.index('normal'), 'comment')))

    def test_comments2(self):
        code = 'normal\n\n.. this is a comment\n indented\n  comments\nnormal\n'
        self.assertTrue(self.in_highlights(code, (code.index('..'),
                                                  code.rindex('normal'),
                                                  'comment')))

    def test_comments3(self):
        code = 'normal\n\n..\n indented\n  comments\nnormal\n'
        self.assertTrue(self.in_highlights(code, (code.index('..'),
                                                  code.rindex('normal'),
                                                  'comment')))

    def test_comments4(self):
        code = 'normal\n\n..\n indented\n\nnormal\n'
        self.assertTrue(self.in_highlights(
                        code, (code.index('..'),
                               code.rindex('normal'), 'comment')))

    def test_footnote(self):
        self.assertTrue('footnote' in self.highlighting.get_styles())
        code = '.. [2] this is a footnote\nnormal\n'
        self.assertTrue(self.in_highlights(code, (0, code.index(']') + 2,
                                                  'footnote')))

    def test_footnote2(self):
        code = 'normal\n\n.. [hey] this is a footnote\n indented\n  footnote\nnormal\n'
        self.assertTrue(self.in_highlights(code, (code.index('..'),
                                                  code.rindex(']') + 2,
                                                  'footnote')))

    def test_suspected_region_lists(self):
        text = '* 0\n* 1\n* 2\n* 3\n'
        suspected = self.highlighting.get_suspected_region_after_change(
            text, text.index('2'), text.index('2') + 1)
        self.assertEquals((text.index('* 1'), text.index('* 3') - 1), suspected)


def suite():
    result = unittest.TestSuite()
    result.addTests(unittest.makeSuite(HighlightTest))
    result.addTests(unittest.makeSuite(ReSTHighlightTest))
    return result

if __name__ == '__main__':
    unittest.main()

