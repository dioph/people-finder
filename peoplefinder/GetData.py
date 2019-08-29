import os
from time import sleep

from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def text(driver):
    header_xpath = '/html/body/div[1]/div/div/div[4]/div/header'
    while True:
        try:
            driver.find_element(By.XPATH, header_xpath).click()
        except ElementClickInterceptedException:
            continue
        else:
            break
    sleep(1)
    status_xpath = '/html/body/div[1]/div/div/div[2]/div[3]/span/div/span/div/div/div/div[4]/div[2]/div/div'
    number_xpath = '/html/body/div[1]/div/div/div[2]/div[3]/span/div/span/div/div/div/div[4]/div[3]/div/div'
    try:
        driver.find_element(By.XPATH, number_xpath)
    except NoSuchElementException:
        status = ''
    else:
        status = driver.find_element(By.XPATH, status_xpath).text
    return status


def screenshot(driver, savedir, phone):
    filename = os.path.join(savedir, phone + '.png')
    picbox_xpath = '/html/body/div[1]/div/div/div[2]/div[3]/span/div/span/div/div/div/div[1]/div[1]/div/img'
    pic_xpath = '/html/body/div[1]/div/span[3]/div/div/div[2]/div/div/div/div/img'
    try:
        driver.find_element(By.XPATH, picbox_xpath).click()
    except (NoSuchElementException, ElementNotInteractableException):
        filename = ''
    else:
        sleep(2)
        pic = driver.find_element(By.XPATH, pic_xpath)
        pic.screenshot(filename)
    return filename


def get_data(driver, phone, savedir):
    """Takes the photo and number of a given contact in WhatsApp
    """

    driver.get('https://web.whatsapp.com/send?phone={}'.format(phone))
    header_xpath = '/html/body/div[1]/div/div/div[4]/div/header'
    sleep(2.0)
    try:
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, header_xpath)))
    except TimeoutException:
        return None

    try:
        status = text(driver)
        filename = screenshot(driver, savedir, phone)
    except ElementClickInterceptedException:
        return None

    return filename, status
