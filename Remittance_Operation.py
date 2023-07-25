from selenium.webdriver import ChromeOptions
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time

def login_to_accountium(email, password):
    # Set Chrome options and initialize the driver
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)
    chrome_options.add_argument("--no-sandbox")
    chrome_driver_path ="./chromedriver"
    driver = Chrome(options=chrome_options)

    # Get URL
    driver.get("https://www.myaccountium.ca/")
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.set_page_load_timeout(20)

    # Login
    email_element = driver.find_element(by="xpath", value="//*[@id='email']")
    email_element.click()
    email_element.send_keys(email)
    password_element = driver.find_element(by="xpath", value="//*[@id='password']")
    password_element.click()
    password_element.send_keys(password)
    login = driver.find_element(by="xpath", value="/html/body/div/div/div/form/button")
    driver.execute_script("arguments[0].click();", login)
    return driver


def create_remittance(driver, month, year):

    payroll = driver.find_element(by="xpath", value="//*[@id='payrolla']/p/i")
    driver.execute_script("arguments[0].click();", payroll)

    remittance = driver.find_element(by="xpath", value="//*[@id='payrollmodule']/ul/li[3]/a/p")
    driver.execute_script("arguments[0].click();", remittance)

    add_new = driver.find_element(by="xpath", value="//*[@id='createNewRemittanceButton']")
    driver.execute_script("arguments[0].click();", add_new)

    remittance_report_calendar = driver.find_element(by="xpath", value="//*[@id='Date']")
    remittance_report_calendar.send_keys(month)
    action = ActionChains(driver)
    action.key_down(Keys.ARROW_RIGHT).perform()
    remittance_report_calendar.send_keys(year)
    create_button = driver.find_element(by="xpath", value="//*[@id='createRemittanceReport']")
    create_button.click()
    time.sleep(5)
    alert = Alert(driver)
    alert.accept()
    return driver

def send_email(driver):
    email_dropdown = driver.find_element(by="xpath", value="//*[@id='dropbtn']")
    driver.execute_script("arguments[0].click();", email_dropdown)
    time.sleep(5)
    email = driver.find_element(by="xpath", value="//*[@id='dropdown1']/li[2]/a")
    driver.execute_script("arguments[0].click();", email)
    time.sleep(5)
    alert = Alert(driver)
    alert.accept()
    return driver

def send_existingRemittance(driver, month, year):
    #open remittance
    payroll = driver.find_element(by="xpath", value="//*[@id='payrolla']/p/i")
    driver.execute_script("arguments[0].click();", payroll)
    remittance = driver.find_element(by="xpath", value="//*[@id='payrollmodule']/ul/li[3]/a/p")
    driver.execute_script("arguments[0].click();", remittance)
    container = driver.find_element(by="xpath", value="//*[@id='rowsContainer']")

    # iterate over each row（by tr）
    rows = container.find_elements(by="xpath", value=".//tr")

    for row in rows:
        # Find the first td element in the current row
        index = 1
        first_td = row.find_element(by="xpath", value=f"./td[{index}]")
        # get text form td
        date_text = first_td.text
        print(date_text)
        # Check if the text content matches the entered year and month
        if year in date_text and month in date_text:
            email_dropdown = row.find_element(by="xpath", value=".//*[@id='dropbtn']").click()
            driver.execute_script("arguments[0].click();", email_dropdown)
            time.sleep(5)
            email = row.find_element(by="xpath", value=".// *[ @ id = 'dropdown1'] / li[2] / a")
            driver.execute_script("arguments[0].click();", email)
            time.sleep(5)
            alert = Alert(driver)
            alert.accept()
            return driver
        else:
            create_remittance(driver, month, year)
            return driver


def quit_driver(driver):
    driver.quit()




