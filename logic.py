from PyQt6.QtWidgets import *
from gui import *


class Television(QMainWindow, Ui_MainWindow):
    """
    Handles the logic for a television object
    """
    MIN_VOLUME = 0
    MAX_VOLUME = 2
    MIN_CHANNEL = 0
    MAX_CHANNEL = 9

    def __init__(self) -> None:
        """
        Assigns channel and volume values, as well as the status of the mute and power toggle by either
        reading from data file or creates a new file and assigns default values.
        """
        super().__init__()
        self.setupUi(self)

        try:
            input_file = open('data.txt', 'r')
            self.data = input_file.readlines()
            for i in range(len(self.data)):
                self.data[i] = self.data[i].rstrip()
            self.__status = bool(self.data[0])
            self.__muted = bool(self.data[1])
            self.__volume = int(self.data[2])
            self.__channel = int(self.data[3])
            input_file.close()

        except (FileNotFoundError, IndexError):
            self.__status = False
            self.__muted = False
            self.__volume = self.MIN_VOLUME
            self.__channel = self.MIN_CHANNEL

        if self.__status == True:
            self.teleScreen.setPixmap(QPixmap(f'images/ch{self.__channel}Pic.png'))
        else:
            self.teleScreen.setPixmap(QPixmap(f'images/PowerOffPic.png'))

        if self.__muted == False and self.__volume > 0 and self.__status == True:
            self.volumeStatus.setPixmap(QPixmap(f'images/vol{self.__volume}.png'))

        self.telePowerButton.clicked.connect(lambda: self.power())
        self.teleMuteButton.clicked.connect(lambda: self.mute())

        self.remotePowerButton.clicked.connect(lambda: self.power())
        self.remoteMuteButton.clicked.connect(lambda: self.mute())
        self.volIncButton.clicked.connect(lambda: self.volume_up())
        self.volDecButton.clicked.connect(lambda: self.volume_down())
        self.chIncButton.clicked.connect(lambda: self.change_channel(-2))
        self.chDecButton.clicked.connect(lambda: self.change_channel(-1))
        self.chOneButton.clicked.connect(lambda: self.change_channel(1))
        self.chTwoButton.clicked.connect(lambda: self.change_channel(2))
        self.chThreeButton.clicked.connect(lambda: self.change_channel(3))
        self.chFourButton.clicked.connect(lambda: self.change_channel(4))
        self.chFiveButton.clicked.connect(lambda: self.change_channel(5))
        self.chSixButton.clicked.connect(lambda: self.change_channel(6))
        self.chSevenButton.clicked.connect(lambda: self.change_channel(7))
        self.chEightButton.clicked.connect(lambda: self.change_channel(8))
        self.chNineButton.clicked.connect(lambda: self.change_channel(9))
        self.chZeroButton.clicked.connect(lambda: self.change_channel(0))

    def power(self) -> None:
        """
        Toggles power status
        """
        if self.__status == True:
            self.teleScreen.setPixmap(QPixmap('images/PowerOffPic.png'))
            self.volumeStatus.setPixmap(QPixmap('null'))
            self.__status = False
        else:
            self.teleScreen.setPixmap(QPixmap(f'images/ch{self.__channel}Pic.png'))
            self.volumeStatus.setPixmap(QPixmap(f'images/vol{self.__volume}'))
            self.__status = True

    def mute(self) -> None:
        """
        Toggles mute status
        """
        if self.__status == True:
            if self.__muted == True:
                self.volumeStatus.setPixmap(QPixmap(f'images/vol{self.__volume}.png'))
                self.__muted = False
            else:
                self.volumeStatus.setPixmap(QPixmap('null'))
                self.__muted = True

    def change_channel(self, value: int) -> None:
        """
        Changes channel up, down, or jumps to channel
        :param value: Indicates how to change channel, -1 goes down, -2 goes up, any other value
        changes the channel to said value
        """
        if self.__status == True:
            if value == -1:
                if self.__channel > self.MIN_CHANNEL:
                    self.__channel -= 1
                else:
                    self.__channel = self.MAX_CHANNEL
            elif value == -2:
                if self.__channel < self.MAX_CHANNEL:
                    self.__channel += 1
                else:
                    self.__channel = self.MIN_CHANNEL
            else:
                self.__channel = value

            self.teleScreen.setPixmap(QPixmap(f'images/ch{self.__channel}Pic.png'))

    def volume_up(self) -> None:
        """
        Turns volume up
        """
        if self.__status == True:
            self.__muted = False
            if self.__volume < self.MAX_VOLUME:
                self.__volume += 1
            self.volumeStatus.setPixmap(QPixmap(f'images/vol{self.__volume}.png'))

    def volume_down(self) -> None:
        """
        Turns volume down
        """
        if self.__status == True:
            self.__muted = False
            if self.__volume > self.MIN_VOLUME:
                self.__volume -= 1
                self.volumeStatus.setPixmap(QPixmap(f'images/vol{self.__volume}.png'))
            else:
                self.volumeStatus.setPixmap(QPixmap('null'))

    def closeEvent(self, event: object) -> None:
        """
        Saves data to a file when window is closed
        """
        output_file = open('data.txt', 'w')
        if self.__status == False:
            output_file.write('\n')
        else:
            output_file.write(f'{str(self.__status)}\n')
        if self.__muted == False:
            output_file.write('\n')
        else:
            output_file.write(f'{str(self.__muted)}\n')

        output_file.write(f'{str(self.__volume)}\n')
        output_file.write(f'{str(self.__channel)}\n')
        output_file.close()
