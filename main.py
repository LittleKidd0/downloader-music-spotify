import sys
import json
import os
import time
import webbrowser
import platform
from io import BytesIO
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QLabel, 
                             QMessageBox, QTextEdit, QSizePolicy, QScrollArea, 
                             QGridLayout, QSlider, QFrame) 
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QRegion
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import qdarktheme

# --- IMPORTACIONES DE MUTAGEN (Requiere: pip install mutagen) --- Downloader
try:
    from mutagen.mp3 import MP3
    from mutagen.mp4 import MP4, MP4Cover 
    from mutagen.id3 import ID3NoHeaderError, APIC
    from mutagen.easyid3 import EasyID3 
    from mutagen.easymp4 import EasyMP4
except ImportError:
    print("------------------------------------------------------------------")
    print("¡ERROR! Falta la librería 'mutagen'.")
    print("Por favor, ejecuta en tu terminal: pip install mutagen")
    print("------------------------------------------------------------------")
    sys.exit(1)

# --- CONFIGURACIÓN Y UTILIDADES GLOBALES ---

system_ = platform.system()

# Ruta a la carpeta de música de Windows (ajustada para Windows 10)
if system_ == "Windows":
    MUSIC_FOLDER = os.path.join(os.path.expanduser("~"), "Music")
else:
    MUSIC_FOLDER = os.path.join(os.path.expanduser("~"), "Music") 

def remove_temp_files():
    """Limpia los archivos JSON temporales generados por los scripts de Node."""
    files_to_remove = ['data.json', 'final.json', 'datos2.json', 'links.json', 'datos3.json']
    for file in files_to_remove:
        try:
            os.remove(file)
        except OSError:
            pass # Ignorar si el archivo no existe

