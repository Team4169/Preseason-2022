import wpilib
import wpilib.drive
import ctre
import deadzone
from constants import constants
from netowrktables import NetworkTables
import navx
import Encoder


class MyRobot(wpilib.TimedRobot):
    kSlotIdx = 0
    kPIDLoopIdx = 0
    kTimeoutMs = 10
    def robotInit(self):
        self.front_left_motor = wpilib.Talon(constants["frontLeftPort"])
        self.rear_left_motor = wpilib.Talon(constants["rearLeftPort"])
        self.left = wpilib.SpeedControllerGroup(self.front_left_motor, self.rear_left_motor)

        self.front_right_motor = wpilib.Talon(constants["frontRightPort"])
        self.rear_right_motor = wpilib.Talon(constants["rearRightPort"])
        self.right = wpilib.SpeedControllerGroup(self.front_right_motor, self.rear_right_motor)
        '''
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
        # '''
        self.controller = wpilib.XboxController(0)
        self.test_motor = ctre.WPI_TalonSRX(constants["testMotorPort"])
        self.timer = wpilib.Timer()

        self.sd = NetworkTables.getTable("SmartDashboard")
        self.gyro = navx.AHRS.create_i2c()

        self.front_left_motor.configSelectedFeedbackSensor(
            WPI_TalonSRX.FeedbackDevice.CTRE_MagEncoder_Relative,
            self.kPIDLoopIdx,
            self.kTimeoutMs
        )
        self.front_left_motor.setSensorPhase(False)
        self.front_left_motor.configNominalOutputForward(0, self.kTimeoutMs)
        self.front_left_motor.configNominalOutputReverse(0, self.kTimeoutMs)
        self.front_left_motor.configPeakOutputForward(1, self.kTimeoutMs)
        self.front_left_motor.configPeakOutputReverse(-1, self.kTimeoutMs)
        self.front_left_motor.configAllowableClosedloopError(0, self.kPIDLoopIdx, self.kTimeoutMs)
        self.front_left_motor.selectProfileSlot(self.kSlotIdx, self.kTimeoutMs)
        self.front_left_motor.config_kF(0, 0, self.kTimeoutMs)
        self.front_left_motor.config_kP(0, 0.1, self.kTimeoutMs)
        self.front_left_motor.config_kI(0, 0, self.kTimeoutMs)
        self.front_left_motor.config_kD(0, 0, self.kTimeoutMs)
        self.front_left_motor.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)

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
        print("The gyro yaw value is: ", self.gyro.getYaw())
        # print("Encoder Value is: ", self.enc)
        self.sd.putValue("Gyro Yaw Value", self.gyro.getYaw())
        self.sd.putValue("Encoder Value", self.front_left_motor.getSelectedSensorPosition(self.kPIDLoopIdx))
        self.left_turn = self.controller.getTriggerAxis(self.controller.Hand.kLeftHand)
        self.right_turn = self.controller.getTriggerAxis(self.controller.Hand.kRightHand)
        self.turn = self.right_turn - self.left_turn
        print("The turn value is: ", self.turn)
        self.drive.driveCartesian(
            self.controller.getX(self.controller.Hand.kLeftHand),
            self.controller.getY(self.controller.Hand.kLeftHand),
            self.controller.getY(self.controller.Hand.kRightHand), 0)
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
