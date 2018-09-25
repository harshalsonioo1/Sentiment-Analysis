from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .forms import userinput
from secrets import Oauth_Secrets
import tweepy
from textblob import TextBlob

def index(request):
    user_input = userinput()
    return render(request, "index.html", {'input_hastag': user_input})

def analyse(request):
    user_input = userinput(request.GET or None)
    if request.GET and user_input.is_valid():
        #input_hastag = user_input.cleaned_data['q']
        input_hastag = "NASA"
        print (input_hastag)
        
        secrets = Oauth_Secrets()       #secrets imported from secrets.py
        auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
        auth.set_access_token(secrets.access_token, secrets.access_token_secret)

        api = tweepy.API(auth)
        input_hastag = "NASA"
        N = 1000                          #Number of Tweets
        Tweets = tweepy.Cursor(api.search, q= 'NASA').items(N)
        neg = 0.0
        pos = 0.0
        neg_count = 0
        neutral_count = 0
        pos_count = 0
        for tweet in Tweets:
            # print tweet.text
            blob = TextBlob(tweet.text)
            if blob.sentiment.polarity < 0:         #Negative
                neg += blob.sentiment.polarity
                neg_count += 1
            elif blob.sentiment.polarity == 0:      #Neutral
                neutral_count += 1
            else:                                   #Positive
                pos += blob.sentiment.polarity
                pos_count += 1
        # print "Total tweets",N
        # print "Positive ",float(pos_count/N)*100,"%"
        # print "Negative ",float(neg_count/N)*100,"%"
        # print "Neutral ",float(neutral_count/N)*100,"%"
        data = [['Sentiment', 'no. of tweets'],['Positive',pos_count]
                ,['Neutral',neutral_count],['Negative',neg_count]]
        
        return render(request, "result.html", {'data': data})
    return render(request, "index.html", {'input_hastag': user_input})