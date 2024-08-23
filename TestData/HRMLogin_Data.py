# Importing all required packages
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Importing class files from respective files
from TestLocators.HRMLogin_Locators import locators
from Utilities.ExcelFunction import excelFunction


class HRMLoginData:
    # Class to handle login operations with test data and interactions

    # config file which are needed for reading input and writing output using excel sheet
    excel_file = "D:\\VinoLEarning\\ T12Project\\TestData\\HRMLoginExcel.xlsx"
    sheet_number = "Sheet1"

    # Initialize data readers for Excel
    excel_obj = excelFunction(excel_file, sheet_number)

    # Read configuration and test data from YAML
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    dashboard_url = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
    error_text = "Invalid credentials"
    pass_data = "Test Passed"
    fail_data = "Test Failed"
    # Getting maximum row count for looping through the rows to read respective data
    row = excel_obj.row_count()

    def __init__(self, url, driver):
        """
        Initialize with URL and WebDriver instance.
        """
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 30)
        self.excel_obj = excelFunction(self.excel_file, self.sheet_number)

    @classmethod
    def read_login_data(cls):
        """
        Read login data for testing from the Excel file.
        Returns a list of tuples containing username, password, and row number.
        """
        data = []
        # login creds need to be fetched from excel sheet and it need to loop through each row
        for row in range(2, cls.row + 1):
            # column number 6 and 7 has username and password values in excel sheet respectively
            username = cls.excel_obj.read_data(row, 6)
            password = cls.excel_obj.read_data(row, 7)
            data.append((username, password, row))
        return data

    def WebPageAccess(self):
        """
        Access the specified URL and maximize the browser window.
        Returns the title of the current page.
        """
        try:
            self.driver.maximize_window()
            self.driver.get(self.url)
            return self.driver.title
        except TimeoutException as e:
            print(e)

    def login(self, username, password):
        """
        Perform login with provided username and password.
        Handles both successful and failed login attempts.
        """
        try:
            username_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_username)))
            username_element.send_keys(username)
            print(username)
            pswd_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_password)))
            pswd_element.send_keys(password)
            print(password)
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, locators.loc_login)))
            login_button.click()
            # Check for error message indicating a failed login
            # Checking if error message is found and if its not found validating current url to check if login is success
            try:
                error_message_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_error)))
                print(error_message_element.text)
                error_text = error_message_element.text
                return {"status": "failure", "error_message": error_text}
            except TimeoutException:
                current_url = self.driver.current_url
                return {"status": "success", "url": current_url}
        except TimeoutException as e:
            print(f"TimeoutException occurred: {e}")
            return False
        except NoSuchElementException as e:
            print(f"NoSuchElementException occurred: {e}")
            return False
