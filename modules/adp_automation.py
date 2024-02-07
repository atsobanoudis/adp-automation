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
    page.locator("[aria-label='Enter your User I-D']").type(user_id, delay=random.randint(60, 120))
    time.sleep(random.uniform(1, 2))
    
    if page.locator("[aria-label='Enter your password']").count() == 0:
        page.locator("[aria-label='Enter your User I-D']").press("Enter")
    time.sleep(random.uniform(1, 2))

    # Assuming correction for the selector
    page.locator("[aria-label='Enter your password']").type(password, delay=random.randint(60, 120))
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

def adp_filler(page, formatted_date, df):
    """
    Handles filling date-related fields in ADP after successful login
    """
    select_all = "Meta+A" if platform.system() == "Darwin" else "Control+A"

    # Wait for iframe to load
    page.wait_for_selector("iframe#shellPortletIframe", timeout=60000)
    frame = page.frame_locator("iframe#shellPortletIframe").first

    start_date_locator = frame.locator('input#dateRangestart')
    end_date_locator = frame.locator('input#dateRangeend')

    # Inputs user's date into start range
    start_date_locator.click()
    time.sleep(random.uniform(0.2, 0.8))
    page.keyboard.press(select_all)
    start_date_locator.type(formatted_date, delay=random.randint(60, 120))
    time.sleep(random.uniform(0.2, 0.8))

    # Inputs user's date into end range
    end_date_locator.click()
    time.sleep(random.uniform(0.2, 0.8))
    page.keyboard.press(select_all)
    end_date_locator.type(formatted_date, delay=random.randint(60, 120))
    time.sleep(random.uniform(0.2, 0.8))

    # Submits date range
    frame.locator('text="Find"').click()
    time.sleep(random.uniform(1, 2))

    # Initial textbox counter starts at 1
    validation_textbox_counter = 1 # For string fields
    duration_textbox_counter = 1 # For integer fields (Hours)

    # Iterate through DataFrame rows
    for index, row in df.iterrows():

        # Range of seconds to wait before moving to next form
        min_fill_wait = 0.4
        max_fill_wait = 0.8 

        # Calculate row's unique identifier based on the known pattern
        if index == 0:
            form_row_identifier = 1
        elif index == 1:
            form_row_identifier = 3
        else:
            form_row_identifier = index + 2  # Skips #2 and increments by 1 for each subsequent row

        # Logic to add new row if necessary after the first 5 rows are processed
        if index == 4:
            additional_rows_needed = len(df) - 5
            while additional_rows_needed > 0:
                frame.get_by_label("Options Row 6").click()
                frame.get_by_role("cell", name="Add Blank Row").click()
                additional_rows_needed -= 1
                time.sleep(random.uniform(min_fill_wait, max_fill_wait))  # Wait a bit after adding a row

        # Dynamically build the field identifiers using the row's unique pattern
        pay_code_selector = f"#r_{form_row_identifier}_c_{form_row_identifier}_PayCodeID"
        hours_selector = f"#r_{form_row_identifier}_c_{form_row_identifier}_Value"
        customer_selector = f"#r_{form_row_identifier}_c_{form_row_identifier}_WorkedJobID"
        payroll_item_selector = f"#r_{form_row_identifier}_c_{form_row_identifier}_Lcf5"
        service_item_selector = f"#r_{form_row_identifier}_c_{form_row_identifier}_Lcf6"
        class_selector = f"#r_{form_row_identifier}_c_{form_row_identifier}_Lcf7"
        billable_selector = f"#r_{form_row_identifier}_c_{form_row_identifier}_Lcf8"

        # Fill in Pay Code
        frame.locator(pay_code_selector).click()
        time.sleep(random.uniform(min_fill_wait, max_fill_wait))
        frame.locator(f"#revit_form_ValidationTextBox_{validation_textbox_counter}").type(row['Pay Code'], delay=random.randint(60, 120))
        validation_textbox_counter += 2

        # Fill in the Hours
        frame.locator(hours_selector).click()
        time.sleep(random.uniform(min_fill_wait, max_fill_wait))
        frame.locator(f"#TLMWidgets_TimeEntry_DurationTextBox_{duration_textbox_counter}").type(str(row['Hours']), delay=random.randint(60, 120))
        duration_textbox_counter += 2

        # Fill in the Worked Job ID
        frame.locator(customer_selector).click()
        time.sleep(random.uniform(min_fill_wait, max_fill_wait))
        frame.locator(f"#revit_form_ValidationTextBox_{validation_textbox_counter}").type(row['Customer'], delay=random.randint(60, 120))
        time.sleep(random.uniform(1, 2))
        frame.locator(f"text='{row['Customer']}'").click()
        validation_textbox_counter += 2

        # Fill in the Payroll Item
        frame.locator(payroll_item_selector).click()
        time.sleep(random.uniform(min_fill_wait, max_fill_wait))
        frame.locator(f"#revit_form_ValidationTextBox_{validation_textbox_counter}").type(row['Payroll Item'], delay=random.randint(60, 120))
        validation_textbox_counter += 2

        # Fill in the Service Item
        frame.locator(service_item_selector).click()
        time.sleep(random.uniform(min_fill_wait, max_fill_wait))
        frame.locator(f"#revit_form_ValidationTextBox_{validation_textbox_counter}").type(row['Service Item'], delay=random.randint(60, 120))
        validation_textbox_counter += 2

        # Fill in the Class
        frame.locator(class_selector).click()
        time.sleep(random.uniform(min_fill_wait, max_fill_wait))
        frame.locator(f"#revit_form_ValidationTextBox_{validation_textbox_counter}").type(row['Class'], delay=random.randint(60, 120))
        validation_textbox_counter += 2

        #Fill in the Billable
        frame.locator(billable_selector).click()
        time.sleep(random.uniform(min_fill_wait, max_fill_wait))
        frame.locator(f"#revit_form_ValidationTextBox_{validation_textbox_counter}").type(row['Billable'], delay=random.randint(60, 120))
        validation_textbox_counter += 2

    # Submit sheet for day
    frame.locator("text='Save'").click()

    # Confirming save
    try:
        # Wait for either the success message or the error message, whichever comes first
        success_selector = "text='Operation Successful.'"
        error_selector = "text='Error Saving Employee'"
        page.wait_for_selector(f"{success_selector}, {error_selector}", timeout=300000)  # Adjust timeout as needed
        
        # After waiting, check which message is present
        if page.locator(success_selector).count() > 0:
            print("Operation was successful.")
        elif page.locator(error_selector).count() > 0:
            print("Error Saving Employee. Manual intervention may be required.")
        else:
            print("Unexpected state: neither success nor error message found.")
        
    except Exception as e:
        print(f"An error occurred while waiting for operation completion: {e}")
        time.sleep(300)  # Wait for 5 minutes to allow for manual intervention
    
def adp_automation(user_date, df):
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
        adp_filler(page, formatted_date, df)

    context.close()
    browser.close()