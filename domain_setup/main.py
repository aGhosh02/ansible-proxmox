import json

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import argparse

PROXY_ADMIN_URL = "http://10.0.200.2:81"
PROXY_EMAIL = "arghyag5@gmail.com"
PROXY_PASS = "#Iamdevil1"

CLOUDFLARE_TUNNEL_URL = "https://one.dash.cloudflare.com/fa8f1f901b1ca07b29487dc6bed0a269/access/tunnels/63de5bac-15c9-4878-a01b-73bbee81f671?tab=publicHostname"
CLOUDFLARE_EMAIL = "arghyag5@gmail.com"
CLOUDFLARE_PASS = "#Iamdevil1"


def add_proxy(name, internal):
    ip, port = internal.split(':')

    options = Options()
    # options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
    driver.get(PROXY_ADMIN_URL)

    # Login
    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "identity"))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "secret"))
    )
    submit_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "btn-teal"))
    )

    email_field.send_keys(PROXY_EMAIL)
    password_field.send_keys(PROXY_PASS)
    submit_button.click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Proxy Hosts"))
    ).click()

    # Check if proxy exists
    try:
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '" + name + ".arghyaghosh.cloud')]")))
        return
    except:
        pass

    # Add Proxy
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Add Proxy Host"))
    ).click()

    domain_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "input-domains-selectized")))
    domain_input.send_keys(name + ".arghyaghosh.cloud")
    domain_input.send_keys(Keys.ENTER)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "forward_host"))
    ).send_keys(ip)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "forward_port"))
    ).send_keys(port)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "btn-teal"))
    ).click()


def main():
    # parser = argparse.ArgumentParser(description='Do all the things')
    # parser.add_argument('public', type=bool, help='Should add to cloudflare?')
    # parser.add_argument('internal', type=str, help='internal address')
    # parser.add_argument('name', type=str, help='app name')
    # args = parser.parse_args()
    with open('config.json') as user_file:
        file_contents = user_file.read()
    parsed_json = json.loads(file_contents)
    for item in parsed_json:
        print(item)
        add_proxy(item['name'], item['internal'])
    # add_proxy(args.name, args.internal)


if __name__ == "__main__":
    main()
