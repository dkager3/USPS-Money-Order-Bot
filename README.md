# USPS-Money-Order-Bot
Periodically checks the status of a USPS money order. Please read this whole document to get a better understanding of how the bot works.

## Dependencies
The following need to be installed to work. Follow the links for instructions on installing each dependency.
* [Python 3](https://www.python.org/downloads/)
* [selenium](https://selenium-python.readthedocs.io/installation.html)
* [chromedriver](https://chromedriver.chromium.org/getting-started)
* [Tk](https://tkdocs.com/tutorial/install.html)
* [PySimpleGUI](https://pypi.org/project/PySimpleGUI/)

## Features
* GUI window
* Logger capable of printing to screen and/or log file
* Email alerts<sup>1</sup>
* Customizability through INI file

<sup>1</sup>INI needs to be properly set. Separate Gmail account with [app password](https://support.google.com/accounts/answer/185833) required for bot to send emails.

## Running the Bot
You can run the bot by navigating to **USPS-Money-Order-Bot/src/** and running:

    python3 MOBot.py

![clip_w_email](https://user-images.githubusercontent.com/47905974/204064951-ed9d571f-f9e1-4a67-a460-f483c7002123.png)

***Bot with email alerts configured***

![clip_wo_email](https://user-images.githubusercontent.com/47905974/204064954-c042a177-99a7-47c7-8678-1f9f1adbb075.png)

***Bot without email alerts configured***

## INI File
The INI file allows for more fine-tune control/customization of the bot. Within the INI, you may:
* Set Money Order details so they populate their respective fields when the bot starts
* Change how frequently the bot checks the status of the Money Order
* Change logging preferences
* Insert email information for the bot to send alerts

### Default Functionality
The default INI file included does not define much other than logging preferences. The bot's default behavior from the INI is the folowing:
* All Money Order fields are blank and need to be filled in
* Email functionality is disabled
* Log messages only printed to the console
* Status checking every two hours

**Note**: In the absence of the INI file, the bot will still default to the behavior above.

### Modifying the INI File
To modify the INI file, you can open **USPS-Money-Order-Bot/src/Config/BotSettings.ini**. Simply update any of the values you'd like, but be careful! The bot expects certain data types from the INI and could crash if you enter something that doesn't make sense. Don't fret, you can always change the INI back to its original state.

Some lines are commented out. You can uncomment them by removing the semicolon at the front of the line, then edit the placeholder value stuck there. For instance:

    [order_details]
    ;serial_num = <serial_num_here>
    ;post_office_num = <post_office_num_here>
    ;amount = <amount_here>
    
Can be edited to something like this:

    [order_details]
    serial_num = 12345678901
    post_office_num = 080540
    amount = 50.00

## Important Notes
* If you check your status too often, USPS might "block" your IP. If that happens, don't fret. Either stop checking for a day or use a VPN for a little while. Eventually your IP will be "unblocked" from checking. I don't know exactly what the threshold is, but setting the bot to check the Money Order status too often can cause this issue.
* The bot emails are configured to be sent through a Gmail account. You'll need one dedicated for the bot if you want it to send you emails to your personal account. Create a new Gmail account and create an app password from the instructions [here](https://support.google.com/accounts/answer/185833). Then feed the email address and app password to the INI file to get email notifications.
* The computer running the bot must NOT be sleeping for it to run properly. If desired, you can change your settings such that your display turns off, but the computer does not go to sleep.
