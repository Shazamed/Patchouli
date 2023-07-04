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


def caesar(text):
    text = text.split(', ')
    caesarList = []
    if text[0] == 'e' and len(text) == 3:
        if text[2].isdecimal():
            for character in text[1].upper():
                if 64 < ord(character) < 91:
                    caesarList.append(chr((ord(character) + int(text[2]) - 65) % 26 + 65))  # caesar cipher formula
                else:
                    caesarList.append(character)
        elif text[2].upper() == 'ALL':
            for shiftAll in range(0, 26):
                caesarList.append('ROT-' + str(shiftAll) + ': ')
                for character in text[1].upper():
                    if 64 < ord(character) < 91:
                        caesarList.append(chr((ord(character) + int(shiftAll) - 65) % 26 + 65))
                    else:
                        caesarList.append(character)
                caesarList.append('\n')
        else:
            return 'Something is wrong with the value of shift entered, type an integer or "all"'
    elif text[0] == 'd' and len(text) == 3:
        if text[2].isdecimal():
            for character in text[1].upper():
                if 64 < ord(character) < 91:
                    caesarList.append(chr((ord(character) - int(text[2]) - 65) % 26 + 65))  # caesar cipher formula
                else:
                    caesarList.append(character)
        elif text[2].upper() == 'ALL':
            for shiftAll in range(0, 26):
                caesarList.append('+' + str(shiftAll) + ': ')
                for character in text[1].upper():
                    if 64 < ord(character) < 91:
                        caesarList.append(chr((ord(character) - int(shiftAll) - 65) % 26 + 65))
                    else:
                        caesarList.append(character)
                caesarList.append('\n')
        else:
            return 'Something is wrong with the value of shift entered, type an integer or "all"'
    else:
        return 'Something is wrong with the command arguments, use ", " to separate arguments'
    caesarFinal = ''.join(caesarList)
    return caesarFinal


def ascii_decoder(text):
    asciiList = []
    if all(character.isdecimal() or character.isspace() for character in text):
        for number in text.split():
            if len(number) == 8 and all(character == '1' or character == '0' for character in number):
                asciiList.append(chr(int(number, 2)))
            else:
                asciiList.append(chr(int(number)))
    elif text[0] == '+' and all(character.isalnum() or character.isspace() for character in text[1:]) and len(
            text) != 1:
        for number in text[1:].split():
            asciiList.append(chr(int(number, 16)))
    else:
        for character1 in text:
            asciiList.append(str(ord(character1)) + ' ')
        asciiList.append('\n')
        for character2 in text:
            asciiList.append('{0:08b} '.format(ord(character2)))
    asciiFinal = ''.join(asciiList)
    return asciiFinal


