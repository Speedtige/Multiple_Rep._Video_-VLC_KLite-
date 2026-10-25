
# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Desarrollado Por: Cristian M. Veliz Cano
Verción del Soft: V-03
Nombre del Soft: Video_Player_Widget_Logic_v03
Distribución: Gratuito  -->OPENSOURCE<--
'''
##=============================================================================================
##=============================================================================================

import sys, os, webbrowser, tempfile

from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtWidgets import (QMessageBox, QFileDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QAction, 
    QSlider, QStyle, QSizePolicy, QMenu, QLabel, QAbstractItemView, QActionGroup)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QEvent
from PyQt5.QtGui import QIcon, QFont, QPixmap, QCursor

##=============================================================================================
##=============================================================================================
##Clase para todos, los Assets Varios
class Path():
    
    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for pyinstaller"""
        try:
            #PyInstaller Create a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

##=============================================================================================
##=============================================================================================
##Clase Principal para Todos, Todos Todos los Videos, o Cualquier Video Individual
class VideoPlayerWidget(QWidget):
    # Señales:
    clicked = pyqtSignal(QWidget)         # Señal para cada click en los Botones, o Pantalla
    request_close = pyqtSignal(QWidget)   # Señal para cerrar este video

    def __init__(self, parent=None):
        super().__init__(parent)

        # Metodo para la Captura, de los Eventos, en el Mouse (Well)
        self.setMouseTracking(True)

        # Bariable, para copiar, Metodo Full Screen
        self.Objeto_Video = ""
        self.file_path_vid = []
        self.index = 0

        self.check_2 = False

        self.carpeta_capturas = Path.resource_path("capturas")
        self.carpeta_grabaciones = Path.resource_path("grabaciones")

        dirpath = os.path.exists(self.carpeta_grabaciones)

        if dirpath == False:
            import tempfile
            self.carpeta_capturas = tempfile.gettempdir()
            self.carpeta_grabaciones = tempfile.gettempdir()
        else:
            print('Existo')

        # ---- Se Crea el MediaPlayList ----
        self.playlist = QMediaPlaylist()

        # ---- MediaPlayer ----
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)

        # 🔥 Detectar cambios de estado
        self.mediaPlayer.mediaStatusChanged.connect(self.handle_status)

        # Creamos el QVideoWidget(), donde Viviran todos los Videos
        self.videoWidget = QVideoWidget()
        # Pocicionamiento Global de QVideoWidget(), esencial antes del Redimencionamiento
        self.videoWidget.setGeometry(self.pos().x(), self.pos().y(), self.width(), self.height())
        # Reacomodamos Cada Video, para que no Desproporcione
        self.videoWidget.setMinimumSize(300, 200)
        self.videoWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.set_aspect_ratio_mode(Qt.IgnoreAspectRatio)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # ---- Título del video ----
        self.titleLabel = QLabel("Sin título")
        self.titleLabel.setStyleSheet("""QLabel {color: #000040; font-size: 14px; padding: 3px;
                background-color: #ff8cff;}""")
        self.titleLabel.setAlignment(Qt.AlignCenter)

        # ---- Botón Atras ----
        self.atrasButton = QPushButton()
        self.atrasButton.setEnabled(False)
        self.atrasButton.setFixedWidth(25)
        self.atrasButton.setFixedHeight(25)
        self.atrasButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.atrasButton.setStyleSheet('QPushButton:hover {background-color: #ffffff;}')
        self.atrasButton.clicked.connect(self.atras)

        # ---- Botón Play / Pause ----
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedWidth(25)
        self.playButton.setFixedHeight(25)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.setStyleSheet('QPushButton:hover {background-color: #ffffff;}')
        self.playButton.clicked.connect(self.play)

        # ---- Botón Stop ----
        self.stopButton = QPushButton()
        self.stopButton.setEnabled(False)
        self.stopButton.setFixedWidth(25)
        self.stopButton.setFixedHeight(25)
        self.stopButton.setStyleSheet('QPushButton:hover {background-color: #ffffff;}')
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))

        # ---- Botón Siguiente ----
        self.sigButton = QPushButton()
        self.sigButton.setEnabled(False)
        self.sigButton.setFixedWidth(25)
        self.sigButton.setFixedHeight(25)
        self.sigButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.sigButton.setStyleSheet('QPushButton:hover {background-color: #ffffff;}')
        self.sigButton.clicked.connect(self.siguiente)

        # ---- Botón Muted (Mudo) ----
        self.icon_muted = QIcon()
        self.btn_muted = QPushButton()
        self.btn_muted.setFixedWidth(25)
        self.btn_muted.setFixedHeight(25)
        self.muted = Path.resource_path('assets\\Ico\\volume-off.png')
        self.icon_muted.addPixmap(QPixmap(self.muted), QIcon.Normal, QIcon.Off)
        self.btn_muted.setIcon(self.icon_muted)
        self.btn_muted.setIconSize(QtCore.QSize(18, 18))
        self.btn_muted.setObjectName("btn_muted")
        self.btn_muted.setStyleSheet('QPushButton:hover {background-color: #ffffff;}')
        self.btn_muted.clicked.connect(self.Muted_Vol)
        self.stopButton.clicked.connect(self.stop)

        # --> NUEVO: Slider de Volumen (más corto) ──○── <--
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.setFixedWidth(40)
        self.volumeSlider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #565a5e;
                height: 8px;
                background: #565a5e;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #007bff;
                border: 1px solid #565a5e;
                width: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::add-page:horizontal {
                background: #565a5e;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: #007bff;
                border-radius: 4px;
            }
        """)
        self.volumeSlider.valueChanged.connect(self.set_volume)

        # ================================================================
        # NUEVO: Slider de posición ────────○────── con temporizador
        # ================================================================
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #565a5e;
                height: 8px;
                background: #565a5e;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #007bff;
                border: 1px solid #565a5e;
                width: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::add-page:horizontal {
                background: #565a5e;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: #007bff;
                border-radius: 4px;
            }
        """)
        self.positionSlider.sliderMoved.connect(self.set_position)

        # Label´s contol Time (Status, Duration):
        self.currentTimeLabel = QLabel("00:00")
        self.currentTimeLabel.setStyleSheet("""QLabel {color: #000000; font-size: 14px;}""")
        self.totalTimeLabel = QLabel("00:00")
        self.totalTimeLabel.setStyleSheet("""QLabel {color: #000000; font-size: 14px;}""")

        # Layout:
        timeLayout = QHBoxLayout()
        timeLayout.setContentsMargins(0, 0, 0, 0)
        timeLayout.setSpacing(2)
        timeLayout.addWidget(self.currentTimeLabel)
        timeLayout.addWidget(self.positionSlider)
        timeLayout.addWidget(self.totalTimeLabel)

        # ---- Botón Menú ----
        icon_4 = QIcon()
        self.btnMenu = QPushButton()
        self.btnMenu.setFixedWidth(25)
        self.btnMenu.setFixedHeight(25)
        self.menu = Path.resource_path('assets\\Ico\\menu.png')
        icon_4.addPixmap(QPixmap(self.menu), QIcon.Normal, QIcon.Off)
        self.btnMenu.setIcon(icon_4)
        self.btnMenu.setIconSize(QtCore.QSize(18, 18))
        self.btnMenu.setStyleSheet('QPushButton:hover {background-color: #ffffff;}')
        self.btnMenu.clicked.connect(lambda: Menu_Clic.create_rightmenu(self))

        self.btn_speed_down = QPushButton()
        self.btn_speed_down.setFixedWidth(25)
        self.btn_speed_down.setFixedHeight(25)
        self.btn_speed_down.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.btn_speed_down.setStyleSheet('QPushButton:hover {background-color: #ffffff;}')
        self.btn_speed_down.setToolTip("Reducir velocidad")
        self.btn_speed_down.clicked.connect(self.reduce_speed)
        #self.speed_layout.addWidget(self.btn_speed_down)

        self.speed_label = QLabel("1.0x")
        self.speed_label.setStyleSheet("color: #000000; font-weight: bold; min-width: 40px;")
        self.speed_label.setAlignment(Qt.AlignCenter)
        #self.speed_layout.addWidget(self.speed_label)

        self.btn_speed_up = QPushButton()
        self.btn_speed_up.setFixedWidth(25)
        self.btn_speed_up.setFixedHeight(25)
        self.btn_speed_up.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.btn_speed_up.setStyleSheet('QPushButton:hover {background-color: #ffffff;}')
        self.btn_speed_up.setToolTip("Aumentar velocidad")
        self.btn_speed_up.clicked.connect(self.increase_speed)
        #self.speed_layout.addWidget(self.btn_speed_up)

        # ---- Botón Cerrar ----
        icon_5 = QIcon()
        self.closeButton = QPushButton()
        self.closeButton.setFixedWidth(25)
        self.closeButton.setFixedHeight(25)
        self.menu_close = Path.resource_path('assets\\Ico\\close.png')
        icon_5.addPixmap(QPixmap(self.menu_close), QIcon.Normal, QIcon.Off)
        self.closeButton.setIcon(icon_5)
        self.closeButton.setIconSize(QtCore.QSize(18, 18))
        self.closeButton.setStyleSheet('QPushButton:hover {background-color: #ffffff;}')
        self.closeButton.clicked.connect(self._request_close)

        # ---- Layout de controles ----
        controlsLayout = QHBoxLayout()
        controlsLayout.setContentsMargins(0, 0, 0, 0)
        controlsLayout.setSpacing(0)

        controlsLayout.setSpacing(5)
        controlsLayout.addWidget(self.atrasButton)
        controlsLayout.setSpacing(5)
        controlsLayout.addWidget(self.playButton)
        controlsLayout.setSpacing(5)
        controlsLayout.addWidget(self.stopButton)
        controlsLayout.setSpacing(5)
        controlsLayout.addWidget(self.sigButton)

        #controlsLayout.addStretch()

        controlsLayout.setSpacing(5)
        controlsLayout.addLayout(timeLayout)
        controlsLayout.setSpacing(5)
        controlsLayout.addWidget(self.btn_muted)
        controlsLayout.setSpacing(5)
        controlsLayout.addWidget(self.volumeSlider)
        controlsLayout.setSpacing(5)
        controlsLayout.addWidget(self.btnMenu)  
        controlsLayout.setSpacing(5)      
        # Agregar al layout de controles (antes del stretch)
        controlsLayout.setSpacing(5)
        ##controlsLayout.addLayout(self.speed_layout)        
        controlsLayout.addWidget(self.btn_speed_down)
        controlsLayout.setSpacing(5)
        controlsLayout.addWidget(self.speed_label)
        controlsLayout.setSpacing(5)
        controlsLayout.addWidget(self.btn_speed_up)
        controlsLayout.setSpacing(5)
        controlsLayout.addWidget(self.closeButton)   # A LA DERECHA

        # ---- Layout principal ----
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.videoWidget)        
        layout.addWidget(self.titleLabel)
        layout.addLayout(controlsLayout)
        self.setLayout(layout)

        # ---- Conectar QVideoWidget, con el Evento de Full Screen y Clic IzQuierdo----
        self.videoWidget.installEventFilter(self)# Conecte a las funciones de visualización del menú
        self.videoWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.videoWidget.customContextMenuRequested.connect(lambda: Menu_Clic.create_rightmenu(self))

        # ---- Conectar MediaPlayer ----
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.media_state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        ##Para color del Menú
        self.color_bg = str("#000000")
        self.color_color = str("blue")

        ##Para la Selección del Color en Menú
        self.color_bg_selection = str("#ffffff")
        self.color_color_selection = str("#000000")

        ##Definimos el Color del Menú, Click Izquierdo
        self.menu_color = str(f"background-color:{self.color_bg} ; color: {self.color_color} ; selection-background-color: {self.color_bg_selection} ; selection-color: {self.color_color_selection} ")

        # Create Font Size, Font Bold, Font Wieight, Font PonintSize
        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setWeight(50)

##=============================================================================================
##=============================================================================================

## Metodo para Hacer Full Screen el Widget del Video (QMediaPlayer())
## Metodo (Original), con (MouseButtonDblClick)
    def eventFilter(self, obj, event):

        ## print(event.type())
        ## print(help(QEvent))  ##<-Para Obtener Alluda Sobre Todos los Eventos en la App.-

        self.Objeto_Video = obj   ## Variable que Copia el (obj)

        if event.type() == QEvent.MouseButtonDblClick:
            obj.setFullScreen(not obj.isFullScreen())
            self.play()

        elif event.type() == QEvent.MouseButtonPress:
            self.play()

        return False

    # ============================================================
    # --------------MODO EXPANDIDO DE LOS VIDEOS  ----------------
    # ============================================================
    def set_aspect_ratio_mode(self, mode):        
        self.videoWidget.setAspectRatioMode(mode)

    # -----------------------------
    #  Señales / eventos
    # -----------------------------
    def _request_close(self):
        """Notifica a MainWindow que este video debe cerrarse."""
        self.request_close.emit(self)

    def mousePressEvent(self, event):
        if self.videoWidget.underMouse():
            self.clicked.emit(self)
        super().mousePressEvent(event)

    def wheelEvent(self, event):
        if self.videoWidget.underMouse():
            delta = event.angleDelta().y()
            if delta > 0:
                self.volumeSlider.setValue(self.volumeSlider.value() + 5)
            else:
                self.volumeSlider.setValue(self.volumeSlider.value() - 5)
            event.accept()
        else:
            event.ignore()

    # -----------------------------
    #   Acorta el Nombre
    # -----------------------------
    def acortando_title(self, text, length=40):

        name, ext = os.path.splitext(text)

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ....{ext}"

    # -----------------------------
    #   Carga de archivo, desde Principal
    # -----------------------------
    def open_file(self, file_path):

        # 🔥 LIMPIAR antes de cargar
        self.file_path_vid.clear()
        self.playlist.clear()

        for i in file_path:
            self.file_path_vid.append(i)

        if file_path:

            file_path = self.file_path_vid[0]
            self.playButton.setEnabled(True)
            self.sigButton.setEnabled(True)
            self.atrasButton.setEnabled(True)
            self.stopButton.setEnabled(True)
            #self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))

            self.playlist = QMediaPlaylist()
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(file_path)))

            self.mediaPlayer.setPlaylist(self.playlist)
            self.mediaPlayer.playlist().setCurrentIndex(self.index)
            #self.mediaPlayer.play()
            
            # Asignar título basado en el nombre del archivo
            name1 = os.path.basename(file_path)
            name = self.acortando_title(name1)
            self.titleLabel.setText(name)

    # -----------------------------
    #   Controles
    # -----------------------------
    def load(self, source):

        self.playlist.clear()
        #self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(source)))
        self.index = self.file_path_vid.index(f"{source}")

        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(source)))

        self.mediaPlayer.setPlaylist(self.playlist)
        self.mediaPlayer.playlist().setCurrentIndex(self.index)
        ## self.mediaPlayer.play()

    def load_selected(self, index):

        self.index = self.file_path_vid.index(f"{index}")

        name = self.file_path_vid[self.index]
        source_path = Path.resource_path(f"{name}")
        source = str(source_path)

        # Asignar título basado en el nombre del archivo
        name1 = os.path.basename(source)
        name = self.acortando_title(name1)
        self.titleLabel.setText(name)

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.load(source)
            self.mediaPlayer.play()

    def play(self):

        try:

            name = self.file_path_vid[self.index]
            name = Path.resource_path(f"{name}")
            fpath, fname = os.path.split(name)
            self.titleLabel.setText(fname)

            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.mediaPlayer.pause()
            else:
                self.mediaPlayer.play()

        except Exception as e:
            print(e)

            self.index = 0

    def stop(self):
        self.mediaPlayer.stop()

    def siguiente(self):

        try:

            self.index += 1
            self.load(self.file_path_vid[self.index])
            self.play()

        except Exception as e:
            print(e)

            self.index = 0
            self.load(self.file_path_vid[self.index])
            self.play()

    def atras(self):

        try:

            self.index -= 1
            self.load(self.file_path_vid[self.index])
            self.play()

        except Exception as e:
            print(e)

            self.index = 0
            self.load(self.file_path_vid[self.index])
            self.play()

    def set_volume(self, volume):
        self.mediaPlayer.setVolume(volume)

    def Muted_Vol(self):

        if self.mediaPlayer.isMuted() == True:
            self.mediaPlayer.setMuted(False)

            self.muted = Path.resource_path('assets\\Ico\\volume-off.png')
            self.icon_muted.addPixmap(QPixmap(self.muted), QIcon.Normal, QIcon.Off)
            self.btn_muted.setIcon(self.icon_muted)
            self.btn_muted.setIconSize(QtCore.QSize(18, 18))

        else:

            self.mediaPlayer.setMuted(True)

            self.muted = Path.resource_path('assets\\Ico\\volume-down.png')
            self.icon_muted.addPixmap(QPixmap(self.muted), QIcon.Normal, QIcon.Off)
            self.btn_muted.setIcon(self.icon_muted)
            self.btn_muted.setIconSize(QtCore.QSize(18, 18))

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    # -----------------------------
    #   Actualización UI
    # -----------------------------
    def media_state_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.positionSlider.setValue(position)
        self.currentTimeLabel.setText(self.format_time(position))

    def duration_changed(self, duration):
        self.positionSlider.setRange(0, duration)
        self.totalTimeLabel.setText(self.format_time(duration))

    # -----------------------------
    #   Utilidad formato de tiempo
    # -----------------------------
    def format_time(self, ms):
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def handle_status(self, status):

        try:
            # 🔥 AQUÍ ESTÁ LA MAGIA
            if status == QMediaPlayer.EndOfMedia:
                ###self.index += 1
                self.siguiente()

        except Exception as e:
            print(e)
            # 🔥 AQUÍ ESTÁ LA MAGIA
            if status == QMediaPlayer.EndOfMedia:
                self.index = 0
                self.siguiente()

    def show_window_two(self):  ## Creamos la Ventana Emergente para Ver la Lista en Reproducción.-

        self.List = QtWidgets.QWidget()
        New_Win.File_List_rep(self, self.List)
        self.List.show()

    def dialog_Warning(self, e):

        QMessageBox.warning(self, 'Precaución', 'Ya no hay medios para Reproducir\nAgrega Medios para su reproducción\n\nMuchas Gracias')

    def reduce_speed(self):
        """Reduce la velocidad de reproducción"""
        current_rate = self.mediaPlayer.playbackRate()
        new_rate = max(0.25, current_rate - 0.25)  # Mínimo 0.25x
        self.mediaPlayer.setPlaybackRate(new_rate)
        self.speed_label.setText(f"{new_rate:.1f}x")

    def increase_speed(self):
        """Aumenta la velocidad de reproducción"""
        current_rate = self.mediaPlayer.playbackRate()
        new_rate = min(3.0, current_rate + 0.25)  # Máximo 3.0x
        self.mediaPlayer.setPlaybackRate(new_rate)
        self.speed_label.setText(f"{new_rate:.1f}x")

##=========================================================================================================
##=========================================================================================================

class New_Win(VideoPlayerWidget):

    def __init__(self):
        super().__init__()

    def File_List_rep(self, List):

        List.setWindowTitle("File Name List.:")
        List.resize(600, 300)
        List.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.Ico_app = Path.resource_path('Ico\\1.png')
        List.setWindowIcon(QIcon(self.Ico_app))

        ##=================================================================================================
        ##=================================================================================================
        
        self.Ico_app = Path.resource_path('Ico\\1.png')
        List.setWindowIcon(QIcon(self.Ico_app))

        ##=================================================================================================
        ##=================================================================================================
        
        self.gridLayout = QtWidgets.QGridLayout(List)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")

        ##=================================================================================================
        ##=================================================================================================
        
        self.frame = QtWidgets.QFrame(List)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        ##=================================================================================================
        ##=================================================================================================
        
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        ##=================================================================================================
        ##=================================================================================================
        
        self.tableView = QtWidgets.QTableWidget(self.frame)
        self.tableView.setObjectName("tableView")
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.tableView.setFont(font)
        self.tableView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tableView.setStyleSheet("color: #17b4ff;\n"   ##> : rgba(255, 255, 255)  ##->Names Vid´s (Seleste-Azul-Claro)
"background-color: #000000 ;\n"   ##> : rgba(0, 0, 0, 0)    ##->Color Fondo de Pantalla (Negro)
"\n"
"selection-background-color: rgb(255, 140, 64);\n"
"selection-color: rgb(255, 255, 255);\n"
"padding:10px;\n"
"")
        self.tableView.setRowCount(0)

        self.tableView.setColumnCount(2)
        columnheaders = ['ID_File', 'File Name']

        self.tableView.setHorizontalHeaderLabels(columnheaders)

        self.gridLayout_2.addWidget(self.tableView, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        
        # Menú contextual
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(lambda posicion: New_Win.menuContextual(self, posicion))

        ##=================================================================================================
        ##=================================================================================================
        
        QtCore.QMetaObject.connectSlotsByName(List)
        self.tableView.clicked.connect(lambda e: New_Win.btn_press(self, e))

        ##=================================================================================================
        ##=================================================================================================

        self.WinNew_ListVids = List
        New_Win.insert_items(self)

        ##=================================================================================================
        ##=================================================================================================

    def insert_items(self):

        self.tableView.clear()
        self.tableView.setColumnCount(2)
        columnheaders = ['ID_File', 'File Name']

        self.tableView.setHorizontalHeaderLabels(columnheaders)
        self.tableView.setRowCount(0)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setTextElideMode(Qt.ElideRight)
        self.tableView.setWordWrap(False)
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        for indice, ancho in enumerate((50, 120), start=0):
            self.tableView.setColumnWidth(indice, ancho)

        if self.file_path_vid == [] or self.file_path_vid == "":
            pass

        else:
            i = len(self.file_path_vid)

            self.tableView.setHorizontalHeaderLabels(columnheaders)
            self.tableView.setRowCount(i)

            Cont = 0
            for rows in self.file_path_vid:

                fpath, fname = os.path.split(rows)

                Cant = Cont+1
                self.tableView.setItem(Cont, 0, QtWidgets.QTableWidgetItem(str(Cant)))
                self.tableView.setItem(Cont, 1, QtWidgets.QTableWidgetItem(fname))
                Cont += 1

    def find_id(self):

        row = self.tableView.currentRow()
        item = self.tableView.item(row, 0)

        if item is not None:

            self.name_item = item.text()

            name_fil = int(self.name_item)
            self.index = name_fil-1

    def btn_press(self, e=None):

            New_Win.find_id(self)
            New_Win.Capture_Event_List(self)

    def Capture_Event_List(self):
        
        try:

            VideoPlayerWidget.stop(self)
            self.playlist.clear()

            print(self.file_path_vid[self.index])


            VideoPlayerWidget.load(self, self.file_path_vid[self.index])        
            VideoPlayerWidget.play(self)

        except Exception as e:
            print(e)

            if self.check_2 == True:

                VideoPlayerWidget.siguiente(self)

            elif self.check_2 == False:

                VideoPlayerWidget.stop(self)
                VideoPlayerWidget.dialog_Warning(self, e)

##==========================================================================================
##==========================================================================================

    def menuContextual(self, posicion):
        indices = self.tableView.selectedIndexes()

        if indices:

            menu = QMenu()

            itemsGrupo = QActionGroup(self)
            itemsGrupo.setExclusive(True)

            open_file = menu.addAction(QAction("Open Directorio Del Video?", itemsGrupo))
            open_file = menu.addAction(QAction("Borrar de la Lista de Rep?", itemsGrupo))

            itemsGrupo.triggered.connect(lambda accion: New_Win.copiarTableWidgetItem(self, accion))            
            menu.exec_(self.tableView.viewport().mapToGlobal(posicion))

    def copiarTableWidgetItem(self, accion):
        filaSeleccionada = [dato.text() for dato in self.tableView.selectedItems()]
        
        fpath, fname = os.path.split(self.file_path_vid[self.index])
        path = str(fpath+"/")
            
        if accion.text() == "Open Directorio Del Video?":
            webbrowser.open(f'{path}/')

        elif accion.text() == "Borrar de la Lista de Rep?":

            filaSeleccionada = self.tableView.selectedItems()

            if filaSeleccionada:
                fila = filaSeleccionada[0].row()
                self.tableView.removeRow(fila)

                self.tableView.clearSelection()
                self.file_path_vid.remove(self.file_path_vid[self.index])

                self.index -= 1
                VideoPlayerWidget.siguiente(self)
                New_Win.limpiarTabla(self)
                New_Win.insert_items(self)

    def limpiarTabla(self):
        self.tableView.clearContents()
        self.tableView.setRowCount(0)

##=============================================================================================
##=============================================================================================
##Clase Menú Clic Izquierdo
class Menu_Clic(VideoPlayerWidget):

    def __init__(self):
        super().__init__()

    def create_rightmenu(self):

        # Objeto de menú
        self.groupBox_menu = QMenu(self)
        self.groupBox_menu.setFont(self.font)
        self.groupBox_menu.setStyleSheet(self.menu_color)

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.edit_ico = Path.resource_path('Ico\\Ok-icon.png')
        self.table_submenu = self.groupBox_menu.addMenu(QIcon(self.edit_ico), '&Lista Previa de los (ITEM´s)')

        self.Lista_file = Path.resource_path('Ima_Menu\\list.png')
        self.lbl_list = QAction(QIcon(self.Lista_file), '&Listas de Reproducción', self)
        self.lbl_list.setShortcut('L')

        self.lbl_list.setStatusTip("List_Rep.")
        self.lbl_list.triggered.connect(lambda: VideoPlayerWidget.show_window_two(self))
        self.table_submenu.addAction(self.lbl_list)
        
        self.table_submenu.addSeparator()
        self.table_submenu.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.Full_Screen1 = Path.resource_path('assets\\Ico\\expand.png')
        self.Full_Screen = QAction(QIcon(self.Full_Screen1), 'Full Screen Video', self)
        self.Full_Screen.triggered.connect(lambda: full_screen_video.Full_Screen_Video(self)) 
        self.groupBox_menu.addAction(self.Full_Screen)

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        self.groupBox_menu.addSeparator()
        self.groupBox_menu.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.edit_ico = Path.resource_path('Ico\\png\\Ok-icon.png')
        self.aspect_ratio = self.groupBox_menu.addMenu(QIcon(self.edit_ico), '&Proporcionar Pantalla')

        self.aspect_ratio.addSeparator()
        self.aspect_ratio.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.agregar_nuevo = Path.resource_path('Ico\\plus.png') 
        self.original_aspect_action = QAction(QIcon(self.agregar_nuevo), 'Original', self)
        self.original_aspect_action.setShortcut('7')

        self.original_aspect_action.setStatusTip('Original')        
        self.original_aspect_action.triggered.connect(lambda: VideoPlayerWidget.set_aspect_ratio_mode(self, Qt.IgnoreAspectRatio))
        self.aspect_ratio.addAction(self.original_aspect_action)

        self.aspect_ratio.addSeparator()
        self.aspect_ratio.addSeparator()

        self.agregar_nuevo = Path.resource_path('Ico\\plus.png') 
        self.keep_aspect_action = QAction(QIcon(self.agregar_nuevo), 'Keep Aspect Ratio', self)
        self.keep_aspect_action.setShortcut('8')

        self.keep_aspect_action.setStatusTip('Keep Aspect Ratio')        
        self.keep_aspect_action.triggered.connect(lambda: VideoPlayerWidget.set_aspect_ratio_mode(self, Qt.KeepAspectRatio))
        self.aspect_ratio.addAction(self.keep_aspect_action)

        self.aspect_ratio.addSeparator()
        self.aspect_ratio.addSeparator()

        self.agregar_nuevo = Path.resource_path('Ico\\plus.png') 
        self.crop_aspect_action = QAction(QIcon(self.agregar_nuevo), 'Crop Aspect Ratio', self)
        self.crop_aspect_action.setShortcut('9')

        self.crop_aspect_action.setStatusTip('Crop Aspect Ratio')        
        self.crop_aspect_action.triggered.connect(lambda: VideoPlayerWidget.set_aspect_ratio_mode(self, Qt.KeepAspectRatioByExpanding))
        self.aspect_ratio.addAction(self.crop_aspect_action)

        self.aspect_ratio.addSeparator()
        self.aspect_ratio.addSeparator()

        ##================================================================================================================
        ##================================================================================================================

        self.groupBox_menu.popup(QCursor.pos())

##=============================================================================================
##=============================================================================================
## Clase para Hacer Full Screen el Widget del Video (QMediaPlayer())
class full_screen_video(VideoPlayerWidget):

    def __init__(self):
        super().__init__()

    ## Metodo (Copia), para poder utilizar la Tecla (F11) o (Menú-Full_Screen)
    def Full_Screen_Video(self):
        global obj_vid

        obj_vid = self.Objeto_Video  ## Variable que Copia el (obj)

        if obj_vid == self.Objeto_Video:
                obj_vid.setFullScreen(not obj_vid.isFullScreen())

##=============================================================================================
##=============================================================================================