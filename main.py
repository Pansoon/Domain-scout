from UI import DomainScannerApp
from PyQt5.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    scanner_app = DomainScannerApp()

    # Instead of using get_user_input, we launch the PyQt5 application
    scanner_app.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
