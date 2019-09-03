# -*- coding: utf-8 -*-
"""
This PyQt5 Audio Conveter Tools (brianlu0703)
Vesion 02
Example: WAV file to MP3 file

Created on Mon Aug 26 10:52:58 2019

@author: Brian Lu
"""
"""Fixed QT import error only (pyinstaller)"""
#import fix_qt_import_error

import sys, os, time
from PyQt5.QtWidgets import QApplication, QFileDialog, QComboBox
from PyQt5.QtWidgets import QLabel, QTextEdit, QPushButton, QMainWindow, QAction, QProgressBar, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QBasicTimer
from pydub import AudioSegment


files    = []
wavfiles = []
mp3files = []
curdir = ""
combo_act = "WAV to MP3"
audio_dic = { "WAV to MP3": ["wav","mp3"], "MP3 to WAV": ["mp3","wav"]}
src_audio = "wav"
des_audio = "mp3"
helpmsgtitle = "About audio conveter tool"

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'This PyQt5 Audio Conveter Tools v02'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):
        global os_platform
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
         
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        helpMenu = mainMenu.addMenu('Help')
        
        newAct = QAction('New', self)
        newAct.setShortcut('Ctrl+N')
        newAct.setStatusTip('New Files')
        newAct.triggered.connect(self.toggle_menu)
        
        exitButton = QAction(QIcon('exit.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        
        fileMenu.addAction(newAct)
        fileMenu.addAction(exitButton)
        
        readAct = QAction('About', self)
        readAct.setStatusTip('About ths application')
        readAct.triggered.connect(self.toggle_help_menu)
        helpMenu.addAction(readAct)
        
        # Create textbox
        self.textbox = QTextEdit(self)
        self.textbox.move(10, 70)
        self.textbox.resize(300,360)
        
        self.textbox_view = QTextEdit(self)
        self.textbox_view.move(320, 70)
        self.textbox_view.resize(300,360)
        
        self.label = QLabel('The Audio Source Files', self)
        self.label.resize(250,32)
        self.label.move(10,40)
        
        self.label2 = QLabel('The Audio Destination Files', self)
        self.label2.resize(250,32)
        self.label2.move(320,40)
        
        self.label3 = QLabel('Convert Files:', self)
        self.label3.resize(125,30)
        self.label3.move(10,440)
        
        self.combo = QComboBox(self)
        combo_list = ["WAV to MP3", "MP3 to WAV"]
        
        for cl in combo_list:
            self.combo.addItem(cl)
        
        self.combo.resize(150,30)
        self.combo.move(130, 440)
        self.combo.activated[str].connect(self.onChanged) #Signal
        
        # Create Convert Button
        self.button = QPushButton("RUN", self)
        self.button.resize(100,30)
        self.button.move(320,440)
        self.button.clicked.connect(self.on_click)
        
        #self.button = QPushButton("Stop", self)
        #self.button.resize(80,32)
        #self.button.move(330,440)
        #self.button.clicked.connect(self.on_click)
        
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(430, 440, 200, 30)
        
        self.step = 0
        self.timer = QBasicTimer()
        
        self.show_select_files()
        self.show()
    
    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.step = 0
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)
        
    def onChanged(self, text):
        global combo_act 
        global src_audio
        global des_audio

        self.textbox_view.setText("")
        self.timer.stop()
        self.step = 0
        self.pbar.setValue(0) 
    
        #self.textbox_view.setText(text)
        combo_act = text
        #self.textbox_view.setText(combo_act)
        
        if combo_act in audio_dic:
            src_audio = audio_dic[combo_act][0]
            des_audio = audio_dic[combo_act][1]
            #for k in audio_dic[combo_act]:
            #    self.textbox_view.append(k+"\n")
            #self.textbox_view.setText(src_audio + des_audio)
    
    def toggle_help_menu(self):
        QMessageBox.about(self, helpmsgtitle, "This tool is convert any audio files")
        
    def toggle_menu(self):
        global files
        global wavfiles
        global curdir
        files    = []
        wavfiles = []
        curdir = ""
        
        self.openFileNamesDialog()
        self.show_select_files()
  
        self.textbox_view.setText("")
        self.timer.stop()
        self.step = 0
        self.pbar.setValue(0) 
    
    def openFileNamesDialog(self):
        global files
        global curdir
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Select all audio files", "","All Files (*);;Python Files (*.py)", options=options)

        #Check current open dir
        for f in files:       
            if sys.platform == "win32":
                tmp = f.split("/")
            else:
                tmp = f.split("/")
                
            n = len(tmp)
            fs = len(tmp[n-1])
            curdir = f[:-fs]
            #self.textbox_view.append(curdir+"\n")
            print("Current dir is " + curdir)
            break
            
    def show_select_files(self):
        global files
        global wavfiles
        
        #textboxValue = self.textbox.text()
        msgs = ""
        self.textbox.setText(msgs)
        
        for msg in files:
            if sys.platform == "win32":
                tmp = msg.split("/")
            else:
                tmp = msg.split("/")
                
            n = len(tmp)
            msgs += tmp[n-1] + "\n" 
            wavfiles.append(tmp[n-1])
            
        self.textbox.setText(msgs)
        
    def on_click(self):
        print("button clicked, clear the view textbox")
        self.textbox_view.setText("")
        self.convert_audio()
            
    def convert_audio(self):
        global files
        global wavfiles
        global curdir
        global combo_act 
        global src_audio
        global des_audio
        
        try:
            
            #if not self.timer.isActive():
            #self.timer.start(100, self)
            #self.pbar.setMinimum(0)
            #self.pbar.setMaximum(0)

            if sys.platform == "win32":
                filedir = os.getcwd() + "\convert_" + des_audio
            else:
                filedir = os.getcwd() + "/convert_" + des_audio
             
            if not os.path.exists(filedir):
                os.makedirs(filedir)
            
            total = len(wavfiles)
            
            for i, fn in enumerate(wavfiles):
                
                #if fn.endswith('.wav') or fn.endswith('.WAV'): 
                if fn.endswith('.'+src_audio) or fn.endswith('.'+src_audio.upper()):
                    # check system platform add appropriate file path
                    if sys.platform == "win32":
                        newpath = "\\"
                    else:
                        newpath = "/"
                        
                    src = curdir  + fn[:-4] + "." + src_audio
                    dst = filedir + newpath + fn[:-4] + "." + des_audio
                
                    print("convert from {0} to {1}".format(src,dst))
                    
                    if os.path.isfile(dst):
                        #print("Found {} audio file and deleted it".format(dst))
                        os.remove(dst)
                        
                    # convert wav to mp3   
                    if  src_audio == "wav":                                                        
                        sound = AudioSegment.from_wav(src)
                    elif src_audio == "mp3":
                        sound = AudioSegment.from_mp3(src)
                        
                    sound.export(dst, format=des_audio)
                    self.textbox_view.append(dst[len(filedir)+1:])
                    
                    #Update progress bar after converted 
                    #Due to QT Basictimer event can't increas step value while converting file
                    self.pbar.setValue(i/total*100)
                    time.sleep(0.2)
                    
            self.pbar.setValue(100)
        except:
            print("convert audio {} to {} file error".format(src_audio,des_audio))        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())