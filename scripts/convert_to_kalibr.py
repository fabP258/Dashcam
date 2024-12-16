"""
Converter script for Kalibr `bagcreator`
"""

# ref. https://github.com/ethz-asl/kalibr/wiki/bag-format

import cv2
from pathlib import Path

folder_path = Path(
    "/home/fabio/Data/Dashcam/HW2/Multicam_YUV/Calibration/20241214_14_06_37"
)


def extract_images_from_video(
    video_path: Path, timestamp_file_path: Path, cam_idx: int
):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError

    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()

    frame_timestamps_ns = []
    with open(timestamp_file_path, "r") as f:
        for line in f:
            line = line.replace("\n", "")
            ts_ms = float(line)
            frame_timestamps_ns.append(int(ts_ms * 1e6))

    if len(frames) != len(frame_timestamps_ns):
        raise RuntimeError("Number of frames should equal number of timestamps.")

    output_path = video_path.parent / "kalibr" / f"cam{cam_idx}"
    output_path.mkdir(parents=True, exist_ok=True)
    for frame, timestamp in zip(frames, frame_timestamps_ns):
        file_name = output_path / f"{timestamp:010d}.png"
        cv2.imwrite(file_name, frame)


def extract_imu_data(imu_data_path: Path):
    with open(imu_data_path, "r") as f:
        out_data = []
        for i, line in enumerate(f):
            if i == 0:
                continue
            line = line.replace("\n", "")
            splitted_line = line.split(",")
            new_line = f"{int(float(splitted_line[0]) * 1e9):010d}" + ","

            # add gyro data
            new_line += splitted_line[4] + ","
            new_line += splitted_line[5] + ","
            new_line += splitted_line[6] + ","

            # add accel data
            new_line += splitted_line[1] + ","
            new_line += splitted_line[2] + ","
            new_line += splitted_line[3]

            out_data.append(new_line)

    output_path = imu_data_path.parent / "kalibr"
    output_path.mkdir(parents=True, exist_ok=True)
    with open(output_path / "imu0.csv", "w") as f:
        header = "timestamp,omega_x,omega_y,omega_z,alpha_x,alpha_y,alpha_z\n"
        f.write(header)
        for line in out_data:
            f.write(line + "\n")


extract_images_from_video(
    folder_path / "imx708.h264", folder_path / "imx708_timestamps.txt", 0
)
extract_images_from_video(
    folder_path / "imx708_wide.h264", folder_path / "imx708_wide_timestamps.txt", 1
)
extract_imu_data(folder_path / "imu_data.txt")
