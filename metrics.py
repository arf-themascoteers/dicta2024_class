class Metrics:
    def __init__(self,time, oa, aa, k, selected_features, selected_weights):
        self.time = time
        self.r2 = oa
        self.rmse = aa
        self.rpd = k
        self.selected_features = selected_features
        self.selected_weights = selected_weights

