import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
from datetime import datetime

class BotEmail:
  """
  Class to send emails.
  
  Attributes
  ----------
  login : str
    Login for bot email
  password : str
    Password for bot email
  
  Methods
  -------
  send(subject, body, recipient)
    Sends email to recipient with given subject and body
  """
  
  def __init__(self, login, password):
    """
    Constructor.
    
    Parameters
    ----------
      login : str
        Login for bot email
      password : str
        Password for bot email
    """
    
    self.login = login
    self.password = password
    
  def send(self, subject, body, recipient):
    """
    Sends email to recipient with given subject and body. 
    
    Paramters
    ---------
      subject : str
        Email subject
      body : str
        Email body
      recipient : str
        Email recipient
        
    Returns
    -------
     True if successful, False otherwise : Bool
    """
    
    ret = True
    msg = MIMEMultipart()
    
    try:
      msg["From"] = self.login
      msg["To"] = recipient
      msg["Subject"] = subject
      msg.attach(MIMEText(body, "plain"))
                
      server = smtplib.SMTP("smtp.gmail.com", 587)
      server.starttls()
      server.login(self.login, self.password)

      text = msg.as_string()
      server.sendmail(self.login, recipient, text)
      server.quit()
    except:
      ret = False
    
    return ret