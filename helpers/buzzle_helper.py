import base64
import aiohttp
import bs4
import requests
from urllib.parse import quote
import datetime
import re
import pandas
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import dateutil
from helpers import db_helper

async def a1z26_e(text):  # a1z26 cipher
    output_text = f"Encoding {text}:\n"
    if all(character.isalpha() or character.isspace() for character in text):  # if encoding
        for characterA1Z26 in text.upper():
            if characterA1Z26 == ' ':
                output_text += '/ '
            elif characterA1Z26 == '\n':
                output_text += '\n'
            else:
                output_text += str(ord(characterA1Z26) - 64).lower() + " "
    return output_text

async def a1z26_d(text):
    output_text = f"Decoding {text}:\n"
    if all(character.isdecimal() or character.isspace() for character in text):  # if decoding
        for numberA1Z26 in text.split():  # split the text by spaces
            output_text += chr(((int(numberA1Z26) - 1) % 26 + 65)).lower()  # a1z26 to ASCII then to char
    return output_text


def caesar(text, shift):
    output_text = f"Shifting {text} by {shift}:"
    if not (shift.isdecimal() or shift.lower() == "all"):
        return "\nThere is something wrong with the shift value. Please only type in a number or 'all' in the shift " \
               "field"
    if shift.isdecimal():
        output_text += "\n"
        for char in text:
            if 64 < ord(char) < 91 or 96 < ord(char) < 123:
                if 64 < ord(char) < 91:
                    base_index = 65
                else:
                    base_index = 97
                output_text += chr((ord(char) + int(shift) - base_index) % 26 + base_index)
            else:
                output_text += char
    else:
        for shift in range(0, 26):
            output_text += f'\nROT-{shift}: '
            for char in text:
                if 64 < ord(char) < 91 or 96 < ord(char) < 123:
                    if 64 < ord(char) < 91:
                        base_index = 65
                    else:
                        base_index = 97
                    output_text += chr((ord(char) + int(shift) - base_index) % 26 + base_index)
                else:
                    output_text += char
    return output_text


async def ascii_decoder(text):
    output_text = ""
    if all(character.isdecimal() or character.isspace() for character in text):
        for number in text.split():
            if len(number) == 8 and all(character == '1' or character == '0' for character in number):
                output_text += chr(int(number, 2))
            else:
                output_text += chr(int(number))
    elif text[0] == '+' and all(character.isalnum() or character.isspace() for character in text[1:]) and len(
            text) != 1:
        for number in text[1:].split():
            output_text += chr(int(number, 16))
    else:
        for character1 in text:
            output_text += ord(character1) + ' '
        for character2 in text:
            output_text = '{0:08b} '.format(ord(character2))

    return output_text


async def morse(text, direction):
    output_text = ""
    morse_dict = {
        "a": ".-", "b": "-...", "c": "-.-.",
        "d": "-..", "e": ".", "f": "..-.",
        "g": "--.", "h": "....", "i": "..",
        "j": ".---", "k": "-.-", "l": ".-..",
        "m": "--", "n": "-.", "o": "---",
        "p": ".--.", "q": "--.-", "r": ".-.",
        "s": "...", "t": "-", "u": "..-",
        "v": "..._", "w": ".--", "x": "-..-",
        "y": "-.--", "z": "--..", "1": ".----",
        "2": "..---", "3": "...--", "4": "....-",
        "5": ".....", "6": "-....", "7": "--...",
        "8": "---..", "9": "----.", "0": "-----"
    }
    text = text.replace('–', '-')
    text = text.replace('/', ' ')
    if direction == 'd':
        if all(character in ['.', '-', ' ', '/'] for character in text):
            output_text += f"Decoding {text}:\n"
            for sequence in text.split():
                for morse_char, morse_sequence in morse_dict.items():
                    if morse_sequence == sequence:
                        output_text += morse_char.upper()
        else:
            return "Invalid format for decoding"
    elif direction == 'e':
        if all(character.isalnum() or character.isspace() for character in text):
            output_text += f"Encoding {text}:\n"
            for morse_char in text.lower():
                if morse_dict.get(morse_char) is not None:
                    output_text += morse_dict.get(morse_char) + "\t"
        else:
            return "Invalid format for encoding, use alphanumerical characters only"

    return output_text


