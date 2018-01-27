#!/usr/bin/env python3

import magicbot
import wpilib

from automations.intake import IntakeAutomation
from components.intake import Intake
from ctre import WPI_TalonSRX



class Robot(magicbot.MagicRobot):
    # Add magicbot components here using variable annotations.
    # Any components that directly actuate motors should be declared after
    # any higher-level components (automations) that depend on them.

    # Automations
    intake_automation: IntakeAutomation

    # Actuators
    intake: Intake

    def createObjects(self):
        """Create non-components here."""
        """This is to state what channel our xbox controller is on"""
        self.xbox = wpilib.XboxController(0)
        """This controls the front section of the intake mechanism, This controls two motors."""
        self.intake_motor1 = WPI_TalonSRX(1)
        """This controls the back section of the intake mechanism, this controls two motors."""
        self.intake_motor2 = WPI_TalonSRX(2)
        """This controls the left arm in the containment mechanism"""
        self.clamp_arm_left = wpilib.Solenoid(0)
        """This controls the right arm in the containment mechanism"""
        self.clamp_arm_right = wpilib.Solenoid(1)
        """This controls the kicker in the back section of the intake mechanism"""
        self.intake_kicker = wpilib.Solenoid(3)
        """This is the limit switch at the back of the containment section"""
        self.limit_switch = wpilib.DigitalInput(0)

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        self.intake.intake_clamp(False)
        self.intake.intake_push(False)
        self.lift_motor = WPI_TalonSRX(0)

    def teleopPeriodic(self):
        """
        Process inputs from the driver station here.

        This is run each iteration of the control loop before magicbot
        components are executed.
        """

        # self.intake.intake_arm(self.xbox.getBButton())

        if self.xbox.getXButtonReleased():
            self.intake_automation.engage()


if __name__ == '__main__':
    wpilib.run(Robot)
