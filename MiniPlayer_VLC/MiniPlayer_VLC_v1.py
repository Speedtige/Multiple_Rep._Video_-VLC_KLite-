# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 Visor de Imágenes Múltiple - MÓDULO REP. DE VIDEOS 🔥
Versión        : v-05
Framework      : PyQt5
Integración    : PyQt5 - Media Player - VLC_v5.py

Desarrollado por: Cristian M. Veliz Cano
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
"""

##=========================================================================================================
##=========================================================================================================
from tkinter import *
import platform
import queue
import sys
import time
import vlc
import os
os.add_dll_directory(os.getcwd())
##===================================================
##===================================================
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtPrintSupport import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtPrintSupport import *
from PyQt5.QtGui import QIcon
##=========================================================================================================
global filename
filename = []
##=========================================================================================================
class Path():
    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for pyinstaller"""
        try:
            #PyInstaller Create a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
##=========================================================================================================
##=========================================================================================================
class Player(QMainWindow):
    def __init__(self, file_list=None):
        super().__init__()

        self.file_list = []
        self.filename2 = []
        self.file_list.append(file_list)
        self.filename2.append(file_list)
        
        self.setWindowTitle("PyQt5 - Media Player - VLC_v5")
##================================================================
        self.Ico_app = Path.resource_path('Ico\\1.png')
        self.setWindowIcon(QIcon(self.Ico_app))
##================================================================
        self.center_on_screen()

        try:
	        # Create a basic vlc instance
	        self.instance = vlc.Instance('--verbose 3')

	        self.media = None

	        # Create an empty vlc media player
	        self.mediaplayer = self.instance.media_player_new()

	        self.create_ui()
	        self.data_queue = queue.Queue()
	        self.is_paused = False

	        self.timer = QtCore.QTimer(self)
	        self.timer.setInterval(100)
	        self.timer.timeout.connect(self.update_ui)
	        self.timer.timeout.connect(self.update_time_label)
        except Exception as e:
            print(e)

        self.mediaplayer.video_set_mouse_input(True)
        self.mediaplayer.video_set_key_input(True)
        self.mediaplayer.audio_set_volume(5)

        self.installEventFilter(self)

