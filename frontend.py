from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem,
    QFrame, QSpacerItem, QSizePolicy, QMessageBox, QHeaderView,
    QDialog, QFormLayout, QComboBox, QDialogButtonBox, QStackedWidget
)
from PyQt6.QtCore import Qt
import sys

from backend import DatabaseManager

class EquipmentDialog(QDialog):
    def __init__(self, parent=None, data=None):
        """
        data: Un tuplu/lista cu datele echipamentului daca suntem in modul EDITARE.
              (Nume, Categorie, Serie, Locatie, Status)
        """
        super().__init__(parent)
        self.setWindowTitle("Echipament")
        self.setModal(True)
        self.resize(400, 300)
        self.setStyleSheet("""
            QDialog { background-color: #202124; color: #E8EAED; }
            QLabel { color: #E8EAED; font-weight: bold; }
            QLineEdit, QComboBox { 
                background-color: #303134; border: 1px solid #5F6368; 
                color: #FFF; padding: 5px; border-radius: 4px;
            }
        """)
        
        layout = QFormLayout(self)
        
        self.name_input = QLineEdit()
        self.cat_input = QComboBox()
        self.cat_input.addItems(["Laptop", "Desktop", "Monitor", "Imprimantă", "Rețelistică"])
        
        self.serial_input = QLineEdit()
        self.loc_input = QLineEdit()
        
        self.status_input = QComboBox()
        self.status_input.addItems(["Activ", "În Service", "Garanție", "Casat"])
        
        layout.addRow("Denumire:", self.name_input)
        layout.addRow("Categorie:", self.cat_input)
        layout.addRow("Serie (S/N):", self.serial_input)
        layout.addRow("Locație:", self.loc_input)
        layout.addRow("Stare:", self.status_input)
        
        if data:
            self.setWindowTitle("Editează Echipament")
            self.name_input.setText(str(data[0]))
            self.cat_input.setCurrentText(str(data[1]))
            self.serial_input.setText(str(data[2]))
            self.loc_input.setText(str(data[3]))
            self.status_input.setCurrentText(str(data[4]))
        else:
            self.setWindowTitle("Adaugă Echipament Nou")
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        return (
            self.name_input.text(),
            self.cat_input.currentText(),
            self.serial_input.text(),
            self.loc_input.text(),
            self.status_input.currentText()
        )

class ModernDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.db = DatabaseManager()
        
        self.init_ui()
        self.refresh_table()
        self.update_dashboard_stats()

    def init_ui(self):
        self.setWindowTitle("Evidență Echipamente IT - Parchet")
        self.resize(1200, 700)
        self.setStyleSheet(self.styles())

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(10)
        sidebar_layout.setContentsMargins(20, 30, 20, 20)

        logo = QLabel("⚙️ IT Manager")
        logo.setObjectName("logo")
        sidebar_layout.addWidget(logo)
        sidebar_layout.addSpacing(20)

        self.btn_dashboard = self.create_nav_button("📊 Dashboard")
        self.btn_equipments = self.create_nav_button("💻 Echipamente")
        self.btn_users = self.create_nav_button("👥 Utilizatori")
        
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0))
        self.btn_equipments.clicked.connect(lambda: self.switch_page(1))
        
        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_equipments)
        sidebar_layout.addWidget(self.btn_users)

        sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        logout_btn = QPushButton("Ieșire")
        logout_btn.setObjectName("logoutButton")
        logout_btn.clicked.connect(self.close)
        sidebar_layout.addWidget(logout_btn)

        content_frame = QFrame()
        content_frame.setObjectName("content")
        content_layout = QVBoxLayout(content_frame)
        
        self.header_title = QLabel("Panou de Control")
        self.header_title.setObjectName("headerTitle")
        content_layout.addWidget(self.header_title)

        self.pages = QStackedWidget()
        
        self.page_home = QWidget()
        self.setup_home_page()
        self.pages.addWidget(self.page_home)
        
        self.page_equipments = QWidget()
        self.setup_equipment_page()
        self.pages.addWidget(self.page_equipments)
        
        content_layout.addWidget(self.pages)

        root.addWidget(sidebar)
        root.addWidget(content_frame)

    def create_nav_button(self, text):
        btn = QPushButton(text)
        btn.setObjectName("navButton")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn

    def setup_home_page(self):
        layout = QVBoxLayout(self.page_home)
        stats_container = QHBoxLayout()
        
        self.card_total = self.create_stat_card("Total Echipamente", "0", "#00BCD4")
        self.card_active = self.create_stat_card("Active", "0", "#4CAF50")
        self.card_service = self.create_stat_card("În Service", "0", "#FF5252")
        
        stats_container.addWidget(self.card_total)
        stats_container.addWidget(self.card_active)
        stats_container.addWidget(self.card_service)
        
        layout.addLayout(stats_container)
        layout.addStretch()

    def create_stat_card(self, title, value, color):
        card = QFrame()
        card.setStyleSheet(f"background-color: #25262A; border-radius: 10px; border-left: 5px solid {color};")
        l = QVBoxLayout(card)
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("color: #9AA0A6; font-size: 14px;")
        v_lbl = QLabel(value)
        v_lbl.setObjectName("statValue")
        v_lbl.setStyleSheet("color: #FFF; font-size: 32px; font-weight: bold;")
        l.addWidget(t_lbl)
        l.addWidget(v_lbl)
        return card

    def setup_equipment_page(self):
        layout = QVBoxLayout(self.page_equipments)
        
        top_bar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Caută echipament...")
        self.search_input.textChanged.connect(self.filter_table)
        
        add_btn = QPushButton("+ Adaugă")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.open_add_dialog)

        edit_btn = QPushButton("✏️ Editează")
        edit_btn.setObjectName("secondaryButton")
        edit_btn.clicked.connect(self.open_edit_dialog)
        
        top_bar.addWidget(self.search_input)
        top_bar.addWidget(edit_btn)
        top_bar.addWidget(add_btn)
        layout.addLayout(top_bar)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Model", "Categorie", "Serie", "Locație", "Stare"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

    def switch_page(self, index):
        self.pages.setCurrentIndex(index)
        if index == 0:
            self.header_title.setText("Panou de Control")
            self.update_dashboard_stats()
        elif index == 1:
            self.header_title.setText("Gestiune Echipamente")

    def update_dashboard_stats(self):
        total, active, service = self.db.get_stats()
        self.card_total.findChild(QLabel, "statValue").setText(str(total))
        self.card_active.findChild(QLabel, "statValue").setText(str(active))
        self.card_service.findChild(QLabel, "statValue").setText(str(service))

    def open_add_dialog(self):
        dialog = EquipmentDialog(self)
        if dialog.exec():
            name, cat, serial, loc, status = dialog.get_data()
            if name and serial:
                self.db.add_equipment(name, cat, serial, loc, status)
                self.refresh_table()
                QMessageBox.information(self, "Succes", "Echipamentul a fost adăugat!")
            else:
                QMessageBox.warning(self, "Eroare", "Denumirea și Seria sunt obligatorii!")

    def open_edit_dialog(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Atenție", "Selectează un echipament din tabel pentru a-l edita!")
            return

        row = self.table.currentRow()
        equip_id = self.table.item(row, 0).text()
        name = self.table.item(row, 1).text()
        category = self.table.item(row, 2).text()
        serial = self.table.item(row, 3).text()
        location = self.table.item(row, 4).text()
        status = self.table.item(row, 5).text()

        current_data = (name, category, serial, location, status)

        dialog = EquipmentDialog(self, data=current_data)
        if dialog.exec():
            new_name, new_cat, new_serial, new_loc, new_status = dialog.get_data()
            
            if new_name and new_serial:
                success = self.db.update_equipment(equip_id, new_name, new_cat, new_serial, new_loc, new_status)
                if success:
                    self.refresh_table()
                    self.update_dashboard_stats()
                    QMessageBox.information(self, "Succes", "Echipamentul a fost actualizat!")
                else:
                    QMessageBox.critical(self, "Eroare", "Nu s-a putut actualiza echipamentul.")
            else:
                QMessageBox.warning(self, "Eroare", "Denumirea și Seria sunt obligatorii!")

    def refresh_table(self):
        data = self.db.get_equipment_data()
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, val in enumerate(row_data):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

    def filter_table(self, text):
        text = text.lower()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def styles(self):
        return """
        QWidget { background-color: #121212; color: #E8EAED; font-family: 'Segoe UI', sans-serif; font-size: 14px; }
        #sidebar { background-color: #1E1E1E; border-right: 1px solid #2D2D2D; }
        #content { background-color: #181818; }
        #logo { font-size: 22px; font-weight: bold; color: #00BCD4; }
        #navButton {
            background-color: transparent; color: #9AA0A6; text-align: left;
            padding: 12px 15px; border-radius: 8px; font-size: 15px;
        }
        #navButton:hover { background-color: #2D2D2D; color: #FFF; }
        #logoutButton {
            background-color: #2B2B2B; color: #FF5252; border-radius: 8px; padding: 10px;
        }
        #logoutButton:hover { background-color: #3C4043; }
        #headerTitle { font-size: 24px; font-weight: bold; color: #FFF; margin-bottom: 15px; }
        QLineEdit {
            background-color: #242424; border: 1px solid #3C4043; border-radius: 6px;
            padding: 8px 12px; color: #FFF; font-size: 14px;
        }
        QLineEdit:focus { border: 1px solid #00BCD4; }
        
        QPushButton#primaryButton {
            background-color: #00BCD4; color: #000; font-weight: bold;
            border-radius: 6px; padding: 8px 16px;
        }
        QPushButton#primaryButton:hover { background-color: #26C6DA; }

        QPushButton#secondaryButton {
            background-color: #2B2B2B; color: #00BCD4; font-weight: bold;
            border: 1px solid #00BCD4; border-radius: 6px; padding: 8px 16px;
        }
        QPushButton#secondaryButton:hover { background-color: #3C4043; }

        QTableWidget {
            background-color: #202124; border: 1px solid #3C4043; border-radius: 8px;
            gridline-color: #3C4043;
        }
        QHeaderView::section {
            background-color: #2D2D2D; color: #E8EAED; border: none; padding: 8px; font-weight: bold;
        }
        QTableWidget::item:selected { background-color: #00BCD4; color: #000; }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernDashboard()
    window.show()
    sys.exit(app.exec())