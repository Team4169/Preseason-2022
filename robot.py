import wpilib
import wpilib.drive
import ctre
from constants import constants
from networktables import NetworkTables
import navx

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.front_left_motor = ctre.WPI_TalonSRX(constants["frontLeftPort"])
        self.rear_left_motor = ctre.WPI_VictorSPX(constants["rearLeftPort"])
        self.rear_left_motor.setInverted(True)
        self.left = wpilib.SpeedControllerGroup(
            self.front_left_motor, self.rear_left_motor)

        self.front_right_motor = ctre.WPI_TalonSRX(constants["frontRightPort"])
        self.rear_right_motor = ctre.WPI_VictorSPX(constants["rearRightPort"])
        self.rear_right_motor.setInverted(True)
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
        self.front_left_motor.configSelectedFeedbackSensor(
            ctre.FeedbackDevice.QuadEncoder, 0, 0)
        self.front_right_motor.configSelectedFeedbackSensor(
            ctre.FeedbackDevice.QuadEncoder, 0, 0)

    def autnomousInit(self):
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        print("The drive X value is: ", self.controller.getX(
            self.controller.Hand.kLeftHand))
        print("The drive Y value is: ", self.controller.getY(
            self.controller.Hand.kLeftHand))
        print("The gyro Yaw value is: ", self.gyro.getYaw())
        self.sd.putValue("Gyro Yaw", self.gyro.getYaw())
        self.sd.putValue("Left Encoder Value",
                         self.front_left_motor.getSelectedSonsorPosition())
        self.sd.putValue("Right Encoder Value",
                         self.front_right_motor.getSelectedSensorPosition())
# 		self.drive.arcadeDrive(
# 			self.controller.getX(self.controller.Hand.kLeftHand),
# 			self.controller.getY(self.controller.Hand.kLeftHand),
# 			True
# 		)
        isAPressed = self.controller.getAButton()
        isBPressed = self.controller.getBButton()
        isXPressed = self.controller.getXButton()
        isYPressed = self.controller.getYButton()
        if(isAPressed):
            self.front_left_motor.set(0.5)
        if(isBPressed):
            self.rear_left_motor.set(0.5)
        if(isXPressed):
            self.front_right_motor.set(0.5)
        if(isYPressed):
            self.rear_right_motor.set(0.5)


if __name__ == "__main__":
    wpilib.run(MyRobot)
