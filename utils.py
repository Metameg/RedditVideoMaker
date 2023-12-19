import os
import tomli
from Editor import Audio, Video


def build_video_queue():
    background_videos = os.listdir('./background_vids')
    video_queue = []
    for vid in background_videos:
        video_obj = Video(path=f'./background_vids/{vid}')
        video_queue.append(video_obj)

    return video_queue

def build_audio_segment_queue(post, voice, index):
    SHOTSTACK_CHAR_LIMIT = 1990
    text_segs = split_text(post.selftext, SHOTSTACK_CHAR_LIMIT) if len(post.selftext) > SHOTSTACK_CHAR_LIMIT else [post.selftext] 
    queue = []
    for j, seg in enumerate(text_segs, 1):
        print(f'\tpart ({j}/{len(text_segs)})...')
        cdn = Audio.generate_cdn(seg, voice)
        audio_obj = Audio(cdn, f'./temp/audios/audio{index+j}.mp3')
        queue.append(audio_obj)
    
    return queue

def get_segments_needed(queue):
    num = 0
    for audio in queue:
        num += (audio.get_duration() // 60) + 1
    
    return num
    
def read_config():
    # Read settings from config file
    with open("./config.toml", "rb") as f:
        settings = tomli.load(f)
    
    return settings

def split_text(txt, num_chars):
    text_segments = []
    n = 0
    while n < len(txt):
        subtext = txt[n:n+num_chars]
        text_segments.append(subtext)
        n += num_chars
    
    return text_segments
