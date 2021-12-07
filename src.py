#!C:\Users\Dell\anaconda3\pkgs\python-3.8.3-he1778fa_2/python.exe
#seting up enviroment----------------------------------------
import cgi, cgitb
import sys
import os
sys.path.append("C:\\Users\Dell\\anaconda3\lib\site-packages")
from tika import parser 
from gtts import gTTS
import smtplib
print("Content-type:text/html\r\n\r\n")
#all moudule is downloaded ______________________________________________


form = cgi.FieldStorage()

# Get data from fields
Speed = form.getvalue('speed')
accent = form.getvalue('lang')
bookName = form['filename']
email=form.getvalue('mail')


# Test if the file was uploaded
if bookName.filename:
	fn=os.path.basename(bookName.filename)
	open(fn,'wb').write(bookName.file.read())
	message='submitted'
else:
	message = 'No file was uploaded'
#working with raw data 
rawData = parser.from_file(fn)
rawData=rawData['content']
mainData=rawData.replace('\n',' ')
#html page

#converting mp3

tts=gTTS(mainData,slow=Speed,lang="en")
tts.save("temp.mp3")

message="""
Enjoy your Book 

"""
message+="audio file link: http://localhost/pdfAudio/temp.mp3"

#making html page of script
print(f"""
<!DOCTYPE html>
<html>
    <head>
        <title>Audiobook Genrator </title>
        <meta name="viewport" description='device-width'>
        <link rel="stylesheet" href="main.css">
        <link rel="styl" href="main.css">
    </head>
    <body>
        
        <header>
            Readers Delight
        </header>
""")
if (email==""):
	print(f"<a class='srcpage' href='http://localhost/pdfAudio/temp.mp3'>Your File Is Ready</a>")

else:
	print(f"<h5 class='srcpage' >file Path is sent Successfully</h5>")
	s=smtplib.SMTP('smtp.gmail.com',587)
	s.starttls()
	s.login("sangrah170@gmail.com","Sangrah@op#")
	s.sendmail("sangrah170@gmail.com",email,message)
	s.quit()


#ending of html file
print(f"""
       
    </body>
</html>
""")
