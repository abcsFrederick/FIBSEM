# FIBSEM

##### Summary:
CMM requested software infrastructure support from ABCS to develop a run time augmentation system for high resolution FIBSEM imaging. In responding to the CMM request, ABCS proposes two solutions as described in this document.

###### Build docker image:
docker build -t $imageName .

###### Docker run task:
docker run -it -v $PWD/snapshot:/snapshot -v $PWD/repo:/repo -v $PWD/dataset/input:/input -v $PWD/dataset/output:/output  -e module=$taskName $imageName 



python script.py -m test -i ./dataset/input -o ./dataset/output ./