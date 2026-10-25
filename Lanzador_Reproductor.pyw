
# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
====================================================================================
Desarrollado Por: Cristian M. Veliz Cano
Versión del Soft: V-01
Nombre del Soft: "Lanzador de Video Individual"
Distribución: Gratuito --> OPEN-SOURCE / FREE-CODE <--
Licencia: MIT License
Tecnologías: Python + PyQt5
Módulos de Reproducción:
    - Video_Player_Widget_Logic_v3.py
    - MiniPlayer_VLC_v1.py
====================================================================================

LANZADOR DE VIDEO INDIVIDUAL
Interfaz Gráfica para la Selección y Reproducción de Vídeos

DESCRIPCIÓN GENERAL:

Lanzador de Video Individual es una aplicación de escritorio desarrollada en
Python mediante PyQt5, diseñada para ofrecer acceso a dos alternativas de
reproducción de archivos multimedia desde una misma ventana principal.

La aplicación permite seleccionar vídeos del equipo y abrirlos mediante uno
de los dos módulos de reproducción integrados: un reproductor basado en un
widget personalizado de vídeo y un reproductor que utiliza VLC.

Su interfaz gráfica dispone de dos opciones principales, cada una asociada
a un módulo diferente. Antes de utilizar los reproductores, presenta avisos
informativos sobre los componentes multimedia necesarios para su funcionamiento.

El programa incorpora ventanas independientes para la reproducción, iconos
personalizados, una imagen de fondo y un sistema de administración de rutas
preparado para localizar recursos tanto durante el desarrollo como en una
aplicación empaquetada con PyInstaller.

CARACTERÍSTICAS PRINCIPALES:

- Interfaz gráfica de escritorio desarrollada con PyQt5.
- Ventana principal con diseño compacto y tamaño fijo.
- Dos alternativas para abrir y reproducir archivos multimedia.
- Integración con un reproductor de vídeo basado en un widget personalizado.
- Integración con un reproductor basado en VLC Media Player.
- Selección de archivos multimedia mediante cuadros de diálogo.
- Compatibilidad con múltiples selecciones de archivos en los diálogos.
- Filtros para localizar formatos de vídeo y otros archivos multimedia.
- Apertura del reproductor en una ventana independiente.
- Cierre de una ventana de reproducción anterior antes de abrir otra.
- Centrado de las ventanas de reproducción en la pantalla.
- Iconos personalizados para la aplicación y sus reproductores.
- Imagen de fondo configurable mediante recursos externos.
- Avisos informativos sobre los requisitos de los reproductores.
- Enlaces a los sitios oficiales de K-Lite Codec Pack y VLC Media Player.
- Opción para abrir un instalador local de VLC desde la interfaz.
- Mensajes personalizados mediante cuadros de diálogo QMessageBox.
- Administración centralizada de las rutas de recursos.
- Compatibilidad prevista con la distribución mediante PyInstaller.

MÓDULOS DE REPRODUCCIÓN:

1. REPRODUCTOR PERSONALIZADO — MEDIA PLAYER

   Utiliza el módulo externo Video_Player_Widget_Logic_v3.py, desde el cual
   importa la clase VideoPlayerWidget.

   La aplicación crea una ventana independiente, carga los archivos
   seleccionados en el widget de reproducción y conecta la señal de cierre
   del reproductor con el método encargado de cerrar su ventana contenedora.

   El programa muestra un aviso informativo relacionado con los componentes
   de audio y vídeo necesarios para el funcionamiento de este módulo.

2. REPRODUCTOR VLC — MINI PLAYER

   Utiliza el módulo externo MiniPlayer_VLC_v1.py, desde el cual importa
   la clase Player.

   La aplicación crea una ventana independiente para el reproductor VLC,
   le entrega la lista de archivos seleccionados y solicita el inicio de
   la reproducción mediante el método playlist_start().

   El programa presenta un aviso sobre la versión de VLC indicada por el
   proyecto y proporciona acceso al instalador local configurado.

SELECCIÓN DE ARCHIVOS:

La aplicación dispone de cuadros de diálogo para localizar archivos en el
sistema de archivos del equipo.

Entre las extensiones contempladas por los filtros se encuentran:

- MP4
- MKV
- AVI
- MOV
- WMV
- FLV
- WEBM
- MPG
- MP4V
- DIVX
- M4A
- RMVB
- GIF
- FLAC
- MP3

Los formatos disponibles dependen del filtro utilizado en cada módulo y de
las capacidades del reproductor y sus componentes multimedia instalados.

INTERFAZ Y EXPERIENCIA DE USUARIO:

La ventana principal presenta dos secciones identificadas por el módulo
de reproducción correspondiente.