#==============================================================
    def playlist_start(self):
        global filename

        if not self.file_list:
            return

        #==============================================================
        #==============================================================
        filename = self.file_list[0][0]
        print(filename)    

        # cargar al VLC tu playlist:
        for item in filename:
            print(self.item)
            
        self.open_file()

        #==============================================================
        #==============================================================

        #self.media_player.play()

    def center_on_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = 700, 500
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2
        self.setGeometry(x, y, w, h)

    def create_ui(self):
        """Set up the user interface, signals & slots
        """

        QToolTip.setFont(QFont('SansSerif', 10))

        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if platform.system() == "Darwin":  # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtWidgets.QFrame()

        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        # Create the time display
        self.timelabel = QtWidgets.QLabel("00:00:00", self)

        # Create the "status_time" label
        self.status_time = QtWidgets.QLabel("Status time:")

        # Create the position slider (QSlider)
        self.positionslider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setToolTip("Position")
        self.positionslider.setMaximum(1000)
        self.positionslider.sliderMoved.connect(self.set_position)
        self.positionslider.sliderMoved.connect(self.update_time_label)

        # Create the time duration
        self.timelabel_2 = QtWidgets.QLabel("00:00:00", self)

        # Create the "status_time_trans label
        self.status_time_trans = QtWidgets.QLabel("Time trans:")
        self.Space_status = QtWidgets.QLabel("-\\\\-", self)

        # Create the position slider (QSlider) Volume
        self.vol = 50
        self.volume_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.volume_slider.setMaximum(200)
        self.volume_slider.setValue(self.mediaplayer.audio_get_volume())
        self.volume_slider.setToolTip("Volume")
        self.volume_slider.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.volume_slider.sliderMoved.connect(self.move_vol)
        self.volume_slider.setValue(self.vol)

        self.label_1 = QtWidgets.QLabel(self)
        self.label_1.setText('Vol. 50')
        self.label_1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create the "previous frame" button
        self.previousframe = QtWidgets.QPushButton()
        self.previousframe.setFixedWidth(25)
        self.previousframe.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaSkipBackward))
        self.previousframe.setToolTip('Rep. Anterior')
        self.previousframe.clicked.connect(self.on_previous_frame)

        # Create the play button and connect it to the play/pause function
        self.playbutton = QtWidgets.QPushButton()
        self.playbutton.setFixedWidth(40)
        self.playbutton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.playbutton.setToolTip('Rep. Play\\Paused')
        self.playbutton.clicked.connect(self.play_pause)

        # Create the "next frame" button
        self.nextframe = QtWidgets.QPushButton()
        self.nextframe.setFixedWidth(25)
        self.nextframe.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaSkipForward))
        self.nextframe.setToolTip('Rep. Siguiente')
        self.nextframe.clicked.connect(self.on_next_frame)

        # Set the title of the track as window title        
        self.now_playing = QtWidgets.QLabel("Ahora Suena: ")        

        # Create the "decrease playback rate" button
        self.decr_pb_rate = QtWidgets.QPushButton()
        self.decr_pb_rate.setFixedWidth(30)
        self.decr_pb_rate.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaSeekBackward))
        self.decr_pb_rate.setToolTip('Rep. Low Frame')
        self.decr_pb_rate.clicked.connect(self.decr_mov_play_rate)

        # Create the stop button and connect it to the stop function
        self.stopbutton = QtWidgets.QPushButton()
        self.stopbutton.setFixedWidth(30)
        self.stopbutton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaStop))
        self.stopbutton.setToolTip('Rep. Stop')
        self.stopbutton.clicked.connect(self.stop)

        # Create the "increase playback rate" button
        self.incr_pb_rate = QtWidgets.QPushButton()
        self.incr_pb_rate.setFixedWidth(30)
        self.incr_pb_rate.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaSeekForward))
        self.incr_pb_rate.setToolTip('Rep. Fast Frame')
        self.incr_pb_rate.clicked.connect(self.incr_mov_play_rate)

        icon_2 = QIcon()
        self.info_app = QtWidgets.QPushButton()
        self.info = Path.resource_path('Ico\\info_2.png')
        self.info_app.setFixedWidth(30)
        icon_2.addPixmap(QPixmap(self.info), QIcon.Normal, QIcon.Off)
        self.info_app.setToolTip('Info App')
        self.info_app.setIcon(icon_2)
        self.info_app.clicked.connect(self.Info_App_Soft)

        icon_3 = QIcon()
        self.agregar_a_rep = QtWidgets.QPushButton()
        self.agregar = Path.resource_path('Ico\\plus.png')
        self.agregar_a_rep.setFixedWidth(30)
        icon_3.addPixmap(QPixmap(self.agregar), QIcon.Normal, QIcon.Off)
        self.agregar_a_rep.setToolTip('Open File´s')
        self.agregar_a_rep.setIcon(icon_3)
        self.agregar_a_rep.clicked.connect(self.agregar_lista)

        self.top_control_box = QtWidgets.QHBoxLayout()

        # Add the time and position slider to the 1st controls layout
        self.top_control_box.addWidget(self.status_time)
        self.top_control_box.addWidget(self.timelabel_2)
        self.top_control_box.addWidget(self.positionslider)
        self.top_control_box.addWidget(self.status_time_trans)
        self.top_control_box.addWidget(self.timelabel)
        self.top_control_box.addWidget(self.Space_status)
        self.top_control_box.addWidget(self.volume_slider)
        self.top_control_box.addWidget(self.label_1)

        self.bottom_control_box = QtWidgets.QHBoxLayout()

        # Add the buttons to the 2nd controls layout
        self.bottom_control_box.addWidget(self.previousframe)
        self.bottom_control_box.addWidget(self.playbutton)
        self.bottom_control_box.addWidget(self.nextframe)
        self.bottom_control_box.addWidget(self.now_playing)
        self.bottom_control_box.addWidget(self.decr_pb_rate)
        self.bottom_control_box.addWidget(self.stopbutton)
        self.bottom_control_box.addWidget(self.incr_pb_rate)
        self.bottom_control_box.addWidget(self.agregar_a_rep)
        self.bottom_control_box.addWidget(self.info_app)

        self.vboxlayout = QtWidgets.QVBoxLayout()

        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addLayout(self.top_control_box)
        self.vboxlayout.addLayout(self.bottom_control_box)

        self.widget.setLayout(self.vboxlayout)

        #==============================================================
        #==============================================================

        # # Create submenu to start new processes from file menu
        file_menu = self.menuBar().addMenu("&File")

        # # Create actions to load a new media file and to close the app
        open_file = Path.resource_path('Ico\\Abrir_Archivo.png')        
        open_action =  QtWidgets.QAction(QIcon(open_file), "Load Video", self)
        
        Exit_file = Path.resource_path('Ico\\Salir.png')
        close_action = QtWidgets.QAction(QIcon(Exit_file), "Close App", self)

        Capture_file = Path.resource_path('Ico\\png\\image.png')
        capture = QtWidgets.QAction(QIcon(Capture_file), "Capture Pick", self)

        Volume_Off = Path.resource_path('Ico\\png\\volume-off.png')
        mute = QtWidgets.QAction(QIcon(Volume_Off), "Mute Media-Player", self)

        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(capture)
        file_menu.addAction(mute)
        file_menu.addSeparator()
        file_menu.addAction(close_action)        

        open_action.triggered.connect(self.open_file)
        capture.triggered.connect(self.Cap_Pick)
        mute.triggered.connect(self.OnMute)
        close_action.triggered.connect(sys.exit)

        #==============================================================
        #==============================================================

        self.sb = 0
        self.filename2 = []
        self.volMuted = False
        self.value_wind_vid  = False
        self.volume_value = 0

        # Conecte a las funciones de visualización del menú
        self.widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.widget.customContextMenuRequested.connect(self.create_rightmenu)

