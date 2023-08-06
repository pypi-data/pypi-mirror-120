from data_scraper import *
import json
link1='http://coinmarketcap.com/currencies/bitcoin/'
link2='http://coinmarketcap.com/currencies/ethereum/'
response=scraper.train(link1,link2)
print(response["id"])
response=scraper.run(link1,id=response["id"])
#response=scraper.run(link1,id="2SRQX7B96MOUKY1")
print("response keys",response.keys())
with open ("data.json","w",encoding="utf-8") as d:
    d.write(json.dumps(response,sort_keys=False,indent=4))