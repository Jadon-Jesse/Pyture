if __name__ == '__main__':
    import sys
    from PyQt5 import QtWidgets
    from package.app import PytureApplication

    app = QtWidgets.QApplication(sys.argv)


    pyture_app = PytureApplication()
    # appTimer = QtCore.QTimer()
    # appTimer.timeout.connect(lambda: None)
    # appTimer.start(100)

    pyture_app.show()
    sys.exit(app.exec_())
