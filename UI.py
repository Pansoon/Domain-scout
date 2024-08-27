import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QRadioButton, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
from IP_address import resolve_domain_to_ip
from PORT_scan import scan_ports
from HTTP_status import get_http_status_code
from aggregation import aggregate_results
from report import generate_report
from config import load_config

class DomainScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_config = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Domain Scanner Tool")
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Domain Entry
        domain_label = QLabel("Enter Domain:")
        self.entry_domain = QLineEdit()
        layout.addWidget(domain_label)
        layout.addWidget(self.entry_domain)

        # Load from File Button
        load_button = QPushButton("Load from File")
        load_button.clicked.connect(self.load_domains_from_file)
        layout.addWidget(load_button)

        # Report Type Option
        report_type_layout = QHBoxLayout()
        report_type_label = QLabel("Report Type:")
        report_type_layout.addWidget(report_type_label)

        self.report_type_var_text = QRadioButton("Text")
        self.report_type_var_text.setChecked(True)
        self.report_type_var_pdf = QRadioButton("PDF")
        report_type_layout.addWidget(self.report_type_var_text)
        report_type_layout.addWidget(self.report_type_var_pdf)
        layout.addLayout(report_type_layout)

        # Load Config Button
        config_button = QPushButton("Load Config")
        config_button.clicked.connect(self.load_config_file)
        layout.addWidget(config_button)

        # Run Scan Button
        scan_button = QPushButton("Run Scan")
        scan_button.clicked.connect(self.run_scan)
        layout.addWidget(scan_button)

        # Results Display
        self.text_results = QTextEdit()
        self.text_results.setReadOnly(True)
        layout.addWidget(self.text_results)

    def sanitize_domain_name(self, domain):
        return re.sub(r'[\\/:"*?<>|]', '_', domain)

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
        domain_input = self.entry_domain.text().strip()
        domains = [domain.strip() for domain in domain_input.split(',')]  # Support multiple domains in a comma-separated list

        if not domains:
            self.display_error("No domains provided.")
            return

        results_list = []

        try:
            for domain in domains:
                sanitized_domain = self.sanitize_domain_name(domain)

                # Step 1: Resolve domain to IP
                ip_address = resolve_domain_to_ip(domain)
                if not ip_address:
                    self.display_error(f"Failed to resolve IP for {domain}.")
                    continue
                self.display_message(f"Resolved IP for {domain}: {ip_address}")

                # Step 2: Scan ports with the loaded configuration
                ports = self.current_config['ports'] if self.current_config else [80, 443, 22]
                port_status = scan_ports(ip_address, ports)
                self.display_message(f"Port scan results for {domain}: {port_status}")

                # Step 3: Get HTTP status code
                http_status = get_http_status_code(domain)
                self.display_message(f"HTTP status code for {domain}: {http_status}")

                # Step 4: Aggregate results
                results = {
                    "Domain Name": sanitized_domain,
                    "IP Address": ip_address,
                    "Port Status": port_status,
                    "HTTP Status": http_status
                }

                results_list.append(results)  # Add the current domain's results to the list

            # Step 5: Display and generate report for all results
            if results_list:
                report_type = 'pdf' if self.report_type_var_pdf.isChecked() else 'text'
                generate_report(results_list, report_type=report_type)
                self.display_message(f"Report generated as {report_type} format for all domains.")
            else:
                self.display_error("No valid results to report.")

        except Exception as e:
            self.display_error(str(e))

    def display_message(self, message):
        self.text_results.append(message)

    def display_error(self, message):
        QMessageBox.critical(self, "Error", message)

def main():
    import sys
    app = QApplication(sys.argv)
    scanner_app = DomainScannerApp()
    scanner_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
