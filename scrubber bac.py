import re
from lxml import etree
import pandas
import requests
import time
from pprint import pprint
from bs4 import BeautifulSoup
path = "http://static.bacalaureat.edu.ro/2022/rapoarte/B/rezultate/alfabetic/page_"

last_page = 1540

def get_trs(url):
    r = requests.get(url)
    page = BeautifulSoup(r.content, "lxml")
    table = page.find("table",{"class":"mainTable"})
    return table.find_all("tr")[2:]

with open("results_2022_bac.csv", "w", encoding="utf-8") as file_object:
    header = ["student_id, scoala, specializare, math, limba romana, medie\n"]
    file_object.writelines(header)
    for i in range(1,last_page+1):
        
        url = path + str(i) + ".html"
        print(i)

        time.sleep(0.2)
        while True:
            try:
                trs = get_trs(url)
                break
            except:
                time.sleep(1)
                print("retrying")
    
        lines = []
        student_id = ""
        scoala = ""
        specializare = ""
        nota_mate = ""
        nota_romana = ""
        linecount = 0
        for tr in trs:
            linecount += 1
            tds = tr.find_all("td")
            #if i is even
            if linecount % 2 == 1:
                student_id = "tds[1].get_text()"
                
                scoala = tds[4].get_text()
                specializare = tds[7].get_text()
                nota_romana = tds[11].get_text()
            else: 
                nota_mate = tds[6].get_text()
                
                if nota_romana in ("-", "Absent") or nota_mate in ("-", "Absent"):
                    continue
                medie = (float(nota_mate) + float(nota_romana))/2
                lines.append(f'{student_id}, {scoala}, {specializare}, {nota_mate}, {nota_romana}, {round(medie, 2)}' + '\n')
        file_object.writelines(lines)