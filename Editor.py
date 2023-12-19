import os
import sys
import requests
from HTTP import Request
from pytube import YouTube
import ffmpeg
import utils
import ast
from io import BytesIO

class Audio():
    def __init__(self, link, outfile):
        self.link = link
        self.file_path = outfile
        self.duration = self.get_duration()
        
    @staticmethod
    def render(queue, placeholder):
        inputs = []
        for audio in queue:
            inputs.append(ffmpeg.input(audio.file_path))
        
        output_options = {
                    'hide_banner': None,
                    'loglevel': 'error'
        }
        outfile = f'./temp/audios/audio{placeholder}.mp3'
        render = ffmpeg.concat(*inputs, v=0, a=1)
        ffmpeg.output(render, outfile, **output_options).run(overwrite_output=True)

        # Clean audio sub-part files
        for i in range(len(queue)):
            os.remove(queue[i].file_path)

    @staticmethod
    def generate_cdn(text, voice):
        settings = utils.read_config()  

        # Audio request url and headers
        audio_url = "https://api.shotstack.io/create/stage/assets/"
        audio_headers = {'content-type': 'application/json',
                    'x-api-key': settings['shotstack']['x-api-key']
                    }
        audio_data = {
            "provider": "shotstack",
            "options": {
                "type": "text-to-speech",
                "text": f'''{text}''',

                "voice": f'{voice}'
            },       
        }

        # Get audio cdn from post to shotstack API
        request_audio = Request(audio_url, data=audio_data, headers=audio_headers)
        resp = request_audio.post()

        # if resp.status_code >= 200 and resp.status_code < 300:
        audio_id = str(ast.literal_eval(resp.text)["data"]["id"])
        request_audio.url += audio_id
        # else:
        #     print("Something went wrong with text to speech.")
        
        resp = Request.audio_complete_callback(request_audio)
        audio_cdn = ast.literal_eval(resp)["data"]["attributes"]["url"]

        return audio_cdn
    
    def get_duration(self):  
        if self.link != self.file_path: 
            data = self._curl_from_cdn()
            # Create audios directory inside temp folder if it doesn't already exist
            if not os.path.exists('./temp/audios'):
                os.makedirs('./temp/audios')

            # Save the raw data to a temporary file
            with open(self.file_path, 'wb') as temp_file:
                temp_file.write(data.getvalue())

        try:
            # Get information about the audio file using ffprobe
            probe = ffmpeg.probe(self.file_path)
            # Extract duration from the probe result
            duration = float(probe['format']['duration'])
            
            return duration
        
        except ffmpeg.Error as e:
            print(f"Error: {e.stderr}")
            return None
    
    def _curl_from_cdn(self):
        response = requests.get(self.link)
        audio = BytesIO(response.content)
        
        return audio
    
    
