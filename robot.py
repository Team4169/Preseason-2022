#Test Jan 10th
import wpilib
import wpilib.drive
import ctre
from constants import constants

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """Robot initialization function"""

        # object that handles basic drive operations
        self.front_left_motor = ctre.WPI_TalonSRX(constants["frontLeftPort"])
        self.rear_left_motor = ctre.WPI_TalonSRX(constants["rearLeftPort"])
        self.left = wpilib.SpeedControllerGroup(
            self.front_left_motor, self.rear_left_motor)

        self.front_right_motor = ctre.WPI_TalonSRX(constants["frontRightPort"])
        self.rear_right_motor = ctre.WPI_TalonSRX(constants["rearRightPort"])
        self.right = wpilib.SpeedControllerGroup(
            self.front_right_motor, self.rear_right_motor)

        self.drive = wpilib.drive.DifferentialDrive(
            self.right,
            self.left
        )

        # Xbox controller
        self.controller = wpilib.XboxController(0)

    def teleopInit(self):
        #self.myRobot.setSafetyEnabled(True)
        pass

    def teleopPeriodic(self):
        # drive in "tank" mode (left stick to left motor; right stick to right motor)
        self.drive.tankDrive(
            self.controller.getLeftY(),
            self.controller.getLeftY() * -1)


if __name__ == "__main__":
    wpilib.run(MyRobot)
