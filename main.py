
import numpy as np
import pyautogui as gui
import pyrealsense2 as rs
import argparse
import cv2
import os
from bs import getHand, getFingerTip,getFingerTip1

ub = [[[60, 240,256]]]
lb = [[[3,80,-1]]]

LOAD_BAG = False
# borrowed from internet, load frames (from file or camera) and save as png
def main():
    if not os.path.exists(args.directory):
        os.mkdir(args.directory)
    try:
        config = rs.config()
        if LOAD_BAG:
            rs.config.enable_device_from_file(config, args.input, False)

        pipeline = rs.pipeline()
        # print(dir(rs.stream),dir(rs.format))
        #config.enable_stream(rs.stream.depth, 640, 480, rs.format.y8, 10)
        #config.enable_stream(rs.stream.infrared,1, 640, 480, rs.format.y8, 10) # change second arg between 1, 2 to swtich left and right infrared cam
        # config.enable_stream(rs.stream.color, 480, 360, rs.format.rgb8, 10) # change second arg between 1, 2 to swtich left and right infrared cam
        config.enable_all_streams()
        pipeline.start(config)

        # print(rs.context().devices[0].sensors[0].profiles)
        align_to = rs.stream.color
        alignedFs = rs.align(align_to)
        
        # read frames from either camera or bag file
        i = 0
        pos = [1,1]
        start = 0
        while True:
            print("Saving frame:", i)
            frames = pipeline.wait_for_frames()
            frames = alignedFs.process(frames)

            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            # depth_image = np.asanyarray(depth_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data(), dtype=np.uint8)
            color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            # depth_image = 
            cv2.imwrite(args.directory + "/depth" +str(i).zfill(6) + ".png", depth_image.astype(np.uint8))
            cv2.imwrite(args.directory + "/color" +str(i).zfill(6) + ".png", color_image)
            #if i == 0:
            # print(depth_image[240,320])
            # cv2.rectangle(depth_image, (235,315), (245, 325), (0,255,0), 2)
            a = depth_image.astype(np.uint8)
            # print(np.mean(a))
            # cv2.imshow("IM", depth_image.astype(np.uint8))
            if i > 30 and i%5==4:
                color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
                x = getHand(color_image, ub, lb)
                # print(a.shape)
                finger = getFingerTip1(x,a)
                # print(finger)qq
                if finger[0] > 0 and finger[1] > 0:

                    cv2.circle(color_image,finger,10,(0,0,255))
                    # print(x.sum(),x.shape)
                    
                    # cv2.imshow("IM", x.astype(np.uint8) * 255)
                    cv2.imshow("IM", color_image)
                

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            #cv2.waitKey(0)
            i += 1
            # if i > 60:
            #     break
    except RuntimeError as e:
        print(e)
        print("No more frames arrived, reached end of BAG file!")

    finally:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, help="Path to save the images")
    parser.add_argument("-i", "--input", type=str, help="Bag file to read")
    args = parser.parse_args()

    main()
