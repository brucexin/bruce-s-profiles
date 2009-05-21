import unittest

from ropetest import testutils

from ropeide.templates import Template


class TemplateTest(unittest.TestCase):

    def test_template_get_variables(self):
        template = Template('Name = ${name}')
        self.assertEquals(['name'], template.variables())

    def test_template_get_variables_multiple_variables(self):
        template = Template('Name = ${name}\nAge = ${age}\n')
        self.assertEquals(['name', 'age'], template.variables())

    def test_substitution(self):
        template = Template('Name = ${name}\nAge = ${age}\n')
        self.assertEquals('Name = Ali\nAge = 20\n',
                          template.substitute({'name': 'Ali', 'age': '20'}))

    def test_underlined_variables(self):
        template = Template('Name = ${name_var}')
        self.assertEquals(['name_var'], template.variables())
        self.assertEquals('Name = Ali', template.substitute({'name_var': 'Ali'}))

    @testutils.assert_raises(KeyError)
    def test_unmapped_variable(self):
        template = Template('Name = ${name}')
        template.substitute({})

    def test_double_dollar_sign(self):
        template = Template('Name = $${name}')
        self.assertEquals([], template.variables())
        self.assertEquals('Name = ${name}', template.substitute({'name': 'Ali'}))

    def test_untemplate_dollar_signs(self):
        template = Template('$name = ${value}')
        self.assertEquals(['value'], template.variables())
        self.assertEquals('$name = Ali', template.substitute({'value': 'Ali'}))

    def test_template_get_variables_multiple_variables2(self):
        template = Template('Name = ${name}${age}\n')
        self.assertEquals(['name', 'age'], template.variables())

    def test_template_get_variables_start_of_the_string(self):
        template = Template('${name}\n')
        self.assertEquals(['name'], template.variables())

    def test_the_same_variable_many_times(self):
        template = Template("Today is ${today}, the day after ${today} is ${tomorrow}")
        self.assertEquals(['today', 'tomorrow'], template.variables())
        self.assertEquals("Today is 26th, the day after 26th is 27th",
                         template.substitute({'today': '26th', 'tomorrow': '27th'}))

    def test_cursor_in_templates(self):
        template = Template('My name is ${name}${cursor}.')
        self.assertEquals(['name'], template.variables())
        self.assertEquals('My name is Ali.', template.substitute({'name': 'Ali'}))

    def test_get_cursor_location(self):
        template = Template('My name is ${name}${cursor}.')
        self.assertEquals(14, template.get_cursor_location({'name': 'Ali'}))

    def test_get_cursor_location_with_no_cursor(self):
        template = Template('My name is ${name}.')
        self.assertEquals(15, template.get_cursor_location({'name': 'Ali'}))


if __name__ == '__main__':
    unittest.main()
