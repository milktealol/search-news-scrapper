#import what we need
from requests_html import HTMLSession
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

def newsscrap(choice):

    # Selection Choice Settings

    # Google
    if choice == 1:
        mainContainerDiv = 'a.WlydOe'
        articleContainerDiv = '.mCBkyc.y355M.ynAwRc.MBeuO.nDgy9d'
        articleTimeDiv = '.OSrXXb'
        descriptionDiv = '.GI74Re'

    elif choice == 2:
        mainContainerDiv = '.result__body'
        articleContainerDiv = 'h2'
        articleTimeDiv = '.result__timestamp'
        descriptionDiv = '.result__snippet'

    # list of individuals we are querying
    search_list = pd.read_csv("search-list.csv")

    session = HTMLSession()
    
    # Looping of search list
    for x in range(len(search_list.index)):
        #retrieve URL link for each individual
        r = session.get(search_list["URL"][x])

        if (r == '<Response [429]>'):
            print("Please scrap again later, response 429")
            print(search_list["URL"][x])
            break

        #Rendering of page
        r.html.render(sleep=1, scrolldown=2)

        articles = r.html.find(mainContainerDiv)

        #list of result
        newslist = []

        #number of pages to scrap
        numberOfPage = 1

        for i in range(numberOfPage):
            
            for item in articles:
                print(item)
                try:
                    newsitem = item.find(articleContainerDiv, first=True)
                    title = newsitem.text
                    articleTime = item.find(articleTimeDiv, first=True).text
                    description = item.find(descriptionDiv, first=True).text
                    newsarticle = {
                        'title': title,
                        'time': articleTime,
                        'description' : description
                    }
                    newslist.append(newsarticle)
                except:
                    print("error 2")
                    pass
            
            if choice == 1:
                try:
                    #Proceeding to next page
                    nextPage = r.html.find('.d6cvqb.BBwThe')[-1]
                    nextPageURL = nextPage.find('a', first=True).attrs['href']
                    nextPageURL = 'https://www.google.com' + nextPageURL
                    r = session.get(nextPageURL)

                    #Render and sleep to prevent ban
                    r.html.render(sleep=1, scrolldown=2)
                    articles = r.html.find('a.WlydOe')
                    time.sleep(2)
                except:
                    print("Error no next page for: ")
                    print(search_list["URL"][x])
                    print("---")
                    pass

        df = pd.DataFrame(newslist)
        df.to_csv(search_list["Name"][x]+'.csv')

    #ends process
    session.close()


def seln(searchEchoice):
    driver = webdriver.Chrome(executable_path='PATH HERE')

    if searchEchoice == 2:
        mainContainerDiv = '.result__body'
        articleContainerDiv = 'h2'
        articleTitleDiv = '.result__title'
        articleTimeDiv = '.result__timestamp'
        descriptionDiv = '.result__snippet'
        buttonMore = '.result--more__btn'
    
    elif searchEchoice == 3:
        mainContainerDiv = '.NewsArticle'
        articleTitleDiv = '.s-title a'
        articleTimeDiv = '.s-time'
        descriptionDiv = '.s-desc'
        buttonMore = '.compPagination a.next'

    search_list = pd.read_csv("search-list.csv")

    for x in range(len(search_list.index)):
        newslist = []
        articleCounter = 0
        driver.get(search_list["URL"][x])

        driver.implicitly_wait(3)

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)

        while articleCounter < 100:
            for result in driver.find_elements(By.CSS_SELECTOR, mainContainerDiv):
                title = result.find_element(By.CSS_SELECTOR, articleTitleDiv).text
                articleTime = result.find_element(By.CSS_SELECTOR, articleTimeDiv).text
                description = result.find_element(By.CSS_SELECTOR, descriptionDiv).text

                newsarticle = {
                    'title': title,
                    'time': articleTime,
                    'description' : description
                }

                newslist.append(newsarticle)

                articleCounter += 1
            
            try:
                if articleCounter < 100:
                    nextbtn = driver.find_element(By.CSS_SELECTOR, buttonMore);
                    nextbtn.click()
                    print("Next Page")
                    time.sleep(5);
                    driver.implicitly_wait(3)
            except:
                print("No next page")
                break

        print(search_list["URL"][x] + ' ended')
        df = pd.DataFrame(newslist)
        df.to_csv(search_list["Name"][x]+'.csv')

# Main Run
while True:
    try:
        print("1 - for Google News Search")
        print("2 - for Duck Duck Go News Search")
        print("3 - for Yahoo News Search")
        searchEchoice = int(input("Enter Choice: "))

        if searchEchoice == 1:
            newsscrap(searchEchoice)
            print("---------------")
            print("Scrapping done")
            break

        elif searchEchoice == 2:
            seln(searchEchoice)
            print("---------------")
            print("Scrapping done")
            break

        elif searchEchoice == 3:
            seln(searchEchoice)
            print("---------------")
            print("Scrapping done")
            break
        else:
            print("Invalid choice")

    except ValueError:
        print("Invalid choice")
