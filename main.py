import numpy as np
import pyautogui as gui
import pyrealsense2 as rs
import argparse
import cv2
import os

LOAD_BAG = True
# borrowed from internet, load frames (from file or camera) and save as png
def main():
    if not os.path.exists(args.directory):
        os.mkdir(args.directory)
    try:
        config = rs.config()
        if LOAD_BAG:
            rs.config.enable_device_from_file(config, args.input, False)

        pipeline = rs.pipeline()

        config.enable_stream(rs.stream.infrared,1, 640, 480, rs.format.y8, 30) # change second arg between 1, 2 to swtich left and right infrared cam

        pipeline.start(config)

        # print(rs.context().devices[0].sensors[0].profiles)
        
        # read frames from either camera or bag file
        i = 0
        while True:
            print("Saving frame:", i)
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_infrared_frame()
            depth_image = np.asanyarray(depth_frame.get_data())
            cv2.imwrite(args.directory + "/" +str(i).zfill(6) + ".png", depth_image)
            i += 5
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