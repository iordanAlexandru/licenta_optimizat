from django.shortcuts import render
import pyttsx3
import nltk

import speech_recognition as sr  # importing speech recognition package from google api
# from pygame import mixer
import playsound  # to play saved mp3 file
from gtts import gTTS  # google text to speech
import os  # to save/open files
import wolframalpha  # to calculate strings into formula, its a website which provides api, 100 times per day
from selenium import webdriver  # to control browser operations
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from tensorflow.keras.models import load_model
model = load_model('static/chatbot_model.h5')
import json
import random
from tutorial.models import PacientParsing

intents = json.loads(open('static/intents.json').read())
words = pickle.load(open('static/words.pkl','rb'))
classes = pickle.load(open('static/classes.pkl','rb'))



# Create your views here.


def home(request):
    return render(request, 'speech_bot/home_bot.html')
num = 1

def assistant_speaks(output):
    global num
    num += 1
    print("PerSon : ", output)
    toSpeak = gTTS(text=output, lang='en-US', slow=False)
    file = str(num) + ".mp3"
    toSpeak.save(file)
    # mp3_fp = BytesIO()
    # toSpeak = gTTS(output, 'en', slow=False)
    # toSpeak.write_to_fp(mp3_fp)
    # os.system("D:\PeRSon\\audio\spoken.mp3")
    '''mixer.init()
    mixer.music.load('D:\PeRSon\\audio\spoken.mp3')
    mixer.music.play()
    time.sleep(5)
    mixer.music.stop()'''
    # song = AudioSegment.from_file(mp3_fp, format="mp3")
    # playsound.playsound(mp3_fp)
    playsound.playsound(file, True)
    os.remove(file)


def get_audio():
    r = sr.Recognizer()
    audio = ''
    with sr.Microphone() as source:
        print("Speak...")
        audio = r.listen(source, phrase_time_limit=5)
    print("Stop.")
    try:
        text = r.recognize_google(audio, language='en-US')
        print("You : ", text)
        return text
    except:
        assistant_speaks("Could not understand your audio, PLease try again!")
        return 0


def search_web(input):
    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    driver.maximize_window()
    if 'youtube' in input.lower():
        assistant_speaks("Opening in youtube")
        indx = input.lower().split().index('youtube')
        query = input.split()[indx + 1:]
        driver.get("http://www.youtube.com/results?search_query=" + '+'.join(query))
        return

    elif 'wikipedia' in input.lower():
        assistant_speaks("Opening Wikipedia")
        indx = input.lower().split().index('wikipedia')
        query = input.split()[indx + 1:]
        driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query))
        return
    else:
        if 'google' in input:
            indx = input.lower().split().index('google')
            query = input.split()[indx + 1:]
            driver.get("https://www.google.com/search?q=" + '+'.join(query))
        elif 'search' in input:
            indx = input.lower().split().index('google')
            query = input.split()[indx + 1:]
            driver.get("https://www.google.com/search?q=" + '+'.join(query))
        else:
            driver.get("https://www.google.com/search?q=" + '+'.join(input.split()))
        return


def open_application(input):
    if "chrome" in input:
        assistant_speaks("Google Chrome")
        os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
        return
    elif "firefox" in input or "mozilla" in input:
        assistant_speaks("Opening Mozilla Firefox")
        os.startfile('C:\Program Files\Mozilla Firefox\\firefox.exe')
        return
    elif "word" in input:
        assistant_speaks("Opening Microsoft Word")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Word 2013.lnk')
        return
    elif "excel" in input:
        assistant_speaks("Opening Microsoft Excel")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Excel 2013.lnk')
        return
    else:
        assistant_speaks("Application not available")
        return


negative_phrases = []
with open('static/stopwords.txt', 'r') as file:
    stopwords = file.read().replace('\n', '')


def parse_stopwords(text):
    result = ''
    text_split = text.split(' ')
    result = [word for word in text_split if word not in stopwords]
    result = ' '.join(result)
    return 'google ' + result


def process_text(input, intent):
    try:
        if intent == 'youtube':
            ans = get_audio()
            assistant_speaks('Searching youtube for ' + ans)
            search_web('youtube ' + ans)
        if intent == 'web':
            ans = get_audio()
            assistant_speaks('Searching the web for ' +ans)
            search_web('google '+ ans)
        if intent == 'bad_mood':
            blob1 = TextBlob(input)
            print(format(blob1.sentiment))
            assistant_speaks("can you be more specific and tell me exactly what disturbed you?")
            ans = get_audio()
            negative_phrases.append(ans)
            assistant_speaks("Now I am going to use my wizard powers to make you feel better")
            while(blob1.polarity<0):
                search_web('youtube funny videos')
                blob1 = TextBlob(input)
                # random joke,video, meme
                # after x randoms i ask him how he is feeling
    except Exception as e:
        print(e)
        assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?")
        ans = get_audio()
        if 'yes' in str(ans) or 'yeah' in str(ans):
            search_web(input)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    intent = next(iter(ints[0].values()))
    res = getResponse(ints, intents)
    return res, intent



def speech_to_text(request):
    data = request.POST.get('record')
    import speech_recognition as sr

    # get audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        audio = r.listen(source)
    try:
        output = " " + r.recognize_google(audio)
    except sr.UnknownValueError:
        output = "Could not understand audio"
    except sr.RequestError as e:
        output = "Could not request results; {0}".format(e)
    data = output
    while (1):
        assistant_speaks('What can i do for you?')
        text = get_audio()
        res, intent = chatbot_response(text)
        assistant_speaks(res)
        if text == 0:
            continue
        # assistant_speaks(text)
        if "exit" in str(text) or "bye" in str(text) or "go " in str(text) or "sleep" in str(text):
            assistant_speaks('Ok bye, Alex.')
            break
        text = text.lower()
        print(intent)
        process_text(text, intent)
    return render(request, 'speech_bot/speech_to_text.html', {'data': 'See ya later !'})