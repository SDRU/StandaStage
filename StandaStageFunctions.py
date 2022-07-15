# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 11:04:45 2021

@author: Sandora
"""

from pyximc import *


def info(lib, device_id):
    x_device_information = device_information_t()
    result = lib.get_device_information(device_id, byref(x_device_information))
    print("Result: " + repr(result))
    if result == Result.Ok:
        print("Device information:")
        print(" Manufacturer: " +
                repr(string_at(x_device_information.Manufacturer).decode()))
        print(" ManufacturerId: " +
                repr(string_at(x_device_information.ManufacturerId).decode()))
        print(" ProductDescription: " +
                repr(string_at(x_device_information.ProductDescription).decode()))
        print(" Major: " + repr(x_device_information.Major))
        print(" Minor: " + repr(x_device_information.Minor))
        print(" Release: " + repr(x_device_information.Release))
        
        
def get_serial_nr(lib, device_id):
    nr = serial_number_t()
    result = lib.get_serial_number(device_id, byref(nr))
    print(f"Serial number is {nr.SN}")
    return nr.SN

def status(lib, device_id):
    x_status = status_t()
    result = lib.get_status(device_id, byref(x_status))
    print("Result: " + repr(result))
    if result == Result.Ok:
        print("Status.Ipwr: " + repr(x_status.Ipwr))
        print("Status.Upwr: " + repr(x_status.Upwr))
        print("Status.Iusb: " + repr(x_status.Iusb))
        print("Status.Flags: " + repr(hex(x_status.Flags)))

def get_position(lib, device_id):
    x_pos = get_position_t()
    result = lib.get_position(device_id, byref(x_pos))
    # if result == Result.Ok:
    #     print("Position: {0} steps, {1} microsteps".format(x_pos.Position, x_pos.uPosition))
    return x_pos.Position, x_pos.uPosition

def left(lib, device_id):
    result = lib.command_left(device_id)
    print("Moved left: " + repr(result))
    
def right(lib, device_id):
    result = lib.command_right(device_id)
    print("Moved right: " + repr(result))

def move(lib, device_id, distance, udistance):
    result = lib.command_move(device_id, distance, udistance)
    print(f"Moved to {distance} steps, {udistance} microsteps: " + repr(result))

def wait_for_stop(lib, device_id, interval):
    # print("\nWaiting for stop")
    result = lib.command_wait_for_stop(device_id, interval)

def serial(lib, device_id):
    x_serial = c_uint()
    result = lib.get_serial_number(device_id, byref(x_serial))
    if result == Result.Ok:
        print("Serial: " + repr(x_serial.value))

def get_speed(lib, device_id)        :
    # Create move settings structure
    mvst = move_settings_t()
    # Get current move settings from controller
    result = lib.get_move_settings(device_id, byref(mvst))
    print(f"Speed is {mvst.Speed}: " + repr(result))   
    return mvst.Speed
        
def set_speed(lib, device_id, speed):
    # Create move settings structure
    mvst = move_settings_t()
    # Get current move settings from controller
    result = lib.get_move_settings(device_id, byref(mvst))
    # Change current speed
    mvst.Speed = int(speed)
    # Write new move settings to controller
    result = lib.set_move_settings(device_id, byref(mvst))
    # Print command return status. It will be 0 if all is OK
    print(f"Speed changed to {speed}: " + repr(result))        
 

def set_microstep_mode_256(lib, device_id):
    print("\nSet microstep mode to 256")
    # Create engine settings structure
    eng = engine_settings_t()
    # Get current engine settings from controller
    result = lib.get_engine_settings(device_id, byref(eng))
    # Print command return status. It will be 0 if all is OK
    print("Read command result: " + repr(result))
    # Change MicrostepMode parameter to MICROSTEP_MODE_FRAC_256
    # (use MICROSTEP_MODE_FRAC_128, MICROSTEP_MODE_FRAC_64 ... for other microstep modes)
    eng.MicrostepMode = MicrostepMode.MICROSTEP_MODE_FRAC_256
    # Write new engine settings to controller
    result = lib.set_engine_settings(device_id, byref(eng))
    # Print command return status. It will be 0 if all is OK
    print("Write command result: " + repr(result))    
    
def set_engine_settings(lib, device_id):
    print("\nSet microstep mode to full, enable backlash correction")
    # Create engine settings structure
    eng = engine_settings_t()
    # Get current engine settings from controller
    result = lib.get_engine_settings(device_id, byref(eng))
    # Print command return status. It will be 0 if all is OK
    # Change MicrostepMode parameter to MICROSTEP_MODE_FRAC_256
    # (use MICROSTEP_MODE_FRAC_128, MICROSTEP_MODE_FRAC_64 ... for other microstep modes)
    eng.MicrostepMode = MicrostepMode.MICROSTEP_MODE_FULL
    eng.ENGINE_ANTIPLAY = 1
    # Write new engine settings to controller
    result = lib.set_engine_settings(device_id, byref(eng))
    # Print command return status. It will be 0 if all is OK
    print("Write command result: " + repr(result))    
    
def get_syncin_settings(lib, device_id)        :
    # Create syncin settings structure
    mvst = sync_in_settings_t()
    # Get current syncin settings from controller
    result = lib.get_sync_in_settings(device_id, byref(mvst))
    # Print command return status. It will be 0 if all is OK
    print("Got syncin settings: " + repr(result))   
    return mvst

def set_syncin_settings(lib, device_id,position,speed):
    # Create engine settings structure
    sync = sync_in_settings_t()
    result = lib.get_sync_in_settings(device_id, byref(sync))
    # 1 1 1 enable sync, falling edge, move absolute
    sync.SyncInFlags = int('101',2)
    sync.Position = position
    sync.Speed = speed
    result = lib.set_sync_in_settings(device_id, byref(sync))
    # Print command return status. It will be 0 if all is OK
    # print("Wrote syncin settings: " + repr(result))        
    

def get_syncout_settings(lib, device_id)        :
    # Create syncin settings structure
    mvst = sync_out_settings_t()
    # Get current syncin settings from controller
    result = lib.get_sync_out_settings(device_id, byref(mvst))
    # Print command return status. It will be 0 if all is OK
    print("Got syncout settings: " + repr(result))   
    return mvst

def get_calibration_settings(lib, device_id)        :
    # Create syncin settings structure
    mvst = calibration_settings_t()
    # Get current syncin settings from controller
    result = lib.get_calibration_settings(device_id, byref(mvst))
    # Print command return status. It will be 0 if all is OK
    print("Got calibration settings: " + repr(result))   
    return mvst

def main(lib, device_id, pos1, pos2, speed):
    info(lib, device_id)
    serial_nr = get_serial_nr(lib,device_id)
    
    if serial_nr == 14954:
        step = 394745/25
    if serial_nr == 14976:
        step = 393358/25
        
    pos1 = int(step*pos1)
    pos2 = int(step*pos2)
    speed = int(step*speed)
    

    status(lib, device_id)
    set_engine_settings(lib, device_id)

    lib.command_homezero(device_id)
    wait_for_stop(lib, device_id, 1000)
    pos, upos = get_position(lib, device_id) 
    move = 1
    print(pos)
   
    while True:
        pos, upos = get_position(lib, device_id) 
        if ((pos in range(pos1-200,pos1+200)) and (move == 1)):
            wait_for_stop(lib, device_id, 1000)
            pos, upos = get_position(lib, device_id) 
            set_syncin_settings(lib, device_id,pos2,speed)
            move = 2
            print("Moving to pos2")
            # syncin_settings=get_syncin_settings(lib, device_id)
            print(pos-pos1)
            
        if ((pos in range(pos2-200,pos2+200)) and (move == 2)):
            wait_for_stop(lib, device_id, 1000)
            pos, upos = get_position(lib, device_id) 
            set_syncin_settings(lib, device_id,pos1,speed)
            move = 1
            print("Moving to pos1")
            # syncin_settings=get_syncin_settings(lib, device_id)
            print(pos-pos2)