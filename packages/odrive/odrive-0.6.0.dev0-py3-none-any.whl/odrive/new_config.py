
import odrive.database
from odrive.enums import *
from odrive.rich_text import RichText
import odrive.enums
import time
import struct
import functools

example_config = {
    "version": 0.1,

    "odrives": [
        {
            "serial_number": "356E395D3339",
            "board_version": "v4.4-58V",
            "inc_enc": [(0, 0)],
            "motors": [(0, 0)],
            "thermistors": [None]
        },
    ],

    "axes": [
        {
            "motors": [
                {
                    "type": "D5065-270KV",
                    "scale": 1.0
                }
            ],
            "encoders": [
                {
                    "type": "amt102",
                    "scale": 1.0
                },
            ],
            "pos_encoder": 0,
            "vel_encoder": 0,
            "commutation_encoder": 0,
        }
    ],

    # Each entry represents one RS485 bus
    "rs485": [
        # Each entry in a bus represents one port
        #[("axis.encoder", 0, 0), ("odrive.rs485", 0, 0)]
    ]
}

db = odrive.database.load()

CALIBRATION_STATUS_OK = object()
CALIBRATION_STATUS_NEEDED = object()
CALIBRATION_STATUS_RECOMMENDED = object()
CALIBRATION_STATUS_UNKNOWN = object()

class CalibrationTask():
    def __init__(self, name, func, status):
        self.name = name
        self.func = func
        self.status = status

    def run(self):
        self.func()

class ConfigObjectType():
    GLOBAL = object()
    ODRIVE = object()
    AXIS = object()
    AXIS_MOTOR = object()
    AXIS_ENCODER = object()
    RS485 = object()

class IssueType():
    ERROR = object() # error level issues prevent the configuration from being written onto the ODrive(s)
    WARN = object() # warn level issues don't prevent the configuration from being applied but require user attention

class IssueCollection():
    def __init__(self):
        self.issues = []

    def append(self, scope, coord, message, level = IssueType.ERROR):
        """
        Appends an issue to the issue collection.

        `scope` and `coord` defines which object in the user configuration the
        issue pertains to.

        `scope` must be one of ConfigObjectType's members.
        """
        self.issues.append((scope, coord, message, level))

    def get(self, scope, coord):
        """
        Returns all issues pertaining to the specified configuration object.
        """
        for _scope, _coord, message, level in self.issues:
            if (_scope, _coord) == (scope, coord):
                yield message, level


def run_state(axis, state):
    axis.requested_state = state
    while axis.requested_state == state:
        time.sleep(0.1)
    while axis.procedure_result == PROCEDURE_RESULT_BUSY:
        time.sleep(0.1)

    result = axis.procedure_result
    if result != PROCEDURE_RESULT_SUCCESS:
        codes = {v: k for k, v in odrive.enums.__dict__ .items() if k.startswith("PROCEDURE_RESULT_")}
        raise Exception("Device returned {}".format(codes.get(result, "unknown code {}".format(result))))

def run_motor_calibration(axis, motor_config):
    run_state(axis, AXIS_STATE_MOTOR_CALIBRATION)
    motor_config['phase_resistance'] = axis.motor.config.phase_resistance
    motor_config['phase_inductance'] = axis.motor.config.phase_inductance

def run_encoder_offset_calibration(axis):
    run_state(axis, AXIS_STATE_ENCODER_OFFSET_CALIBRATION)