async def vigenere(text, key, direction):
    output_text = ""
    if direction == 'e' and key.isalpha():
        direction = 1  # direction = 1 for encoding and -1 for decoding
        output_text += "Encoding "
    elif direction == 'd' and key.isalpha():
        direction = -1  # direction = 1 for encoding and -1 for decoding
        output_text += "Decoding "
    else:
        return "Key must only contain alphabetical characters"
    output_text += f"text: '{text}' with key: '{key}'\n"
    j = 0
    for i in range(len(text)):
        if text[i].isalpha():
            output_text += chr(((ord(text[i].upper()) - 65 + direction * ord(key[j % len(key)].upper()) - 65) % 26) + 65)
            j += 1
        else:
            output_text += text[i]
    return output_text


async def b64(text, direction):
    if direction == 'e':
        text_bytes = text.encode()
        text_b64_bytes = base64.b64encode(text_bytes)
        return text_b64_bytes.decode()
    else:
        text_b64_bytes = text.encode()
        text_bytes = base64.b64decode(text_b64_bytes)
        return text_bytes.decode()


async def freq(text):
    freq_dict = {}
    freq_list = []
    for character in text.upper():
        freq_dict.setdefault(character, 0)
        freq_dict[character] += 1
    freq_dict.pop('\n', None)
    for characterType, characterCount in freq_dict.items():
        freq_list.append(f'"{characterType}": {characterCount}')
    freq_list.sort()
    output_text = '\n'.join(freq_list)
    return output_text


async def nutrimatic(text):
    text = quote(text)
    nutrimatic_url = f'https://nutrimatic.org/?q={text}&go=Go'
    output_text = nutrimatic_url
    async with aiohttp.ClientSession() as session:
        async with session.get(nutrimatic_url) as resp:
            if resp.status != 200:
                return "Error retrieving info!"
            content = await resp.text()
            soup = bs4.BeautifulSoup(content, 'html.parser')
            if len(soup.find_all('span')) == 0:
                elems_error = soup.select('body > p > b > font')
                output_text += f"\n{elems_error[0].text.strip()}"
            for elements in range(2, min(22, 2 * len(soup.find_all('span')) + 1), 2):
                elems = soup.select(f'body > span:nth-child({elements})')
                elems_font = soup.find_all('span')[int(elements / 2 - 1)]
                font_size = elems_font['style']
                print(font_size[11:-2])
                if float(font_size[11:-2]) > 2.5:
                    output_text += '\n**' + elems[0].text.strip() + '**'
                else:
                    output_text += "\n" + elems[0].text.strip()
    return output_text


async def calendar():
    cal_url = "http://puzzlehuntcalendar.com/"
    output_text = cal_url
    async with aiohttp.ClientSession() as session:
        async with session.get(cal_url) as resp:
            if resp.status != 200:
                return "Error retrieving info!"
            content = await resp.text()
    soup = bs4.BeautifulSoup(content, 'html.parser')
    date_list = soup.find_all("div", {"class": "date"})
    title_list = soup.find_all("span", {"class": "title"})
    desc_list = soup.find_all("div", {"class": "description"})

    for num in range(0, min(len(date_list), 10)):
        if desc_list[num].a is not None:
            site_url = desc_list[num].a['href']
            output_text += f'\n**{title_list[num].text}**: {date_list[num].text}\n<{site_url}>'
        else:
            output_text += f'\n**{title_list[num].text}**: {date_list[num].text}'
    return output_text



async def hexadecimal(text, direction):
    output_text = ""
    if direction == 'e':
        for number in text.split():
            if number.isdecimal():
                output_text += format(int(number), 'x')
            else:
                return 'Text must be decimal'
    elif direction == 'd':
        for number in text.split():
            output_text += str(int(number, 16))
    else:
        return 'Something is wrong with the command arguments, use ", " to separate arguments'
    return output_text


async def reverse(text):
    return text[::-1]


