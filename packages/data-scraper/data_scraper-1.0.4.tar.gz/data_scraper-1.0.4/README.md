With Data Scraper you can scrape any website without the need of inspecting web elements or parsing HTML using Beautiful Soup etc.  
With just links as input you get JSON data as output.  
First you need to train the scraper for particular website & then run it.

![Data Scraper Explanation](https://firebasestorage.googleapis.com/v0/b/datakund-studio.appspot.com/o/Pypi%20data%20scraper.png?alt=media&token=e1e961db-6694-4823-82f6-b7fb41139075)

### Train Scraper
```sh
from data_scraper import *
link1='https://pypi.org/search/?q=request'
link2='https://pypi.org/search/?q=datakund'
response=scraper.train(link1,link2)
print(response)
#{'id':'QJP4LW2EBTQM45N',success:true}
open('PyPi Scraper.txt', 'w').write(response['id'])
```

### Run Scraper
```sh
from data_scraper import *
Id=open('PyPi Scraper.txt', 'r').read()
#This is id of scraper we got in training above
link3='https://pypi.org/search/?q=scraper'
response=scraper.run(link3,id=Id)
with open('./data.json','w') as data:
	data.write(json.dumps(response,indent=4))
```

### How it works?
* It takes two similiar links to train the scraper.
* It learns from the links of the web pages given by you and builds a scraper.
* In the response you get ID of the scraper.
* That ID can be used to run the scraper for the links simililiar to the above training links.


### Examples
Below are some of the examples of links using which you can train the scraper:-
1. Pypi packages scraper [https://pypi.org/search/?q=firebase](https://pypi.org/search/?q=firebase)  [https://pypi.org/search/?q=datakund](https://pypi.org/search/?q=datakund)
2. Wordpress theme scraper [https://wordpress.org/themes/search/green/](https://wordpress.org/themes/search/green/)   [https://wordpress.org/themes/search/red/](https://wordpress.org/themes/search/red/)
3. Cryptocurrency details scraper [https://coinmarketcap.com/](https://coinmarketcap.com/)  [https://coinmarketcap.com/?page=2](https://coinmarketcap.com/?page=2)
4. PlayStore app details scraper[https://play.google.com/store/apps/details?id=com.whatsapp](https://play.google.com/store/apps/details?id=com.whatsapp)   [https://play.google.com/store/apps/details?id=org.telegram.messenger](https://play.google.com/store/apps/details?id=org.telegram.messenger)

### Queries/ Feedback
If you have some queries or feedback please contact us at following links
[Telegram](https://t.me/datakund)
[Email](abhishek@datakund.com)