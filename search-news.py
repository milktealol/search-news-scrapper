#import what we need
from requests_html import HTMLSession
session = HTMLSession()

#use session to get the page
#r = session.get('https://duckduckgo.com/?q=robert+downey+jr&atb=v314-1&iar=news&ia=news')
r = session.get('https://www.google.com/search?q=robert+downey+jr&sxsrf=ALiCzsYx3PgO2Q0fFe0Al_LplnUUVeU9uQ:1664606729446&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiylLKmt776AhW0R2wGHUh7AdUQ_AUoAnoECAIQBA&biw=1918&bih=943&dpr=1')

r.html.render(sleep=1, scrolldown=2)

#find all the articles by using inspect element and create blank list
#articles = r.html.find('result__body')
articles = r.html.find('a.WlydOe')
newslist = []

# Duck duck go
# Google
for item in articles:    
##    try:
##        newsitem = item.find('h2', first=True)
##        title = newsitem.text
##        link = newsitem.absolute_links
##        time = item.find('.result__timestamp', first=True).text
##        description = item.find('.result__snippet', first=True).text
##        newsarticle = {
##            'title': title,
##            'link': link,
##            'time': time,
##            'description' : description
##        }
##        newslist.append(newsarticle)
##    except:
##       pass

    try:
        newsitem = item.find('.mCBkyc.y355M.ynAwRc.MBeuO.nDgy9d', first=True)
        title = newsitem.text
        time = item.find('.OSrXXb', first=True).text
        description = item.find('.GI74Re', first=True).text
        newsarticle = {
            'title': title,
            'time': time,
            'description' : description
        }
        newslist.append(newsarticle)
    except:
       pass

#ends process
session.close()

#print the length of the list
print(newslist)
