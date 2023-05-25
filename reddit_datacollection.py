import json
import praw
from dotenv import load_dotenv

subreddits = ['austria', 'de', 'linz', 'graz', 'wien', 'wirklichgutefrage', 'dezwo', 'fragreddit', 'politikwirtschaft']
keywords = [
    'klimakrise',
    'klimakatastrophe',
    'klimawandel',
    'klimakleber',
    'letzte generation',
    'erderwärmung',
    'umwelt',
    'klima',
    'letztegeneration',
    'last generation',
    'lastgeneration',
]


load_dotenv()
reddit = praw.Reddit()


def check_post(title, text):
    for keyword in keywords:
        if keyword in title.lower():
            return True
        if keyword in text.lower():
            return True
    return False


def get_author(entry):
    try:
        data = {
            'name': entry.author.name,
            'id': entry.author.id,
        }
        return data
    except:
        return None


def get_comments(comments):
    comments.replace_more(limit=None)
    posts = []
    for comment in comments:
        data = {
            'id': comment.id,
            'text': comment.body,
            'created': comment.created_utc,
            'permalink': comment.permalink,
            'author': get_author(comment),
            'comments': get_comments(comment.replies)
        }
        posts.append(data)
    return posts


def crawl():
    posts = []
    for subreddit in subreddits:
        print('\n------------------------')
        submissions = reddit.subreddit(subreddit).new(limit=3000)
        for submission in submissions:
            if check_post(submission.title, submission.selftext):
                data = {
                    'id': submission.id,
                    'title': submission.title,
                    'text': submission.selftext,
                    'subreddit': subreddit,
                    'created': submission.created_utc,
                    'permalink': submission.permalink,
                    'url': submission.url,
                    'author': get_author(submission),
                    'comments': get_comments(submission.comments)
                }
                posts.append(data)
        print(f'r/{subreddit}')
        print(f'found {len(posts)} submissions')
    with open('reddit_data.json', 'w') as f:
        json.dump(posts, f)


if __name__ == '__main__':
    crawl()
