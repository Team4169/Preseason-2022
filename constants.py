#
# The constants module is a convenience place for teams to hold robot-wide
# numerical or boolean constants. Don't use this for any other purpose!
#

import math
import wpilib

# Motors
kLeftMotor1Port = 8
kLeftMotor2Port = 2
kRightMotor1Port = 10
kRightMotor2Port = 6

# Encoders
# kLeftEncoderPorts = (0, 1)
# kRightEncoderPorts = (2, 3)
kLeftEncoderReversed = False
kRightEncoderReversed = True

kEncoderCPR = 1024
kWheelDiameterInches = 6
# Assumes the encoders are directly mounted on the wheel shafts
# kEncoderDistancePerPulse = (kWheelDiameterInches * math.pi) / kEncoderCPR
kEncoderDistancePerPulse = 1 / 924 * 12 #in inches

# Autonomous
kAutoDriveDistanceInches = 60
kAutoBackupDistanceInches = 20
kAutoDriveSpeed = 0.5

# Operator Interface
kDriverControllerPort = 0

# Physical parameters
kDriveTrainMotorCount = 2
kTrackWidth = 0.381 * 2
kGearingRatio = 8
kWheelRadius = 0.0508

# kEncoderResolution = -
