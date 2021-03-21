import boto3
import logging
import os
import feedparser
from random import randint
from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement, context, audio, current_stream

# connect to S3
s3 = boto3.client('s3')

# create app
app = Flask(__name__)
ask = Ask(app, "/")
logger = logging.getLogger()
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

# alexa, run Jokebox
@ask.launch
def launch():
    return playRandomAudio()

@ask.intent('TellmeAJokeIntent')
def playRandomAudio():
    # get welcome message from template
    if request["locale"] == "es-MX":
        speech = render_template('welcome_message_es')
    else:
        speech = render_template('welcome_message_en')
    logger.debug("speech: " + speech)
    # play a random audio file from my S3 bucket
    stream_url = getRandomAudio(s3, logger)
    return audio(speech).play(stream_url)

@ask.intent('AMAZON.PauseIntent')
def pause():
    return audio('Ok!').stop()

@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Ok!').resume()

@ask.intent('AMAZON.StopIntent')
def stop():
    return audio('Ok!').clear_queue(stop=True)

@ask.intent('AMAZON.HelpIntent')
def resume():
    return audio('Ok!').resume()

@ask.intent('AMAZON.CancelIntent')
def resume():
    return audio('Ok!').resume()

# function to get random audio file from S3
def getRandomAudio(s3, logger):
    # get all files from our bucket
    bucket_name = os.environ.get("audio_bucket")
    logger.debug("bucket_name: " + bucket_name)
    objects = s3.list_objects(
        Bucket=bucket_name
    )
    bucket_files = objects['Contents']
    # pick a random file from our bucket
    random_index = randint(0,len(bucket_files)-1)
    logger.debug("random_index: " + str(random_index))
    random_file = bucket_files[random_index]['Key']
    logger.debug("random_file: " + random_file)
    # generate pre-signed url for our picked file
    signed_url = s3.generate_presigned_url(
        ClientMethod = "get_object",
        ExpiresIn = 60,
        Params = {
            "Bucket": bucket_name,
            "Key": random_file
        }
    )
    logger.debug("signed_url: " + signed_url)
    # finish
    return signed_url

if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
    if verify == 'false':
        app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
