import re
import time
import sys
import argparse  # สำหรับการอ่าน arguments
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog,
    QRadioButton, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox, QGridLayout, QStatusBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from IP_address import resolve_domain_to_ip
from PORT_scan import scan_ports
from HTTP_status import get_http_status_code
from report import generate_report
from config import load_config
from screenshot_module import capture_domain_screenshot
from datetime import datetime
from output_storage import save_scan_results  # Import the save_scan_results function



# Set up logging to a file
logging.basicConfig(filename='http_status_debug.log', level=logging.INFO)

import re
import time
import logging
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime
from IP_address import resolve_domain_to_ip
from PORT_scan import scan_ports
from HTTP_status import get_http_status_code
from screenshot_module import capture_domain_screenshot
from report import generate_report
from output_storage import save_scan_results


class ScanWorker(QThread):
    update_status = pyqtSignal(str)
    finished = pyqtSignal()
    domains_received = pyqtSignal(list)  # New signal for domains

    def __init__(self, domains, config, headless):
        super().__init__()
        self.domains = domains
        self.config = config
        self.headless = headless  # Headless (fast scan) or full browser (detailed scan)

    def run(self):
        results_list = []
        scan_results_to_save = []  # List to store scan results for saving
        
        self.domains_received.emit(self.domains)  # Emit domains when scan starts
        
        try:
            for domain in self.domains:
                sanitized_domain = re.sub(r'[\\/:*?"<>|]', '_', domain)
                self.update_status.emit(f"Starting scan for {domain}...")

                # Initialize variables to ensure they are always defined
                http_status_code = "N/A"
                http_status_desc = "N/A"
                ip_address = None
                port_status = {}
                screenshot_path = None
                redirected_url = None  # Store redirected URL

                # Step 1: Resolve domain to IP
                try:
                    ip_address = resolve_domain_to_ip(domain)
                    if not ip_address:
                        self.update_status.emit(f"Failed to resolve IP for {domain}.")
                        continue
                    self.update_status.emit(f"Resolved IP for {domain}: {ip_address}")
                except Exception as e:
                    self.update_status.emit(f"Error resolving IP for {domain}: {str(e)}")
                    continue

                # Step 2: Scan ports
                try:
                    ports = self.config.get('ports', [80, 443, 22])
                    port_status = scan_ports(ip_address, ports)
                    self.update_status.emit(f"Port scan results for {domain}: {port_status}")
                except Exception as e:
                    self.update_status.emit(f"Error scanning ports for {domain}: {str(e)}")
                    port_status = {}

                # Step 3: Get HTTP status code
                try:
                    http_status_code, http_status_desc = get_http_status_code(domain)
                    logging.info(f"Raw HTTP response for {domain}: {http_status_code} - {http_status_desc}")
                    
                    if http_status_code is None:
                        http_status_code, http_status_desc = "N/A", "N/A"
                        logging.warning(f"Empty or None HTTP status code for {domain}, defaulting to 'N/A'")
                    
                    self.update_status.emit(f"HTTP status code for {domain}: {http_status_code} - {http_status_desc}")
                except Exception as e:
                    self.update_status.emit(f"Failed to retrieve HTTP status for {domain}: {str(e)}")
                    http_status_code, http_status_desc = "N/A", "N/A"
                    logging.error(f"Error retrieving HTTP status for {domain}: {str(e)}")

                # Step 4: Capture a screenshot and get redirected URL
                try:
                    self.update_status.emit(f"Capturing screenshot for {domain}...")

                    # Capture screenshot and ensure it waits for full completion, also capture redirected URL
                    screenshot_path, redirected_url = capture_domain_screenshot(f"http://{domain}", headless=self.headless)
                    mode = "headless" if self.headless else "full browser mode"
                    self.update_status.emit(f"Screenshot captured for {domain} in {mode}. Saved to: {screenshot_path}")
                    self.update_status.emit(f"Redirected URL: {redirected_url}")

                    # Add a small delay to ensure the screenshot process completes
                    time.sleep(3)

                except Exception as e:
                    self.update_status.emit(f"Failed to capture screenshot for {domain}: {str(e)}")

                # Step 5: Aggregate results
                results = {
                    "Domain Name": sanitized_domain,
                    "IP Address": ip_address,
                    "Port Status": port_status,
                    "HTTP Status": f"{http_status_code} - {http_status_desc}",
                    "Screenshot": screenshot_path,
                    "Redirected URL": redirected_url  # Include the redirected URL
                }

                results_list.append(results)
                self.update_status.emit(f"Aggregated results for {domain}")

                # Step 6: Prepare scan results for saving
                scan_results_to_save.append({
                    'domain_name': sanitized_domain,
                    'scan_date': datetime.now().strftime('%Y-%m-%d'),
                    'port_status': port_status,
                    'http_status_code': http_status_code,
                    'http_status_desc': http_status_desc,
                    'additional_info': screenshot_path,
                    'redirected_url': redirected_url,  # Save the redirected URL
                    'type_of_phishing': 'N/A'  # Modify this based on your logic
                })

                # Step 7: Wait between domain scans to ensure synchronization
                self.update_status.emit(f"Waiting before scanning the next domain...")
                time.sleep(5)  # Wait 5 seconds before moving to the next domain

            # Step 8: Generate the report
            if results_list:
                try:
                    report_type = 'pdf' if self.config.get('report_type') == 'pdf' else 'text'
                    generate_report(results_list, report_type=report_type)
                    self.update_status.emit(f"Report generated successfully.")
                except Exception as e:
                    self.update_status.emit(f"Failed to generate report: {str(e)}")
            else:
                self.update_status.emit("No valid results to report.")

            # Step 9: Save the scan results to CSV
            try:
                save_scan_results(scan_results_to_save)
                self.update_status.emit(f"Scan results saved to output storage.")
            except Exception as e:
                self.update_status.emit(f"Failed to save scan results: {str(e)}")

        except Exception as e:
            self.update_status.emit(f"An unexpected error occurred: {str(e)}")

        # Signal that the scanning is complete
        self.finished.emit()

