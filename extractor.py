import os
import cv2
import rosbag
import argparse
import pandas as pd
from cv_bridge import CvBridge
from tqdm import tqdm

from misc import (
    parse_imu,
    parse_motor,
    parse_gps,
    parse_target_rpm,
    parse_camera_pulse,
    parse_ctrl_current,
    parse_rtk_gps
)

ROOT_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "VID_dataset")

# TODO: When including indoor data, add ground truth topic

topic_map = {
    '/camera/depth/image_rect_raw': 'depth/rectified/', 
    '/camera/infra1/image_rect_raw': 'infrared/rectified_left/',
    '/camera/infra2/image_rect_raw': 'infrared/rectified_right/',
    '/djiros/imu_hwts': 'imu/', 
    # '/djiros/pulse': 'pps_pulse/',
    # '/m100withm3508/cap_n3pps': 'cap_n3pps/',
    '/m100withm3508/cap_camerapulse': 'cap_camerapulse/',
    '/m100withm3508/target_rpm': 'target_motor_speed/',
    '/m100withm3508/ctrl_current': 'target_motor_current/',
    '/m100withm3508/m3508_m1': 'motor_speed/motor1/',
    '/m100withm3508/m3508_m2': 'motor_speed/motor2/',
    '/m100withm3508/m3508_m3': 'motor_speed/motor3/',
    '/m100withm3508/m3508_m4': 'motor_speed/motor4/',
    '/djiros/gps': 'gps/',
    '/rtk_zhd_parser/GPS': 'rtk_gps/',
    # '/vicon/m100/m100': 'ground_truth/',
}

topic_to_header = {
    '/djiros/imu_hwts': ['timestamp', 'ax', 'ay', 'az', 'wx', 'wy', 'wz', 'qw', 'qx', 'qy', 'qz', 'linear_acceleration_covariance_0', 'linear_acceleration_covariance_1', 'linear_acceleration_covariance_2', 'linear_acceleration_covariance_3', 'linear_acceleration_covariance_4', 'linear_acceleration_covariance_5', 'linear_acceleration_covariance_6', 'linear_acceleration_covariance_7', 'linear_acceleration_covariance_8', 
    'angular_velocity_covariance_0', 'angular_velocity_covariance_1', 
    'angular_velocity_covariance_2', 'angular_velocity_covariance_3', 
    'angular_velocity_covariance_4', 'angular_velocity_covariance_5', 
    'angular_velocity_covariance_6', 'angular_velocity_covariance_7', 
    'angular_velocity_covariance_8', 
    'orientation_covariance_0', 'orientation_covariance_1', 
    'orientation_covariance_2', 'orientation_covariance_3', 
    'orientation_covariance_4', 'orientation_covariance_5', 
    'orientation_covariance_6', 'orientation_covariance_7', 
    'orientation_covariance_8'],
    '/m100withm3508/m3508_m1': ['timestamp', 'id', 'rpm', 'current'],
    '/m100withm3508/m3508_m2': ['timestamp', 'id', 'rpm', 'current'],
    '/m100withm3508/m3508_m3': ['timestamp', 'id', 'rpm', 'current'],
    '/m100withm3508/m3508_m4': ['timestamp', 'id', 'rpm', 'current'],
    '/djiros/gps': ['timestamp', 'latitude', 'longitude', 'altitude', 'position_covariance_type',
        'position_covariance_0', 'position_covariance_1', 'position_covariance_2',
        'position_covariance_3', 'position_covariance_4', 'position_covariance_5',
        'position_covariance_6', 'position_covariance_7', 'position_covariance_8'],
    '/m100withm3508/target_rpm': ['timestamp', 'target_rpm_0', 'target_rpm_1', 'target_rpm_2', 'target_rpm_3'],
    '/m100withm3508/cap_camerapulse': ['timestamp', 'id'],
    '/m100withm3508/ctrl_current': ['timestamp', 'current_0', 'current_1', 'current_2', 'current_3'],
    '/rtk_zhd_parser/GPS': ['timestamp', 'latitude', 'longitude', 'altitude', 'position_covariance_type',
        'position_covariance_0', 'position_covariance_1', 'position_covariance_2',
        'position_covariance_3', 'position_covariance_4', 'position_covariance_5',
        'position_covariance_6', 'position_covariance_7', 'position_covariance_8'],
}

