from algorithm import Algorithm
import torch
import torch.nn as nn
import attn_handler
import math
import csv


class Sparse(nn.Module):
    def __init__(self, dataset):
        super().__init__()
        self.dataset = dataset
        self.last_k = 0

    def forward(self, X, epoch,l0_norm):
        self.last_k = self.get_k(epoch,l0_norm)
        X = torch.where(torch.abs(X) < self.last_k, 0, X)
        return X

    def get_k(self, epoch,l0_norm):
        l0_norm_threshold = 40
        start = 250
        maximum = 0.5
        end = 500
        minimum = 0

        if l0_norm <= l0_norm_threshold:
            return self.last_k

        if epoch < start:
            return minimum
        elif epoch > end:
            return maximum
        else:
            return (epoch - start) * (maximum / (end - start))


class ZhangNet(nn.Module):
    def __init__(self, bands, dataset):
        super().__init__()

        self.bands = bands
        self.dataset = dataset
        self.number_of_classes = attn_handler.get_number_of_classes(dataset.name)
        self.weighter = nn.Sequential(
            nn.Linear(self.bands, 512),
            nn.ReLU(),
            nn.Linear(512, self.bands)
        )
        self.classnet = nn.Sequential(
            nn.Linear(self.bands, 32),
            nn.ReLU(),
            nn.BatchNorm1d(32),
            nn.Linear(32, self.number_of_classes),
        )
        self.sparse = Sparse(self.dataset)
        num_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        print("Number of learnable parameters:", num_params)

    def forward(self, X, epoch, l0_norm):
        acw = self.weighter(X)
        acw = torch.abs(acw)
        channel_weights = torch.mean(acw, dim=0)
        sparse_weights = self.sparse(channel_weights, epoch, l0_norm)
        reweight_out = X * sparse_weights
        output = self.classnet(reweight_out)
        return acw, channel_weights, sparse_weights, output


class Algorithm_v9_weight(Algorithm):
    def __init__(self, target_size:int, dataset, tag, reporter, verbose):
        super().__init__(target_size, dataset, tag, reporter, verbose)
        self.criterion = torch.nn.CrossEntropyLoss()
        self.zhangnet = ZhangNet(self.dataset.get_train_x().shape[1], dataset).to(self.device)
        self.total_epoch = 500

        self.X_train = torch.tensor(self.dataset.get_train_x(), dtype=torch.float32).to(self.device)
        self.y_train = torch.tensor(self.dataset.get_train_y(), dtype=torch.long).to(self.device)

    def get_selected_indices(self):
        optimizer = torch.optim.Adam(self.zhangnet.parameters(), lr=0.001, betas=(0.9,0.999))
        channel_weights = None
        loss = 0
        l1_loss = 0
        mse_loss = 0
        sparse_weights = None
        for epoch in range(self.total_epoch):
            optimizer.zero_grad()
            if sparse_weights is None:
                l0_norm = self.X_train.shape[1]
            else:
                l0_norm = torch.norm(sparse_weights, p=0).item()
            acw, channel_weights, sparse_weights, y_hat = self.zhangnet(self.X_train, epoch, l0_norm)

            with open("v9_weights.csv", mode='a', newline='') as f:
                acw = acw[0:128]
                #self.do_print(acw)
                acw = acw[:,33]
                cv = torch.std(acw) / torch.mean(acw)
                #print(cv.item())
                writer = csv.writer(f)
                writer.writerow(acw.tolist())

            deciding_weights = channel_weights
            mean_weight, all_bands, selected_bands = attn_handler.get_indices(deciding_weights, self.target_size)
            self.set_all_indices(all_bands)
            self.set_selected_indices(selected_bands)
            self.set_weights(mean_weight)
            mse_loss = self.criterion(y_hat, self.y_train)
            l1_loss = self.l1_loss(channel_weights)
            lambda_value = self.get_lambda(l0_norm)
            loss = mse_loss + lambda_value*l1_loss
            if epoch%10 == 0:
                attn_handler.report_stats(self, channel_weights, sparse_weights, epoch, mse_loss, l1_loss.item(), lambda_value,loss)
            loss.backward()
            optimizer.step()

        print(self.get_name(),"selected bands and weights:")
        print("".join([str(i).ljust(10) for i in self.selected_indices]))
        return self.zhangnet, self.selected_indices

    def do_print(self, acw):
        inds = [36, 159, 108, 181, 149, 148, 98,33,5,6,9]
        for i in inds:
            acw2 = acw[:, i]
            cv = torch.std(acw2) / torch.mean(acw2)
            print(i, cv.item())

    def l1_loss(self, channel_weights):
        return torch.norm(channel_weights, p=1) / torch.numel(channel_weights)

    def get_lambda(self, l0_norm):
        return attn_handler.get_lambda(l0_norm)