def process_config(odrives, config):
    """
    Processes the provided configuration while taking into account the list of
    connected ODrives and their state.

    Returns a tuple (odrv_list, output_configs, issues, axis_calib)
    where:

    odrv_list: A list of ODrive objects that need to be configured. Some entries
        can be None.
    output_configs: A list of multi-level dictionaries that hold all
        configuration settings for all ODrives, whether they are connected or
        not. The order an length of this list corresponds to `odrv_list`.
    odrv_infos: TODO: this might be removed
    axis_infos: A list of lists of strings representing human readable warnings
        and errors that pertain to each axis.
        Each list in axis_infos corresponds to an axis in the input `config`.
        Each string represents a problem with the configuration.
    axis_calib: A list of lists of CalibrationTask objects representing the
        available calibration tasks for this axis.
        Each list in axis_calib corresponds to an axis in the input `config`.
    """

    assert(config['version'] == 0.1)

    inverter_ids = [[] for _ in range(len(config['axes']))]
    axis_calib = [[] for _ in range(len(config['axes']))]
    encoder_ids = [{} for _ in range(len(config['odrives']))]
    output_configs = [{} for _ in range(len(config['odrives']))]
    odrv_list = [None for _ in range(len(config['odrives']))]

    issues = IssueCollection()

    # Associate ODrive axes with machine axes
    for odrv_num, odrv_config in enumerate(config['odrives']):
        for inv_num, motor_coords in enumerate(odrv_config['motors']):
            if motor_coords is None:
                continue
            (axis_num, motor_num) = motor_coords
            inverter_ids[axis_num].append((odrv_num, inv_num))

    # Configure all RS485 components (currently only encoders)
    for bus_num, connection in enumerate(config['rs485']):
        all_odrives_on_bus = [port[1:] for port in connection if port[0] == "odrive.rs485"]
        all_encoders_on_bus = [port[1:] for port in connection if port[0] == "axis.encoder"]

        if len(all_odrives_on_bus) > 1:
            issues.append(ConfigObjectType.RS485, bus_num, "Multiple ODrives are not allowed on the same RS485 bus")
            continue

        for odrv_num, rs485_num in all_odrives_on_bus:
            odrv_output_config = output_configs[odrv_num]

            for axis_num, enc_num in all_encoders_on_bus:
                encoder_config = config['axes'][axis_num]['encoders'][enc_num]
                if encoder_config['type'] != 'amt21':
                    issues.append(ConfigObjectType.AXIS_ENCODER, (axis_num, enc_num), f"Encoder type {encoder_config['type']} not supported over RS485.")
                    continue # ignore encoder

                # Each amt21_encoder_group is dedictated to one RS485 port on the ODrive.
                # One port can talk to multiple encoders (needs firmware change!).
                if f'amt21_encoder_group{rs485_num}' in odrv_output_config:
                    amt21_encoder_group_config = odrv_output_config[f'amt21_encoder_group{rs485_num}']
                else:
                    amt21_encoder_group_config = {'config': {'enable': True, 'rs485': rs485_num}}
                    odrv_output_config[f'amt21_encoder_group{rs485_num}'] = amt21_encoder_group_config

                if 'addr0' in amt21_encoder_group_config['config']:
                    issues.append(ConfigObjectType.ODRIVE, odrv_num, f"Current firmware does not support more than AMT21 encoder.")
                    continue # ignore encoder

                amt21_encoder_group_config['config']['addr0'] = encoder_config.get('addr', 0x54) # use default AMT21 address if unspecified
                encoder_ids[odrv_num][(axis_num, enc_num)] = ENCODER_ID_AMT21_ENCODER0


    for odrv_num, odrv_config in enumerate(config['odrives']):
        odrv_output_config = output_configs[odrv_num]

        if not 'serial_number' in odrv_config:
            issues.append(ConfigObjectType.ODRIVE, odrv_num, 'Not associated with any serial number.')
            odrv_list[odrv_num] = None
        elif not odrv_config['serial_number'] in odrives:
            issues.append(ConfigObjectType.ODRIVE, odrv_num, 'Not connected.')
            odrv_list[odrv_num] = None
        else:
            odrv_list[odrv_num] = odrives[odrv_config['serial_number']]

        # Configure incremental encoders
        for i in range(len(odrv_config['inc_enc'])):
            if odrv_config['inc_enc'][i] is None:
                continue
            (axis_num, encoder_num) = odrv_config['inc_enc'][i]
            axis_config = config['axes'][axis_num]
            enc_config = axis_config['encoders'][encoder_num]
            enc_data = db.get_encoder(enc_config['type'])

            odrv_output_config["inc_encoder{}".format(i)] = {
                'config': {'cpr': enc_data['cpr']}
            }
            encoder_ids[odrv_num][(axis_num, encoder_num)] = [ENCODER_ID_INC_ENCODER0, ENCODER_ID_INC_ENCODER1][i]

        # Configure motors
        for odrv_inv_num, motor_coords in enumerate(odrv_config['motors']):
            if motor_coords is None:
                continue
            (axis_num, motor_num) = motor_coords
            axis_config = config['axes'][axis_num]
            motor_config = axis_config['motors'][motor_num]
            motor_data = db.get_motor(motor_config['type'])

            axis_output_config = odrv_output_config['axis{}'.format(odrv_inv_num)] = {'motor': {'config': {}}, 'controller': {'config': {}}, 'config': {}}

            if 'phase_resistance' in motor_config:
                axis_output_config['motor']['config']['phase_resistance'] = motor_config['phase_resistance']
            else:
                axis_output_config['motor']['config']['phase_resistance'] = motor_data['phase_resistance']

            if 'phase_inductance' in motor_config:
                axis_output_config['motor']['config']['phase_inductance'] = motor_config['phase_inductance']
            else:
                axis_output_config['motor']['config']['phase_inductance'] = motor_data['phase_inductance']

            # TODO: take into account user max current
            # Note: we multiply the motor current limit by two since it's given in "continuous max"
            inv_data = db.get_odrive(odrv_config['board_version'])['inverters'][odrv_inv_num]
            axis_output_config['motor']['config']['current_lim'] = min(inv_data['max_current'], 2 * motor_data['max_current'])

            axis_output_config['motor']['config']['pole_pairs'] = motor_data['pole_pairs']
            axis_output_config['motor']['config']['torque_constant'] = motor_data['torque_constant']
            axis_output_config['motor']['config']['pre_calibrated'] = True

            calibrated = 'phase_resistance' in motor_config and 'phase_inductance' in motor_config
            if not odrv_list[odrv_num] is None:
                calib = functools.partial(run_motor_calibration, getattr(odrv_list[odrv_num], 'axis{}'.format(odrv_inv_num)), motor_config)
            else:
                calib = None
            axis_calib[axis_num].append(CalibrationTask(
                "Motor Calibration",
                calib,
                CALIBRATION_STATUS_OK if calibrated else CALIBRATION_STATUS_RECOMMENDED
                ))

        # Configure thermistors
        for temp_in_num, motor_coords in enumerate(odrv_config['thermistors']):
            if motor_coords is None:
                continue # this thermistor input is not connected anywhere
            (axis_num, motor_num) = motor_coords
            axis_config = config['axes'][axis_num]
            motor_config = axis_config['motors'][motor_num]
            motor_data = db.get_motor(motor_config['type'])

            if motor_coords != odrv_config['motors'][temp_in_num]:
                issues.append(ConfigObjectType.AXIS_MOTOR, motor_coords, f"The motor thermistor must either be disconnected or connected to the thermistor input that corresponds to the same ODrive and axis to which the motor is connected.")
                continue

            axis_output_config = odrv_output_config['axis{}'.format(temp_in_num)]

            odrv_data = db.get_odrive(odrv_config['board_version'])
            temp_in_data = odrv_data['temp_in'][temp_in_num]

            coeffs = odrive.utils.calculate_thermistor_coeffs(3, temp_in_data['r_load'], motor_data['thermistor_r25'], motor_data['thermistor_beta'], 0, motor_data['max_temp'] + 10, temp_in_data['thermistor_bottom'])
            axis_output_config['motor']['motor_thermistor'] = {
                'config': {
                    'poly_coefficient_0': float(coeffs[3]),
                    'poly_coefficient_1': float(coeffs[2]),
                    'poly_coefficient_2': float(coeffs[1]),
                    'poly_coefficient_3': float(coeffs[0]),
                    'temp_limit_lower': motor_data['max_temp'] - 20,
                    'temp_limit_upper': motor_data['max_temp'],
                    'enabled': True # requires reboot (?)
                }
            }
            # TODO: set corresponding GPIO mode to 3 (or probably should be handled by firmware)

        # Configure shunt conductance
        for odrv_inv_num, shunt_conductance in enumerate(odrv_config.get('shunt_conductance', [None] * len(odrv_config['motors']))):
            if not shunt_conductance is None:
                axis_output_config = odrv_output_config['axis{}'.format(odrv_inv_num)]
                axis_output_config['motor']['config']['shunt_conductance'] = shunt_conductance

        # Other configuration
        # TODO: set vbus voltage trip level based on power supply setting
        # TODO: set dc_max_negative_current based on power supply setting
        odrv_output_config['config'] = {}
        odrv_output_config['config']['enable_brake_resistor'] = False
        odrv_output_config['config']['dc_max_negative_current'] = -1

    # Configure axes
    for axis_num, axis_config in enumerate(config['axes']):
        axis_coords = (odrv_num, axis_num)
        inverter_id = inverter_ids[axis_num]
        if len(inverter_id) == 0:
            issues.append(ConfigObjectType.AXIS, axis_num, f"Not connected to any inverter.")
            continue
        if len(inverter_id) > 1:
            issues.append(ConfigObjectType.AXIS, axis_num, f"Connected to more than one inverters.")
        odrv_num, odrv_inv_num = inverter_id[0]

        axis_output_config = output_configs[odrv_num]['axis{}'.format(odrv_inv_num)]

        if 'calib_scan_vel' in axis_config:
            axis_output_config['config']['calib_scan_vel'] = axis_config['calib_scan_vel'] * motor_data['pole_pairs'] * motor_config['scale']
        
        if 'calib_scan_distance' in axis_config:
            axis_output_config['config']['calib_scan_distance'] = axis_config['calib_scan_distance'] * motor_data['pole_pairs'] * motor_config['scale']
        
        if 'calib_scan_range' in axis_config:
            axis_output_config['config']['calib_scan_range'] = axis_config['calib_scan_range']
        
        # TODO: check if larger than current limit
        if 'calib_torque' in axis_config:
            axis_output_config['motor']['config']['calibration_current'] = axis_config['calib_torque'] / motor_data['torque_constant']

        enc_id = encoder_ids[odrv_num].get((axis_num, axis_config['pos_encoder']), None)
        if enc_id is None:
            issues.append(ConfigObjectType.AXIS, axis_num, f"Load encoder of this axis must be connected to the same odrive as the motor ({odrv_config['serial_number']})")
        else:
            axis_output_config['config']['load_encoder'] = enc_id

        enc_id = encoder_ids[odrv_num].get((axis_num, axis_config['commutation_encoder']), None)
        if enc_id is None:
            issues.append(ConfigObjectType.AXIS, axis_num, f"Commutation encoder of this axis must be connected to the same odrive as the motor ({odrv_config['serial_number']})")
        else:
            axis_output_config['config']['commutation_encoder'] = enc_id

        if axis_config['vel_encoder'] == axis_config['commutation_encoder']:
            axis_output_config['controller']['config']['use_commutation_vel'] = False
        elif axis_config['vel_encoder'] == axis_config['pos_encoder']:
            axis_output_config['controller']['config']['use_commutation_vel'] = True
        else:
            issues.append(ConfigObjectType.AXIS, axis_num, "The velocity encoder must be the same as either the position encoder or the commutation encoder.")

        #if enc_id in [ENCODER_ID_INC_ENCODER0, ENCODER_ID_INC_ENCODER1]:
        axis = None if odrv_list[odrv_num] is None else getattr(odrv_list[odrv_num], 'axis{}'.format(odrv_inv_num))
        axis_calib[axis_num].append(CalibrationTask(
            "Encoder Offset Calibration",
            None if axis is None else functools.partial(run_encoder_offset_calibration, axis),
            (CALIBRATION_STATUS_OK if ((not axis is None) and axis.commutation_mapper.status == COMPONENT_STATUS_NOMINAL) else
             CALIBRATION_STATUS_NEEDED if ((not axis is None) and axis.commutation_mapper.status == COMPONENT_STATUS_RELATIVE_MODE) else
             CALIBRATION_STATUS_UNKNOWN)
        ))

    for k, o in odrives.items():
        if not k in [c['serial_number'] for c in config['odrives']]:
            issues.append(ConfigObjectType.GLOBAL, None, "Unused ODrive: " + k, IssueType.WARN)

    return odrv_list, output_configs, issues, axis_calib