#==============================================================
    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            sys.exit()

        elif event.key() == 79:     ## O
            self.open_file()

        elif event.key() == 80:     ## P
            self.play_pause()

        elif event.key() == 70:     ## F
            self.on_previous_frame()

        elif event.key() == 78:     ## N
            self.on_next_frame()

        elif event.key() == 83:     ## S
            self.stop()

        elif event.key() == 77:     ## M
            self.agregar_lista()

        elif event.key() == 73:     ## I
            self.Info_App_Soft()

        elif event.key() == 67:     ## C
            self.Cap_Pick()

        elif event.key() == 86:     ## V
            self.OnMute()

        elif event.key() == 69:     ## E
            self.Expand_Win_Vid()

    def Expand_Win_Vid(self):

        if self.value_wind_vid == False:
            print('Valor de Self.Mute:  ', self.value_wind_vid)

            try:

                self.play_pause()  
                self.stop()

                self.value_wind_vid = True

                # Create a basic vlc instance
                instance = vlc.Instance('--verbose 3')
                # Create an empty vlc media player
                self.mediaplayer = instance.media_player_new()
                self.mediaplayer.set_mrl(self.filename2[self.sb])
                self.mediaplayer.set_fullscreen(self.value_wind_vid)

                self.mediaplayer.toggle_teletext()
                self.timer.start()

                self.mediaplayer.play()
                
                self.mediaplayer.video_set_mouse_input(True)
                self.mediaplayer.video_set_key_input(True)

            except Exception as e:
                print(e)

                self.play_pause()

        elif self.value_wind_vid == True:
            print('Valor de Self.Mute:  ', self.value_wind_vid)

            try:

                self.value_wind_vid = False
                self.mediaplayer.stop()
                self.mediaplayer.set_fullscreen(self.value_wind_vid)
                self.on_next_frame()

            except Exception as e:
                print(e)

        self.OnVolume()

        # Set the title of the track as window title
        txt_title1 = self.filename2[self.sb]
        txt_title2 = txt_title1.split("/")
        txt_title3 = txt_title2[-1]
        self.now_playing.setText("Ahora Suena:  \\\\  {}".format(txt_title3))

