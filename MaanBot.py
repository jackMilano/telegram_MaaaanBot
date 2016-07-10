import random  #
import re  # REGular EXpression
from time import sleep
import telepot  # Python framework for Telegram Bot API
from sys import argv


# If in a chat conversation somebody says the word 'man' with one or more 'a' the bot must answer with a 'man'
# with a random number of 'a'. The bot is case insensitive.


def handle(msg):
    flavor = telepot.flavor(msg)
    # pprint(msg)

    # chat message
    if flavor == 'chat':
        content_type, chat_type, chat_id = telepot.glance(msg)
        if chat_type == 'group' or chat_type == 'private':
            if content_type == 'text':
                text = msg['text']
                # text message parsing
                world_list = re.findall(regexStringPattern, text)
                prev_word = ""
                for word in world_list:
                    result = regexWordObj.match(word)
                    maan_bot_response = "ERROR"
                    # Somebody wrote the word of interest
                    if result is not None:
                        maan_bot_response = compute_response(word)
                        if prev_word == "bella":
                            maan_bot_response = "bella " + maan_bot_response + " :))"
                        else:
                            if prev_word == "ciao":
                                maan_bot_response = "ciàm" + maan_bot_response + "!!"
                        bot.sendMessage(chat_id, maan_bot_response)
                    else:
                        # we check if the word instead of 'man' is 'pullman'
                        result_pullman = regexPullmanWordObj.match(word)
                        if result_pullman is not None:
                            maan_bot_response = "il pull" + compute_response(word)
                            bot.sendMessage(chat_id, maan_bot_response)
                    prev_word = word
            elif content_type == 'left_chat_member':
                if msg['left_chat_member']['first_name'] != 'MaaanBot':
                    bot.sendMessage(chat_id, 'addio maaaaan :\'-(')
            elif content_type == 'new_chat_member':
                bot.sendMessage(chat_id, 'ciao maaaaan')
            else:
                print('content_type = ' + content_type)
        else:
            print('chat_type = ' + chat_type)

    # callback query - originated from a callback button
    elif flavor == 'callback_query':
        query_id, from_id, query_data = telepot.glance(msg, flavor=flavor)
        print('Callback query:', query_id, from_id, query_data)

    # inline query - need `/setinline`
    elif flavor == 'inline_query':
        query_id, from_id, query_string = telepot.glance(msg, flavor=flavor)
        print('Inline Query:', query_id, from_id, query_string)

        # Compose your own answers
        articles = [{'type': 'article', 'id': 'abc', 'title': 'ABC', 'message_text': 'maaaaaan!'}]

        bot.answerInlineQuery(query_id, articles)

    # chosen inline result - need `/setinlinefeedback`
    elif flavor == 'chosen_inline_result':
        result_id, from_id, query_string = telepot.glance(msg, flavor=flavor)
        print('Chosen Inline Result:', result_id, from_id, query_string)
        # Remember the chosen answer to do better next time

    else:
        raise telepot.BadFlavor(msg)


def compute_response(word):
    maan_bot_response = 'm'
    # The random number of 'a' is calculated
    a_num = 0
    word_chars = list(word.lower())
    for letter in word_chars:
        if letter == 'a':
            a_num += 1
    a_num_min = a_num + 2
    a_num_max = int(max(3, 2 * a_num))
    if a_num_min > a_num_max:
        tmp = a_num_min
        a_num_min = a_num_max
        a_num_max = tmp
    a_num_random = random.randint(a_num_min, a_num_max)
    for x in range(0, a_num_random):
        maan_bot_response += 'a'
    maan_bot_response += 'n'
    return maan_bot_response


# The token has to be passed from command line because it has to be kept secret.
TOKEN = argv[1]

# Regex setup
regexStringPattern = r"[\w']+"
# regexCompleteWordPattern = r"^.*ma+n$"
regexWordPattern = r"^ma+n$"
regexPullmanPattern = r"^(pull)?ma+n$"
regexWordObj = re.compile(regexWordPattern, re.IGNORECASE)
regexPullmanWordObj = re.compile(regexPullmanPattern, re.IGNORECASE)

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

# Keep the program running.
while 1:
    sleep(10)
