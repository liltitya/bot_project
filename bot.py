import telebot
from TOKEN import token_st, admins
import requests
import os


def delete_user(chatID):
    with open('users_st.txt') as users:
        just_users = users.readlines()
    if str(chatID) + '\n' in just_users:
        just_users.remove(str(chatID) + '\n')
        with open('new_users_st.txt', 'w') as new_users:
            for i in range(len(just_users)):
                new_users.write(just_users[i])
        os.remove('users_st.txt')
        os.rename('new_users_st.txt', 'users_st.txt')
        return 1

    else:
        params = {
            'chat_id': int(chatID),
            'text': 'Ты еще не получаешь уведомления!'
        }

        requests.get(f'https://api.telegram.org/bot{token_st}/sendMessage', params=params)
        return 0


def add_user(chatId, chatUsername):
    with open('users_st.txt') as users:
        if users:
            just_users = users.readlines()
        else:
            just_users = []
    with open('dict_users.txt') as dict_users:
        if dict_users:
            dict_just_users = dict_users.readlines()
        else:
            dict_just_users = []
    users_nicknames = {}
    for user in dict_just_users:
        user = user.replace('\n', '').split(' ')
        users_nicknames[user[0]] = user[1]
    if str(chatId) not in users_nicknames:
        users_nicknames[chatId] = chatUsername
    with open('new_dict_users.txt', 'w') as new_dict:
        for chat_id, chat_username in users_nicknames.items():
            new_dict.write(str(chat_id) + ' ' + str(chat_username) + '\n')
    os.remove('dict_users.txt')
    os.rename('new_dict_users.txt', 'dict_users.txt')
    if str(chatId) + '\n' not in just_users:
        just_users.append(str(chatId) + '\n')
        with open('new_users_st.txt', 'w') as new_users:
            for i in range(len(just_users)):
                new_users.write(just_users[i])
        os.remove('users_st.txt')
        os.rename('new_users_st.txt', 'users_st.txt')
        return 1
    else:
        params = {
            'chat_id': int(chatId),
            'text': 'Ты уже получаешь уведомления!'
        }

        requests.get(f'https://api.telegram.org/bot{token_st}/sendMessage', params=params)
    return 0


bot = telebot.TeleBot(token_st)


@bot.message_handler(commands=['stop'])
def stop(message):
    if delete_user(message.chat.id):
        params = {
            'chat_id': message.chat.id,
            'text': 'Теперь ты не получишь уведомлений!'
        }

        requests.get(f'https://api.telegram.org/bot{token_st}/sendMessage', params=params)


@bot.message_handler(commands=['start'])
def start_message(message):
    if add_user(message.chat.id, message.chat.username):
        params = {
            'chat_id': message.chat.id,
            'text': 'Привет! Здесь будут появляться выгодные для тебя предложения! В этом боте первостепенным являются три банка : Сбербанк, Тинькофф, Райффайзен. Удачных сделок!'
        }

        requests.get(f'https://api.telegram.org/bot{token_st}/sendMessage', params=params)


@bot.message_handler(commands=['list'])
def list(message):
    if message.chat.id in admins:
        with open('users_st.txt') as users:
            just_users=users.readlines()
        for i in range(len(just_users)):
            just_users[i]=just_users[i].replace('\n','')
        ans=[]
        with open('dict_users.txt') as dic:
            for line in dic:
                info=line.replace('\n','').split()
                if info[0] in just_users:
                    ans.append(info[1])
        params = {
            'chat_id': message.chat.id,
            'text': '\n'.join(ans)
        }

        requests.get(f'https://api.telegram.org/bot{token_st}/sendMessage', params=params)


@bot.message_handler(content_types=['text'])
def block(message):
    if message.chat.id in admins:
        if message.text.lower()[:6]=='delete':
            username=message.text.lower()[7:]
            with open('dict_users.txt') as dict_users:
                if dict_users:
                    dict_just_users = dict_users.readlines()
                else:
                    dict_just_users = []
            users_nicknames = {}
            for user in dict_just_users:
                user = user.replace('\n', '').split(' ')
                users_nicknames[user[1]] = user[0]
            if username in users_nicknames:
                delete_user(users_nicknames[username])
                params = {
                    'chat_id': message.chat.id,
                    'text': f'{username} успешно удален'
                }

                requests.get(f'https://api.telegram.org/bot{token_st}/sendMessage', params=params)


bot.infinity_polling()


if __name__ == '__main__':
    main()
