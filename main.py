import telebot
import sqlalchemy
from telebot import types
import database as db
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('api_key')
i = 2
bot = telebot.TeleBot(api_key)

db.initDB()
db.addToDB('start')
print(db.getAllId())

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я бот по оцениванию и публикации рисунков с хомячками", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global i
    if message.text == 'Начать':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Опубликовать рисунок')
        btn2 = types.KeyboardButton('Оценивать рисунки')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'Выберите интуресующий вас вариант : ', reply_markup=markup)
    elif message.text == 'Опубликовать рисунок':
        bot.send_message(message.from_user.id, 'Отправьте вашего хамстера!')
    elif message.text == 'Оценивать рисунки':
        bot.send_message(message.from_user.id, i)
        print(db.selectFromDB(i))
        bot.send_photo(message.from_user.id, open(os.path.join(db.selectFromDB(i)[0][1]), 'rb'))
        if max(db.getAllId()) > i+1:
            i += 1
    else:
        pass

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.photo:
        #os.makedirs('pics', exist_ok=True)
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        save_path = 'pics/photo' + str(max(db.getAllId())) + '.jpg'
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        db.addToDB(save_path)
        bot.reply_to(message, 'Фотография сохранена.')

bot.polling(none_stop=True, interval=0)