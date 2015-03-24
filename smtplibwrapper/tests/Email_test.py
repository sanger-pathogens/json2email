import unittest
from smtplibwrapper import Email
from mock import MagicMock

class TestEmail(unittest.TestCase):

  def test_should_send(self):
    template = MagicMock()
    email = Email(template=template, data={})

    empty_template_response = (False, "Email was empty")
    render_failure_response = (False, "Couldn't render email")
    ok_response = (True, "Seems OK to send")

    negative_render_return_cases = ['', ' ', ' \n ', ' \t ', ' \n\t ']
    for test_case in negative_render_return_cases:
      email.template.render.return_value = test_case
      self.assertEqual(email.should_send(), empty_template_response, "Should not send if rendered output is '%s'" % test_case)

    positive_render_return_cases = ['foo', '\nfoo']
    for test_case in positive_render_return_cases :
      email.template.render.return_value = test_case
      self.assertEqual(email.should_send(), ok_response, "Should send if rendered output is '%s'" % test_case)

    email.template.render.side_effect = Exception("Fake template rendering exception")
    self.assertEqual(email.should_send(), render_failure_response, "Should not send if rendering raises an Exception")
