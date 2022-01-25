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
        pass
        # print("The drive X value is: ", self.controller.getX(
        #     self.controller.Hand.kLeftHand))
        # print("The drive Y value is: ", self.controller.getY(
        #     self.controller.Hand.kLeftHand))
        # print("The gyro Yaw value is: ", self.gyro.getYaw())
        # self.sd.putValue("Gyro Yaw", self.gyro.getYaw())
        # self.sd.putValue("Left Encoder Value",
        #                  self.front_left_motor.getSelectedSonsorPosition())
        # self.sd.putValue("Right Encoder Value",
        #                  self.front_right_motor.getSelectedSensorPosition())
# 		self.drive.arcadeDrive(
# 			self.controller.getX(self.controller.Hand.kLeftHand),
# 			self.controller.getY(self.controller.Hand.kLeftHand),
# 			True
# 		)
        #isAPressed = self.controller.getAButton()
        #isBPressed = self.controller.getBButton()
        #isXPressed = self.controller.getXButton()
        #isYPressed = self.controller.getYButton()
        #if(isAPressed):
        #   self.front_left_motor.set(0.5)
        #if(isBPressed):
        #   self.rear_left_motor.set(0.5)
        #if(isXPressed):
        #   self.front_right_motor.set(0.5)
        #if(isYPressed):
        #   self.rear_right_motor.set(0.5)


if __name__ == "__main__":
    wpilib.run(MyRobot)
