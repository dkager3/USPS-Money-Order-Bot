import os
import time
from pathlib import Path

# Logging codes
VERBOSE = 0
INFO    = 1
WARNING = 2
ERROR   = 3

class Logger:
  """
  Class to log events that occur in the program.
  
  Attributes
  ----------
  console_logging : bool
    Print log to console
  file_logging : bool
    Write log to file
  verbose : bool
    Print/write verbose logs
  max_log_len : int
    Maximum length of a log line
  logs_folder : pathlib.<PlatformPath>
    Path to the logs folder
  log_file : pathlib.<PlatformPath>
    Full path to the log file
  
  Methods
  -------
  setConsoleLogging
    Sets whether or not to output logs to console
  setFileLogging(code)
    Sets whether or not to output logs to file
  setVerbose(code)
    Sets verbose logging setting
  setMaxLogLen(code)
    Sets maximum length of each log entry
  setLogFile(code)
    Sets the path of the log file
  removeLogs(code)
    Removes logs from log file directory
  log(code)
    Logs given message according to the set logging settings
  """
  
  def __init__(self):
    """
    Constructor.
    
    Parameters
    ----------
      None
    """
    
    self.console_logging = False
    self.file_logging = False
    self.verbose = False
    self.max_log_len = 70
    self.logs_folder = None
    self.log_file = None
  
  def setConsoleLogging(self, val):
    """
    Enable/disable console logging.
    
    Paramters
    ---------
      val : bool
        Value to enable/disable console logging
    
    Returns
    -------
      None
    """
    
    self.console_logging = val
    
  def setFileLogging(self, val):
    """
    Enable/disable file logging.
    
    Paramters
    ---------
      val : bool
        Value to enable/disable file logging
    
    Returns
    -------
      None

    """
    
    self.file_logging = val   

  def setVerbose(self, val):
    """
    Enable/disable verbose logging.
    
    Paramters
    ---------
      val : bool
        Value to enable/disable verbose logging
    
    Returns
    -------
      None
    """
    
    self.verbose = val

  def setMaxLogLen(self, val):
    """
    Set max log message length.
    
    Paramters
    ---------
      val : int
        Value to set the max log message length
    
    Returns
    -------
      None
    """
    
    self.max_log_len = 70
  
  def setLogFile(self, folder_path, file_name):
    """
    Set max log message length.
    
    Paramters
    ---------
      folder_path : str
        Path to logs folder
      file_name : str
        Name of the log file
    
    Returns
    -------
      None
    """
    
    self.logs_folder = Path(folder_path).absolute().resolve()
    if not os.path.exists(self.logs_folder):
      os.mkdir(self.logs_folder)
    self.log_file = self.logs_folder / file_name
    
  def removeLogs(self):
    """
    Removes old logs from logs folder.
    
    Paramters
    ---------
      None
    
    Returns
    -------
      None
    """
    
    try:
      self.log_file.unlink()
    except:
      pass

  def log(self, logmsg, event_type=INFO):
    """
    Set max log message length.
    
    Paramters
    ---------
      logmsg : str
        Message to log
      event_type : int
        Type of message to log
    
    Returns
    -------
      None
    """
    
    event_time = time.ctime(time.time())
    contentList = []
    
    # If verbose message and verbose setting is "off"
    if (not self.verbose) and (event_type == VERBOSE):
      return
    
    if len(logmsg) > self.max_log_len:
      logmsg = logmsg[0:config.msg_len]
      
    if event_type == VERBOSE:
      contentList.append("[VERBOSE]")
    elif event_type == WARNING:
      contentList.append("[WARNING]")
    elif event_type == ERROR:
      contentList.append("[ERROR]")
    else:
      contentList.append("[INFO]")
        
    contentList.append("{} ET".format(str(event_time)))
    contentList.append(logmsg)
    
    content = "{: <7} {: <25} {: <50}".format(*contentList)
    
    if self.console_logging:
      print(content)
    
    if self.file_logging and self.log_file is not None:
      if not self.logs_folder.exists():
        print("Error: Invalid path to run log ({})".format(self.log_file))
      else:
        try:
          with open(self.log_file, "a") as run_log:
            run_log.write(content)
            run_log.write("\n")
        except:
          print("Error writing to {}".format(self.log_file))
