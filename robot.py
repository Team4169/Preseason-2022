from networktables import NetworkTables
import wpilib


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.sd = NetworkTables.getTable("SmartDashboard")
        self.limitswitch = wpilib.DigitalInput(0)

    def autnomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        print("switch = ",self.limitswitch.get())
        self.sd.putValue("limitswitch", self.limitswitch.get())

if __name__ == "__main__":
    wpilib.run(MyRobot)
