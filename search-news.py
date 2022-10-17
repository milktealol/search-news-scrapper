#import what we need
from requests_html import HTMLSession
import time
import pandas as pd


# list of individuals we are querying
search_list = pd.read_csv("search-list.csv")

#Google
session = HTMLSession()

for x in range(len(search_list.index)):

    #use session to get the page
    #Duckduckgo
    #r = session.get('https://duckduckgo.com/?q=robert+downey+jr&atb=v314-1&iar=news&ia=news')

    #retrieve URL link for each individual
    r = session.get(search_list["URL"][x])

    #Rendering of page
    r.html.render(sleep=1, scrolldown=2)

    articles = r.html.find('a.WlydOe')

    #list of result
    newslist = []

    #number of pages to scrap
    numberOfPage = 5

    for i in range(numberOfPage):
        
        for item in articles:
        ##    #Duck duck go
        ##    try:
        ##        newsitem = item.find('h2', first=True)
        ##        title = newsitem.text
        ##        link = newsitem.absolute_links
        ##        articleTime = item.find('.result__timestamp', first=True).text
        ##        description = item.find('.result__snippet', first=True).text
        ##        newsarticle = {
        ##            'title': title,
        ##            'link': link,
        ##            'time': articleTime,
        ##            'description' : description
        ##        }
        ##        newslist.append(newsarticle)
        ##    except:
        ##       pass
            
            # Google
            try:
                newsitem = item.find('.mCBkyc.y355M.ynAwRc.MBeuO.nDgy9d', first=True)
                title = newsitem.text
                articleTime = item.find('.OSrXXb', first=True).text
                description = item.find('.GI74Re', first=True).text
                newsarticle = {
                    'title': title,
                    'time': articleTime,
                    'description' : description
                }
                newslist.append(newsarticle)
            except:
                pass

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
            print("error")
            print(search_list["URL"][x])
            print("---")
            pass

    df = pd.DataFrame(newslist)
    df.to_csv(search_list["Name"][x]+'.csv')

#ends process
session.close()
