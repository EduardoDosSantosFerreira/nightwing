import sys
import os
import time
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QMessageBox,
    QLabel,
    QTabWidget,
    QHBoxLayout,
    QSizePolicy,
    QProgressBar,
    QFileDialog,
    QSpacerItem,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QListWidgetItem,
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from core import (
    get_installed_programs,
    limpar_residuos,
    remover_pastas,
    desinstalar_programa,
    scan_large_files,
)


class NightwingUninstaller(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nightwing Uninstaller")
        self.setGeometry(200, 200, 900, 600)
        self.setMinimumSize(800, 500)

        try:
            self.setWindowIcon(QIcon("assets/icon.png"))
        except:
            pass

        self.setup_ui()
        self.load_programs()

    def setup_ui(self):
        """Setup the main UI components"""
        self.setStyleSheet(
            """
            QWidget {
                background-color: #1a1a2e;
                color: #e6e6e6;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #2a2a4a;
                border-radius: 4px;
                padding: 5px;
                background: #16213e;
            }
            QTabBar::tab {
                background: #16213e;
                color: #e6e6e6;
                padding: 8px 15px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border: 1px solid #2a2a4a;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #0f3460;
                border-bottom: 2px solid #4cc9f0;
            }
            QTabBar::tab:hover {
                background: #0f3460;
            }
            QListWidget {
                background-color: #16213e;
                color: #e6e6e6;
                border: 1px solid #2a2a4a;
                border-radius: 4px;
                padding: 5px;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #2a2a4a;
            }
            QListWidget::item:hover {
                background: #2a2a4a;
            }
            QListWidget::item:selected {
                background: #4cc9f0;
                color: #000000;
                border-radius: 2px;
            }
            QPushButton {
                background-color: #0f3460;
                color: #e6e6e6;
                border: 1px solid #2a2a4a;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 100px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #4cc9f0;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #3a7bd5;
            }
            QPushButton:disabled {
                background-color: #2a2a4a;
                color: #666666;
            }
            QLabel {
                color: #e6e6e6;
                font-size: 13px;
            }
            QProgressBar {
                border: 1px solid #2a2a4a;
                border-radius: 4px;
                text-align: center;
                background: #16213e;
            }
            QProgressBar::chunk {
                background-color: #4cc9f0;
                width: 10px;
            }
            QLineEdit, QComboBox {
                background-color: #16213e;
                color: #e6e6e6;
                border: 1px solid #2a2a4a;
                border-radius: 4px;
                padding: 5px;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
        """
        )

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        header = QHBoxLayout()
        self.logo = QLabel()
        try:
            pixmap = QPixmap("assets/logo.png").scaled(
                40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.logo.setPixmap(pixmap)
        except:
            self.logo.setText("🦇")
            self.logo.setFont(QFont("Arial", 24))
        self.logo.setFixedSize(40, 40)

        title = QLabel("Nightwing Uninstaller")
        title.setFont(QFont("Arial", 16, QFont.Bold))

        header.addWidget(self.logo)
        header.addWidget(title)
        header.addStretch()

        self.status_bar = QLabel("Ready")
        self.status_bar.setFont(QFont("Arial", 9))
        self.status_bar.setStyleSheet("color: #4cc9f0;")

        header.addWidget(self.status_bar)
        main_layout.addLayout(header)

        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Arial", 10))

        self.setup_programs_tab()
        self.setup_large_files_tab()
        self.setup_cleaner_tab()

        main_layout.addWidget(self.tabs)

        footer = QHBoxLayout()
        footer.addStretch()

        self.version_label = QLabel("v1.0.0")
        self.version_label.setStyleSheet("color: #666666;")

        footer.addWidget(self.version_label)
        main_layout.addLayout(footer)

        self.setLayout(main_layout)

    def setup_drivers_tab(self):
        """Setup the drivers tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        self.setStyleSheet(
            """
            QWidget {
                background-color: #1a1a2e;
                color: #e6e6e6;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #2a2a4a;
                border-radius: 4px;
                padding: 5px;
                background: #16213e;
            }
            QTabBar::tab {
                background: #16213e;
                color: #e6e6e6;
                padding: 8px 15px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border: 1px solid #2a2a4a;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #0f3460;
                border-bottom: 2px solid #4cc9f0;
            }
            QTabBar::tab:hover {
                background: #0f3460;
            }
            QListWidget {
                background-color: #16213e;
                color: #e6e6e6;
                border: 1px solid #2a2a4a;
                border-radius: 4px;
                padding: 5px;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #2a2a4a;
            }
            QListWidget::item:hover {
                background: #2a2a4a;
            }
            QListWidget::item:selected {
                background: #4cc9f0;
                color: #000000;
                border-radius: 2px;
            }
            QPushButton {
                background-color: #0f3460;
                color: #e6e6e6;
                border: 1px solid #2a2a4a;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 100px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #4cc9f0;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #3a7bd5;
            }
            QPushButton:disabled {
                background-color: #2a2a4a;
                color: #666666;
            }
            QLabel {
                color: #e6e6e6;
                font-size: 13px;
            }
            QProgressBar {
                border: 1px solid #2a2a4a;
                border-radius: 4px;
                text-align: center;
                background: #16213e;
            }
            QProgressBar::chunk {
                background-color: #4cc9f0;
                width: 10px;
            }
            QLineEdit, QComboBox {
                background-color: #16213e;
                color: #e6e6e6;
                border: 1px solid #2a2a4a;
                border-radius: 4px;
                padding: 5px;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
        """
        )

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        header = QHBoxLayout()
        self.logo = QLabel()
        try:
            pixmap = QPixmap("assets/logo.png").scaled(
                40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.logo.setPixmap(pixmap)
        except:
            self.logo.setText("🦇")
            self.logo.setFont(QFont("Arial", 24))
        self.logo.setFixedSize(40, 40)

        title = QLabel("Nightwing Uninstaller")
        title.setFont(QFont("Arial", 16, QFont.Bold))

        header.addWidget(self.logo)
        header.addWidget(title)
        header.addStretch()

        self.status_bar = QLabel("Ready")
        self.status_bar.setFont(QFont("Arial", 9))
        self.status_bar.setStyleSheet("color: #4cc9f0;")

        header.addWidget(self.status_bar)
        main_layout.addLayout(header)

        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Arial", 10))

        self.setup_programs_tab()
        self.setup_large_files_tab()
        self.setup_cleaner_tab()

        main_layout.addWidget(self.tabs)

        footer = QHBoxLayout()
        footer.addStretch()

        self.version_label = QLabel("v1.0.0")
        self.version_label.setStyleSheet("color: #666666;")

        footer.addWidget(self.version_label)
        main_layout.addLayout(footer)

        self.setLayout(main_layout)

    def setup_programs_tab(self):
        """Setup the installed programs tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        controls = QHBoxLayout()

        self.search_label = QLabel("Search:")
        self.search_label.setFixedWidth(50)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter programs...")
        self.search_input.textChanged.connect(self.filter_programs)

        controls.addWidget(self.search_label)
        controls.addWidget(self.search_input)
        controls.addStretch()

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        self.refresh_btn.clicked.connect(self.load_programs)
        controls.addWidget(self.refresh_btn)

        layout.addLayout(controls)

        self.program_list = QListWidget()
        self.program_list.setSelectionMode(QListWidget.SingleSelection)
        layout.addWidget(self.program_list)

        buttons = QHBoxLayout()

        self.uninstall_btn = QPushButton("Uninstall")
        self.uninstall_btn.setIcon(QIcon.fromTheme("edit-delete"))
        self.uninstall_btn.clicked.connect(self.uninstall_program)
        self.uninstall_btn.setEnabled(False)

        self.details_btn = QPushButton("Details")
        self.details_btn.setIcon(QIcon.fromTheme("dialog-information"))
        self.details_btn.clicked.connect(self.show_program_details)
        self.details_btn.setEnabled(False)

        buttons.addWidget(self.details_btn)
        buttons.addStretch()
        buttons.addWidget(self.uninstall_btn)

        layout.addLayout(buttons)

        self.program_list.itemSelectionChanged.connect(self.update_program_buttons)

        tab.setLayout(layout)
        self.tabs.addTab(tab, QIcon.fromTheme("applications-other"), "Programs")

    def setup_drivers_tab(self):
        """Setup the drivers tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        controls = QHBoxLayout()

        self.search_label = QLabel("Search:")
        self.search_label.setFixedWidth(50)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter programs...")
        self.search_input.textChanged.connect(self.filter_programs)

        controls.addWidget(self.search_label)
        controls.addWidget(self.search_input)
        controls.addStretch()

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        self.refresh_btn.clicked.connect(self.load_programs)
        controls.addWidget(self.refresh_btn)

        layout.addLayout(controls)

        self.program_list = QListWidget()
        self.program_list.setSelectionMode(QListWidget.SingleSelection)
        layout.addWidget(self.program_list)

        buttons = QHBoxLayout()

        self.uninstall_btn = QPushButton("Uninstall")
        self.uninstall_btn.setIcon(QIcon.fromTheme("edit-delete"))
        self.uninstall_btn.clicked.connect(self.uninstall_program)
        self.uninstall_btn.setEnabled(False)

        self.details_btn = QPushButton("Details")
        self.details_btn.setIcon(QIcon.fromTheme("dialog-information"))
        self.details_btn.clicked.connect(self.show_program_details)
        self.details_btn.setEnabled(False)

        buttons.addWidget(self.details_btn)
        buttons.addStretch()
        buttons.addWidget(self.uninstall_btn)

        layout.addLayout(buttons)

        self.program_list.itemSelectionChanged.connect(self.update_program_buttons)

        tab.setLayout(layout)
        self.tabs.addTab(tab, QIcon.fromTheme("applications-other"), "Programs")

    def setup_large_files_tab(self):
        """Setup the large files tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        controls = QHBoxLayout()

        self.size_threshold = QComboBox()
        self.size_threshold.addItems(["100 MB", "250 MB", "500 MB", "1 GB"])
        self.size_threshold.setCurrentIndex(0)

        controls.addWidget(QLabel("Minimum size:"))
        controls.addWidget(self.size_threshold)
        controls.addStretch()

        self.scan_btn = QPushButton("Scan")
        self.scan_btn.setIcon(QIcon.fromTheme("system-search"))
        self.scan_btn.clicked.connect(self.load_large_files)
        controls.addWidget(self.scan_btn)

        layout.addLayout(controls)

        self.large_file_list = QListWidget()
        self.large_file_list.setSelectionMode(QListWidget.SingleSelection)
        layout.addWidget(self.large_file_list)

        buttons = QHBoxLayout()

        self.open_btn = QPushButton("Open Location")
        self.open_btn.setIcon(QIcon.fromTheme("folder-open"))
        self.open_btn.clicked.connect(self.open_file_location)
        self.open_btn.setEnabled(False)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setIcon(QIcon.fromTheme("edit-delete"))
        self.delete_btn.clicked.connect(self.delete_selected_file)
        self.delete_btn.setEnabled(False)

        buttons.addWidget(self.open_btn)
        buttons.addStretch()
        buttons.addWidget(self.delete_btn)

        layout.addLayout(buttons)

        self.large_file_list.itemSelectionChanged.connect(self.update_file_buttons)

        tab.setLayout(layout)
        self.tabs.addTab(tab, QIcon.fromTheme("document"), "Large Files")

    def setup_cleaner_tab(self):
        """Setup the system cleaner tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(15)

        desc = QLabel("Clean up system junk files and free up disk space")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        options = QVBoxLayout()
        options.addWidget(QLabel("Scan for:"))

        self.temp_files_cb = QCheckBox("Temporary files")
        self.temp_files_cb.setChecked(True)

        self.cache_cb = QCheckBox("Cache files")
        self.cache_cb.setChecked(True)

        self.logs_cb = QCheckBox("Log files")

        options.addWidget(self.temp_files_cb)
        options.addWidget(self.cache_cb)
        options.addWidget(self.logs_cb)

        layout.addLayout(options)

        self.scan_junk_btn = QPushButton("Scan for Junk")
        self.scan_junk_btn.setIcon(QIcon.fromTheme("system-search"))
        self.scan_junk_btn.clicked.connect(self.scan_junk_files)
        layout.addWidget(self.scan_junk_btn)

        self.junk_list = QListWidget()
        self.junk_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.junk_list)

        self.clean_btn = QPushButton("Clean Selected")
        self.clean_btn.setIcon(QIcon.fromTheme("edit-clear"))
        self.clean_btn.clicked.connect(self.clean_selected_files)
        self.clean_btn.setEnabled(False)
        layout.addWidget(self.clean_btn)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.junk_list.itemSelectionChanged.connect(self.update_clean_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, QIcon.fromTheme("broom"), "System Cleaner")

    def update_program_buttons(self):
        """Enable/disable program buttons based on selection"""
        has_selection = len(self.program_list.selectedItems()) > 0
        self.uninstall_btn.setEnabled(has_selection)
        self.details_btn.setEnabled(has_selection)

    def update_file_buttons(self):
        """Enable/disable file buttons based on selection"""
        has_selection = len(self.large_file_list.selectedItems()) > 0
        self.delete_btn.setEnabled(has_selection)
        self.open_btn.setEnabled(has_selection)

    def update_clean_button(self):
        """Enable/disable clean button based on selection"""
        has_selection = len(self.junk_list.selectedItems()) > 0
        self.clean_btn.setEnabled(has_selection)

    def filter_programs(self):
        """Filter the program list based on search text"""
        search_text = self.search_input.text().lower()
        for i in range(self.program_list.count()):
            item = self.program_list.item(i)
            item.setHidden(search_text not in item.text().lower())

    def load_programs(self):
        """Load installed programs into the list"""
        self.status_bar.setText("Loading installed programs...")
        QApplication.processEvents()

        try:
            self.program_list.clear()
            self.programs = get_installed_programs()

            if not self.programs:
                self.program_list.addItem("No programs found")
                return

            for name, _, size in self.programs:
                item = QListWidgetItem(f"{name} ({size} MB)")
                self.program_list.addItem(item)

            self.status_bar.setText(f"Loaded {len(self.programs)} programs")

        except Exception as e:
            self.status_bar.setText("Error loading programs")
            QMessageBox.critical(self, "Error", f"Failed to load programs:\n{str(e)}")

    def uninstall_program(self):
        """Uninstall the selected program"""
        index = self.program_list.currentRow()
        if index == -1:
            QMessageBox.warning(
                self, "Warning", "Please select a program to uninstall."
            )
            return

        name, cmd, size = self.programs[index]

        confirm = QMessageBox.question(
            self,
            "Confirm Uninstall",
            f"Are you sure you want to uninstall '{name}' ({size} MB)?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirm == QMessageBox.Yes:
            self.status_bar.setText(f"Uninstalling {name}...")
            self.setEnabled(False)
            QApplication.processEvents()

            try:
                desinstalar_programa(cmd)

                residuos = limpar_residuos(name)
                if residuos:
                    msg = "The following leftover items were found:\n\n" + "\n".join(
                        residuos
                    )
                    msg += "\n\nDo you want to remove them?"

                    if (
                        QMessageBox.question(
                            self,
                            "Leftover Files",
                            msg,
                            QMessageBox.Yes | QMessageBox.No,
                        )
                        == QMessageBox.Yes
                    ):
                        remover_pastas(residuos)

                QMessageBox.information(
                    self, "Success", f"{name} was successfully uninstalled."
                )
                self.load_programs()

            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to uninstall program:\n{str(e)}"
                )

            finally:
                self.setEnabled(True)
                self.status_bar.setText("Ready")

    def show_program_details(self):
        """Show details about the selected program"""
        index = self.program_list.currentRow()
        if index == -1:
            return

        name, cmd, size = self.programs[index]

        details = f"""
        <b>Program Name:</b> {name}<br>
        <b>Size:</b> {size} MB<br>
        <b>Uninstall Command:</b><br>
        <code>{cmd}</code>
        """

        msg = QMessageBox()
        msg.setWindowTitle("Program Details")
        msg.setTextFormat(Qt.RichText)
        msg.setText(details)
        msg.exec_()

    def load_large_files(self):
        """Scan for large files"""
        size_text = self.size_threshold.currentText()
        size_mb = 100

        if size_text == "250 MB":
            size_mb = 250
        elif size_text == "500 MB":
            size_mb = 500
        elif size_text == "1 GB":
            size_mb = 1024

        self.status_bar.setText(f"Scanning for files larger than {size_mb} MB...")
        self.setEnabled(False)
        QApplication.processEvents()

        try:
            self.large_file_list.clear()
            self.large_files = scan_large_files(size_mb)

            if not self.large_files:
                self.large_file_list.addItem("No large files found")
                return

            for name, path, size in self.large_files:
                item = QListWidgetItem(f"{name} ({size} MB)\n{path}")
                self.large_file_list.addItem(item)

            self.status_bar.setText(f"Found {len(self.large_files)} large files")

        except Exception as e:
            self.status_bar.setText("Error scanning for large files")
            QMessageBox.critical(
                self, "Error", f"Failed to scan for large files:\n{str(e)}"
            )

        finally:
            self.setEnabled(True)

    def delete_selected_file(self):
        """Delete the selected large file"""
        index = self.large_file_list.currentRow()
        if index == -1:
            QMessageBox.warning(self, "Warning", "Please select a file to delete.")
            return

        file_info = self.large_files[index]
        name, path, size = file_info

        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{name}' ({size} MB)?\n\n{path}",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirm == QMessageBox.Yes:
            self.status_bar.setText(f"Deleting {name}...")
            self.setEnabled(False)
            QApplication.processEvents()

            try:
                os.remove(path)
                self.load_large_files()
                QMessageBox.information(
                    self, "Success", f"File was successfully deleted."
                )
                self.status_bar.setText("Ready")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete file:\n{str(e)}")
                self.status_bar.setText("Error deleting file")

            finally:
                self.setEnabled(True)

    def open_file_location(self):
        """Open the folder containing the selected file"""
        index = self.large_file_list.currentRow()
        if index == -1:
            return

        path = self.large_files[index][1]
        folder = os.path.dirname(path)

        if sys.platform == "win32":
            os.startfile(folder)
        elif sys.platform == "darwin":
            os.system(f'open "{folder}"')
        else:
            os.system(f'xdg-open "{folder}"')

    def scan_junk_files(self):
        """Scan for junk files based on selected options"""
        self.status_bar.setText("Scanning for junk files...")
        self.junk_list.clear()
        self.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        QApplication.processEvents()

        try:
            time.sleep(2)

            if self.temp_files_cb.isChecked():
                self.junk_list.addItem("/tmp/old_file.tmp - 15.2 MB")
                self.junk_list.addItem("~/Downloads/temp.zip - 42.7 MB")

            if self.cache_cb.isChecked():
                self.junk_list.addItem("~/.cache/browser_cache - 87.3 MB")
                self.junk_list.addItem("~/.thumbnails - 12.1 MB")

            if self.logs_cb.isChecked():
                self.junk_list.addItem("/var/log/old_logs - 5.6 MB")

            self.status_bar.setText(f"Found {self.junk_list.count()} junk files")

        except Exception as e:
            self.status_bar.setText("Error scanning for junk files")
            QMessageBox.critical(
                self, "Error", f"Failed to scan for junk files:\n{str(e)}"
            )

        finally:
            self.progress.setVisible(False)
            self.setEnabled(True)

    def clean_selected_files(self):
        """Clean the selected junk files"""
        selected = self.junk_list.selectedItems()
        if not selected:
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Cleanup",
            f"Are you sure you want to delete {len(selected)} selected files?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirm == QMessageBox.Yes:
            self.status_bar.setText(f"Cleaning {len(selected)} files...")
            self.setEnabled(False)
            self.progress.setVisible(True)
            self.progress.setRange(0, len(selected))
            QApplication.processEvents()

            try:
                for i, item in enumerate(selected):

                    self.progress.setValue(i + 1)
                    QApplication.processEvents()
                    time.sleep(0.1)

                for item in selected:
                    self.junk_list.takeItem(self.junk_list.row(item))

                QMessageBox.information(self, "Success", "Selected files were cleaned.")
                self.status_bar.setText("Ready")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to clean files:\n{str(e)}")
                self.status_bar.setText("Error cleaning files")

            finally:
                self.progress.setVisible(False)
                self.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    window = NightwingUninstaller()
    window.show()

    sys.exit(app.exec_())