topic_to_parser = {
    '/djiros/imu_hwts': parse_imu,
    '/m100withm3508/m3508_m1': parse_motor,
    '/m100withm3508/m3508_m2': parse_motor,
    '/m100withm3508/m3508_m3': parse_motor,
    '/m100withm3508/m3508_m4': parse_motor,
    '/djiros/gps': parse_gps,
    '/m100withm3508/target_rpm': parse_target_rpm,
    '/m100withm3508/cap_camerapulse': parse_camera_pulse,
    '/m100withm3508/ctrl_current': parse_ctrl_current,
    '/rtk_zhd_parser/GPS': parse_rtk_gps,
}

image_topics = ['/camera/depth/image_rect_raw', '/camera/infra1/image_rect_raw', '/camera/infra2/image_rect_raw']
csv_topics = [topic for topic in topic_map.keys() if topic not in image_topics]
bridge = CvBridge()

def parse_args():
    parser = argparse.ArgumentParser(description="Extract data from ROS bag files.")
    parser.add_argument('-f', '--bag_file', type=str, default='all', help='Path to the ROS bag file.')
    return parser.parse_args()



def extract(input_file: str, output_dir: str):

    # === CSV Extraction ===
    csv_data = {topic: [] for topic in csv_topics}

    print("[*] Reading bag file...")
    with rosbag.Bag(input_file, 'r') as bag:
        for i, (topic, msg, t) in tqdm(enumerate(bag.read_messages())):
            timestamp = t.to_nsec()
            if topic in image_topics:
                # === Image Extraction ===
                try:
                    desired_image_encodings = 'passthrough' if topic == '/camera/depth/image_rect_raw' else 'bgr8'
                    cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding=desired_image_encodings)
                    filename = os.path.join(output_dir, topic_map.get(topic), f"{timestamp}.png")
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    cv2.imwrite(filename, cv_img)
                except Exception as e:
                    print(f"Image conversion error on {topic}: {e}")

            elif topic in csv_topics:
                
                data = topic_to_parser.get(topic, lambda x, y: None)(msg, timestamp)
                if data is None:
                    print(f"Skipping topic {topic} due to missing data.")
                    continue
                csv_data[topic].append(data)

    # === Save CSVs ===
    for topic, rows in csv_data.items():
        print(f"[+] Saving CSV for topic: {topic} with {len(rows)} rows.")
        df = pd.DataFrame(rows, columns=topic_to_header.get(topic, []))
        csv_filename = os.path.join(output_dir, topic_map.get(topic), 'data.csv')
        os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
        df.to_csv(csv_filename, index=False)
        print(f"[+] Saved CSV for {topic} → {csv_filename}")


if __name__ == "__main__":
    args = parse_args()

    bag_files = []
    if args.bag_file == 'all':
        # walk through the raw_bag_files directory and find all bag files
        for root, dirs, files in os.walk(os.path.join(ROOT_DATA_DIR, 'raw_bag_files')):
            for file in files:
                if file.endswith('.bag'):
                    bag_files.append(os.path.join(root, file))
    else:
        if os.path.exists(args.bag_file):
            bag_files.append(args.bag_file)
    
    if len(bag_files) == 0:
        raise ValueError("No bag files found in 'raw_bag_files' directory. Please check the directory structure.")
    
    output_dirs = []
    for bag_file_path in bag_files:
        print(f"Processing bag file: {bag_file_path}")
        output_dir = os.path.join(ROOT_DATA_DIR, "extracted_data", os.path.splitext(os.path.basename(bag_file_path))[0])
        # output_dir = os.path.join(ROOT_DATA_DIR, "extracted_data", 'test_parsed')
        os.makedirs(output_dir, exist_ok=True)
        output_dirs.append(output_dir)

    for bag_file, output_dir in zip(bag_files, output_dirs):
        print(f"Extracting data from {bag_file} to {output_dir}...")
        extract(bag_file, output_dir)
        print(f"Extraction completed for {bag_file}. Data saved to {output_dir}.")