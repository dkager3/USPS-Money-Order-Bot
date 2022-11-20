#!/usr/bin/python
import threading
from time import sleep
import MoneyOrder as mo

class StatusCheckThread(threading.Thread):
  """
  Thread to initiate Money Order status check.
  
  Attributes
  ----------
  THREAD_ID : str
    ID for thread to invoke GUI event
  window : PySimpleGUI.Window
    Window object to invoke event for
  order : MO.MoneyOrder
    Money Order details
  
  Methods
  -------
  run()
    Performs Money Order status check
  """
  
  def __init__(self, THREAD_ID, window, order):
    """
    Constructor.
    
    Parameters
    ----------
      THREAD_ID : str
        ID for thread to invoke GUI event
      window : PySimpleGUI.Window
        Window object to invoke event for
      order : MO.MoneyOrder
        Money Order details
    """
    
    super(StatusCheckThread, self).__init__()
    self.THREAD_ID = THREAD_ID
    self.window = window
    self.order = order
    
  def run(self):
    """
    Performs Money Order status check.
    
    After getting Money Order status, this method invokes an event
    with the status in the GUI window.
    
    Paramters
    ---------
      None
    
    Returns
    -------
      None
    """
    
    # TODO: Uncomment below line to actually retrieve status
    #self.window.write_event_value(self.THREAD_ID, self.order.statusStr(self.order.checkStatus()))
    
    # Simulation to prevent USPS from thinking I'm spamming them
    # during development
    # TODO: Remove when done
    sleep(2)
    self.window.write_event_value(self.THREAD_ID, self.order.statusStr(mo.ORDR_NCASH))