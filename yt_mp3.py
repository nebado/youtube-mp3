#!/usr/bin/python3

import sys, re, requests, youtube_dl

url = "https://www.youtube.com/results?search_query=programming+music"

def scrape_video(url):
  page = requests.get(url).content
  data = str(page).split(' ')
  item = '/watch?v='
  pattern = 'watch\?v=[a-zA-Z0-9]*'

  videos = []

  for line in data:
    result = line.find(item)
    
    if (result != -1):
      string = re.findall(pattern, line, flags=re.IGNORECASE)
      if len(string[0]) == 19:
        videos.append(string)

  save_file(videos)

  return videos

def save_file(videos):
  with open('list-video.txt', 'w') as txt_file:
    for video in videos:
      txt_file.write(" ".join(video) + "\n")
      
ydl_opts = {
  'format': 'bestaudio/best',
  'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
    'preferredquality': '192',
  }],
}

if __name__ == "__main__":
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    urls = scrape_video(url)

    for url in urls:
      full_url = "https://youtube.com/" + "".join(url)
      ydl.download(full_url.split())
