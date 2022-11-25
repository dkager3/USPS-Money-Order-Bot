#!/usr/bin/python
from BotEmail import BotEmail as be
from BotThreads import StatusCheckThread as sct
from BotThreads import TimerThread as tt
from Config import config
from datetime import datetime
from datetime import timedelta
from Logger import logger as lg
import MoneyOrder as mo
import PySimpleGUI as sg
from threading import Lock

# Globals
INI_FILE = './Config/BotSettings.ini'
STATUS_THREAD_ID = 'StatusThread'
TIMER_THREAD_ID = 'TimerThread'
EMAIL_DISABLED = False
status_lock = Lock()
next_check = None

def init_logger(logger, conf):
  '''
  Inits logger with values from the INI.
  
      Parameters:
          logger (logger.Logger): Logging functionality
          config (configparser.SectionProxy): Config logging settings
      
      Returns:
          None
  '''
  
  try:
    logger.setConsoleLogging(bool(int(conf['log_to_console'])))
  except:
    pass
    
  try:
    logger.setFileLogging(bool(int(conf['log_to_file'])))
  except:
    pass
    
  try:
    logger.setVerbose(bool(int(conf['log_verbose'])))
  except:
    pass
    
  try:
    logger.setMaxLogLen(int(conf['max_log_len']))
  except:
    pass
  
  try:
    logger.setLogFile(conf['log_folder_path'], conf['log_file_name'])
  except:
    pass
    
    
def performStatusCheck(config, window):
  '''
  Initiates Money Order status check.
  
  To initiate the status check, the money order details are
  sent to a thread to perform the status check, as to not hang
  the window.
  
      Parameters:
          config (Config.ConfigSettings): Config settings
          window (PySimpleGUI.Window): GUI window
      
      Returns:
          None
  '''
  
  global EMAIL_DISABLED
  global next_check
  
  # Update window to reflect status being checked
  window['Start'].update(disabled=True)
  order = mo.MoneyOrder(values['-SN_IN-'], values['-PO_IN-'], values['-AMT_IN-'])
  window['-MO_STAT-'].update('Checking status ...')
  
  # Launch thread to check Money Order status
  check_thread = sct.StatusCheckThread(STATUS_THREAD_ID, window, order)
  check_thread.setDaemon(True)
  check_thread.start()
  
  # Update date/time of last and next check
  timestamp = datetime.now()
  window['-LAST_CHECK-'].update(timestamp.strftime('%m/%d/%Y %I:%M:%S %p'))
  try:
    timestamp += timedelta(seconds=int(config.run['check_frequency_sec']))
  except:
    timestamp += timedelta(hours=12)
  
  if not EMAIL_DISABLED:
    next_check = timestamp
    window['-NEXT_CHECK-'].update(timestamp.strftime('%m/%d/%Y %I:%M:%S %p'))
  
def sendAlert(order_status
             ,send_cashed
             ,send_not_cashed
             ,recipient
             ,email_login
             ,email_password):
  '''
  Sends email alert to user if conditions are met
  
      Parameters:
          order_status (int): Status code of the Money Order
          send_cashed (bool): Send alert on cashed Money Order
          send_not_cashed (bool): Send alert on non-cashed Money Order
          email_login (str): Login for bot email
          email_password (str): Password for bot email
      
      Returns:
          Status of sending alert (bool)
  '''
  
  ret = True
  email = be.BotEmail(email_login, email_password)
  subject = "USPS MONEY ORDER STATUS: "
  body = "Hello,"\
         "\n\nPlease see your USPS Money Order status in the subject.\n\nThanks and best regards,\n\nUSPS Money Order Bot"
  
  if order_status == mo.ORDR_CASH and send_cashed:
    subject = subject + "Cashed!"
    ret = email.send(cashed_subject, body, recipient)
  elif order_status == mo.ORDR_NCASH and send_not_cashed:
    subject = subject + "NOT Yet Cashed!"
    ret = email.send(subject, body, recipient)
  
  return ret

def setWindowDefaults(config, window):
  '''
  Sets default values for elements in the GUI window.
  
      Parameters:
          config (Config.ConfigSettings): Config settings
          window (PySimpleGUI.Window): GUI window
      
      Returns:
          None
  '''
  
  global EMAIL_DISABLED
  
  # Populate Money Order serial num if it's in the ini
  try:
    window['-SN_IN-'].update(config.order_details['serial_num'])
  except:
    pass
  
  # Populate Money Order post office num if it's in the ini
  try:
    window['-PO_IN-'].update(config.order_details['post_office_num'])
  except:
    pass
  
  # Populate Money Order amount if it's in the ini
  try:
    window['-AMT_IN-'].update(config.order_details['amount'])
  except:
    pass
  
  # Populate email settings from ini, or disable if the bot's
  # email login info is missing.
  if config.email is None or \
     not('bot_email_login' in config.email and 'bot_email_paswd' in config.email):
    EMAIL_DISABLED = True
    window['-EMAIL-OPT-'].update('Email Options (INI Error: Not Available)')
    window['-EMAIL_RECP-'].update(disabled=True)
    window['-NOTIFY_CASH-'].update(disabled=True)
    window['-NOTIFY_NCASH-'].update(disabled=True)
  else:
    try:
      window['-EMAIL_RECP-'].update(config.email['recipient_email'])
    except:
      pass
      
    try:
      if config.email['notify_cashed'] == '1':
        window['-NOTIFY_CASH-'].update(True)
    except:
      pass
      
    try:
      if config.email['notify_not_cashed'] == '1':
        window['-NOTIFY_NCASH-'].update(True)
    except:
      pass
  
  window['Stop'].update(disabled=True)
  window['-LAST_CHECK-'].update('TBD')
  window['-NEXT_CHECK-'].update('TBD')
  window['-MO_STAT-'].update('TBD')

