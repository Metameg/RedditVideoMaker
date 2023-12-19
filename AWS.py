import os
import boto3
import utils

class Bucket():
    def __init__(self):
        self.output_videos = os.listdir('./output_vids')
        
        settings = utils.read_config()

        self.bucket = settings['amazon']['bucket']
        self.session = boto3.Session(
            aws_access_key_id=settings['amazon']['aws_access_key_id'],
            aws_secret_access_key=settings['amazon']['aws_secret_access_key'],
        )

    def upload_videos(self):
        placeholder = 1
        for video in self.output_videos:
            print(f'Uploading video ({placeholder}/{len(self.output_videos)}) to Amazon S3 bucket...')
            s3 = self.session.resource('s3')
            s3.meta.client.upload_file(Filename=f'./output_vids/{video}', Bucket=self.bucket, Key=video)
            placeholder+=1