import unittest
from smtplibwrapper import Email, EmailServer
from smtplibwrapper import Failure, NoContent, OK
from mock import MagicMock, patch
from smtplib import SMTPResponseException

class TestEmailServer(unittest.TestCase):

  def test_send(self):
    email_server = EmailServer()
    email = MagicMock()
    email_server.server = MagicMock()

    email.should_send.return_value = NoContent("Email was empty")
    response = email_server.send(email)
    self.assertIsInstance(response, NoContent)
    self.assertEqual(response.message, "Email was empty")

    email.should_send.return_value = Failure("Couldn't render email")
    response = email_server.send(email)
    self.assertIsInstance(response, Failure)
    self.assertEqual(response.message, "Couldn't render email")

    email.should_send.return_value = OK("Seems OK to send")
    response = email_server.send(email)
    self.assertIsInstance(response, OK)
    self.assertEqual(response.message, "Sent OK")

    email_server.server.sendmail.side_effect = SMTPResponseException(500, "Fake exception")
    response = email_server.send(email)
    self.assertIsInstance(response, Failure)
    self.assertEqual(response.message, "Problem sending the email")

class TestEmail(unittest.TestCase):

  def test_should_send(self):
    template = MagicMock()
    email = Email(template=template, data={})

    negative_render_return_cases = ['', ' ', ' \n ', ' \t ', ' \n\t ']
    for test_case in negative_render_return_cases:
      email.template.render.return_value = test_case
      self.assertIsInstance(email.should_send(), NoContent, "Should not send if rendered output is '%s'" % test_case)

    positive_render_return_cases = ['foo', '\nfoo']
    for test_case in positive_render_return_cases :
      email.template.render.return_value = test_case
      self.assertIsInstance(email.should_send(), OK, "Should send if rendered output is '%s'" % test_case)

    email.template.render.side_effect = Exception("Fake template rendering exception")
    self.assertIsInstance(email.should_send(), Failure, "Should not send if rendering raises an Exception")
