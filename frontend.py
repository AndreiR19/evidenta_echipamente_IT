from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem,
    QFrame, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
import sys

class ModernDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Evidență Echipamente IT - Parchet Brăila")
        self.resize(1000, 600)
        self.setStyleSheet(self.styles())

        # Main layout
        root = QHBoxLayout(self)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(20)

        logo = QLabel("⚙️ IT Manager")
        logo.setObjectName("logo")
        sidebar_layout.addWidget(logo)

        buttons = ["Dashboard", "Adaugă", "Echipamente", "Utilizatori", "Setări"]
        for name in buttons:
            btn = QPushButton(name)
            btn.setObjectName("menuButton")
            sidebar_layout.addWidget(btn)

        sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("logoutButton")
        sidebar_layout.addWidget(logout_btn)

        # Main content area
        content = QFrame()
        content.setObjectName("content")
        content_layout = QVBoxLayout(content)

        title = QLabel("Echipamente IT")
        title.setObjectName("title")
        content_layout.addWidget(title)

        # Search bar
        top_bar = QHBoxLayout()
        search = QLineEdit()
        search.setPlaceholderText("🔍 Caută echipament...")
        add_button = QPushButton("+ Adaugă echipament")
        add_button.setObjectName("primaryButton")
        top_bar.addWidget(search)
        top_bar.addWidget(add_button)
        content_layout.addLayout(top_bar)

        # Table
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["ID", "Denumire", "Categorie", "Serie"])
        table.verticalHeader().setVisible(False)
        content_layout.addWidget(table)

        # Sample data
        data = [
            (1, "Laptop Lenovo ThinkPad", "Laptop", "SN12345"),
            (2, "Monitor Dell 24\"", "Monitor", "SN54321"),
            (3, "Imprimantă HP LaserJet", "Periferic", "SN98765"),
        ]
        for row, item in enumerate(data):
            table.insertRow(row)
            for col, val in enumerate(item):
                table.setItem(row, col, QTableWidgetItem(str(val)))

        root.addWidget(sidebar, 1)
        root.addWidget(content, 4)

    def styles(self):
        return """
        QWidget {
            background-color: #121212;
            color: #E8EAED;
            font-family: 'Segoe UI';
            font-size: 14px;
        }

        #sidebar {
            background-color: #1E1E1E;
            border-top-left-radius: 16px;
            border-bottom-left-radius: 16px;
            padding: 20px;
        }

        #logo {
            font-size: 20px;
            font-weight: bold;
            color: #00BCD4;
            margin-bottom: 20px;
        }

        #menuButton {
            background-color: transparent;
            color: #E8EAED;
            text-align: left;
            padding: 10px 14px;
            border-radius: 8px;
        }

        #menuButton:hover {
            background-color: #2D2D2D;
            color: #00BCD4;
        }

        #logoutButton {
            background-color: #2B2B2B;
            color: #FF5252;
            border-radius: 8px;
            padding: 8px;
        }

        #logoutButton:hover {
            background-color: #3C4043;
        }

        #content {
            background-color: #181818;
            border-top-right-radius: 16px;
            border-bottom-right-radius: 16px;
            padding: 25px;
        }

        #title {
            font-size: 22px;
            font-weight: bold;
            color: #00BCD4;
            margin-bottom: 15px;
        }

        QLineEdit {
            background-color: #242424;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 8px 12px;
            color: #E8EAED;
        }

        QLineEdit:focus {
            border: 1px solid #00BCD4;
        }

        QPushButton#primaryButton {
            background-color: #00BCD4;
            color: #121212;
            font-weight: bold;
            border-radius: 8px;
            padding: 8px 16px;
        }

        QPushButton#primaryButton:hover {
            background-color: #14D3E0;
        }

        QTableWidget {
            background-color: #202124;
            border: 1px solid #333;
            border-radius: 10px;
            gridline-color: #333;
            selection-background-color: #00BCD4;
            selection-color: #121212;
        }

        QHeaderView::section {
            background-color: #2A2A2A;
            color: #E8EAED;
            border: none;
            padding: 8px;
        }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernDashboard()
    window.show()
    sys.exit(app.exec())
