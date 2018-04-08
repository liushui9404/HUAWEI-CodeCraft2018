from matrix import matrix
import math

def create_dataset(time_series, time_step, predict_span):
    rows = len(time_series) - time_step - predict_span
    cols = time_step
    x_train = matrix(rows, cols)
    y_train = matrix(rows, 1)
    x_last = matrix(1, cols)

    for i in range(rows):
        for j in range(cols):
            x_train[i, j] = time_series[i+j]
        y_train[i, 0] = sum(time_series[i+cols:i+cols+predict_span])

    for i in range(cols):
        x_last[0, i] = time_series[i-cols]

    return x_train, y_train, x_last


def avg_filter(time_series):
    avg = 0
    cnt = 0
    for i in range(len(time_series)):
        if time_series[i] != 0:
            avg += time_series[i]
            cnt += 1
    avg /= cnt

    for i in range(len(time_series)):
        if time_series[i] > avg:
            time_series[i] = avg

    return time_series


def get_pow(time_series, n):
    for i in range(len(time_series)):
        time_series[i] = time_series[i] ** n
    return time_series


def batch_add(time_series, n):
    for i in range(len(time_series)):
        time_series[i] = time_series[i] + n * (i+1) / len(time_series)
    return time_series


def gaussian_weighted(data_mat):
    for i in range(data_mat.rows_):
        for j in range(data_mat.cols_):
            p = 0.0044
            w = math.exp(- math.pow(data_mat[i, j] - data_mat[i, -1], 2) / 2 * p)
            data_mat[i, j] = w * data_mat[i, j]
    return data_mat
