import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import time
import random
from tensorboardX import SummaryWriter


class LSTM (nn.Module):
    def __init__(self, input_size=1, hidden_layer_size=300, output_size=1):
        super ().__init__ ()
        self.hidden_layer_size = hidden_layer_size

        self.lstm = nn.LSTM (input_size, hidden_layer_size, batch_first=HyperParameter["batch_first"])

        self.linear = nn.Linear (hidden_layer_size, output_size)

        self.hidden_cell = (torch.zeros (1, 1, self.hidden_layer_size),
                            torch.zeros (1, 1, self.hidden_layer_size))

    def forward(self, input_seq):
        lstm_out, self.hidden_cell = self.lstm (input_seq, self.hidden_cell)
        predictions = self.linear (lstm_out)
        return predictions[0][-1]


def save_model(model, epoch):
    t = time.strftime ("%Y%m%d%H%M%s")
    filename = f"{Model_Folder}/{t}_{epoch}_params.pkl"
    torch.save (model.state_dict (), filename)


def load_model(model, filename):
    model.load_state_dict (torch.load (f"{Model_Folder}/{filename}"))


def evalute(model, test_seq):
    model.eval ()
    correct = 0
    total = len (test_seq)
    for x, y in test_seq:
        with torch.no_grad ():
            logits = model (x).reshape (1, -1)
            pred = logits.argmax (dim=1)
        correct += torch.eq (pred, y).sum ().float ().item ()
    return correct / total  # acc


def train_model(train_inout_seq, model, epochs=150):
    val_list = pd.DataFrame (columns=["loss", "val_acc"], index=range (epochs))
    best_epoch = 0
    best_acc = 0
    for epoch in range (epochs):
        total = len (train_inout_seq)
        fi = 0
        num_correct = 0
        loss = 0
        for seq, labels in train_inout_seq:
            seq = seq.unsqueeze (0)
            optimizer.zero_grad ()
            model.hidden_cell = (torch.zeros (1, 1, model.hidden_layer_size),
                                 torch.zeros (1, 1, model.hidden_layer_size))
            y_pred = model (seq)
            y_pred = y_pred.reshape (1, -1)
            single_loss = loss_function (y_pred, labels)
            single_loss.backward ()
            optimizer.step ()
            num_correct += torch.eq (y_pred, labels).sum ().float ().item ()
            loss += single_loss.item ()

            fi += 1
            print (f"\repoch:{epoch:3} training {fi / total:3.2%}", end="")
        val_acc = num_correct / total
        if val_acc > best_acc:
            best_epoch = epoch
            best_acc = val_acc
        save_model (model, epoch)
        val_list.iloc[epoch, 0] = single_loss.item ()
        val_list.iloc[epoch, 1] = val_acc
        writer.add_scalar ("Train_loss", loss, epoch)
        if epoch % 1 == 0:
            print (f'\tepoch: {epoch:3} loss: {loss:6.8e} acc : {val_acc}')
        # writer.add_graph (model, (inputs,))
    # writer.add_graph (model, train_inout_seq[0][0].reshape (1, HyperParameter["input_size"]))
    val_list.to_csv (f"{Model_Folder}/{time.strftime ('%Y%m%d%H%M%s')}_loss_log.csv")
    return best_epoch


def model_predict(test_seq, scaler):
    train_window = HyperParameter["train_window"]
    with torch.no_grad ():
        model.hidden = (torch.zeros (1, 1, model.hidden_layer_size),
                        torch.zeros (1, 1, model.hidden_layer_size))
        test_inputs.append (model (seq).item ())
    actual_predictions = scaler.inverse_transform (np.array (test_inputs[train_window:]).reshape (-1, 1))
    actual_predictions = np.apply_along_axis (no_negtive, 1, actual_predictions)
    return actual_predictions


def no_negtive(num):
    if num < 0:
        return 0
    else:
        return num


def data_normalized(data):
    scaler = MinMaxScaler (feature_range=(-1, 1))
    data_normalized = scaler.fit_transform (data.to_numpy ())
    return data_normalized


