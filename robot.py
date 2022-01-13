#Test Jan 10th
import wpilib
import wpilib.drive
import ctre
from constants import constants
from networktables import NetworkTables
import navx

class MyRobot(wpilib.TimedRobot):
    speed = 0
    back = False

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
        self.timer.reset()
        self.timer.start()
        timer=0

    def teleopPeriodic(self):
      global speed
      global back
	    self.myRobot.tankDrive(
	      self.controller.getY(self.controller.Hand.kLeftHand) * -1,
            self.controller.getY(self.controller.Hand.kRightHand) * -1)
	    )
      speed=abs(speed)
      #Gradual speed decrease
      if speed >= 0.05 and self.timer.get()>=timer+0.025:
        speed=speed-0.05

      #Pull: Stop
      if self.controller.getYButton(): 
        speed=0
      #Bop-It: Increase Speed
      if self.controller.getXButtonPressed():
        if speed<=0.9:
          speed+=0.1
      #Spin: Reverse Direction
      if self.conroller.getAButtonPressed(): 
        back=!back
      if back:
        speed=speed*-1
      #Twist: Left
      if self.controller.getBButton():  
        self.right.set(-1*speed)
        self.left.set(speed)
      #Flick: Right
      elif self.controller.getBumper(): 
        self.left.set(-1*speed)
        self.right.set(speed)
      #Else: Streight
      else:
        self.right.set(speed)
        self.left.set(speed)
      timer=self.time.get()
      
      
      
if __name__ == "__main__":
    wpilib.run(MyRobot)
