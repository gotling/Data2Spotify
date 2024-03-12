# Data to Spotify
# - Utdelningsdag
# - Elpris

import os
import base64
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import locale
import time
import datetime
locale.setlocale(locale.LC_TIME, 'sv_SE.UTF-8')

from dotenv import load_dotenv
from dateparser.date import DateDataParser
import requests
import spotipy
import spotipy.util as util
import schedule

W = H = 512
background_img = "background.jpg"
icon_img = "mailbox.png"
font_file = "./LTSaeada-Medium.otf"
font_size = W / 6
icon_size = (180, 180)

load_dotenv()

token = util.prompt_for_user_token(
    username=os.environ['SPOTIPY_USER'],
    scope='playlist-modify-private,ugc-image-upload', 
    client_id=os.environ['SPOTIPY_CLIENT_ID'],
    client_secret=os.environ['SPOTIPY_CLIENT_SECRET'], 
    redirect_uri="https://127.0.0.1:9000"
)
spotify = spotipy.Spotify(auth=token)


def make_image(current, next):
    icon = Image.open(icon_img).convert("RGBA").resize(icon_size)

    with Image.open(background_img) as im:
        draw = ImageDraw.Draw(im)

        im.paste(icon, (30, 230), icon)

        # Day
        font = ImageFont.truetype(font_file, font_size)
        draw.text((W/2, 130), current.strftime('%A'), font=font, anchor="mm")

        # Weekday
        font = ImageFont.truetype(font_file, 200)
        draw.text((W/4*3-50, 320), str(current.day), font=font, anchor="mm")

        # Next
        font = ImageFont.truetype(font_file, font_size/3)
        draw.text((W/2, 450), "{} {}".format(next.strftime('%A'), str(next.day)), font=font, anchor="mm")

        # This method will show image in any image viewer
        #im.show()
        #exit()

        buffered = BytesIO()
        im.save(buffered, format="JPEG")

        return base64.b64encode(buffered.getvalue())


def date_string_to_date(text):
    day, month, year = text.split(' ')
    month = month.strip(',')

    ddp = DateDataParser(languages=['sv'])

    return ddp.get_date_data("{}-{}-{}".format(year, month, day)).date_obj


def get_postnord_delivery_days(postalCode):
    r = requests.get('https://portal.postnord.com/api/sendoutarrival/closest?postalCode={}'.format(postalCode))
    result = r.json()

    return date_string_to_date(result['delivery']), date_string_to_date(result['upcoming'])


# Create playlist
#results = spotify.user_playlist_create(os.environ['SPOTIPY_USER'], 'Utdelning', public=False)
#exit()

def job():
    print("Running..")
    current, next = get_postnord_delivery_days(os.environ['POSTAL_CODE'])
    print("Delivery day: {}".format(current.day))
    #img = make_image(current, next)

    name = f'Utdelning'
    description = 'Data 2 Spotify @ github.com/gotling ({})'.format(datetime.datetime.now().replace(microsecond=0).isoformat())

    result = spotify.playlist_change_details(os.environ['PLAYLIST_ID'], name=name, public=False, description=description)

    img = make_image(current, next)

    result = spotify.playlist_upload_cover_image(os.environ['PLAYLIST_ID'], img)

    print("Spotify playlist updated")


schedule.every().day.at("01:00").do(job)
job()

while True:
    schedule.run_pending()
    time.sleep(1)