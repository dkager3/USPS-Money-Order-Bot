#!/usr/bin/python
import configparser

# Status Codes
READ_FAIL = 0 # Failed to read config file
READ_SUCC = 1 # Config file read successfully

class ConfigSettings:
  """
  Class to store config settings from ini file.
  
  Attributes
  ----------
  ini_file : str
    Path to bot settings ini file
  order_details : configparser.SectionProxy
    Order details section in ini file
  run : configparser.SectionProxy
    Run settings section in ini file
  logging : configparser.SectionProxy
    Logging settings section in ini file
  email : configparser.SectionProxy
    Email settings section in ini file
  
  Methods
  -------
  readConfigFile()
    Reads bot settings ini file and stores sections
  """
  
  def __init__(self, ini_file):
    """
    Constructor.
    
    Parameters
    ----------
      ini_file : str
        Path to bot settings ini file
    """
    
    self.ini_file      = ini_file
    self.order_details = None
    self.run           = None
    self.logging       = None
    self.email         = None
    
  def readConfigFile(self):
    """
    Validate ini exists and read it.
    
    Paramters
    ---------
      None
    
    Returns
    -------
      Read status : int
    """

    # Read ini
    config = configparser.ConfigParser()
    try:
      if not config.read(self.ini_file):
        return READ_FAIL
    except:
      return READ_FAIL
    
    # Extract MO details from ini
    try:
      self.order_details = config['order_details']
    except:
      pass
        
    # Extract run settings from ini
    try:
      self.run = config['bot_settings.run']
    except:
      pass
    
    # Extract log settings from ini    
    try:
      self.logging = config['bot_settings.logging']
    except:
      pass
     
    # Extract email settings from ini     
    try:
      self.email = config['bot_settings.email']
    except:
      pass
    
    return READ_SUCC
