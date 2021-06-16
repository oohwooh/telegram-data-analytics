from matplotlib.font_manager import FontProperties
import json
import datetime
import pandas
import concurrent.futures
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
import emoji
usage_data = {}
from tqdm import tqdm

with open('result.json', encoding='utf-8') as f:
    chats_data = json.load(f)['chats']['list']
for chat in tqdm(chats_data):
    if chat['type'] == ['saved_messages', 'bot_chat']:
        continue
    messages = [message for message in chat['messages'] if message.get('from_id') == 5436062408 and not message.get('forwarded_from')]
    for message in tqdm(messages):
        date = message['date'].split('T')[0]
        message = strip_extra_squiggly_bracket_stuffs(message['text'])
        emojis = emoji.emoji_lis(message)
        for e in [e['emoji'] for e in emojis]:
            if e not in usage_data:
                usage_data[e] = {}
            usage_data[e][date] = usage_data[e].get(date, 0) + 1

dataframe = pandas.DataFrame.from_dict(usage_data).sort_index()
dataframe = dataframe.fillna(0)
print(dataframe)
for e in usage_data:
    dataframe[e] = dataframe[e].rolling(window=5, min_periods=1).mean()
print(dataframe)
dataframe = dataframe.apply(lambda x: x/x.sum()*100, axis=1)
print(dataframe)
import bar_chart_race as bcr
bcr.bar_chart_race(
    df=dataframe,
    filename='emoji/tg-bar-racing_emoji.mp4',
    n_bars=5,
    interpolate_period=False,
    fixed_max=True,
    steps_per_period=1,
    label_bars=True,
    figsize=(10, 5),
    dpi=50,
    period_summary_func='',
    period_label=False,
    title='Emoji Usage',
    bar_kwargs={'alpha': 1},
    shared_fontdict= {'family': 'Segoe UI Emoji'},
    filter_column_colors=True)