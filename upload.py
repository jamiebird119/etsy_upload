from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from csv import DictReader

import time


def upload():
    # Insert path to web driver here
    driver = webdriver.Chrome(r"C:\Users\J\Documents\GitHub\product_upload\chromedriver.exe")
    driver.set_window_size(1200, 900)
    driver.get('https://www.etsy.com/')

    def click_login_button():
        try:
            # pop up sometimes intercepting click so this runs it again if this happens
            driver.find_element_by_class_name("select-signin").click()
        except ElementClickInterceptedException:
            driver.find_element_by_xpath("//*[@id='gdpr-single-choice-overlay']/div/div[2]/div[2]/button").click()
            click_login_button()

    def navigate_to_upload():
        # clicks shop manager
        driver.find_element_by_xpath("//*[@href='https://www.etsy.com/uk/your/shops/me/dashboard?ref=hdr-mcpa']").click()
        time.sleep(1)
        # clicks listing
        driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div[3]/div/div[1]/div[2]/ul/li[3]/a/div/div[2]/span").click()
        time.sleep(1)

    def upload_product(product):
        # clicks add listing
        driver.find_element_by_xpath("//*[@id='page-region']/div/div/div[1]/header/div[1]/div/div[3]/div/div/a").click()
        time.sleep(1)

        # Inserts product information to form.

        # splits filenames for images by the / and then for each follows function
        filenames = product["Image"].split("/")
        print(filenames)
        for filename in filenames:
            print(filename)
            # here goes file path for images folder
            path = r"C:/Users/J/Documents/GitHub/product_upload/images/" + filename
            print(path)
            # click upload button
            print(driver.find_element_by_id("listing-edit-image-upload"))
            driver.find_element_by_id("listing-edit-image-upload").send_keys(path)
            # wait then add path to dialogue and click enter
            time.sleep(0.5)
        time.sleep(1)
        # Attach Title
        driver.find_element_by_id('title').send_keys(product["Title"])
        # Fill in 'Who made me'
        select = Select(driver.find_element_by_id("who_made"))
        select.select_by_visible_text('I did')
        # Fill in 'What is it'
        select = Select(driver.find_element_by_id("is_supply"))
        select.select_by_visible_text('A finished product')
        # Fill in 'When made'
        select = Select(driver.find_element_by_id("when_made"))
        select.select_by_visible_text('Made to order')
        # Fill in 'Category'
        driver.find_element_by_id("taxonomy-search").send_keys(product["Category"])
        time.sleep(2)
        driver.find_element_by_id("taxonomy-search").send_keys(Keys.RETURN)
        time.sleep(1.5)

        # Handle DEFAULT information currently the same for all products unless field in csv file
        # Room
        checkbox_values = driver.find_elements_by_css_selector(".select-multi-checkbox")
        checkbox_array = {}

        # Finds the available checkbox - label combinations and puts into a dict
        for box in checkbox_values:
            text_value = box.find_element_by_css_selector("input[type='checkbox']").get_attribute('value')
            id_value = box.find_element_by_css_selector("span[class='checkbox-label']").text
            checkbox_array[id_value] = text_value

        if 'Room' in product.keys():
            checkboxes = product['room'].split("/")
        else:
            checkboxes = ['Bedroom', 'Entryway', 'Office', 'Living room', 'Kitchen & dining']
        for box in checkboxes:
            try:
                # Searches dict for room value, finds and clicks
                print(checkbox_array[box])
                element = driver.find_element_by_xpath(f'//input[@value="{checkbox_array[box]}"]')
                driver.execute_script("arguments[0].click();", element)
            except Exception as err:
                print(err)

        # Subject
        if 'Subject' in product.keys():
            subject_boxes = product['Subject'].split("/")
        else:
            subject_boxes = ['Animal', 'Plants and trees']
        for box in subject_boxes:
            try:
                element = driver.find_element_by_xpath(f'//input[@value="{subject_boxes[box]}"]')
                driver.execute_script("arguments[0].click();", element)
            except Exception as err:
                print(err)

        # Framing
        try:
            unframed = driver.find_element_by_xpath("//span[@class='radio-label' and contains(text(), 'Unframed')]")
            driver.execute_script("arguments[0].click();", unframed)
        # If framed comment out above and uncomment
            # framed = driver.find_element_by_xpath("//span[@class='radio-label' and contains(text(), 'Framed')")
            # driver.execute_script("arguments[0].click();", framed)
        except Exception as err:
            print(err)

        # Fill in Description
        driver.find_element_by_id("description-text-area-input").send_keys(product["Description"])

        # Handle Tags
        tags = ["poster", "art", "artwork", "art print", "print", "paper", "retro", "archive", "vintage"]
        additional_tags = product["Tags"].split("/")
        for tag in additional_tags:
            tags.append(tag)
        for tag in tags:
            driver.find_element_by_id("tags").send_keys(tag)
            driver.find_element_by_id("tags").send_keys(Keys.RETURN)


        # Quantity and SKU
        driver.find_element_by_id("quantity_retail-input").send_keys(product["Quantity"])
        driver.find_element_by_id("SKU-input").send_keys(product["SKU"])

        # Sizes/ Prices
        element = driver.find_element_by_id("add_variations_button")
        driver.execute_script("arguments[0].click();", element)

        time.sleep(1)
        select = Select(driver.find_element_by_xpath('//select[@name="variation_property"]'))
        select.select_by_visible_text('Size')
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[@id='wt-modal-container']/div[3]/div/div/div[2]/div[1]/div[1]/div[3]/div[1]/label/span").click()
        time.sleep(0.5)
        select = Select(driver.find_element_by_xpath('//*[@id="wt-modal-container"]/div[3]/div/div/div[2]/div[1]/div[1]/div[2]/label/select'))
        select.select_by_visible_text('Centimeters')
        price_info = []
        size_info = []
        with open('prices.csv', 'r') as read_obj:
            # pass the file object to DictReader() to get the DictReader object
            csv_dict_reader = DictReader(read_obj)
            for row in csv_dict_reader:
                price_info.append(row["Price"])
                size_info.append(row["Size"])
        for size in size_info:
            driver.find_element_by_id("undefined-input").send_keys(size)
            driver.find_element_by_id("undefined-input").send_keys(Keys.RETURN)
        driver.find_element_by_xpath('//*[@id="wt-modal-container"]/div[3]/div/div/div[3]/div[2]/button').click()
        time.sleep(1)
        element = 1
        while element < len(price_info)+1:
            input_element = driver.find_element_by_xpath("//input[@name='price-input'][@value='0']")
            input_element.clear()
            input_element.send_keys(price_info[int(element-1)])
            input_element.send_keys(Keys.RETURN)
            id_string = input_element.get_attribute("id")
            id_number = id_string.split("_")[1]
            try:
                checkbox_element = driver.find_element_by_xpath(f"//input[@name='{id_number}-select-bulk-edit']")
                driver.execute_script("arguments[0].click();", checkbox_element)
                element += 1
                driver.find_element_by_xpath(
                    "//*[@id='page-region']/div/div/div[2]/div/div/div/div[7]/div/div/div/div[3]/div[2]/div[2]/div[1]/div/div[2]/div/button").click()
                time.sleep(1)
                driver.find_element_by_xpath("//button[text()='Save and continue']").click()
            except Exception as err:
                print(err)
        # driver.find_element_by_xpath('//*[@id="page-region"]/div/div/div[2]/div/div/div/div[7]/div/div/div/div[3]/div[2]/div[2]/div[1]/div/div[1]/div/button').click()

        # Shipping
        checkbox = driver.find_element_by_xpath("//input[@name='source_shipping_profile']")
        driver.execute_script("arguments[0].click();", checkbox)
        print("Added product Successfully")
        time.sleep(2)

        driver.find_element_by_xpath('/html/body/div[3]/section/div/div[4]/div/div/div/div[3]/div/div[1]/div/div/div[2]/button[2]').click()
        time.sleep(5)

    def read_csv():
        product_info = []
        # open file in read mode
        with open('product_info.csv', 'r') as read_obj:
            # pass the file object to DictReader() to get the DictReader object
            csv_dict_reader = DictReader(read_obj)
            for row in csv_dict_reader:
                product_info.append(row)

        return product_info

    # Originally clicks log in button.
    click_login_button()

    try:
        # waits until login pop up shows or for 5 sec
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "join_neu_email_field")))

    except Exception as e:
        print(f"{e}: Could not find login inputs")

    else:
        # fill in log in details
        username_element = driver.find_element_by_id("join_neu_email_field")

        # Enter USERNAME HERE
        username = ""
        username_element.send_keys(username)

        time.sleep(1)
        password_element = driver.find_element_by_id("join_neu_password_field")

        # Enter PASSWORD
        password = ""
        password_element.send_keys(password)
        time.sleep(1)
        try:
            # click login button
            driver.find_element_by_xpath("//*[@id='join-neu-form']/div[1]/div/div[6]/div/button").click()
            time.sleep(2)

        except Exception as e:
            print(e)
    # Note that if a captcha appears the program will fail. This only happened after 40 or so repeated logins, but aware it is a possibility. Wait 24 hours if this is the case.
    navigate_to_upload()
    products = read_csv()
    for product in products:
        upload_product(product)

upload()








