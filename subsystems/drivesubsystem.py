import commands2
import wpilib
import wpilib.drive
import ctre
import constants
from networktables import NetworkTables
import wpimath.controller
import navx

class DriveSubsystem(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        self.left1 = ctre.WPI_TalonSRX(constants.kLeftMotor1Port)
        self.left2 = ctre.WPI_TalonSRX(constants.kLeftMotor2Port)
        self.right1 = ctre.WPI_TalonSRX(constants.kRightMotor1Port)
        self.right2 = ctre.WPI_TalonSRX(constants.kRightMotor2Port)

        self.tpf = -924
        self.maxDriveSpeed = 0.6
        self.maxTurnSpeed = 0.5

        # smartdashboard
        self.sd = NetworkTables.getTable("SmartDashboard")

        # Create PID Controller for Turning
        self.TurnkP = self.sd.getValue("TurnkP", 0.032)
        self.TurnkI = self.sd.getValue("TurnkI", 0)
        self.TurnkD = self.sd.getValue("TurnkD", 0)
        self.turnController = wpimath.controller.PIDController(self.TurnkP, self.TurnkI, self.TurnkD)
        self.turnController.enableContinuousInput(-180.0, 180.0)
        self.turnController.setTolerance(10.0)

        # Create PID Controller for Drive
        self.DrivekP = self.sd.getValue("DrivekP", 0.02)
        self.DrivekI = self.sd.getValue("DrivekI", 0.02)
        self.DrivekD = self.sd.getValue("DrivekD", 0.0005)
        self.driveController = wpimath.controller.PIDController(self.DrivekP, self.DrivekI, self.DrivekD)
        self.driveController.setTolerance(-0.1 * self.tpf)

        # gyro
        self.gyro = navx.AHRS(wpilib.SerialPort.Port.kUSB1)

        # The robot's drive
        self.right1.setInverted(True)
        self.right2.setInverted(True)
        self.drive = wpilib.drive.DifferentialDrive(
            wpilib.SpeedControllerGroup(self.left1, self.left2),
            wpilib.SpeedControllerGroup(self.right1, self.right2),
        )

        # The left-side drive encoder
        # NOTE FROM NOAH - I commented the encoders out, will use the talon interface to get encoders
        # self.leftEncoder = wpilib.Encoder(
        #     *constants.kLeftEncoderPorts,
        #     reverseDirection=constants.kLeftEncoderReversed
        # )
        #
        # # The right-side drive encoder
        # self.rightEncoder = wpilib.Encoder(
        #     *constants.kRightEncoderPorts,
        #     reverseDirection=constants.kRightEncoderReversed
        # )
        self.left1.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)
        self.right2.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)

        # Sets the distance per pulse for the encoders
        # NOTE FROM NOAH - Expirement with these two following lines later, for now commenting them out
        # self.leftEncoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)
        # self.rightEncoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)

    def arcadeDrive(self, fwd: float, rot: float) -> None:
        """
        Drives the robot using arcade controls.

        :param fwd: the commanded forward movement
        :param rot: the commanded rotation
        """
        self.drive.arcadeDrive(fwd, rot)

    def resetEncoders(self) -> None:
        self.left1.setSelectedSensorPosition(0, 0, 10)
        self.right2.setSelectedSensorPosition(0, 0, 10)
        """Resets the drive encoders to currently read a position of 0."""

    def getAverageEncoderDistance(self) -> float:
        """Gets the average distance of the TWO encoders."""
        self.sd.putValue("Left Encoder Value", self.left1.getSelectedSensorPosition())
        self.sd.putValue("Right Encoder Value", self.right2.getSelectedSensorPosition())
        return (self.left1.getSelectedSensorPosition() + self.right2.getSelectedSensorPosition()) / 2.0 * 12 / 924

    def getAverageEncoderTicks(self) -> float:
        """Gets the average distance of the TWO encoders."""
        self.sd.putValue("Left Encoder Value", self.left1.getSelectedSensorPosition())
        self.sd.putValue("Right Encoder Value", self.right2.getSelectedSensorPosition())
        return (self.left1.getSelectedSensorPosition() + self.right2.getSelectedSensorPosition()) / -2.0

    def setMaxOutput(self, maxOutput: float):
        """
        Sets the max output of the drive. Useful for scaling the
        drive to drive more slowly.
        """
        self.drive.setMaxOutput(maxOutput)

    def validateDriveSpeed(self, speed):
        if speed > self.maxDriveSpeed:
            return self.maxDriveSpeed
        if speed < -1 * self.maxDriveSpeed:
            return -1 * self.maxDriveSpeed
        return speed

    def validateTurnSpeed(self, turnSpeed):
        if turnSpeed > self.maxTurnSpeed:
            return self.maxTurnSpeed
        if turnSpeed < -1 * self.maxTurnSpeed:
            return -1 * self.maxTurnSpeed
        return turnSpeed
