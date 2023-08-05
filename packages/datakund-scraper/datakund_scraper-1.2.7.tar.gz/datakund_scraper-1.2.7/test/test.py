from datakund_scraper import *
import json
link1='https://www.topuniversities.com/search/universities#q=engineering'
link2='https://www.topuniversities.com/search/universities#q=science'
response=scraper.train(link1,link2)
print(response["id"])
res=scraper.run(link1,id=response["id"])
#res=scraper.run(link1,id="2SRQX7B96MOUKY1")
print("response keys",res.keys())
with open ("data.json","w",encoding="utf-8") as d:
    d.write(json.dumps(res,sort_keys=False,indent=4))