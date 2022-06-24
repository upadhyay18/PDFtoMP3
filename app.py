from lib2to3.pytree import convert
from flask import Flask,render_template,request
import sys
import os
sys.path.append("C:\\Users\Dell\\anaconda3\lib\site-packages")
import os
from tika import parser 
from gtts import gTTS
import smtplib
app=Flask(__name__)
PATH=os.path.join(os.getcwd(),"static")
app.config['UPLOAD_FOLDER']=PATH

def parseTextData(filePath):
    rawData = parser.from_file(filePath)
    rawData=rawData['content']
    mainData=rawData.replace('\n',' ')
    return mainData

def convertToMP3(data,speed,accent):
    filePath=os.path.join(PATH,"tempMusic/temp.mp3",)
    tts=gTTS(data,slow=speed,lang=accent)
    tts.save(filePath)
    return filePath
def sendMail(filePath,email):
    message="Enjoy your Book\n"
    message+=filePath
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login("sangrah170@gmail.com","Sangrah@op#")
    s.sendmail("sangrah170@gmail.com",email,message)
    s.quit()
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        speed=request.form['Speed']
        accent = request.form['lang']
        bookName = request.files['filename']
        email=request.form['mail']
        filePath=""
        if bookName.filename:
            filePath=os.path.join(PATH,"tempFile",bookName.filename)
            bookName.save(filePath)
            message='submitted'
        else:
            message = 'No file was uploaded'
        #working with raw data 
        if(filePath!=""):
            data=parseTextData(filePath)
            filePath=convertToMP3(data,speed,accent)
        else:
            return render_template("error.html",message)
        if email!="" and filePath !="":
            sendMail(filePath,email)
        return render_template('result.html')
    return  render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)