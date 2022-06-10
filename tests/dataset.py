import glob

import torch
from torch.utils.data import Dataset, DataLoader
import os
from numpy.random import choice as npc
import numpy as np
import time
import random
import torchvision.datasets as dset
from PIL import Image
import logger

class CT_MRI_Train(Dataset):

    def __init__(self, dataPath, transform=None, train=True):
        super(CT_MRI_Train, self).__init__()
        # np.random.seed(0)
        # self.dataset = dataset
        self.transform = transform
        self.imagePairs, self.imagePairsLabel, self.imagePairsPaths = self.loadToMem(dataPath, train)
        # self.train = train

    def loadToMem(self, dataPath, train):
        random.seed(42) # ensure pairs are created are reproducible

        patientPathsList = []

        # Create matching pairs
        imagePairs = []
        imagePairsLabel = []
        imagePairsPaths = []
        # print(dataPath)
        ctSlicesPathList = []
        mriSlicesPathList = []
        if(train == True):
            # for patient_dirs in os.listdir(dataPath):
            #     print("Directories :" + patient_dirs)
            #     patient_paths = os.path.join(dataPath, patient_dirs)
            #     patientPathsList.append(patient_paths)
            #
            #     if (patient_dirs != ".DS_Store" and os.path.isdir(patient_paths)):
            label = 1
            patient_paths = "/home/timothysumhonmun/data/Matching_Slices_Same_Patient_three_z_points_jpg_plt/Lymphoma_1031"
            for slices in os.listdir(patient_paths):
                # print(slices)
                print("begin loading training dataset to memory")
                slices_path = os.path.join(patient_paths, slices)

                similar_CT_MR_image = []
                similar_CT_MR_paths = []
                if(slices != ".DS_Store" and os.path.isdir(slices_path)):
                    for images in os.listdir(slices_path):
                        try:
                            imagePath = os.path.join(slices_path, images)
                            image = Image.open(imagePath).convert('L')
                            image.verify()
                            # print(image)
                            # similar_CT_MR_image[images] = image

                            similar_CT_MR_image.append(image)
                            similar_CT_MR_paths.append(imagePath)
                            if ("CT" in images):
                                ctSlicesPathList.append(imagePath)
                            if ("MRI" in images):
                                mriSlicesPathList.append(imagePath)
                        except(IOError, SyntaxError):
                            print("Image is empty :" + image)


                    imagePairs.append(similar_CT_MR_image)
                    imagePairsLabel.append(label)
                    imagePairsPaths.append(similar_CT_MR_paths)

            # Creating CT-CT matching pair
            for slices in os.listdir(patient_paths):
                # print(slices)
                slices_path = os.path.join(patient_paths, slices)

                similar_CT_CT_image = []
                similar_CT_CT_paths = []
                if(slices != ".DS_Store" and os.path.isdir(slices_path)):
                    for images in os.listdir(slices_path):
                        try:
                            # print(image)
                            # similar_CT_MR_image[images] = image

                            if ("CT" in images):
                                # ctSlicesPathList.append(imagePath)
                                imagePath = os.path.join(slices_path, images)
                                image = Image.open(imagePath).convert('L')
                                # print(np.array(image).dtype)
                                image.verify()
                                similar_CT_CT_image.append(image)
                                similar_CT_CT_image.append(image)
                                similar_CT_CT_paths.append(imagePath)
                                similar_CT_CT_paths.append(imagePath)
                        except(IOError, SyntaxError):
                            print("Image is empty :" + image)


                    imagePairs.append(similar_CT_CT_image)
                    imagePairsLabel.append(label)
                    imagePairsPaths.append(similar_CT_CT_paths)

            # create negative pairs
            label = 0
            for i in range(0, 100):
                index = random.randint(0, len(ctSlicesPathList) - 1)
                negative_match_index = random.randint(0, len(mriSlicesPathList) - 1)
                while (index == negative_match_index):
                    negative_match_index = random.randint(0, len(mriSlicesPathList) - 1)
                ct_path = ctSlicesPathList[index]

                mri_path = mriSlicesPathList[negative_match_index]
                print("Neg CT Path " + ct_path)
                print("Neg MRI Path " + mri_path)
                diffImage1 = Image.open(os.path.join(ct_path)).convert('L')
                diffImage2 = Image.open(os.path.join(mri_path)).convert('L')
                imagePairs.append([diffImage1, diffImage2])
                imagePairsLabel.append(label)
                imagePairsPaths.append([ct_path, mri_path])

        else:
            # for patient_dirs in os.listdir(dataPath):
            #     print("Directories :" + patient_dirs)
            #     patient_paths = os.path.join(dataPath, patient_dirs)
            #     patientPathsList.append(patient_paths)
            #     if (patient_dirs != ".DS_Store" and os.path.isdir(patient_paths)):
            patient_paths = "/home/timothysumhonmun/data/Matching_Slices_Same_Patient_three_z_points_jpg_plt/Lymphoma_1030"
            label = 1
            for slices in os.listdir(patient_paths):
                # print(slices)
                slices_path = os.path.join(patient_paths, slices)

                similar_CT_MR_image = []
                similar_CT_MR_paths = []
                if (slices != ".DS_Store" and os.path.isdir(slices_path)):
                    for images in os.listdir(slices_path):
                        try:
                            imagePath = os.path.join(slices_path, images)
                            image = Image.open(imagePath).convert('L')
                            image.verify()
                            # print(image)
                            # similar_CT_MR_image[images] = image
                            similar_CT_MR_image.append(image)
                            similar_CT_MR_paths.append(imagePath)
                            if ("CT" in images):
                                ctSlicesPathList.append(imagePath)
                            if ("MRI" in images):
                                mriSlicesPathList.append(imagePath)
                        except(IOError, SyntaxError):
                            print("Image is empty :" + image)

                    imagePairs.append(similar_CT_MR_image)
                    imagePairsLabel.append(label)
                    imagePairsPaths.append(similar_CT_MR_paths)


            # Creating CT-CT matching pair
            for slices in os.listdir(patient_paths):
                # print(slices)
                slices_path = os.path.join(patient_paths, slices)

                similar_CT_CT_image = []
                similar_CT_CT_paths = []
                if (slices != ".DS_Store" and os.path.isdir(slices_path)):
                    for images in os.listdir(slices_path):
                        try:
                            # print(image)
                            # similar_CT_MR_image[images] = image

                            if ("CT" in images):
                                # ctSlicesPathList.append(imagePath)
                                imagePath = os.path.join(slices_path, images)
                                image = Image.open(imagePath).convert('L')
                                image.verify()
                                similar_CT_CT_image.append(image)
                                similar_CT_CT_image.append(image)
                                similar_CT_CT_paths.append(imagePath)
                                similar_CT_CT_paths.append(imagePath)
                        except(IOError, SyntaxError):
                            print("Image is empty :" + image)

                    imagePairs.append(similar_CT_CT_image)
                    imagePairsLabel.append(label)
                    imagePairsPaths.append(similar_CT_CT_paths)

            # create negative pairs
            label = 0
            for i in range(0, 100):
                index = random.randint(0, len(ctSlicesPathList) - 1)
                negative_match_index = random.randint(0, len(mriSlicesPathList) - 1)
                while (index == negative_match_index):
                    negative_match_index = random.randint(0, len(mriSlicesPathList) - 1)
                ct_path = ctSlicesPathList[index]

                mri_path = mriSlicesPathList[negative_match_index]
                print("Neg CT Path " + ct_path)
                print("Neg MRI Path " + mri_path)
                diffImage1 = Image.open(os.path.join(ct_path)).convert('L')
                diffImage2 = Image.open(os.path.join(mri_path)).convert('L')
                imagePairs.append([diffImage1, diffImage2])
                imagePairsLabel.append(label)
                imagePairsPaths.append([ct_path, mri_path])
            print("finish loading test dataset to memory")



        imagePairsLabel = torch.from_numpy(np.array(imagePairsLabel, dtype=np.float32))


        # shuffling = list(zip(imagePairs,imagePairsLabel,imagePairsPaths))
        # random.shuffle(shuffling)
        # imagePairs, imagePairsLabel, imagePairsPaths = zip(*shuffling)
        return imagePairs, imagePairsLabel, imagePairsPaths

    def __len__(self):
        return len(self.imagePairs)

    def __get_imagePairs__(self):
        return self.imagePairs

    def __getitem__(self, index):
        paths = self.imagePairsPaths[index]
        images = self.imagePairs[index]
        try:
            image1 = images[0]
            path1 = paths[0]
            image2 = images[1]
            path2 = paths[1]
            # print(image1)
            # print(image2)
        except(IndexError, TypeError) as e:
            print("Index: " + str(e))
            print("File Paths :")
            print(paths)
            print("Images :")
            print(images)

        # print(len(self.imagePairs[index]))

        label = self.imagePairsLabel[index]
        if self.transform:
            # if(type(image1) == list or type(image2)==list):
            #     print("Image 1 or 2 is a list")
            #     return
            # print("Hello World")
            # image1 = np.array(image1)
            # image1 = (image1 - np.min(image1)) / (np.max(image1) - np.min(image1))
            #
            # image2 = np.array(image2)
            # image2 = (image2 - np.min(image2)) / (np.max(image2) - np.min(image2))
            # print("Max :" + str(np.max(image1)))
            # print("Min : " + str(np.min(image1)))
            # image1 = Image.fromarray(image1)
            # image2 = Image.fromarray(image2)

            image1 = self.transform(image1)
            image2 = self.transform(image2)
            # print("Max :" + str(torch.max(image1)))
            # print("Min : " + str(torch.min(image1)))
            # print("Mean" + str(torch.mean(image1)))

        # if(isinstance(image1) or isinstance(image2)):
        #     print("Image 1 or 2 is a list")

        return image1, image2, torch.from_numpy(np.array([label], dtype=np.float32))

