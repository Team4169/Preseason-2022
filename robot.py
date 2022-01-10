#Test Jan 10th
import wpilib
import wpilib.drive
import ctre
from constants import constants
from networktables import NetworkTables
import navx

class MyRobot(wpilib.TimedRobot):


    def robotInit(self):
        """Robot initialization function"""

        # object that handles basic drive operations
     	  self.front_left_motor = ctre.WPI_TalonSRX(constants["frontLeftPort"])
        self.rear_left_motor = ctre.WPI_VictorSPX(constants["rearLeftPort"])
        self.left = wpilib.SpeedControllerGroup(
            self.front_left_motor, self.rear_left_motor)

        self.front_right_motor = ctre.WPI_TalonSRX(constants["frontRightPort"])
        self.rear_right_motor = ctre.WPI_VictorSPX(constants["rearRightPort"])
        self.right = wpilib.SpeedControllerGroup(
            self.front_right_motor, self.rear_right_motor)

	  self.drive = wpilib.drive.DifferentialDrive(
            self.right,
            self.left
        )

        # Xbox controller
        self.controller = wpilib.XboxController(0)

    def teleopInit(self):
        self.myRobot.setSafetyEnabled(True)

    def teleopPeriodic(self):
	  self.myRobot.tankDrive(
	      self.controller.getY(self.controller.Hand.kLeftHand) * -1,
            self.controller.getY(self.controller.Hand.kRightHand) * -1)
	  )
           

if __name__ == "__main__":
    wpilib.run(MyRobot)
