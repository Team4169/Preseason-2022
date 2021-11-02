import wpilib
import wpilib.drive
import ctre
import deadzone
from constants import constants
from wpilib._wpilib import Encoder
import navx


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.front_left_motor = ctre.WPI_TalonSRX(constants["frontLeftPort"])
        self.rear_left_motor = ctre.WPI_TalonSRX(constants["rearLeftPort"])
        self.front_left_motor.setInverted(True)
        self.rear_left_motor.setInverted(True)
        self.left = wpilib.SpeedControllerGroup(self.front_left_motor, self.rear_left_motor)
        self.front_right_motor = ctre.WPI_TalonSRX(constants["frontRightPort"])
        self.rear_right_motor = ctre.WPI_TalonSRX(constants["rearRightPort"])
        self.front_right_motor.setInverted(True)
        self.rear_right_motor.setInverted(True)
        self.right = wpilib.SpeedControllerGroup(self.front_right_motor, self.rear_right_motor)
        self.drive = wpilib.drive.MecanumDrive(
            self.front_left_motor,
            self.rear_left_motor,
            self.front_right_motor,
            self.rear_right_motor
        )
        '''
        self.drive = wpilib.drive.DifferentialDrive(
            self.left,
            self.right
        )
        '''
        self.controller = wpilib.XboxController(0)
        self.test_motor = ctre.WPI_TalonSRX(constants["testMotorPort"])
        self.timer = wpilib.Timer()
        self.encoder = wpilib.Encoder(self.front_left_motor)
        self.gyro = navx.AHRS()

    def autonomousInit(self):
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        # driveCartesian(ySpeed: float, xSpeed: float, zRotation: float, gyroAngle: float =0.0)
        if self.timer.get() < 2:
            self.drive.driveCartesian(0.25, 0.0, 0.0)
        elif self.timer.get() < 4:
            self.drive.driveCartesian(0.0, 0.25, 0.0)
        elif self.timer.get() < 8:
            self.drive.driveCartesian(0.0, 0.0, 0.25)
        else:
            self.drive.driveCartesian(0.0, 0.0, 0.0)

    def teleopPeriodic(self):
        print("The drive X value is: ", self.controller.getX(self.controller.Hand.kLeftHand))
        print("The drive Y value is: ", self.controller.getY(self.controller.Hand.kLeftHand))
        print("The gyro yaw value is: ", self.gyro.getAngle())
        print("Encoder Value is: ", self.encoder)
        self.left_turn = self.controller.getTriggerAxis(self.controller.Hand.kLeftHand)
        self.right_turn = self.controller.getTriggerAxis(self.controller.Hand.kRightHand)
        self.turn = self.left_turn - self.right_turn
        self.drive.driveCartesian(
            self.controller.getX(self.controller.Hand.kLeftHand),
            self.controller.getY(self.controller.Hand.kLeftHand),
            self.turn, 0)
        isApressed = self.controller.getAButton()
        # print(isApressed)
        isBpressed = self.controller.getBButton()
        # print(isBpressed)
        if isApressed:
            self.test_motor.set(0.5)
        elif isBpressed:
            self.test_motor.set(-0.5)
        else:
            self.test_motor.set(0)


if __name__ == "__main__":
    wpilib.run(MyRobot)
