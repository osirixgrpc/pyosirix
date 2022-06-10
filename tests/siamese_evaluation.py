import torch
import os
import pickle
import torchvision
import numpy as np
from torchvision import transforms
import torchvision.datasets as dset
from torchvision import transforms
# from dataset import CT_MRI_Train, CT_MRI_Test
from dataset import CT_MRI_Train

from torch.utils.data import DataLoader
from torch.autograd import Variable
import matplotlib.pyplot as plt
from PIL import Image
from siamese_model import Siamese
import SimpleITK as sitk
from osirix import ViewerController

import grpc
import pytest
import numpy as np
import matplotlib.pyplot as pl
from osirix.osirix_utils import Osirix, OsirixService
from osirix.Exceptions import GrpcException

import osirix.pb2.osirix_pb2 as osirix_pb2
import osirix.pb2.utilities_pb2 as utilities_pb2
import osirix.pb2.types_pb2 as types_pb2
import osirix.pb2.viewercontroller_pb2 as viewercontroller_pb2
import osirix.pb2.vrcontroller_pb2 as vrcontroller_pb2
import osirix.pb2.dcmpix_pb2 as dcmpix_pb2
import osirix.pb2.roi_pb2 as roi_pb2
import osirix.pb2.roivolume_pb2 as roivolume_pb2
import osirix.pb2.osirix_pb2_grpc as osirix_pb2_grpc

#%%

# pwd

#%%

