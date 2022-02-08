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

        self.front_left_motor.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)
        self.rear_right_motor.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)
        self.controller = wpilib.XboxController(0)
        self.timer = wpilib.Timer()
        self.sd = NetworkTables.getTable("SmartDashboard")
        self.gyro = navx.AHRS.create_i2c(wpilib.I2C.Port.kMXP)
        self.left_tpf = -924

    def teleopInit(self):
        """
        Runs at the beginning of the teleop period
        """
        self.gyro.reset()
        self.front_left_motor.setSelectedSensorPosition(0, 0, 10)
        self.rear_right_motor.setSelectedSensorPosition(0, 0, 10)
        # self.gyro.setSensitivity(
            # self.voltsPerDegreePerSecond
        # )  # calibrates gyro values to equal degrees

    def teleopPeriodic(self):
        """
        Sets the gyro sensitivity and drives the robot when the joystick is pushed. The
        motor speed is set from the joystick while the RobotDrive turning value is assigned
        from the error between the setpoint and the gyro angle.
        """
        self.isAPressed = self.controller.getAButton()
        self.isBPressed = self.controller.getBButton()
        self.isXPressed = self.controller.getXButton()
        self.isYPressed = self.controller.getYButton()
        self.dist = self.sd.getValue("Drive Dist", 5) * self.left_tpf
        # speed = self.controller.getY(self.controller.Hand.kLeftHand)
        self.sd.putValue("Left Encoder Value", self.front_left_motor.getSelectedSensorPosition())
        self.sd.putValue("Right Encoder Value", self.rear_right_motor.getSelectedSensorPosition())
        self.drive.arcadeDrive(self.controller.getRightY(), self.controller.getLeftY())
        if self.isBPressed:
            self.sd.putValue("dist", self.dist)
            self.drive_straight(self.dist, 0)
        elif self.isAPressed:
            self.drive_straight(0, 90)
        elif self.isYPressed:
            self.gyro.reset()
            self.front_left_motor.setSelectedSensorPosition(0, 0, 10)
            self.rear_right_motor.setSelectedSensorPosition(0, 0, 10)

    def drive_straight(self, dist, angle):
        self.angleSetpoint = angle
        self.pGain = self.sd.getValue("PGain", 0.032)
        self.error = dist - self.front_left_motor.getSelectedSensorPosition()
        self.kP = self.sd.getValue("kP", 0.05)
        # self.kI = self.sd.getValue("kI", 0.05)
        turningValue = (self.angleSetpoint - self.gyro.getYaw()) * self.pGain
        if turningValue > 1:
            turningValue = 1
        if turningValue < -1:
            turningValue = -1
        speed = self.error * self.kP
        if speed > 0.75:
            speed = 0.75
        if speed < -0.75:
            speed = -0.75
        if abs(self.front_left_motor.getSelectedSensorPosition()) < abs(self.dist):
            self.drive.arcadeDrive(speed, turningValue)
        self.sd.putValue("Gyro Yaw", self.gyro.getYaw())
        self.sd.putValue("Turning Value", turningValue)
        self.sd.putValue("PGain", self.pGain)
        self.sd.putValue("Straight", self.isBPressed)
        self.sd.putValue("error", self.error)
        self.sd.putValue("Speed", speed)


if __name__ == "__main__":
    wpilib.run(MyRobot)
