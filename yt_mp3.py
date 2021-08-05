#!/usr/bin/python3

import os, sys, re, requests, youtube_dl

def scrape_video(url):
  path_list = 'list-video.txt'
  
  if os.path.exists(path_list) and os.path.getsize(path_list) > 0:
    return read_file(path_list)

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
      txt_file.write("".join(video) + "\n")

def read_file(videos):
  videos_file = open(videos, "r")
  videos = videos_file.read().split('\n')
  return videos

if __name__ == "__main__":
  if (len(sys.argv) < 2):
    exit("Enter url search query for download")

  url = sys.argv[1]
  
  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
    }],
  }

  urls = scrape_video(url)

  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    acc = 0
    for url in urls:
      if acc > 0:
        urls.pop(0)
        save_file(urls)
        exit()

      if len(url) == 0:
        exit("Empty list")
      full_url = "https://youtube.com/" + "".join(url)
      ydl.download(full_url.split())
      acc += 1