class Similarity_Learning_Dataset(Dataset):

    def __init__(self, dataPath, patientList, transform=None, train=True):
        super(Similarity_Learning_Dataset, self).__init__()
        # np.random.seed(0)
        # self.dataset = dataset
        self.dataPath = dataPath
        self.transform = transform
        self.patientList = patientList
        self.train = train
        self.imagePairs, self.imagePairsLabel, self.imagePairsPaths = self.loadToMem()


    def loadToMem(self):
        random.seed(42)

        # Create matching pairs
        imagePairsList = []
        imagePairsLabelList = []
        imagePairsPathsList = []
        # print(dataPath)
        ctSlicesPathLists = []
        mriSlicesPathLists = []
        if(self.train == True):
            label = 1
            patient_paths = self.dataPath
            for slices in os.listdir(patient_paths):
                for patient in self.patientList:
                    # print(slices)
                    print("begin loading training dataset to memory")
                    slices_path = os.path.join(patient_paths, slices)
                    if("CT_CT" in slices):
                        imagePairs, imagePairsLabel, imagePairsPaths, ctSlicesPathList, mriSlicesPathList = self.create_matching_image_pairs(label, patient, slices, slices_path)

                    elif ("CT_MRI" in slices):
                        imagePairs, imagePairsLabel, imagePairsPaths, ctSlicesPathList, mriSlicesPathList= self.create_matching_image_pairs(label, patient, slices, slices_path)

                    else:
                        print("Neither CT-CT or CT-MRI in slice folder names")
                        imagePairs = []
                        imagePairsLabel = []
                        imagePairsPaths = []
                        ctSlicesPathList = []
                        mriSlicesPathList = []
                    imagePairsList = imagePairsList + imagePairs
                    imagePairsLabelList = imagePairsLabelList + imagePairsLabel
                    imagePairsPathsList = imagePairsPathsList + imagePairsPaths
                    ctSlicesPathLists = ctSlicesPathLists + ctSlicesPathList
                    mriSlicesPathLists = mriSlicesPathLists + mriSlicesPathList


            print("Length of Positive_CT_MRI and CT_CT pairs:" + str(len(imagePairsList)))


            # create negative CT-CT and CT-MRI pairs
            label = 0
            for i in range(0, 500):
                ct_mri_imagePairs, ct_mri_imagePairsLabel, ct_mri_imagePairsPaths = self.create_negative_pairs(ctSlicesPathLists, label, mriSlicesPathLists)
                ct_ct_imagePairs, ct_ct_imagePairsLabel, ct_ct_imagePairsPaths = self.create_negative_pairs(ctSlicesPathLists, label, ctSlicesPathLists)
                imagePairsList = imagePairsList + ct_mri_imagePairs + ct_ct_imagePairs
                imagePairsLabelList = imagePairsLabelList + ct_mri_imagePairsLabel + ct_ct_imagePairsLabel
                imagePairsPathsList = imagePairsPathsList + ct_mri_imagePairsPaths + ct_ct_imagePairsPaths
            print("Length of Positive and Negative CT-CT/CT_MRI pairs:" + str(len(imagePairsList)))
            # print("Length of Negative_CT_CT_pairs:" + str(len(ct_ct_imagePairs)))
        return imagePairsList, imagePairsLabelList, imagePairsPathsList

    def create_negative_pairs(self, slicesPathList1, label, slicesPathList2):

        imagePairs = []
        imagePairsLabel = []
        imagePairsPaths = []

        index = random.randint(0, len(slicesPathList1) - 1)
        negative_match_index = random.randint(0, len(slicesPathList2) - 1)
        while (index == negative_match_index):
            negative_match_index = random.randint(0, len(slicesPathList2) - 1)
        ct_path = slicesPathList1[index]
        mri_path = slicesPathList2[negative_match_index]
        print("Neg CT Path " + ct_path)
        print("Neg MRI Path " + mri_path)
        diffImage1 = Image.open(os.path.join(ct_path)).convert('L')
        diffImage2 = Image.open(os.path.join(mri_path)).convert('L')
        imagePairs.append([diffImage1, diffImage2])
        imagePairsLabel.append(label)
        imagePairsPaths.append([ct_path, mri_path])

        return imagePairs, imagePairsLabel, imagePairsPaths

    def create_matching_image_pairs(self, label, patient, slices, slices_path):

        imagePairs = []
        imagePairsLabel = []
        imagePairsPaths = []
        ctSlicesPathList = []
        mriSlicesPathList = []

        anchor_image_path = glob.glob(os.path.join(slices_path, "CT_*Lymphoma_1031_*.jpg"))
        anchor_image = Image.open(anchor_image_path[0]).convert('L')
        print("Anchor Image:" + anchor_image_path[0])
        if (slices != ".DS_Store" and os.path.isdir(slices_path)):

            for images in os.listdir(slices_path):
                try:
                    imagePath = os.path.join(slices_path, images)
                    if (patient in images):
                        # print(images)
                        image =Image.open(imagePath).convert('L')

                        image.verify()

                        # similar_images.append(image)
                        # similar_paths.append(imagePath)
                        imagePairs.append([anchor_image, image])
                        imagePairsPaths.append([anchor_image_path[0], imagePath])
                        imagePairsLabel.append(label)
                        if ("CT" in images):
                            ctSlicesPathList.append(imagePath)
                        if ("MRI" in images):
                            mriSlicesPathList.append(imagePath)
                except(IOError, SyntaxError):
                    print("Image is empty :" + image)

            return imagePairs, imagePairsLabel, imagePairsPaths, ctSlicesPathList, mriSlicesPathList

    def __len__(self):
        return len(self.imagePairs)

    def __get_imagePairs__(self):
        return self.imagePairs

    def __getitem__(self, index):
        # image1, image2 = self.imagePairs[index][0]
        paths = self.imagePairsPaths[index]
        images = self.imagePairs[index]
        try:
            image1 = images[0]
            path1 = paths[0]
            image2 = images[1]
            path2 = paths[1]
        except(IndexError, TypeError) as e:
            print("Index: " + str(e))
            print("File Paths :")
            print(paths)
            print("Images :")
            print(images)

        # print(len(self.imagePairs[index]))

        label = self.imagePairsLabel[index]
        if self.transform:
            # if(type(image1) == list or type(image2)==list):
            #     print("Image 1 or 2 is a list")
            #     return
            image1 = self.transform(image1)
            image2 = self.transform(image2)

        # if(isinstance(image1) or isinstance(image2)):
        #     print("Image 1 or 2 is a list")
        return image1, image2, torch.from_numpy(np.array([label], dtype=np.float32))

