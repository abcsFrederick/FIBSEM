# FIBSEM

***CMM requested software infrastructure support from ABCS to develop a run time augmentation system for high resolution FIBSEM imaging. In responding to the CMM request, ABCS proposes a solution as described below:***

A docker container has been designed to run imaging algorithms as needed.  The container  bundles multiple algorithms together with a method to execute the algorithms automatically.  Each algorithm is contained in a single python script file in the repo/ directory.  The container automatically watches for new images in the input directory.  Whenever a new image is added, the selected algorithm (see the taskName below) is run on the image and the output is written to the selected output directory.  

#### Download docker image:
    git clone https://github.com/abcsFrederick/FIBSEM.git

#### Build docker image:
1. Go to 'FIBSEM' directory and export FIBSEM
  ```sh
  export FIBSEM=$PWD
  ```
2. Give an **lowercase** image name:
  ```sh
  export imageName=fibsem
  ```
3. Build image:
  ```sh
  docker build -t $imageName .
  ```
#### Docker run task:
1. Select a module name that exist under **repo** directory
  ```sh
  export taskName=test
  ```
  or
  ```sh
  export taskName=threshold
  ```
  or
  ```sh
  export taskName=inference
  ```
  For test purpose the **test** module will just process an image and output a 128 x 128 thumbnail of it.  The **threshold** algorithm processes single channel SEM images to remove
  background values (replacing the background with black). The **inference** tasks performs forward inferencing using a UNET network to perform segmentation used a pre-trained network. 

2. Run docker image
  ```sh
  docker run --gpus all -id -v $FIBSEM/snapshot:/snapshot \
  -v $FIBSEM/repo:/repo -v $FIBSEM/dataset/input:/input \
  -v $FIBSEM/dataset/output:/output  -e module=$taskName \
  $imageName
  ```
3. Whenever put new image to the **dataset/input** directory, it will automatically generate output image into the **dataset/output** directory.

#### New module rules:
Create python module and put it under **repo** directory, name entry point as a function named **run**.
