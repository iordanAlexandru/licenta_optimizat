import sys
import re
import time
import requests
from django.shortcuts import render
from newsapi import NewsApiClient
# from key import b71542370a6247d493860e6b01d0d713
import datetime as dt
import pandas as pd
import nltk
from django.core.mail import send_mail
import speech_recognition as sr  # importing speech recognition package from google api
# from pygame import mixer
import playsound  # to play saved mp3 file
from gtts import gTTS  # google text to speech
import os  # to save/open files
import wolframalpha  # to calculate strings into formula, its a website which provides api, 100 times per day
from selenium import webdriver  # to control browser operations
from textblob import TextBlob
from textblob import Word
from fake_useragent import UserAgent
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from bs4 import BeautifulSoup
from tensorflow.keras.models import load_model

model = load_model('static/chatbot_model.h5')
import json
import random
from tutorial.models import PacientParsing, Pacient, AlzheimerParsing, DepressionParsing, DiabetesParsing, \
    PacientDetails
from datetime import datetime, timedelta
import datefinder
import wikipedia
from tmdbv3api import TMDb, Discover

tmdb = TMDb()
tmdb.api_key = '530ff67defeb9213256896802945b0d2'

intents = json.loads(open('static/intents.json').read())
words = pickle.load(open('static/words.pkl', 'rb'))
classes = pickle.load(open('static/classes.pkl', 'rb'))

num = 1


