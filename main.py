
import numpy as np
import pyautogui as gui
import pyrealsense2 as rs
import argparse
import cv2
import os
from bs import getHand, getFingerTip,getFingerTip1, getBackground, backgroundSubtraction

ub = [[[19, 240,256]]]
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
        history = np.zeros((20,2),dtype=np.int32)
        coord = np.array([1,1])
        bg = None
        bg_std = None
        depth_history = None # average depth for latest 3 frames before a frame gets displayed 
        # labels = np.array((20))
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
            # cv2.imwrite(args.directory + "/depth" +str(i).zfill(6) + ".png", depth_image.astype(np.uint8))
            # cv2.imwrite(args.directory + "/color" +str(i).zfill(6) + ".png", color_image)


            depth = depth_image.astype(np.uint8)
            color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)


            # build background model
            if i == 0:
                H,W,C = color_image.shape
                imgs = np.zeros((10,H,W,C))
                depth_history = np.zeros(depth.shape)
                
            
            elif i > 10 and i < 20:
                imgs[i-11,:,:,:] = color_image
                
            elif i == 20:
                imgs[i-11,:,:,:] = color_image
                bg, bg_std = getBackground(imgs)
            elif i > 20 and i < 40:
                # stable match
                # color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

                x = getHand(color_image, ub, lb)
                # print(a.shape)
                r,c = getFingerTip1(x,depth)
                history[i-21,:] = np.array([r,c])
            elif i == 40:
                # find stable match
                print('match')
                change = (history[0:18,:] - history[1:19,:]).sum(axis=1)
                prev_sum = np.array([0, 0],dtype=np.int32)
                prev = 0
                cur_sum = np.array([0, 0],dtype=np.int32)
                cur = 0
                for j in range(18):
                    if change[j] <= 10:
                        cur_sum += history[j,:]
                        cur += 1

                    else: 
                        if cur > prev:
                            prev = cur
                            prev_sum = cur_sum
                        
                        cur = 0
                        cur_sum = np.array([0, 0],dtype=np.int32)

                coord = prev_sum / prev
                r = coord[0]
                c = coord[1]

            elif i > 40 and i%5==4:
                
                depth_history = ((depth_history +depth) / 3).astype(np.uint8) # average depth
                
                
                x = getHand(color_image, ub, lb, prev=coord)
                # print(a.shape)
                r,c = getFingerTip1(x,depth_history, prev=coord)
                # print(finger)qq
                if r > 0 and c > 0:
                    color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)
                    cv2.circle(color_image,(c,r),10,(0,0,255))
                    # print(x.sum(),x.shape)
                    
                    # cv2.imshow("IM", x.astype(np.uint8) * 255)
                    cv2.imshow("IM", color_image)
                    # cv2.imwrite(args.directory + "/result" +str(i).zfill(6) + ".png", color_image.astype(np.uint8))
                

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                depth_history[:,:] = 0 # clear avg depth

            elif i > 40 and i%3!=2:
                # sum up depth frame in consecutinve frames and take average
                depth_history += cv2.GaussianBlur(depth,(3,3),0)

            #cv2.waitKey(0)
            i += 1
            # if i >= 80:
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
