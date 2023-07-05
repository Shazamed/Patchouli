from dotenv import load_dotenv
import os
import random
import praw

load_dotenv()
REDDIT_TOKEN = os.getenv('REDDIT_SECRET')
REDDIT_ID = os.getenv('REDDIT_ID')


async def reddit(subreddit, nsfw):
    reddit = praw.Reddit(client_id=REDDIT_ID,
                         client_secret=REDDIT_TOKEN,
                         user_agent="discord:patchouli:v1.0.0 (by u/DarthGL)",
                         check_for_async=False)
    if reddit.subreddit(subreddit).over18 is True and nsfw is False:
        return 'This is not a NSFW channel!\nBonk! Go to horny jail'
    submissionList = reddit.subreddit(subreddit).hot()
    submission = submissionList
    limit = random.randint(1, 10)
    for i in range(0, limit):
        submission = next(x for x in submissionList if not x.stickied)
    return submission.title + '\n' + submission.url