class Video():

    def __init__(self, link=None, path=None):
        self.link = link
        self.path = path
        self.segments_path = "./temp/segments"

    @staticmethod
    def compile_segments(audio_queue, video_queue):
        video_segs = os.listdir('./temp/segments')
        segs_needed = utils.get_segments_needed(audio_queue)
        init_segs = len(video_segs)

        segs_remaining = segs_needed - init_segs
        starti = 0
        while segs_remaining > 0:
            print(f'More footage needed. Attempting to cut background video...')
            print(f'Footage minutes remaining: {segs_remaining}')

            if len(video_queue) == 0:
                print(f'No videos found. Add more mp4 files to background_vids directory.\n \
                    Total footage minutes needed: {segs_needed}')
                sys.exit()

            else:
                video_obj = video_queue[0]
                print(video_obj.path)
                # Create more usable video segments
                video_obj.cut(video_obj.path, starti)

                os.remove(video_obj.path)
                del video_queue[0]
                pre_length = len(video_segs)
                video_segs = os.listdir('./temp/segments')
                post_length = len(video_segs)
                segs_remaining -= post_length - pre_length
                starti = post_length

    def cut(self, video_path, starti):
        # Get the duration of the input video
        probe = ffmpeg.probe(video_path)
        duration = float(probe['format']['duration'])

        # Set the segment duration to 1 minute (60 seconds)
        segment_duration = 60

        # Calculate the number of segments
        num_segments = int(duration / segment_duration)

        # Create segments directory inside temp folder if it doesn't already exist
        if not os.path.exists(self.segments_path):
            os.makedirs(self.segments_path)

        # Cut the video into segments and remove audio
        for i in range(num_segments):
            p = starti + i
            start_time = i * segment_duration
            output_file = os.path.join(self.segments_path, f'segment_{p+1}.mp4')
            
            print(f'Splitting video segment ({i+1}/{num_segments})...')

            output_options = {
                't': segment_duration,
                'an': None,
                'hide_banner': None,
                'loglevel': 'error'
            }
            input_stream = ffmpeg.input(video_path, ss=start_time)
            ffmpeg.output(input_stream, output_file, **output_options).run(overwrite_output=True)



    def download_youtube_video(self, output_path='temp'):
        def on_progress(stream, chunk, bytes_remaining):
            download_percent = int((stream.filesize-bytes_remaining)/stream.filesize*100)
            print(f'\rProgress: {download_percent} %')
            
        def on_complete(stream, file_path):
            print(f'Download complete. Video saved to {file_path}')
            self.cut("./" + output_path + "/output-video-uncut.mp4")

        youtube = YouTube(self.link,
                            on_progress_callback=on_progress, 
                            on_complete_callback=on_complete)

        # Get the highest resolution stream (mp4)
        video_stream = youtube.streams.filter(file_extension='mp4').get_highest_resolution()


        print(f"Fetching \"{video_stream.title}\"..")
        print(f"Fetching successful\n")
        print(f"Information: \n"
            f"File size: {round(video_stream.filesize * 0.000001, 2)} MegaBytes\n"
            f"Highest Resolution: {video_stream.resolution}\n"
            f"Author: {youtube.author}")
        print("Views: {:,}\n".format(youtube.views))

        print(f"Downloading video")
        
        # Download the video
        self.out_file = video_stream.download(output_path, filename="output-video-uncut.mp4")         
        
class Renderer():
    def __init__(self, audio_obj, outfile='./output_vids/out.mp4', needs_video_download=False):
        self.audio = audio_obj
        self.silent_audio_path = './temp/audios/silence.mp3'
        self.outfile = outfile
        self.needs_video_download = needs_video_download
        self.video_segments_path = os.path.join("temp", "segments")

    def render(self):

        # if self.needs_video_download:
        #     try:
        #         self.video.download_youtube_video()
        #     except Exception as e:
        #         print("f'Error: {e}'")
        #         print("\nSomething likely went wrong with downloading your video. \
        #            Consider using a video that is installed on your device. \
        #            Try and run the program again with the --video-file flag.\n \
        #            Ex. python main.py --video-path path/to/video.mp4")
        # else:
        #     self.video.cut(self.video.path)

        AUDIO_DELAY = 3
        # Get list of filenames for clips in video segments path
        clips = os.listdir(self.video_segments_path)

        # Calculate number of full 1-minute clips needed
        numfullclips = int((self.audio.duration + AUDIO_DELAY) // 60 )
        # Put the full 1 minute clips into the input array
        fullclips = [os.path.join(self.video_segments_path, clips[i]) for i in range(numfullclips)]

        # Convert the clips to ffmpeg input streams
        video_inputs = [ffmpeg.input(clip, t=60) for clip in fullclips]
        
        # Calculate how long the last clip should be and add to inputs 
        remainder_time = (self.audio.duration % 60) + AUDIO_DELAY
        remainder = ffmpeg.input(os.path.join(self.video_segments_path, clips[numfullclips]), t=remainder_time)
        video_inputs.append(remainder)

        # Add audio overlay
        audio_inputs=[]
        silent_audio = ffmpeg.input(self.silent_audio_path, t=AUDIO_DELAY)
        audio_inputs.append(silent_audio)
        text_audio = ffmpeg.input(self.audio.file_path)
        audio_inputs.append(text_audio)

        # Concatenate audio and video clips
        audio = ffmpeg.concat(*audio_inputs, v=0, a=1)
        video = ffmpeg.concat(*video_inputs, v=1, a=0)
        
        # Run the ffmpeg command
        ffmpeg.output(video, audio, self.outfile).run(overwrite_output=True)
        
        # Clean temp directory of inputs just used
        for i in range(len(video_inputs)):
            os.remove(os.path.join('temp','segments', clips[i]))
        os.remove(self.audio.file_path)
    
        print("\nRendering success! Video downloaded to output_vids directory.\n")

    
