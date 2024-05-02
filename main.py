import json
import logging
import os
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Set up the Chrome driver (you need to download the ChromeDriver executable)
options = Options()

# options.add_argument("--headless")
options.add_argument("--disable-logging")


# Start the ChromeDriver service
service = Service()
# Create a new Chrome browser session
driver = webdriver.Chrome(service=service, options=options)
# Open the login page
driver.get('https://rexel.it/login')


# # Dismiss the cookie consent dialog by clicking on the "Accept" button
# accept_button = driver.find_element("id", "CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll")
# accept_button.click()


# Find the username and password input fields and enter your credentials
username_field = driver.find_element('id', 'MainContent_wucLoginBoxes_UserName')
username_field.send_keys('')

password_field = driver.find_element('id', 'MainContent_wucLoginBoxes_Password')
password_field.send_keys('')

# Submit the login form
login_button = driver.find_element('id', 'lbLogin')
login_button.click()

# Wait for the login process to complete (you may need to adjust the delay depending on the website)
driver.implicitly_wait(5)  # Wait for 5 seconds

no_of_pages = 13977
count = 2
# Navigate to the desired page
driver.get(f'https://rexel.it/prodotti?search=&page=1')


# Wait for the page to load after scrolling (you may need to adjust the delay depending on the website)
sleep(6)  # Wait for 10 seconds

# Get the page source after scrolling
page_source = driver.page_source

# Create a BeautifulSoup object from the page source
soup = BeautifulSoup(page_source, 'html.parser')

# Find the desired elements using Beautiful Soup
products = soup.select('.col-product')

products_list = []

for product in products:
    # Extract product name
    name = product.select_one(".name-product").text.strip()
    
    # Extract product price
    # price = product.select_one('.price-span, .price-final').text.strip()
    
    # Extract product code
    code = product.select_one(".code").text.strip()

    offer = product.select_one(".alert")

    if offer is not None:
        offer = offer.text.strip()
        if 'Offerta limitata' in offer and 'A solo: € 0,00' not in offer:
            
            price = offer.split('\n')[2].replace('A solo: ','').strip()
            offer = 'Offerta limitata'
            # Create a dictionary for the product
            product_dict = {
                "Product Name": name,
                "Price": price.split('x')[0].rstrip(),
                "Code": code.split('Cod. Produttore')[0].strip(),
                # "Offer": offer
            }

            # Append the product dictionary to the list
            products_list.append(product_dict)
            # Process or store the extracted data as needed
            print(f"Product Name: {name}")
            print(f"Price: {price.split('x')[0].rstrip()}")
            print(f"{code.split('Cod. Produttore')[0].strip()}")
            # print(f"Offerta: {offer}")

            print("---")
        else: offer ='NA'

    
  

    

print(f'SUCCESSFULLY SCRAPED PAGE 1')    

while count < no_of_pages:
    driver.get(f'https://rexel.it/prodotti?search=&page={count}')


    # Wait for the page to load after scrolling (you may need to adjust the delay depending on the website)
    sleep(6)  # Wait for 10 seconds

    # Get the page source after scrolling
    page_source = driver.page_source

    # Create a BeautifulSoup object from the page source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the desired elements using Beautiful Soup
    products = soup.select('.col-product')



    for product in products:
        # Extract product name
        name = product.select_one(".name-product").text.strip()
        
        # Extract product price
        # price = product.select_one('.price-span, .price-final').text.strip()
        
        # Extract product code
        code = product.select_one(".code").text.strip()

        offer = product.select_one(".alert")

        if offer is not None:
            offer = offer.text.strip()
            if 'Offerta limitata' in offer and 'A solo: € 0,00' not in offer:
                
                price = offer.split('\n')[2].replace('A solo: ','').strip()
                offer = 'Offerta limitata'
                # Create a dictionary for the product
                product_dict = {
                    "Product Name": name,
                    "Price": price.split('x')[0].rstrip(),
                    "Code": code.split('Cod. Produttore')[0].strip(),
                    "Oùffer": offer
                }


                # Append the product dictionary to the list
                products_list.append(product_dict)

                # Process or store the extracted data as needed
                print(f"Product Name: {name}")
                print(f"Price: {price.split('x')[0].rstrip()}")
                print(f"{code.split('Cod. Produttore')[0].strip()}")
                # print(f"Offerta: {offer}")

                print("---")
            else: offer ='NA'

        
        
        
    
    if count%5 == 0: print(f'SUCCESSFULLY SCRAPED PAGE {count}')
    count+=1

# Save the products list as JSON
with open("products.json", "w") as json_file:
    json.dump(products_list, json_file)



# Close the browser session
driver.quit()
