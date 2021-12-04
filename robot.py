import wpilib
import wpilib.drive
import ctre
from constants import constants
from networktables import NetworkTables
import navx

class MyRobot(wpilib.TimedRobot):
  
  def robotInit(self):
  	self.front_left_motor = ctre.WPI_TalonSRX(constants["frontLeftPort"])
  	self.rear_left_motor = ctre.WPI_TalonSRX(constants["rearLeftPort"])
  	self.rear_left_motor.setInverted(True)
  	self.left = wpilib.SpeedControllerGroup(self.front_left_motor, self.rear_left_motor)
    
  	self.front_right_motor = ctre.WPI_TalonSRX(constants["frontRightPort"])
  	self.rear_right_motor = ctre.WPI_TalonSRX(constants["rearRightPort"])
  	self.rear_right_motor.setInverted(True)
  	self.right = wpilib.SpeedControllerGroup(self.front_right_motor, self.rear_right_motor)
    
    self.drive = wpilib.drive.DifferentialDrive(
      self.right,
      self.left
    )
	self.controller = wpilib.XboxController(0)
	self.timer = wpilib.Timer()
	self.sd = NetworkTables.getTable("SmartDashboard")
	self.gyro = navx.AHRS.create_i2c()
	
def autnomousInit(self):
	self.timer.reset()
	self.timer.start()

def autonomousPeriodic(self):
	
def teleopInit(self):
	
def teleopPeriodic(self):
	print("The drive X value is: ", self.controller.getX(self.controller.Hand.kLeftHand))
	print("The drive Y value is: ", self.controller.getY(self.controller.Hand.kLeftHand))
	print("The gyro Yaw value is: ", self.gyro.getYaw())
	self.sd.putValue("Gyro Yaw", self.gyro.getYaw())
	self.drive.driveCartesian(
		self.controller.getX(self.controller.Hand.kLeftHand),
		self.controller.getY(self.controller.Hand.kLeftHand),
		self.controller.getY(self.controller.Hand.kRightHand), 0)
	isAPressed = self.controller.getAButton()
	isBPressed = self.controller.getBButton()
	isXPressed = self.controller.getXButton()
	isYPressed = self.controller.getYButton()

if __name__ == "__main__":
	wpilib.run(MyRobot)
