import os
import sys
import args
import utils
from Creatomate import Creatomate
from Reddit import RedditScraper
from Editor import Audio, Video, Renderer
from gpt import GPT

# add shotstack provider filter
# add all-time to filter arg
# integrate char limits into gpt
# change the title of custom stories to be the first sentence of the story (GPT generated)


# Get arguments from command line
text = args.get_text()
title = args.get_title()
subreddit = args.get_subreditt()
num_posts = args.get_num_posts()
voice = args.get_voice()
filter = args.get_filter()
min_charlimit = args.get_min_charlimit()
max_charlimit = args.get_max_charlimit()


# Read Configuration File
settings = utils.read_config()

# Obtain posts from Reddit Scraper
scraper = RedditScraper()

# Scrape posts if input text file is not provided, otherwise set posts to a dummy post
if text is None:
    posts = scraper.scrape_posts(num_posts, subreddit, filter, min_charlimit, max_charlimit)
    if len(posts) == 0:
        print("No posts found on this subreddit. Exiting.")
        sys.exit()
else:
    posts = [scraper.get_dummy_submission(title, text)]

audio_url = "https://api.shotstack.io/create/stage/assets/"
audio_headers = {'content-type': 'application/json',
                 'x-api-key': settings['shotstack']['x-api-key']
                }

# Build mp3s from text-to-speech API 
audio_queue = []
post_titles = []

for i, post in enumerate(posts, 1):
    if title is not None:
        post.title = title
    if text is not None:
        post.selftext = text
    
    print (post.selftext)
    # Re-write story using chat-gpt
    gpt = GPT(post.selftext, post.title)
    post.selftext = gpt.recreate_story()
    post.title = gpt.recreate_title()
    post.selftext = post.title + post.selftext
    post_titles.append(post.title)
    print(f'rendering audio ({i}/{len(posts)})...')
    seg_queue = utils.build_audio_segment_queue(post, voice, i)
      
    Audio.render(seg_queue, i)
    audio = Audio(f'./temp/audios/audio{i}.mp3', f'./temp/audios/audio{i}.mp3')
    audio_queue.append(audio)

# Build video queue
video_queue = utils.build_video_queue()
Video.compile_segments(audio_queue, video_queue)
    
# Render final mp4s
placeholder = 1
while(len(audio_queue) > 0):
    renderer = Renderer(audio_queue.pop(0), outfile=f'./output_vids/out{placeholder}.mp4')
    renderer.render()
    placeholder += 1

# Post to Creatomate
creatomate = Creatomate()
creatomate.post(post_titles)

# Clean ouput_vids directory
output_vids = os.listdir('./output_vids')
for vid in output_vids:
    os.remove(f'./output_vids/{vid}')




