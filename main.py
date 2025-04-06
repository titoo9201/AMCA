import pyttsx3
import speech_recognition as sr
import pywhatkit
import webbrowser
import datetime
import pyautogui
from plyer import notification
import wikipedia
import json
import smtplib 
import ssl
import requests
import os 
from langdetect import detect



with open("contact.json","r") as file1:
    contact=json.load(file1)

with open("email.json","r") as file2:
    email=json.load(file2) 

with open("huggingface.json","r") as hf_file:
    hf_data=json.load(hf_file)
HUGGINGFACE_API_TOKEN = hf_data["hf_token"]    

engine = pyttsx3.init()
voices = engine.getProperty('voices') 
engine.setProperty('rate',170 ) 

def speak(audio):
     try:
         lang=detect(audio)
         if lang=='hi':
             engine.setProperty('voice',voices[2].id)
         else:
             engine.setProperty('voice',voices[2].id)
     except:
         engine.setProperty('voice',voices[2].id)            
     
     engine.say(audio)
     engine.runAndWait()

def command():
    content=" "
    while content==" ":
        # yha se microphone se voice input hogei 
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        try:
            content=r.recognize_google(audio,language='en-in')
            print("you said (ENGLISH):" + content )
            
        except:
            try:
                content=r.recognize_google(audio,language="hi-IN")
                print("you said (hindi):" + content)
            except:
                print("please try again...")    

    return content
def main_process():
    
    while True:
        request=command().lower()
        if "AmCa" in request:
            speak("Yes sir,AmCa is listening")
            request=request.replace("AmCa","").strip()
        elif "play" in request and "on youtube" in request:
             song_name=request.replace("play","").replace("on youtube","").strip()
             if song_name:
                speak(f"playing {song_name} on YouTube")
                pywhatkit.playonyt(song_name)
             else:
                speak("please say the song name before saying on YouTube.") 

        elif "say time" in request:
             now_time = datetime.datetime.now().strftime("%H:%M")
             speak("Current time is " + str(now_time))    
        elif "say date" in request:
              now_date = datetime.datetime.now().strftime("%d-%m")
              speak("Current date is " + str(now_date))
        elif "new task" in request:
              task=request.replace("new task","")
              task=task.strip()
              if task!="":
                 speak("adding task:"+task)
                 with open("todo.txt","a") as file:
                     file.write(task+"\n")
        elif "speak task " in request:
             with open("todo.txt","r") as file:
                 speak("work we have to do is :"+ file.read())

        elif "show work" in request:
            with open("todo.txt","r") as file:
                 tasks= file.read()

            notification.notify(
                title="Today's work",
                message=tasks
            )

         
        # oepn web browser
        #elif "launch Instagram " in request:
             #webbrowser.open("https://www.instagram.com/")
        # elif "launch Facebook " in request:
        #      os.system(f'{chrome}https://www.instagram.com/')    
        # elif "launch Leetcode " in request:
        #     os.system(f'{chrome}https://www.instagram.com/')
        # elif "launch CodeChef " in request:
        #      os.system(f'{chrome}https://www.instagram.com/')
        # elif "launnch Code" in request:
        #      os.system(f'{chrome}https://www.instagram.com/')       
        # elif "launch Canva " in request:
        #     os.system(f'{chrome}https://www.instagram.com/')
        # elif "launch Amazon " in request:
        #      os.system(f'{chrome}https://www.instagram.com/')
        # elif "launch Flipkart " in request:
        #      os.system(f'{chrome}https://www.instagram.com/')    


# open local app 
        elif "open " in request:
            query=request.replace("open","")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
        

        elif "wikipedia " in request:
            request=request.replace("AmCa","")
            request=request.replace("search wikipedia","")
            result=wikipedia.summary(request, sentences=2)
            print(result)
            speak(result)


        elif "search google " in request:
            request=request.replace("AmCa","")
            request=request.replace("search google","")
            webbrowser.open("https://www.google.com/search?q="+request)

        elif "send whatsapp" in request:
            speak("Whom do you want to message?")
            name = command().lower()

            if name in contact:
                number = contact[name]
                speak(f"What is the message for {name}?")
                message = command()
                now = datetime.datetime.now()
                hour = now.hour
                minute = now.minute + 2  # to avoid time error
                speak(f"Sending your message to {name}. Please wait.")
                pywhatkit.sendwhatmsg(number, message, hour, minute)
                
                    
            else:
                speak("Sorry, this contact is not in your list.")    


        elif "send email" in request:
             speak("Whom do you want to send an email?")
             name = command().lower()
             if name in email:
                  to_email = email[name]
                  speak("What is the subject?")
                  subject = command()
                  speak("What is the message?")
                  message = command()
                  try:
                       with open("config.json", "r") as f:
                           creds = json.load(f)
                       sender_email = creds["gmail_id"]
                       sender_password = creds["gmail_password"]
                       email_message = f"Subject: {subject}\n\n{message}" 
                       context = ssl.create_default_context() 
                       with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                            server.login(sender_email, sender_password)
                            server.sendmail(sender_email, to_email, email_message)
                       speak("Email has been sent successfully.")
                  except Exception as e: 
                       speak("Sorry, I was not able to send the email.")
                       print(e)

             else:
                  speak("I couldn't find that contact.")          
        # main code start here ai role hindi voice ,image generation,ask question 
        #ai se chat ke liye code tha 
        elif "ask ai" in request or "poochho ai se " in request:
            speak("kya poochhna hai AI se?")
            question=command()
            API_URL="https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
            headers={"Authorization":f"Bearer{HUGGINGFACE_API_TOKEN}"}
            payload={
                "input":f"<|system|>Tu ek helpful Hindi assistant hai<|user|>{question}<|assistant|>",
                "parameters":{"max_new_tokens":400}
            }
            response=requests.post(API_URL,headers=headers,json=payload)
            result=response.json()
            try:
                reply=result[0]["generated_text"].split("<|assistant|>")[-1].strip()
            except:
                reply="kuch galat ho gya AI se baat karte time." 
                print(reply)   
                speak(reply)
        # image generation ke liye code hai ab         

        elif "generate image" in request or "image bana de" in request:
            speak("kis cheez ki image chahiye?")
            image_prompt=command()
            API_URL= "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
            headers = { "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
                       "Accept": "application/json"}
            payload = {"inputs": image_prompt}
            speak("Thoda ruk ja bhai, image ban rahi hai...")
            response=requests.post(API_URL,headers=headers,json=payload)
            if response.status_code==200:
                with open("output_image.png","wb") as f:
                    f.write(response.content)
                speak("image bana di bhai, dekh le: output_image.png")
                os.startfile("output_image.png")
            else:
                speak("image generate nahi ho payi.")        
        elif "exit" in request or "band ho ja" in request:
            speak("okay sir,shutting down have a nice day sir !")
            break
main_process()