def startButtonPressed(config, window):
  '''
  Event handler for when the start button is pressed.
  
      Parameters:
          config (Config.ConfigSettings): Config settings
          window (PySimpleGUI.Window): GUI window
      
      Returns:
          None
  '''
  
  global status_lock
  
  if not status_lock.locked():
    status_lock.acquire()
    performStatusCheck(config, window)

def stopButtonPressed(window):
  '''
  Event handler for when the stop button is pressed.
  
  When the stop button is pressed, the GUI updates to reflect that the
  bot is no longer running.
  
      Parameters:
          window (PySimpleGUI.Window): GUI window
      
      Returns:
          None
  '''
  
  global next_check
  
  next_check = None
  window['Stop'].update(disabled=True)
  window['Start'].update(disabled=False)
  window['-NEXT_CHECK-'].update('TBD')

if __name__ == '__main__':
  HEADER_FONT = ("Arial", 14)
  ELEM_FONT = ("Arial", 12)
  
  # Read ini file for bot settings
  config = config.ConfigSettings(INI_FILE)
  if not config.readConfigFile():
    print("WARNING: {} not found or is corrupt. Using default values.".format(INI_FILE))
  
  # Set up logging
  logger = lg.Logger()
  init_logger(logger, config.logging)
  logger.removeLogs()

  # Column layout for Money Order details
  order_col = [
    [sg.Text('Money Order Details', font=HEADER_FONT)]
   ,[sg.Text('Serial Number:', size=(16, 1), font=ELEM_FONT), sg.Input(key='-SN_IN-', size=(15, 20), font=ELEM_FONT)]
   ,[sg.Text('Post Office Number:', size=(16, 1), font=ELEM_FONT), sg.Input(key='-PO_IN-', size=(15, 20), font=ELEM_FONT)]
   ,[sg.Text('Amount:', size=(16, 1), font=ELEM_FONT), sg.Input(key='-AMT_IN-', size=(15, 20), font=ELEM_FONT)]
  ]
  
  # Column layout for email settings
  email_col = [
    [sg.Text('Email Options', font=HEADER_FONT, key='-EMAIL-OPT-')]
   ,[sg.Text('Recipient Address:', font=ELEM_FONT), sg.Input(key='-EMAIL_RECP-', size=(25, 20), font=ELEM_FONT)]
   ,[sg.Checkbox('Notify when Money Order is cashed', key='-NOTIFY_CASH-', font=ELEM_FONT)]
   ,[sg.Checkbox('Notify when Money Order is not yet cashed', key='-NOTIFY_NCASH-',font=ELEM_FONT)]
  ]
  
  # Column layout for control buttons
  control_button_col = [
    [sg.Button('Start', font=HEADER_FONT), sg.Button('Stop', font=HEADER_FONT)]
  ]
  
  # Column layout for status details
  status_col = [
    [sg.Text('Status:', size=(15, 1), font=ELEM_FONT), sg.Text('', font=ELEM_FONT, key='-MO_STAT-')]
   ,[sg.Text('Last Status Check:', size=(15, 1), font=ELEM_FONT), sg.Text('', font=ELEM_FONT, key='-LAST_CHECK-')]
   ,[sg.Text('Next Status Check:', size=(15, 1), font=ELEM_FONT), sg.Text('', font=ELEM_FONT, key='-NEXT_CHECK-')]
  ]
  
  # Combine all column layouts
  layout = [
    [sg.Column(order_col) ,sg.VSeperator() ,sg.Column(email_col)]
   ,[sg.Column(control_button_col)]
   ,[sg.Column(status_col)]
  ]
  
  window = sg.Window('USPS Money Order Status Bot', layout, finalize=True)
  setWindowDefaults(config, window)
  
  try:
    timer_thread = tt.TimerThread(TIMER_THREAD_ID, window, int(config.run['check_frequency_sec']))
  except:
    timer_thread = tt.TimerThread(TIMER_THREAD_ID, window, 43200)
  timer_thread.setDaemon(True)
  timer_thread.start()

  while True:
    event, values = window.read()
    logger.log("Event: {}".format(str(event)), event_type=lg.VERBOSE)
    
    if event == sg.WIN_CLOSED:
      break
    elif event == 'Start':
      startButtonPressed(config, window)
    elif event == 'Stop':
      stopButtonPressed(window)
    elif event == STATUS_THREAD_ID:
      # Avoid re-enabling 'Stop' button if it's been disabled
      # before thread completes. Don't re-enable if periodic
      # checking is not happening.
      if not EMAIL_DISABLED and next_check is not None:
        window['Stop'].update(disabled=False)
      elif EMAIL_DISABLED:
        window['Start'].update(disabled=False)

      # Update status message
      window['-MO_STAT-'].update(values[STATUS_THREAD_ID][1])
      
      # Release lock
      if status_lock.locked():
        status_lock.release()
      
      # Send alerts, if needed
      if not EMAIL_DISABLED:
        if not sendAlert(values[STATUS_THREAD_ID][0]
                        ,values['-NOTIFY_CASH-']
                        ,values['-NOTIFY_NCASH-']
                        ,values['-EMAIL_RECP-']
                        ,config.email['bot_email_login']
                        ,config.email['bot_email_paswd']):
          logger.log("Failed to send email to {}".format(values['-EMAIL_RECP-']), event_type=lg.ERROR)
        else:
          logger.log("Status email sent to {}".format(values['-EMAIL_RECP-']))
      
    elif event == TIMER_THREAD_ID:
      # Periodic status check
      if next_check is not None:
        if not status_lock.locked():
          logger.log("Performing status check", event_type=lg.VERBOSE)
          status_lock.acquire()
          performStatusCheck(config, window)
    
  window.close()