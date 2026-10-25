
# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Desarrollado Por: Cristian M. Veliz Cano
'''
##=========================================================================================================
##=========================================================================================================
import sys, os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, 
							 QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush
# IMPORTA TU VLC PLAYER
from MiniPlayer_VLC_v1 import Player

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
##=========================================================================================================
##=========================================================================================================

class LauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MiniPlayer_VLC")

        # Colocamos un Icono
        self.Ico_app = Path.resource_path('Ico\\VLC.ico')
        self.setWindowIcon(QIcon(self.Ico_app))
        self.setFixedSize(420, 260)  # Establece el tamaño fijo de la ventana
        self.center_on_screen()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        bg_path = Path.resource_path("Ico/1.jpg")
        pixmap = QPixmap(bg_path)

        palette = QPalette()
        palette.setBrush(
            QPalette.Window,
            QBrush(
                pixmap.scaled(
                    self.size(),
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation
                )
            )
        )

        self.setPalette(palette)

        # --- Área central ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)

        # --- BOTÓN ÚNICO ---
        self.open_button = QPushButton("Buscar y Abrir Video")
        self.open_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
        #self.open_button.setFixedSize(220, 60)

        self.open_button.clicked.connect(self.open_video_dialog)
        layout.addWidget(self.open_button)

        # Ventana del reproductor VLC
        self.player_window = None

    def center_on_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = 400, 150
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2
        self.setGeometry(x, y, w, h)

    def open_video_dialog(self):
        """Abre diálogo para seleccionar un archivo de video."""
        file_filter = "Videos (*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm *.mp4v *.avf *.divx \
        			  *.mpg *.m4a *.rmvb *.gif *.wap *.webm *.cda *.flac *.mp3);;Todos (*.*)"

        file_path, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar video", "", file_filter
        )

        if file_path:
            self.show_player_window(file_path)

    def show_player_window(self, video_path):
        """Crea y muestra la ventana del VLC Player."""
        
        # Si ya existe una ventana previa → se cierra
        if self.player_window:
            self.player_window.close()
            self.player_window = None

        # Crear la ventana contenedora
        self.player_window = QMainWindow()
        self.player_window.setWindowTitle("Mini Reproductor VLC")
        self.Ico_app = Path.resource_path('Ico\\1.png')
        self.player_window.setWindowIcon(QIcon(self.Ico_app))
        
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = 700, 500
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2
        self.player_window.setGeometry(x, y, w, h)

        # Crear tu reproductor VLC
        vlc_widget = Player([video_path])  # Acepta lista
        self.player_window.setCentralWidget(vlc_widget)

        # Mostrar
        self.player_window.show()

        # Iniciar reproducción
        try:
            vlc_widget.playlist_start()
        except:
            pass  # por si tu módulo arranca solo

##=========================================================================================================
##=========================================================================================================
def main():
    app = QApplication(sys.argv)
    win = LauncherWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
##=========================================================================================================
##=========================================================================================================