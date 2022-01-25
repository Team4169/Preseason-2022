#Test Jan 10th
import wpilib
import wpilib.drive
import ctre
from constants import constants
from cscore import CameraServer, UsbCamera
from networktables import NetworkTables
import navx

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        wpilib.CameraServer.launch("vision.py:main")

        self.controller = wpilib.XboxController(0)
        self.timer = wpilib.Timer()
        self.sd = NetworkTables.getTable("SmartDashboard")

    def autnomousInit(self):
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        isAPressed = self.controller.getAButton()
        isBPressed = self.controller.getBButton()
        isXPressed = self.controller.getXButton()
        isYPressed = self.controller.getYButton()


if __name__ == "__main__":
    wpilib.run(MyRobot)
