import re
import smtplib
from email.mime.text import MIMEText

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

  def send(self, email):
    response = email.should_send()
    if not isinstance(response, OK):
      return response
    else:
      sender = email.sender
      recipients = email.recipients
      try:
        content = email.as_string()
        self.server.sendmail(sender, recipients, content)
      except Exception:
        return Failure("Problem sending the email")
      return OK("Sent OK")

class Email(object):
  def __init__(self, sender, recipients, subject, template, data):
    self.sender = sender
    self.recipients = self.parse_recipients(recipients)
    self.subject = subject
    self.template = template
    self.data = data

  def parse_recipients(self, recipients):
    if isinstance(recipients, str):
      return [recipients]
    else:
      return recipients

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

  def get_text_body(self):
    return self.template.render(self.data)

  def as_string(self):
    text = self.get_text_body()
    msg = MIMEText(text)
    msg['Subject'] = self.subject
    msg['From'] = self.sender
    msg['To'] = ', '.join(self.recipients)
    return msg.as_string()
