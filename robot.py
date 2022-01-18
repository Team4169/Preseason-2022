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

    def teleopInit(self):
        #self.myRobot.setSafetyEnabled(True)
        self.left_enc_init_val = self.front_left_motor.getSelectedSensorPosition()
        self.right_enc_init_val = self.rear_right_motor.getSelectedSensorPosition()

    def teleopPeriodic(self):
        self.drive.tankDrive(
            self.controller.getY(self.controller.Hand.kLeftHand),
            self.controller.getY(self.controller.Hand.kLeftHand))
        # print("Left Enc Value: ", self.front_left_motor.getSelectedSensorPosition())
        # print("Right Enc Value: ", self.rear_right_motor.getSelectedSensorPosition())
        self.sd.putValue("Left Enc Value", self.front_left_motor.getSelectedSensorPosition() - self.left_enc_init_val)
        self.sd.putValue("Right Enc Value", self.rear_right_motor.getSelectedSensorPosition() - self.right_enc_init_val)


if __name__ == "__main__":
    wpilib.run(MyRobot)