def morse(text):
    morseList = []
    morseDict = {
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
    if all(character in ['.', '-', ' ', '/'] for character in text):
        for sequence in text.split():
            for characterMorse, sequenceMorse in morseDict.items():
                if sequenceMorse == sequence:
                    morseList.append(characterMorse.upper())
        morseFinal = ''.join(morseList)
    elif all(character.isalnum() or character.isspace() for character in text):
        for characterMorse in text.lower():
            if morseDict.get(characterMorse) is not None:
                morseList.append(morseDict.get(characterMorse))
        morseFinal = '  '.join(morseList)
    else:
        return "Type alpha or morse sequence in text only"

    return morseFinal


def vigenere(text):
    vigenereList = []
    text = text.split(', ')
    if len(text) == 3 and text[0] == 'e' and text[2].isalpha():
        direction = 1  # direction = 1 for encoding and -1 for decoding
    elif len(text) == 3 and text[0] == 'd' and text[2].isalpha():
        direction = -1  # direction = 1 for encoding and -1 for decoding
    else:
        return 'Something is wrong with the command arguments, use ", " to separate arguments'
    string = text[1]
    key = text[2]
    j = 0
    for i in range(len(string)):
        if string[i].isalpha():
            vigenereList.append(
                chr(((ord(string[i].upper()) - 65 + direction * ord(key[j % len(key)].upper()) - 65) % 26) + 65))
            j += 1
        else:
            vigenereList.append(string[i])
    vigenereFinal = ''.join(vigenereList)
    return vigenereFinal


def b64(text):
    text = text.split(', ')
    if len(text) == 2 and text[0] == 'e':
        textBytes = text[1].encode()
        textBase64Bytes = base64.b64encode(textBytes)
        return textBase64Bytes.decode()
    elif len(text) == 2 and text[0] == 'd':
        textBase64Bytes = text[1].encode()
        textBytes = base64.b64decode(textBase64Bytes)
        return textBytes.decode()
    else:
        return 'Something is wrong with the command arguments, use ", " to separate arguments'


def freq(text):
    freqDict = {}
    freqList = []
    for character in text.upper():
        freqDict.setdefault(character, 0)
        freqDict[character] += 1
    freqDict.pop('\n', None)
    for characterType, characterCount in freqDict.items():
        freqList.append(f'"{characterType}": {characterCount}')
    freqList.sort()
    freqFinal = '\n'.join(freqList)
    return freqFinal


async def nutrimatic(text):
    # nutrimaticList = []
    text = quote(text)
    nutrimatic_url = f'https://nutrimatic.org/?q={text}&go=Go'
    output_text = nutrimatic_url
    
    # nutrimaticList.append(nutrimaticURL)
    # res = requests.get(nutrimaticURL)
    # res.raise_for_status()
    async with aiohttp.ClientSession() as session:
        async with session.get(nutrimatic_url) as resp:
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



def hexadecimal(text):
    hexList = []
    text = text.split(', ')
    if text[0] == 'e' and len(text) == 2:
        for number in text[1].split():
            if number.isdecimal():
                hexList.append(format(int(number), 'x'))
            else:
                return 'Text must be decimal'
    elif text[0] == 'd' and len(text) == 2:
        for number in text[1].split():
            hexList.append(str(int(number, 16)))
    else:
        return 'Something is wrong with the command arguments, use ", " to separate arguments'
    hexFinal = ' '.join(hexList)
    return hexFinal


def reverse(text):
    return text[::-1]


def braille(text):
    brailleDict = {
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
    brailleDotsDict = {
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
    brailleList = []
    if all(character in ['1', '0', ' ', '/'] for character in text) and len(text) > 5:
        for brailleSequence in text.split():
            for brailleLetter, brailleDot in brailleDotsDict.items():
                if brailleSequence == brailleDot:
                    brailleList.append(brailleLetter)
    else:
        for character in text.lower():
            if brailleDict.get(character) is not None:
                brailleList.append(brailleDict.get(character))
        brailleList.append('\n')
        for character in text.lower():
            if brailleDict.get(character) is not None:
                brailleList.append(brailleDotsDict.get(character) + ' ')
    brailleFinal = ''.join(brailleList)
    return brailleFinal


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


def multi_tap(text):
    phoneList = []
    phoneDict = {
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
            for phoneLetter, phoneNum in phoneDict.items():
                if phoneNum == sequence:
                    phoneList.append(phoneLetter)
        phoneFinal = ''.join(phoneList)
        return phoneFinal
    else:
        for letters in text:
            if phoneDict.get(letters) is not None:
                phoneList.append(phoneDict.get(letters))
        phoneFinal = ' '.join(phoneList)
        return phoneFinal


def schedule_search(month, day, link):
    timezones = {'PDT': 15, 'EST': 13, 'EDT': 12}
    regex = fr'({month}[a-zA-Z]*|{day}) ({day}|{month}[a-zA-Z]*),? 202\d,? (at )?\d?\d:\d\d (p|a).?m.? [a-zA-Z](s|d|m)T(\+\d)?'
    res = requests.get(link)
    res.raise_for_status()
    buzzleMatch = re.search(regex, res.text, re.IGNORECASE)
    if buzzleMatch is None:
        return None
    buzzleTimeStr = buzzleMatch.group()
    buzzleTimeStr = buzzleTimeStr.replace(',', '')
    buzzleTime = datetime.datetime.strptime(' '.join(buzzleTimeStr.split()[:-2]), '%B %d %Y at %H:%M')
    buzzleTimeZone = buzzleTimeStr.split()[-1].upper()
    if (buzzleTimeStr.split()[-2].lower() == 'pm' or buzzleTimeStr.split()[-2].lower() == 'p.m.') and buzzleTime.hour != 12:
        buzzleTime = buzzleTime + datetime.timedelta(hours=12)
    elif (buzzleTimeStr.split()[-2].lower() == 'am' or buzzleTimeStr.split()[-2].lower() == 'a.m.') and buzzleTime.hour == 12:
        buzzleTime = buzzleTime - datetime.timedelta(hours=12)
    if buzzleTimeZone in timezones:
        buzzleTime = buzzleTime + datetime.timedelta(hours=timezones.get(buzzleTimeZone))
    elif buzzleTimeZone.startswith('GMT'):
        if buzzleTimeZone[-2] == '+':
            buzzleTime = buzzleTime + datetime.timedelta(hours=8 - int(buzzleTimeZone[-1]))
        else:
            buzzleTime = buzzleTime + datetime.timedelta(hours=8 + int(buzzleTimeZone[-1]))
    return buzzleTime


def schedule_read():
    scheduleStrList = ["Schedule:"]
    scheduleDF = pandas.read_csv('./data/schedule.csv', parse_dates=['Start date'])
    scheduleDF = scheduleDF.sort_values(by='Start date')
    for x in range(0, len(scheduleDF)):
        scheduleStrList.append(f'**{scheduleDF.iloc[x,0]}**: {scheduleDF.iloc[x,1]} to {scheduleDF.iloc[x,2]}')
    scheduleFinal = '\n'.join(scheduleStrList)
    return scheduleFinal


def schedule_add(scheduled):
    scheduleStrList = ['Schedule:']
    calURL = 'http://puzzlehuntcalendar.com/'
    res = requests.get(calURL)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    elemsTime = soup.select(f'body > div:nth-child({int(scheduled) + 2}) > div.date')
    elemsName = soup.select(f'body > div:nth-child({int(scheduled) + 2}) > span.title')
    buzzleName = elemsName[0].text.strip()
    buzzleFullTime = elemsTime[0].text.strip()
    buzzleTime = buzzleFullTime.split('-')[0]
    elemsDes = soup.find_all('div', class_='description')
    idNum = elemsDes[int(scheduled) - 1].get('id')
    if int(idNum) < 10:
        buzzleURL = soup.select(f'#\\3{idNum}  > a')[0].text.strip()
    else:
        buzzleURL = soup.select(f'#\\3{idNum[0]} {idNum[1]} > a')[0].text.strip()
    buzzleMonth = buzzleTime.split()[0]
    buzzleDay = buzzleTime.split()[1]
    buzzleDateTime = schedule_search(buzzleMonth, buzzleDay, buzzleURL)
    if buzzleDateTime is None:
        if ':' in buzzleTime:
            buzzleDateTime = datetime.datetime.strptime(buzzleTime[:-1], '%b %d %H:%M')
        else:
            buzzleDateTime = datetime.datetime.strptime(buzzleTime, '%b %d')
        if len(buzzleFullTime.split()) == 3:
            buzzleDateTime = buzzleDateTime.replace(year=int(buzzleFullTime.split()[2]))
        else:
            buzzleDateTime = buzzleDateTime.replace(year=datetime.datetime.today().year)
        buzzleDateTime = buzzleDateTime + datetime.timedelta(hours=15)
        if buzzleTime[-1] == 'p':
            buzzleDateTime = buzzleDateTime + datetime.timedelta(hours=12)
    scheduleDF = pandas.read_csv('./data/schedule.csv', parse_dates=['Start date'])
    scheduleDF.loc[len(scheduleDF)] = [buzzleName, buzzleDateTime, '???']
    scheduleDF.to_csv("./data/schedule.csv", index=False)
    scheduleDF = scheduleDF.sort_values('Start date')
    for x in range(0, len(scheduleDF.index)):
        scheduleStrList.append(f'**{scheduleDF.iloc[x,0]}**: {scheduleDF.iloc[x,1]} to {scheduleDF.iloc[x,2]}')
    scheduleFinal = '\n'.join(scheduleStrList)
    return scheduleFinal


def schedule_remove():
    scheduleStrList = ["Schedule:"]
    scheduleDF = pandas.read_csv("./data/schedule.csv", parse_dates=['Start date'])
    scheduleDF = scheduleDF[:-1]
    scheduleDF.to_csv("./data/schedule.csv", index=False)
    scheduleDF = scheduleDF.sort_values('Start date')
    for x in range(0, len(scheduleDF)):
        scheduleStrList.append(f'**{scheduleDF.iloc[x, 0]}**: {scheduleDF.iloc[x, 1]} to {scheduleDF.iloc[x, 2]}')
    scheduleFinal = '\n'.join(scheduleStrList)
    return scheduleFinal


def schedule_countdown():
    strList = []
    time = datetime.datetime.today().replace(microsecond=0)
    scheduleDF = pandas.read_csv("./data/schedule.csv")
    if len(scheduleDF) == 0:
        return 'There are no buzzles scheduled. Use !sch [list number of !cal] to schedule a buzzle hunt'
    scheduleDF = scheduleDF.sort_values("Start date")
    scheduled_name = scheduleDF.iloc[0, 0]
    scheduled_end = scheduleDF.iloc[0, 2]
    scheduled_time = datetime.datetime.strptime(scheduleDF.iloc[0, 1], '%Y-%m-%d %H:%M:%S')
    try:
        scheduled_end = datetime.datetime.strptime(scheduled_end, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        scheduled_end = False
    time_left = scheduled_time - time
    if time_left < datetime.timedelta(hours=0) and scheduled_end is not False:
        time_left = scheduled_end - time
        strList.append(
            f'**Ongoing:**\nThe ongoing buzzle hunt, {scheduled_name}, ends in {time_left}, on {scheduled_end.strftime("%A, %b %d, at %H:%M:%S")}')
        if len(scheduleDF) > 1:
            scheduled_name2 = scheduleDF.iloc[1, 0]
            scheduled_time2 = datetime.datetime.strptime(scheduleDF.iloc[1, 1], '%Y-%m-%d %H:%M:%S')
            time_left2 = scheduled_time2 - time
            strList.append(f'**Next:**\nTime to the next buzzle hunt, {scheduled_name2}, is in {time_left2}, on {scheduled_time2.strftime("%A, %b %d, at %H:%M:%S")}')
        return '\n'.join(strList)
    else:
        return f'Time to the next buzzle hunt, {scheduled_name}, is in {time_left}, on {scheduled_time.strftime("%A, %b %d, at %H:%M:%S")}'


def timer():
    time = datetime.datetime.today().replace(microsecond=0)
    scheduleDF = pandas.read_csv("./data/schedule.csv")
    if len(scheduleDF) == 0:
        return False
    scheduleDF = scheduleDF.sort_values("Start date")
    scheduled_time = scheduleDF.iloc[0, 1]
    scheduled_time = datetime.datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M:%S')
    timeTrue = time == scheduled_time
    scheduled_end = scheduleDF.iloc[0, 2]
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
        scheduleDF = scheduleDF.iloc[1:]
        scheduleDF.to_csv("./data/schedule.csv", index=False)
    else:
        endTrue = time == scheduled_end
        time_end = scheduled_end - time
        if endTrue is True:
            scheduleDF = scheduleDF.iloc[1:]
            scheduleDF.to_csv("./data/schedule.csv", index=False)
            return 'end'
        elif time_end < datetime.timedelta(hours=0):
            scheduleDF = scheduleDF.iloc[1:]
            scheduleDF.to_csv("./data/schedule.csv", index=False)
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
