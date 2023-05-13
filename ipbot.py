from turtle import title
import telebot
import requests
import re, math
from bs4 import BeautifulSoup

def result(roll):
    url = f'http://127.0.0.1:8000/result/{roll}/'
    d = requests.get(url)
    
    status = d.status_code
    if status == 404:
        return "No result found"
    s = d.json()
    semester = s["semester"]
    
    totalMarks = 0
    totalSubMarks = 0
    
    marks = ""
    for i in semester:
        apiTotal = semester[i]["total"]
        apiMarks = semester[i]["marks"]
        subLength = len(apiMarks)
        totalSubMarks += subLength
        apiPercent = semester[i]["percentage"]
        totalMarks += apiTotal
        marks += f"""SPLITSemester {i}\n\nTotal Marks - {apiTotal}\nPercentage - {apiPercent:.2f}%"""
    
    marks += f"SPLITFor detailed result,\nvisit {url}\n\n[Link Not Activate Yet (because not hosted on production server)]\n\nClick /notice for IPU notices."
    
    data = f"""Name - {s["name"].title()}\nBatch - {s["batch"]}\nEnrollment No. - {s["enrollment"]}\nInstitute - {s["institution"].title()}\n\nTotal Marks - {totalMarks}\nPercentage - {(totalMarks / totalSubMarks):.2f}%"""
    data += marks
    
    return data

def notice():
    URL = 'http://ggsipu.ac.in/ExamResults/ExamResultsmain.htm'
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    table_body=soup.find('tbody')
    # tr = table_body.find_all('tr')[:-1]
    tr = table_body.find_all('tr')[:10]
    return tr

TOKEN = "1426966987:AAEM7ENyw3guZcpeO2CCZD1auEtaQNXZr_Y"

bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Enter enrollment number to fetch your result and /notice to fetch 10 latest IPU notices.")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Howdy, how are you doing? Enter your enrolment number to get your result.")

@bot.message_handler(commands=['notice'])
def send_welcome(message):

    notices = notice()
    u = 'http://ggsipu.ac.in/ExamResults/'
    data = ""
    for row in notices:
        cols = row.find_all('td')
        cols=[x.text.strip() for x in cols]
        title = re.sub('\s+',' ',cols[0])
        date = re.sub('\s+',' ',cols[1])
        links = row.find_all('a')
        url = ""
        for a in links:
            url = u+a['href']
        data += f"""\n{title}\n\n{url}\n\n{date}\nSPLIT"""
    
    data = data.split("SPLIT")

    for x in range(0, len(data)-1):
        bot.send_message(message.chat.id, text=data[x])
    
    bot.send_message(message.chat.id, data)

@bot.message_handler(func=lambda m: True)
def echo_all(message):

    roll = message.text
    l = len(roll)
    if (l > 11 or l < 11):
        bot.send_message(message.chat.id, text="Enter a valid Enrollment Number")
    else:
        data = result(roll)
        data = data.split("SPLIT")
        for x in range(0, len(data)):
            bot.send_message(message.chat.id, text=data[x])

bot.infinity_polling()