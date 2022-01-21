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

    def get_side_distance(self, side):
        if side == "left":
            return -1 * ((self.front_left_motor.getSelectedSensorPosition() - self.left_enc_init_val) * 1 / self.left_tick_per_foot)
        if side == "right":
            return (self.rear_right_motor.getSelectedSensorPosition() - self.right_enc_init_val) * 1 / self.right_tick_per_foot
    
    def teleopInit(self):
        #self.myRobot.setSafetyEnabled(True)
        self.left_enc_init_val = self.front_left_motor.getSelectedSensorPosition()
        self.right_enc_init_val = self.rear_right_motor.getSelectedSensorPosition()
        self.going_to_goal = False
        self.sd.putValue("kP", 0.05)

    def teleopPeriodic(self):
        # self.drive.arcadeDrive(
        #     self.controller.getY(self.controller.Hand.kLeftHand),
        #     self.controller.getY(self.controller.Hand.kRightHand))
        # print("Left Enc Value: ", self.front_left_motor.getSelectedSensorPosition())
        # print("Right Enc Value: ", self.rear_right_motor.getSelectedSensorPosition())
        self.sd.putValue("Left Enc Value", self.front_left_motor.getSelectedSensorPosition() - self.left_enc_init_val)
        self.sd.putValue("Right Enc Value", self.rear_right_motor.getSelectedSensorPosition() - self.right_enc_init_val)
        # if self.controller.getAButton() and not self.going_to_goal:
        #     self.cur_left_enc = self.front_left_motor.getSelectedSensorPosition()
        #     self.goal_dist = self.cur_left_enc + self.left_tick_per_foot
        #     self.going_to_goal = True
        # if self.controller.getBButton() and not self.going_to_goal:
        #     self.cur_left_enc = self.front_left_motor.getSelectedSensorPosition()
        #     self.goal_dist = self.cur_left_enc + 2 * self.left_tick_per_foot
        #     self.going_to_goal = True
        # if self.controller.getXButton() and not self.going_to_goal:
        #     self.cur_left_enc = self.front_left_motor.getSelectedSensorPosition()
        #     self.goal_dist = self.cur_left_enc - 2 * self.left_tick_per_foot
        #     self.going_to_goal = True
        # if self.controller.getYButton() and not self.going_to_goal:
        #     self.cur_left_enc = self.front_left_motor.getSelectedSensorPosition()
        #     self.goal_dist = self.cur_left_enc - self.left_tick_per_foot
        #     self.going_to_goal = True
        # if self.going_to_goal:
        #     self.cur_left_enc = self.front_left_motor.getSelectedSensorPosition()
        #     if abs(self.cur_left_enc - self.goal_dist) < 100:
        #         self.drive.arcadeDrive(
        #             0,
        #             0
        #         )
        #         self.going_to_goal = False
        #     elif self.cur_left_enc > self.goal_dist:
        #         self.drive.arcadeDrive(
        #             -0.5,
        #             0
        #         )
        #     elif self.cur_left_enc < self.goal_dist:
        #         self.drive.arcadeDrive(
        #             0.5,
        #             0
        #         )
        kP = self.sd.getValue("kP",.05)
        error = self.get_side_distance("left") - self.get_side_distance("right")
        print(f"error{error}")
        self.sd.putValue("rightdistance",self.get_side_distance("right"))
        self.sd.putValue("leftdistance",self.get_side_distance("left"))
        print(f"left: {self.get_side_distance('left')}, right: {self.get_side_distance('right')}")
        self.drive.tankDrive(.4 - kP * error, .4 + kP * error);



if __name__ == "__main__":
    wpilib.run(MyRobot)
