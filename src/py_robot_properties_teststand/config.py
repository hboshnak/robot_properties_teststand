"""
@file config.py
@author Maximilien Naveau (maximilien.naveau@gmail.com)
@license License BSD-3-Clause
@copyright Copyright (c) 2019, New York University and Max Planck Gesellschaft.
@date 2019-05-22
@brief Define the interface between the control and the hardware
"""

import numpy as np
from math import pi
import rospkg
from os.path import join
import pinocchio as se3


class TeststandConfig:
    # name that is used by every other entities. I do not exactly why...
    robot_name = "teststand"

    # PID gains
    kp = 5.0
    kd = 0.1
    ki = 0.0

    # here we use the same urdf as for the quadruped but without the freeflyer
    urdf_path = (
        join(rospkg.RosPack().get_path("robot_properties_teststand"),
             "urdf",
             "teststand.urdf")
    )

    yaml_path = (
        join(rospkg.RosPack().get_path("robot_properties_teststand"),
             "config",
             "teststand.yaml")
    )

    # The inertia of a single blmc_motor
    motor_inertia = 0.0000045

    # The motor gear ratio
    motor_gear_ration = 9.

    # The Kt constant of the motor [Nm/A]: tau = I * Kt
    motor_torque_constant = 0.025

    # pinocchio model
    robot_model = se3.buildModelFromUrdf(urdf_path)
    robot_model.rotorInertia[1:] = motor_inertia
    robot_model.rotorGearRatio[1:] = motor_gear_ration

    # the number of motors, here they are the same as there are only revolute
    # joints
    nb_joints = robot_model.nv - 1

    # control time period
    control_period = 0.001
    dt = control_period


    # maxCurrent = 12 # Ampers
    max_current = 2

    # maximum torques
    max_torque = motor_torque_constant * max_current

    # maximum control one can send, here the control is the current.
    max_control = max_current

    # mapping between the ctrl vector in the device and the urdf indexes
    urdf_to_dgm = (0,1,2)

    # ctrl_manager_current_to_control_gain I am not sure what it does so 1.0.
    ctrl_manager_current_to_control_gain=1.0

    map_joint_name_to_id = {}
    map_joint_limits = {}
    for i, (name, lb, ub) in enumerate(zip(robot_model.names[1:],
                                       robot_model.lowerPositionLimit,
                                       robot_model.upperPositionLimit)):
        map_joint_name_to_id[name] = i
        map_joint_limits[i] = [float(lb), float(ub)]

    max_qref = pi

    @staticmethod
    def buildRobotWrapper():
        return se3.robot_wrapper.RobotWrapper(TeststandConfig.robot_model)
