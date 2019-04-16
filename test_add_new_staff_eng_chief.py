import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os
import time
import warnings
from dotenv import load_dotenv

load_dotenv()
from pathlib import Path

env_path = '.env'
load_dotenv(dotenv_path=env_path)


@pytest.mark.usefixtures("setup")
class TestAddNewStaffEngChief:
	def test_access_web(self):
		driver = self.driver
		assert "BAMMS :: Building & Apartment Mobile Management System" in driver.title
	
	def test_login_staging_1pr(self):
		print("Verify login account")
		driver = self.driver
		driver.find_element_by_id("username").click()
		driver.find_element_by_id("username").clear()
		EMAIL = self.email
		PASSWORD = self.password
		driver.find_element_by_id("username").send_keys(EMAIL)
		driver.find_element_by_id("password").send_keys(PASSWORD)
		driver.find_element_by_xpath(
			"(.//*[normalize-space(text()) and normalize-space(.)='remove_red_eye'])[1]/following::button[1]").click()
		
		driver.implicitly_wait(10)
		
		dashboard_title = driver.find_element_by_xpath("(.//*[@id='app']/div[3]/div/div[1]/div[1]/h1)")
		
		assert dashboard_title.text == 'Dashboard'
	
	def test_access_list_stafff_page(self):
		driver = self.driver
		URL = self.url
		driver.get(URL+"/#!/staff")
		WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//div[@class='title-bar-user-title']")))
	
	def test_add_new_staff(self):
		driver = self.driver
		
		driver.find_element(By.XPATH,
		                    "//div[contains(@class,'col-md-12 vuetable-wrapper-top')]//div[contains(@class,'vuetable-wrapper')]//a[2]").click()
		
		WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//h1[contains(@class,'title-bar-title')]")))
		
		driver.find_element(By.ID, "fullname").send_keys("Eng Chief")
		driver.find_element(By.ID, "via").click()
		Select(driver.find_element(By.ID, "via")).select_by_visible_text("Male")
		driver.find_element(By.XPATH, "//input[contains(@placeholder,'Date Of Birth')]").send_keys("20/03/2019")
		driver.find_element(By.ID, "fullname").click()		
		driver.find_element(By.ID, "email").send_keys(os.getenv("ENG_CHIEF"))
		driver.find_element(By.ID, "password").send_keys(os.getenv("PASSWORD"))
		driver.find_element(By.ID, "phone").send_keys("089899778787")
		driver.find_element(By.ID, "id").send_keys("1211212121")
		driver.find_element(By.ID, "department").click()
		Select(driver.find_element(By.ID, "department")).select_by_visible_text("Engineering")
		driver.find_element(By.XPATH, "//*[@id='app']/div[3]/div/div[1]/div[2]/form/div[9]/div/select").click()
		Select(driver.find_element(By.XPATH,
		                           "//*[@id='app']/div[3]/div/div[1]/div[2]/form/div[9]/div/select")).select_by_visible_text(
			"Chief")
		driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()
		
		notification = driver.find_element(By.XPATH, "//div[contains(@class,'toast-message')]")
		if notification.text == 'The email has already been taken.':
			print("Email already been taken")
		
		else:
			print("Success to add new staff")
		
		time.sleep(3)
