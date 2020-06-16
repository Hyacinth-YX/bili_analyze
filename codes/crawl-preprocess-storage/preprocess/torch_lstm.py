import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


class LSTM (nn.Module):
    def __init__(self, input_size=1, hidden_layer_size=300, output_size=1):
        super ().__init__ ()
        self.hidden_layer_size = hidden_layer_size

        self.lstm = nn.LSTM (input_size, hidden_layer_size)

        self.linear = nn.Linear (hidden_layer_size, output_size)

        self.hidden_cell = (torch.zeros (1, 1, self.hidden_layer_size),
                            torch.zeros (1, 1, self.hidden_layer_size))

    def forward(self, input_seq):
        lstm_out, self.hidden_cell = self.lstm (input_seq.view (len (input_seq), 1, -1), self.hidden_cell)
        predictions = self.linear (lstm_out.view (len (input_seq), -1))
        return predictions[-1]


def create_inout_sequences(input_data, tw):
    inout_seq = []
    L = len (input_data)
    for i in range (L - tw):
        train_seq = input_data[i:i + tw]
        train_label = input_data[i + tw:i + tw + 1]
        inout_seq.append ((train_seq, train_label))
    return inout_seq


def pre_process(data_item):
    isnull = data_item.isnull ()
    nullindex = data_item[isnull].index.tolist ()
    data_pre = data_item.drop (nullindex)
    train_data_len = int (len (data_pre) - 12 - 1)
    train_data = data_pre[0:train_data_len]
    test_data = data_pre[train_data_len + 1:]
    # print(len(train_data))
    # print(len(test_data))
    normaled_train_data, scaler = data_normalized (train_data)
    normaled_train_data = torch.FloatTensor (normaled_train_data).view (-1)
    normaled_test_data, scaler_test = data_normalized (test_data)
    normaled_test_data = torch.FloatTensor (normaled_test_data).view (-1)
    return normaled_train_data, normaled_test_data, test_data, train_data, scaler, scaler_test


def data_normalized(data):
    scaler = MinMaxScaler (feature_range=(-1, 1))
    train_data_normalized = scaler.fit_transform (data.to_numpy ().reshape (-1, 1))
    return train_data_normalized, scaler


def train_model(train_inout_seq, model, epochs=150):
    for i in range (epochs):
        for seq, labels in train_inout_seq:
            optimizer.zero_grad ()
            model.hidden_cell = (torch.zeros (1, 1, model.hidden_layer_size),
                                 torch.zeros (1, 1, model.hidden_layer_size))

            y_pred = model (seq)

            single_loss = loss_function (y_pred, labels)
            single_loss.backward ()
            optimizer.step ()

        if i % 25 == 1:
            print (f'epoch: {i:3} loss: {single_loss.item ():10.8f}')

    print (f'epoch: {i:3} loss: {single_loss.item ():10.10f}')


def model_predict(future_pred, test_inputs, scaler):
    for i in range (future_pred):
        seq = torch.FloatTensor (test_inputs[-train_window:])
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


if __name__ == '__main__':
    # filepath = './cleaned_data.xlsx'
    filepath = '附件1数据完成清理_ratio.xlsx'
    data = pd.read_excel (filepath, sheet_name=0, parse_dates=[0], index_col=0)
    i = -1
    # train_windows = [20,20,8,8,8,8,8,8,8,8,8,8,8,8,8,8]
    # epochss = [300,300,300,300,300,300,300,300,300,300,300,300,300,300,300,300]
    # hidden_layer_sizes = [300,230,170,170,170,170,170,170,170,170,170,170,170,170,170,170]
    train_windows =      [ 6,    6,   8,   6,    6,    8,   6,   8,   6,   7,   5,     7,    8,   8,   6,   7]
    epochss =            [100, 160, 165, 200,  150,  60,  180, 180, 200, 150,  150,  200,  250, 180, 150, 140]
    hidden_layer_sizes = [150, 170, 200, 80,   100,  250, 150, 100, 180, 150,  180,   100, 150, 150, 140, 130]
    # no ratio data       √     √    √    √    √    √    √    √    √    √    √    √    √    √    √
    # train_windows =      [4,    6,   8,   5,   6,   8,   6,   9,   6,   6,   7,   7,   8,   6,   6,   7]
    # epochss =            [350, 160, 165, 190, 70,  60, 230,  180,  350, 280, 300, 250, 200, 160, 150, 140]
    # hidden_layer_sizes = [150, 170, 200, 180, 200, 250, 150, 100, 180, 150, 100, 100, 150, 150, 140, 130]
    forecast_data = pd.DataFrame (index=pd.date_range (start='2020/01/31', end='2020/10/31', freq='3M'),
                                  columns=data.columns)
    for index, item in data.iteritems ():
        i += 1
        # if i not in [11,12]:
        #     continue
        train_window = train_windows[i]
        epochs = epochss[i]
        # 数据预处理
        normaled_train_data, normaled_test_data, test_data, train_data, scaler, scaler_test = pre_process (item)
        train_inout_seq = create_inout_sequences (normaled_train_data, train_window)
        # 初始化模型 使用交叉熵损失;使用adam优化器。
        model = LSTM (hidden_layer_size=hidden_layer_sizes[i])
        loss_function = nn.MSELoss ()
        optimizer = torch.optim.Adam (model.parameters (), lr=0.001)
        try:
            # 训练模型
            train_model (train_inout_seq, model, epochs)
        except Exception as e:
            continue
        try:
            # 训练集预测
            start_point = 12
            # if i == 10:
            #     start_point = 4
            train_inputs = normaled_train_data[start_point:train_window+start_point].tolist ()
            train_predict_num = len (train_data) - train_window  - start_point
            actual_predictions = model_predict (train_predict_num, train_inputs, scaler)
            train_pred = pd.DataFrame (actual_predictions,
                                       index=pd.date_range (start=train_data.index[train_window+start_point], end=train_data.index[-1],
                                                            periods=train_predict_num))
            # 画图
            plt.plot (train_pred)

            # test预测
            test_inputs = normaled_train_data[-train_window:].tolist ()
            # print (test_inputs)
            actual_predictions = model_predict (len (test_data), test_inputs, scaler)
            pred = pd.DataFrame (actual_predictions,
                                 index=pd.date_range (start=test_data.index[0], end=test_data.index[-1],
                                                      periods=len (test_data)))
            MSE = mean_squared_error(actual_predictions, test_data.values)
            print(f"测试集均方误差为：{MSE:10.10e}")
            MSE_data = pd.DataFrame({'MSE':MSE},index=[index]).to_csv('./MSE_data.csv', index=False, mode='a', encoding='utf8')
            # 画图
            plt.plot (train_data)
            plt.plot (test_data)
            plt.plot (pred)

            # 目标值预测
            pred_inputs = normaled_test_data[-train_window:].tolist ()
            actual_predictions_fore = model_predict (4, pred_inputs, scaler_test)
            forecast_data[index] = actual_predictions_fore
            plt.plot (forecast_data[index])
            plt.savefig (index + '.png')
            plt.show ()
        except Exception as e:
            forecast_data.to_csv ('./forecast_data_temp.csv', index=False, mode='a', encoding='utf8')
            continue
    forecast_data.to_csv ('./forecast_data.csv', index=False, mode='w', encoding='utf8')
