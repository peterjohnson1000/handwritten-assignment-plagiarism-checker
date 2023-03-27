import argparse
from typing import List

import os
import cv2
import matplotlib.pyplot as plt 
from path import Path
from matplotlib import pyplot as plt 
from matplotlib import pyplot as plt1
import time
import uuid


from word_detector import detect, prepare_img, sort_multiline

import numpy as np
from PIL import Image as im


#########################
import subprocess

# define the path to the code 2 script
path_to_script = "src/main.py"

# define the argument to pass to the script
#image_file = "../image_paths/faizameer.txt"
image_file = "./image_paths"



#########################

list_image_names_serial = []

def get_img_files(data_dir: Path) -> List[Path]:
    """Return all image files contained in a folder."""
    res = []
    for ext in ['*.png', '*.jpg', '*.bmp']:
        res += Path(data_dir).files(ext)
    return res

parser = argparse.ArgumentParser()
#parser.add_argument('--data', type=Path, default=Path('data/page'))
parser.add_argument('--data', type=Path, default=Path('assignment_input'))
parser.add_argument('--kernel_size', type=int, default=25)
parser.add_argument('--sigma', type=float, default=11)
parser.add_argument('--theta', type=float, default=5)
parser.add_argument('--min_area', type=int, default=100)
parser.add_argument('--img_height', type=int, default=1000)
parsed = parser.parse_args()

segmented_images = 'segmented_images'
image_paths = 'image_paths'

def save_image_name_to_text_file():

    # Get all image files in the data directory
    data_dir = parsed.data
    image_files = get_img_files(data_dir)
    print(image_files)

    for i, fn_img in enumerate(image_files):
        list_image_names_serial.clear()
        # save_dir = parsed.data / 'output_images' + str(uuid.uuid4())[:8]

        # save_dir = parsed.data / 'output_images ' + fn_img.stem
        # save_dir.mkdir()
        # print(save_dir) assignment_input/output_images peterjohnson

        save_dir = os.path.join(segmented_images, 'output_images ' + fn_img.stem)
        os.mkdir(save_dir)
        # print(save_dir) segmented_images/output_images peterjohnson

        # print(fn_img)
        # print(f'Processing file {fn_img}')

        # load image and process it
        img = prepare_img(cv2.imread(fn_img), parsed.img_height)
        detections = detect(img,
                            kernel_size=parsed.kernel_size,
                            sigma=parsed.sigma,
                            theta=parsed.theta,
                            min_area=parsed.min_area)

        # sort detections: cluster into lines, then sort each line
        lines = sort_multiline(detections)

        # plot results
        plt.imshow(img, cmap='gray')
        num_colors = 7
        colors = plt.cm.get_cmap('rainbow', num_colors)
        
        # generate a unique file name using a timestamp and a unique identifier
        #filename = time.strftime("img_names_sequence_%Y%m%d%H%M%S_") + str(uuid.uuid4())[:8] + ".txt"
        filename = fn_img.stem + ".txt"

        for line_idx, line in enumerate(lines):
            for word_idx, det in enumerate(line):
                xs = [det.bbox.x, det.bbox.x, det.bbox.x + det.bbox.w, det.bbox.x + det.bbox.w, det.bbox.x]
                ys = [det.bbox.y, det.bbox.y + det.bbox.h, det.bbox.y + det.bbox.h, det.bbox.y, det.bbox.y]
                plt.plot(xs, ys, c=colors(line_idx % num_colors))
                plt.text(det.bbox.x, det.bbox.y, f'{line_idx}/{word_idx}')

                xs = [det.bbox.x, det.bbox.x, det.bbox.x + det.bbox.w, det.bbox.x + det.bbox.w, det. bbox.x]
                ys = [det.bbox.y, det.bbox.y + det.bbox.h, det.bbox.y + det.bbox.h, det.bbox.y, det.bbox.y]
                
                plt.plot(xs, ys, c=colors (line_idx % num_colors)) 
                plt.text(det.bbox.x, det.bbox.y, f'{line_idx}/{word_idx}') 
                # print(det.bbox.x, det.bbox.y, det.bbox.w, det.bbox.h)
                
                crop_img = img[det.bbox.y:det.bbox.y+det.bbox.h,det.bbox.x:det.bbox.x+det.bbox.w]
                
                #cv2.imwrite("line"+str(line_idx) +"word"+str(word_idx)+".jpg" , crop_img)
                
                # specify path to save image in the new directory
                # img_path = save_dir / f'line{line_idx}_word{word_idx}.jpg'
                img_path = os.path.join(save_dir, f'line{line_idx}_word{word_idx}.jpg')
                cv2.imwrite(str(img_path), crop_img)

                # add path to list of image names
                #full_img_path = os.path.relpath(img_path, start=parsed.data)
                full_img_path = os.path.relpath(img_path, start=parsed.data)
                # list_image_names_serial.append(full_img_path)
                list_image_names_serial.append(full_img_path[1:])

                # full_img_path = "data/mydataset/line"+str(line_idx)+"word"+str(word_idx)+".jpg" 
                # list_image_names_serial.append(full_img_path)
                
                # print(list_image_names_serial)

                llist_image_names_serial_set = set(list_image_names_serial)

                # specify path to save text file in the new directory
                # textfile_path = save_dir / (filename)
                textfile_path = os.path.join(image_paths, filename)

                # # open the new file in write mode
                # with open(filename, 'w') as textfile:
                #     # write each element to the file
                #     for element in list_image_names_serial:
                #         textfile.write(element + "\n")
                # open the new file in write mode
                with open(str(textfile_path), 'w') as textfile:
                    # write each element to the file
                    for element in list_image_names_serial:
                        textfile.write(element + "\n")
                # list_image_names_serial.clear()

    # plt.show()

save_image_name_to_text_file()

# call the script with the argument using subprocess
subprocess.call(["/usr/local/bin/python3", path_to_script, "--img_file", image_file])
# time.sleep(2)
# subprocess.call(["python3", "plagiarismChecker.py"])
