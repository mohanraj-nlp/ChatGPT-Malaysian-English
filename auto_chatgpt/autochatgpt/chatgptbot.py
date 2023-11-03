import os
import random
import time

import undetected_chromedriver as uc
from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from autochatgpt import login

# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait


class ChatGPTBot:
    OPENAI_URL = "https://chat.openai.com/"

    def __init__(self, EMAIL_ADDRESS, PASSWORD, headless=True, wait=60):
        self.implicitly_wait_time = wait
        self.driver = self.set_driver(headless, self.implicitly_wait_time)
        self.driver.get(ChatGPTBot.OPENAI_URL)
        self.login(EMAIL_ADDRESS, PASSWORD)

    def set_driver(self, headless, wait_time):
        options = uc.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        driver = uc.Chrome(options=options)
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')

        # wait for the page to load
        driver.implicitly_wait(wait_time)
        return driver

    def set_chat_history_and_training(self, check):
        # Open Data Controls settings window
        self.driver.find_element(By.XPATH, '//div[@class="group relative" and @data-headlessui-state=""]').click()
        self.driver.find_element(By.XPATH, '//a[contains(text(),"Settings")]').click()
        self.driver.find_element(By.XPATH, '//button[contains(., "Data controls")]').click()

        checked_value = self.driver.find_element(By.XPATH, "//button[@aria-checked]").get_attribute("aria-checked")
        checked_bool = True if checked_value == "true" else False

        if checked_bool != check:
            # click Chat History and Training Button
            self.driver.find_element(By.XPATH, '//button[contains(@role, "switch")]').click()

        # close settings window
        self.driver.find_element(By.XPATH, '//button[contains(@class, "inline-block")]').click()

    def get_driver(self):
        return self.driver

    def login(self, EMAIL_ADDRESS, PASSWORD):
        # login.bypassing_cloudflare(driver)
        login.click_login_button(self.driver)
        load_dotenv(verbose=True)
        ACCOUNT_TYPE = "GOOGLE"
        if ACCOUNT_TYPE == "OPENAI":
            login.login_openai(self.driver, email_address=EMAIL_ADDRESS, password=PASSWORD)
        elif ACCOUNT_TYPE == "GOOGLE":
            login.login_google_account(self.driver, email_address=EMAIL_ADDRESS, password=PASSWORD)
        else:
            raise ValueError("ACCOUNT_TYPE must be OPENAI or GOOGLE")
        # login.skip_start_message(self.driver)

    def set_gpt_model(self, model_version):
        if model_version not in ["GPT-3.5", "GPT-4"]:
            raise ValueError("model_version must be GPT-3.5 or GPT-4")
        self.driver.find_element(By.XPATH, f"//button[contains(., '{model_version}')]").click()

    def send_prompt(self, prompt):
        textarea = self.driver.find_element(By.CSS_SELECTOR, "textarea")
        textarea.clear()
        textarea.send_keys(prompt)
        time.sleep(random.uniform(1, 5))
        self.driver.find_element(By.CSS_SELECTOR, "button.absolute").click()

    def get_user_prompt(self):
        user_elements = self.driver.find_elements(
            By.XPATH,
            '//div[contains(@class, "group w-full text-gray-800 dark:text-gray-100 border-b border-black/10 dark:border-gray-900/50 dark:bg-gray-800")]',
        )
        return [user_element.text for user_element in user_elements]

    def get_gpt_response(self, timeout=60):
        # Temporarily disable implicit wait
        self.driver.implicitly_wait(0)

        try:
            # Check if the element that is being output exists
            WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "result-streaming")]'))
            )

            # If it exists, wait until the output is finished
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.XPATH, '//div[contains(@class, "result-streaming")]'))
            )
        except TimeoutException:
            # If the element doesn't exist, continue to get the text
            pass
        finally:
            # Re-enable implicit wait
            self.driver.implicitly_wait(self.implicitly_wait_time)

        # Get the element after the output is finished
        gpt_elements = self.driver.find_elements(
            By.XPATH,
            '//div[contains(@class, "markdown")]',
        )
        return [gpt_element.text for gpt_element in gpt_elements]

    def resume_conversation(self, chatid):
        resume_chat_page = ChatGPTBot.OPENAI_URL + f"/c/{chatid}"
        self.driver.get(resume_chat_page)
        time.sleep(1)
        if self.driver.current_url != resume_chat_page:
            raise ValueError("Unable to load conversation page. Check if the chatid is correct.")
