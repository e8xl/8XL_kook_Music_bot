import json
from khl import Bot, Message, ChannelPrivacyTypes
from khl.card import Card, CardMessage, Element, Module, Types
from datetime import datetime, timedelta
import aiohttp

with open('./config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
# 初始化一个bot，下方更新卡片消息需要
bot = Bot(token=config['token'])


# 天气 来自http://api.asilu.com/#today
async def weather(msg: Message, city: str):
    url = f'https://query.asilu.com/weather/gaode?address={city}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json_dict = json.loads(await response.text())
    current_time = datetime.now()
    cm = CardMessage()
    c1 = Card(Module.Header(
        f"已为您查询 {json_dict['forecasts'][0]['city']} 的天气，更新于 {json_dict['forecasts'][0]['reporttime']}"),
            Module.Context('力尽不知热，但惜夏日长...\n'f"当前时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"))

    # 使用datetime计算"今天"、"明天"和"后天"的日期
    today = datetime.now()
    days = ["今天", "明天", "后天"]

    c1.append(Module.Divider())

    for i, forecast in enumerate(json_dict['forecasts'][0]['casts'][:3]):
        date_str = (today + timedelta(days=i)).strftime('%Y-%m-%d')
        dayweather = forecast['dayweather']
        daytemp = forecast['daytemp']
        nighttemp = forecast['nighttemp']
        c1.append(
            Module.Section(
                f"日期: {date_str}（{days[i]}） 天气: {dayweather} 温度: {daytemp}℃~{nighttemp}℃"
            )
        )
        c1.append(Module.Divider())

    c1.append(Module.Context('天气部分来自高德，部分结果可能有出入，数据更新不及时敬请谅解'))
    cm.append(c1)
    await msg.reply(cm)