class Triplet_Dataset(Dataset):

    def __init__(self, dataPath, patientList, transform=None, train=True):
        super(Triplet_Dataset, self).__init__()
        np.random.seed(42)
        # self.dataset = dataset
        self.dataPath = dataPath
        self.transform = transform
        self.patientList = patientList
        self.train = train
        self.imagePairs, self.imagePairsPaths = self.loadToMem()

    # def loadCTandMRIPathsList(self, slices, slices_path):
    #
    #     ctSlicesPathList = []
    #     mriSlicesPathList = []
    #
    #     anchor_image_path = glob.glob(os.path.join(slices_path, "CT_*Lymphoma_1031_*.jpg"))
    #     anchor_image = Image.open(anchor_image_path[0]).convert('L')
    #     print("Anchor Image:" + anchor_image_path[0])
    #     # if (slices != ".DS_Store" and os.path.isdir(slices_path)):
    #     #
    #     #     for images in os.listdir(slices_path):
    #     #         try:
    #     #             imagePath = os.path.join(slices_path, images)
    #     #             if (patient in images):
    #     #                 # print(images)
    #     #                 image = Image.open(imagePath).convert('L')
    #     #
    #     #                 image.verify()
    #     #
    #     #                 # similar_images.append(image)
    #     #                 # similar_paths.append(imagePath)
    #     #                 imagePairs.append([anchor_image, image])
    #     #                 imagePairsPaths.append([anchor_image_path[0], imagePath])
    #     #                 imagePairsLabel.append(label)
    #     #                 if ("CT" in images):
    #     #                     ctSlicesPathList.append(imagePath)
    #     #                 if ("MRI" in images):
    #     #                     mriSlicesPathList.append(imagePath)
    #     #         except(IOError, SyntaxError):
    #     #             print("Image is empty :" + image)
    #     #
    #     #     return imagePairs, imagePairsLabel, imagePairsPaths, ctSlicesPathList, mriSlicesPathList

    def loadToMem(self):
        random.seed(42)
        slices_away = 10
        # Create matching pairs
        imagePairsList = []
        imagePairsLabelList = []
        imagePairsPathsList = []
        # print(dataPath)
        ctSlicesPathLists = []
        mriSlicesPathLists = []
        patient_paths = self.dataPath
        for slices in os.listdir(patient_paths):
            for patient in self.patientList:
                # print(slices)
                print("begin loading training dataset to memory")
                slices_path = os.path.join(patient_paths, slices)
                if("CT_CT" in slices):
                    imagePairs, imagePairsPaths, ctSlicesPathList, mriSlicesPathList = self.create_matching_image_pairs(patient, slices, slices_path)

                elif ("CT_MRI" in slices):
                    imagePairs, imagePairsPaths, ctSlicesPathList, mriSlicesPathList= self.create_matching_image_pairs(patient, slices, slices_path)

                else:
                    print("Neither CT-CT or CT-MRI in slice folder names")
                    imagePairs = []
                    imagePairsPaths = []
                    ctSlicesPathList = []
                    mriSlicesPathList = []
                imagePairsList = imagePairsList + imagePairs
                imagePairsPathsList = imagePairsPathsList + imagePairsPaths
                ctSlicesPathLists = ctSlicesPathLists + ctSlicesPathList
                mriSlicesPathLists = mriSlicesPathLists + mriSlicesPathList


            print("Length of Positive_CT_MRI and CT_CT pairs:" + str(len(imagePairsList)))


            # add negative image to create triplet pair

            tripletImages, tripletImagesPaths = self.create_triplet_image_pairs(slices_away, imagePairsList, imagePairsPathsList, ctSlicesPathLists, mriSlicesPathLists)

            print("Length of Positive and Negative CT-CT/CT_MRI Triplets:" + str(len(tripletImages)))
            # print("Length of Negative_CT_CT_pairs:" + str(len(ct_ct_imagePairs)))
        return tripletImages, tripletImagesPaths

    def create_triplet_image_pairs(self, slices_away, imagePairsList, imagePairsPathsList, ctSlicesPathLists, mriSlicesPathLists):
        tripletImages = []
        tripletImagesPaths = []

        for i in range(len(imagePairsList)):
            imagePairs = imagePairsList[i]
            imagePairsPath = imagePairsPathsList[i]

            if(i < slices_away + 1):
                indexToIgnore = list(range(i + slices_away))
                selectedNegativeSlicePath = self.select_negative_image_path(ctSlicesPathLists, indexToIgnore, i, mriSlicesPathLists)
                image = Image.open(selectedNegativeSlicePath).convert('L')
                image.verify()
                imagePairs.append(image)
                imagePairsPath.append(selectedNegativeSlicePath)

            elif (len(imagePairsList) - i < slices_away):
                indexToIgnore = list(range(i - slices_away))
                selectedNegativeSlicePath = self.select_negative_image_path(ctSlicesPathLists, indexToIgnore, i, mriSlicesPathLists)
                image = Image.open(selectedNegativeSlicePath).convert('L')
                image.verify()
                imagePairs.append(image)
                imagePairsPath.append(selectedNegativeSlicePath)
            else:
                indexToIgnore = list(range(i - slices_away, i + slices_away))
                selectedNegativeSlicePath = self.select_negative_image_path(ctSlicesPathLists, indexToIgnore, i, mriSlicesPathLists)
                image = Image.open(selectedNegativeSlicePath).convert('L')
                image.verify()
                imagePairs.append(image)
                imagePairsPath.append(selectedNegativeSlicePath)

            tripletImages.append(imagePairs)
            tripletImagesPaths.append(imagePairsPath)
        return tripletImages, tripletImagesPaths

    def select_negative_image_path(self, ctSlicesPathLists, indexToIgnore, i, mriSlicesPathLists):

        ctSlicesPathListsNew = [value for (i, value) in enumerate(ctSlicesPathLists) if i not in indexToIgnore]
        mriSlicesPathListsNew = [value for (i, value) in enumerate(mriSlicesPathLists) if i not in indexToIgnore]
        ctIndex = random.randint(0, len(ctSlicesPathLists) - 1)
        mriIndex = random.randint(0, len(mriSlicesPathLists) - 1)
        selectedNegativeSlicePath = random.choice([ctSlicesPathListsNew[ctIndex], mriSlicesPathListsNew[mriIndex]])
        return selectedNegativeSlicePath

    def create_matching_image_pairs(self, patient, slices, slices_path):

        imagePairs = []
        imagePairsPaths = []
        ctSlicesPathList = []
        mriSlicesPathList = []

        anchor_image_path = glob.glob(os.path.join(slices_path, "CT_*Lymphoma_1031_*.jpg"))
        anchor_image = Image.open(anchor_image_path[0]).convert('L')
        print("Anchor Image:" + anchor_image_path[0])
        if (slices != ".DS_Store" and os.path.isdir(slices_path)):

            for images in os.listdir(slices_path):
                try:
                    imagePath = os.path.join(slices_path, images)
                    if (patient in images):
                        # print(images)
                        image = Image.open(imagePath).convert('L')

                        image.verify()

                        # similar_images.append(image)
                        # similar_paths.append(imagePath)
                        imagePairs.append([anchor_image, image])
                        imagePairsPaths.append([anchor_image_path[0], imagePath])
                        if ("CT" in images):
                            ctSlicesPathList.append(imagePath)
                        if ("MRI" in images):
                            mriSlicesPathList.append(imagePath)
                except(IOError, SyntaxError):
                    print("Image is empty :" + image)

            return imagePairs, imagePairsPaths, ctSlicesPathList, mriSlicesPathList

    def __len__(self):
        return len(self.imagePairs)

    def __get_imagePairs__(self):
        return self.imagePairs

    def __getitem__(self, index):
        # image1, image2 = self.imagePairs[index][0]
        paths = self.imagePairsPaths[index]
        images = self.imagePairs[index]
        try:
            image1 = images[0]
            path1 = paths[0]
            image2 = images[1]
            path2 = paths[1]
        except(IndexError, TypeError) as e:
            print("Index: " + str(e))
            print("File Paths :")
            print(paths)
            print("Images :")
            print(images)

        # print(len(self.imagePairs[index]))

        label = self.imagePairsLabel[index]
        if self.transform:
            # if(type(image1) == list or type(image2)==list):
            #     print("Image 1 or 2 is a list")
            #     return
            image1 = self.transform(image1)
            image2 = self.transform(image2)

        # if(isinstance(image1) or isinstance(image2)):
        #     print("Image 1 or 2 is a list")
        return image1, image2, image3, torch.from_numpy(np.array([label], dtype=np.float32))


