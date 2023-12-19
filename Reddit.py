import praw
import sys
import utils

class RedditScraper():
    
    def __init__(self):
        settings = utils.read_config()
        client_id = settings['reddit']['client_id']
        secret = settings['reddit']['secret']
        user_agent = settings['reddit']['user_agent']
        self.reddit = praw.Reddit(client_id=client_id, client_secret=secret, user_agent=user_agent)
        self.dummy_submission = praw.Reddit.submission(self.reddit, id='15q3rso')

    def scrape_posts(self, num_posts, sub, filter, min_charlimit=1300, max_charlimit=2500):
        posts = []
        try: 
            if filter == 'hot':
                filtered_posts = self.reddit.subreddit(sub).hot(limit=300)
            elif filter == 'rising':
                filtered_posts = self.reddit.subreddit(sub).rising(limit=300)

            for post in filtered_posts: 
                if  len(post.selftext) >= min_charlimit and \
                    len(post.selftext) < max_charlimit and \
                    not post.over_18:
                    
                    posts.append(post)

                    if len(posts) == num_posts:
                        break

        except Exception:
            print(f'Subreddit {sub} not found. Exiting.')
            sys.exit()
        
        return posts
    
    def get_dummy_submission(self, title, text):
        self.dummy_submission.title = title
        self.dummy_submission.selftext = text

        return self.dummy_submission