async def braille(text, direction):
    braille_dict = {
        'a': '⠁', 'b': '⠃', 'c': '⠉',
        'd': '⠙', 'e': '⠑', 'f': '⠋',
        'g': '⠛', 'h': '⠓', 'i': '⠊',
        'j': '⠚', 'k': '⠅', 'l': '⠇',
        'm': '⠍', 'n': '⠝', 'o': '⠕',
        'p': '⠏', 'q': '⠟', 'r': '⠗',
        's': '⠎', 't': '⠞', 'u': '⠥',
        'v': '⠧', 'w': '⠺', 'x': '⠭',
        'y': '⠽', 'z': '⠵', ' ': '⠀'
    }
    braille_dots_dict = {
        'a': '100000', 'b': '101000', 'c': '110000',
        'd': '110100', 'e': '100100', 'f': '111000',
        'g': '111100', 'h': '101100', 'i': '011000',
        'j': '011100', 'k': '100010', 'l': '101010',
        'm': '110010', 'n': '110110', 'o': '100110',
        'p': '111010', 'q': '111110', 'r': '101110',
        's': '011010', 't': '011110', 'u': '100011',
        'v': '101011', 'w': '011101', 'x': '110011',
        'y': '110111', 'z': '100111', ' ': '/'
    }
    output_text = ""
    if direction == 'd':
    # if all(character in ['1', '0', ' ', '/'] for character in text) and len(text) > 5:
        for braille_sequence in text.split():
            for braille_character, braille_dot in braille_dots_dict.items():
                if braille_sequence == braille_dot:
                    output_text += braille_character
    else:
        for character in text.lower():
            if braille_dict.get(character) is not None:
                output_text += braille_dict.get(character)
        output_text += '\n'
        for character in text.lower():
            if braille_dict.get(character) is not None:
                output_text += braille_dots_dict.get(character) + ' '
    return output_text


def atbash(text):
    atbashList = []
    for character in text.upper():
        if character.isalpha():
            atbashList.append(chr(90 - ord(character) + 65))
        else:
            atbashList.append(character)
    atbashFinal = ''.join(atbashList)
    return atbashFinal


async def qat(text):
    text = quote(text)
    qat_url = f"https://www.quinapalus.com/cgi-bin/qat?pat={text}&ent=Search&dict=0"
    output_text = qat_url
    async with aiohttp.ClientSession() as session:
        async with session.get(qat_url) as resp:
            if resp.status != 200:
                return "Error retrieving data"
            content = await resp.text()
    soup = bs4.BeautifulSoup(content, 'html.parser')
    elems = soup.find_all('div', class_="in")
    results = elems[0].text.strip().split('Total solutions found:')[0]
    regex_match = re.search(r'Length(.|\n)+', results)
    if regex_match is None:
        output_text += "\nNo results found."
        return output_text
    results = regex_match.group()
    results = re.sub(r'Length (\d)+', r'**Length \1**', results)
    output_text += f'\n{results}'
    return output_text


def multi_tap(text, ):
    output_text = ""
    phone_dict = {
        'a': '2', 'b': '22', 'c': '222',
        'd': '3', 'e': '33', 'f': '333',
        'g': '4', 'h': '44', 'i': '444',
        'j': '5', 'k': '55', 'l': '555',
        'm': '6', 'n': '66', 'o': '666',
        'p': '7', 'q': '77', 'r': '777',
        's': '7777', 't': '8', 'u': '88',
        'v': '888', 'w': '9', 'x': '99',
        'y': '999', 'z': '9999'
    }
    text = text.replace('-', ' ')
    if all(character.isdecimal() or character.isspace() for character in text):
        for sequence in text.split():
            for phoneLetter, phoneNum in phone_dict.items():
                if phoneNum == sequence:
                    phoneList.append(phoneLetter)
        phoneFinal = ''.join(phoneList)
        return phoneFinal
    else:
        for letters in text:
            if phone_dict.get(letters) is not None:
                phoneList.append(phone_dict.get(letters))
        phoneFinal = ' '.join(phoneList)
        return phoneFinal


