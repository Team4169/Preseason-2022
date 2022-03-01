import commands2

from subsystems.drivesubsystem import DriveSubsystem


class MoveCommand(commands2.CommandBase):
    def __init__(self, distance: float, heading: float, drive: DriveSubsystem) -> None:
        super().__init__()
        # Feature to add - difference tolerance per command instance. Currently uses the default from DriveSubsystem
        # Feature to add - different max speed for each command. Currently uses method of DriveSubsystem.
        self.drive = drive
        self.distance = distance * self.drive.tpf
        self.heading = heading
        self.goal_threshold_ticks = 20 # I believe 50 ticks per second, confirm.
        self.addRequirements(drive)


    def initialize(self) -> None:
        self.drive.resetEncoders()
        # This increases everytime the robot remains in the target
        self.in_threshold = 0
        self.drive.driveController.setSetpoint(self.distance)
        self.drive.turnController.setSetpoint(self.heading)

    def execute(self) -> None:
        if self.distance:
            drivespeed = self.drive.driveController.calculate(self.drive.getAverageEncoderDistance(), self.distance)
            drivespeed = self.drive.validateDriveSpeed(drivespeed)
        else:
            drivespeed = 0
        turnspeed = self.drive.turnController.calculate(self.drive.gyro.getYaw(), self.heading)
        turnspeed = self.drive.validateTurnSpeed(turnspeed)
        self.drive.arcadeDrive(drivespeed, turnspeed)

    def end(self, interrupted: bool) -> None:
        self.drive.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        if self.drive.turnController.atSetpoint() and self.distance and self.drive.driveController.atSetpoint():
            self.in_threshold += 1
        else:
            self.in_threshold = 0
        if self.in_threshold > self.goal_threshold_ticks:
            return True
        return False