class OmniglotTrain(Dataset):

    def __init__(self, dataPath, transform=None):
        super(OmniglotTrain, self).__init__()
        np.random.seed(0)
        # self.dataset = dataset
        self.transform = transform
        self.datas, self.num_classes = self.loadToMem(dataPath)

    def loadToMem(self, dataPath):
        print("begin loading training dataset to memory")
        datas = {}
        agrees = [0, 90, 180, 270]
        idx = 0
        for agree in agrees:
            print("Agree: " + str(agree))
            for alphaPath in os.listdir(dataPath):
                if alphaPath != ".DS_Store":
                    print("Alpha Path: " + alphaPath)

                    for charPath in os.listdir(os.path.join(dataPath, alphaPath)):
                        print("Char Path: " + charPath)
                        if charPath != ".DS_Store":
                            datas[idx] = []
                            for samplePath in os.listdir(os.path.join(dataPath, alphaPath, charPath)):
                                filePath = os.path.join(dataPath, alphaPath, charPath, samplePath)
                                datas[idx].append(Image.open(filePath).rotate(agree).convert('L'))
                            idx += 1
        print("finish loading training dataset to memory")
        return datas, idx

    def __len__(self):
        return 21000000

    def __getitem__(self, index):
        # image1 = random.choice(self.dataset.imgs)
        label = None
        img1 = None
        img2 = None
        # get image from same class
        if index % 2 == 1:
            label = 1.0
            idx1 = random.randint(0, self.num_classes - 1)
            image1 = random.choice(self.datas[idx1])
            image2 = random.choice(self.datas[idx1])
        # get image from different class
        else:
            label = 0.0
            idx1 = random.randint(0, self.num_classes - 1)
            idx2 = random.randint(0, self.num_classes - 1)
            while idx1 == idx2:
                idx2 = random.randint(0, self.num_classes - 1)
            image1 = random.choice(self.datas[idx1])
            image2 = random.choice(self.datas[idx2])

        if self.transform:
            image1 = self.transform(image1)
            image2 = self.transform(image2)
        return image1, image2, torch.from_numpy(np.array([label], dtype=np.float32))


