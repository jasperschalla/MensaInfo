from bs4 import BeautifulSoup
import bs4
import requests
from datetime import date
import datetime
import json
from git import Repo

PATH_OF_GIT_REPO = '/home/pi/Documents/python/mymensa/.git'  
COMMIT_MESSAGE = 'Update mensa data from raspberry pi'

date_dict = {}

today = datetime.datetime.now()
monday = today - datetime.timedelta(days = today.weekday())
offset = datetime.timedelta(days=1)

for weekdays in range(7):
    temp = monday + offset * weekdays
    date_dict[temp.strftime("%Y-%m-%d")] = {"weekday":temp.strftime("%a").lower()}


rempi_link = "https://www.swfr.de/essen/mensen-cafes-speiseplaene/freiburg/mensa-rempartstrasse"
insti_link = "https://www.swfr.de/essen/mensen-cafes-speiseplaene/freiburg/mensa-institutsviertel"
litti_link = "https://www.swfr.de/essen/mensen-cafes-speiseplaene/freiburg/mensa-littenweiler"

req_rempi = requests.get(rempi_link)
req_insti = requests.get(insti_link)
req_litti = requests.get(litti_link)

rempi = BeautifulSoup(req_rempi.text, "html.parser")
insti = BeautifulSoup(req_insti.text, "html.parser")
litti = BeautifulSoup(req_litti.text, "html.parser")

div_id = "tabsWeekdaysMenu"

rempi_div = rempi.find("div", {"id": div_id})
insti_div = insti.find("div", {"id": div_id})
litti_div = litti.find("div", {"id": div_id})

results = {"rempartstraße":{

          },
          "institutsviertel": {

          },
          "littenweiler": {

          }}


for key,item in date_dict.items():

    results["rempartstraße"][key] = []
    results["institutsviertel"][key] = []
    results["littenweiler"][key] = []

    weekday = item["weekday"]


    try:
        rempi_day = rempi_div.find("div",{"id":f"tab-{weekday}"})
        rempi_food = rempi_day.find_all("div",{"class":"col-span-1"})

        for food in rempi_food:

            title = food.find("h5").getText()
            food_str = [str(i) for i in food.find("small").contents]
            food_clean = [i for i in food_str if not i=="<br/>"]
            price = food.find("dd").getText()
            food_type = food.find("img").attrs["src"].split("/")[-1].split(".")[0]

            if food_type=="plus-cyan":
                food_type = "meat"

            results["rempartstraße"][key].append({"title":title,"description":food_clean,"price":price,"type":food_type})
    except Exception:
        continue
    
    try:
        insti_day = insti_div.find("div",{"id":f"tab-{weekday}"})
        insti_food = insti_day.find_all("div",{"class":"col-span-1"})

        for food in insti_food:

            title = food.find("h5").getText()
            food_str = [str(i) for i in food.find("small").contents]
            food_clean = [i for i in food_str if not i=="<br/>"]
            price = food.find("dd").getText()
            food_type = food.find("img").attrs["src"].split("/")[-1].split(".")[0]

            if food_type=="plus-cyan":
                food_type = "meat"

            results["institutsviertel"][key].append({"title":title,"description":food_clean,"price":price,"type":food_type})
    except Exception:
        continue
    
    try: 
        litti_day = litti_div.find("div",{"id":f"tab-{weekday}"})
        litti_food = litti_day.find_all("div",{"class":"col-span-1"})

        for food in litti_food:

            title = food.find("h5").getText()
            food_str = [str(i) for i in food.find("small").contents]
            food_clean = [i for i in food_str if not i=="<br/>"]
            price = food.find("dd").getText()
            food_type = food.find("img").attrs["src"].split("/")[-1].split(".")[0]

            if food_type=="plus-cyan":
                food_type = "meat"

            results["littenweiler"][key].append({"title":title,"description":food_clean,"price":price,"type":food_type})
    except Exception:
        continue

with open("/home/pi/Documents/python/mymensa/mensa_info.json","w") as fp:
    json.dump(results,fp)


repo = Repo(PATH_OF_GIT_REPO)
repo.git.add(update=True)
repo.index.commit(COMMIT_MESSAGE)
origin = repo.remote(name='origin')
origin.push()




