from locale import normalize
import wpilib
from wpilib.drive import DifferentialDrive
import ctre
from constants import constants
from networktables import NetworkTables
import navx



class MyRobot(wpilib.TimedRobot):
    """This is a demo program showing how to use Gyro control with the
    DifferentialDrive class."""

    def robotInit(self):
        """Robot initialization function"""
        # smart dashboard
        self.sd = NetworkTables.getTable("SmartDashboard")
        # gyro calibration constant, may need to be adjusted
        # gyro value of 360 is set to correspond to one full revolution

        # self.voltsPerDegreePerSecond = 0.0128

        self.front_left_motor = ctre.WPI_TalonSRX(constants["frontLeftPort"])
        self.rear_left_motor = ctre.WPI_VictorSPX(constants["rearLeftPort"])
        self.left = wpilib.SpeedControllerGroup(
            self.front_left_motor, self.rear_left_motor)

        self.rear_right_motor = ctre.WPI_TalonSRX(constants["rearRightPort"])
        self.front_right_motor = ctre.WPI_VictorSPX(constants["frontRightPort"])
        self.rear_right_motor.setInverted(True)
        self.front_right_motor.setInverted(True)
        self.right = wpilib.SpeedControllerGroup(
            self.front_right_motor, self.rear_right_motor)

        self.drive = wpilib.drive.DifferentialDrive(
            self.right,
            self.left
        )

        self.front_left_motor.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)
        self.controller = wpilib.XboxController(0)
        self.timer = wpilib.Timer()
        self.sd = NetworkTables.getTable("SmartDashboard")
        self.gyro = navx.AHRS.create_i2c(wpilib.I2C.Port.kMXP)
        #change to negative if necessary
        self.tpf = -924
        self.max_speed = 0.4

    def teleopInit(self):
        """
        Runs at the beginning of the teleop period
        """
        self.gyro.reset()
        self.front_left_motor.setSelectedSensorPosition(0, 0, 10)
        # self.gyro.setSensitivity(
        # self.voltsPerDegreePerSecond
        # )  # calibrates gyro values to equal degrees
        self.pGain = self.sd.getValue("PGain", 0.032)
        # self.kP = self.sd.getValue("kP", 0.03)
        self.kP = 0.03
        self.sd.putValue("kP",self.kP)
        self.steps = [{
            "Step_Type": "Straight", #Step_Type says whether we will be driving forward, or turning in this step
            "Distance": 5, # How far we need to move forward in this step
            "Angle": 0, # What angle we need to turn to in this step
            "Threshold_Value": .1, # To complete the step, we need to be within the threshold feet of the target distance
            "Threshold_Time": 1, # Once we are in the threshold for this amount of time, we move to the next step
        },{ #top left turn
            "Step_Type": "Turn",
            "Distance": 0,
            "Angle": 90,
            "Threshold_Value": 5,
            "Threshold_Time": 1, 
        },{
            "Step_Type": "Straight",
            "Distance": 5,
            "Angle": 90,
            "Threshold_Value": .1,
            "Threshold_Time": 1,
        },{# top right turn
            "Step_Type": "Turn",
            "Distance": 0,
            "Angle": 180,
            "Threshold_Value": 5,
            "Threshold_Time": 1, 
        },{
            "Step_Type": "Straight",
            "Distance": 5,
            "Angle": 180,
            "Threshold_Value": .1,
            "Threshold_Time": 1,
        },{#bottom right turn
            "Step_Type": "Turn",
            "Distance": 0,
            "Angle": -90,
            "Threshold_Value": 5,
            "Threshold_Time": 1, 
        },{
            "Step_Type": "Straight",
            "Distance": 5,
            "Angle": -90,
            "Threshold_Value": .1,
            "Threshold_Time": 1,
        },{#bottome left turn back to orientation at the start
            "Step_Type": "Turn",
            "Distance": 0,
            "Angle": 0,
            "Threshold_Value": 5,
            "Threshold_Time": 1, 
        },
        ]
        self.current_step_index = 0
        self.current_step = self.steps[self.current_step_index]
        self.in_threshold_time = 0
        self.in_threshold_start_time = 0
        self.in_threshold = False
        self.steps_complete = False
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        self.sd.putValue("Left Encoder Value", self.front_left_motor.getSelectedSensorPosition())

    def teleopPeriodic(self):
        self.isAPressed = self.controller.getAButton()
        self.isBPressed = self.controller.getBButton()
        self.isXPressed = self.controller.getXButton()
        self.isYPressed = self.controller.getYButton()
        # self.drive.arcadeDrive(.5,0)
        # return
        if self.isXPressed: #Use X to cancel program
            self.steps_complete = True
            return
        if self.steps_complete:
            return

        self.goal_tick_dist = self.current_step['Distance'] * self.tpf
        self.goal_angle = self.current_step['Angle']

        if self.in_threshold:
            self.in_threshold_time = self.timer.get() - self.in_threshold_start_time
        else:
            self.in_threshold_time = 0
        #Determine if in threshold
        if self.current_step['Step_Type'] == "Straight":
            current_in_threshold = -1 * abs(self.goal_tick_dist - self.front_left_motor.getSelectedSensorPosition()) / self.tpf < self.current_step[
                'Threshold_Value']
        elif self.current_step['Step_Type'] == "Turn":
            current_in_threshold = self.goal_angle - self.gyro.getYaw() < self.current_step['Threshold_Value']
        self.sd.putValue("Current_in_threshold",current_in_threshold)
        if current_in_threshold:
            if self.in_threshold == False:
                #Just entered the threshold
                self.in_threshold = True
                self.in_threshold_start_time = self.timer.get()
            if self.in_threshold_time > self.current_step['Threshold_Time']:
                #Been in threshold for a good amount of time, move to next step
                self.current_step_index += 1
                if self.current_step_index == len(self.steps):
                    self.steps_complete = True
                    return
                else:
                    self.current_step = self.steps[self.current_step_index]
                self.front_left_motor.setSelectedSensorPosition(0, 0, 10)
                self.in_threshold = False
        else:
            self.in_threshold = False

        #Setting Speed
        if self.current_step['Step_Type'] == "Straight":
            self.distance_error = self.goal_tick_dist - self.front_left_motor.getSelectedSensorPosition()
            self.speed = self.distance_error * self.kP * -1
            if self.speed > self.max_speed:
                self.speed = self.max_speed
            if self.speed < self.max_speed * -1:
                self.speed = -1 * self.max_speed
        elif self.current_step['Step_Type'] == "Turn":
            self.speed = 0 # we don't want to move forward when turning (turn in place)
            self.goal_tick_dist = None
            self.distance_error = None

        #Setting Angle - this drives helps drive
        normalizeYaw = self.gyro.getYaw()
        turningValue = (self.goal_angle - normalizeYaw) * self.pGain * -1
        if turningValue < -.5:
            turningValue = -.5
        if turningValue > .5:
            turningValue = .5
        #move the robot
        self.drive.arcadeDrive(self.speed, turningValue)

        #print debug values

        # self.sd.putValue("debug value for inthreshold",abs(self.goal_tick_dist - self.front_left_motor.getSelectedSensorPosition()) / self.tpf)
        self.sd.putValue("IsBPressed", self.isBPressed)
        self.sd.putValue("current_step_index", self.current_step_index)
        self.sd.putValue("Step Type", self.current_step['Step_Type'])

        self.sd.putValue("Current Time", self.timer.get())
        self.sd.putValue("in_threshold_start_time", self.in_threshold_start_time)
        self.sd.putValue("in_threshold", self.in_threshold)
        self.sd.putValue("in_threshold_time", self.in_threshold_time)
        self.sd.putValue("Steps Complete?", self.steps_complete)

        self.sd.putValue("Goal Angle", self.goal_angle)
        self.sd.putValue("Gyro Yaw", self.gyro.getYaw())
        self.sd.putValue("Turning Value", turningValue)
        self.sd.putValue("PGain", self.pGain)

        self.sd.putValue("goal_tick_dist", self.goal_tick_dist)
        self.sd.putValue("Left Encoder Value", self.front_left_motor.getSelectedSensorPosition())
        self.sd.putValue("Distance Error", self.distance_error)
        self.sd.putValue("Speed", self.speed)


if __name__ == "__main__":
    wpilib.run(MyRobot)
