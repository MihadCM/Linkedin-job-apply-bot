from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

ACCOUNT_EMAIL = "admin@gmail.com" # Replace with your LinkedIn email
ACCOUNT_PASSWORD = "123abc"       # Replace with your LinkedIn password
PHONE = "+91 9999999999"          # Replace with your phone number


def abort_application():
    # Click Close Button
    close_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
    close_button.click()

    time.sleep(2)
    # Click Discard Button
    discard_button = driver.find_elements(by=By.CSS_SELECTOR, value='button[data-control-name="discard_application_confirm_btn"]')
    discard_button.click()
    print("dicarded application clicked")


# Optional - Keep the browser open if the script crashes.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.linkedin.com/jobs/search/?currentJobId=4261101801&f_AL=true&geoId=102713980&keywords=python%20automation&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true")



# Click Reject Cookies Button
# reject_button = driver.find_element(by=By.CSS_SELECTOR, value='button[action-type="DENY"]')
# reject_button.click()

# Click Sign in Button
time.sleep(2)
sign_in_button = driver.find_element(by=By.XPATH, value="//*[@id='base-contextual-sign-in-modal']/div/section/div/div/div/div[2]/button")
sign_in_button.click()

# Sign using Email and Password
time.sleep(2)
email_field = driver.find_element(by=By.XPATH, value="//*[@id='base-sign-in-modal_session_key']")
email_field.send_keys(ACCOUNT_EMAIL)
password_field = driver.find_element(by=By.XPATH, value="//*[@id='base-sign-in-modal_session_password']")
password_field.send_keys(ACCOUNT_PASSWORD)
password_field.send_keys(Keys.ENTER)


# CAPTCHA - Solve Puzzle Manually
input("Press Enter when you have solved the Captcha")
time.sleep(6)  # Wait for the user to solve the captcha manually

# Get Listings
time.sleep(2)
all_listings = driver.find_elements(by=By.CSS_SELECTOR, value=".scaffold-layout__list-item")

# all_listings = driver.find_elements(by=By.CSS_SELECTOR, value=".job-card-container--clickable")
# ember-view   lJTERlOdbyLHUMMtJINeUiAZaYwdBnHYHBXU occludable-update p0 relative scaffold-layout__list-item
# all_listings = driver.find_elements(by=By.CSS_SELECTOR, value=".job-card-list__title")

print(f"Found {len(all_listings)} listings")


# Apply for Jobs

count = 0
skipped = 0
for listing in all_listings[:3]:  # Limit to first 3 listings for testing
    print(f"listing: {listing}\n")
    listing.click()
    print("Opening Listing")
    time.sleep(2)
    try:
        # Click Apply Button
        
        apply_button = driver.find_element(by=By.CSS_SELECTOR, value=".jobs-apply-button")
        apply_button.click()
        print("Clicked Apply Button")

        # Find an <input> element where the id contains phoneNumber
        time.sleep(5)

        # phone = driver.find_element(by=By.XPATH, value="//*[@id='single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-4260160447-21469002628-phoneNumber-nationalNumber'']")
        # if phone.text == " ":
        #     phone.send_keys(PHONE)

        # Wait object
        wait = WebDriverWait(driver, 10)

        # Loop to click all "Next" buttons
        while True:
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Continue to next step"]')
                if next_button.is_enabled():
                    next_button.click()
                    print("Clicked Next Button")
                    time.sleep(3)
                else:
                    print(" Next button found but not enabled.")
                    break
            except:
                print(" No more Next button. Going to next step!! Review.")
                break

        # Try to click Review button
        try:
            review_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Review your application"]')))
            review_button.click()
            print("Clicked Review button.")
            time.sleep(3)
        except:
            print("Review button not clickable or not found.")

        # Check the Submit Button
        # submit_button = driver.find_element(by=By.CSS_SELECTOR, value="footer button")
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[data-live-test-easy-apply-submit-button]')
        if submit_button.is_enabled():
            submit_button.click()
            print("Clicked Submit Button")
            count += 1
        else:
            abort_application()
            skipped += 1
            print("Submit button not enabled, application skipped.")
            continue


        # time.sleep(2)
        # # Click Close Button
        # close_button = driver.find_element(by=By.CSS_SELECTOR, value=".artdeco-button__icon ")
        # close_button.click()
        

    except NoSuchElementException:
        abort_application()
        print("No application button, skipped.")
        continue

print(f"total application skipped= {skipped}")
print(f"Applied to {count} jobs")
time.sleep(5)
driver.quit()