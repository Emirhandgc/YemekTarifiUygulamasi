import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QTextEdit, QListWidget, QDialog, QSlider
from PyQt5.QtGui import QColor

class TarifUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yemek Tarifi Uygulaması")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label = QLabel("Tarif Adı:")
        self.label.setStyleSheet("color: white;")
        self.layout.addWidget(self.label)

        self.tarif_adi_input = QTextEdit()
        self.layout.addWidget(self.tarif_adi_input)

        self.label_malzemeler = QLabel("Malzemeler:")
        self.label_malzemeler.setStyleSheet("color: white;")
        self.layout.addWidget(self.label_malzemeler)

        self.malzemeler_input = QTextEdit()
        self.layout.addWidget(self.malzemeler_input)

        self.label_tarif = QLabel("Tarif:")
        self.label_tarif.setStyleSheet("color: white;")
        self.layout.addWidget(self.label_tarif)

        self.tarif_input = QTextEdit()
        self.layout.addWidget(self.tarif_input)

        self.button_kaydet = QPushButton("Tarifi Kaydet")
        self.button_kaydet.clicked.connect(self.tarif_kaydet)
        self.button_kaydet.setObjectName("CustomButton")
        self.button_kaydet.setStyleSheet("color: white;")
        self.layout.addWidget(self.button_kaydet)

        self.button_ara = QPushButton("Tarif Ara")
        self.button_ara.clicked.connect(self.open_tarif_ara)
        self.button_ara.setObjectName("CustomButton")
        self.button_ara.setStyleSheet("color: white;")
        self.layout.addWidget(self.button_ara)

        self.button_degerlendir = QPushButton("Tarifi Değerlendir")
        self.button_degerlendir.clicked.connect(self.open_tarif_degerlendir)
        self.button_degerlendir.setObjectName("CustomButton")
        self.button_degerlendir.setStyleSheet("color: white;")
        self.layout.addWidget(self.button_degerlendir)

        self.central_widget.setLayout(self.layout)

        # SQLite veritabanına bağlan
        self.baglanti = sqlite3.connect('tarifler.db')
        self.cursor = self.baglanti.cursor()

        # Tarif tablosunu oluştur
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tarifler (
                                id INTEGER PRIMARY KEY,
                                tarif_adi TEXT,
                                malzemeler TEXT,
                                tarif TEXT,
                                puan INTEGER DEFAULT 0
                                )''')
        self.baglanti.commit()

        # Tema ve Stil Tanımlama
        self.setStyleSheet("""
            QPushButton#CustomButton {
                background-color: #eeba2c;
                color: #161616;
                border: 1px solid #eeba2c;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QPushButton#CustomButton:hover {
                background-color: #ffc72c;
            }
            QPushButton#CustomButton:pressed {
                background-color: #c69c1e;
            }
        """)

        # Arka plan rengini #161616 olarak ayarla
        self.central_widget.setStyleSheet("background-color: #161616;")

    def tarif_kaydet(self):
        tarif_adi = self.tarif_adi_input.toPlainText()
        malzemeler = self.malzemeler_input.toPlainText()
        tarif = self.tarif_input.toPlainText()

        # Tarifi veritabanına ekleyelim
        self.cursor.execute("INSERT INTO tarifler (tarif_adi, malzemeler, tarif) VALUES (?, ?, ?)", (tarif_adi, malzemeler, tarif))
        self.baglanti.commit()

        print("Tarif kaydedildi!")
        self.clear_inputs()

    def open_tarif_ara(self):
        self.ara_window = TarifAramaWindow(self.cursor)
        self.ara_window.show()

    def open_tarif_degerlendir(self):
        self.degerlendir_window = TarifDegerlendirWindow(self.cursor)
        self.degerlendir_window.exec_()  # exec_() kullanarak pencerenin modal olarak açılmasını sağlayalım

    def clear_inputs(self):
        self.tarif_adi_input.clear()
        self.malzemeler_input.clear()
        self.tarif_input.clear()

class TarifAramaWindow(QWidget):
    def __init__(self, cursor):
        super().__init__()

        self.setWindowTitle("Tarif Ara")
        self.setGeometry(200, 200, 400, 200)

        self.cursor = cursor

        layout = QVBoxLayout()

        label = QLabel("Aranacak Tarif:")
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

        self.search_input = QTextEdit()
        layout.addWidget(self.search_input)

        self.result_label = QLabel("")
        self.result_label.setStyleSheet("color: white;")
        layout.addWidget(self.result_label)

        self.puan_label = QLabel("")
        self.puan_label.setStyleSheet("color: white;")
        layout.addWidget(self.puan_label)

        button_ara = QPushButton("Ara")
        button_ara.clicked.connect(self.ara)
        button_ara.setObjectName("CustomButton")
        button_ara.setStyleSheet("color: white;")
        layout.addWidget(button_ara)

        # Display saved recipes
        self.list_widget = QListWidget()
        self.display_tarifler()
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def display_tarifler(self):
        self.list_widget.clear()
        self.cursor.execute("SELECT tarif_adi FROM tarifler")
        tarifler = self.cursor.fetchall()
        for tarif in tarifler:
            self.list_widget.addItem(tarif[0])

    def ara(self):
        search_query = self.search_input.toPlainText()

        # Aranan tarifin listemizde olup olmadığını kontrol edelim
        self.cursor.execute("SELECT * FROM tarifler WHERE tarif_adi LIKE ?", ('%' + search_query + '%',))
        aranan_tarif = self.cursor.fetchone()

        if aranan_tarif:
            self.result_label.setText("Aranan Tarif: " + aranan_tarif[1])
            self.puan_label.setText("Değerlendirme Puanı: " + str(aranan_tarif[4]))
        else:
            self.result_label.setText("Aranan Tarif: Bulunamadı")
            self.puan_label.setText("Değerlendirme Puanı: -")

class TarifDegerlendirWindow(QDialog):
    def __init__(self, cursor):
        super().__init__()

        self.setWindowTitle("Tarifi Değerlendir")
        self.setGeometry(200, 200, 400, 200)

        self.cursor = cursor

        layout = QVBoxLayout()

        label = QLabel("Değerlendirilecek Tarif:")
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

        self.degerlendir_input = QTextEdit()
        layout.addWidget(self.degerlendir_input)

        self.slider_label = QLabel("Puan: 5")
        self.slider_label.setStyleSheet("color: white;")
        layout.addWidget(self.slider_label)

        self.slider = QSlider()
        self.slider.setOrientation(1)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.setValue(5)
        self.slider.valueChanged.connect(self.slider_changed)
        layout.addWidget(self.slider)

        button_degerlendir = QPushButton("Değerlendir")
        button_degerlendir.clicked.connect(self.degerlendir)
        button_degerlendir.setObjectName("CustomButton")
        button_degerlendir.setStyleSheet("color: white;")
        layout.addWidget(button_degerlendir)

        # Display saved recipes
        self.list_widget = QListWidget()
        self.display_tarifler()
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def display_tarifler(self):
        self.list_widget.clear()
        self.cursor.execute("SELECT tarif_adi FROM tarifler")
        tarifler = self.cursor.fetchall()
        for tarif in tarifler:
            self.list_widget.addItem(tarif[0])

    def slider_changed(self):
        value = self.slider.value()
        self.slider_label.setText("Puan: " + str(value))

    def degerlendir(self):
        degerlendirme = self.degerlendir_input.toPlainText()
        puan = self.slider.value()

        selected_item = self.list_widget.currentItem()
        if selected_item:
            tarif_adi = selected_item.text()
            self.cursor.execute("UPDATE tarifler SET puan = ? WHERE tarif_adi = ?", (puan, tarif_adi))
            self.cursor.connection.commit()

        self.accept()  # Pencereyi kapat

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TarifUygulamasi()
    window.show()
    sys.exit(app.exec_())
