from data_scraper import *
import json
link1='https://www.nykaa.com/personal-care/feminine-hygiene/sanitary-napkins/c/391?root=nav_4'
link2='http://www.nykaa.com/personal-care/face/facewash/c/1387?ptype=lst&id=1387&root=nav_3&dir=desc&order=popularity'
response=scraper.train(link1,link2)
print(response["id"])
response=scraper.run(link1,id=response["id"])
#response=scraper.run(link1,id="2SRQX7B96MOUKY1")
print("response keys",response.keys())
with open ("data.json","w",encoding="utf-8") as d:
    d.write(json.dumps(response,sort_keys=False,indent=4))