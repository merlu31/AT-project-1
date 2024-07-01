import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from pageObjects.LoginPage import LoginPage
from pageObjects.PIMPage import PIMPage


@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.close()
    driver.quit()


@pytest.mark.parametrize(("username", "password", "firstname", "middlename", "lastname"), [
    ("Admin", "admin123", "archana", "F", "merlin")
])
def test_add_employee(driver, username, password, firstname, middlename, lastname):
    login_page = LoginPage(driver)
    pim_page = PIMPage(driver)
    login_page.open_page("https://opensource-demo.orangehrmlive.com")

    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login_button()

    pim_page.click_pim_side_menu()
    pim_page.enter_employee_id_in_search("0295")
    pim_page.click_search_button()
    pim_page.click_edit_icon()
    pim_page.click_male_radio_button()
    pim_page.click_save_button()
    try:
        assert "pim" in driver.current_url.lower(), "Failed to add employee"
        print("Employee updated successfully")
    except AssertionError as e:
        error_message = pim_page.get_error_message()
        print(f"Error message: {error_message}")
        raise e
