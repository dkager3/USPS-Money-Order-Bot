#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

# Status Codes
PAGE_ACCS  = -1 # Failed to access page
SERN_INPT  = -2 # Failed to input serial number
POST_INPT  = -3 # Failed to input post office number
AMNT_INPT  = -4 # Failed to input order amount
SUBT_FORM  = -5 # Failed to submit form
READ_STAT  = -6 # Failed to read status
PROC_EROR  = -7 # Unable to process request
ORDR_INVL  = -8 # Money Order details are invalid
ORDR_NCASH = 0  # Order not yet cashed
ORDR_CASH  = 1  # Order cashed 

class MoneyOrder:
  """
  Class to store Money Order details and scrape status.
  
  Attributes
  ----------
  serial : str
    Money Order seial number
  post_office : str
    Post office number that sold Money Order
  amount : str
    Amount of money order
  
  Methods
  -------
  checkStatus()
    Scrapes USPS website to see money order status
  statusStr(code)
    Returns explanation of code returned from checkStatus()
  """
  
  def __init__(self, serial, post_office, amount):
    """
    Constructor.
    
    Parameters
    ----------
      serial : str
        Money Order seial number
      post_office : str
        Post office number that sold Money Order
      amount : str
        Amount of money order
    """
    
    self.serial = serial
    self.post_office = post_office
    self.amount = amount

  def checkStatus(self):
    """
    Scrapes USPS website to see money order status.
    
    Paramters
    ---------
      None
    
    Returns
    -------
      Money Order status : int
    """
    
    # Set webdriver options to turn off logging messages and go headless
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('headless')
    web = webdriver.Chrome(options=options)
    
    # Open webpage
    try:
      web.get('https://tools.usps.com/money-orders.htm')
      sleep(2)
    except:
      return PAGE_ACCS
    
    # Input serial number of money order
    try:
      serial_field = web.find_element(By.XPATH, '//*[@id="serialNumberEntered"]')
      serial_field.send_keys(self.serial)
    except:
      return SERN_INPT
      
    # Input post office number of money order
    try:
      post_office_field = web.find_element(By.XPATH, '//*[@id="postOfficeNumber"]')
      post_office_field.send_keys(self.post_office)
    except:
      return POST_INPT

    # Input issued amount of money order
    try:
      amount_field = web.find_element(By.XPATH, '//*[@id="issuedAmountBox"]')
      amount_field.send_keys(self.amount)
    except:
      return AMNT_INPT

    # Submit status request
    try:
      view_status_button = web.find_element(By.XPATH, '//*[@id="viewStatus"]')
      view_status_button.click()
      sleep(2)
    except:
      return SUBT_FORM

    # Extract status message
    try:
      status_msg = web.find_element(By.XPATH, '//*[@id="moStatus"]').text
    except:
      return READ_STAT

    if 'We are unable to process your request at this time' in status_msg:
      return PROC_EROR
    elif 'but not cashed' in status_msg:
      return ORDR_NCASH
    elif 'is invalid' in status_msg:
      return ORDR_INVL
    else:
      return ORDR_CASH
      
  def statusStr(self, code):
    """
    Returns explanation of code returned from checkStatus().
    
    Paramters
    ---------
      None
    
    Returns
    -------
      None
    """
    
    if code == PAGE_ACCS:
      return "Failed to access page." 
    elif code == SERN_INPT:
      return "Failed to input serial number."
    elif code == POST_INPT:
      return "Failed to input post office number."
    elif code == AMNT_INPT:
      return "Failed to input order amount."
    elif code == SUBT_FORM:
      return "Failed to submit form."
    elif code == READ_STAT:
      return "Failed to read status."
    elif code == PROC_EROR:
      return "Unable to process request."
    elif code == ORDR_INVL:
      return "Money Order details are invalid."
    elif code == ORDR_NCASH:
      return "Order not yet cashed."
    elif code == ORDR_CASH:
      return "Order cashed."
    else:
      return "Unknown error code ({}).".format(code)