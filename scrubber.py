import re
from lxml import etree
import pandas
import requests
import time
from pprint import pprint
from bs4 import BeautifulSoup
path = "http://evaluare.edu.ro/Evaluare/CandFromJudIAD.aspx?Jud=24&Poz=0&PageN="

last_page = 807

def get_trs(url):
    r = requests.get(url)
    page = BeautifulSoup(r.content, "lxml")
    table = page.find("table",{"class":"mainTable"})
    return table.find_all("tr")[2:]

with open("results_2023_ilfov.csv", "w", encoding="utf-8") as file_object:
    header = ["student_id, scoala, math, limba romana, limba materna, medie, media materna\n"]
    file_object.writelines(header)
    for i in range(1,last_page+1):
        
        url = path + str(i)
        print(i)

        time.sleep(1)
        while True:
            try:
                trs = get_trs(url)
                break
            except:
                time.sleep(1)
                print("retrying")
    
        lines = []
        for tr in trs:
            tds = tr.find_all("td")
            student_id = tds[1].get_text()
            
            scoala = tds[3].find("a").get_text()
            nota_mate = tds[4].get_text()
            nota_romana = tds[7].get_text()
            nota_materna = tds[13].get_text()
            if nota_romana in ("-", "Absent") or nota_mate in ("-", "Absent"):
                continue
            medie = (float(nota_mate) + float(nota_romana))/2
            if nota_materna not in ("-", "Absent"):
                medie_materna = (float(nota_mate) + float(nota_romana) + float(medie_materna))/3
            else:
                medie_materna = 0
            lines.append(f'{student_id}, {scoala}, {nota_mate}, {nota_romana}, {nota_materna}, {round(medie, 2)}, {round(medie_materna, 2)}' + '\n')
        file_object.writelines(lines)