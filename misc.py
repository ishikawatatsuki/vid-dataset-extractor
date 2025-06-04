
def parse_imu(msg, timestamp) -> list:
    
    w = getattr(msg, 'angular_velocity', None)
    a = getattr(msg, 'linear_acceleration', None)
    orientation = getattr(msg, 'orientation', None)
    linear_acceleration_covariance = getattr(msg, 'linear_acceleration_covariance', None)
    angular_velocity_covariance = getattr(msg, 'angular_velocity_covariance', None)
    orientation_covariance = getattr(msg, 'orientation_covariance', None)

    if w is None or a is None or orientation is None or \
        linear_acceleration_covariance is None or angular_velocity_covariance is None or orientation_covariance is None:
        return None
    
    return [
        timestamp,  # Timestamp
        w.x, w.y, w.z,  # Angular velocity
        a.x, a.y, a.z,  # Linear acceleration
        orientation.w, orientation.x, orientation.y, orientation.z,  # Orientation quaternion
        *linear_acceleration_covariance,
        *angular_velocity_covariance,
        *orientation_covariance
    ]

def parse_motor(msg, timestamp) -> list:
    
    id = getattr(msg, 'id', None)
    rpm = getattr(msg, 'rpm', None)
    current = getattr(msg, 'current', None)
    if id is None or rpm is None or current is None:
        return None
    
    return [
        timestamp,
        id,
        rpm,
        current
    ]

def parse_gps(msg, timestamp) -> list:

    latitude = getattr(msg, 'latitude', None)
    longitude = getattr(msg, 'longitude', None)
    altitude = getattr(msg, 'altitude', None)
    position_covariance = getattr(msg, 'position_covariance', None)
    position_covariance_type = getattr(msg, 'position_covariance_type', None)
    
    if latitude is None or longitude is None or altitude is None or\
        position_covariance is None or position_covariance_type is None:
        return None
    
    return [
        timestamp,
        latitude,
        longitude,
        altitude,
        position_covariance_type,
        *position_covariance
    ]

def parse_target_rpm(msg, timestamp) -> list:

    target_rpm = getattr(msg, 'data', None)
    if target_rpm is None:
        return None
    
    return [
        timestamp,
        *target_rpm
    ]

def parse_camera_pulse(msg, timestamp) -> list:
    
    id = getattr(msg, 'id', None)
    if id is None:
        return None
    
    return [
        timestamp,
        id
    ]

def parse_pps_pulse(msg, timestamp) -> list:
    id = getattr(msg, 'id', None)
    if id is None:
        return None
    
    return [
        timestamp,
        id
    ]

def parse_ctrl_current(msg, timestamp) -> list:
    
    data = getattr(msg, 'data', None)
    if data is None:
        return None
    
    return [
        timestamp,
        *data
    ]

def parse_rtk_gps(msg, timestamp) -> list:

    latitude = getattr(msg, 'latitude', None)
    longitude = getattr(msg, 'longitude', None)
    altitude = getattr(msg, 'altitude', None)
    position_covariance = getattr(msg, 'position_covariance', None)
    position_covariance_type = getattr(msg, 'position_covariance_type', None)
    
    if latitude is None or longitude is None or altitude is None or\
        position_covariance is None or position_covariance_type is None:
        return None
    
    return [
        timestamp,
        latitude,
        longitude,
        altitude,
        position_covariance_type,
        *position_covariance
    ]