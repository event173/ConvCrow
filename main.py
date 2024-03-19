import sys
import os
import io
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageOps
import zipfile
from PyQt5.QtGui import QIcon



class ImageConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Image Converter'
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet("""
            QWidget {background-color: #2b2b2b; color: #dcdcdc;}
            QPushButton {background-color: #3c3f41; border: 1px solid #3c3f41; border-radius: 2px; padding: 5px; color: #dcdcdc;}
            QPushButton:hover {background-color: #454748;}
            QPushButton:pressed {background-color: #4b6eaf;}
            QLabel {color: #dcdcdc;}
        """)

        self.setWindowIcon(QIcon('icon.ico'))

        self.mainLayout = QVBoxLayout()
        
        self.imageLabel = QLabel('Kein Bild geladen')
        self.imageLabel.setFixedSize(760, 440)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.imageLabel)

        self.buttonLayout = QHBoxLayout()
        
        self.loadButton = QPushButton('Bild laden')
        self.loadButton.clicked.connect(self.loadImage)
        self.buttonLayout.addWidget(self.loadButton)
        
        self.saveButton = QPushButton('Bild speichern als...')
        self.saveButton.clicked.connect(self.saveImage)
        self.saveButton.setEnabled(False)
        self.buttonLayout.addWidget(self.saveButton)

        self.icoSetButton = QPushButton('ICO Set generieren und ZIP speichern')
        self.icoSetButton.clicked.connect(self.generateIcoSet)
        self.icoSetButton.setEnabled(False)
        self.buttonLayout.addWidget(self.icoSetButton)
        
        self.mainLayout.addLayout(self.buttonLayout)
        self.setLayout(self.mainLayout)
    
    def loadImage(self):
        formatOptions = 'Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif *.webp)'
        filePath, _ = QFileDialog.getOpenFileName(self, "Bild laden", "", formatOptions)
        if filePath:
            self.currentImage = filePath
            pixmap = QPixmap(filePath)
            self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.width(), self.imageLabel.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.saveButton.setEnabled(True)
            self.icoSetButton.setEnabled(True)
    
    def saveImage(self):
        formatOptions = 'PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp);;GIF (*.gif);;WebP (*.webp);;ICO (*.ico)'
        filePath, selectedFilter = QFileDialog.getSaveFileName(self, "Bild speichern als", "", formatOptions)
        if filePath:
            image = Image.open(self.currentImage)
            format = selectedFilter.split(' ')[0]
            image.save(filePath, format=format)
            QMessageBox.information(self, "Erfolg", "Bild erfolgreich gespeichert!")

    def generateIcoSet(self):
        sizes = [16, 32, 48, 64, 128, 256]
        zipPath, _ = QFileDialog.getSaveFileName(self, "ICO Set speichern als ZIP", "", "ZIP files (*.zip)")
        if zipPath:
            if not zipPath.endswith('.zip'):
                zipPath += '.zip'
            with zipfile.ZipFile(zipPath, 'w') as myzip:
                image = Image.open(self.currentImage)
                for size in sizes:
                    temp_icon_io = io.BytesIO()  # Erstelle einen BytesIO-Stream als temporären Speicher
                    resized_image = image.resize((size, size), Image.Resampling.LANCZOS)
                    resized_image.save(temp_icon_io, format='ICO', sizes=[(size, size)])
                    temp_icon_io.seek(0)
                    myzip.writestr(f"icon_{size}x{size}.ico", temp_icon_io.read())  # Schreibe den Stream ins ZIP
            QMessageBox.information(self, "Erfolg", "ICO Set erfolgreich in ZIP gespeichert!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageConverterApp()
    ex.show()
    sys.exit(app.exec_())
