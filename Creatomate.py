from AWS import Bucket
from HTTP import Request
import utils

class Creatomate():
    def __init__(self):
        self.bucket = Bucket()
        self.settings = utils.read_config()

        self.url = "https://api.creatomate.com/v1/renders"
        self.headers = {
            'content-type': 'application/json',
            'Authorization': self.settings['creatomate']['api_key']
        }
        
    def post(self, post_titles):
        self.bucket.upload_videos()

        for i, video in enumerate(self.bucket.output_videos, 0):
            creatomate_data = {
                "template_id": self.settings['creatomate']['template_id'],
                "modifications": {
                    "Video-1": f'https://creatomatebot.s3.us-west-2.amazonaws.com/{video}',
                    "95b8b3ee-2065-4340-8a00-3543c9736657": f'{post_titles[i]}'                
                }
            }

            creatomate_request = Request(self.url, creatomate_data, self.headers)
            print(f'Uploading video ({i+1}/{len(self.bucket.output_videos)}) to Creatomate... ')
            creatomate_request.post()