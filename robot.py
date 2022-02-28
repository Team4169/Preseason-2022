from locale import normalize
import wpilib
from wpilib.drive import DifferentialDrive
import ctre
from constants import constants
from networktables import NetworkTables
import navx
import wpimath.controller

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
        self.gyro = navx.AHRS(wpilib.SerialPort.Port.kUSB1)

        self.tpf = -924
        self.max_speed = 0.5
    def autonomousInit(self):
        """
        Runs at the beginning of the teleop period
        """

        self.gyro.reset()
        self.front_left_motor.setSelectedSensorPosition(0, 0, 10)
        from autos.LucAutoStart import auto
        self.steps = auto
        self.current_step_index = 0
        self.current_step = self.steps[self.current_step_index]
        self.in_threshold_time = 0
        self.in_threshold_start_time = 0
        self.in_threshold = False
        self.steps_complete = False
        # Create PID Controller for Turning
        self.TurnkP = self.sd.putValue("TurnkP", 0.025)
        self.TurnkP = self.sd.getValue("TurnkP", 0.025)
        self.TurnkI = self.sd.putValue("TurnkI",0.03)
        self.TurnkI = self.sd.getValue("TurnkI",0.03)
        self.TurnkD = self.sd.putValue("TurnkD",0.015)
        self.TurnkD = self.sd.getValue("TurnkD",0.015)
        turnController = wpimath.controller.PIDController(
            self.TurnkP,
            self.TurnkI,
            self.TurnkD,
        )
        turnController.enableContinuousInput(-180.0, 180.0)
        turnController.setTolerance(2.0)
        self.turnController = turnController

        # Create PID Controller for Drive
        self.DrivekP = self.sd.putValue("DrivekP", 0.03)
        self.DrivekP = self.sd.getValue("DrivekP", 0.03)
        self.DrivekI = self.sd.putValue("DrivekI",0.02)
        self.DrivekI = self.sd.getValue("DrivekI",0.02)
        self.DrivekD = self.sd.putValue("DrivekD",0)
        self.DrivekD = self.sd.getValue("DrivekD",0)

        driveController = wpimath.controller.PIDController(
            self.DrivekP,
            self.DrivekI,
            self.DrivekD,
        )
        driveController.setTolerance(-0.1 * self.tpf)
        self.driveController = driveController

        self.timer.reset()
        self.timer.start()

    def teleopPeriodic(self):
        self.sd.putValue("Left Encoder Value", self.front_left_motor.getSelectedSensorPosition())

    def autonomousPeriodic(self):
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
        self.driveController.setSetpoint(self.goal_tick_dist)

        self.goal_angle = self.current_step['Angle']
        self.turnController.setSetpoint(self.goal_angle)

        if self.in_threshold:
            self.in_threshold_time = self.timer.get() - self.in_threshold_start_time
        else:
            self.in_threshold_time = 0

        #Setting Speed
        if self.current_step['Step_Type'] == "Straight":
            self.speed = -1 * self.driveController.calculate(self.front_left_motor.getSelectedSensorPosition(), self.goal_tick_dist)
            if self.speed > self.max_speed:
                self.speed = self.max_speed
            if self.speed < self.max_speed * -1:
                self.speed = -1 * self.max_speed
        elif self.current_step['Step_Type'] == "Turn":
            self.speed = 0 # we don't want to move forward when turning (turn in place)
            self.goal_tick_dist = None

        #Setting Angle - this drives helps drive straight and turn
        turningValue = -1 * self.turnController.calculate(self.gyro.getYaw(), self.goal_angle)
        if turningValue < -.5:
            turningValue = -.5
        if turningValue > .5:
            turningValue = .5

        #Determine if in threshold
        if self.current_step['Step_Type'] == "Straight":
            current_in_threshold = self.driveController.atSetpoint()
        elif self.current_step['Step_Type'] == "Turn":
            current_in_threshold = self.turnController.atSetpoint()
        self.sd.putValue("Current_in_threshold", current_in_threshold)
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
                if self.current_step["Step_Type"] == "Straight":
                    self.sd.putValue("drive tolerance", abs(self.current_step["Threshold_Value"] * self.tpf))
                    self.driveController.setTolerance(abs(self.current_step["Threshold_Value"] * self.tpf))
                elif self.current_step["Step_Type"] == "Turn":
                    self.turnController.setTolerance(self.current_step["Threshold_Value"])
                self.in_threshold = False
        else:
            self.in_threshold = False

        #move the robot
        self.drive.arcadeDrive(self.speed, turningValue)

        #print debug values

        # self.sd.putValue("debug value for inthreshold",abs(self.goal_tick_dist - self.front_left_motor.getSelectedSensorPosition()) / self.tpf)
        self.sd.putValue("at setpoint", self.driveController.atSetpoint())
        self.sd.putValue("setpoint", self.driveController.getSetpoint())
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
        self.sd.putValue("TurnkP", self.TurnkP)

        self.sd.putValue("goal_tick_dist", self.goal_tick_dist)
        self.sd.putValue("Left Encoder Value", self.front_left_motor.getSelectedSensorPosition())
        self.sd.putValue("Speed", self.speed)


if __name__ == "__main__":
    wpilib.run(MyRobot)
