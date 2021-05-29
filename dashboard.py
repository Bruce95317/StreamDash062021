import streamlit as st
import pandas as pd
import numpy as np
import tweepy
import requests
import config

auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY,
                           config.TWITTER_CONSUMER_SECRET)
auth.set_access_token(config.TWITTER_ACCESS_TOKEN,
                      config.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

option = st.sidebar.selectbox("Which Dashbboard", ('twitter',
                                                   'wallstreetbets', 'stocktwits', 'chart', 'pattern'))

st.header(option)

if option == 'twitter':
    for username in config.TWITTER_USERNAMES:
        user = api.get_user(username)
        tweets = api.user_timeline(username)

        st.image(user.profile_image_url)

        for tweet in tweets:
            if '$' in tweet.text:
                words = tweet.text.split(' ')
                for word in words:
                    if word.startswith('$') and word[1:].isalpha():
                        symbol = word[1:]
                        st.write(symbol)
                        st.write(tweet.text)
                        st.image(
                            f"https://charts2.finviz.com/chart.ashx?t={symbol}")


if option == 'chart':
    st.subheader('this is the chart dashboard')

if option == 'stocktwits':
    symbol = st.sidebar.text_input("Symbol", value='AAPL', max_chars=5,
                                   key=None, type='default', help=None)
    # st.subheader('stocktwits')
    r = requests.get(
        f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")

    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])
