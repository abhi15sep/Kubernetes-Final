import logging
import os
import feedparser

from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement, context, audio, current_stream

app = Flask(__name__)
ask = Ask(app, "/")
logger = logging.getLogger()
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@ask.launch
def launch():
  return chileNews()

# run my custom intent: alexa, ask Chile News the news
@ask.intent('ChileNewsIntent')
def chileNews():
  # get welcome message from template
  if request["locale"] == "es-MX":
      speech = render_template('welcome_message_es')
  else:
      speech = render_template('welcome_message_en')
  logger.debug("speech: " + speech)
  # play latest newsflash from feed
  stream_url = getTodayNews()
  return audio(speech).play(stream_url)

# function to get latest newsflash from remote feed
def getTodayNews():
  url = os.environ.get("feed_url")
  logger.debug("feed_url: " + url)
  d = feedparser.parse(url)
  audio_url = d.entries[0].media_content[0]['url']
  audio_url_https = audio_url.replace('http://','https://')
  return audio_url_https

@ask.intent('AMAZON.PauseIntent')
def pause():
  return audio('Pausing.').stop()

@ask.intent('AMAZON.ResumeIntent')
def resume():
  return audio('Resuming.').resume()

@ask.intent('AMAZON.StopIntent')
def stop():
  return audio('Stopping.').clear_queue(stop=True)

if __name__ == '__main__':
  if 'ASK_VERIFY_REQUESTS' in os.environ:
    verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
    if verify == 'false':
      app.config['ASK_VERIFY_REQUESTS'] = False
  app.run(debug=True)