if __name__ == "__main__":
    siamese_nn = Siamese()
    # siamese_nn.double()

    # siamese_nn.load_state_dict(torch.load("//home//timothysumhonmun//models//model-inter-10.pt"), strict=False)
    checkpoint = torch.load("/Users/admintmun/models/model12-8exa-2way-ep5000-lr00005-contrastive-loss-best-86.pt", map_location=torch.device('cpu'))
    # siamese_nn.load_state_dict(torch.load("//home//timothysumhonmun//models//model3-best-19.pt"), strict = True)

    state_dict = checkpoint['model_state_dict']

    # print(state_dict.items())

    # from collections import OrderedDict
    # new_state_dict = OrderedDict()
    # for k, v in state_dict.items():
    #     name = k[7:] # remove 'module.' of dataparallel
    #     new_state_dict[name]=v

    siamese_nn.load_state_dict(state_dict)

    siamese_nn.eval()

    #%%
    port = 50051
    domain = "localhost:"
    # address
    channel_opt = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                   ('grpc.max_receive_message_length', 512 * 1024 * 1024)]

    osirix_service = OsirixService(channel_opt=channel_opt, domain=domain, port=port).get_service()
    osirix = Osirix(osirix_service)
    browser_controller = osirix.current_browser()
    study_series = browser_controller.database_selection()
    study_tuple, series_tuple = study_series
    print("Studies: ", study_tuple)
    print("Series: ", series_tuple)
    study = study_tuple[0]
    series = study.series
    print("Series: " + str(series))
    viewers = osirix.displayed_2d_viewers()
    print(viewers[0].modality)
    print(viewers[1].modality)
    print(viewers[2].modality)

    #%%
    # print(series[10].name)

    mri = viewers[0]
    ct = viewers[1]
    mri_1030 = viewers[2]
    ct.cur_dcm()

    print(mri.title)
    print(mri.idx)
    print(ct.title)
    print(ct.idx)
    mri_dcm_pictures = mri.pix_list(movie_idx=0)
    ct_dcm_pictures = ct.pix_list(movie_idx=0)
    mri_1030_dcm_pictures = mri_1030.pix_list(movie_idx=0)
    # mri_dcm_pictures = tuple(reversed(mri.pix_list(movie_idx=0)))
    # ct_dcm_pictures = tuple(reversed(ct.pix_list(movie_idx=0)))
    # mri_1030_dcm_pictures = tuple(reversed(mri_1030.pix_list(movie_idx=0)))

    print(len(mri_dcm_pictures))
    print(len(ct_dcm_pictures))
    #%% md

    #%%
    # ct_pix = ct_dcm_pictures[162]
    i = 163
    ct_pix = ct_dcm_pictures[i]
    ct_image_np = ct_pix.image
    ct_slice_location = ct_pix.slice_location
    ct_sitk = sitk.GetImageFromArray(ct_pix.image)

    newpath = "./output"
    # img1 = sitk.Cast(sitk.RescaleIntensity(ct_sitk), sitk.sitkUInt8)
    # ct_image_np = sitk.GetArrayFromImage(img1)
    # sitk.WriteImage(img1, os.path.join(newpath, "CT_Matching_Slice_" + str(i) + ".jpg"))
    # img1 = Image.open(
    #     os.path.join(newpath, "CT_Matching_Slice_" + str(i) + ".jpg")).convert('L')


    # ct_image_np = ct_pix.image
    ct_image_tensor = transforms.Resize((105,105))(transforms.ToTensor()(ct_image_np).float()).unsqueeze(0)
    # ct_image_tensor = transforms.Resize((105,105))(transforms.ToTensor()(img1).float()).unsqueeze(0)

    image_distance_tuple_list = []
    most_similar_list = []

    min_distance = 10000
    most_similar_image_pair = ()
    mri_dcm_pictures_indexed = []

    for index, mri_pix in enumerate(mri_dcm_pictures):
        mri_dcm_pictures_indexed.append((index, mri_pix))


    # mri_dcm_pictures = mri_dcm_pictures[33:164]
    mri_dcm_pictures_indexed = mri_dcm_pictures_indexed[33:164]

    # mri_1030_dcm_pictures = mri_1030_dcm_pictures[33:164]
    for index, mri_pix in mri_dcm_pictures_indexed:
        mri_slice_location = mri_pix.slice_location
        print(index)
        print(mri_slice_location)
        mri_image_np = mri_pix.image
        mri_sitk = sitk.GetImageFromArray(mri_image_np)

        # img2 = sitk.Cast(sitk.RescaleIntensity(mri_sitk), sitk.sitkUInt8)
        # mri_image_np = sitk.GetArrayFromImage(img2)
        # sitk.WriteImage(img2, os.path.join(newpath, "MRI_Matching_Slice_" + str(index) + ".jpg"))
        # img2 = Image.open(
        #     os.path.join(newpath, "MRI_Matching_Slice_" + str(index) + ".jpg")).convert('L')


        mri_image_tensor = transforms.Resize((105, 105))(transforms.ToTensor()(mri_image_np).float()).unsqueeze(0)
        # mri_image_tensor = transforms.Resize((105, 105))(transforms.ToTensor()(img2).float()).unsqueeze(0)

        output = siamese_nn.forward(ct_image_tensor, mri_image_tensor)
        output_distance = siamese_nn.forward_distance(ct_image_tensor, mri_image_tensor)
        feature1, feature2 = siamese_nn.forward_features(ct_image_tensor, mri_image_tensor)

        prediction = round(torch.nn.Sigmoid()(output).item(), 2)
        mean_distance = round(torch.mean(output_distance).item(), 2)
        sum_distance = round(torch.sum(output_distance).item(), 2)
        print("Logits :" + str(output.item()))
        # print(torch.mean(output_distance))
        print("Mean distance between features :" + str(torch.mean(output_distance).item()))
        print("Sum distance between features :" + str(torch.sum(output_distance).item()))
        print("")

        image_distance_tuple_list.append(
            (
                mri_image_np,
                mri_image_tensor.squeeze().cpu().numpy(),
                prediction,
                mean_distance,
                sum_distance,
                mri_slice_location,
                ct_slice_location
            )
        )

        if (min_distance > sum_distance):
            min_distance = sum_distance
            most_similar_image_pair = (ct_image_np,
                                       mri_image_np,
                                       mri_image_tensor.squeeze().cpu().numpy(),
                                       mri_slice_location,
                                       ct_slice_location,
                                       index,
                                       prediction,
                                       mean_distance,
                                       sum_distance
                                       )
            most_similar_list.append(most_similar_image_pair)



    print(len(most_similar_list))
    ct_image, most_similar_mri, most_similar_mri_post, mri_slice_location, ct_slice_location, index, prediction, mean_distance, sum_distance = most_similar_image_pair

    # for most_similar_mri_post in most_similar_list:
    #     ct_image, most_similar_mri, most_similar_mri_post, mri_slice_location, ct_slice_location, index, prediction, mean_distance, sum_distance = most_similar_image_pair
    #     print(index)
    #     print("MRI Slice Location : " + str(mri_slice_location))
    #     print("CT Slice Location : " + str(ct_slice_location))
    #     print(mean_distance)
    #     print(sum_distance)
    #     print(index)
    print("MRI Slice Location : " + str(mri_slice_location))
    print("CT Slice Location : " + str(ct_slice_location))
    print(mean_distance)
    print(sum_distance)
    fig = plt.figure(figsize = (10,8))
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.imshow(ct_image,
    #            aspect=6.711409396,
    #            origin='lower',
              cmap="gray")
    # ax1.set_title("Prediction : " + str(prediction.item()))

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.imshow(most_similar_mri,
    #            aspect=6.711409396,
    #            origin='lower',
              cmap="gray")

    # print(most_similar_mri.astype(float).flatten().tolist())
    mri.idx = index
    ct.idx = i
    # ax2.set_title("Prediction : " + str(prediction.item()))
    # print(output)
    # plt.title("Sum Distance :" + str(sum_distance) + ", Mean Distance :" + str(mean_distance) + ", Pred :" + str(prediction) + ", Slice Location :" + str(slice_location))


    plt.show()



    # ct_image_tensor = transforms.Resize((105,105))(transforms.ConvertImageDtype(torch.double)(transforms.ToTensor()(ct_image_np))).unsqueeze(0)
    # ct_image_tensor = ct_image_tensor.astype(torch.float32)
    # print(ct_image_tensor.dtype)
    # mri_image_np = mri_pix.image
    # mri_image_tensor = transforms.Resize((105,105))(transforms.ToTensor()(mri_image_np).float()).unsqueeze(0)
    # print(mri_image_tensor.dtype)
    # # mri_image_tensor = mri_image_tensor.astype(torch.float32)
    # # mri_image_tensor = transforms.Resize((105,105))(transforms.ConvertImageDtype(torch.double)(transforms.ToTensor()(mri_image_np))).unsqueeze(0)
    #
    # # print(ct_image_np.shape)
    # # plt.imshow(ct_image_np, cmap='gray')
    # # siamese_nn = siamese_nn.float()
    # output = siamese_nn.forward(ct_image_tensor, mri_image_tensor)
    # output_distance = siamese_nn.forward_distance(ct_image_tensor, mri_image_tensor)
    # feature1, feature2 = siamese_nn.forward_features(ct_image_tensor, mri_image_tensor)
    #
    # prediction = round(torch.nn.Sigmoid()(output).item(), 2)
    # mean_distance = round(torch.mean(output_distance).item(), 2)
    # sum_distance = round(torch.sum(output_distance).item(), 2)
    # print("Logits :"  + str(output.item()))
    # # print(torch.mean(output_distance))
    # print("Mean distance between features :" + str(torch.mean(output_distance).item()))
    # print("Sum distance between features :" + str(torch.sum(output_distance).item()))
    #
    # # prediction = F.softmax(output, dim=1)
    # # prediction = torch.softmax(output, 1)
    # # prediction = torch.nn.Sigmoid()(output)
    #
    # # print("Sigmoid Predictions :" + str(prediction.item()))
    #
    # fig = plt.figure(figsize = (10,8))
    # ax1 = fig.add_subplot(1, 2, 1)
    # ax1.imshow(ct_image_tensor.squeeze().cpu().numpy(),
    # #            aspect=6.711409396,
    # #            origin='lower',
    #           cmap=plt.cm.Greys_r)
    # # ax1.set_title("Prediction : " + str(prediction.item()))
    #
    # ax2 = fig.add_subplot(1, 2, 2)
    # ax2.imshow(mri_image_tensor.squeeze().cpu().numpy(),
    # #            aspect=6.711409396,
    # #            origin='lower',
    #           cmap=plt.cm.Greys_r)
    # # ax2.set_title("Prediction : " + str(prediction.item()))
    # print(output)
    # plt.title("Sum Distance :" + str(sum_distance) + ", Mean Distance :" + str(mean_distance) + ", Pred :" + str(prediction))
    #
    # plt.show()