# def schedule_search(month, day, link):
#     timezones = {'PDT': 15, 'EST': 13, 'EDT': 12}
#     regex = fr'({month}[a-zA-Z]*|{day}) ({day}|{month}[a-zA-Z]*),? 202\d,? at \d?\d:\d\d (p|a).?m.? [a-zA-Z](s|d|m)T(\+\d)?'
#     res = requests.get(link)
#     res.raise_for_status()
#     buzzleMatch = re.search(regex, res.text, re.IGNORECASE)
#     if buzzleMatch is None:
#         return None
#     buzzle_startStr = buzzleMatch.group()
#     buzzle_startStr = buzzle_startStr.replace(',', '')
#     buzzle_start = datetime.datetime.strptime(' '.join(buzzle_startStr.split()[:-2]), '%B %d %Y at %H:%M')
#
#     buzzle_startZone = buzzle_startStr.split()[-1].upper()
#     if (buzzle_startStr.split()[-2].lower() == 'pm' or buzzle_startStr.split()[-2].lower() == 'p.m.') and buzzle_start.hour != 12:
#         buzzle_start = buzzle_start + datetime.timedelta(hours=12)
#     elif (buzzle_startStr.split()[-2].lower() == 'am' or buzzle_startStr.split()[-2].lower() == 'a.m.') and buzzle_start.hour == 12:
#         buzzle_start = buzzle_start - datetime.timedelta(hours=12)
#     if buzzle_startZone in timezones:
#         buzzle_start = buzzle_start + datetime.timedelta(hours=timezones.get(buzzle_startZone))
#     elif buzzle_startZone.startswith('GMT'):
#         if buzzle_startZone[-2] == '+':
#             buzzle_start = buzzle_start + datetime.timedelta(hours=8 - int(buzzle_startZone[-1]))
#         else:
#             buzzle_start = buzzle_start + datetime.timedelta(hours=8 + int(buzzle_startZone[-1]))
#     return buzzle_start


async def schedule_read():
    output_text = ""
    schedule_df = pandas.read_csv('./data/schedule.csv', parse_dates=['Start date'])
    schedule_df = schedule_df.sort_values(by='Start date')
    for x in range(0, len(schedule_df)):
        start_date_epoch = int(schedule_df.iloc[x, 1].to_pydatetime().timestamp())
        try:
            end_date_epoch = int(dateutil.parser.parse(schedule_df.iloc[x, 2]).timestamp())
            output_text += f'\n**{schedule_df.iloc[x, 0]}**: <t:{start_date_epoch}> to <t:{end_date_epoch}>'
        except:
            output_text += f'\n**{schedule_df.iloc[x, 0]}**: <t:{start_date_epoch}> to {schedule_df.iloc[x, 2]}'
    return output_text


