#!/usr/bin/env python3

import magicbot
import wpilib
from automations.lifter import LifterAutomation
from automations.intake import IntakeAutomation
from components.intake import Intake
from components.lifter import Lifter
import ctre
from networktables import NetworkTables


class Robot(magicbot.MagicRobot):
    # Add magicbot components here using variable annotations.
    # Any components that directly actuate motors should be declared after
    # any higher-level components (automations) that depend on them.

    # Automations
    intake_automation: IntakeAutomation
    lifter_automation: LifterAutomation
    # Actuators
    intake: Intake
    lifter: Lifter

    def createObjects(self):
        """Create non-components here."""
        """This is to state what channel our xbox controller is on"""
        self.xbox = wpilib.XboxController(0)
        """This controls the front section of the intake mechanism, This controls two motors."""
        self.intake_motor1 = ctre.WPI_TalonSRX(1)
        """This controls the back section of the intake mechanism, this controls two motors."""
        self.intake_motor2 = ctre.WPI_TalonSRX(2)
        """This controls the left arm in the containment mechanism"""
        self.clamp_arm_left = wpilib.Solenoid(0)
        """This controls the right arm in the containment mechanism"""
        self.clamp_arm_right = wpilib.Solenoid(1)
        """This controls the kicker in the back section of the intake mechanism"""
        self.intake_kicker = wpilib.Solenoid(2)
        self.extension_arm_left = wpilib.Solenoid(3)
        self.extension_arm_right = wpilib.Solenoid(4)
        """This is the limit switch at the back of the containment section"""
        self.limit_switch = wpilib.DigitalInput(0)

        self.lift_motor = ctre.WPI_TalonSRX(5)

        self.sd = NetworkTables.getTable("SmartDashboard")

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        self.intake.intake_clamp(False)
        self.intake.intake_push(False)
        self.intake.extensions(True)

    def teleopPeriodic(self):
        """
        Process inputs from the driver station here.

        This is run each iteration of the control loop before magicbot
        components are executed.
        """
        self.put_dashboard()

        # self.intake.intake_arm(self.xbox.getBButton())
        if self.xbox.getPOV() != -1:
            self.lifter.pov_change(self.xbox.getPOV())

        if self.xbox.getXButtonReleased():
            self.intake_automation.engage()

    def put_dashboard(self):
        self.sd.putString("default_height", self.lifter.default_height)


if __name__ == '__main__':
    wpilib.run(Robot)
