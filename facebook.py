import logging
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

logging.basicConfig(filename="out.log", level=logging.INFO, format="%(asctime)s - %(message)s", encoding="utf-8")

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service("D:/PyCharm/Projects/FacebookTest/chromedriver/chromedriver.exe") # за потреби змінити на своє розташування


def login_to_facebook(email, password):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.facebook.com/") # сервіс з яким працюємо

    try:
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys(email)

        password_input = driver.find_element(By.ID, "pass")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        logging.info("Успішно виконано вхід у Facebook.")
        time.sleep(5)  # Чекаємо, щоб сторінка завантажилася

        logging.info("Зупинено після введення логіну та паролю.")

        # Програма чекає, поки не введете '1'
        while True:
            user_input = input("Введіть '1' для продовження(у випадку якщо з'явилась капча, вирішити її): ")
            if user_input == "1":
                break

        return driver

    except Exception as e:
        logging.error(f"Помилка входу: {e}")
        driver.quit()


def extract_profile_picture_url(driver, profile_url):
    try:
        driver.get(profile_url)
        time.sleep(5)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        image_element = soup.find("image")

        if image_element:
            image_url = image_element.get("xlink:href")
            if image_url:
                logging.info(f"URL фото профілю: {image_url}")
                print(f"URL фото профілю: {image_url}")
                return image_url
            else:
                logging.error("Не вдалося знайти URL.")
                return None
        else:
            logging.error("Не вдалося знайти елемент <image> на сторінці.")
            return None

    except Exception as e:
        logging.error(f"Помилка при отриманні фото: {e}")
        return None


if __name__ == "__main__":
    email = input("Введіть email або номер телефону: ")
    password = input("Введіть пароль: ")

    driver = login_to_facebook(email, password)

    if driver:
        profile_url = "https://www.facebook.com/me"
        extract_profile_picture_url(driver, profile_url)

        # Закриваємо браузер
        driver.quit()