def assistant_speaks(output):
    global num
    num += 1
    print("Alexa : ", output)
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
    assistant_speaks('Opening Firefox')
    return result
    # search_web('google '+result)


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return (np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
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
        if (i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result


def chatbot_response(msg):
    ints = predict_class(msg, model)
    intent = next(iter(ints[0].values()))
    res = getResponse(ints, intents)
    return res, intent


def get_audio():
    r = sr.Recognizer()
    audio = ''
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=50)
    print("Stop.")
    try:
        text = r.recognize_google(audio, language='en-US')
        print("You : ", text)
        res, intent = chatbot_response(text)
        if intent == 'goodbye':
            assistant_speaks(res)
            sys.exit()
        return text
    except:
        assistant_speaks("Could not understand your audio, PLease try again!")
        sys.exit()


def parse_details(ans):
    result = ''
    ans = ans.split()
    for word in ans:
        if word not in stopwords:
            result += word + ' '
    return result


def parse_text(input, keyword):
    if keyword in input:
        ans = input
        indx = ans.split().index(keyword)
        query = ans.split()[indx + 1:]
        result = wikipedia.page(' '.join(query))
        assistant_speaks(result.title)
        assistant_speaks(result.summary[0:400])
        assistant_speaks('Do you want me to continue?')
        ans = get_audio()
        res, intent = chatbot_response(ans)
        if intent == 'yes':
            assistant_speaks(result.summary[400:])
        elif intent == 'no':
            assistant_speaks('Exiting wikipedia module')
    else:
        suggestion = wikipedia.suggest(input)
        result = wikipedia.page(suggestion)
        assistant_speaks(result.title)
        assistant_speaks(result.summary[0:400])


def parse_movies(genre_id, discover, movieInstance, genre_string):
    assistant_speaks("The top 3 best " + genre_string + " movies are the following")
    movie = discover.discover_movies({
        'with_genres': genre_id,
        'sort_by': 'vote_average.desc'
    })
    assistant_speaks('I will read the title and the description')
    for mov in movie[0:3]:
        mov = str(mov)
        searchMovie = movieInstance.search(mov)
        result = searchMovie[0]
        assistant_speaks(mov)
        assistant_speaks('description is ' + result.overview)
    assistant_speaks('exiting movie module')


def process_text(input, intent, request=None):
    try:
        if intent == 'youtube':
            assistant_speaks('Sure. Tell me what do you want to search for')
            ans = get_audio()
            result = parse_stopwords(ans)
            search_web('youtube ' +result)
        if intent == 'knowledge':
            if 'about' in input:
                parse_text(input, 'about')
            if 'what is' in input:
                parse_text(input, 'is')
            if 'who was' in input:
                parse_text(input, 'was')
        if intent == 'web_search':
            if 'about' in input:
                ans = input
                indx = ans.split().index('about')
                query = ans.split()[indx + 1:]
                string_query = ' '.join(query)
                result = parse_stopwords(string_query)
                search_web('google ' + result)
            if 'for' in input:
                ans = input
                indx = ans.split().index('for')
                query = ans.split()[indx + 1:]
                string_query = ' '.join(query)
                result = parse_stopwords(string_query)
                search_web('google ' + result)

        movie_list_intents = ['movie', 'horror', 'action', 'comedy', 'popular', 'thriller']
        if intent in movie_list_intents:
            from tmdbv3api import Movie

            movie = Movie()
            discover = Discover()
            if intent == 'popular':
                pop_movie = discover.discover_movies({
                    'sort_by': 'popularity.desc'
                })
                assistant_speaks("The most popular 5 movies are the following")
                pop_movies = ", ".join(str(x) for x in pop_movie[0:5])
                assistant_speaks(pop_movies)
            if intent == 'horror':
                parse_movies(27, discover, movie, 'horror')
            if intent == 'action':
                parse_movies(28, discover, movie, 'action')
            if intent == 'comedy':
                parse_movies(35, discover, movie, 'comedy')
            if intent == 'thriller':
                parse_movies(53, discover, movie, 'thriller')
            if intent == 'movie':
                assistant_speaks('Do you want a movie recommendation?')
                ans = get_audio()
                if 'yes' in ans:
                    pacient = Pacient.objects.get(user=request.user)

                    pac_details = PacientDetails.objects.get(pacient=pacient)
                    fav_movie = pac_details.fav_movie
                    search_movie = movie.search(fav_movie)
                    assistant_speaks('I will read top three recommended movies based on your favorite movie')
                    res = search_movie[0]
                    recommendations = movie.recommendations(movie_id=res.id)
                    cnt = 0
                    for recommendation in recommendations:
                        if cnt >= 3:
                            break
                        else:
                            assistant_speaks(recommendation.title)
                            assistant_speaks(recommendation.overview)
                        cnt += 1
                else:
                    assistant_speaks(
                        'I can give you the top movies based on a genre. Just tell me what are you looking for')
                    ans = get_audio()
                    res, ints = chatbot_response(ans)
                    process_text(ans, ints)

        pacient = Pacient.objects.get(user=request.user)
        pac_pars = PacientParsing.objects.get(pacient=pacient)
        if intent == 'event':
            from googleapiclient.discovery import build
            from google_auth_oauthlib.flow import InstalledAppFlow
            scopes = ['https://www.googleapis.com/auth/calendar']
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
            credentials = flow.run_console()
            pickle.dump(credentials, open("token.pkl", "wb"))
            credentials = pickle.load(open("token.pkl", "rb"))
            service = build("calendar", "v3", credentials=credentials)

            calendarlist = service.calendarList().list().execute()
            calendar_id = calendarlist['items'][0]['id']
            result = service.events().list(calendarId=calendar_id, timeZone="Europe/Bucharest").execute()

            timp_event = get_audio()

            assistant_speaks("What about the name of the event?")
            name = get_audio()

            assistant_speaks("would you like to add a description?")
            ans = get_audio()
            sub_resp, sub_intent = chatbot_response(ans)
            if sub_intent == 'yes':
                assistant_speaks("please tell me the description")
                desc = get_audio()
                assistant_speaks("should i add a location too?")
                ans = get_audio()
                sub_resp, sub_intent = chatbot_response(ans)
                if sub_intent == 'yes':
                    assistant_speaks("Go ahead, tell me the location")
                    location = get_audio()
                    create_event(service, timp_event, name,1, desc, location)
                elif sub_intent == 'no':
                    create_event(service, timp_event, name,1, desc)
            elif sub_intent == 'no':
                create_event(service, timp_event, name)
            assistant_speaks('Event ' + name + ' created.')
        if intent == 'web':
            ans = get_audio()
            result = parse_stopwords(ans)
            search_web('google '+result)
        if intent == 'discussion':
            assistant_speaks('Is there a certain topic you would like to discuss?')
            ans = get_audio()
            print(ans)
            sub_resp, sub_intent = chatbot_response(ans)
            print(sub_intent)
            if sub_intent == 'no':
                assistant_speaks('Then how about you tell me more about yourself?')
                try:
                    pac_details = PacientDetails.objects.get(pacient=pacient)
                except PacientDetails.DoesNotExist:
                    pac_details = PacientDetails.objects.create(pacient=pacient)
                if pac_details.fav_activity == '':
                    assistant_speaks('Tell me your favorite activity')
                    ans = get_audio()
                    if "don't" not in ans or 'no' not in ans:
                        ans = parse_details(ans)
                        print(ans)
                        pac_details.fav_activity = ans
                        pac_details.save()
                if pac_details.fav_movie == '':
                    assistant_speaks('what about your favorite movie?')
                    ans = get_audio()
                    if "don't" not in ans or 'no' not in ans:
                        ans = parse_details(ans)
                        pac_details.fav_movie = ans
                        pac_details.save()
                if pac_details.fav_game == '':
                    assistant_speaks('Tell me your favorite game')
                    ans = get_audio()
                    if "don't" not in ans or 'no' not in ans:
                        ans = parse_details(ans)
                        pac_details.fav_game = ans
                        pac_details.save()
                if pac_details.fav_passion == '':
                    assistant_speaks('Do you have a favorite passion?')
                    ans = get_audio()
                    if "don't" not in ans or 'no' not in ans:
                        ans = parse_details(ans)
                        pac_details.fav_passion = ans
                        pac_details.save()
                if pac_details.fav_song == '':
                    assistant_speaks('What is your favorite song?')
                    ans = get_audio()
                    if "don't" not in ans or 'no' not in ans:
                        ans = parse_details(ans)
                        pac_details.fav_song = ans
                        pac_details.save()
                if pac_details.fav_book == '':
                    assistant_speaks('And your favorite book is?')
                    ans = get_audio()
                    if "don't" not in ans or 'no' not in ans:
                        ans = parse_details(ans)
                        pac_details.fav_book = ans
                        pac_details.save()
                assistant_speaks("How was your day so far? When you have finished talking, please say that's it")
                r = sr.Recognizer()
                list = []
                happy_list = ['That sounds great !', 'Wow, I am glad for you', 'Good job!', 'This sounds awesome']
                neutral_list = ['Okay, continue', 'Understood', 'What next?', 'Is there something more?']
                sad_list = ['What is the specific reason that made you feel this way? Please keep it short',
                            'Can you please tell me what is the root of the problem? Please keep it short',
                            'what disturbed you that much? Please keep it short']
                with sr.Microphone() as source:
                    while (1):
                        try:
                            print('Listening to your day: ')
                            audio = r.listen(source)
                            text = r.recognize_google(audio, language='en-US')
                            blob1 = TextBlob(text)
                            blob1 = blob1.correct()
                            text = text.lower()
                            print(format(blob1.sentiment))
                            if "that's it" in text:
                                break
                            if blob1.polarity < 0:
                                assistant_speaks(random.choice(sad_list))
                                motiv = get_audio()
                                pac_pars._negative_problems += motiv + '\n'
                                pac_pars.contor_mesaje += 1
                                if pac_pars.contor_mesaje % 3 == 0:
                                    pac_pars.contor_mesaje = 0
                                    send_mail(
                                        'Mesaj informare pacient ' + str(pacient),
                                        'Urmatoarele probleme par sa-l afecteze pe pacient: ' + pac_pars._negative_problems,
                                        'virtual_assistant@gov.com',
                                        ['bpiwbpiw1@gmail.com'],
                                        fail_silently=False,
                                    )
                                list.append(motiv)
                                pac_pars.save()
                            if blob1.polarity > 0.5:
                                assistant_speaks(random.choice(happy_list))
                            elif blob1.polarity <= 0.5 and blob1.polarity >= 0:
                                assistant_speaks(random.choice(neutral_list))
                        except:
                            continue

                motiv = random.choice(list)
                research_later = "what+to+do+when+" + motiv
                ua = UserAgent()
                google_url = "https://www.google.com/search?q=" + research_later
                response = requests.get(google_url, {"User-Agent": ua.random})
                soup = BeautifulSoup(response.text, "html.parser")
                result_div = soup.find_all('div', attrs={'class': 'ZINbbc'})

                links = []
                titles = []
                descriptions = []
                for r in result_div:
                    # Checks if each element is present, else, raise exception
                    try:
                        link = r.find('a', href=True)
                        title = r.find('div', attrs={'class': 'vvjwJb'}).get_text()
                        description = r.find('div', attrs={'class': 's3v9rd'}).get_text()

                        # Check to make sure everything is present before appending
                        if link != '' and title != '' and description != '':
                            links.append(link['href'])
                            titles.append(title)
                            descriptions.append(description)
                    # Next loop if one element is not present
                    except:
                        continue
                to_remove = []
                clean_links = []
                for i, l in enumerate(links):
                    clean = re.search('\/url\?q\=(.*)\&sa', l)

                    # Anything that doesn't fit the above pattern will be removed
                    if clean is None:
                        to_remove.append(i)
                        continue
                    clean_links.append(clean.group(1))
                # Remove the corresponding titles & descriptions
                # for x in to_remove:
                #     print(titles[x])
                #     print(descriptions[x])
                #     del titles[x]
                #     del descriptions[x]
                random_seed = random.randint(0, 3)
                print('rand_seed: ')
                print(random_seed)
                print('titles: ' + str(len(titles)))
                print('links: ' + str(len(clean_links)))
                assistant_speaks("I have found something regarding the problems you have just told me")
                assistant_speaks("The article title is called")
                assistant_speaks(titles[random_seed])
                assistant_speaks("Do you want me to open the link for you?")
                ans = get_audio()
                sub_resp, sub_intent = chatbot_response(ans)
                if sub_intent == 'yes':
                    driver = webdriver.Firefox()
                    driver.implicitly_wait(1)
                    driver.maximize_window()
                    driver.get(clean_links[random_seed])
                    assistant_speaks('I have opened the browser for you. Exiting discussion module')
                else:
                    return

        if intent == 'news':
            assistant_speaks("Would you like the news on a specific subject?")
            ans = get_audio()
            newsapi = NewsApiClient(api_key='b71542370a6247d493860e6b01d0d713')
            sub_resp, sub_intent = chatbot_response(ans)
            if sub_intent == 'yes':
                assistant_speaks('What would you like me to search for? Please be as specific as you can.')
                ans = get_audio()
                data = newsapi.get_everything(q=ans, language='en', page_size=5)
                articles = data['articles']
                assistant_speaks(
                    'You could choose one article by saying stop when i finish reading the headline. To continue '
                    'reading the headlines, just say continue. I found the following articles: ')
                for article in articles:
                    title = article['title']
                    url = article['url']
                    content = article['content']
                    assistant_speaks(title)
                    ans = get_audio()
                    if 'continue' in ans:
                        continue
                    elif 'stop' in ans:
                        assistant_speaks('I will read the article content')
                        assistant_speaks(content)
                        assistant_speaks(
                            'I can open the webpage which contains the article source. Do you want me to do that? ')
                        ans = get_audio()
                        sub_resp, sub_intent = chatbot_response(ans)
                        if sub_intent == 'yes':
                            driver = webdriver.Firefox()
                            driver.implicitly_wait(1)
                            driver.maximize_window()
                            driver.get(url)
                            r = sr.Recognizer()
                            assistant_speaks(
                                'I have opened your browser. To resume the articles read, just say resume. '
                                'If you want me to stop, just say stop')
                            with sr.Microphone() as source:
                                while (1):
                                    print('Listening ...')
                                    audio = r.listen(source)
                                    try:
                                        text = r.recognize_google(audio, language='en-US')
                                        if 'resume' in text:
                                            break
                                        elif 'stop' in text:
                                            return
                                    except:
                                        continue
                        elif sub_intent == 'no':
                            assistant_speaks('would you like me to continue reading the next articles?')
                            ans = get_audio()
                            sub_resp, sub_intent = chatbot_response(ans)
                            if sub_intent == 'yes':
                                continue
                            elif sub_intent == 'no':
                                assistant_speaks('If you want to find out more, just let me know. Exiting news module')
                                break
            elif sub_intent == 'no':
                assistant_speaks('Alright, i am going to search for the top headlines')
                url = ('http://newsapi.org/v2/top-headlines?'
                       'country=us&'
                       'apiKey=b71542370a6247d493860e6b01d0d713')
                response = requests.get(url).json()
                articles = response['articles']
                assistant_speaks(
                    'Say stop after I finish reading the headline to tell you its content. To continue reading '
                    'the headlines, just say continue. I found the following articles: ')
                for article in articles:
                    title = article['title']
                    url = article['url']
                    content = article['content']
                    assistant_speaks(title)
                    ans = get_audio()
                    if 'continue' in ans:
                        continue
                    elif 'stop' in ans:
                        assistant_speaks('I will read the article content')
                        assistant_speaks(content)
                        assistant_speaks('I can open the webpage which contains the article source. Do you want me'
                                         ' to do that? ')
                        ans = get_audio()
                        sub_resp, sub_intent = chatbot_response(ans)
                        if sub_intent == 'yes':
                            driver = webdriver.Firefox()
                            driver.implicitly_wait(1)
                            driver.maximize_window()
                            driver.get(url)
                        elif sub_intent == 'no':
                            assistant_speaks('would you like me to continue reading the next articles?')
                            ans = get_audio()
                            sub_resp, sub_intent = chatbot_response(ans)
                            if sub_intent == 'yes':
                                return
                            elif sub_intent == 'no':
                                assistant_speaks('If you want to find out more, just let me know')
                                break
                    elif 'exit' in ans:
                        break
    except Exception as e:
        print(e)
        assistant_speaks("I don't understand, Can you please repeat?")
        ans = get_audio()


def create_event(service, start_time_str, summary, duration=1, description=None, location=None):
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Europe/Bucharest',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Europe/Bucharest',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return service.events().insert(calendarId='primary', body=event).execute()
