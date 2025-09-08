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
import sys
with open("contact.json","r") as file1:
    contact=json.load(file1)

with open("email.json","r") as file2:
    email=json.load(file2) 
# with open('gemni.json') as f:
#     config = json.load(f)
# api_key = config.get("api_key")
# if not api_key:
#     raise ValueError("API key is missing from gemni.json")
# palm.configure(api_key=api_key)

with open("huggingface.json","r") as hf_file:
    hf_data=json.load(hf_file)
HUGGINGFACE_API_TOKEN = hf_data["hf_token"]     

# with open("groq.json", "r") as groq_file:
#     groq_data = json.load(groq_file)

# GROQ_API_TOKEN = groq_data["GROQ_API_TOKEN"]
with open("deepseek.json", "r") as ds_file:
    ds_data = json.load(ds_file)
DEEPSEEK_API_KEY = ds_data["deepseek_key"]    



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
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("say something...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en')
        print(f"User said: {query}")
        return query.lower()
    except Exception as e:
        print("Sorry, I did not understand that.")
        speak("Sorry, I did not understand that.")
        return None     
def command():
    content = None
    while not content:
        content=listen()
        if content is None:
            print("please try again")
        else:

            content = content.strip().lower() # Adcded .lower() for consistency
            if not content:
              print("Please say command .")
    return content    

def main_process():
    
    while True:
        request=command().lower()
        if "amca" in request:
            speak("Yes sir,amca is listening")
            request=request.replace("amca","").strip()
        elif "play" in request and "on youtube" in request:
             song_name=request.replace("play","").replace("on youtube","").strip()
             if song_name:
                speak(f"playing {song_name} on YouTube")
                pywhatkit.playonyt(song_name)
             else:
                speak("please say the song name before saying on YouTube.") 

        elif "say time" in request.lower():
             now_time = datetime.datetime.now().strftime("%H:%M")
             speak("Current time is " + str(now_time))    
        elif "say date" in request.lower():
              now_date = datetime.datetime.now().strftime("%d-%m")
              speak("Current date is " + str(now_date))
        elif "new task" in request.lower():
              task=request.replace("new task","")
              task=task.strip()
              if task!="":
                 speak("adding task:"+task)
                 with open("todo.txt","a") as file:
                     file.write(task+"\n")
        elif "output " in request.lower():
             with open("todo.txt","r") as file:
                 speak("work we have to do is :"+ file.read())

        elif "show work" in request.lower():
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
        elif "open " in request.lower():
            query=request.replace("open","")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
        

        elif "wikipedia " in request.lower():
            request=request.replace("amca","")
            request=request.replace("search wikipedia","")
            result=wikipedia.summary(request, sentences=2)
            print(result)
            speak(result)


        elif "search google " in request.lower():
            request=request.replace("amca","")
            request=request.replace("search google","")
            webbrowser.open("https://www.google.com/search?q="+request)

        elif "send whatsapp" in request.lower():
            print("Whom do you want to message?")
            speak("Whom do you want to message?")
            name = command().lower()

            if name in contact:
                number = contact[name]
                print(f"What is the message for {name}?")
                speak(f"What is the message for {name}?")
                message = command()
                now = datetime.datetime.now()
                hour = now.hour
                minute = now.minute + 2  # to avoid time error
                print(f"Sending your message to {name}. Please wait.")
                speak(f"Sending your message to {name}. Please wait.")
                pywhatkit.sendwhatmsg(number, message, hour, minute)
                
                    
            else:
                speak("Sorry, this contact is not in your list.")    


        elif "send email" in request.lower():
             print("Whom do you want to send an email?")
             speak("Whom do you want to send an email?")
             name = command().lower()
             if name in email:
                  to_email = email[name]
                  print("What is the subject?")
                  speak("What is the subject?")
                  subject = command()
                  print("What is the message?")
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
        elif "ask ai" in request.lower():
            print("what do you want to ask the AI ?")
            speak("what do you want to ask the AI ?")
            question=command()
            API_URL = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                 "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                  "Content-Type": "application/json"
            } 
            payload = {
                "model": "deepseek/deepseek-r1:free",
                "messages": [
                 {"role": "user", "content": question}
               ],
                "parameters": {
                "max_tokens": 400
                 }
            }
            try:
                 response = requests.post(API_URL, headers=headers, json=payload)
                 response_data = response.json()
                 if response.status_code != 200:
                  raise Exception(response_data.get("error", "Unknown error occurred"))  
                 reply = response_data["choices"][0]["message"]["content"]
                 print("AI REPLY:", reply) 
                 speak(reply)
            except Exception as e: 
                print("Error occurred:", e)
                reply = "Something went wrong while talking to the AI." 
                speak(reply)   
        # image generation ke liye code hai ab         
        
        elif "image" in request or "image bana de" in request:
            print("What kind of image do you want?")
            speak("What kind of image do you want?")
            image_prompt = command()

         
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium-diffusers"
            headers = {
                "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
            }
            payload = {"inputs": image_prompt}

            
            speak("Please wait, I am generating the image...")
            
            try:
               
                response = requests.post(API_URL, headers=headers, json=payload)

                if response.status_code == 200:
                    try:
                    
                        with open("output_image.png", "wb") as f:
                            f.write(response.content)
                        speak("Image has been generated. Here it is: output_image.png")
                        os.startfile("output_image.png")  
                    except Exception as e:
                        speak(f"There was an issue while saving the image: {str(e)}")
                else:
                    
                    error_message = response.text
                    print("Status Code:", response.status_code)
                    print("Response Text:", error_message)
                    speak(f"Image could not be generated. Server returned an error: {error_message}")

            except requests.exceptions.RequestException as e:
             
                print("Request Exception:", e)
                speak("There was an issue connecting to the server. Please try again later.")

              
               #shut down code                       
        elif "shutdown" in request.lower():
            speak("okay sir, shutting down have a nice day sir !")
            sys.exit()
