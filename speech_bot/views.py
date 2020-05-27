from speech_bot.text_processing import process_text, assistant_speaks, chatbot_response
from django.shortcuts import render
# from key import b71542370a6247d493860e6b01d0d713
import speech_recognition as sr  # importing speech recognition package from google api


def home(request):
    return render(request, 'speech_bot/home_bot.html')


# wikipediapyth


def speech_to_text(request):
    data = request.POST.get('record')

    # get audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("(Test) Speak:")
        audio = r.listen(source)
    try:
        output = " " + r.recognize_google(audio)
    except sr.UnknownValueError:
        output = "Could not understand audio"
    except sr.RequestError as e:
        output = "Could not request results; {0}".format(e)
    data = output
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
                if 'alexa' in text:
                    text_split = text.split('alexa ')
                    text = text_split[1]
                    res, intent = chatbot_response(text)
                    if res != "":
                        assistant_speaks(res)
                    print('intent: ' + intent)
                    text = text.lower()
                    process_text(text, intent, request)
            except:
                continue


    return render(request, 'speech_bot/speech_to_text.html', {'data': 'See ya later !'})
