import threading

from speech_bot.text_processing import process_text, assistant_speaks, chatbot_response
from django.shortcuts import render
from tutorial.decorators import pacient_and_admin_only
# from key import b71542370a6247d493860e6b01d0d713
import speech_recognition as sr  # importing speech recognition package from google api

@pacient_and_admin_only
def home(request):
    return render(request, 'speech_bot/home_bot.html')

def thread_loop(request, r):
    with sr.Microphone() as source:
        while (1):
            try:
                print('Listening ...')
                audio = r.listen(source)

                text = r.recognize_google(audio, language='en-US')

                res, intent = chatbot_response(text)
                print(intent)
                if intent == 'goodbye':
                    assistant_speaks(res)
                    break
                text = text.lower()
                print('You: ' + text)
                if 'emma' in text:
                    text_split = text.split('emma ')
                    text = text_split[1]
                    res, intent = chatbot_response(text)
                    if res != "":
                        assistant_speaks(res)
                    print('intent: ' + intent)
                    text = text.lower()
                    process_text(text, intent, request)
            except:
                continue

@pacient_and_admin_only
def speech_to_text(request):
    r = sr.Recognizer()
    threadTalkLoop = threading.Thread(target=thread_loop, kwargs={'request':request, 'r':r})
    threadTalkLoop.start()
    return render(request, 'speech_bot/home_bot.html', {'data': 'See ya later !'})
