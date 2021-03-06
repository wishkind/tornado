import os
import sys
import time
from datetime import datetime
import subprocess as sp
import logging
import tweepy
import pytz

# Set timezone
tz = pytz.timezone('UTC')

RTMP_URL = os.getenv('RTMP_URL')
STREAM_KEY = os.getenv('STREAM_KEY')
INPUT_FILE = os.getenv('INPUT_FILE')

TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
STREAM_URL = os.getenv('STREAM_URL')

# Setup tweepy
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Setup logger
log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)

def stream_siren(request):
    """Streams siren video to Twitch
    """
    # Check if first Wednesday of the month
    today = datetime.today().astimezone(tz)
    if today.weekday() == 2 and today.day <= 7:
        # Tweet reminder
        log.info('Tweeting reminder...')
        try:
            date_str = today.strftime('%b %d, %Y')
            api.update_status(f'Virtual siren for {date_str} has started at {STREAM_URL}!')
        except tweepy.TweepError:
            log.warning('Could not send tweet.')

        # FFMPEG stream to RTMP server
        log.info('Starting stream...')
        sp.run([
            'ffmpeg',
            '-re',
#-re这个选项会将输入的读取速度降低到输入的本地帧速率。它对于实时输出(例如直播流)很有用
            '-i', INPUT_FILE,
            '-vcodec', 'libx264',
            '-profile:v', 'main',
            '-preset:v', 'medium',
            '-r', '30',
            '-g', '60',
            '-keyint_min', '60',
            '-sc_threshold', '0',
            '-b:v', '2500k',
            '-maxrate', '2500k',
            '-bufsize', '2500k',
            '-sws_flags', 'lanczos+accurate_rnd',
            '-b:a', '96k',
            '-ar', '48000',
            '-ac', '2',
            '-f', 'flv',
            os.path.join(RTMP_URL, STREAM_KEY),
        ])

