import requests
import os.path
import base64
from email.message import EmailMessage
import datetime
import numpy as np

#Takes a product ID and get's the current product availiability information from the BB Product API for that product
#Where the product id is the final after the final slash of the bestbuy url
#header are used to fool the url to think that it's a human. Without headers, it will take forever for the server to respond
def getAvailability(product_id, url="https://www.bestbuy.ca/api/v2/json/product/", header={"User-Agent": f"Mozilla/5.0 (X11; CrOS x86_64 12871.102.{np.random.randint(0, 145)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.{np.random.randint(0, 145)} Safari/537.36"}, logging=True):
  #Concat string
  url = url + (str(product_id))
  json = requests.get(url, headers=header).json()
  isAvailableOnline = json["availability"]["isAvailableOnline"] #Not False
  onlineAvailability = json["availability"]["onlineAvailability"] #Not "SoldOut"
  onlineAvailabilityCount = json["availability"]["onlineAvailabilityCount"] #> 0
  buttonState = json["availability"]["buttonState"] #Not "SoldOut"
  isAvailableForOrder = json["isAvailableForOrder"] #Not False
  isAvailableForPickup = json["isAvailableForPickup"] #Not "SoldOut"
  isBackorderable = json["isBackorderable"] #Not False
  itemName = json["name"]
  #print(isAvailableOnline, onlineAvailability, onlineAvailabilityCount, buttonState, isAvailableForOrder, isAvailableForPickup, isBackorderable)
  #If any of these is true, then notify
  if (isAvailableOnline != False and (onlineAvailability not in ["SoldOut", "OutOfStockOnBackorder"])) or buttonState != "SoldOut" or isAvailableForOrder != False or isAvailableForPickup != False or isBackorderable != False:
    return product_id, itemName, True
  else:
    return product_id, itemName, False

# prompt: write a function to use gmail to send an email without using any of the functions that I'v written

#This option will need 2fa enable on gmail account and setup app-password. Then use the app-password to login.
#see https://stackoverflow.com/questions/75021886/gmail-smtp-send-535-5-7-8-username-and-password-not-accepted
import smtplib
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, receiver_email, product_id, item_name, logging=True):
  """Sends an email notification using Gmail's SMTP server."""

  msg = MIMEText(f'Item {item_name} with Product ID {product_id} is available.\n Visit: https://www.bestbuy.ca/en-ca/product/{product_id}')
  msg['Subject'] = f'BB Item {item_name} Availability Notice'
  msg['From'] = sender_email
  msg['To'] = receiver_email

  try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
      smtp.login(sender_email, sender_password)
      smtp.send_message(msg)
    if logging:
      print("Email sent successfully!\n")
  except Exception as e:
    print(f"Error occured at login or when sending email: {e}\n")
    
def send_email_error(sender_email, sender_password, receiver_email, product_id, item_name, monitorError, logging=True):
  """Sends an email notification using Gmail's SMTP server."""

  msg = MIMEText(f'An error has occured when trying to get information about Item {item_name} with Product ID {product_id}.\n Link: https://www.bestbuy.ca/en-ca/product/{product_id}. \nThe erorr message is {monitorError}')
  msg['Subject'] = f'Error - Script ran into issues during monitoring'
  msg['From'] = sender_email
  msg['To'] = receiver_email

  try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
      smtp.login(sender_email, sender_password)
      smtp.send_message(msg)
    if logging:
      print("Email sent successfully!\n")
  except Exception as e:
    print(f"Error occured at login or when sending email: {e}\n")
    
    
import time

def startMonitoring(productIDList, toEmail, fromEmail, fromPassword, monitorFrequencyInSec=30, logging=True):

  if logging:
    print(f"Monitor is now active: it will check the following product with the provided produtID every {monitorFrequencyInSec} seconds.\n ProductIds to check are: {productIDList}\n")

  while True:
    #Set up Mailling component
    availabilityList = []
    
    #Set up checks the items for each productID, and add all availiable ones to the availabilityList List
    for productID in productIDList:
      try:
        productID, itemName, isAvailable = getAvailability(productID, logging=logging)
        if isAvailable:
          availabilityList.append((productID, itemName))
        else:
          if logging:
            print(f"Stock {itemName} is currently not available.")
      except Exception as e:
        try:
          productID, itemName, isAvailable = getAvailability(productID, logging=logging)
          if isAvailable:
            availabilityList.append((productID, itemName))
        except Exception as e:
          print(f"An error occurred when checking productID {productID}: {e}\n")
          errorSent = send_email_error(fromEmail, fromPassword, toEmail, productID, itemName, e, logging=logging)
    #Send email for containing all the available products
    for productID, itemName in availabilityList:
      try:
        if logging:
          print(f"Stock {itemName} is currently available, email will be sent shortly.")
        gmailSent = send_email(fromEmail, fromPassword, toEmail, productID, itemName, logging=logging)
      except Exception as e:
        print(f"An error occurred when sending email for productID {productID}: {e}\n")
        return

    #Sleep for monitorFrequencyInSec +- floor(monitorFrequencyInSec/2) seconds
    time.sleep(np.random.randint(monitorFrequencyInSec - (np.floor(monitorFrequencyInSec / 2)), monitorFrequencyInSec + (np.floor(monitorFrequencyInSec / 2))))
    
    
def main():
    #18931348 - 5090 FE
    startMonitoring([18931348], "test@gmail.com", "test@gmail.com", "your app password", monitorFrequencyInSec=30, logging=True)
    
if __name__ == "__main__":
    main()