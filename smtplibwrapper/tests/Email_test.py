import unittest
from smtplibwrapper import Email, EmailServer
from smtplibwrapper import Failure, NoContent, OK
from mock import MagicMock, patch
from smtplib import SMTPResponseException

class TestEmailServer(unittest.TestCase):

  def test_send(self):
    email_server = EmailServer()
    email_server.server = MagicMock()

    email = MagicMock()
    email.recipients = ['bob', 'betty']
    email.sender = 'ben'
    email.as_string.return_value = 'An email'

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

    email_server.server.sendmail.assert_called_with('ben', ['bob', 'betty'], 'An email')
    email_server.server.sendmail.reset_mock()

    email_server.server.sendmail.side_effect = SMTPResponseException(500, "Fake exception")
    response = email_server.send(email)
    self.assertIsInstance(response, Failure)
    self.assertEqual(response.message, "Problem sending the email")

    email_server.server.sendmail.assert_called_with('ben', ['bob', 'betty'], 'An email')

class TestEmail(unittest.TestCase):

  def test_parse_recipients(self):
    template = MagicMock()
    email = Email(sender='ben', recipients=['bob', 'betty'], subject='email', template=template, data={})

    self.assertEqual(email.parse_recipients('ben'), ['ben'])
    self.assertEqual(email.parse_recipients(['ben']), ['ben'])
    self.assertEqual(email.parse_recipients(['ben', 'bob']), ['ben', 'bob'])

  def test_should_send(self):
    template = MagicMock()
    email = Email(sender='ben', recipients=['bob', 'betty'], subject='email', template=template, data={})

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

  def test_get_text_body(self):
    template = MagicMock()
    template.render.side_effect = str
    email = Email(sender='ben', recipients=['bob', 'betty'], subject='email', template=template, data={'foo': 'bar'})

    self.assertEqual(email.get_text_body(), "{'foo': 'bar'}")

  def test_as_string(self):
    email = Email(sender='ben', recipients=['bob', 'betty'], subject='email', template=None, data=None)
    email.get_text_body = MagicMock()
    email.get_text_body.return_value = 'Some text'

    expected_string = """\
Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: email
From: ben
To: bob, betty

Some text"""

    self.assertEqual(email.as_string(), expected_string)
