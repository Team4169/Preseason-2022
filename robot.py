import wpilib
import wpilib.drive
import ctre
from constants import constants
from networktables import NetworkTables
import navx
# import Encode


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.front_left_motor = ctre.WPI_TalonSRX(constants["frontLeftPort"])
        self.rear_left_motor = ctre.WPI_VictorSPX(constants["rearLeftPort"])
        self.left = wpilib.SpeedControllerGroup(
            self.front_left_motor, self.rear_left_motor)

        self.front_right_motor = ctre.WPI_VictorSPX(constants["frontRightPort"])
        self.rear_right_motor = ctre.WPI_TalonSRX(constants["rearRightPort"])
        self.rear_right_motor.setInverted(True)
        self.front_right_motor.setInverted(True)
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
        self.rear_right_motor.configSelectedFeedbackSensor(
            ctre.FeedbackDevice.QuadEncoder, 0, 0)

    def autonomousInit(self):
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        path = 1
        if path == 1:
            if self.timer.get() < 2:
                self.drive.arcadeDrive(0.5, 0)
            elif self.timer.get() < 2.5:
                self.drive.arcadeDrive(0, 0.5)
            elif self.timer.get() < 3.5:
                self.drive.arcadeDrive(0.5, 0)
            elif self.timer.get() < 5:
                # where the ball motors run
                self.drive.arcadeDrive(0,0)

            elif self.timer.get() < 6:
                self.drive.arcadeDrive(-0.5, 0)
            elif self.timer.get() < 6.5:
                self.drive.arcadeDrive(0, 0.75)
            elif self.timer.get() < 7.5:
                self.drive.arcadeDrive(0.75, 0)
                # Run the ball catching motors
            elif self.timer.get() < 8:
                self.drive.arcadeDrive(0, 0.75)
            elif self.timer.get() < 9:
                self.drive.arcadeDrive(0.75, 0)
            elif self.timer.get() < 9.5:
                self.drive.arcadeDrive(0, 0.5)
            elif self.timer.get() < 10.5:
                self.drive.arcadeDrive(0.5, 0)
            elif self.timer.get() < 12:
                # Run more robot ball catching motors, but this time, deposit the ball
                self.drive.arcadeDrive(0,0)
            elif self.timer.get() < 15:
                self.drive.arcadeDrive(-0.5, 0)
            else:
                self.drive.arcadeDrive(0,0)

        if path == 2:
            self.pGain = self.sd.getValue("PGain", 0.032)
            # self.dist = self.sd.getValue("Drive Dist", 5) * self.left_tpf
            self.error = self.dist - self.front_left_motor.getSelectedSensorPosition()
            self.kP = self.sd.getValue("kP", 0.05)
            self.isBPressed = self.controller.getBButton()

            turningValue = (self.angleSetpoint - self.gyro.getYaw()) * self.pGain
            # speed = self.controller.getY(self.controller.Hand.kLeftHand)
            speed = self.error * self.kP
            self.sd.putValue("Speed", speed)
            self.sd.putValue("Left Encoder Value", self.front_left_motor.getSelectedSensorPosition())
            if self.isBPressed and abs(self.front_left_motor.getSelectedSensorPosition()) < abs(self.dist):
                self.drive.arcadeDrive(speed, turningValue)

            gyro_reset()
            self.dist = self.sd.getValue("Drive Dist", 2) * self.left_tpf
            self.drive.arcadeDrive(1, 0)
            gyro_reset()
            self.dist = self.sd.getValue("Drive Dist", 1) * self.left_tpf
            # Run those ball depositing motors
            gyro_reset()
            self.dist = self.sd.getValue("Drive Dist", -1) * self.left_tpf
            for i in range(5):
                self.drive.arcadeDrive(1, 0)
            gyro_reset()
            self.dist = self.sd.getValue("Drive Dist", 5) * self.left_tpf
            # pick up another ball
            for i in range(7):
                self.drive.arcadeDrive(1, 0)  # turn 180 degrees
            gyro_reset()
            self.dist = self.sd.getValue("Drive Dist", 5) * self.left_tpf
            self.drive.arcadeDrive(1, 0)
            gyro_reset()
            self.dist = self.sd.getValue("Drive Dist", 1) * self.left_tpf
            # deposit the ball
            gyro_reset()
            self.dist = self.sd.getValue("Drive Dist", -5) * self.left_tpf
            gyro_reset()

        print("Time: ", self.timer.get())

    def gyro_reset(self):
        self.gyro.reset()
        self.front_left_motor.setSelectedSensorPosition(0, 0, 10)

    def teleopInit(self):
        print("Starting teleop...")

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
        self.drive.arcadeDrive(
            self.controller.getX(self.controller.Hand.kLeftHand),
            self.controller.getY(self.controller.Hand.kLeftHand),
            True
        )


if __name__ == "__main__":
    wpilib.run(MyRobot)
