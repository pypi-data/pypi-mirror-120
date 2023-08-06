Data Scraper is a library that extracts the data in a structured json format from any url given. 


![Data Scraper Explanation](https://firebasestorage.googleapis.com/v0/b/datakund-studio.appspot.com/o/Pypi%20data%20scraper.png?alt=media&token=e1e961db-6694-4823-82f6-b7fb41139075)

### Train Scraper
* Training the scraper requires urls of 2 pages as input.
* These pages should look similar but contain different data.
* Then it finds the pattern in the 2 pages & returns scraper id.
* This id can be used to fetch JSON data out of the other similar pages.
* Training may take 2-3 minutes but once trained ,then scraper runs fast

**link1:-** link from where you want to scrape data
**link2:-** similiar link to link1 (explained below)
**response:-** returns id and status, id will be used for runing scraper
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
Running the scraper requires 2 inputs .
First is the url which you want to scrape data from
Second is the 'id' of the scraper which was given in response of training
**Id:-** Id of the scraper fetched during training
**link3:-** specify link from where you want to extract data
**response:-** structured json data 
**Output Example:-** 
{
  "Search Results": [
    {
      "title": "datakund-scraper",
      "description": "Web scraper library"
    },
    {}
  ],
  "Other_Pages_Results": [
    {
      "page": 2,
      "page_link": "/page=2"
    }
  ]
}
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
* Then in backend algorithms are applied on them to save the data structure for those kind of pages.
* It learns from the links of the web pages given by you and builds a scraper.
* In the response you get ID of the scraper.
* That id can be used to run the scraper for the links simililiar to the above training links.

### How to train scraper?
For the training, we need two similiar links. 
Two similiar links means where data is different but the structure of page is same.
* **First Link:-** Link from where you want to scrape data.
* **Second Link:-** Similiar link to above, like next pages link, different search results

Let us see from examples, to understand second link.
* **Pypi search results:-** search results for different keywords, other pages links(page=1,page=2,...)
For example:-https://pypi.org/search/?q=firebase, https://pypi.org/search/?q=sql
https://pypi.org/search/?o=&q=datakund&page=2, https://pypi.org/search/?o=&q=datakund&page=3
* **Coin market cap of Bitcoin:-** another currency page(Etherum, Microbitcoin)
For example:- https://coinmarketcap.com/currencies/bitcoin/ https://coinmarketcap.com/currencies/microbitcoin/

### Examples
Below are some of the examples of links using which you can train autoscraper:-
1. Pypi packages scraper [https://pypi.org/search/?q=firebase](https://pypi.org/search/?q=firebase)  [https://pypi.org/search/?q=datakund](https://pypi.org/search/?q=datakund)
2. Wordpress theme scraper [https://wordpress.org/themes/search/green/](https://wordpress.org/themes/search/green/)   [https://wordpress.org/themes/search/red/](https://wordpress.org/themes/search/red/)
3. Cryptocurrency details scraper [https://coinmarketcap.com/](https://coinmarketcap.com/)  [https://coinmarketcap.com/?page=2](https://coinmarketcap.com/?page=2)
4. PlayStore app details scraper[https://play.google.com/store/apps/details?id=com.whatsapp](https://play.google.com/store/apps/details?id=com.whatsapp)   [https://play.google.com/store/apps/details?id=org.telegram.messenger](https://play.google.com/store/apps/details?id=org.telegram.messenger)

### Queries/ Feedback
If you have some queries or feedback please contact us at following links
[Telegram](https://t.me/datakund)
[Email](abhishek@datakund.com)