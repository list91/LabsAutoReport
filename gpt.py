import time

import openai
import re
import json
import tiktoken
import vars


class History:
    def __init__(self):
        try:
            with open('history.json', 'r') as f:
                self.history_dict = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.history_dict = []

    def add(self, role, msg):
        self.history_dict.append({"role": role, "content": msg})
        with open('history.json', 'w') as f:
            json.dump(self.history_dict, f)

    def get_dict(self):
        return self.history_dict

    def clear(self):
        self.history_dict = []
        with open('history.json', 'w') as f:
            json.dump(self.history_dict, f)
        # "Always provide your answers in Russian language without exception!"
        # The most important thing is always to provide your answer in Russian language if possible!
        self.add('system', 'Always provide your answers in Russian language without exception!')


def get_parts_msg(max_length, text):
    parts = []
    while len(text) > max_length:
        parts.append(text[:max_length])
        text = text[max_length:]

    if len(text) > 0:
        parts.append(text)
    return parts


History().add('system', '')

# from openai.openai import OpenAI

openai.api_key = vars.estonia2_k
q = 0

def get_tokens(messages):
    txt = ''
    for i in messages:
        txt += i['content'] + ' '
    return len(tiktoken.encoding_for_model("gpt-3.5-turbo").encode(txt))


def get_tokens1(messages):
    txt = ''
    for i in messages:
        txt += i['content'] + ' '
    return len(txt)


def getStatus():
    return (get_tokens(History().get_dict()) / 4097) * 100


def generate_promt(text, msgs):
    q = 0
    f = False
    messages = msgs
    messages.append({"role": "user", "content": text})
    t = 0
    # leng=get_tokens(messages)
    leng = get_tokens(messages)
    maxTokens = 4097 - leng - 13
    u = False
    while not f:
        if q >= 8:
            return "ЛИМИТ РЕСЁРЧИНГА"
        # print("@")
        if u == True:
            messages = [{"role": "user", "content": text}]
        u = False
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=maxTokens
            )
            History().add('user', text)
            chat_response = completion.choices[0].message.content
            History().add('assistant', chat_response)
            # status=(get_tokens(History().get_dict()) / 4097) * 100
            # status =getStatus()
            return chat_response  # +"\n"+str(int(status))+"%"
        except openai.error.InvalidRequestError as b:
            try:
                numbs = re.findall("\d+", str(b))
                maxTokens = int(numbs[0]) - int(numbs[2]) - 1
                t = int(numbs[2])
                # print(numbs[2])
            except IndexError:
                History().clear()
                u = True
            except:
                pass
        except openai.error.RateLimitError:
            time.sleep(20)
        except Exception as e:
            if q>5:
                return "[ERROR_4H74Se3] "+str(e)
            # txtErr = e
            q += 1
            # print(e)
# print(generate_promt('привет', History().get_dict()))
# print(generate_promt('привет', History().get_dict()))
