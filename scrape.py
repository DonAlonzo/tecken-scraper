from bs4 import BeautifulSoup
from requests import session
import sys
import re
import moviepy.editor as mp
import pyvips

if len(sys.argv) < 2: raise Exception('Missing arguments.')

url = "https://teckensprakslexikon.su.se"
word_id = sys.argv[1];
word_url = "{}/ord/{}".format(url, word_id)
animation_file = "images/{}-animation.gif".format(word_id)
transcription_file = "images/{}-transcription.png".format(word_id)

with session() as c:
  result = c.get(word_url)

  matches = re.search("file: \"(\\/.*\\.mp4)\"", result.text)
  video_src = matches.group(1)
  video_url = "{}{}".format(url, video_src)
  clip = mp.VideoFileClip(video_url)
  clip.write_gif(animation_file, program='ffmpeg')

  page = BeautifulSoup(result.text, "lxml")
  transcription = ''.join(page.find("div", {"class": "transfont"}).contents)
  image = pyvips.Image.text(transcription, dpi=300, font="FreeSans SWL")
  image.write_to_file(transcription_file)