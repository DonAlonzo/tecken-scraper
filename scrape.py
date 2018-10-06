from bs4 import BeautifulSoup
from requests import session
import sys
import re
import os
import moviepy.editor as mp
from moviepy.video.fx.all import crop
import pyvips

if len(sys.argv) < 2:
  print('Missing arguments.')
  exit(1)

with session() as c:
  for word_id in sys.argv[1:]:
    url = "https://teckensprakslexikon.su.se"
    word_url = "{}/ord/{}".format(url, word_id)
    animation_file = "images/{}-animation.gif".format(word_id)
    transcription_file = "images/{}-transcription.png".format(word_id)

    result = c.get(word_url)
    matches = re.search("<source src=\"(\\/.*\\.mp4)\"", result.text)
    video_src = matches.group(1)
    video_url = "{}{}".format(url, video_src)
    clip = mp.VideoFileClip(video_url)
    
    clip = clip.resize(height=400)
    (width, height) = clip.size
    if width > 540:
      clip = crop(clip, width=540, x_center=width/2)

    fps = 25
    done = False
    while not done:
      clip.write_gif(animation_file, program='ffmpeg', fps=fps)
      if os.path.getsize(animation_file) > 7 * 1024 * 1024:
        fps = fps - 1
      else:
        done = True 


    page = BeautifulSoup(result.text, "lxml")
    transcription = ''.join(page.find("div", {"class": "transfont"}).contents)
    image = pyvips.Image.text(transcription, dpi=300, font="FreeSans SWL").invert()
    image.write_to_file(transcription_file)