def load_json(file_name):
    """Carga datos desde un archivo JSON, manejando errores de lectura."""
    try:
        with open(file_name, 'r', encoding='utf8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def run_node_module(app_instance, script, *args):
    """Ejecuta un script de Node.js y dirige la salida a la consola de logs."""
    command = f"node ./modulos/{script} {' '.join(args)}"
    app_instance.log_message(f"[CMD] Ejecutando: {command}", color="gray")
    
    try:
        # Usamos os.popen para capturar la salida de la consola del script de Node
        with os.popen(command) as process:
            output = process.read()
            app_instance.log_message(f"[NODE LOG] {output.strip()}", color="darkgray")
            
    except Exception as e:
        app_instance.log_message(f"ERROR al ejecutar Node: {e}", color="red")
        
    app_instance.log_message(f"[CMD] Finalizado: {script}", color="gray")

def get_album_art(song_path):
    """Extrae la carátula de un archivo MP3 o M4A usando mutagen."""
    image_data = None
    
    try:
        if song_path.lower().endswith(('.mp3', '.flac', '.wav')):
            audio = MP3(song_path)
            if audio.tags is not None:
                # Buscar carátulas tipo 'APIC'
                for tag in audio.tags.values():
                    if isinstance(tag, APIC):
                        image_data = tag.data
                        break
        
        elif song_path.lower().endswith(('.m4a', '.mp4')):
            audio = MP4(song_path)
            if 'covr' in audio.tags and audio.tags['covr']:
                # Las carátulas M4A son listas de MP4Cover o bytes
                cover = audio.tags['covr'][0]
                if isinstance(cover, MP4Cover):
                     image_data = cover
                else:
                    image_data = cover
        
    except ID3NoHeaderError:
        pass
    except Exception as e:
        pass
        
    return image_data

# --- Clase Personalizada para el Cuadrado de la Canción (Carátula) ---

class SongSquare(QFrame):
    """Widget que muestra la carátula y el nombre de la canción, y maneja clics."""
    def __init__(self, song_name, song_path, app_instance, parent=None):
        super().__init__(parent)
        self.song_name = song_name
        self.song_path = song_path
        self.app_instance = app_instance
        self.setFixedSize(120, 150)

        # Estilo base
        self.setStyleSheet("""
            SongSquare {
                background-color: #282828;
                border: 1px solid #282828; 
                border-radius: 5px;
            }
            SongSquare:hover {
                background-color: #404040;
                border: 1px solid #1DB954;
            }
            QLabel {
                background-color: transparent;
                color: white;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignCenter)
        
        # 1. Carátula (Imagen)
        self.cover_label = QLabel()
        self.cover_label.setAlignment(Qt.AlignCenter)
        self.cover_label.setFixedSize(110, 110)
        self.cover_label.setStyleSheet("background-color: #404040; border-radius: 5px;")
        self._load_cover_art()

        # 2. Nombre de la canción
        display_name = song_name.replace(".mp3", "").replace(".m4a", "")
        if len(display_name) > 15:
            display_name = display_name[:12] + "..."
            
        self.title_label = QLabel(display_name)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setToolTip(song_name)
        self.title_label.setStyleSheet("color: white; font-size: 8pt;")
        
        layout.addWidget(self.cover_label)
        layout.addWidget(self.title_label)
        
    def _load_cover_art(self):
        """Carga la carátula del archivo de audio o muestra un placeholder."""
        image_data = get_album_art(self.song_path)
        
        if image_data:
            pixmap = QPixmap()
            if pixmap.loadFromData(image_data):
                scaled_pixmap = pixmap.scaled(self.cover_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.cover_label.setPixmap(scaled_pixmap)
                return
            
        # Placeholder si no hay imagen o falla la carga
        self.cover_label.setText("🎶") 
        self.cover_label.setStyleSheet("font-size: 50pt; background-color: #404040; border-radius: 5px; color: lightgray;")


    def mousePressEvent(self, event):
        """Maneja el evento de clic para reproducir la canción."""
        if event.button() == Qt.LeftButton:
            self.app_instance._load_local_track_by_path(self.song_path, self.song_name)

# --- Clase Principal de la GUI ---

class SpotifyDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Downloader - v1.5 GUI | Littlekidd0")
        self.setGeometry(100, 100, 950, 750) 
        
        # --- RUTA DE MÚSICA LOCAL ---
        self.local_music_dir = MUSIC_FOLDER 
        
        # --- Listas de canciones y estado de reproducción ---
        self.available_songs = [] 
        self.current_track_index = -1
        
        self.mediaPlayer = QMediaPlayer(self)
        self.mediaPlayer.setVolume(70) 
        self.current_track_path = None
        self.is_playing = False

        script_dir = os.path.dirname(__file__) 
        self.logo_path = os.path.join(script_dir, 'modulos/imagenes/logo.png')
        
        self._main_widget = QWidget()
        self.setCentralWidget(self._main_widget)
        self.layout = QVBoxLayout(self._main_widget)
        
        self._setup_ui()
        
        # Conexiones del reproductor
        self.mediaPlayer.positionChanged.connect(self._update_position)
        self.mediaPlayer.durationChanged.connect(self._update_duration)
        self.mediaPlayer.stateChanged.connect(self._update_player_state)
        self.mediaPlayer.stateChanged.connect(self._handle_media_finished)

    # --- Log y Utilidades ---

    def log_message(self, message, color="white"):
        timestamp = time.strftime("[%H:%M:%S]")
        formatted_message = f'<span style="color: lightgray;">{timestamp}</span> <span style="color: {color};">{message}</span>'
        
        if hasattr(self, 'log_console'):
            self.log_console.append(formatted_message)
        else:
            print(f"LOG: {message}")

    # --- Métodos de UI y Estructura ---

    def _setup_ui(self):
        
        # --- Logo en la interfaz ---
        logo_label_layout = QHBoxLayout()
        logo_label_layout.setAlignment(Qt.AlignCenter) 
        logo_label = QLabel()
        
        if os.path.exists(self.logo_path):
            pixmap = QPixmap(self.logo_path)
            scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setStyleSheet("border: none; background-color: transparent;")
            self.log_message(f"[INIT] Logo de la aplicación cargado.", color="lightgreen")
        else:
             logo_label.setText("Downloader - v1.5 GUI")
             logo_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: #1DB954;")
             self.log_message(f"[ERROR] No se encontró el archivo del logo: {self.logo_path}", color="red")
            
        logo_label_layout.addWidget(logo_label)
        self.layout.addLayout(logo_label_layout) 
        
        # Inicializar módulos de Node
        self.log_message("[INIT] Inicializando módulos de Node...", color="yellow")
        QTimer.singleShot(10, lambda: run_node_module(self, "src/prueba_de_pagina.js"))
        QTimer.singleShot(50, lambda: self.log_message("[INIT] Inicialización Node en curso...", color="#1DB954"))
        
        # --- Sección de Navegación/Opciones ---
        options_layout = QHBoxLayout()
        options_layout.setAlignment(Qt.AlignCenter)
        self.btn_track = self._create_nav_button("Descargar Pista Única", self._show_track_view)
        self.btn_album = self._create_nav_button("Descargar Álbum", self._show_album_view)
        self.btn_playlist = self._create_nav_button("Descargar Playlist (👷)", self._show_playlist_view)
        self.btn_local = self._create_nav_button("🎵 Archivos Locales", self._show_local_view)
        options_layout.addWidget(self.btn_track)
        options_layout.addWidget(self.btn_album)
        options_layout.addWidget(self.btn_playlist)
        options_layout.addWidget(self.btn_local)
        self.layout.addLayout(options_layout)
        
        # --- Contenedores de Vistas ---
        self.download_container = QWidget()
        self.download_layout = QVBoxLayout(self.download_container)
        self.download_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.local_container = QWidget()
        self.local_layout = QHBoxLayout(self.local_container) 
        self.local_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.local_container.setVisible(False)
        
        self.main_content_stack = QVBoxLayout()
        self.main_content_stack.addWidget(self.download_container)
        self.main_content_stack.addWidget(self.local_container)
        self.layout.addLayout(self.main_content_stack)
        
        self._init_download_views()
        self._init_local_view_ui() 
        
        # --- Consola de Logs (QTextEdit) ---
        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setMaximumHeight(150)
        self.log_console.setStyleSheet("background-color: #191414; color: white; border: 1px solid #1DB954;")
        self.log_console.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.log_console)
        
        self.log_message("Consola de Logs lista.", color="#1DB954")
        
        # --- Botones inferiores ---
        bottom_layout = QHBoxLayout()
        self.btn_creator = self._create_simple_button("Página del Creador", self._open_creator_page)
        self.btn_clear_log = self._create_simple_button("Limpiar Log", self.log_console.clear)
        self.btn_exit = self._create_simple_button("Salir", self.close)
        bottom_layout.addWidget(self.btn_creator)
        bottom_layout.addWidget(self.btn_clear_log)
        bottom_layout.addWidget(self.btn_exit)
        self.layout.addLayout(bottom_layout)
        
        self._show_track_view()

    # --- Métodos de UI / Navegación (Descarga) ---

    def _create_nav_button(self, text, handler):
        btn = QPushButton(text)
        btn.clicked.connect(handler)
        btn.setFixedSize(180, 40)
        btn.setStyleSheet("QPushButton {border: none; padding: 10px; font-weight: bold; background-color: #282828; color: white;} QPushButton:hover {background-color: #404040;} QPushButton:checked {background-color: #1DB954; color: black;}")
        btn.setCheckable(True)
        return btn

    def _create_simple_button(self, text, handler):
        btn = QPushButton(text)
        btn.clicked.connect(handler)
        btn.setFixedSize(150, 30)
        return btn

    def _clear_nav_buttons(self):
        for btn in [self.btn_track, self.btn_album, self.btn_playlist, self.btn_local]:
            btn.setChecked(False)

    def _init_download_views(self):
        self.track_widget = QWidget()
        self.track_layout = QVBoxLayout(self.track_widget)
        self.track_widget.hide() 
        self._create_track_ui(self.track_layout)

        self.album_widget = QWidget()
        self.album_layout = QVBoxLayout(self.album_widget)
        self.album_widget.hide() 
        self._create_album_ui(self.album_layout)
        
        self.playlist_widget = QWidget()
        self.playlist_layout = QVBoxLayout(self.playlist_widget)
        self.playlist_widget.hide()
        self._create_playlist_ui(self.playlist_layout) 
        
        self.download_layout.addWidget(self.track_widget)
        self.download_layout.addWidget(self.album_widget)
        self.download_layout.addWidget(self.playlist_widget)
        
    def _hide_all_download_views(self):
        self.track_widget.hide()
        self.album_widget.hide()
        self.playlist_widget.hide()

    def _show_track_view(self):
        self._clear_nav_buttons()
        self.btn_track.setChecked(True)
        self.local_container.hide()
        self.download_container.show()
        self._hide_all_download_views()
        self.track_widget.show()
        
    def _create_track_ui(self, layout):
        self.track_url_input = QLineEdit()
        self.track_url_input.setPlaceholderText("Introduce la URL de la Pista de Spotify aquí...")
        download_btn = QPushButton("Descargar Pista")
        download_btn.setStyleSheet("background-color: #1DB954; color: black; font-weight: bold;")
        download_btn.clicked.connect(lambda: self._download_track(self.track_url_input.text()))
        layout.addWidget(QLabel("## 🎧 Descarga de Pista Única"))
        layout.addWidget(self.track_url_input)
        layout.addWidget(download_btn)
        layout.addStretch(1) # Relleno
        
    def _show_album_view(self):
        self._clear_nav_buttons()
        self.btn_album.setChecked(True)
        self.local_container.hide()
        self.download_container.show()
        self._hide_all_download_views()
        self.album_widget.show()

    def _create_album_ui(self, layout):
        self.album_url_input = QLineEdit()
        self.album_url_input.setPlaceholderText("Introduce la URL del Álbum de Spotify aquí...")
        download_btn = QPushButton("Descargar Álbum")
        download_btn.setStyleSheet("background-color: #1DB954; color: black; font-weight: bold;")
        download_btn.clicked.connect(lambda: self._download_album(self.album_url_input.text()))
        layout.addWidget(QLabel("## 💿 Descarga de Álbum"))
        layout.addWidget(self.album_url_input)
        layout.addWidget(download_btn)
        layout.addStretch(1) # Relleno

    def _show_playlist_view(self):
        self._clear_nav_buttons()
        self.btn_playlist.setChecked(True)
        self.local_container.hide()
        self.download_container.show()
        self._hide_all_download_views()
        self.playlist_widget.show()
        QTimer.singleShot(2000, self._show_track_view) 

    def _create_playlist_ui(self, layout):
        label = QLabel("## 🚧 Descarga de Playlist - ¡En Desarrollo! 👷")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: yellow; font-size: 16pt;")
        layout.addWidget(label)
        layout.addStretch(1) 
        
    # --- Vista Local (Cuadrícula y Reproductor) ---

    def _init_local_view_ui(self):
        
        # 1. Explorador de archivos (Cuadrícula, a la izquierda)
        self.explorer_area = QScrollArea() 
        self.explorer_area.setWidgetResizable(True)
        self.explorer_area.setMinimumWidth(300)
        self.explorer_area.setStyleSheet("border: none; background-color: transparent;")
        
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.grid_layout.setSpacing(15) 
        self.explorer_area.setWidget(self.grid_widget)
        
        explorer_container = QVBoxLayout()
        explorer_container.addWidget(QLabel(f"📂 **Archivos Locales ({self.local_music_dir})**"))
        explorer_container.addWidget(self.explorer_area)

        explorer_widget_main = QWidget()
        explorer_widget_main.setLayout(explorer_container)
        explorer_widget_main.setMaximumWidth(600) 
        self.local_layout.addWidget(explorer_widget_main, 2) 
        
        # 2. Reproductor de música (a la derecha)
        self.player_widget = QWidget()
        self.player_layout = QVBoxLayout(self.player_widget)
        self.player_widget.setStyleSheet("background-color: #191414; border: 1px solid #1DB954; border-radius: 10px; padding: 10px;")
        
        # --- Etiqueta de la Carátula Actual ---
        self.current_cover_label = QLabel()
        self.current_cover_label.setAlignment(Qt.AlignCenter)
        self.current_cover_label.setFixedSize(250, 250)
        self.current_cover_label.setStyleSheet("background-color: #404040; border-radius: 10px;")
        self.current_cover_label.setText("🎶") 
        self.current_cover_label.setStyleSheet("font-size: 120pt; background-color: #404040; border-radius: 10px; color: lightgray;")
        
        cover_layout = QHBoxLayout()
        cover_layout.setAlignment(Qt.AlignCenter)
        cover_layout.addWidget(self.current_cover_label)

        # --- Etiqueta del Nombre de la Canción (MODIFICADO: OCULTADO) ---
        self.current_song_label = QLabel("Selecciona una canción de la cuadrícula")
        self.current_song_label.setAlignment(Qt.AlignCenter)
        self.current_song_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #1DB954;")
        self.current_song_label.hide() # <--- ¡CAMBIO AQUÍ!
        
        # --- Controles de Reproducción ---
        self.prev_btn = QPushButton("⏮️ Anterior")
        self.prev_btn.setFixedSize(80, 40)
        self.prev_btn.clicked.connect(self._play_previous_track)
        
        self.play_pause_btn = QPushButton("▶️ Play")
        self.play_pause_btn.setFixedSize(100, 40)
        self.play_pause_btn.clicked.connect(self._toggle_playback)

        self.next_btn = QPushButton("Siguiente ⏭️")
        self.next_btn.setFixedSize(80, 40)
        self.next_btn.clicked.connect(self._play_next_track)
        
        player_controls = QHBoxLayout()
        player_controls.setAlignment(Qt.AlignCenter)
        player_controls.addWidget(self.prev_btn)
        player_controls.addWidget(self.play_pause_btn)
        player_controls.addWidget(self.next_btn)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.mediaPlayer.setPosition)
        
        self.player_layout.addLayout(cover_layout)
        self.player_layout.addWidget(self.current_song_label) # Agregamos el widget, aunque esté oculto.
        self.player_layout.addLayout(player_controls)
        self.player_layout.addWidget(self.slider)
        
        self.local_layout.addWidget(self.player_widget, 1) 
        
        self._refresh_local_files()

    def _show_local_view(self):
        self._clear_nav_buttons()
        self.btn_local.setChecked(True)
        self.download_container.hide()
        self.local_container.show()
        self._refresh_local_files()

    def _refresh_local_files(self):
        # 1. Limpiar la cuadrícula existente
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
        # 2. Recargar lista de canciones disponibles
        self.available_songs = []
        try:
            target_dir = self.local_music_dir
            if not os.path.exists(target_dir):
                error_label = QLabel(f"ERROR: La carpeta '{target_dir}' no existe.")
                error_label.setStyleSheet("color: red;")
                self.grid_layout.addWidget(error_label, 0, 0)
                return
            
            files = [f for f in os.listdir(target_dir) if f.lower().endswith(('.mp3', '.m4a', '.flac', '.wav'))]
            
            if files:
                num_cols = 4 
                for index, song_name in enumerate(files):
                    row = index // num_cols
                    col = index % num_cols
                    
                    song_path = os.path.join(target_dir, song_name)
                    self.available_songs.append((song_name, song_path))
                    
                    # Usamos SongSquare que carga la carátula
                    song_square = SongSquare(song_name, song_path, self) 
                    self.grid_layout.addWidget(song_square, row, col)
                    
                self.log_message(f"Explorador de archivos: Se cargaron {len(files)} canciones.", color="cyan")
            else:
                info_label = QLabel(f"No se encontraron archivos de audio en la carpeta '{target_dir}'.")
                info_label.setStyleSheet("color: gray;")
                self.grid_layout.addWidget(info_label, 0, 0)
        except Exception as e:
            error_label = QLabel(f"Error al cargar archivos locales: {e}")
            error_label.setStyleSheet("color: red;")
            self.grid_layout.addWidget(error_label, 0, 0)
        
        self.current_track_index = -1
    
    # --- LÓGICA DE REPRODUCCIÓN (MODIFICADA) ---
    
    def _load_local_track_by_path(self, song_path, song_name):
        try:
            self.current_track_index = [i for i, (name, path) in enumerate(self.available_songs) if path == song_path][0]
        except IndexError:
            self.current_track_index = -1
            self.log_message(f"Advertencia: No se encontró la pista {song_name} en la lista de canciones.", color="yellow")
            
        self._start_playback(song_path, song_name)

    def _load_current_cover(self, song_path):
        """Carga la carátula de la canción en el reproductor principal."""
        image_data = get_album_art(song_path)
        size = self.current_cover_label.size()
        
        if image_data:
            pixmap = QPixmap()
            if pixmap.loadFromData(image_data):
                scaled_pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.current_cover_label.setPixmap(scaled_pixmap)
                return
            
        # Placeholder si no hay imagen o falla la carga
        self.current_cover_label.setText("🎶") 
        self.current_cover_label.setStyleSheet("font-size: 120pt; background-color: #404040; border-radius: 10px; color: lightgray;")


    def _start_playback(self, song_path, song_name):
        self.current_track_path = song_path
        
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.stop()
            
        media_content = QMediaContent(QUrl.fromLocalFile(song_path))
        
        if media_content.isNull():
            self.log_message(f"ERROR: No se pudo cargar el archivo (verifique códecs): {song_name}", color="red")
            # Ya no actualizamos la etiqueta de la canción, solo el log y la imagen
            # self.current_song_label.setText(f"ERROR al cargar (Códec?): {song_name}") 
            
            # Resetear la imagen a placeholder si falla
            self.current_cover_label.setText("❌") 
            self.current_cover_label.setStyleSheet("font-size: 120pt; background-color: #404040; border-radius: 10px; color: red;")
            return

        # 1. Cargar y mostrar la carátula en el reproductor
        self._load_current_cover(song_path)
        
        # 2. Iniciar reproducción
        self.mediaPlayer.setMedia(media_content)
        # self.current_song_label.setText(f"{song_name.replace('.mp3', '').replace('.m4a', '')}") # <--- ¡CAMBIO AQUÍ! (Línea eliminada)
        self.mediaPlayer.play()
        self.is_playing = True
        self.play_pause_btn.setText("⏸️ Pausa")
        self.log_message(f"Reproduciendo: {song_name}", color="green")
        
    def _play_next_track(self):
        if not self.available_songs: return
            
        next_index = (self.current_track_index + 1) % len(self.available_songs)
        
        self.current_track_index = next_index
        song_name, song_path = self.available_songs[self.current_track_index]
        self._start_playback(song_path, song_name)

    def _play_previous_track(self):
        if not self.available_songs: return
            
        prev_index = (self.current_track_index - 1 + len(self.available_songs)) % len(self.available_songs)
        
        self.current_track_index = prev_index
        song_name, song_path = self.available_songs[self.current_track_index]
        self._start_playback(song_path, song_name)

    def _handle_media_finished(self, state):
        if state == QMediaPlayer.StoppedState and self.mediaPlayer.mediaStatus() == QMediaPlayer.EndOfMedia:
            self._play_next_track()

    def _toggle_playback(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.is_playing = False
        else:
            if self.current_track_path:
                self.mediaPlayer.play()
                self.is_playing = True
            elif self.available_songs:
                self._play_next_track()
            else:
                self.log_message("Selecciona una canción primero para reproducir.", color="yellow")
            
    def _update_player_state(self, state):
        if state == QMediaPlayer.PlayingState:
            self.play_pause_btn.setText("⏸️ Pausa")
        elif state == QMediaPlayer.PausedState:
            self.play_pause_btn.setText("▶️ Play")
        elif state == QMediaPlayer.StoppedState:
            self.play_pause_btn.setText("▶️ Play")
            self.is_playing = False
        
    def _update_position(self, position):
        if not self.slider.isSliderDown():
            self.slider.setValue(position)

    def _update_duration(self, duration):
        self.slider.setRange(0, duration)
        
    # --- LÓGICA DE DESCARGA ---
    
    def _download_track(self, url_track):
        if "track" not in url_track:
            QMessageBox.warning(self, "URL Inválida", "La URL debe ser de una pista de Spotify (contiene 'track').")
            return
        
        self.log_message(f"Iniciando descarga de pista: {url_track}", color="cyan")
        
        QTimer.singleShot(100, lambda: run_node_module(self, "track/track_datos.js", url_track))
        QTimer.singleShot(2000, lambda: run_node_module(self, "track/track_descarga.js"))
        QTimer.singleShot(4000, lambda: self._open_track_download_link())
        
    def _open_track_download_link(self):
        dlink_data = load_json('final.json')
        dlink = dlink_data.get('dlink') if dlink_data else None

        if dlink:
            self.log_message(f"Enlace encontrado. Abriendo navegador para descargar...", color="green")
            webbrowser.open(dlink)
            QMessageBox.information(self, "Descarga Iniciada", f"La descarga se ha abierto en tu navegador. El archivo debería aparecer en tu carpeta de Descargas o Música.")
        else:
            self.log_message("ERROR: Enlace de descarga no encontrado. Revisa los logs de Node.", color="red")
            QMessageBox.critical(self, "Error", "Enlace de descarga no encontrado. Verifica la URL y los logs.")

        remove_temp_files()
        
    def _download_album(self, url_album):
        if "album" not in url_album:
            QMessageBox.warning(self, "URL Inválida", "La URL debe ser de un álbum de Spotify (contiene 'album').")
            return
            
        self.log_message(f"Iniciando descarga de álbum: {url_album}", color="cyan")
        
        QTimer.singleShot(100, lambda: run_node_module(self, "album/album_datos.js", url_album))
        QTimer.singleShot(3000, lambda: run_node_module(self, "/album/album_descarga.js"))
        QTimer.singleShot(6000, lambda: run_node_module(self, "src/ordenamiento.js"))
        QTimer.singleShot(8000, lambda: self._open_album_download_links())

    def _open_album_download_links(self):
        links = load_json('links.json')
        
        if links and isinstance(links, list):
            self.log_message(f"Se encontraron {len(links)} pistas. Abriendo enlaces en navegador...", color="green")
            
            for i, link in enumerate(links, 1):
                QTimer.singleShot(i * 1500, lambda l=link, i=i: self._open_single_link_with_log(l, i, len(links)))
            
            QTimer.singleShot(len(links) * 1500 + 2000, lambda: QMessageBox.information(self, "Descargas Iniciadas", f"{len(links)} descargas de pistas del álbum se han abierto en tu navegador."))
            
        else:
            self.log_message("ERROR: No se encontraron enlaces de descarga para el álbum.", color="red")
            QMessageBox.critical(self, "Error", "No se encontraron enlaces de descarga para el álbum. Verifica la URL y los logs.")

        remove_temp_files()

    def _open_single_link_with_log(self, link, current, total):
        webbrowser.open(link)
        self.log_message(f"Abriendo pista {current}/{total} en el navegador...", color="lightgreen")

    def _open_creator_page(self):
        self.log_message("Abriendo página del creador en el navegador...", color="white")
        webbrowser.open("https://github.com/LittleKidd0")

# --- Ejecución de la Aplicación ---

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    try:
        qdarktheme.setup_theme("dark", custom_colors={"primary": "#1DB954"})
    except Exception:
        try:
            app.setStyleSheet(qdarktheme.load_stylesheet())
        except Exception:
             pass 
    
    window = SpotifyDownloaderApp()
    window.show()
    sys.exit(app.exec_())