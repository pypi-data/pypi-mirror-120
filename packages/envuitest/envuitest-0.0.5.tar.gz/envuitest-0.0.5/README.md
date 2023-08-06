# Salesforce Web Driver
Web Auto Test Framework with Selenium For Salesforce Lightning App

Function APIS:
- login: login Salesforce's Scratch Org
- open_url: open target url
- click_element: click element by visibility text
- set_value: set value to element by it's label or visibility text
- check_table_value: check table data by record data and row_index

Example:

```python

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome('/your path/chrome_driver/chromedriver', chrome_options=chrome_options)

login(driver, 'test@example.com', 'password')
open_url(driver, 'https://builder-playground-4380-dev-ed.lightning.force.com/lightning/n/PC_DivisionTab')
record = {'体系编号': 'DIV007'}
check_table_value(driver, record, False)
click_element(driver, '新建体系', '')
check_table_value(driver, record, True)

```