#Test Jan 10th
import wpilib
import wpilib.drive
import ctre
from constants import constants
from networktables import NetworkTables
#import navx

class MyRobot(wpilib.TimedRobot):
	# back = False
	# time=0

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
		self.speed = 0
		self.back = False
		self.time = 0

		# Xbox controller
		self.controller = wpilib.XboxController(0)
		self.timer=wpilib.Timer()

	def teleopInit(self):
		#self.drive.setSafetyEnabled(True)
		self.timer.reset()
		self.timer.start()

	def teleopPeriodic(self):
		# global speed
		# global back
		# global time
		self.drive.tankDrive(
			self.controller.getY(self.controller.Hand.kLeftHand) * -1,
			self.controller.getY(self.controller.Hand.kRightHand) * -1
		)
		self.speed=abs(self.speed)
		#Gradual speed decrease
		if self.speed >= 0.05 and self.timer.get()>=self.time+0.025:
			self.speed=self.speed-0.05

		#Pull: Stop
		if self.controller.getYButton():
			self.speed=0
		#Bop-It: Increase Speed
		if self.controller.getXButtonPressed():
			if self.speed<=0.9:
				self.speed+=0.1
		#Spin: Reverse Direction
		if self.controller.getAButtonPressed():
			self.back=not self.back
		if self.back:
			self.speed= self.speed*-1
		#Twist: Left
		if self.controller.getBButton():
			self.right.set(-1*self.speed)
			self.left.set(self.speed)
		#Flick: Right
		elif self.controller.getBumper():
			self.left.set(-1*self.speed)
			self.right.set(self.speed)
		#Else: Streight
		else:
			self.right.set(self.speed)
			self.left.set(self.speed)
		time=self.timer.get()



if __name__ == "__main__":
	wpilib.run(MyRobot)
