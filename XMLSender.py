from urllib.request import urlopen
from nonebot import get_bot
from hoshino import Service
from hoshino.typing import HoshinoBot, CQEvent
from quart import request
import os

try:
    import ujson as json
except ImportError:
    import json

sv = Service(name='XMLSender')
app = get_bot().server_app

host = json.load(urlopen('http://jsonip.com'))['ip']
port = get_bot().config.PORT
curr_bot = get_bot()
try:
    password = json.load(open(os.path.dirname(__file__) + '/config.json'), 'r')['password']
except IOError:
    password = '123456'
    json.dump({'password': password}, open(os.path.dirname(__file__) + '/config.json', 'w'))


@sv.on_prefix('发送XML')
async def sendXML(bot: HoshinoBot, ev: CQEvent):
    msg = ev.message.extract_plain_message()
    await bot.send(ev, f'[CQ:xml,data={msg}]')


@sv.on_fullmatch('在线发送XML')
async def sendXMLWeb(bot: HoshinoBot, ev: CQEvent):
    await bot.send(ev, f'http://{host}:{port}/XMLSender')


@sv.on_prefix('设置XML密码')
async def setPassword(bot: HoshinoBot, ev: CQEvent):
    global password
    password = ev.message.extract_plain_text()
    json.dump({'password': password}, open(os.path.dirname(__file__) + '/config.json', 'w'))

@app.route('/XMLSender', methods=['GET'])
def sendg():
    return '''
    <form action="XMLSender" method="post"><br />
        密码：<input type="text" name="psw"><br />
        群号：<input type="text" name="group"><br />
        XML：<br />
        <textarea rows="10" cols="30" name="XML"></textarea><br />
        <button type="submit">发送</button>
    </form>
    '''


@app.route('/XMLSender', methods=['POST'])
async def sendp():
    XML_data = await request.form
    group_id = int(XML_data.get('group'))
    xml = XML_data.get('XML')
    psw = XML_data.get('psw')
    if psw == password:
        await curr_bot.send_group_msg(group_id=group_id, message=f'[CQ:xml,data={xml}]')
        return '''
            <form action="XMLSender" method="post"><br />
                密码：<input type="text" name="psw"><br />
                群号：<input type="text" name="group"><br />
                XML：<br />
                <textarea rows="10" cols="30" name="XML"></textarea><br />
                <button type="submit">发送</button>
            </form>
            发送成功!
            '''
    else:
        return '''
            <form action="XMLSender" method="post"><br />
                密码：<input type="text" name="psw"><br />
                群号：<input type="text" name="group"><br />
                XML：<br />
                <textarea rows="10" cols="30" name="XML"></textarea><br />
                <button type="submit">发送</button>
            </form>
            密码错误!
            '''
