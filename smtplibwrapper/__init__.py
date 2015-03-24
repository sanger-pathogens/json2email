import re
import smtplib

class EmailServer(object):
  def __init__(self, *args, **kwargs):
    self.server = smtplib.SMTP(*args, **kwargs)

  def __del__(self):
    self.server.quit()

  def send(self, email):
    (should_send, reason) = email.should_send()
    if not should_send:
      return (False, reason)
    else:
      sender = email.sender
      recipients = email.recipients
      try:
        email_content = email.to_string()
        self.server.sendmail(sender, recipients, email_content)
        self.server.foo()
      except Exception:
        return (False, "Problem sending the email")
      return (True, "Sent OK")

class Email(object):
  def __init__(self, template, data):
    self.template = template
    self.data = data

  def should_send(self):
    just_whitespace = re.compile('^\s*$')
    try:
      output = self.template.render(self.data)
    except:
      return (False, "Couldn't render email")
    matches = just_whitespace.match(output)
    if matches == None:
      return (True, "Seems OK to send")
    else:
      return (False, "Email was empty")
