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


def create_payroll(driver, year, month, date, employee_details):


    payroll = driver.find_element(by="xpath", value="//*[@id='payrolla']/p/i")
    driver.execute_script("arguments[0].click();", payroll)

    run_payroll = driver.find_element(by="xpath", value="//*[@id='payrollmodule']/ul/li[2]/a/p")
    driver.execute_script("arguments[0].click();", run_payroll)

    time.sleep(2)
    add_new = driver.find_element(by="xpath", value="//*[@id='createNewRunPayrollButton']")
    driver.execute_script("arguments[0].click();", add_new)

    multiple = driver.find_element(by="xpath", value="//*[@id='MultipleTab']")
    driver.execute_script("arguments[0].click();", multiple)

    time.sleep(5)

    yearInput = driver.find_element(by="xpath", value="/html/body/div[1]/div[2]/main/div/div/div[1]/div/div/div[2]/div[1]/input").send_keys(year)

    action = ActionChains(driver)
    action.key_down(Keys.ARROW_RIGHT).perform()

    monthInput = driver.find_element(by="xpath", value="/html/body/div[1]/div[2]/main/div/div/div[1]/div/div/div[2]/div[1]/input").send_keys(month)

    action = ActionChains(driver)
    action.key_down(Keys.ARROW_RIGHT).perform()

    dateInput = driver.find_element(by="xpath", value="/html/body/div[1]/div[2]/main/div/div/div[1]/div/div/div[2]/div[1]/input").send_keys(date)

    print(year, month, date)

    # no_of_items = driver.find_element(by="xpath",value="//*[@id='show']")
    # no_of_items.click()
    # drop = Select(no_of_items)
    time.sleep(5)
    name_hours_list = []
    for employee_name, hours_or_salary in employee_details:
        name_hours_list.append((employee_name, hours_or_salary))
    time.sleep(5)
    # name_hours_list = [("Lil Wayne", 30), ("BC Payroll Biweekly", 3840), ("BC Payroll Semimonthly", 45)]
    emp_name = driver.find_elements(by="xpath", value="//*[@id='emp_name']/p[1]")
    hours_inputs = driver.find_elements(by="xpath", value="//*[@id='gross_income']/input")
    delete_buttons = driver.find_elements(by="xpath", value="//*[@id='delete_button']")

    display_names_list = []
    matched_names_list = []
    for i, element in enumerate(emp_name):
        matching_element = None
        first_name = element.text.split()[0]
        for index, (name, hours) in enumerate(name_hours_list):
            if first_name == name:
                matching_element = first_name
                matched_names_list.append((element.text, hours))
                print(matched_names_list)
                break
        if matching_element is None:
            display_names_list.append(element.text)

    for name in display_names_list:
        driver.find_element(by="xpath", value="//p[.='" + str(
            name) + "']/../following-sibling::td/button").click()
        for full_name, hours in matched_names_list:
            employee = driver.find_element(by="xpath", value="//p[text()='" + str(
                full_name) + "']/../following-sibling::td/input")
            employee.clear()
            employee.send_keys(str(hours))

    create = driver.find_element(by="xpath", value="//*[@id='createRunPayroll']")
    driver.execute_script("arguments[0].click();", create)
    print(123321)
    time.sleep(5)
    alert = Alert(driver)
    alert.accept()
    return driver

def quit_driver(driver):
    driver.quit()




