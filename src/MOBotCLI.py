#!/usr/bin/python
from BotEmail import BotEmail as be
from Config import config
from datetime import datetime
from datetime import timedelta
from Logger import logger as lg
from MoneyOrder import MoneyOrder as mo
import sys
import time

# Globals
INI_FILE = './Config/BotSettings.ini'
EMAIL_DISABLED = False

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
          recipient (str): Email to send status to
          email_login (str): Login for bot email
          email_password (str): Password for bot email
      
      Returns:
          Status of sending alert (bool)
  '''
  
  ret = None
  now = datetime.now()
  email = be.BotEmail(email_login, email_password)
  subject = "[USPS MO STATUS] "
  body = "Hello,"\
         "\n\nPlease see your USPS Money Order status in the subject. "\
         "The status is current as of {}."\
         "\n\nThanks and best regards,\n\nUSPS Money Order Bot".format(now.strftime('%m/%d/%Y %I:%M:%S %p'))
  
  if order_status == mo.ORDR_CASH and send_cashed:
    subject = subject + "Cashed!"
    ret = email.send(cashed_subject, body, recipient)
  elif order_status == mo.ORDR_NCASH and send_not_cashed:
    subject = subject + "NOT Yet Cashed!"
    ret = email.send(subject, body, recipient)
  
  return ret

if __name__ == '__main__':
  # Read ini file for bot settings
  config = config.ConfigSettings(INI_FILE)
  if not config.readConfigFile():
    sys.exit("ERROR: {} not found or is corrupt. Using default values.".format(INI_FILE))
  
  # Set up logging
  logger = lg.Logger()
  init_logger(logger, config.logging)
  logger.removeLogs()

  # Get Money Order details
  try:
    order = mo.MoneyOrder(config.order_details['serial_num']
                         ,config.order_details['post_office_num']
                         ,config.order_details['amount'])
  except:
    logger.log("Money Order details missing from the INI.", event_type=lg.ERROR)
    sys.exit()
  
  # Get email details
  try:
    email_login = config.email['bot_email_login']
    email_paswd = config.email['bot_email_paswd']
    notify_cashed = bool(int(config.email['notify_cashed']))
    notify_not_cashed = bool(int(config.email['notify_not_cashed']))
    recipient = config.email['recipient_email']
  except:
    EMAIL_DISABLED = True
    logger.log("Email disabled. Details missing from the INI.", event_type=lg.WARNING)
  
  # Get frequency to check Money Order status
  try:
    check_frequency_s = int(config.run['check_frequency_sec'])
  except:
    logger.log("Check frequency not in INI. Default = 43200s.", event_type=lg.WARNING)
    check_frequency_s = 43200

  try:
    while True:
      logger.log("Performing status check ...")
      
      # Get time of next check
      timestamp = datetime.now()
      timestamp += timedelta(seconds=check_frequency_s)
      next_check = timestamp.strftime('%m/%d/%Y %I:%M:%S %p')
      
      # Check status and log result
      status = order.checkStatus()
      logger.log("Order Status: {}".format(order.statusStr(status)))
      
      # Send alerts, if needed
      if not EMAIL_DISABLED:
        send_alert_status = sendAlert(status
                                     ,notify_cashed
                                     ,notify_not_cashed
                                     ,recipient
                                     ,email_login
                                     ,email_paswd)
        if send_alert_status is not None:
          if send_alert_status:
            logger.log("Status email sent to {}".format(recipient))
          else:
            logger.log("Failed to send email to {}".format(recipient), event_type=lg.ERROR)
      
      # Log next time a check will occur
      logger.log("Next Check: {}\n".format(next_check))

      # Sleep until next status check   
      time.sleep(check_frequency_s)
  except KeyboardInterrupt:
    logger.log("Bot shutdown")