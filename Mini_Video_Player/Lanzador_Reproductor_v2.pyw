
# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Desarrollado Por: Cristian M. Veliz Cano
Verción del Soft: V-02
Nombre del Soft: Lanzador de Video Individual
Distribución: Gratuito  -->OPENSOURCE<--
'''
import sys, os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush

# Importamos la clase del reproductor desde tu módulo
from Video_Player_Widget_Logic_v3 import VideoPlayerWidget
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

# --- Ventana Principal (El Lanzador) ---
class LauncherWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lanzador de Video Individual")
        self.Ico_app = Path.resource_path('Ico\\1.Ico')
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

        self.player_windows = []

        # Widget central y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter) # Centrar el botón

        # Botón para buscar y abrir el video
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
        self.open_button.clicked.connect(self.open_video_dialog)

        layout.addWidget(self.open_button)

        # Esta variable guardará la referencia a la ventana del reproductor
        self.player_window = []

    def center_on_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = 420, 260
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2
        self.setGeometry(x, y, w, h)

    def open_video_dialog(self):
        """Abre el diálogo para seleccionar un archivo de video."""
        # Filtro para tipos de video comunes
        file_filter = "Archivos de Video (*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm);;Todos los archivos (*.*)"
        
        file_path, _ = QFileDialog.getOpenFileNames(self, "Seleccionar un archivo de video", "", file_filter)

        if file_path:
            # Si se seleccionó un archivo, creamos la ventana emergente
            self.show_player_window(file_path)

    def show_player_window(self, video_path):
        """Crea y muestra una nueva ventana con el reproductor de video."""

        player_window = QMainWindow()
        player_window.setWindowTitle("Reproductor de Video")
        self.Ico_app = Path.resource_path('Ico\\1.ico')
        player_window.setWindowIcon(QIcon(self.Ico_app))

        screen = QApplication.primaryScreen().availableGeometry()
        w, h = 800, 600
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2
        player_window.setGeometry(x, y, w, h)

        player_widget = VideoPlayerWidget()

        # conectar señal de cierre
        player_widget.request_close.connect(
            lambda: self.close_player_window(player_window)
        )

        player_widget.open_file(video_path)

        player_window.setCentralWidget(player_widget)

        # guardar referencia
        self.player_windows.append(player_window)

        player_window.show()

    def close_player_window(self, window):
        """Cierra una ventana específica."""
        if window in self.player_windows:
            window.close()
            self.player_windows.remove(window)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape: ## Key Board (Teclado - Tecla Escape (ESC))
            sys.exit()              ## Exit (Clouse App) Cerrar la Aplicación

##-------------------------------------------------------------------------
##-------------------------------------------------------------------------
# --- Función Principal para ejecutar la aplicación ---
def main():
    app = QApplication(sys.argv)
    launcher = LauncherWindow()
    launcher.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
##-------------------------------------------------------------------------
##-------------------------------------------------------------------------