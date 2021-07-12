#!/usr/bin/env python
# coding: utf-8

# In[75]:


import os
import PIL.Image
from datetime import datetime
import json
from datetime import date
import smtplib
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import random    
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

miesiac_dzis = date.today().strftime("%m")
dzien_dzis =  date.today().strftime("%d")

def wysylka_email(zdjecia):
    mail_content = 'Hej, \n \nOto zdjęcia z przeszłości, które umilą Ci dzień.'
    sender_address = 'adresc@gmail.com'
    sender_pass = 'haslo'
    receiver_address = 'receiver@gmail.com'

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Wspominacz zdjęć'   #The subject line
    message.attach(MIMEText(mail_content, 'plain'))

    fixed_height = 400

    for zdjecie in zdjecia:
        image = Image.open(zdjecie)
        height_percent = (fixed_height / float(image.size[1]))
        width_size = int((float(image.size[0]) * float(height_percent)))
        image = image.resize((width_size, fixed_height), Image.BILINEAR)

        draw = ImageDraw.Draw(image)
        draw.text((0, 380),f'{dictionary[zdjecie][:10]}',(255,255,255))
        draw.text((0, 370),f'{dictionary[zdjecie][:10]}',(0,0,0))

        image.save(f'{zdjecie.split("/")[-1]}', "JPEG", quality=70, optimize=True, progressive=True)
        fp = open(f'{zdjecie.split("/")[-1]}', 'rb')
        imageData = MIMEImage(fp.read(), 'jpg') 
        imageData.add_header('Content-Disposition', f'attachment; filename={zdjecie.split("/")[-1]}')
        message.attach(imageData)

        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        image.close()
        print('Mail Sent')
    for zdjecie in zdjecia:
        os.remove(f'{zdjecie.split("/")[-1]}')

                
logi = open("logi.txt", "r").readlines()
dni = [(i.replace("\n", "")).replace(" ","") for i in logi]
if date.today().strftime("%Y-%m-%d") not in dni:
    pliki = open("slownik_zdjec.json", "r").read()
    dictionary = json.loads(pliki)
    zdjecia = [v for v,k in dictionary.items() if k[5:7]==miesiac_dzis and k[8:10]==dzien_dzis]
    if len(zdjecia)>0:
        print("Zidentyfikowano ", len(zdjecia), "zdjęć")
        if len(zdjecia)>10:
            zdjecia = random.sample(zdjecia, 10)
        wysylka_email(zdjecia)     
    else:
        print("Nie zidentyfikowano zdjęć.")
                  
    with open("logi.txt", "a") as myfile:
        dopis = f'\n{date.today().strftime("%Y-%m-%d")}'
        myfile.write(dopis)
    print("Dopisano dzień")

