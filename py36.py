import re
import requests
import csv
import telebot
import time
GROUP_ID=-1001383125195
TOKEN=""
bot = telebot.TeleBot(TOKEN)

url='http://rangefinder.ru/glr/showtopgallery.php'
r=requests.get(url)
pat='<td[ ]align="center"[ ]class="medium">.+?<a href.+?>(.+?)</a>.+?Пользователь.+?href=.+?>(.+?)</a>.+?href="(.+?)".+?</a>'
pat2='<img.+?src="(http://rangefinder.ru/glr/data/\d+/.+?)"'
GalleryList=re.findall(pat,r.text,re.DOTALL)

with open('current36.csv', newline='') as csvfile:
    old36 = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
print(old36[0])

with open('current36.csv', 'w',newline='') as f: 
    write = csv.writer(f)
    write.writerow([x[2] for x in GalleryList])
print(len(GalleryList))


for r in GalleryList:
    print(r[0],r[1],r[2])
    if r[2] not in old36[0]:
        print(r[2])
        req=requests.get(r[2])
        ResUrl=[x for x in re.findall(pat2,req.text) if "thumb" not in x]
        print(ResUrl)
        #bot.send_message(GROUP_ID,'\r\n'.join([r[0]+" ("+ResUrl[0]+")",r[1]]))
        medias=[telebot.types.InputMediaPhoto(x,'\r\n'.join(r))for x in ResUrl]
        bot.send_media_group(GROUP_ID,medias)
        time.sleep(3)