class OmniglotTest(Dataset):

    def __init__(self, dataPath, transform=None, times=200, way=20):
        np.random.seed(1)
        super(OmniglotTest, self).__init__()
        self.transform = transform
        self.times = times
        self.way = way
        self.img1 = None
        self.c1 = None
        self.datas, self.num_classes = self.loadToMem(dataPath)

    def loadToMem(self, dataPath):
        print("begin loading test dataset to memory")
        datas = {}
        idx = 0
        for alphaPath in os.listdir(dataPath):
            for charPath in os.listdir(os.path.join(dataPath, alphaPath)):
                datas[idx] = []
                for samplePath in os.listdir(os.path.join(dataPath, alphaPath, charPath)):
                    filePath = os.path.join(dataPath, alphaPath, charPath, samplePath)
                    datas[idx].append(Image.open(filePath).convert('L'))
                idx += 1
        print("finish loading test dataset to memory")
        return datas, idx

    def __len__(self):
        return self.times * self.way

    def __getitem__(self, index):
        idx = index % self.way
        label = None
        # generate image pair from same class
        if idx == 0:
            self.c1 = random.randint(0, self.num_classes - 1)
            self.img1 = random.choice(self.datas[self.c1])
            img2 = random.choice(self.datas[self.c1])

            label = 1
        # generate image pair from different class
        else:
            c2 = random.randint(0, self.num_classes - 1)
            while self.c1 == c2:
                c2 = random.randint(0, self.num_classes - 1)
            img2 = random.choice(self.datas[c2])
            label = 0

        if self.transform:
            img1 = self.transform(self.img1)
            img2 = self.transform(img2)
        return img1, img2, torch.from_numpy(np.array([label], dtype=np.float32))