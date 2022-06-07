#%% load required packages
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd   

    
#%% scrape all properties available for buying in Metro Manila
website = 'https://www.lamudi.com.ph/metro-manila/buy/'
driver = driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(website)

soup = BeautifulSoup(driver.page_source, features = 'html.parser')


listings = []
while True:
    try:
        # get all listing info
        listing_info = soup.find_all('div', class_ = 'ListingCell-AllInfo ListingUnit')
        
        for listing in listing_info:
            values = listing.attrs
            values.update({
                'title': listing.find('div', class_ = 'ListingCell-TitleWrapper').h2.text.strip(),
                'short_description': listing.find('div', class_ = 'ListingCell-shortDescription').text.strip(),
                'address':listing.find('span', class_ = 'ListingCell-KeyInfo-address-text').text.strip()
                })
            listings.append(values)
        
        # click for next
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[2]/div[2]/div[2]/div[70]/div/div[3]/div/a'))).click()

    except TimeoutException:
        break

    
df = pd.DataFrame(listings) #convert to data frame
df.to_csv('./Scraped Data/listings_available_to_buy_metro_manila.csv', index = False) # save as csv