#def print_status(odrives, config):



def show_status(odrives, config, rich_text = True):
    """
    Prints the status of the configuration in a human readable format.
    This includes warnings about any issues with the configuration, calibration
    status and more.
    """

    odrv_list, output_configs, issues, axis_calib = process_config(odrives, config)

    lines = []

    check_sign = "\u2705"
    info_sign = "\U0001F4A1"
    warning_sign = "\u26A0\uFE0F "
    error_sign = "\u274C"
    question_sign = "  " # TODO

    sign = {
        IssueType.WARN: warning_sign,
        IssueType.ERROR: error_sign
    }

    style = {
        IssueType.WARN: RichText.STYLE_YELLOW,
        IssueType.ERROR: RichText.STYLE_RED
    }

    def compare(obj, config):
        equal = True
        for k, v in config.items():
            if isinstance(v, dict):
                equal = equal and compare(getattr(obj, k), v)
            elif isinstance(v, float):
                # TODO: this comparison is a bit fragile (shouldn't compare floats like this)
                equal = equal and struct.unpack("f", struct.pack("f", v))[0]
            else:
                equal = equal and getattr(obj, k) == v
            #if not equal:
            #    print(k)
        return equal

    for odrv_num, odrv in enumerate(odrv_list):
        if not odrv is None and not compare(odrv, output_configs[odrv_num]):
            # TODO: this should not be an error but a warning/recommended action
            issues.append(ConfigObjectType.ODRIVE, odrv_num, "Configuration needs to be committed to ODrive", IssueType.WARN)

    for message, level in issues.get(ConfigObjectType.GLOBAL, None):
        lines.append(sign[level] + " " + RichText(message, style[level]))

    for odrv_num, odrv_config in enumerate(config.get('odrives', [])):
        if 'serial_number' in odrv_config:
            name = "ODrive with serial number " + str(odrv_config['serial_number'])
        else:
            name = f"ODrive with unspecified serial number (#{odrv_num})"
        lines.append(name)
        for message, level in issues.get(ConfigObjectType.ODRIVE, odrv_num):
            lines.append("  " + sign[level] + " " + RichText(message, style[level]))

    for axis_num, axis_config in enumerate(config.get('axes', [])):
        lines.append("Axis " + str(axis_num))
        for message, level in issues.get(ConfigObjectType.AXIS, axis_num):
            lines.append("  " + sign[level] + RichText(message, style[level]))
        for motor_num in range(len(axis_config.get('motors', []))):
            for message, level in issues.get(ConfigObjectType.AXIS_MOTOR, (axis_num, motor_num)):
                lines.append("  " + sign[level] + " Motor " + str(motor_num) + ": " + RichText(message, style[level]))
        for enc_num in range(len(axis_config.get('encoders', []))):
            for message, level in issues.get(ConfigObjectType.AXIS_ENCODER, (axis_num, enc_num)):
                lines.append("  " + sign[level] + " Encoder " + str(enc_num) + ": " + RichText(message, style[level]))
        for calib in axis_calib[axis_num]:
            if calib.status == CALIBRATION_STATUS_OK:
                lines.append("  " + check_sign + " " + RichText(str(calib.name) + " ok", RichText.STYLE_GREEN))
            elif calib.status == CALIBRATION_STATUS_RECOMMENDED:
                lines.append("  " + info_sign + " " + RichText(str(calib.name) + " recommended", RichText.STYLE_DEFAULT))
            elif calib.status == CALIBRATION_STATUS_NEEDED:
                lines.append("  " + warning_sign + " " + RichText(str(calib.name) + " needed", RichText.STYLE_BOLD))
            elif calib.status == CALIBRATION_STATUS_UNKNOWN:
                lines.append("  " + question_sign + " " + RichText(str(calib.name) + ": unknown status", RichText.STYLE_GRAY))
            else:
                assert(False)

    print(RichText("\n").join(lines))


