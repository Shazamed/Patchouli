import bs4
import requests
import random
import praw
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import selenium
from dotenv import load_dotenv
import os

load_dotenv()
REDDIT_TOKEN = os.getenv('REDDIT_SECRET')
REDDIT_ID = os.getenv('REDDIT_ID')

def stonks(ticker):
    stonksURL = f'https://www.marketwatch.com/investing/stock/{ticker}'
    stonksList = [f'<{stonksURL}>']
    res = requests.get(stonksURL)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    elems1 = soup.select(
        "#maincontent > div.region.region--intraday > div.column.column--aside > div > div.intraday__data > h2 > bg-quote")
    stonksList.append(f"\nThe price of {ticker.upper()} is ${elems1[0].text.strip()}")
    if ticker.lower() == 'gme':
        stonksList.append(':rocket: :rocket:')
    elems2 = soup.select('body > div.container.container--body > div.region.region--intraday > '
                         'div.column.column--aside > div > div.intraday__data > bg-quote > span.change--point--q > '
                         'bg-quote')
    elems3 = soup.select('body > div.container.container--body > div.region.region--intraday > '
                         'div.column.column--aside > div > div.intraday__data > bg-quote > span.change--percent--q > '
                         'bg-quote')
    stonksList.append(f'\n{elems2[0].text.strip()}  {elems3[0].text.strip()} ')
    if elems3[0].text.strip()[0] == '-':
        stonksList.append(':chart_with_downwards_trend:')
    else:
        stonksList.append(':chart_with_upwards_trend:')
    stonksFinal = ''.join(stonksList)
    return stonksFinal


def cbt():
    cbtText = ['''Cock and ball torture (CBT), is a sexual activity involving application of pain or constriction to 
the penis or testicles. This may involve directly painful activities, such as genital piercing, wax play, 
genital spanking, squeezing, ball-busting, genital flogging, urethral play, tickle torture, 
erotic electrostimulation, kneeing or kicking. The recipient of such activities may receive direct physical 
pleasure via masochism, or emotional pleasure through erotic humiliation, or knowledge that the play is pleasing 
to a sadistic dominant. Many of these practices carry significant health risks.''',
               '''Cog and barque torture (CBT) is a naval activity involving transportation of troops or landing to 
the enemy country. This may involve directly painful activities, such as building galleys, 
fighting the English navy, taking naval or maritime ideas, protecting trade with light ships or even 
attempting to understand naval combat. The recipient of such activities may receive direct physical 
pleasure via masochism, or emotional pleasure through erotic humiliation, or knowledge that the play 
is pleasing to a sadistic dominant. Many of these practices carry significant bankruptcy risks. ''',
               '''Combat (CBT) Medic, is a National Service vocation responsible for delivering responsive
and professional care to soldiers in need of medical attention. This may involve directly 
painful activities, such as tying bandages, dispensing medicine, taking temperature, 
performing intravenous infusions, chest compressions, carrying casulties or even administering the 
Covid-19 vaccine. The recipient of such activities may receive direct physical pleasure via masochism, 
or emotional pleasure through erotic humiliation, or knowledge that the play is pleasing to a sadistic dominant. Many of 
these practices carry significant depression risks.''',
               '''Cognitive behavioral therapy (CBT) is a psycho-social intervention that aims to improve 
mental health. CBT focuses on challenging and changing cognitive distortions (e.g. thoughts, 
beliefs, and attitudes) and behaviors, improving emotional regulation, and the development of 
personal coping strategies that target solving current problems. Originally, it was designed to treat 
depression, but its uses have been expanded to include treatment of a number of mental health 
conditions, including anxiety. CBT includes a number of cognitive or behavior psychotherapies 
that treat defined psychopathologies using evidence-based techniques and strategies.''',
               '''Chicken and ball ToriQ (CBT) is a meal involving chicken and ball. This may involve directly purchasing sticks, such as chicken, or ball. The recipient of such ToriQ may receive direct physical 
pleasure via satiation, or emotional pleasure through attaining self-actualisation, or knowledge that the ToriQ is pleasing 
to a sated recipient. Many of these practices carry insignificant financial risks.'''
               ]
    return random.choice(cbtText)


def reddit(subreddit, nsfw):
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


def proxy(URL):
    path = "./data/screenshots/proxy_ss.png"
    try:
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(URL)
        elem = driver.find_element_by_tag_name("body")
        elem.screenshot(path)
        driver.quit()
        return True
    except selenium.common.exceptions.InvalidArgumentException:
        return False
