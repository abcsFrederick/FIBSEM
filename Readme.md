# FIBSEM

***CMM requested software infrastructure support from ABCS to develop a run time augmentation system for high resolution FIBSEM imaging. In responding to the CMM request, ABCS proposes two solutions as described in this document.***

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
1. Give an module name that exist under **repo** directory
  ```sh
  export taskName=test
  ```
  For test purpose the **test** module will just process an image and output a 128 x 128 thumbnail of it.

2. Run docker image
  ```sh
  docker run -id -v $FIBSEM/snapshot:/snapshot \
  -v $FIBSEM/repo:/repo -v $FIBSEM/dataset/input:/input \
  -v $FIBSEM/dataset/output:/output  -e module=$taskName \
  $imageName
  ```
3. Whenever put new image to the **dataset/input** directory, it will automatically generate output image into the **dataset/output** directory.

#### New module rules:
Create python module and put it under **repo** directory, name entry point as a function named **run**.