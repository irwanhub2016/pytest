import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
env_path = '.env'
load_dotenv(dotenv_path=env_path)

@pytest.fixture(scope="session")
def setup(request):
    print("initiating chrome driver")
    # options = webdriver.ChromeOptions()
    # options.add_argument("--incognito")
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.headless = True
    # driver = webdriver.Chrome(chrome_options=options)
    
    driver = webdriver.Chrome()
    url = os.getenv("URL_Lavie")
    email = os.getenv("EMAIL")
    password = 'superadmin'
    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "driver", driver)
        setattr(cls.obj, "url", url)
        setattr(cls.obj, "email", email)
        setattr(cls.obj, "password", password)
    driver.get(url)
    #driver.maximize_window()

    yield driver
    driver.close()