#==============================================================
#==============================================================
    def OnVolume(self, e = None):
        """Volume slider changed, adjust the audio volume."""
        if self.filename2 == "" or self.filename2 == [] or self.filename2 == None:
            pass
        else:

            vol = min(self.volume_slider.value(), 200)

            if self.mediaplayer and not self.volMuted:
                if self.mediaplayer.audio_set_volume(vol):
                    print(e)
#==============================================================
#==============================================================

    def agregar_lista(self):

        try:

            self.play_pause()
            self.info_msg2()

            new_filename, _ = QFileDialog.getOpenFileNames(self, "Open file", "", 
                "Video files: (*.mp4) ;; Video files: (*.mp4v)) ;; Video files: (*.avi) ;; \
                Video files: (*.flv) ;; Video files: (*.mkv)) ;; Video files: (*.wap) ;; \
                Video files: (*.cda) ;; Video files: (*.flac) ;; Video files: (*.mp3) ;; \
                All Files (*.*)")

            for plus_music in new_filename:            
                self.filename2.append(plus_music)

            self.play_pause()
            return None

        except Exception as e:
            print(e)

    def set_volume(self, volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(volume)

    def move_vol(self, e):

        self.label_1.setText('Vol. ' + str(e))

    def Cap_Pick(self):

        self.play_pause()

        dir_salida = QFileDialog.getSaveFileName(self, "Save file", "", ("Image file(*.png) ;; All Files (*.*)"))
        print('Esta es la Salida:  ', dir_salida[0])

        num = 0
        psz_filepath = dir_salida[0]
        i_width = int(1920)     ## Ancho
        i_height = int(1200)    ## Alto     

        self.mediaplayer.video_take_snapshot(num, psz_filepath, i_width, i_height)

        self.play_pause()

    def OnMute(self, e=None):

        print('Valor de Self.Mute:  ', self.volMuted)

        if self.volMuted == False:

            """Mute/Unmute audio."""
            # audio un/mute may be unreliable, see vlc.py docs.
            volMuted = m = not self.volMuted  # player.audio_get_mute()
            self.mediaplayer.audio_set_mute(m)

            print('Valor de Self.Mute:  ', self.volMuted)

            self.volMuted = True

        elif self.volMuted == True:

            """Mute/Unmute audio."""
            # audio un/mute may be unreliable, see vlc.py docs.
            volMuted = m = not self.volMuted  # player.audio_get_mute()
            self.mediaplayer.audio_set_mute(m)

            print('Valor de Self.Mute:  ', self.volMuted)

            self.volMuted = False

#==============================================================
#==============================================================

    def Info_App_Soft(self):
        
        QMessageBox.information(self, 'Info', 'Este Software, esta desarrollado en forma Minimalista\
            \ncon el lenguaje de Programación:\nPython 3.8.3, en PyQt5, sin el Diseñador.\
            \nDesarrollado por: \n\nCristian M. Veliz Cano\nCorreo Electronico: cristianvel2015mvc@gmail.com\
            \nVerción del Soft: v-5\n\nPara Windows con base 64(bits)')

    def info_msg(self):

        QMessageBox.information(self, 'Aviso', 'Procede a Indicar los Medios,\nPara La reproducción.\nGracias')


    def info_msg2(self):

        QMessageBox.information(self, 'Aviso', 'Procede a Seleccionar los Medios,\nPara Agregar A La reproducción.\nGracias')

#==============================================================
#==============================================================

    def play_pause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            signal = 'p'
            self.mediaplayer.pause()
            self.playbutton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
            self.is_paused = True
            self.timer.stop()
        else:
            if self.mediaplayer.play() == -1:
                self.open_file()
                return

            signal = 'P'
            self.mediaplayer.play()
            self.mediaplayer.video_set_mouse_input(True)
            self.mediaplayer.video_set_key_input(True)
            self.playbutton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
            self.timer.start()
            self.is_paused = False

            # Set the title of the track as window title
            txt_title1 = self.filename2[self.sb]
            txt_title2 = txt_title1.split("/")
            txt_title3 = txt_title2[-1]
            self.now_playing.setText("Ahora Suena:  \\\\  {}".format(txt_title3))

        # Reset the queue & send the appropriate signal, i.e., play/pause
        self.data_queue.queue.clear()
        self.data_queue.put('d')
        self.data_queue.put(signal)

    def stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        self.playbutton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))

        # Reset the time label back to 00:00:00
        time = QtCore.QTime(0, 0, 0, 0)
        self.timelabel.setText(time.toString())

        # Reset the queue
        self.data_queue.queue.clear()
        self.data_queue.put('d')
        self.data_queue.put('S')

        # Reset the media position slider
        self.positionslider.setValue(0)

        # Set the title of the track as window title
        self.now_playing.setText("El Estado es:  \\\\  In Paused")

        self.timer.stop()