def apply_config(odrives, config):
    """
    Applies the configuration to the odrives.

    If there a are problems with the configuration this function throws an
    exception and does not change anything on any ODrive.
    In this case show_status() can be used to get more detailed error
    information.
    """

    odrv_list, output_configs, issues, axis_calib = process_config(odrives, config)

    if any([m for _, _, m, level in issues.issues if level == IssueType.ERROR]):
        print([m for _, _, m, level in issues.issues if level == IssueType.ERROR])
        raise Exception("There are problems with this configuration. No changes were applied to the ODrive(s).")

    def apply(obj, config):
        for k, v in config.items():
            if isinstance(v, dict):
                apply(getattr(obj, k), v)
            else:
                setattr(obj, k, v)

    for odrv_num, odrv in enumerate(odrv_list):
        if not odrv is None:
            apply(odrv, output_configs[odrv_num])


def calibrate(odrives, config, include_recommended = False):
    odrv_list, output_configs, issues, axis_calibs = process_config(odrives, config)
    
    for axis_num, axis_calib in enumerate(axis_calibs):
        for calib in axis_calib:
            if (calib.status == CALIBRATION_STATUS_RECOMMENDED and include_recommended) or calib.status == CALIBRATION_STATUS_NEEDED:
                print("Running {} on axis {}...".format(calib.name, axis_num))
                calib.run()
    print("Done!")
