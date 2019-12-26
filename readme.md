
# Real-time point finger direstion tracking (finger as pointer)


## Requirements
Python==3.6
Install intel realsense SDK version 2, we will use api from it for development
Install packages in `requirements.txt`

## Usage
`python main.py -d=out -i=data/1.bag` if use with .bag video file
Otherwise plug in realsense D435 camera and run `python main.py -d=out`
setup cython file: `python setup.py build_ext --inplace`
