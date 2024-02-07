# adp_filler.py
from playwright.sync_api import sync_playwright
import sys
import time
import random
import platform  # Import platform to detect the operating system

sys.path.append('..') # Adjust the path accordingly if your main.py is in a different directory
from .secure_login import load_login_details, save_login_details

def launch_browser():
    playwright = sync_playwright().start()
    if platform.system() == "Darwin":  # macOS
        browser = playwright.webkit.launch(headless=False)
    else:  # Windows or other OS -> use *local installation of Chrome*
        with playwright.sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
    return browser

def adp_login(page, user_id, password):
    """
    Handles the login process to ADP
    """
    page.goto("https://workforcenow.adp.com/")
    page.locator("[aria-label='Enter your User I-D']").fill(user_id)
    time.sleep(random.uniform(1, 2))
    
    if page.locator("[aria-label='Enter your password']").count() == 0:
        page.locator("[aria-label='Enter your User I-D']").press("Enter")
    time.sleep(random.uniform(1, 2))

    # Assuming correction for the selector
    page.locator("[aria-label='Enter your password']").fill(password)
    time.sleep(random.uniform(1, 2))
    page.locator("[aria-label='Enter your password']").press("Enter")

    verification_prompt_found = False
    try:
        page.wait_for_selector('text="Get a Verification Code"', timeout=5000)
        verification_prompt_found = True
        print("Verification required. Please complete the verification process in the browser.")
    except:
        print("No immediate verification prompt detected. Proceeding to check for login success.")

    try:
        page.wait_for_selector('text="VIEW TIMECARD"', timeout=60000)
        print("Login and/or verification successful.")
        time.sleep(random.uniform(1, 2))
        page.locator('role=button[name="VIEW TIMECARD"]').click()
    except:
        if verification_prompt_found:
            print("Verification prompt was detected but not completed in time. Please try again.")
        else:
            print("Unable to confirm login success. Please check your credentials or verification status.")
        return False  # Indicates failure to login
    return True  # Indicates successful login

def adp_filler(page, formatted_date):
    """
    Handles filling date-related fields in ADP after successful login
    """
    select_all = "Meta+A" if platform.system() == "Darwin" else "Control+A"

    frame = page.frame_locator("#shellPortletIframe")

    start_date_locator = frame.locator('input#dateRangestart')
    end_date_locator = frame.locator('input#dateRangeend')

    # Inputs user's date into start range
    start_date_locator.click()
    time.sleep(random.uniform(1, 2))
    page.keyboard.press(select_all)
    start_date_locator.fill(formatted_date)
    time.sleep(random.uniform(1, 2))

    # Inputs user's date into end range
    end_date_locator.click()
    time.sleep(random.uniform(1, 2))
    page.keyboard.press(select_all)
    end_date_locator.fill(formatted_date)
    time.sleep(random.uniform(1, 2))

    # Submits date range
    frame.locator('text="Find"').click()
    time.sleep(random.uniform(10, 20))

def adp_automation(user_date):
    user_id, password = load_login_details()
    if not user_id or not password:
        print("No saved login details found. Please enter your login information.")
        user_id = input("User ID: ")
        password = input("Password: ")
        save_login_details(user_id, password)

    formatted_date = user_date.strftime("%m/%d/%Y")

    # OS dependent browsers
    browser = launch_browser()
    context = browser.new_context()
    page = context.new_page()

    if adp_login(page, user_id, password):
        adp_filler(page, formatted_date)

    context.close()
    browser.close()