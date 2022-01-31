#Test Jan 10th
import wpilib
import wpilib.drive
from constants import constants
from networktables import NetworkTables

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        wpilib.CameraServer.launch('vision.py:main')

    def autnomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        pass


if __name__ == "__main__":
    wpilib.run(MyRobot)
