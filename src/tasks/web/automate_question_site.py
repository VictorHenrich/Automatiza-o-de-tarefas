from start import app
from server.cli import Task

from selenium.webdriver import Edge
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pathlib import Path
from time import sleep


@app.cli.add_task('teste')
class AutomateQuestionSite(Task):
    name = "automacao_joao"
    title = "Automação do João"

    path_exec: Path = Path() / '..' / 'drives' / 'msedgedriver.exe'

    access_url: str = "https://www.lifepointspanel.com/pt-br/member/dashboard"

    username: str = "joao_bernadino@hotmail.com"
    password: str = "Jhonesw2@"

    def perform_authentication(self, browser: WebDriver):
        id_input_user: str = "edit-contact-email"
        id_input_password: str = "edit-password"
        css_selector_submit: str = "a[class*='login-btn login_submit']"

        user_field = browser.find_element(By.ID, id_input_user)
        pass_fields = browser.find_element(By.ID, id_input_password)
        submit = browser.find_element(By.CSS_SELECTOR, css_selector_submit)

        user_field.send_keys(AutomateQuestionSite.username)
        pass_fields.send_keys(AutomateQuestionSite.password)

        submit.submit()

        sleep(5)

        

    def run(self) -> None:
        browser: WebDriver = Edge(AutomateQuestionSite.path_exec)

        browser.get(AutomateQuestionSite.access_url)

        self.perform_authentication(browser)
    