async def schedule_add(scheduled):
    output_text = ""
    cal_url = 'http://puzzlehuntcalendar.com/'
    res = requests.get(cal_url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    time_elem = soup.select(f'body > div:nth-child({int(scheduled) + 2}) > div.date')
    name_elem = soup.select(f'body > div:nth-child({int(scheduled) + 2}) > span.title')
    if not name_elem:
        return "Range of index is out of bounds!"
    buzzle_name = name_elem[0].text.strip()
    buzzle_time_text = time_elem[0].text.strip()
    time_split = buzzle_time_text.removesuffix(" (recurring)").split("-")
    buzzle_start_datetime = dateutil.parser.parse(time_split[0])

    # await db_helper.insert_row(buzzle_name, buzzle_start_datetime, buzzle_start_datetime)

    if len(time_split) > 1:
        if time_split[1].isdecimal():
            buzzle_end_datetime = dateutil.parser.parse(" ".join(buzzle_time_text.split(" ")[:-1])+" "+time_split[1])
        else:
            buzzle_end_datetime = dateutil.parser.parse(time_split[1])
    else:
        buzzle_end_datetime = '???'
    
    schedule_df = pandas.read_csv('./data/schedule.csv', parse_dates=['Start date'])
    schedule_df.loc[len(schedule_df)] = [buzzle_name, buzzle_start_datetime, str(buzzle_end_datetime)]
    schedule_df.to_csv("./data/schedule.csv", index=False)
    schedule_df = schedule_df.sort_values('Start date')

    for x in range(0, len(schedule_df)):
        start_date_epoch = int(schedule_df.iloc[x, 1].to_pydatetime().timestamp())
        try:
            end_date_epoch = int(dateutil.parser.parse(schedule_df.iloc[x, 2]).timestamp())
            output_text += f'\n**{schedule_df.iloc[x, 0]}**: <t:{start_date_epoch}> to <t:{end_date_epoch}>'
        except:
            output_text += f'\n**{schedule_df.iloc[x, 0]}**: <t:{start_date_epoch}> to {schedule_df.iloc[x, 2]}'
    return output_text


async def schedule_remove():
    output_text = "Schedule:"
    schedule_df = pandas.read_csv("./data/schedule.csv", parse_dates=['Start date'])
    schedule_df = schedule_df[:-1]
    schedule_df.to_csv("./data/schedule.csv", index=False)
    schedule_df = schedule_df.sort_values('Start date')
    for x in range(0, len(schedule_df)):
        start_date_epoch = int(schedule_df.iloc[x, 1].to_pydatetime().timestamp())
        output_text += f'\n**{schedule_df.iloc[x, 0]}**: <t:{start_date_epoch}> to {schedule_df.iloc[x, 2]}'
    return output_text


async def schedule_countdown():
    output_text = ""
    time_now = int(datetime.datetime.today().replace(microsecond=0).timestamp())
    schedule_df = pandas.read_csv("./data/schedule.csv")
    if len(schedule_df) == 0:
        return 'There are no buzzles scheduled. Use /sch-add [index of hunt from /cal] to schedule a buzzle hunt'
    schedule_df = schedule_df.sort_values("Start date")
    scheduled_name = schedule_df.iloc[0, 0]
    scheduled_start = int(dateutil.parser.parse(schedule_df.iloc[0, 1]).timestamp())
    scheduled_end = schedule_df.iloc[0, 2]
    time_left = datetime.timedelta(seconds=scheduled_start - time_now)
    try:
        scheduled_end = int(dateutil.parser.parse(scheduled_end).timestamp())
    except ValueError:
        scheduled_end = False
    if time_left < datetime.timedelta(seconds=0) and scheduled_end is not False:
        # time_left = datetime.timedelta(seconds=scheduled_end - time_now)
        output_text += f'\n**Ongoing:**\nThe ongoing buzzle hunt, **{scheduled_name}**, ends <t:{scheduled_end}:R>, on <t:{scheduled_end}:F>'
        if len(schedule_df) > 1:
            scheduled_name2 = schedule_df.iloc[1, 0]
            scheduled_start2 = int(dateutil.parser.parse(schedule_df.iloc[1, 1]).timestamp())
            # time_left2 = datetime.timedelta(seconds=scheduled_start2 - time_now)
            output_text += f'\n**Next:**\nTime to the next buzzle hunt, **{scheduled_name2}**, is <t:{scheduled_start2}:R>, on <t:{scheduled_start2}:F>'
        return output_text
    else:
        return f'Time to the next buzzle hunt, **{scheduled_name}**, is <t:{scheduled_start}:R>, on <t:{scheduled_start}:F>'


def timer():
    time = datetime.datetime.today().replace(microsecond=0)
    schedule_df = pandas.read_csv("./data/schedule.csv")
    if len(schedule_df) == 0:
        return False
    schedule_df = schedule_df.sort_values("Start date")
    scheduled_time = schedule_df.iloc[0, 1]
    scheduled_time = datetime.datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M:%S')
    timeTrue = time == scheduled_time
    scheduled_end = schedule_df.iloc[0, 2]
    time_left = scheduled_time - time
    if timeTrue:
        return 'start'
    elif time_left > datetime.timedelta(hours=0):
        return False
    try:
        scheduled_end = datetime.datetime.strptime(scheduled_end, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        scheduled_end = False
    if scheduled_end is False:
        schedule_df = schedule_df.iloc[1:]
        schedule_df.to_csv("./data/schedule.csv", index=False)
    else:
        endTrue = time == scheduled_end
        time_end = scheduled_end - time
        if endTrue is True:
            schedule_df = schedule_df.iloc[1:]
            schedule_df.to_csv("./data/schedule.csv", index=False)
            return 'end'
        elif time_end < datetime.timedelta(hours=0):
            schedule_df = schedule_df.iloc[1:]
            schedule_df.to_csv("./data/schedule.csv", index=False)
    return False


def quipquip(text):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("https://quipqiup.com/")
    cipherbox = driver.find_element_by_id("ciphertext")
    button = driver.find_element_by_id("solve_button")
    cipherbox.clear()
    cipherbox.send_keys(text)
    button.click()
    time.sleep(1)
    finalText = driver.find_element_by_xpath('//*[@id="soltable"]/tbody/tr[1]/td[3]').text
    driver.quit()
    return finalText