Cada sección dispone de un botón para seleccionar los archivos y abrir
el reproductor asociado.

El diseño incorpora botones con estilos QSS personalizados, colores
contrastantes, bordes redondeados y efectos visuales al pasar el cursor.

Los avisos se presentan mediante ventanas informativas personalizadas,
con iconos, textos explicativos, enlaces web y botones de respuesta.

ADMINISTRACIÓN DE RECURSOS:

La clase Path proporciona métodos para localizar los recursos utilizados
por la aplicación.

Entre los recursos contemplados se encuentran:

- Icono principal de la aplicación.
- Icono específico para VLC.
- Imagen de fondo de la ventana.
- Iconos empleados en los mensajes informativos.
- Instalador local de VLC.

La función resource_path() permite construir las rutas de los recursos
tanto durante la ejecución desde el código fuente como en entornos
empaquetados que utilicen el directorio temporal de PyInstaller.

TECNOLOGÍAS UTILIZADAS:

- Python 3: lenguaje de programación principal.
- PyQt5: desarrollo de la interfaz gráfica de usuario.
- Qt Widgets: creación de ventanas, botones, etiquetas y cuadros de diálogo.
- QMainWindow: ventanas principales y contenedoras de los reproductores.
- QFileDialog: selección de archivos multimedia.
- QMessageBox: presentación de avisos y opciones al usuario.
- QPixmap y QPalette: administración de imágenes y fondos visuales.
- QIcon: configuración de los iconos de la aplicación.
- QBrush y QColor: personalización de elementos visuales.
- Qt Style Sheets (QSS): personalización de los botones y la interfaz.
- webbrowser: apertura de recursos locales mediante el navegador o la
  aplicación asociada al sistema.
- PyInstaller: compatibilidad prevista con aplicaciones empaquetadas.
- VLC Media Player: reproducción multimedia mediante el módulo integrado.

ESTRUCTURA MODULAR:

El proyecto separa la ventana lanzadora de los módulos encargados de
reproducir los archivos multimedia.

Archivos principales:

- Lanzador de Video Individual: ventana de acceso a los reproductores.
- Video_Player_Widget_Logic_v3.py: módulo del reproductor personalizado.
- MiniPlayer_VLC_v1.py: módulo del reproductor VLC.
- Ico/: recursos gráficos e iconos.
- assets/: recursos adicionales para los mensajes.
- VLC/: ubicación prevista para el instalador local de VLC.

La disponibilidad de estos módulos y recursos depende de la estructura
de archivos utilizada al distribuir el proyecto.

APLICACIONES Y USOS:

- Reproducción de archivos de vídeo desde una interfaz unificada.
- Acceso a dos alternativas de reproducción multimedia.
- Organización de módulos de reproducción independientes.
- Consulta de archivos multimedia almacenados localmente.
- Integración de reproductores externos en aplicaciones PyQt5.
- Aprendizaje práctico del desarrollo de lanzadores multimedia.
- Experimentación con ventanas independientes y componentes gráficos.
- Distribución de herramientas multimedia de escritorio.

DISTRIBUCIÓN Y FILOSOFÍA DEL PROYECTO:

Lanzador de Video Individual busca reunir distintas alternativas de
reproducción multimedia en una aplicación sencilla y accesible.

Su estructura modular permite mantener separados el lanzador gráfico
y los componentes responsables de la reproducción.

El proyecto está orientado al uso personal, educativo y práctico,
con posibilidades de adaptación y ampliación según las necesidades
de cada usuario.

