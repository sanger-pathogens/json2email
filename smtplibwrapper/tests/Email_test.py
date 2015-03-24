import unittest
from smtplibwrapper import Email
from mock import MagicMock

class TestEmail(unittest.TestCase):

  def test_should_send(self):
    template = MagicMock()
    email = Email(template=template, data={})

    negative_render_return_cases = ['', ' ', ' \n ', ' \t ', ' \n\t ']
    for test_case in negative_render_return_cases:
      email.template.render.return_value = test_case
      self.assertFalse(email.should_send(), "Should not send if rendered output is '%s'" % test_case)

    positive_render_return_cases = ['foo', '\nfoo']
    for test_case in positive_render_return_cases :
      email.template.render.return_value = test_case
      self.assertTrue(email.should_send(), "Should send if rendered output is '%s'" % test_case)

    email.template.render.side_effect = Exception("Fake template rendering exception")
    self.assertFalse(email.should_send(), "Should not send if rendering raises an Exception")
