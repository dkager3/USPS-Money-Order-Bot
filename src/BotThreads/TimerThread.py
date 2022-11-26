#!/usr/bin/python
from BotThreads import BotThread
import time

class TimerThread(BotThread.BotThread):
  """
  Thread to start status event timer.
  
  Inherits from BotThread.
  
  Attributes
  ----------
  window : PySimpleGUI.Window
    Window object to invoke event for
  frequency : int
    Frequency (s) in which status check events
    are invoked
  
  Methods
  -------
  run()
    Periodically sends status check event to window.
  """
  
  def __init__(self, THREAD_ID, window, frequency):
    """
    Constructor.
    
    Parameters
    ----------
      THREAD_ID : str
        ID for thread to invoke GUI event
      window : PySimpleGUI.Window
        Window object to invoke event for
      frequency : int
        Frequency (s) in which status check events
        are invoked
    """
    
    super().__init__(THREAD_ID)
    self.window = window
    self.frequency = frequency
    
  def run(self):
    """
    Periodically sends status check event to window.
    
    After getting Money Order status, this method invokes an event
    with the status in the GUI window.
    
    Paramters
    ---------
      None
    
    Returns
    -------
      None
    """
    
    while True:
      self.window.write_event_value(self.THREAD_ID, None)
      time.sleep(self.frequency)