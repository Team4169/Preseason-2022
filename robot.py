#Test Jan 10th
import wpilib
import wpilib.drive
import ctre
from constants import constants
from networktables import NetworkTables

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """Robot initialization function"""

        # object that handles basic drive operations
        self.front_left_motor = ctre.WPI_TalonSRX(constants["frontLeftPort"])
        self.rear_left_motor = ctre.WPI_VictorSPX(constants["rearLeftPort"])
        self.left = wpilib.SpeedControllerGroup(
            self.front_left_motor, self.rear_left_motor)

        self.front_right_motor = ctre.WPI_VictorSPX(constants["frontRightPort"])
        self.rear_right_motor = ctre.WPI_TalonSRX(constants["rearRightPort"])
        self.right = wpilib.SpeedControllerGroup(
            self.front_right_motor, self.rear_right_motor)

        self.drive = wpilib.drive.DifferentialDrive(
            self.right,
            self.left
        )

        # Xbox controller
        self.controller = wpilib.XboxController(0)
        self.sd = NetworkTables.getTable("SmartDashboard")
        self.front_left_motor.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)
        self.rear_right_motor.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)
        self.left_tick_per_foot = 911
        self.right_tick_per_foot = 610
        self.gyro = navx.AHRS.create_i2c()

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        # self.drive.arcadeDrive(
        #     self.controller.getY(self.controller.Hand.kLeftHand),
        #     self.controller.getY(self.controller.Hand.kRightHand))
        kP = self.sd.getValue("kP")

        rotateToAngle = False
        setpoint = 0.0
        if self.controller.getAButton():
            self.gyro.reset()
        if self.controller.getBButton():
            setpoint = 0.0
            rotateToAngle = True
        elif self.stick.getXButton():
            setpoint = 90.0
            rotateToAngle = True

        if rotateToAngle:
            currentRotationRate = self.turnController.calculate(
                self.gyro.getYaw(), setpoint
            )
        else:
            self.turnController.reset()
            currentRotationRate = self.controller.getY(self.controller.Hand.kRightHand)

        self.drive.driveArcade(
            self.controller.getY(self.controller.Hand.kLeftHand),
            currentRotationRate
        )



if __name__ == "__main__":
    wpilib.run(MyRobot)
