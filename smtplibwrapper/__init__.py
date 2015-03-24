import re

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
