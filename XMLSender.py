from urllib.request import urlopen
from nonebot import get_bot
from hoshino import Service
from hoshino.typing import HoshinoBot, CQEvent
from quart import request
try:
    import ujson as json
except ImportError:
    import json

sv = Service(name='XMLSender')
app = get_bot().server_app

host = json.load(urlopen('http://jsonip.com'))['ip']
port = get_bot().config.PORT
curr_bot = get_bot()
password = ''


@sv.on_prefix('发送XML')
async def sendXML(bot: HoshinoBot, ev: CQEvent):
    msg = ev.message.extract_plain_message()
    await bot.send(ev, f'[CQ:xml,data={msg}]')


@sv.on_fullmatch('在线发送XML')
async def sendXMLWeb(bot: HoshinoBot, ev: CQEvent):
    await bot.send(ev, f'http://{host}:{port}/XMLSender')


@app.route('/XMLSender', methods=['GET'])
def sendg():
    return '''
    <form action="XMLSender" method="post">
        密码<input type="text" name="psw">\n
        群号<input type="text" name="group">\n
        XML<textarea rows="10" cols="30" name="XML"></textarea>\n
        <button type="submit">发送</button>\n
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
            <form action="XMLSender" method="post">
                <input type="text" name="psw">\n
                <input type="text" name="group">\n
                <textarea rows="10" cols="30" name="XML"></textarea>\n
                <button type="submit">发送</button>\n
            </form>发送成功!
            '''
    else:
        return '''
            <form action="XMLSender" method="post">
                <input type="text" name="psw">\n
                <input type="text" name="group">\n
                <textarea rows="10" cols="30" name="XML"></textarea>\n
                <button type="submit">发送</button>\n
            </form>密码错误!
            '''