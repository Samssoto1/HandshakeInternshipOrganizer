# Import all necessities from Tkinter (GUI)
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog

# Import all necessities from Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Web driver updater
from webdriver_manager.chrome import ChromeDriverManager # utilzied for auto updating / installing chrome driver (necessarry for selenium)

# Control amount of time between commands
import time

# Tools used in sorting by date
from datetime import datetime # utilized to convert date into a datetime object
import re # Needed for regex

class Internship:
    '''An internship object is created for each internship read from Handshake'''
    def __init__(self, name, company, location, expiration, exp_date_time):
        self.name = name
        self.company = company
        self.location = location
        self. expiration = expiration
        self.exp_date_time = exp_date_time # Using the expiration data, create another variable in pythons date:time format. (Used to make sorting easier)

def organize_internships(driver):
    print('Preparing to scan internships')
    page_num = 0
    list_of_internships = []
    list_done = False
    while list_done == False:
        page_num += 1
        print('Scanning through page {}'.format(page_num))
        time.sleep(5)
        # Creates a multitude of variables that reference values from important elements needed from the saved internships page
        # list_of_names = driver.find_elements_by_xpath('//div[@class="style__job-title___dJ-Z5"]')
        list_of_names = driver.find_elements(By.XPATH, '//div[@class="style__job-title___dJ-Z5"]')
        # list_of_companies = driver.find_elements_by_xpath('//div[@class="style__job-detail___2ot5x"]/span')
        list_of_companies = driver.find_elements(By.XPATH, '//div[@class="style__job-detail___2ot5x"]/span')
        # list_of_locations = driver.find_elements_by_xpath('//div[@class="style__job-location___XliB3"]')
        list_of_locations = driver.find_elements(By.XPATH, '//div[@class="style__job-location___XliB3"]')
        # list_of_expiration_date = driver.find_elements_by_xpath('//div[@class="style__expiration-date___3hSCG"]')
        list_of_expiration_date = driver.find_elements(By.XPATH, '//div[@class="style__expiration-date___3hSCG"]')
        # Init variables needed for working with the Internship objects
        new_internship = ""
        internship_id = -1
        time.sleep(5) # Program must pause for a short amount of time in order for all of the elements to be loaded into the variables
        # Itterate through all the arrays
        for n, c, l, e in zip(list_of_names, list_of_companies, list_of_locations, list_of_expiration_date):
            # Translate Handshake date into the appropriate format
            adjusted_date_and_year = e.text
            adjusted_date_and_year = (re.sub('[^0123456789, ]', '', adjusted_date_and_year)) # remove characters that aren't 0-9 ',' or ' ' (Ex: February 15, 2022 ->    15, 2022)
            adjusted_date_and_year = adjusted_date_and_year[3:] # remove the leftover 3 spaces (leftover from between the "apply by february 13, 2022")
            
            if adjusted_date_and_year[1].isdigit() == False: # if [1] is a digit.. this tells us the day provided is between 1-9, thus, to convert to datetime formatting we add a 0 (ex: 6 -> 06)
                adjusted_date_and_year = " 0" + adjusted_date_and_year
            else: 
                adjusted_date_and_year = " " + adjusted_date_and_year
            adjusted_month = (e.text)[9:12] # grab the abbreviated month (ex: Apply by February 13, 2022 -> Febr)
            adjusted_expiration = adjusted_month + adjusted_date_and_year # concat the adjusted month and year together into a string
            exp_date_time = datetime.strptime(adjusted_expiration, '%b %d, %Y') # convert that string into a datetime object (for easy sorting)

            internship_id += 1
            new_internship = internship_id
            new_internship = Internship(n.text, c.text, l.text, e.text, exp_date_time) # Create a new internship object
            list_of_internships.append(new_internship) # append that object
            del new_internship # delete the object

        # Once out of the loop.... if theres additional saved internship pages remaining.. click on the next button and go to the next page
        if driver.find_element(By.XPATH, '//button[@data-hook="search-pagination-next"]').is_enabled():
            driver.find_element(By.XPATH, '//button[@data-hook="search-pagination-next"]').click()
            time.sleep(1)
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "style__heading___29i1Z.style__fitted___3L0Tr")))
        else:
            list_done = True


    #Sort the internships by Python datetime object
    print('Sorting internships..')
    list_of_sorted_internships = sorted(list_of_internships, key=lambda x: x.exp_date_time) # sort by each internships datetime obj via: exp_date_time
    
    # Write the organized internships to a new text file
    print('Writing to organized_internships.txt')
    textfile = open("organized_internships.txt", "w", encoding="utf-8")
    for internship in list_of_sorted_internships:
        textfile.write(internship.name + "\n")
        textfile.write(internship.company + "\n")
        textfile.write(internship.location + "\n")
        textfile.write(internship.expiration + "\n")
        textfile.write("\n")
    textfile.close()
    print('Complete!')
    print('\nSaved Handshake internships have been organized by deadline date.')
    
