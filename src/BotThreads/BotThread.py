#!/usr/bin/python
import threading
import time

class BotThread (threading.Thread):
  """
  Parent class for bot threads.
  
  Attributes
  ----------
  THREAD_ID : str
    ID for thread to invoke GUI event
  
  Methods
  -------
  run()
    Performs thread task.
  """

  def __init__(self, THREAD_ID):
    """
    Constructor.
    
    Parameters
    ----------
      THREAD_ID : str
        ID for thread to invoke GUI event
    """
    
    threading.Thread.__init__(self)
    self.THREAD_ID = THREAD_ID
      
  def run(self):
    """
    Performs thread task.
    
    This method is overridden in child classes.
    
    Paramters
    ---------
      None
    
    Returns
    -------
      None
    """
    pass