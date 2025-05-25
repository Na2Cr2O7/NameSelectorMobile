"""
aaaaaa
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import edge_tts
from pathlib import Path
from random import choice
import os

import threading



VOICE = "zh-CN-XiaoxiaoNeural"
OUTPUT_FILE_NAME = "output.mp3"
NAME_LIST='nameList.txt'


def getDownloadFolder():
    t=Path()
    if toga.platform.current_platform=='windows' or toga.platform.current_platform=='linux' or toga.platform.current_platform=='macos':
        t=Path.home() / "Downloads"
    else:
        t=Path('/storage/emulated/0/Download')
    return t


def replaceSlash(s):
    s=str(s)
    return s.replace('\\','/')

from http.server import HTTPServer, BaseHTTPRequestHandler
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'audio/mp3')
        self.end_headers()
        if not os.path.exists(f'{replaceSlash(getDownloadFolder())}/{OUTPUT_FILE_NAME}'):
            self.send_response(404)
            self.end_headers()
            return
        with open(f'{replaceSlash(getDownloadFolder())}/{OUTPUT_FILE_NAME}', 'rb') as f:
            content = f.read()
        self.wfile.write(content)

httpd = HTTPServer(('localhost', 8080), MyHandler)


def g():
    httpd.serve_forever()
threading.Thread(target=g).start()


def getAudio(text):

    communicate = edge_tts.Communicate(text, VOICE)
    communicate.save_sync(getDownloadFolder() / OUTPUT_FILE_NAME)


def getNameList():
    if Path( getDownloadFolder() / NAME_LIST).exists():
        with open(getDownloadFolder() / NAME_LIST, 'r') as f:
            name_list = f.readlines()
        for i in range(len(name_list)):
            name_list[i]=name_list[i].strip()
    else:
        name_list =['在这里添加名单']
    return name_list


def saveNameList(name_list):
    with open(getDownloadFolder() / NAME_LIST, 'w') as f:
        for i in name_list:
            f.write(i)
            f.write('\n')

class NameSelectorMobile(toga.App):
    def startup(self):
        
        self.nameList=getNameList()
        self.nameList2=self.nameList.copy()
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.main_box={'NameSelector':toga.Box(style=Pack(direction=COLUMN)),'NameEditor':toga.Box(style=Pack(direction=COLUMN))}
        self.nameLabel=toga.Label(text='',style=Pack(padding=10,font_size=45))
        nameSelect=toga.Button(text='点名',style=Pack(padding=10,font_size=20,width=300),on_press=self.nameSelect_Click)
        buttonBox=toga.Box(style=Pack(direction=COLUMN))
        editButton=toga.Button(text='编辑名单',style=Pack(padding=10,font_size=15,width=300),on_press=self.editNameList_Click)
        self.doPlay=toga.Switch(text='朗读(需要网络)',style=Pack(padding=10,font_size=15),value=True)
        buttonBox.add(self.doPlay)
        buttonBox.add(nameSelect)
        
        buttonBox.add(editButton)

        backButton=toga.Button(text='返回',style=Pack(padding=10,font_size=15,width=300),on_press=self.back_Click)
        self.editor=toga.MultilineTextInput(style=Pack(padding=10,font_size=15,width=300,height=300),readonly=False,on_change=self.editor_Change)
        self.editor.value='\n'.join(self.nameList)
        self.webview = toga.WebView(style=Pack(padding=10,width=3,height=3))
        
        #self.webview.url='http://localhost:8080'
        
        
        self.main_box['NameSelector'].add(self.nameLabel)
        
        self.main_box['NameSelector'].add(buttonBox)
        


        self.main_box['NameEditor'].add(toga.Label(text='名单编辑器',style=Pack(padding=10,font_size=15)))
        
        self.main_box['NameEditor'].add(self.editor)
        self.main_box['NameEditor'].add(backButton)

        
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box['NameSelector']
        self.main_window.size=(300,400)
        self.main_window.show()
    def editor_Change(self, widget):
        pass
    def back_Click(self, widget):
        #保存

        self.nameList=self.editor.value.split('\n')
        try:
            saveNameList(self.nameList)
        except Exception as e:
            pass
        self.nameList=getNameList()
        self.nameList2=self.nameList.copy()
        self.main_window.content=self.main_box['NameSelector']
    def editNameList_Click(self, widget):
        self.nameList2=self.nameList.copy()
        self.main_window.content=self.main_box['NameEditor']
    def getandPlay(self,name):
        self.webview.url='https://www.example.com'
        getAudio(name)
        self.webview.url='http://localhost:8080'
    async def nameSelect_Click(self, widget):

        name=choice(self.nameList2)
        #threading.Thread(target=self.getandPlay,args=(name,)).start()
        self.nameLabel.text=name

        self.nameList2.remove(name)
        if self.doPlay.value:
            self.getandPlay(name)
        
        
        #await asyncio.to_thread(playSound, getDownloadFolder() / OUTPUT_FILE_NAME)
        if len(self.nameList2)==0:
            self.nameList2=self.nameList.copy()

def main():
    return NameSelectorMobile()
