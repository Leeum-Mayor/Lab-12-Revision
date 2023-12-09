from logic import *


def main() -> None:
    """
    Runs application and loads the window
    """
    application = QApplication([])
    window = Television()
    window.show()
    application.exec()


if __name__ == '__main__':
    main()
