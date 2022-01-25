#!/usr/bin/env python3

import wpilib
from wpilib.drive import DifferentialDrive
import ctre
from constants import constants
from networktables import NetworkTables
import navx

class MyRobot(wpilib.TimedRobot):
    """This is a demo program showing how to use Gyro control with the
    DifferentialDrive class."""

    def robotInit(self):
        """Robot initialization function"""
        self.angleSetpoint = 0.0
        self.pGain = 1  # propotional turning constant

        #smart dashboard
        self.sd = NetworkTables.getTable("SmartDashboard")
        # gyro calibration constant, may need to be adjusted
        # gyro value of 360 is set to correspond to one full revolution
        
        # self.voltsPerDegreePerSecond = 0.0128

        self.front_left_motor = ctre.WPI_TalonSRX(constants["frontLeftPort"])
        self.rear_left_motor = ctre.WPI_VictorSPX(constants["rearLeftPort"])
        self.left = wpilib.SpeedControllerGroup(
            self.front_left_motor, self.rear_left_motor)

        self.rear_right_motor = ctre.WPI_TalonSRX(constants["rearRightPort"])
        self.front_right_motor = ctre.WPI_VictorSPX(constants["frontRightPort"])
        self.right = wpilib.SpeedControllerGroup(
            self.front_right_motor, self.rear_right_motor)

        self.drive = wpilib.drive.DifferentialDrive(
            self.right,
            self.left
        )

        self.controller = wpilib.XboxController(0)
        self.timer = wpilib.Timer()
        self.sd = NetworkTables.getTable("SmartDashboard")
        self.gyro = navx.AHRS.create_i2c()


    def teleopInit(self):
        """
        Runs at the beginning of the teleop period
        """
        self.pGain = self.sd.getValue("PGain", self.pGain)
        # self.gyro.setSensitivity(
            # self.voltsPerDegreePerSecond
        # )  # calibrates gyro values to equal degrees

    def teleopPeriodic(self):
        """
        Sets the gyro sensitivity and drives the robot when the joystick is pushed. The
        motor speed is set from the joystick while the RobotDrive turning value is assigned
        from the error between the setpoint and the gyro angle.
        """

        turningValue = (self.angleSetpoint - self.gyro.getYaw()) * self.pGain
        speed = self.controller.getY(self.controller.Hand.kLeftHand)
        if speed >= 0:
            # forwards
            self.drive.arcadeDrive(speed, turningValue)
        elif speed < 0:
            # backwards
            self.drive.arcadeDrive(speed, -turningValue)
        print(self.gyro.getYaw(), turningValue, self.pGain)
        print(self.controller.getY(self.controller.Hand.kLeftHand), self.controller.getY(self.controller.Hand.kRightHand))
        self.sd.putValue("Gyro Yaw", self.gyro.getYaw())
        self.sd.putValue("Turning Value", turningValue)
        self.sd.putValue("PGain", self.pGain)




if __name__ == "__main__":
    wpilib.run(MyRobot)
