# coding=utf-8
import requests, random, json, jsonpath, tkinter, urllib3, re
from hashlib import md5
from tkinter import ttk
# pyinstaller -F -w "我的翻译 - 副本.py" -i favicon.ico
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()
# 翻译程序
def Translate(content, from_lang, to_lang):
    appid = #百度官网申请
    appkey = #百度官网申请
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path
    query = content
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
    try:
        r = requests.post(url, params=payload, headers=headers)
    except:
        return '网络错误!'
    json = r.json()
    result = jsonpath.jsonpath(json, '$..dst')
    yield result
# 语种识别
def Language_recognition(content):
    url = 'https://fanyi-api.baidu.com/api/trans/vip/language'
    q = content
    appid = 
    appkey = 
    salt = random.randint(1111111111, 9999999999)
    sign = make_md5(appid + q + str(salt) + appkey)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': q, 'salt': salt, 'sign': sign}
    try:
        response = requests.post(url, headers=headers, params=payload)
    except:
        return False
    result = jsonpath.jsonpath(response.json(), '$..src')
    if result is not False:
        return result[0]
    else:
        return None
def Button(source, destination):
    text = source.get(1.0, 'end')
    # 空白信息则不翻译
    if re.findall('^\s*\n*$', text) or text == '':
        destination.configure(state=tkinter.NORMAL)
        destination.delete(1.0, 'end')
        destination.insert('end', '')
        destination.configure(state='disabled')
        return
    from_lang = Language_recognition(text)
    if from_lang != 'zh':
        to_lang = 'zh'
        result = list(Translate(text, from_lang, to_lang))
        for i in result:
            result = ''.join(i)
        destination.configure(state=tkinter.NORMAL)
        destination.delete(1.0, 'end')
        destination.insert('end', result)
        destination.configure(state='disabled')
    elif from_lang == 'zh':
        to_lang = 'en'
        result = list(Translate(text, from_lang, to_lang))
        for i in result:
            result = ''.join(i)
        destination.configure(state=tkinter.NORMAL)
        destination.delete(1.0, 'end')
        destination.insert('end', result)
        destination.configure(state='disabled')
    elif from_lang is False:
        destination.configure(state=tkinter.NORMAL)
        destination.delete(1.0, 'end')
        destination.insert('end', '网络错误!')
        destination.configure(state='disabled')
    else:
        destination.configure(state=tkinter.NORMAL)
        destination.delete(1.0, 'end')
        destination.insert('end', '无翻译结果')
        destination.configure(state='disabled')
if __name__ == '__main__':
    window = tkinter.Tk()
    window.title('我的翻译')
    window.geometry('500x290')
    window.resizable(0, 0)
    source = tkinter.Text(window, font=('微软雅黑', 10))
    destination = tkinter.Text(window, font=('微软雅黑', 10))
    destination.configure(state=tkinter.DISABLED)
    source.place(x=20, y=40, width=200, height=180)
    destination.place(x=270, y=40, width=200, height=180)
    left = tkinter.Label(window, text='原文', justify='left', font=('微软雅黑', 10), fg='black', bd=3)
    right = tkinter.Label(window, text='结果', justify='left', font=('微软雅黑', 10), fg='black', bd=3)
    left.place(x=20, y=6)
    right.place(x=270, y=6)
    text = source.get(1.0, 'end')
    button = ttk.Button(window, text='翻译', width=10, command=lambda: Button(source, destination))
    button.place(x=400, y=250)
    poem = eval(requests.get(r'https://v1.jinrishici.com/all.json').content.decode())
    poetry = tkinter.Label(width=40, height=3, fg='black', font=('华文行楷', 14), bg='#f0f0f0',
                           text=poem['content'] + '\n--《' + poem['origin'] + '》' + poem['author'])
    poetry.place(x=7, y=230)
    menu = tkinter.Menu(window, tearoff=False)
    menu.add_command(label='复制', command=lambda: window.clipboard_append(poetry['text']))
    poetry.bind('<Button-3>', lambda event: menu.post(event.x_root, event.y_root))
    window.mainloop()
