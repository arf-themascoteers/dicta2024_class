from algorithm import Algorithm
import torch
import torch.nn as nn
import bsdr_handler


class LinearInterpolationModule(nn.Module):
    def __init__(self, y_points, device):
        super(LinearInterpolationModule, self).__init__()
        self.device = device
        self.y_points = y_points.to(device)

    def forward(self, x_new_):
        x_new = x_new_.to(self.device)
        batch_size, num_points = self.y_points.shape
        x_points = torch.linspace(0, 1, num_points).to(self.device).expand(batch_size, -1).contiguous()
        x_new_expanded = x_new.unsqueeze(0).expand(batch_size, -1).contiguous()
        idxs = torch.searchsorted(x_points, x_new_expanded, right=True)
        idxs = idxs - 1
        idxs = idxs.clamp(min=0, max=num_points - 2)
        x1 = torch.gather(x_points, 1, idxs)
        x2 = torch.gather(x_points, 1, idxs + 1)
        y1 = torch.gather(self.y_points, 1, idxs)
        y2 = torch.gather(self.y_points, 1, idxs + 1)
        weights = (x_new_expanded - x1) / (x2 - x1)
        y_interpolated = y1 + weights * (y2 - y1)
        return y_interpolated


class ANN(nn.Module):
    def __init__(self, target_size, number_of_classes):
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.target_size = target_size
        self.number_of_classes = number_of_classes

        init_vals = torch.linspace(0.001, 0.99, self.target_size + 2)
        self.indices = nn.Parameter(
            torch.tensor([ANN.inverse_sigmoid_torch(init_vals[i + 1]) for i in range(self.target_size)],
                         requires_grad=True).to(self.device))

        self.fc = nn.Sequential(
            nn.Linear(target_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, self.number_of_classes)
        )

        print("Num classes",self.number_of_classes)

        num_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        print("Number of learnable parameters:", num_params)

        fcp = sum(p.numel() for p in self.fc.parameters() if p.requires_grad)
        print("FC:", fcp)

        idp = sum(p.numel() for p in self.indices if p.requires_grad)
        print("ID:", idp)

        print("FC+ID:", fcp+idp)



    @staticmethod
    def inverse_sigmoid_torch(x):
        return -torch.log(1.0 / x - 1.0)

    def forward(self, linterp):
        outputs = linterp(self.get_indices())
        soc_hat = self.fc(outputs)
        return soc_hat

    def get_indices(self):
        return torch.sigmoid(self.indices)


class Algorithm_bsdr(Algorithm):
    def __init__(self, target_size:int, dataset, tag, reporter, verbose):
        super().__init__(target_size, dataset, tag, reporter, verbose)

        torch.manual_seed(2)
        torch.cuda.manual_seed(2)
        torch.backends.cudnn.deterministic = True

        self.original_feature_size = self.dataset.get_train_x().shape[1]

        self.ann = ANN(self.target_size, bsdr_handler.get_number_of_classes(dataset.name)).to(self.device)
        self.criterion = torch.nn.CrossEntropyLoss()
        self.total_epoch = 2000

        self.X_train = torch.tensor(self.dataset.get_train_x(), dtype=torch.float32).to(self.device)
        self.y_train = torch.tensor(self.dataset.get_train_y(), dtype=torch.long).to(self.device)

        self.linterp_train = LinearInterpolationModule(self.X_train, self.device)

    def get_selected_indices(self):
        optimizer = torch.optim.Adam(self.ann.parameters(), lr=0.01, betas=(0.9,0.999))
        for epoch in range(self.total_epoch):
            optimizer.zero_grad()
            y_hat = self.ann(self.linterp_train)
            loss = self.criterion(y_hat, self.y_train)
            loss.backward()
            optimizer.step()
            self.set_selected_indices(self.get_indices())
            if self.verbose:
                self.report(epoch, loss.item())
        print("|".join([str(i) for i in self.get_indices()]))
        return self.ann, self.selected_indices

    def report(self, epoch, mse):
        if not self.verbose:
            return
        if epoch%10 != 0:
            return

        bsdr_handler.report_stats(self, epoch, mse)


    def get_indices(self):
        indices = torch.round(self.ann.get_indices() * self.original_feature_size ).to(torch.int64)
        indices = torch.clip(indices, 0, self.original_feature_size-1).tolist()
        return list(dict.fromkeys(indices))

    def get_num_params(self):
        return sum(p.numel() for p in self.ann.parameters() if p.requires_grad)


    def is_cacheable(self):
        return False