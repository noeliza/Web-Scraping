#%% load required packages
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

    
#%% scraped all Inquirer News Headlines under latest stories
website = 'https://newsinfo.inquirer.net/category/latest-stories'
driver = driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(website)

def get_headlines():
    soup = BeautifulSoup(driver.page_source, features = 'html.parser') #fetch page content
    headlines = []
    for h2 in soup.find_all('h2'):
        for a in h2.find_all('a'):
            headline = str.strip(a.text)
            headlines.append(headline)
    return headlines


try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[12]/div/div[2]/button'))).click()
except:
    print('No Cookies to Accept')

i = 1
headlines = []
while True:
    try:
        #wait for 20 seconds for next button to appear
        if i == 1:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ch-more-news"]/a'))).click()
        else:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ch-more-news"]/a[2]'))).click()            
      
        headlines += get_headlines()
        i = i + 1
        if i % 10 == 0:
            print('Loading more news headlines -- page %s' % i)
    except TimeoutException:
        break


with open('./Scraped Data/Inquirer_News_Headlines.txt', 'w', encoding="utf-8") as file:
    file.write('\n'.join(headlines))