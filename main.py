import numpy as np
import pyautogui as gui
import pyrealsense2 as rs
import argparse
import cv2
import os

LOAD_BAG = False
# borrowed from internet, load frames (from file or camera) and save as png
def main():
    if not os.path.exists(args.directory):
        os.mkdir(args.directory)
    try:
        config = rs.config()
        if LOAD_BAG:
            rs.config.enable_device_from_file(config, args.input, False)
            print(1)
        pipeline = rs.pipeline()
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        print(3)
        pipeline.start(config)
        print(2)
        i = 0
        while True:
            print("Saving frame:", i)
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            depth_image = np.asanyarray(depth_frame.get_data())
            cv2.imwrite(args.directory + "/" + str(i).zfill(6) + ".png", depth_image)
            i += 1
            if i > 60:
                break
    except RuntimeError:
        print("No more frames arrived, reached end of BAG file!")

    finally:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, help="Path to save the images")
    parser.add_argument("-i", "--input", type=str, help="Bag file to read")
    args = parser.parse_args()

    main()