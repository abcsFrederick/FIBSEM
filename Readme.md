# FIBSEM

***CMM requested software infrastructure support from ABCS to develop a run time augmentation system for high resolution FIBSEM imaging. In responding to the CMM request, ABCS proposes two solutions as described in this document.***

#### Download docker image:
    https://github.com/abcsFrederick/FIBSEM.git

#### Build docker image:
1. Go to 'FIBSEM' directory and export FIBSEM
  ```sh
  export FIBSEM=$PWD
  ```
3. Give an image name:
  ```sh
  export imageName=test
  ```
4. Build image:
  ```sh
  docker build -t $imageName .
  ```
#### Docker run task:
1. Give an module name that exist under **repo** directory
  ```sh
  export taskName=test
  ```
2. Run docker image
  ```sh
  docker run -it -v $FIBSEM/snapshot:/snapshot \
  -v $FIBSEM/repo:/repo -v $FIBSEM/dataset/input:/input \
  -v $FIBSEM/dataset/output:/output  -e module=$taskName \
  $imageName
  ```
#### New module rules:
Create python module and put it under **repo** directory, name entry point as a function named **run**.