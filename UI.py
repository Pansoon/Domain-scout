import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog,
    QRadioButton, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox, QGridLayout, QStatusBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from IP_address import resolve_domain_to_ip  # Make sure these imports match your project structure
from PORT_scan import scan_ports
from HTTP_status import get_http_status_code
from report import generate_report
from config import load_config

class ScanWorker(QThread):
    update_status = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, domains, config):
        super().__init__()
        self.domains = domains
        self.config = config

    def run(self):
        results_list = []

        try:
            for domain in self.domains:
                sanitized_domain = re.sub(r'[\\/:"*?<>|]', '_', domain)
                self.update_status.emit(f"Starting scan for {domain}...")

                # Step 1: Resolve domain to IP
                ip_address = resolve_domain_to_ip(domain)
                if not ip_address:
                    self.update_status.emit(f"Failed to resolve IP for {domain}.")
                    continue
                self.update_status.emit(f"Resolved IP for {domain}: {ip_address}")

                # Step 2: Scan ports with the loaded configuration
                ports = self.config['ports'] if self.config else [80, 443, 22]
                port_status = scan_ports(ip_address, ports)
                self.update_status.emit(f"Port scan results for {domain}: {port_status}")

                # Step 3: Get HTTP status code
                http_status = get_http_status_code(domain)
                self.update_status.emit(f"HTTP status code for {domain}: {http_status}")

                # Step 4: Aggregate results
                results = {
                    "Domain Name": sanitized_domain,
                    "IP Address": ip_address,
                    "Port Status": port_status,
                    "HTTP Status": http_status
                }

                results_list.append(results)

            # Step 5: Generate the report
            if results_list:
                report_type = 'pdf' if self.config['report_type'] == 'pdf' else 'text'
                generate_report(results_list, report_type=report_type)
                self.update_status.emit(f"Report generated successfully.")
            else:
                self.update_status.emit("No valid results to report.")

        except Exception as e:
            self.update_status.emit(f"An error occurred: {str(e)}")

        self.finished.emit()  # Signal that the thread is finished


class DomainScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_config = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Domain Scanner Tool")
        self.setGeometry(100, 100, 600, 400)  # Set window size
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Grid layout for input and options
        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        # Domain Entry
        domain_label = QLabel("Enter Domain(s):")
        domain_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        grid_layout.addWidget(domain_label, 0, 0)
        self.entry_domain = QLineEdit()
        grid_layout.addWidget(self.entry_domain, 0, 1)

        # Load from File Button
        load_button = QPushButton("Load from File")
        load_button.clicked.connect(self.load_domains_from_file)
        grid_layout.addWidget(load_button, 0, 2)

        # Report Type Option
        report_type_label = QLabel("Report Type:")
        report_type_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        grid_layout.addWidget(report_type_label, 1, 0)
        report_type_layout = QHBoxLayout()
        self.report_type_var_text = QRadioButton("Text")
        self.report_type_var_text.setChecked(True)
        self.report_type_var_pdf = QRadioButton("PDF")
        report_type_layout.addWidget(self.report_type_var_text)
        report_type_layout.addWidget(self.report_type_var_pdf)
        grid_layout.addLayout(report_type_layout, 1, 1)

        # Load Config Button
        config_button = QPushButton("Load Config")
        config_button.clicked.connect(self.load_config_file)
        grid_layout.addWidget(config_button, 1, 2)

        # Run Scan Button
        scan_button = QPushButton("Run Scan")
        scan_button.clicked.connect(self.run_scan)
        layout.addWidget(scan_button)

        # Results Display
        self.text_results = QTextEdit()
        self.text_results.setReadOnly(True)
        layout.addWidget(self.text_results)

        # Clear Button
        clear_button = QPushButton("Clear Results")
        clear_button.clicked.connect(self.clear_results)
        layout.addWidget(clear_button)

        # Help Button
        help_button = QPushButton("Help")
        help_button.clicked.connect(self.show_help)
        layout.addWidget(help_button)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def load_domains_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Domain File", "", "Text files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    domains = [line.strip() for line in file if line.strip()]
                self.display_message(f"Loaded domains from {file_path}")
                self.entry_domain.setText(", ".join(domains))
            except Exception as e:
                self.display_error(f"Error loading file: {e}")
        else:
            self.display_error("No file selected")

    def load_config_file(self):
        config_file_path, _ = QFileDialog.getOpenFileName(self, "Open Config File", "", "Configuration files (*.json *.txt)")
        if config_file_path:
            try:
                self.current_config = load_config(config_file_path)
                self.display_message(f"Configuration loaded from '{config_file_path}'")
            except Exception as e:
                self.display_error(f"Error loading configuration file: {e}")
        else:
            self.display_error("No configuration file selected")

    def run_scan(self):
        # Ensure that the configuration is initialized
        if self.current_config is None:
            self.current_config = {
                'ports': [80, 443, 22],  # Default ports to scan
                'report_type': 'text'  # Default report type
            }

        # Collect domain inputs and configuration
        domain_input = self.entry_domain.text().strip()
        domains = [domain.strip() for domain in domain_input.split(',')]  # Support multiple domains
        if not domains:
            self.display_error("No domains provided.")
            return

        report_type = 'pdf' if self.report_type_var_pdf.isChecked() else 'text'
        self.current_config['report_type'] = report_type

        # Start the background scan worker
        self.worker = ScanWorker(domains, self.current_config)
        self.worker.update_status.connect(self.display_message)
        self.worker.finished.connect(self.scan_finished)
        self.worker.start()

    def scan_finished(self):
        self.display_message("Scan completed.")

    def clear_results(self):
        self.text_results.clear()
        self.display_message("Results cleared.")

    def show_help(self):
        help_text = ("Enter one or more domain names, separated by commas.\n"
                     "You can also load a list of domains from a text file.\n"
                     "Choose the report type (Text or PDF) and click 'Run Scan'.\n"
                     "Use the 'Clear Results' button to clear the output.")
        QMessageBox.information(self, "Help", help_text)

    def display_message(self, message):
        self.text_results.append(message)
        self.status_bar.showMessage(message, 5000)  # Show the message in the status bar for 5 seconds

    def display_error(self, message):
        QMessageBox.critical(self, "Error", message)
        self.status_bar.showMessage(f"Error: {message}", 5000)

def main():
    import sys
    app = QApplication(sys.argv)
    scanner_app = DomainScannerApp()
    scanner_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
