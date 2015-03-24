import unittest
from smtplibwrapper import Email, EmailServer
from mock import MagicMock, patch
from smtplib import SMTPResponseException

class TestEmailServer(unittest.TestCase):

  def test_send(self):
    email_server = EmailServer()
    email = MagicMock()
    email_server.server = MagicMock()

    email.should_send.return_value = (False, "Email was empty")
    (succeeded, reason) = email_server.send(email)
    self.assertFalse(succeeded)
    self.assertEqual(reason, "Email was empty")

    email.should_send.return_value = (False, "Couldn't render email")
    (succeeded, reason) = email_server.send(email)
    self.assertFalse(succeeded)
    self.assertEqual(reason, "Couldn't render email")

    email.should_send.return_value = (True, "Seems OK to send")
    (succeeded, reason) = email_server.send(email)
    self.assertTrue(succeeded)
    self.assertEqual(reason, "Sent OK")

    email_server.server.sendmail.side_effect = SMTPResponseException(500, "Fake exception")
    (succeeded, reason) = email_server.send(email)
    self.assertFalse(succeeded)
    self.assertEqual(reason, "Problem sending the email")

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
