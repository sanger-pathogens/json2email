import re
import smtplib

class Response(object):
  def __init__(self, message):
    self.message = message

class Failure(Response):
  pass

class NoContent(Response):
  pass

class OK(Response):
  pass

class EmailServer(object):
  def __init__(self, *args, **kwargs):
    self.server = smtplib.SMTP(*args, **kwargs)

  def __del__(self):
    self.server.quit()

  def send(self, email):
    response = email.should_send()
    if not isinstance(response, OK):
      return response
    else:
      sender = email.sender
      recipients = email.recipients
      try:
        email_content = email.to_string()
        self.server.sendmail(sender, recipients, email_content)
      except Exception:
        return Failure("Problem sending the email")
      return OK("Sent OK")

class Email(object):
  def __init__(self, template, data):
    self.template = template
    self.data = data

  def should_send(self):
    just_whitespace = re.compile('^\s*$')
    try:
      output = self.template.render(self.data)
    except:
      return Failure("Couldn't render email")
    matches = just_whitespace.match(output)
    if matches == None:
      return OK("Seems OK to send")
    else:
      return NoContent("Email was empty")
