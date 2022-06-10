import torch
import torch.nn as nn
import torch.nn.functional as F


class Siamese(nn.Module):

    def __init__(self):
        super(Siamese, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 64, 10),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 7),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 128, 4),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 4),
            nn.ReLU(),
        )
        self.linear = nn.Sequential(nn.Linear(9216, 4096), nn.Sigmoid())
        self.out = nn.Linear(4096, 1)
        self.out_feat1 = None
        self.out_feat2 = None
        self.dis = None

    def get_feature_vectors(self):
        return self.out_feat1, self.out_feat2

    def get_distance(self):
        return self.dis

    def forward_one(self, x):
        x = self.conv(x)
        x = x.view(x.size()[0], -1)
        x = self.linear(x)
        return x

    def forward_features(self, x1, x2):
        out1 = self.forward_one(x1)
        out2 = self.forward_one(x2)

        return out1, out2

    def forward_distance(self, x1, x2):
        out1 = self.forward_one(x1)
        out2 = self.forward_one(x2)
        dis = torch.abs(out1 - out2)

        return dis

    def forward(self, x1, x2):
        self.out_feat1 = self.forward_one(x1)
        self.out_feat2 = self.forward_one(x2)
        self.dis = torch.abs(self.out_feat1 - self.out_feat2) # can change it to different distance such as cosine similarity, pairwise distance
        # print("Abs Distance :")
        # print(dis)
        # l2_norm_dist = torch.nn.PairwiseDistance(p=2)
        # dis1 = l2_norm_dist(out1, out2)
        # print("L2 Norm Distance :")
        # print(dis1)
        out = self.out(self.dis)
        #  return self.sigmoid(out)
        return out

class Triplet(nn.Module):

    def __init__(self):
        super(Triplet, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 64, 10),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 7),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 128, 4),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 4),
            nn.ReLU(),
        )
        self.linear = nn.Sequential(nn.Linear(9216, 4096), nn.Sigmoid())
        self.out = nn.Linear(4096, 1)
        self.out_feat1 = None
        self.out_feat2 = None
        self.out_feat3 = None

    def get_feature_vectors(self):
        return self.out_feat1, self.out_feat2, self.out_feat3

    def forward_one(self, x):
        x = self.conv(x)
        x = x.view(x.size()[0], -1)
        x = self.linear(x)
        return x

    def forward_features(self, x1, x2, x3):
        out1 = self.forward_one(x1)
        out2 = self.forward_one(x2)
        out3 = self.forward_one(x3)

        return out1, out2, out3

    def forward(self, x1, x2, x3):

        return self.forward_features(x1, x2, x3)


# for test
if __name__ == '__main__':
    net = Siamese()
    triplet = Triplet()
    print(net)
    print(list(net.parameters()))
