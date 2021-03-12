import random
import json
from scratch import markov_chain, generate_matrix
def strip_extra_squiggly_bracket_stuffs(message):
    # "text": [
    #    "on ",
    #    {
    #     "type": "link",
    #     "text": "speedtest.net"
    #    },
    #    " or something else?"
    if type(message) == str:
        return message
    elif type(message) == list:
        cleaned = ''
        for bit in message:
            if type(bit) == str:
                cleaned += bit
            elif type(bit) == dict:
                if 'text' in bit:
                    cleaned += bit['text']
        return cleaned
    else:
        return ''
with open('result.json', encoding='utf-8') as f:
    chats_data = json.load(f)['chats']['list']
    for chat in chats_data:
        if chat['type'] == 'saved_messages':
            continue
        messages = [strip_extra_squiggly_bracket_stuffs(message.get('text')).lower() for message in chat['messages'] if message.get('from_id') == 5436062408 and message.get('type') == 'message']
        if len(messages) > 1000:

            wordstream = []
            [wordstream.extend(message.split(" ")) for message in messages]
            print(f'Generating matrix for {chat["name"]} ({len(messages)} total messages, {len(wordstream)} total words)')
            matrix, corpus, corpus_indices = generate_matrix(wordstream)
            print(f'Matrix generated! Generating messages ({len(corpus)} unique words)')
            for i in range(25):
                message_length = random.choice([len(message.split(" ")) for message in messages])
                print('---')
                print(markov_chain(matrix=matrix, corpus=corpus, corpus_indices=corpus_indices,n=message_length*10))
            print('''
============================
''')