class DomainScannerApp(QMainWindow):
    def __init__(self, domains=None, reportType=None, scanType=None):  # เพิ่มพารามิเตอร์ domains
        super().__init__()
        self.current_config = None
        self.worker = None  # Track the worker thread
        self.initUI()

        if domains:  # ถ้ามี domain ส่งเข้ามา ให้ตั้งค่าเริ่มต้นใน input
            self.set_domains(domains)
            
        if reportType:
            self.set_report_type(reportType)
            
        if scanType:
            self.set_scan_type(scanType)

    def set_domains(self, domains):
        logging.info(f"Domains received: {domains}")  
        if isinstance(domains, list):
            self.entry_domain.setText(", ".join(domains))
        else:
            self.entry_domain.setText(domains)

    def set_report_type(self, reportType):
        if reportType == 'text':
         self.report_type_var_text.setChecked(True)
        else:
            self.report_type_var_pdf.setChecked(True)

    def set_scan_type(self, scanType):
        """
        Automatically triggers the appropriate scan based on the scanType received.
        """
        if scanType == 'fast':
            self.run_fast_scan()  # Automatically trigger fast scan
        elif scanType == 'detailed':
            self.run_detailed_scan()  # Automatically trigger detailed scan

    def run_fast_scan(self):
        print("Fast scan started")
        self.run_scan(headless=True)  # Simulate Fast Scan

    def run_detailed_scan(self):
        print("Detailed scan started")
        self.run_scan(headless=False)  # Simulate Detailed Scan


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

        # Fast Scan and Detailed Scan Buttons
        self.fast_scan_button = QPushButton("Fast Scan")
        self.fast_scan_button.clicked.connect(self.start_fast_scan)
        layout.addWidget(self.fast_scan_button)

        self.detailed_scan_button = QPushButton("Detailed Scan")
        self.detailed_scan_button.clicked.connect(self.start_detailed_scan)
        layout.addWidget(self.detailed_scan_button)

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

    def start_fast_scan(self):
        self.run_scan(headless=True)

    def start_detailed_scan(self):
        self.run_scan(headless=False)

    def run_scan(self, headless):
        # Ensure that the configuration is initialized
        if self.current_config is None:
            self.current_config = {
                'ports': [80, 443, 22],  # Default ports to scan
                'report_type': 'text'  # Default report type
            }

        # Collect domain inputs and configuration
        domain_input = self.entry_domain.text().strip()

        # Ensure domain_input is a string
        if not isinstance(domain_input, str):
            self.display_error("Invalid input: Expected a string for domains.")
            return

        # Support multiple domains, split by comma
        domains = [domain.strip() for domain in domain_input.split(',')]
        if not domains or domains == ['']:
            self.display_error("No domains provided.")
            return

        # Prevent starting another scan while one is running
        if self.worker and self.worker.isRunning():
            self.display_message("A scan is already in progress. Please wait.")
            return

        report_type = 'pdf' if self.report_type_var_pdf.isChecked() else 'text'
        self.current_config['report_type'] = report_type

        logging.info(f"Selected report type: {self.current_config['report_type']}")
        
        # Start the background scan worker
        self.worker = ScanWorker(domains, self.current_config, headless=headless)
        self.worker.update_status.connect(self.display_message)
        self.worker.finished.connect(self.scan_finished)
        self.worker.finished.connect(self.cleanup_thread)  # Connect to cleanup function
        self.worker.domains_received.connect(self.set_domains)
        self.worker.start()

    def cleanup_thread(self):
        """Cleanup the thread after it finishes to prevent dangling threads."""
        self.worker = None

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


def main(domains=None, reportType=None,scanType=None):  # เพิ่ม domains argument เพื่อส่งค่าเข้าไปในฟังก์ชัน
    app = QApplication(sys.argv)
    scanner_app = DomainScannerApp(domains, reportType, scanType)
    scanner_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Domain Scanner with PyQt5 UI")
    parser.add_argument('domains', nargs='*', help="List of domains to scan")
    parser.add_argument('reportType', choices=['text', 'pdf'], default='text', help="Report type (text or pdf)")
    parser.add_argument('scanType', choices=['fast', 'detailed'], default='fast', help="Scan type (fast or detailed)")
    args = parser.parse_args()

main(args.domains, args.reportType, args.scanType)  # Pass reportType to the main function
