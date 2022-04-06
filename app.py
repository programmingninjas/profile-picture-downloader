from flask import Flask,render_template,request
from selenium import webdriver
from urllib.request import urlopen,Request,urlretrieve 
from time import sleep
import os
import json
from PIL import Image

app = Flask(__name__)

options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches',['enable-logging'])
options.add_argument(r"user-data-dir={x}".format(x=os.getcwd()+'\\'+'user')) 

@app.route('/',methods=['GET','POST'])
def home():

    return render_template("home.html")

@app.route("/twitter", methods=["GET","POST"])
def twitter():

    if request.method == 'POST':
        
        username = request.form.get('username')  # access the data inside 

        driver  = webdriver.Chrome(options=options, executable_path=r'C:\Program Files (x86)\chromedriver.exe')  #add your own chromedriver path

        driver.get(f"https://twitter.com/{username}/photo")

        sleep(5)

        pfp = driver.find_element_by_class_name("css-9pa8cd")  #class of tag can change so keep it updated

        src = pfp.get_attribute('src')    #image source link

        urlretrieve(src, "profile_pic.jpeg")

        driver.quit()

        image = Image.open("profile_pic.jpeg")

        image.show()

    return render_template("home.html")

@app.route("/instagram", methods=["GET","POST"])
def instagram():
    
    if request.method == 'POST':
        username = request.form.get('username')  # access the data inside 

        driver  = webdriver.Chrome(options=options, executable_path=r'C:\Program Files (x86)\chromedriver.exe')

        driver.get(f"https://instagram.com/{username}")

        sleep(2)

        try:

            pfp = driver.find_element_by_class_name('be6sR')  # class for pvt

        except:                                                # if not found

            pfp = driver.find_element_by_class_name('_6q-tv')   # Must be open so class for open accounts

        src = pfp.get_attribute('src')    

        urlretrieve(src, "profile_pic.png")

        driver.quit()

        image = Image.open("profile_pic.png")

        image.show()

    return render_template("home.html")

@app.route("/github", methods=["GET","POST"])
def github():

    if request.method == 'POST':
        
        username = request.form.get('username')  # access the data inside 

        url = f"https://api.github.com/users/{username}"

        response = urlopen(Request(url,headers={"User-Agent":"Chrome/94.0.4606.81","Accept" : "application/json"}))

        decoded = response.read().decode("utf-8")

        data = json.loads(decoded)

        src = data["avatar_url"]

        urlretrieve(src, "profile_pic.jpeg")

        image = Image.open("profile_pic.jpeg")

        image.show()

    return render_template("home.html")

if __name__ == '__main__':

    app.run()
