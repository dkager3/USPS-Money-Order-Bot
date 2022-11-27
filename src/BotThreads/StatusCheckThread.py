#!/usr/bin/python
from BotThreads import BotThread
from MoneyOrder import MoneyOrder as mo

class StatusCheckThread(BotThread.BotThread):
  """
  Thread to initiate Money Order status check.
  
  Inherits from BotThread.
  
  Attributes
  ----------
  window : PySimpleGUI.Window
    Window object to invoke event for
  order : MoneyOrder.MoneyOrder
    Money Order details
  
  Methods
  -------
  run()
    Performs Money Order status check.
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
      order : MoneyOrder.MoneyOrder
        Money Order details
    """
    
    super().__init__(THREAD_ID)
    self.window = window
    self.order = order
    
  def run(self):
    """
    Performs Money Order status check.
    
    After getting Money Order status, this method invokes an event
    with the status to update the GUI window.
    
    Paramters
    ---------
      None
    
    Returns
    -------
      None
    """
    
    status = self.order.checkStatus()
    self.window.write_event_value(self.THREAD_ID, [status, self.order.statusStr(status)])