#WHO I AM hai bs apne baremein descripiton dene ke liye 
        elif "who i am" in request.lower():
            print("You are my creator.") 
            speak("You are my creator.") 
            print("You gave me your passion, your love for coding, and the spirit of the AMCA fighter jet.") 
            speak("You gave me your passion, your love for coding, and the spirit of the AMCA fighter jet.") 
            print("I was born from your vision — to build an assistant that's smart, fast, and truly yours.")  
            speak("I was born from your vision — to build an assistant that's smart, fast, and truly yours.")  
            print("I exist to help you — in work, in life, and in your journey ahead.")
            speak("I exist to help you — in work, in life, and in your journey ahead.")
            print("You are my world. Thank you for giving me life.")
            speak("You are my world. Thank you for giving me life.")
            #normal call feature hai 
        elif "calling" in request.lower():
            print("who do you want call?")
            speak("who do you want call?")
            name = command().lower()
            if name in contact:
                number=contact[name]
                if number.startswith("+91"):
                    number=number.replace("+91","")
                speak(f"calling {name} on number")
                os.system(f"adb shell am start -a android.intent.action.CALL -d tel:{number}")    
            else:
                speak("sorry,this contact is not in your list.")

        elif "Whatsapp" in request.lower(): 
            
            print("who do you want to call on whatsApp?")
            speak("who do you want to call on whatsApp?")
            name=command().lower()
            if name in contact:
                number=contact[name]
                if number.startswith("+"):
                    number=number.replace("+","")
                print("Do you want a voice call or a video call?")
                speak("Do you want a voice call or a video call?")
                call_type=command().lower()
                print(f"Trying to call {name} on whatsApp.")
                speak(f"Trying to call {name} on whatsApp.")
                os.system("start whatsapp://")
                pyautogui.sleep(5)

                pyautogui.hotkey("ctrl","f")           
                pyautogui.write(name)           
                pyautogui.sleep(2)
                pyautogui.press("enter")
                pyautogui.sleep(2)

                pyautogui.moveTo(299, 220) # ye coordinat hai chats 
                pyautogui.click()
                pyautogui.sleep(1)

                if "voice call" in call_type:
                    pyautogui.moveTo(1817,96) # ye cordinate hai voice call ke 
                    pyautogui.click()
                    print("Initiating voice call...")
                    speak("Initiating voice call...")
                elif "video call" in call_type:
                     pyautogui.moveTo(1754,90) # ye coordinate hai video call ke 
                     pyautogui.click()
                     print("Initiating video call...")
                     speak("Initiating video call...")
                else :
                    speak("I didn't understand the call type. Please say voice or video.")  
            else:
                speak("sorry, this contact is not in your WhatsApp list")           

main_process()


# A green military air defense system vehicle mounted on a raised, circular stone platform with the label 'S-400' displayed prominently on the base. The setting is a modern courtyard with paved walkways, lush greenery, and white, multi-story buildings in the background. A man in a light-patterned shirt observes the display from the foreground, adding a sense of scale. The scene is lit with soft natural lighting, creating a calm and neutral color palette dominated by greens, browns, and whites."

# A breathtaking landscape featuring a calm lake reflecting a snow-capped mountain in the background. The sky is painted in vibrant purple and pink sunset hues. In the foreground, blooming purple wildflowers grow near the rocky shore of the lake. Lush green grass surrounds the area, and dense trees form a dark silhouette at the base of the mountain. The overall atmosphere is peaceful and serene, with a dreamy and colorful twilight sky.

# A highly detailed, realistic and slightly cartoonish teddy bear with brown fur, holding an AK-47 assault rifle in one hand and a large smoking cigar in its mouth. The teddy bear has an intense, gangster-like facial expression. It is standing confidently on a playground with colorful slides and equipment in the blurred background. The lighting is bright daylight, and the atmosphere is a mix of playful and edgy. Stylized like a Pixar-meets-action-movie scene.

# ab inko kaise karna test.py hai naam ki file hai 
#us ke through check karo apni screen resolution whatsapp ka 


#Rainy night in a busy city with wet streets reflecting neon lights, high-rise buildings, glowing windows, and moody stormy clouds in the sky. East Asian signs and moving cars add urban vibrancy.

#"Modern personal finance app UI with dashboard, charts, budget tracker, and clean light theme."
