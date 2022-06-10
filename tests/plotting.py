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
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from sklearn import linear_model

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

    # matching_slices = pd.read_csv('/Users/admintmun/Downloads/drive-download-20211122T035114Z-001/plotting_matching_slices.csv', index_col=0)
    matching_slices = pd.read_csv('/Users/admintmun/Downloads/drive-download-20211122T035114Z-001/plotting_matching_slices_same_patients copy.csv', index_col=0)


    distances = pd.read_csv('/Users/admintmun/Downloads/drive-download-20211122T035114Z-001/plotting_distances_for_ct163_vs_mri_slices_v2.csv', index_col=0)

    # reg = linear_model.Ridge(alpha=0.8)
    # reg = linear_model.Ridge(alpha=0.5)
    # reg = linear_model.Ridge(alpha=0.2)
    # reg = linear_model.Lasso(alpha=0.2)

    matching_slices = matching_slices.dropna()
    # reg = linear_model.LinearRegression()
    reg = linear_model.HuberRegressor(epsilon=1)


    x = matching_slices['CT Slice Location'].to_numpy()
    sample_weight = np.ones(len(x)) * 20

    sample_weight[len(x) * 6 // 10:] = 3

    y = matching_slices['Pred MRI Slice Location'].to_numpy()
    # print(matching_slices['Pred MRI Slice Location'])
    # print(matching_slices['CT Slice Location'])
    y_index = matching_slices['Pred MRI Slice Location'].index.to_numpy()
    x = [[index, item] for index, item in enumerate(x)]
    # y = [[index, item] for index, item in enumerate(y)]


    print(x)
    print(y)
    reg.fit(x, y)
    # reg.fit(x, y, sample_weight=sample_weight)

    sm_model = sm.WLS(y, x, weights = 1.0 / (sample_weight **2))
    result = sm_model.fit()

    # print(reg.coef_)
    # print(reg.intercept_)
    pred_y = reg.predict(x)

    pred_y = result.predict(x)
    print(pred_y)
    matching_slices["Fitted Pred MRI Slice Location"] = pred_y
    fig, ax = plt.subplots()
    matching_slices.plot(kind='line', x='CT Slice Location', y=["True MRI Slice Location",
                                                                "Fitted Pred MRI Slice Location"], ax=ax)
    # df_sorted_desc.to_csv("./check.csv")
    # print(matching_slices.dtypes)
    plt.xlabel('CT Slice Locations', size=10)
    plt.ylabel('MRI Slice Location', size=10)
    # plt.title('Predicted vs Actual Matching MRI Slice', size=15)
    # plt.xticks(np.arange(0, 100,20))
    # plt.axhline(x=0.85, color='r', linestyle='-')
    plt.show()

    fig, ax = plt.subplots(1, 2)
    # print(distances.keys())
    # ax = distances.plot(kind='line', x='MRI Slice Locations', y=[
    #                 "Mean Distance"
    #                 # "Sum Distance"
    #                 ],
    #                subplots=False,
    #                sharex=False,
    #                sharey=False,
    #                layout=(1,2),
    #                figsize=(14,8),
    #                # title='Mean/Sum Distances between feature maps of all MRI Slice Location and one CT Slice',
    #                )
    # # df_sorted_desc.to_csv("./check.csv")
    # print(distances.dtypes)
    # plt.xlabel('MRI Slice Locations', size=10)
    # plt.ylabel('Distance', size=10)
    # # plt.title('Predicted vs Actual Matching MRI Slice', size=15)
    # # plt.xticks(np.arange(0, 100,20))
    # print(ax)
    # # ax[0][0].axvline(x=-467, color='r', linestyle='-')
    # ax.axvline(x=-467, color='r', linestyle='-')
    #
    # # ax[0][1].axvline(x=-467, color='r', linestyle='-')
    # plt.show()