# Reddit Video Bot

## Intro
This bot is designed to run via the command line (Windows) or as a bash shell (macOS and Linux).
At its core, the bot will turn text into an AI generated voice over and a given background video will be split to match the length of the generated audio.
The bot relies on the shotstack API for voice rendering, but ptional services (Reddit Scraper, Creatomate, ChatGPT) can optionally be configured to work with the bot to enhance the output of the video and/or bulk render videos from multiple reddit posts.


## Requirements 
- python 3.9

## Installation 👩‍💻

1. Clone this repository
2. Run `pip install -r requirements.txt`

**Note** - Either create a config.toml and reference sample_config.toml or rename sample_config.toml to config.toml

**\*Required - Shotstack**
   1. Visit https://auth.shotstack.io/ and signup to get a free API-KEY
   2. Insert API KEY into ShotStack section of config.toml (make sure this is the production API-KEY and not the staging).
      
**\*Optional - Reddit App**
   This is needed if you want to scrape Reddit for stories instead of manually entering them into the bot
   
   1. Visit [the Reddit Apps page.](https://www.reddit.com/prefs/apps), and make a Reddit App account
      1.  Select 'are you a developer, create an app' button.
      2.  Create app as a "script".
      3.  Paste any URL in redirect URI. Ex:google.com

   2. Insert credentials into Reddit section of config.toml
   

**\*Optional - AWS S3 Bucket**
   This is needed if you want to upload your videos to Creatomate for automatic subtitling.
   
   1. (https://aws.amazon.com/free/?all-free-tier) Create an AWS free account (credit card needed but usage limits will stay in free tier)
   2. (https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) Follow the 'Using the S3 console' guide4
   3. Insert credentials into Amazon section of config.toml 


**\*Optional - Creatomate (Needs AWS bucket to be configured)**
   1. (https://creatomate.com/sign-in) Create an account
   2. Insert credentials into Creatomate section of config.toml

**\*Optional - GPT**
   1. Visit https://elephas.app/blog/how-to-get-chatgpt-api-key-clh93ii2e1642073tpacu6w934j to get your api key
   2. Insert the API-KEY into GPT section of config.toml

## Usage