====================================================================================
Desarrollado por: Cristian M. Veliz Cano
Software gratuito y de código abierto (Open-Source).
====================================================================================
'''

import sys, os
import webbrowser as web

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QFileDialog, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QBrush

# Importamos la clase del reproductor desde el módulo
from Video_Player_Widget_Logic_v3 import VideoPlayerWidget
# IMPORTA VLC PLAYER
from MiniPlayer_VLC_v1 import Player
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

        self.aviso = True
        self.aviso2 = True

        # Widget central y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter) # Centrar el botón

        self.title = QLabel("Utilizar Modulo - [MediaPlayer]:")

        # Botón para buscar y abrir el video
        self.open_button = QPushButton("Buscar y Abrir Un Solo Video - [MediaPlayer]")
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
        self.open_button.clicked.connect(lambda: Launcher_media.open_video_dialog(self))
        layout.addWidget(self.title)
        layout.addWidget(self.open_button)

        self.title2 = QLabel("Utilizar Modulo - [VLC]:")

        # Botón para buscar y abrir el video
        self.open_button = QPushButton("Buscar y Abrir Multiples Video - [VLC]")
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
        self.open_button.clicked.connect(lambda: Launcher_vlc.open_video_dialog_vlc(self))
        layout.addWidget(self.title2)
        layout.addWidget(self.open_button)

        # Esta variable guardará la referencia a la ventana del reproductor
        self.player_window = None

    def center_on_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = 400, 150
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2
        self.setGeometry(x, y, w, h)

class Launcher_media(LauncherWindow):

    def __init__(self):
        super().__init__()

    def open_video_dialog(self):
        
        ## Aviso Preciso...
        Launcher_media.abiso(self)

        """Abre el diálogo para seleccionar un archivo de video."""
        # Filtro para tipos de video comunes
        file_filter = "Archivos de Video (*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm);;Todos los archivos (*.*)"
        
        file_path, _ = QFileDialog.getOpenFileNames(self, "Seleccionar un archivo de video", "", file_filter)

        if file_path:
            # Si se seleccionó un archivo, creamos la ventana emergente
            Launcher_media.show_player_window(self, file_path)

    def show_player_window(self, video_path):
        """Crea y muestra la ventana emergente con el reproductor de video."""
        # Si ya hay una ventana abierta, la cerramos para evitar múltiples instancias
        if self.player_window:
            self.player_window.close()

        # Creamos una nueva QMainWindow para la ventana emergente
        self.player_window = QMainWindow()
        self.player_window.setWindowTitle("Reproductor de Video")
        self.Ico_app = Path.resource_path('Ico\\1.Ico')
        self.player_window.setWindowIcon(QIcon(self.Ico_app))
        #self.player_window.setGeometry(300, 300, 800, 600) # Tamaño inicial de la ventana del video
        
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = 800, 600
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2
        self.player_window.setGeometry(x, y, w, h)

        # Creamos una instancia de TU widget de video
        player_widget = VideoPlayerWidget()

        # Configuramos la instancia de TU widget para que se comporte como una ventana independiente
        # Conectamos su señal de cierre a la función que cierra la ventana emergente
        player_widget.request_close.connect(lambda: Launcher_media.close_player_window(self))

        # Cargamos el video en el widget
        player_widget.open_file(video_path)

        # Establecemos el widget de video como el widget central de la ventana emergente
        self.player_window.setCentralWidget(player_widget)

        # Mostramos la ventana emergente
        self.player_window.show()

    def close_player_window(self):
        """Cierra la ventana del reproductor."""
        if self.player_window:
            self.player_window.close()
            self.player_window = None

    def abiso(self):

        if self.aviso == True:

            # Instanciamos la clase QMessageBox
            mensaje = QMessageBox(self)

            # Agregamos un icono al cuadro de mensaje
            self.Ico_app2 = Path.resource_path("assets\\icono.png")
            mensaje.setWindowIcon(QIcon(self.Ico_app2))

            # Agregamos un titulo al cuadro de mensaje
            mensaje.setWindowTitle("Mensaje personalizado")

            # Le damos color al fondo del cuadro de mensaje
            paleta = QPalette()
            colorPanel = QPalette.Background
            paleta.setColor(colorPanel, QColor("white"))
            mensaje.setPalette(paleta)

            # Cambiamos el tamaño de la letra del cuadro de mensaje
            fuente = self.font()
            fuente.setPointSize(10)
            mensaje.setFont(fuente)
                            
            # mensaje.setIcon(QMessageBox.Information)
            self.Logo_app = Path.resource_path("Ico\\Qt.png")
            mensaje.setIconPixmap(QPixmap(self.Logo_app).scaled(100, 100, Qt.KeepAspectRatio))
            
            msn = "Aviso, Es Necesario:\nPara poder Utilizar este modulo. Es \
preciso, tener Instalada\nCualquier verción, del Media-Player Clasick [K-Lite Codeck Pack].\nMuchas Gracias..."
            mensaje.setText(f"{msn}")
            mensaje.setInformativeText("""Muchas Gracias...""")

            mensaje.setInformativeText("""Esta es la WEB Oficial de K-Lite Codeck-Pack para Windows (x64bts) - <b>HTML</b>.
                                   <br/><br/> Sitio Oficial <b>URL</b>:
                                   <a href='https://codecguide.com/'>K-Lite Codeck-Pack</a>""")

            mensaje.setDetailedText("""Requiere de: - \"K-Lite Codeck-Pack\" -\n
En cualquier Verción, no precisa de ninguna en Especial, Solamente, por sus Codecks, de \
Video y Audio.\nMuchas, Gracias...""")

            # mensaje.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            botonAceptar = mensaje.addButton("Aceptar", QMessageBox.YesRole)
            #botonAbrir = mensaje.addButton("Instalar?", QMessageBox.AcceptRole)
            botonCancelar = mensaje.addButton("Cancelar", QMessageBox.RejectRole)
            
            mensaje.setDefaultButton(botonAceptar)            
            mensaje.exec_()

            if mensaje.clickedButton() == botonAceptar:
                self.aviso = False
                pass

            elif mensaje.clickedButton() == botonCancelar:
                self.aviso = False
                pass

        elif self.aviso == False:
            self.aviso = False
            pass

class Launcher_vlc(LauncherWindow):

    def __init__(self):
        super().__init__()

    def open_video_dialog_vlc(self):

        ## -->Aviso Inportante:
        Launcher_vlc.abiso(self)

        """Abre diálogo para seleccionar un archivo de video."""
        file_filter = "Videos (*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm *.mp4v *.avf *.divx \
                      *.mpg *.m4a *.rmvb *.gif *.wap *.webm *.cda *.flac *.mp3);;Todos (*.*)"

        file_path, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar video", "", file_filter
        )

        if file_path:
            Launcher_vlc.show_player_window(self, file_path)

    def show_player_window(self, video_path):
        """Crea y muestra la ventana del VLC Player."""
        
        # Si ya existe una ventana previa → se cierra
        if self.player_window:
            self.player_window.close()
            self.player_window = None

        # Crear la ventana contenedora
        self.player_window = QMainWindow()
        self.player_window.setWindowTitle("Mini Reproductor VLC")
        self.Ico_app = Path.resource_path('Ico\\VLC.ico')
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

    def abiso(self):

        ## -->Aviso2 Inportante:
        if self.aviso2 == True:

            # Instanciamos la clase QMessageBox
            mensaje = QMessageBox(self)

            # Agregamos un icono al cuadro de mensaje
            self.Ico_app2 = Path.resource_path("assets\\icono.png")
            mensaje.setWindowIcon(QIcon(self.Ico_app2))

            # Agregamos un titulo al cuadro de mensaje
            mensaje.setWindowTitle("Mensaje personalizado")

            # Le damos color al fondo del cuadro de mensaje
            paleta = QPalette()
            colorPanel = QPalette.Background
            paleta.setColor(colorPanel, QColor("white"))
            mensaje.setPalette(paleta)

            # Cambiamos el tamaño de la letra del cuadro de mensaje
            fuente = self.font()
            fuente.setPointSize(10)
            mensaje.setFont(fuente)
                            
            # mensaje.setIcon(QMessageBox.Information)
            self.Logo_app = Path.resource_path("Ico\\Qt.png")
            mensaje.setIconPixmap(QPixmap(self.Logo_app).scaled(100, 100, Qt.KeepAspectRatio))
            
            msn = "Es Necesario:\nPara poder Utilizar este modulo, es \
preciso, tener Instalada\nSolamente está verción, de vlc-3.0.11-win64."
            mensaje.setText(f"{msn}")
            mensaje.setInformativeText("""Muchas Gracias...""")

            mensaje.setInformativeText("""Esta es la WEB Oficial de <b>VLC Media Player para Windows (x64bts)</b>.
                                   <br/><br/> Sitio Oficial <b>URL</b>:
                                   <a href='https://www.videolan.org//'>VLC Media Player</a>""")

            mensaje.setDetailedText("""Requiere de: - \"VLC-3.2.11-win64(bits)\" -\n
Instalar si no lo tiene, porque sino no funcionara la api de -vlc.  ->O Descargarlo e Instalarlo...""")

            # mensaje.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            botonAceptar = mensaje.addButton("Aceptar", QMessageBox.YesRole)
            botonAbrir = mensaje.addButton("Instalar?", QMessageBox.AcceptRole)
            botonCancelar = mensaje.addButton("Cancelar", QMessageBox.RejectRole)
            
            mensaje.setDefaultButton(botonAceptar)
            
            mensaje.exec_()

            if mensaje.clickedButton() == botonAceptar:
                self.aviso2 = False
                pass

            elif mensaje.clickedButton() == botonAbrir:
                QMessageBox.information(self, "Aviso", "Sera Instalado el Programa: vlc-3.0.11-win64")
                dir_path_vlc = Path.resource_path("VLC\\vlc-3.0.11-win64.exe")
                web.open(dir_path_vlc)
                self.aviso2 = False

            elif mensaje.clickedButton() == botonCancelar:
                self.aviso2 = False
                pass

        elif self.aviso2 == False:
            self.aviso2 = False
            pass


# --- Función Principal para ejecutar la aplicación ---
def main():
    app = QApplication(sys.argv)
    launcher = LauncherWindow()
    launcher.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()