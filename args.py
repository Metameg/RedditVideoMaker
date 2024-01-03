import sys
import argparse

# Help Message
help = "This tool is used to generate a video clip with a background video and AI generated \
        text-to-speech audio overlay. You will have to add your mp4's to the background_videos \
        directory."
# Initialize parser
parser = argparse.ArgumentParser(description=help)
 
# Adding optional argument
parser.add_argument("-tf", "--textfile", help = "Path to text file used for text-to-speech generation.")
parser.add_argument("-t", "--title", help = "Title of the post that will be displayed in the opening banner of the video. \
                                             Be sure this value is surrounded with double quotes.")
parser.add_argument("-p", "--posts", help="Number of posts to scrape.", type=int)
parser.add_argument("-s", "--subreddit", help="Subreddit to scrape from. Defaults to 'confessions'.") 
parser.add_argument("-v", "--voice",
                     help="Which AI voice will read the story. Defaults to Matthew. \
                           List of compatible voices: 'Matthew', 'Ivy', 'Joanna', \
                            'Kendra', 'Kimberly', 'Salli', 'Joey', 'Justin', 'Kevin', 'Ruth', 'Stephen'") 
parser.add_argument("-f", "--filter", help="Filter for the reddit scraper. Either 'hot' or 'rising'")
parser.add_argument("-mn", "--min", help="Minimum number of characters in reddit story.", type=int)
parser.add_argument("-mx", "--max", help="Maximum number of characters in reddit story.", type=int)

# Read arguments from command line
args = parser.parse_args()

def get_subreditt():
    arg = args.subreddit
    if arg:
            return arg
    else:
        print("No subreddit given. Using custom text. If no custom text provided, using r/confessions.")
        return "confessions"

def get_num_posts():
    if not args.posts:
        return 1
    elif args.posts and args.posts <= 20:
        return args.posts
    else:
        raise Exception("Maximum number of posts allowed is 20. Exiting.")
        

def get_text(): 
    if args.textfile:
        try:
            print("Using custom text.")
            with open(args.textfile, 'r') as text_file:
                return text_file.read()
        except Exception:
            raise Exception("Text file not found. Exiting.")
            

# def get_title(): 
#     if args.title:
#         try:
#             print("Using custom title.")
#             with open(args.textfile, 'r') as text_file:
#                 return text_file.read()
#         except Exception:
#             raise Exception("Text file not found. Exiting.")
#     if not args.title and args.textfile:
#         print("Warning: Title will be blank. Use -t or --title to use a title in the banner of the video.")
#     if args.title:
#         print("Using custom title.")
#         return args.title

def get_voice():
    compatible_voices = ['Matthew', 'Ivy', 'Joanna', 'Kendra', 'Kimberly', 'Salli', 'Joey', 'Justin', 'Kevin', 'Ruth', 'Stephen']
    if args.voice in compatible_voices:
        print(f'Using {args.voice} AI voice.')
        return args.voice
    else:
        print("Un-recognized voice. Using Matthew.")
        return 'Matthew'
            
def get_filter():
    filters = ['hot', 'rising']
    if args.filter in filters:
        print(f'Using {args.filter} reddit filter.')
        return args.filter
    else:
        print("Un-recognized filter. Using 'hot'.")
        return 'hot'
    
def get_min_charlimit():
    if args.min and args.min >= 300:
        return args.min
    elif args.min and args.min < 300:
        print("Min char limit should be at least 300.")
        sys.exit()
    else:
        return 1300

def get_max_charlimit():
    if args.max and args.max <= 4000:
        return args.max
    elif args.min and args.min > 4000:
        print("Min char limit should be no more than 4000.")
        sys.exit()
    else:
        return 3000