def create_inout_sequences(input_data, tw):
    inout_seq = []
    L = len (input_data)
    for i in range (L - tw):
        train_seq = input_data[i:i + tw]
        train_label = input_data[i + tw:i + tw + 1]
        inout_seq.append ((train_seq, train_label))
    return inout_seq


def series_process(normalized_data, inout_seq):
    normalized_data = torch.FloatTensor (normalized_data)
    inout_seq.extend (create_inout_sequences (normalized_data, HyperParameter["train_window"]))

    return inout_seq


def pre_process(data):
    inout_seq = []
    data = data_normalized (data)
    aids = list (set (data[:, 0]))
    for aid in aids:
        single_data = data[data[:, 0] == aid]
        if len (single_data) < HyperParameter["train_window"]:
            continue
        series_process (single_data[:, 1:], inout_seq)
    train_seq_num = int (len (inout_seq) * 8 / 10)
    train_seq = inout_seq[0:train_seq_num]
    test_seq = inout_seq[train_seq_num:]
    return train_seq, test_seq


HyperParameter = {"train_window": 5, "epochs": 300, "hidden_layer_sizes": 180, "input_size": 8, "output_size": 8,
                  "batch_first": True}
Model_Folder = "./model_out"
if __name__ == '__main__':
    filepath = './vresult.csv'
    data = pd.read_csv (filepath, parse_dates=[12, 13], index_col=0)
    data = data.iloc[:, 0:9]
    # 数据再次预处理为lstm的标准序列格式
    train_seq, test_seq = pre_process (data)
    shape = train_seq[0][0].shape
    # for i in range (1, len (train_seq)):
    #     b = train_seq[i][0].unsqueeze (0)
    #     a = torch.cat ([a, b], dim=0)
    inputs = torch.from_numpy(np.random.rand(1,shape[0],shape[1])).type(torch.FloatTensor)

    mode = 0
    if mode == 0:  # 训练模式
        writer = SummaryWriter (comment="test_model", log_dir="./scalar")  # 初始化tensorboard

        # 初始化模型 使用交叉熵损失;使用adam优化器。
        model = LSTM (hidden_layer_size=HyperParameter["hidden_layer_sizes"],
                      input_size=HyperParameter["input_size"],
                      output_size=HyperParameter["output_size"])
        loss_function = nn.MSELoss ()
        optimizer = torch.optim.Adam (model.parameters (), lr=0.001)

        try:
            # 训练模型
            best_epoch = train_model (train_seq, model, epochs=HyperParameter["epochs"])
            mode = 1  # 切换模式
        except Exception as e:
            print (e)

        writer.close ()
    if mode == 1:  # 预测模式
        # model_params_file_name = input ("输入保存的参数文件名:")
        model_params_file_name = "2020061715151592378138_1_params.pkl"
        model = LSTM (hidden_layer_size=HyperParameter["hidden_layer_sizes"],
                      input_size=HyperParameter["input_size"],
                      output_size=HyperParameter["output_size"])
        loss_function = nn.MSELoss ()
        optimizer = torch.optim.Adam (model.parameters (), lr=0.001)
        load_model (model, model_params_file_name)

        acc = evalute (model, test_seq)
        #
        # actual_predictions = model_predict (len (test_data), test_inputs, scaler)
        #
        # MSE = mean_squared_error (actual_predictions, test_data.values)
        # print (f"测试集均方误差为：{MSE:10.10e}")
        # MSE_data = pd.DataFrame ({'MSE': MSE}, index=[index]).to_csv ('./MSE_data.csv', index=False, mode='a',
        #                                                               encoding='utf8')
        # # 画图
        # plt.plot (train_data)
        # plt.plot (test_data)
        # plt.plot (pred)
        #
        # # 目标值预测
        # pred_inputs = normaled_test_data[-train_window:].tolist ()
        # actual_predictions_fore = model_predict (4, pred_inputs, scaler_test)
        # forecast_data[index] = actual_predictions_fore
        # plt.plot (forecast_data[index])
        # plt.savefig (index + '.png')
        # plt.show ()
