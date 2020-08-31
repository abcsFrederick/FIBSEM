import os
from PIL import Image

import torch
import numpy as np
import torch
import monai
from monai.transforms import \
    Compose, LoadPNGd, AddChanneld,AsChannelFirstd, ScaleIntensityRanged, \
    ToTensord, ScaleIntensityd, CastToTyped, Resized
from monai.networks.layers import Norm



def run(file, inputMount, outputMount):
  inputPath = os.path.join(inputMount, file.split('/')[-1])
  outputPath = os.path.join(outputMount, file.split('/')[-1])
  print("attempting to infer cell clusters")
  try:

    # open the image only to find its size
    with Image.open(inputPath) as input_img:
        input_bbox = input_img.getbbox()
        input_width = input_bbox[2]-input_bbox[0]
        input_height = input_bbox[3]-input_bbox[1]
        #print('input image size:',input_width,input_height)

    # instantiate the model
    # standard PyTorch program style: create UNet, DiceLoss and Adam optimizer
    #print('checking for cuda device')
    device = torch.device('cuda:0')
    model = monai.networks.nets.UNet(dimensions=2, in_channels=3, out_channels=2, channels=(16, 32, 64, 128, 256),
                                     strides=(2, 2, 2, 2), num_res_units=2, norm=Norm.BATCH).to(device)

    print('attempting load of pretrained network from /tmp directory')
    # read in the pretrained model
    model.load_state_dict(torch.load('/tmp/unet_368x368_segment_model.pth'))
    #print('loading complete')
    model.eval()
    NETWORK_IMAGE_SIZE=368

    # define xforms in MONAI to prepare imagery for PyTorch inferencing
    infer_transforms = Compose([
        LoadPNGd(keys=['image']),
        AsChannelFirstd(keys=['image']),
        Resized(keys=['image'],spatial_size=(NETWORK_IMAGE_SIZE,NETWORK_IMAGE_SIZE),mode='bilinear',align_corners=False),
        CastToTyped(keys=['image'],dtype='float32'),
        ScaleIntensityd(keys=['image'], minv=0.0, maxv=1.0),
        ToTensord(keys=['image'])
    ])

    # create and load a Monai dataset composed of the single image, because the transforms 
    # are performed automatically in MONAI. A spec for the image is needed by the Dataset definition
    infer_files = [{'image': inputPath}]
    infer_ds = monai.data.Dataset(infer_files, transform=infer_transforms)
    infer_loader = monai.data.DataLoader(infer_ds, batch_size=1)

    # get the transformed single image out of the dataset
    input_data = monai.utils.misc.first(infer_loader)

    # move the tensor to the GPU
    input_tensor= input_data['image'].to(device)

    # run the forward prediction
    predict_tensor = model(input_tensor)
    #print('inference complete. preparing output')

    # get the result back from the GPU and drop the first dimension
    infer_array = predict_tensor.detach().cpu().squeeze()

    # rearrange to num channels last and make it a single channel binary image
    pred_array = torch.argmax(np.transpose(infer_array,(1,2,0)),dim=2)

    # convert type back from torch to numpy
    prediction = pred_array.numpy()

    # write the file out in a viewable way, the output image is resized to match the
    # input image size for convenience, even though inferencing is always done at the 
    # size of the pretrained network
    outimg = Image.fromarray(prediction.astype('uint8')*255)
    resized = outimg.resize((input_width,input_height))
    print('saving segmentation to:',outputPath)
    resized.save(outputPath)
    
  except OSError:
      print("cannot create inference image for", file)
