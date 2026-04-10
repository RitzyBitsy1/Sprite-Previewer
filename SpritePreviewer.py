import math

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

'''Document your development effort by making at least 4 commits and pushes to the GitHub repo 
as you write your code with some reasonable time and difference in the code between pushes.'''
'''Commits: 1/4'''

# Code by Annabelle Boyd
# U156172
# https://github.com/RitzyBitsy1/Sprite-Previewer

# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_sprite(sprite_folder_name, number_of_frames):
    frames = []
    padding = math.ceil(math.log(number_of_frames - 1, 10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding, '0') + ".png"
        frames.append(QPixmap(folder_and_file_name))

    return frames

class SpritePreview(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sprite Animation Preview")
        # This loads the provided sprite and would need to be changed for your own.
        self.num_frames = 21
        self.frames = load_sprite('spriteImages',self.num_frames)

        self.current_frame = 0
        self.is_animating = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.advance_frame)

        self.setupUI()

    def setupUI(self):
        # MENU #
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')

        pause_action = QAction('Pause', self)
        pause_action.triggered.connect(self.pause_animation)
        file_menu.addAction(pause_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(QApplication.quit)
        file_menu.addAction(exit_action)

        central = QFrame()
        main_layout = QVBoxLayout(central)

        # SPRITE LABEL #
        self.sprite_label =QLabel()
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sprite_label.setMinimumSize(200, 200)
        if self.frames:
            self.sprite_label.setPixmap(
                self.frames[0].scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.FastTransformation)
                )
        main_layout.addWidget(self.sprite_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        # FPS LABEL #
        fps_title =  QLabel("Frames per second")
        main_layout.addWidget(fps_title)

        self.fps_slider = QSlider(Qt.Orientation.Horizontal)
        self.fps_slider.setMinimum(1)
        self.fps_slider.setMaximum(100)
        self.fps_slider.setValue(12)
        self.fps_slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.fps_slider.setTickInterval(10)
        self.fps_slider.valueChanged.connect(self.on_fps_changed)
        main_layout.addWidget(self.fps_slider)

        self.fps_value_label = QLabel("12")
        main_layout.addWidget(self.fps_value_label)

        # START/STOP #
        self.start_stop_btn = QPushButton("Start")
        self.start_stop_btn.clicked.connect(self.toggle_animation)
        main_layout.addWidget(self.start_stop_btn)

        self.setCentralWidget(central)

    def on_fps_changed(self, value):
        self.fps_value_label.setText(str(value))
        if self.is_animating:
            self.timer.setInterval(int(1000 / value))

    def advance_frame(self):
        self.current_frame = (self.current_frame + 1) % self.num_frames
        self.sprite_label.setPixmap(
            self.frames[self.current_frame].scaled(
                200, 200,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.FastTransformation
            )
        )

    def toggle_animation(self):
        if not self.is_animating:
            fps = self.fps_slider.value()
            self.timer.start(int(1000 / fps))
            self.is_animating = True
            self.start_stop_btn.setText("Stop")
        else:
            self.timer.stop()
            self.is_animating = False
            self.start_stop_btn.setText("Start")

    def pause_animation(self):
        if self.is_animating:
            self.timer.stop()
            self.is_animating = False
            self.start_stop_btn.setText("Pause")

def main():
    app = QApplication([])
    # Create our custom application
    window = SpritePreview()
    # And show it
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
