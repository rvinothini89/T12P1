import pytest
from selenium.common import TimeoutException
from TestData.HRMLogin_Data import HRMLoginData
from Utilities.ExcelFunction import excelFunction


class Test_HRMLogin:
    """
    Class to test OrangeHRM login functionalities using pytest.
    The driver is initialized per class using a fixture in conftest.py to avoid multiple instantiations.
    """

    @pytest.fixture(autouse=True)
    # Fixture to initialize the OrangeHRMHeader object and data readers
    def setup_class(self, driver):
        self.driver = driver
        """
        Initializes the OrangeHRMHeader object and data readers for each test case.
        Uses pytest's type keyword to create class-level instances to avoid initialization issues.
        """
        self.obj1 = HRMLoginData(HRMLoginData.url, driver)
        self.obj1.WebPageAccess()
        self.eobj1 = excelFunction(HRMLoginData.excel_file, HRMLoginData.sheet_number)

# using pytest parametrize to execute same test with different parameters. Here its trying with different credentials
    @pytest.mark.parametrize("username,password,row", HRMLoginData.read_login_data())
    def test_login(self, username, password, row):
        try:
            # Read expected error text and success URL
            expected_error_text = self.obj1.error_text
            expected_success_url = self.obj1.dashboard_url

            # Perform login and capture the result
            result = self.obj1.login(username, password)

            # Check the status of the result
            if result['status'] == "success":
                # Assert that the URL matches the dashboard url post login
                assert result[
                           'url'] == expected_success_url, f"Expected success URL does not match. Got {result['url']}"
                print(f"Successfully logged in using {username}")
                self.eobj1.write_data(row, 8, HRMLoginData.pass_data)

            elif result['status'] == "failure":
                # Assert that the error text matches the expected error text
                assert result[
                           'error_message'] == expected_error_text, f"Expected error text does not match. Got {result['error_message']}"
                print(f"Login failed as expected with error: {result['error_message']}")
                self.eobj1.write_data(row, 8, HRMLoginData.fail_data, result['error_message'])

            else:
                # Handle unexpected result
                raise AssertionError(f"Unexpected result: {result}")

        except AssertionError as e:
            # Handle assertion failure (unexpected result)
            print(f"AssertionError occurred: {e}")
            self.eobj1.write_data(row, 8, HRMLoginData.fail_data, str(e))

        except TimeoutException as e:
            # Handle timeout exceptions specifically
            print(f"TimeoutException occurred: {e}")
            self.eobj1.write_data(row, 8, HRMLoginData.fail_data, str(e))

        except Exception as e:
            # Handle any other unexpected exceptions
            print(f"Unexpected error occurred: {e}")
            self.eobj1.write_data(row, 8, HRMLoginData.fail_data, str(e))