import commands2

import constants

from .drivedistance import DriveDistance
from .movecommand import MoveCommand
from subsystems.drivesubsystem import DriveSubsystem
from .reset_gyro import ResetGyro


class ComplexAuto(commands2.SequentialCommandGroup):
    """
    A complex auto command that drives forward, releases a hatch, and then drives backward.
    """

    def __init__(self, drive: DriveSubsystem):
        super().__init__(
            # Drive forward the specified distance
            ResetGyro(drive),
            MoveCommand(-3, 0, drive),
            MoveCommand(0, 90, drive),
            MoveCommand(-3, 90, drive),
            MoveCommand(0, 180, drive),
            MoveCommand(-3, 180, drive),
            MoveCommand(0, 270, drive),
            MoveCommand(-3, 270, drive),
            MoveCommand(0, 360, drive),
            # DriveDistance(
            #     constants.kAutoDriveDistanceInches, constants.kAutoDriveSpeed, drive
            # ),
            # # Drive backward the specified distance
            # DriveDistance(
            #     constants.kAutoBackupDistanceInches, -constants.kAutoDriveSpeed, drive
            # ),
        )
