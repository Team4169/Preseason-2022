#!/usr/bin/env python3

"""
 * Example demonstrating the motion magic control mode.
 * Tested with Logitech F710 USB Gamepad inserted into Driver Station.
 *
 * Be sure to select the correct feedback sensor using configSelectedFeedbackSensor() below.
 *
 * After deploying/debugging this to your RIO, first use the left Y-stick
 * to throttle the Talon manually.  This will confirm your hardware setup/sensors
 * and will allow you to take initial measurements.
 *
 * Be sure to confirm that when the Talon is driving forward (green) the
 * position sensor is moving in a positive direction.  If this is not the
 * cause, flip the boolean input to the setSensorPhase() call below.
 *
 * Once you've ensured your feedback device is in-phase with the motor,
 * and followed the walk-through in the Talon SRX Software Reference Manual,
 * use button1 to motion-magic servo to target position specified by the gamepad stick.
"""

from ctre import WPI_TalonSRX, WPI_VictorSPX, FeedbackDevice, StatusFrameEnhanced, ControlMode
import wpilib
from constants import constants

class Robot(wpilib.IterativeRobot):

    #: Which PID slot to pull gains from. Starting 2018, you can choose from
    #: 0,1,2 or 3. Only the first two (0,1) are visible in web-based
    #: configuration.
    kSlotIdx = 0

    #: Talon SRX/ Victor SPX will supported multiple (cascaded) PID loops. For
    #: now we just want the primary one.
    kPIDLoopIdx = 0

    #: set to zero to skip waiting for confirmation, set to nonzero to wait and
    #: report to DS if action fails.
    kTimeoutMs = 10

    def robotInit(self):
        self.left = WPI_TalonSRX(constants["frontLeftPort"])
        self.rear_left_motor = WPI_VictorSPX(constants["rearLeftPort"])
        self.rear_left_motor.follow(self.left)

        self.right = WPI_TalonSRX(constants["rearRightPort"])
        self.front_right_motor = WPI_VictorSPX(constants["frontRightPort"])
        self.front_right_motor.follow(self.right)

        self.controller = wpilib.XboxController(0)

        self.loops = 0
        self.timesInMotionMagic = 0

        # first choose the sensor
        self.left.configSelectedFeedbackSensor(
            FeedbackDevice.QuadEncoder, #Changed from the mag encoder used in example to QuadEncoder. Not sure if this will break the code.
            self.kPIDLoopIdx,
            self.kTimeoutMs,
        )

        self.right.configSelectedFeedbackSensor(
            FeedbackDevice.QuadEncoder,
            self.kPIDLoopIdx,
            self.kTimeoutMs
        )

        self.left.setSensorPhase(True)
        self.left.setInverted(False)

        self.right.setSensorPhase(True)
        self.right.setInverted(False)
        # Set relevant frame periods to be at least as fast as periodic rate
        self.left.setStatusFramePeriod(
            StatusFrameEnhanced.Status_13_Base_PIDF0, 10, self.kTimeoutMs
        )
        self.left.setStatusFramePeriod(
            StatusFrameEnhanced.Status_10_MotionMagic, 10, self.kTimeoutMs
        )

        self.right.setStatusFramePeriod(
            StatusFrameEnhanced.Status_13_Base_PIDF0, 10, self.kTimeoutMs
        )
        self.right.setStatusFramePeriod(
            StatusFrameEnhanced.Status_10_MotionMagic, 10, self.kTimeoutMs
        )

        # set the peak and nominal outputs
        self.left.configNominalOutputForward(0, self.kTimeoutMs)
        self.left.configNominalOutputReverse(0, self.kTimeoutMs)
        self.left.configPeakOutputForward(1, self.kTimeoutMs)
        self.left.configPeakOutputReverse(-1, self.kTimeoutMs)

        # set closed loop gains in slot0 - see documentation */
        self.left.selectProfileSlot(self.kSlotIdx, self.kPIDLoopIdx)
        self.left.config_kF(0, 0.2, self.kTimeoutMs)
        self.left.config_kP(0, 0.2, self.kTimeoutMs)
        self.left.config_kI(0, 0, self.kTimeoutMs)
        self.left.config_kD(0, 0, self.kTimeoutMs)
        # set acceleration and vcruise velocity - see documentation
        self.left.configMotionCruiseVelocity(5000, self.kTimeoutMs)
        self.left.configMotionAcceleration(2000, self.kTimeoutMs)
        # zero the sensor
        self.left.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)

        self.left.configNominalOutputForward(0, self.kTimeoutMs)
        self.left.configNominalOutputReverse(0, self.kTimeoutMs)
        self.left.configPeakOutputForward(1, self.kTimeoutMs)
        self.left.configPeakOutputReverse(-1, self.kTimeoutMs)

        # set closed loop gains in slot0 - see documentation */
        self.right.selectProfileSlot(self.kSlotIdx, self.kPIDLoopIdx)
        self.right.config_kF(0, 0.2, self.kTimeoutMs)
        self.right.config_kP(0, 0.2, self.kTimeoutMs)
        self.right.config_kI(0, 0, self.kTimeoutMs)
        self.right.config_kD(0, 0, self.kTimeoutMs)
        # set acceleration and vcruise velocity - see documentation
        self.right.configMotionCruiseVelocity(5000, self.kTimeoutMs)
        self.right.configMotionAcceleration(2000, self.kTimeoutMs)
        # zero the sensor
        self.right.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)

        self.right.configNominalOutputForward(0, self.kTimeoutMs)
        self.right.configNominalOutputReverse(0, self.kTimeoutMs)
        self.right.configPeakOutputForward(1, self.kTimeoutMs)
        self.right.configPeakOutputReverse(-1, self.kTimeoutMs)

        self.targetPos = 1000

    def teleopInit(self):
        self.left.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)
        self.right.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)


    def teleopPeriodic(self):
        wpilib.SmartDashboard.putNumber("target position", self.targetPos)

        """
        This function is called periodically during operator control
        """
        # get gamepad axis - forward stick is positive
        leftYstick = -1.0 * self.controller.getX(self.controller.Hand.kLeftHand)
        # calculate the percent motor output
        motorOutput = self.left.getMotorOutputPercent()

        # prepare line to print
        sb = []
        sb.append("\tOut%%: %.3f" % motorOutput)
        sb.append(
            "\tVel: %.3f" % self.left.getSelectedSensorVelocity(self.kPIDLoopIdx)
        )

        if self.controller.getXButton():
            self.targetPos += 100
        if self.controller.getYButton():
            self.targetPos -= 100

        if self.controller.getBButton():
            # Motion Magic - 4096 ticks/rev * 3 Rotations in either direction
            # This might not be accurate for our encoders - Noah
            self.left.set(ControlMode.MotionMagic, self.targetPos)
            self.right.set(ControlMode.MotionMagic, (-1 * self.targetPos))
            # append more signals to print when in speed mode.
            sb.append("\terr: %s" % self.left.getClosedLoopError(self.kPIDLoopIdx))
            sb.append("\ttrg: %.3f" % self.targetPos)
        else:
            # Percent voltage mode
            pass
            self.left.set(ControlMode.PercentOutput, leftYstick)
            self.right.set(ControlMode.PercentOutput, leftYstick)

        # instrumentation
        self.processInstrumentation(self.left, sb)
        self.processInstrumentation(self.right, sb)

    def processInstrumentation(self, tal, sb):

        # smart dash plots
        wpilib.SmartDashboard.putNumber(
            "SensorVel", tal.getSelectedSensorVelocity(self.kPIDLoopIdx)
        )
        wpilib.SmartDashboard.putNumber(
            "SensorPos", tal.getSelectedSensorPosition(self.kPIDLoopIdx)
        )
        wpilib.SmartDashboard.putNumber(
            "MotorOutputPercent", tal.getMotorOutputPercent()
        )
        wpilib.SmartDashboard.putNumber(
            "ClosedLoopError", tal.getClosedLoopError(self.kPIDLoopIdx)
        )

        # check if we are motion-magic-ing
        if tal.getControlMode() == ControlMode.MotionMagic:
            self.timesInMotionMagic += 1
        else:
            self.timesInMotionMagic = 0

        if self.timesInMotionMagic > 10:
            # print the Active Trajectory Point Motion Magic is servoing towards
            wpilib.SmartDashboard.putNumber(
                "ClosedLoopTarget", tal.getClosedLoopTarget(self.kPIDLoopIdx)
            )

            if not self.isSimulation():
                wpilib.SmartDashboard.putNumber(
                    "ActTrajVelocity", tal.getActiveTrajectoryVelocity()
                )
                wpilib.SmartDashboard.putNumber(
                    "ActTrajPosition", tal.getActiveTrajectoryPosition()
                )
                # wpilib.SmartDashboard.putNumber(
                #     "ActTrajHeading", tal.getActiveTrajectoryHeading()
                # )
                # commented the above lines out because no method apparently
        # periodically print to console
        self.loops += 1
        if self.loops >= 10:
            self.loops = 0
            print(" ".join(sb))

        # clear line cache
        sb.clear()


if __name__ == "__main__":
    wpilib.run(Robot)