#==============================================================
#==============================================================

    def on_next_frame(self):

        self.sb += 1
        if not self.filename2[self.sb]:
            return

        # getOpenFileName returns a tuple, so use only the actual file name
        self.media = self.instance.media_new(self.filename2[self.sb])

        # Put the media in the media player
        # self.mediaplayer.set_media(self.media)
        self.mediaplayer.set_mrl(self.filename2[self.sb])

        # Parse the metadata of the file
        self.media.parse()

        # Set the title of the track as window title
        txt_title1 = self.filename2[self.sb]
        txt_title2 = txt_title1.split("/")
        txt_title3 = txt_title2[-1]
        self.now_playing.setText("Ahora Suena:  \\\\  {}".format(txt_title3))

        # The media player has to be 'connected' to the QFrame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the QFrame (or similar object) to
        # vlc. Different platforms have different functions for this.
        if platform.system() == "Linux":  # for Linux using the X Server
            self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows":  # for Windows
            self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin":  # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

        self.play_pause()

    def on_previous_frame(self):

        self.sb -= 1
        if not self.filename2[self.sb]:
            return

        # getOpenFileName returns a tuple, so use only the actual file name
        self.media = self.instance.media_new(self.filename2[self.sb])

        # Put the media in the media player
        # self.mediaplayer.set_media(self.media)
        self.mediaplayer.set_mrl(self.filename2[self.sb])

        # Parse the metadata of the file
        self.media.parse()

        # Set the title of the track as window title
        txt_title1 = self.filename2[self.sb]
        txt_title2 = txt_title1.split("/")
        txt_title3 = txt_title2[-1]
        self.now_playing.setText("Ahora Suena:  \\\\  {}".format(txt_title3))

        # The media player has to be 'connected' to the QFrame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the QFrame (or similar object) to
        # vlc. Different platforms have different functions for this.
        if platform.system() == "Linux":  # for Linux using the X Server
            self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows":  # for Windows
            self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin":  # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

        self.play_pause()

    def mspf(self):
        """Milliseconds per frame"""
        return int(1000 // (self.mediaplayer.get_fps() or 25))

    def incr_mov_play_rate(self):
        """Increase the movie play rate by a factor of 2."""
        if self.mediaplayer.get_rate() >= 64:
            return

        rate = self.mediaplayer.get_rate() * 2
        result = self.mediaplayer.set_rate(rate)
        if result == 0:
            self.data_queue.queue.clear()
            self.data_queue.put('d')
            self.data_queue.put('>')
            #self.update_pb_rate_label()

    def decr_mov_play_rate(self):
        """Decrease the movie play rate by a factor of 2."""
        if self.mediaplayer.get_rate() <= 0.125:
            return

        rate = self.mediaplayer.get_rate() * 0.5
        result = self.mediaplayer.set_rate(rate)
        if result == 0:
            self.data_queue.queue.clear()
            self.data_queue.put('d')
            self.data_queue.put('<')
            #self.update_pb_rate_label()

#==============================================================
#==============================================================

    def open_file(self):
        global filename
        """Open a media file in a MediaPlayer
        """

        if self.filename2 == []:
        
            self.mediaplayer.pause()
            self.filename2.clear()
            self.mediaplayer.stop()
            time.sleep(0.01)        

            if filename == []:
                file, _ = QFileDialog.getOpenFileNames(self, "Open file", "", 
                    "Video files: (*.mp4) ;; Video files: (*.mp4v)) ;; Video files: (*.avi) ;; \
                    Video files: (*.flv) ;; Video files: (*.mkv)) ;; Video files: (*.wap) ;; \
                    Video files: (*.cda) ;; Video files: (*.flac) ;; Video files: (*.mp3) ;; \
                    All Files (*.*)")
                
                for i in file:
                    filename.append(i)
                    self.filename2.append(i)
                self.sb = 0

            else:
                for i in filename:
                    self.filename2.append(i)
                self.sb = 0

                if not filename[self.sb]:
                    return

            time.sleep(0.01)

            # getOpenFileName returns a tuple, so use only the actual file name
            print(filename[self.sb])
            self.media = self.instance.media_new(filename[self.sb])

            # Put the media in the media player
            # self.mediaplayer.set_media(self.media)
            self.mediaplayer.set_mrl(filename[self.sb])

            # Parse the metadata of the file
            self.media.parse()

            # Set the title of the track as window title
            txt_title1 = self.filename2[self.sb]
            txt_title2 = txt_title1.split("/")
            txt_title3 = txt_title2[-1]
            self.now_playing.setText("Ahora Suena:  \\\\  {}".format(txt_title3))

            # The media player has to be 'connected' to the QFrame (otherwise the
            # video would be displayed in it's own window). This is platform
            # specific, so we must give the ID of the QFrame (or similar object) to
            # vlc. Different platforms have different functions for this.
            if platform.system() == "Linux":  # for Linux using the X Server
                self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
            elif platform.system() == "Windows":  # for Windows
                self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
            elif platform.system() == "Darwin":  # for MacOS
                self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

            self.center_on_screen()
            self.play_pause()

        else:
            self.agregar_lista()

#==============================================================
#==============================================================

    def set_position(self):
        """Set the movie position according to the position slider.

        The vlc MediaPlayer needs a float value between 0 and 1, Qt uses
        integer variables, so you need a factor; the higher the factor,
        the more precise are the results (1000 should suffice).
        """
        # Set the media position to where the slider was dragged
        self.timer.stop()
        pos = self.positionslider.value()

        if pos >= 0:
            self.data_queue.queue.clear()
            self.data_queue.put('d')
            current_time = self.mediaplayer.get_time()

            # If the player is stopped, do not attempt to send a -1!!!
            if current_time == -1:
                self.timer.start()
                return
            self.data_queue.put(current_time)

        self.mediaplayer.set_position(pos * .001)
        self.timer.start()

    def update_ui(self):
        """Updates the user interface"""

        # Set the slider's position to its corresponding media position
        # Note that the setValue function only takes values of type int,
        # so we must first convert the corresponding media position.
        media_pos = int(self.mediaplayer.get_position() * 1000)
        self.positionslider.setValue(media_pos)

        if media_pos >= 0 and self.mediaplayer.is_playing():
            current_time = self.mediaplayer.get_time()
            self.data_queue.put(current_time)
        else:
            self.data_queue.queue.clear()

        # No need to call this function if nothing is played
        if not self.mediaplayer.is_playing():
            self.timer.stop()

            # After the video finished, the play button stills shows "Pause",
            # which is not the desired behavior of a media player.
            # This fixes that "bug".
            if not self.is_paused:
                time.sleep(0.01)
                self.mediaplayer.pause()
                pass
                #self.stop()   <<--- Esta bueeeno Pero Trunca, la Reproducción...

    def update_time_label(self):
        mtime = QtCore.QTime(0, 0, 0, 0)
        self.time = mtime.addMSecs(self.mediaplayer.get_time())
        self.timelabel.setText(self.time.toString())

        t = self.mediaplayer.get_length() * 1e-3 # to seconds
        if t > 0:
            #self.timeSlider.config(to=t)                

            converted_current_time_1 = time.strftime('%H:%M:%S', time.gmtime(int(t-1)))
            self.timelabel_2.setText(converted_current_time_1)

            a = self.timelabel.text()
            b = self.timelabel_2.text()

            if a >= b:
                self.on_next_frame()                
            else:
                pass

    def update_pb_rate_label(self):
        ##self.pb_rate_label.setText("Playback rate: {}x".format(str(self.mediaplayer.get_rate())))
        pass

#==============================================================
#==============================================================

    def closeEvent(self, event):
        try:

            self.mediaplayer.pause()
            self.filename2.clear()
            self.mediaplayer.stop()
            self.mediaplayer.stop()
            
        except Exception as e:
            log_message(f"Error on close: {e}")
        finally:
            sys.exit()

##=========================================================================================================================
##=========================================================================================================================

    def create_rightmenu(self):
        # Objeto de menú
        self.groupBox_menu = QMenu(self)

        self.groupBox_menu.addSeparator()

        #print_action = QAction("Export to PDF", self)
        self.Export_file1 = Path.resource_path('Ico\\png\\image.png')
        Capture_Pick = QAction(QIcon(self.Export_file1), "Capture Pick", self)
        Capture_Pick.setShortcut('C')
        self.groupBox_menu.addAction(Capture_Pick)

        Capture_Pick.setStatusTip("Capture Pick") 
        Capture_Pick.triggered.connect(self.Cap_Pick)
        self.groupBox_menu.addAction(Capture_Pick)

        self.groupBox_menu.addSeparator()

        #print_action = QAction("Export to PDF", self)
        self.Mute_Media_Player1 = Path.resource_path('Ico\\png\\volume-off.png')
        Mute_Media_Player = QAction(QIcon(self.Mute_Media_Player1), "Mute Media-Player", self)
        Mute_Media_Player.setShortcut('V')
        self.groupBox_menu.addAction(Mute_Media_Player)

        Mute_Media_Player.setStatusTip("Mute Media-Player") 
        Mute_Media_Player.triggered.connect(self.OnMute)
        self.groupBox_menu.addAction(Mute_Media_Player)

        self.groupBox_menu.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        #print_action = QAction("Export to PDF", self)
        self.Print_File_2 = Path.resource_path('Ico\\open2.png')
        self.Print_File2 = QAction(QIcon(self.Print_File_2), 'Open File´s', self)
        self.Print_File2.setShortcut('O')
        self.groupBox_menu.addAction(self.Print_File2)

        self.Print_File2.setStatusTip('Open File´s') 
        self.Print_File2.triggered.connect(self.open_file) 
        self.groupBox_menu.addAction(self.Print_File2)

        self.groupBox_menu.addSeparator()

        self.open_file_1 = Path.resource_path('Ico\\png\\play-circle')
        open_file_action = QAction(QIcon(self.open_file_1), 'Rep. Play\\Paused', self)
        open_file_action.setShortcut('P')
        self.groupBox_menu.addAction(open_file_action)

        open_file_action.setStatusTip("Rep. Play\\Paused")        
        open_file_action.triggered.connect(self.play_pause)
        self.groupBox_menu.addAction(open_file_action)

        self.groupBox_menu.addSeparator()

        self.save_file = Path.resource_path('Ico\\png\\rewind-left.png') 
        save_file_action = QAction(QIcon(self.save_file), 'Rep. Anterior', self)
        save_file_action.setShortcut('F')
        self.groupBox_menu.addAction(save_file_action)

        save_file_action.setStatusTip('Rep. Anterior') 
        save_file_action.triggered.connect(self.on_previous_frame) 
        self.groupBox_menu.addAction(save_file_action)
        
        self.saveas_file = Path.resource_path('Ico\\png\\rewind-right.png') 
        saveas_file_action = QAction(QIcon(self.saveas_file), 'Rep. Siguiente', self)
        saveas_file_action.setShortcut('N')
        self.groupBox_menu.addAction(saveas_file_action)

        saveas_file_action.setStatusTip('Rep. Siguiente') 
        saveas_file_action.triggered.connect(self.on_next_frame)
        self.groupBox_menu.addAction(saveas_file_action)

        self.groupBox_menu.addSeparator()

        ##================================================================================================================
        ##================================================================================================================
        
        #print_action = QAction("Export to PDF", self)
        self.Export_file1 = Path.resource_path('Ico\\png\\stop-circle.png')
        Export_file = QAction(QIcon(self.Export_file1), 'Rep. Stop', self)
        Export_file.setShortcut('S')
        self.groupBox_menu.addAction(Export_file)

        Export_file.setStatusTip('Rep. Stop') 
        Export_file.triggered.connect(self.stop) 
        self.groupBox_menu.addAction(Export_file)

        self.groupBox_menu.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.redo_file = Path.resource_path('Ico\\plus.png') 
        redo_action = QAction(QIcon(self.redo_file), 'Agregar a Lista de Rep.', self)
        redo_action.setShortcut('M')
        self.groupBox_menu.addAction(redo_action)

        redo_action.setStatusTip('Agregar a Lista de Rep.')        
        redo_action.triggered.connect(self.agregar_lista)
        self.groupBox_menu.addAction(redo_action)

        self.undo_file = Path.resource_path('Ico\\info_2.png')
        undo_action = QAction(QIcon(self.undo_file), "info_app", self)
        undo_action.setShortcut('I')
        self.groupBox_menu.addAction(undo_action)

        undo_action.setStatusTip("Undo last change")        
        undo_action.triggered.connect(self.Info_App_Soft)

        self.groupBox_menu.addSeparator()

        self.Full_Screen1 = Path.resource_path('Ico\\png\\external-link.png')
        Full_Screen = QAction(QIcon(self.Full_Screen1), '&Close\\Full Screen', self)
        Full_Screen.setShortcut('E')
        self.groupBox_menu.addAction(Full_Screen)

        Full_Screen.setStatusTip("Close\\Full Screen")
        Full_Screen.triggered.connect(self.Expand_Win_Vid) 
        self.groupBox_menu.addAction(Full_Screen)

        self.groupBox_menu.addSeparator()

        self.Exit_file = Path.resource_path('Ico\\Salir.png')
        Exit_action = QAction(QIcon(self.Exit_file), '&Exit', self)
        Exit_action.setShortcut('Escape')
        self.groupBox_menu.addAction(Exit_action)

        Exit_action.setStatusTip("Exit App")
        Exit_action.triggered.connect(qApp.quit) 
        self.groupBox_menu.addAction(Exit_action)
        
        self.groupBox_menu.addSeparator()
        
        self.groupBox_menu.popup(QCursor.pos())
        
        self.groupBox_menu.addSeparator()

        self.groupBox_menu.popup(QCursor.pos())

#==============================================================
#==============================================================

    def play_youtube_url(self, url):
        self.filename2.clear()
        self.filename2.append(url)
        self.sb = 0

        self.mediaplayer.set_mrl(url)

        # conectar el video al QFrame
        if platform.system() == "Linux":
            self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows":
            self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin":
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

        self.media = self.instance.media_new(url)
        self.media.parse()

        self.now_playing.setText(f"Ahora Suena: (YouTube Stream)")
        self.play_pause()

##=========================================================================================================
##=========================================================================================================
def main():
    """Entry point for our simple vlc player
    """
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    mediaplayer = Player()

    mediaplayer.show()
    mediaplayer.resize(700, 500)  ##(640, 480)
    sys.exit(app.exec_())

##=========================================================================================================
##=========================================================================================================
if __name__ == "__main__":
    main()
##=========================================================================================================
##=========================================================================================================