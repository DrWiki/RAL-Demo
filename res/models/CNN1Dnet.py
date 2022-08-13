import torch.nn as nn
class Conv1dNet(nn.Module):
    def __init__(self, num_classes):
        super(Conv1dNet, self).__init__()
        self.conv1 = nn.Conv1d(1, 8, kernel_size=15, stride=2, padding=7, bias=False)
        self.bn1 = nn.BatchNorm1d(8)
        self.relu1 = nn.ReLU(inplace=True)
        self.maxpool1 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)

        # self.dp1 = nn.Dropout(p=0.2)


        self.conv2 = nn.Conv1d(8, 16, kernel_size=15, stride=2, padding=7, bias=False)
        self.bn2 = nn.BatchNorm1d(16)
        self.relu2 = nn.ReLU(inplace=True)
        self.maxpool2 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)

        # self.dp2 = nn.Dropout(p=0.2)


        self.conv3 = nn.Conv1d(16, 32, kernel_size=15, stride=2, padding=7, bias=False)
        self.bn3 = nn.BatchNorm1d(32)
        self.relu3 = nn.ReLU(inplace=True)
        self.maxpool3 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)

        # self.dp3 = nn.Dropout(p=0.1)

        self.avgpool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(32, num_classes)

    def forward(self, x):
        # print("Original",x.shape)
        x = self.conv1(x)
        # print("conv1", x.shape)
        x = self.bn1(x)
        # print("bn1",x.shape)
        x = self.relu1(x)
        # print("relu1",x.shape)
        x = self.maxpool1(x)
        # print("maxpool1",x.shape)

        # x = self.dp1(x)

        x = self.conv2(x)
        # print("conv2", x.shape)
        x = self.bn2(x)
        # print("bn2", x.shape)
        x = self.relu2(x)
        # print("relu2", x.shape)
        x = self.maxpool2(x)
        # print("maxpool2", x.shape)

        # x = self.dp2(x)


        x = self.conv3(x)
        # print("conv3", x.shape)
        x = self.bn3(x)
        # print("bn3", x.shape)
        x = self.relu3(x)
        # print("relu3", x.shape)
        x = self.maxpool3(x)
        # print("maxpool3", x.shape)
        # x = self.dp3(x)


        x = self.avgpool(x)
        # print("avgpool", x.shape)
        x = x.view(x.size(0), -1)
        # print("view", x.shape)
        x = self.fc(x)
        # print("fc", x.shape)
        return x