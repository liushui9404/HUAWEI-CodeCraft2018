# -*- coding: utf-8 -*-
import re
import math
import copy

from matrix import matrix
from parsers import read_data
from preprocess import create_dataset
from preprocess import avg_filter
from preprocess import get_pow
from preprocess import batch_add
from preprocess import gaussian_weighted
from linear_regression import linear_regression

total_flavors = 15
predict_span = 7
exponent = 2
addition = 0


def score(predict, actual):
    sum_1 = 0
    sum_2 = 0
    sum_3 = 0

    for i in range(total_flavors):
        sum_1 += math.pow((predict[i] - actual[i]), 2)
        sum_2 += math.pow((predict[i]), 2)
        sum_3 += math.pow(actual[i], 2)
    score_1 = (1 - math.sqrt(sum_1 / total_flavors) / (
                math.sqrt(sum_2 / total_flavors) + math.sqrt(sum_3 / total_flavors)))
    return score_1


if __name__ == '__main__':
    history_data, future_data, sample_ps, sample_vm, dim_to_be_optimized, history_begin, predict_begin, predict_end, flavor_num = read_data()
    lse_model = linear_regression()
    predict = []
    actual = []
    for i in range(total_flavors):
        predict_list = []
        # history_data[i] = avg_filter(history_data[i])
        history_data[i] = get_pow(history_data[i], exponent)
        history_data[i] = batch_add(history_data[i], addition)

        x_train, y_train, x_last = create_dataset(history_data[i], 7, 1)
        x_train = gaussian_weighted(x_train)
        x_last = gaussian_weighted(x_last)
        lse_model.lse_fit(x_train, y_train)
        x_train.show()

        for j in range(predict_span):
            predict_val = lse_model.predict(x_last)
            predict_list.append(predict_val)
            predict_mat = matrix(1, 1, predict_val)
            x_last.col_append(predict_mat)
            x_last.col_deque()

        predict_list = batch_add(predict_list, -addition)
        predict_list = get_pow(predict_list, 1/exponent)

        predict.append(abs(round((sum(predict_list)).real)))
        actual.append((sum(future_data[i])))

        print("Predict:")
        print(predict[-1])
        print("Actual:")
        print(actual[-1])

    print(score(predict, actual))

    # i = 4
    # predict_list = []
    # history_data[i] = avg_filter(history_data[i])
    # history_data[i] = get_pow(history_data[i], exponent)
    # history_data[i] = batch_add(history_data[i], addition)
    # print(history_data[i])
    #
    # x_train, y_train, x_last = create_dataset(history_data[i], 7, 1)
    # x_last.show()
    # print()
    # lse_model.lse_fit(x_train, y_train)
    # lse_model.parm.show()
    # print()
    # for j in range(predict_span):
    #     predict_val = lse_model.predict(x_last)
    #     predict_list.append(predict_val)
    #     predict_mat = matrix(1, 1, predict_val)
    #     x_last.col_append(predict_mat)
    #     x_last.col_deque()
    #
    # predict_list = batch_add(predict_list, -addition)
    # predict_list = get_pow(predict_list, 1/exponent)
    # print("Predict:")
    # print(round((sum(predict_list)).real))
    # print("Actual:")
    # print(sum(future_data[i]))

