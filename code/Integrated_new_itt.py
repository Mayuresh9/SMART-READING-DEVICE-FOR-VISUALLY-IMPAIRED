import time
import sys
import os

import cv2


import io
import vlc
import pyttsx3


from google.cloud import vision_v1
from google.cloud.vision_v1 import types

from subprocess import call
from gtts import gTTS
from subprocess import PIPE, Popen
import speech_recognition as sr
from PyDictionary import PyDictionary
#import RPi.GPIO as GPIO

#GPIO.setwarnings(False)
count=1
i=1
VALID_IMAGES = [".jpg",".gif",".png",".tga",".tif",".bmp"]
FNULL = open(os.devnull, 'w')
engine = pyttsx3.init()


def create_directory(path):
        if not os.path.exists(path):
            os.makedirs(path)

def check_path(path):
        return bool(os.path.exists(path))



        
def dictionary():
        try:
            # Record Audio
                r = sr.Recognizer()
                dictionary1= PyDictionary()
                print(sr.Microphone.list_microphone_names())
                with sr.Microphone() as source:
                        print("Say something!")
                        s=vlc.MediaPlayer('./say.mp3') # say.mp3
                        s.play()
                        audio = r.listen(source)

                try:
                        mean = r.recognize_google(audio)
                        print("You said: " + mean)
                except Exception as e:
                        print("Voice not Recognised, Please Re-iterate")
                        e=vlc.MediaPlayer('./not_recog.mp3') #not_recog.mp3
                        e.play()
                        print(type(e))    # the exception instance
                        print(e.args)     # arguments stored in .args
                        print(e)
                        dictionary()                    

                try:
                        text = dictionary1.meaning(mean)
                except Exception as inst: 
                        print("No Meaning Found")
                        e=vlc.MediaPlayer('./no_mean.mp3') #no_mean.mp3
                        e.play()
                        print(type(inst))    # the exception instance
                        print(inst.args)     # arguments stored in .args
                        print(inst)
                        dictionary() 
                
                f = open('hello.txt','w')
                f.write("The meaning of %s is %s" %(mean, text))
                f.close()

                lines = open('hello.txt').read().split('\n')

                def removeNonAscii(s):
                        return "".join(i for i in s if ord(i)<128)

                t = [removeNonAscii(i).strip("'").replace('.', ' ').replace('  ', ' ').replace('{','').replace('}','').replace('[','').replace(']','').replace('Noun','') for i in lines]
                dat = '.'.join(t)
                print(dat)

                tts = gTTS(text=dat, lang='en')
                tts.save('./meaning_'+str(count)+'.mp3')
                print(text)

        except Exception as inst:
                print(type(inst))    # the exception instance
                print(inst.args)     # arguments stored in .args
                print(inst)      
                print ("Exception Occured:")
                e=vlc.MediaPlayer('./oops.mp3') #oops.mp3
                e.play()
                time.sleep(3)
                #dictionary()
        


    
    



def plays():
        global v1
        v1= vlc.MediaPlayer('page_'+str(count)+'.mp3')

        k1=vlc.MediaPlayer('./options.mp3')  #options
        k1.play()
        #timer=0
        key=input("Enter 2 to 'start the speech' \n 5 for PAUSE/RESUME \n 6 for STOP\n 9 for Dictionary Query\n 7 for Mechanism\n")
        

        while True:
                if key=='2':

                        v1.play()
                        #time.sleep(50)

                if key=='5':
                        v1.pause()

                if key=='6':
                        v1.stop()
                if key=='9':
                        if v1.is_playing():
                                v1.pause()
                        dictionary()
                        v2=vlc.MediaPlayer('meaning_'+str(count)+'.mp3')
                        k='9'
                        if i==1:
                                
                                print("Press 0 to Stop dictionary")
                                
                                p=vlc.MediaPlayer('./stop_d.mp3') #stop_d
                                p.play()
                                time.sleep(2)
                                
                                while k!='0':
                                        v2.play()
                                        k=input()
                                
                                time.sleep(3)
                                v2.stop()
                        print("Speech Continues here:")
                        sp=vlc.MediaPlayer('./conti.mp3') # conti.mp3
                        sp.play()
                        
                        time.sleep(2)
                        v1.pause()
                if key=='4':
                        exit()
                        
                key=input()
        
        
        
        
        
                
                
def text_2_speech():
        lines = open('./'+str(count)+'.txt').read().split('\n')

        def removeNonAscii(s):
                return "".join(i for i in s if ord(i)<128)


        t = [removeNonAscii(i).strip("'").replace('  ', ' ') for i in lines]
        print(t)
        dat = ' '.join(t)
        print(dat)
        w=vlc.MediaPlayer('./wait.mp3') # wait
        w.play()
        tts = gTTS(text=dat, lang='en',slow = False)
        tts.save('page_'+str(count)+'.mp3')
        plays()
        print("Page_"+str(count)+"Done")
        

def capture(count):
        

        cam=cv2.VideoCapture(1)
        
        ret_val, img=cam.read()
        while not ret_val:
                ret_val, img=cam.read()
        time.sleep(1)
                
        

        if ret_val:
                cam.release()  
                print (ret_val)
                cv2.imwrite('./'+str(count)+'.jpg',img)
                print ("Done:")
                c=vlc.MediaPlayer('./cap_fin.mp3') #cap_fin.mp3
                c.play()
                time.sleep(2)

def process():
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './sonic-proxy-349112-978bf7dd6dc9.json' # Add your own json credentials file
        client = vision_v1.ImageAnnotatorClient()
        path = './'+str(count)+'.jpg'

        with io.open(path, 'rb') as image_file:
                content = image_file.read()

        image = vision_v1.types.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations

        print('"{}"'.format(texts[0].description))

        f = open('./'+str(count)+'.txt','w')
        print("Converted Text:-\n")

        f.write('"{}"'.format(texts[0].description))

        f.close()        
       
        if os.path.isfile('./'+str(count)+'.txt'):
                text_2_speech()
                print("Text created") 
        else:
                print("Text not created") 
            
        
#if __name__=='__main__':
while True:
        st=vlc.MediaPlayer('./start.mp3')
        st.play()
        if input("Enter 1 to start\n")=='1':
                print ("This is page no."+str(count)) 
                print ("Started")
                capture(count)
                process()
                count=count+1
                
        else:
                print (" Invalid Key")
                i=vlc.MediaPlayer('./invalid.mp3')
                i.play()
