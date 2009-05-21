import re
import string


class Template(object):
    """Templates that are used in code assists

    Variables in templates are in ``${variable}`` format. To put a
    dollar sign in the template put $$.  To specify cursor position
    use ${cursor}.

    """

    def __init__(self, template):
        self.template = template

    var_pattern = re.compile(r'((?<=[^\$])|^)\${(?P<variable>\w+)}')

    def variables(self):
        """Get template variables

        Return the list of variables sorted by their order of
        occurence in the template.

        """
        result = []
        for match in self.var_pattern.finditer(self.template):
            new_var = match.group('variable')
            if new_var not in result and new_var != 'cursor':
                result.append(new_var)
        return result

    def _substitute(self, input_string, mapping):
        single_dollar = re.compile('((?<=[^\$])|^)\$((?=[^{\$])|$)')
        template = single_dollar.sub('$$', input_string)
        t = string.Template(template)
        return t.substitute(mapping, cursor='')

    def substitute(self, mapping):
        return self._substitute(self.template, mapping)

    def get_cursor_location(self, mapping):
        cursor_index = len(self.template)
        for match in self.var_pattern.finditer(self.template):
            new_var = match.group('variable')
            if new_var == 'cursor':
                cursor_index = match.start('variable') - 2
        new_template = self.template[0:cursor_index]
        start = len(self._substitute(new_template, mapping))
        return start


class TemplateProposal(object):

    def __init__(self, name, template):
        self.name = name
        self.kind = 'template'
        self.template = template


def default_templates():
    templates = {}
    templates['main'] = Template("if __name__ == '__main__':\n    ${cursor}\n")
    test_case_template = \
        ('import unittest\n\n\n'
         'class ${TestClass}(unittest.TestCase):\n\n'
         '    def setUp(self):\n        super(${TestClass}, self).setUp()\n\n'
         '    def tearDown(self):\n        super(${TestClass}, self).tearDown()\n\n'
         '    def test_trivial_case${cursor}(self):\n        pass\n\n\n'
         'if __name__ == \'__main__\':\n'
         '    unittest.main()\n')
    templates['testcase'] = Template(test_case_template)
    templates['hash'] = Template('\n    def __hash__(self):\n' +
                                 '        return 1${cursor}\n')
    templates['eq'] = Template('\n    def __eq__(self, obj):\n' +
                               '        ${cursor}return obj is self\n')
    templates['super'] = Template('super(${class}, self)')
    return templates
