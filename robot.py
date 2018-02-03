#!/usr/bin/env python3

import magicbot
import wpilib
import numpy as np
from automations.intake import IntakeAutomation
from automations.lifter import LifterAutomation
from automations.motion import ChassisMotion
from components.intake import Intake
from components.lifter import Lifter
from components.vision import Vision
from pyswervedrive.swervechassis import SwerveChassis
from pyswervedrive.swervemodule import SwerveModule
from utilities.bno055 import BNO055
from utilities.functions import rescale_js

import math


class Robot(magicbot.MagicRobot):
    # Add magicbot components here using variable annotations.
    # Any components that directly actuate motors should be declared after
    # any higher-level components (automations) that depend on them.

    vision: Vision

    # Automations
    motion: ChassisMotion
    intake_automation: IntakeAutomation
    lifter_automation: LifterAutomation
    # Actuators
    intake: Intake
    lifter: Lifter

    module_drive_free_speed: float = 780.
    length: float = 0.88

    def createObjects(self):
        """Create non-components here."""

        self.module_a = SwerveModule(  # top left module
            steer_talon=ctre.WPI_TalonSRX(2), drive_talon=ctre.WPI_TalonSRX(9),
            steer_enc_offset=-2055, x_pos=0.31, y_pos=0.26,
            drive_free_speed=Robot.module_drive_free_speed)
        self.module_b = SwerveModule(  # bottom left modulet
            steer_talon=ctre.WPI_TalonSRX(11), drive_talon=ctre.WPI_TalonSRX(13),
            steer_enc_offset=-2583, x_pos=-0.31, y_pos=0.26,
            drive_free_speed=Robot.module_drive_free_speed)
        self.module_c = SwerveModule(  # bottom right modulet
            steer_talon=ctre.WPI_TalonSRX(8), drive_talon=ctre.WPI_TalonSRX(6),
            steer_enc_offset=-1665, x_pos=-0.31, y_pos=-0.26,
            drive_free_speed=Robot.module_drive_free_speed)
        self.module_d = SwerveModule(  # top right modulet
            steer_talon=ctre.WPI_TalonSRX(4), drive_talon=ctre.WPI_TalonSRX(14),
            steer_enc_offset=-286, x_pos=0.31, y_pos=-0.26,
            drive_free_speed=Robot.module_drive_free_speed)

        # create the imu object
        self.bno055 = BNO055()

        # boilerplate setup for the joystick
        self.joystick = wpilib.Joystick(0)

        self.cube_switch = wpilib.DigitalInput(0)

        self.spin_rate = 5

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        self.motion.enabled = False
        self.chassis.set_inputs(0, 0, 0)

    def teleopPeriodic(self):
        """
        Process inputs from the driver station here.

        This is run each iteration of the control loop before magicbot
        components are executed.
        """
        if self.joystick.getRawButtonPressed(10):
            self.chassis.odometry_x = 0.0
            self.chassis.odometry_y = 0.0
            self.motion.set_waypoints(np.array(
                [[0, 0, 0, 1], [1, 0, 0, 1], [1, 1, 0, 1], [2, 1, 0, 1], [2, 1, 0, 0]]))
        if self.joystick.getRawButtonPressed(9):
            self.motion.disable()
            self.chassis.field_oriented = True

        if self.joystick.getRawButtonPressed(8):
            print("Heading sp set")
            self.chassis.set_heading_sp(self.bno055.getAngle() + math.pi)

        # this is where the joystick inputs get converted to numbers that are sent
        # to the chassis component. we rescale them using the rescale_js function,
        # in order to make their response exponential, and to set a dead zone -
        # which just means if it is under a certain value a 0 will be sent
        # TODO: Tune these constants for whatever robot they are on
        vx = -rescale_js(self.joystick.getY(), deadzone=0.05, exponential=1.2, rate=4)
        vy = -rescale_js(self.joystick.getX(), deadzone=0.05, exponential=1.2, rate=4)
        vz = -rescale_js(self.joystick.getZ(), deadzone=0.2, exponential=15.0, rate=self.spin_rate)
        self.chassis.set_inputs(vx, vy, vz)


if __name__ == '__main__':
    wpilib.run(Robot)