def is_info_empty(username, password):
    '''Returns True if either the username or password inputs are empty'''
    if is_user_filled(username) == False or is_pass_filled(password) == False:
        return True
    else:
        return False

def is_user_filled(username):
    '''Returns False if username is empty'''
    if username == "":
        return False
    else:
        return True

def is_pass_filled(password):
    '''Returns False if password is empty'''
    if  password == "":
        return False
    else:
        return True

def close_gui_window(driver, window):
    driver.close()
    window.destroy()

def chrome_driver_reference():
    '''Return chromedriver if properly installed, otherwise return False'''
    try:
        option = webdriver.ChromeOptions()
        option.add_argument("--ignore-certificate-error")
        option.add_argument("--ignore-ssl-errors")
        # option.add_argument('headless') # This can be commented out if user wants to see automation process
        option.add_argument("--log-level=3")
        return webdriver.Chrome(ChromeDriverManager().install() ,options=option)
    except:
        return False

def direct_to_saved_jobs(driver):
    '''Direct to saved jobs page via Handshake'''
    print('Directing to saved_jobs')

def login(driver, username, password):
    '''Login to Handshake'''
    
    print('Attempting to log in...')
    driver.get('https://byui.joinhandshake.com/saved_jobs')
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "sso-button"))) # Wait until element with classname.. appears
    driver.find_element(By.CLASS_NAME,'sso-button').click()

    # Input username and password into the browser
    username_box = driver.find_element(By.ID, 'username')
    username_box.send_keys(username)
    password_box = driver.find_element(By.ID, 'password')
    password_box.send_keys(password)


    driver.find_element(By.NAME, "submit").click()

    # Wait until Two-factor authentication appears before continuing...
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "duo_form")))
    print('Please verify your Two-factor authentication by answering the phone call and pressing the number 1')
    # Wait until we get off of the Two-factor authentication screen before continuing...
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "style__heading___29i1Z.style__fitted___3L0Tr")))
    try:
        # Redirect to the saved jobs tabs
        driver.get("https://byui.joinhandshake.com/saved_jobs")
        print('Success!')
        return True
    except:
        return False


def critical_error():
    showerror("Handshake Internship Organizer", "A critical error has occured.")

def switch_password_view():
    if password_box.cget('show') == '':
        password_box.config(show='*')
        toggle_btn.config(text="Show Password")
    else:
        password_box.config(show='')
        toggle_btn.config(text="Hide Password")

def start_internship_organizer():
    '''This function facilitates the internship organizer'''
    # Get inputs from username / password gui
    username = username_box.get() 
    password = password_box.get()
    
    # Validate if username and password are empty
    if is_info_empty(username, password) == False:
        try:
            # Check that the chrome driver is working
            driver = chrome_driver_reference()
            if driver != False:
                # Commence login process
                print('Initializing Handshake Internship Organizer')
                login_status = login(driver, username, password)
                if login_status == True: # if user was able to properly log in & redirect to the Handshake Saved Jobs page, continue
                    organize_internships(driver) # Reads data, sorts, and creates a new text file with the sorted data
                    close_gui_window(driver, window)
            else:
                showerror("Handshake Internship Organizer", "The chromedriver failed to run correctly, please uninstall, reinstall, and try again.")
        except:
            critical_error()
            close_gui_window(driver, window)
    else:
        showerror("Handshake Internship Organizer", "The username and password fields must both be filled out.")

### Main ###
'''Main'''
window = Tk()

window.title("Handshake Internship Organizer - Login")
window.configure(bg="grey")
window.geometry("570x600")
window.resizable(False, False)

Label(window, text="Handshake Internship Organizer", bg="grey", fg="white", font="Impact 30 bold") \
    .grid(row=1, column=1, sticky=EW)

# Create Labels for inputs (Username and Password)
Label(window, text="Enter your username:", bg="grey", fg="white", font="none 12 bold") \
    .grid(row=2, column=1, sticky=EW, pady=8)
Label(window, text="Enter your password:", bg="grey", fg="white", font="none 12 bold") \
    .grid(row=4, column=1, sticky=EW, pady=8)

# Create inputs (Username and Password)
username_box = Entry(window, width=48, bg="white")
username_box.grid(row=3, column=1)
password_box = Entry(window,  width=48, bg="white")
password_box.grid(row=5, column=1)
password_box.config(show="*")

# "Show password / Hide password Button"
toggle_btn = Button(window, text="Show Password", command=switch_password_view)
toggle_btn.grid(row=6, column=1, pady=10) 

# "Login button commences the rest of the program"
Button(window, text="Login", width=6, command=start_internship_organizer) \
    .grid(row=7, column=1, pady=10)
window.mainloop()
