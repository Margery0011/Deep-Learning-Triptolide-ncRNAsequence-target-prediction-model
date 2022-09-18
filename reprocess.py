import sys
import numpy as np
import tensorflow.keras
import pandas as pd
import sklearn as sk
import tensorflow as tf
from tensorflow.keras.models import load_model


def mse_check(seq_tt, affi_tt, model, alpha=0.1):
    probas = model.predict(seq_tt)
    errors = 0
    idx = []
    for i in range(probas.shape[0]):
        if (probas[i] > (1 + alpha) * affi_tt[i]) | (probas[i] < (1 - alpha) * affi_tt[i]):
            errors += 1
            idx.append(i)
    er = errors / probas.shape[0]
    print(er)
    return er, idx


def one_hot_check(seq_tt, affi_tt, model, gate):
    probas = model.predict(seq_tt)
    errors = 0
    target = [np.argsort(i)[-1] for i in affi_tt]
    pdt = [np.argsort(i)[-1] for i in probas]
    idx = []
    for i in range(probas.shape[0]):
        if (pdt[i] != target[i]) & (probas[i, target[i]] < gate):
            errors += 1
            idx.append(i)
    er = errors / probas.shape[0]
    print(er)
    return er, idx


def bin_check(seq_tt, affi_tt, model):
    probas = model.predict(seq_tt)
    y_hat = np.zeros(probas.shape)
    for i in range(probas.shape[0]):
        if probas[i, :] > 0.5:
            y_hat[i, :] = 1
        else:
            y_hat[i, :] = 0
    error = 0
    idx = []
    for i in range(probas.shape[0]):
        if y_hat[i] != affi_tt[i]:
            error += 1
            idx.append(i)
    er = error / probas.shape[0]
    print(er)
    return er, idx


def range_check(seq_tt, affi_tt, model, wide):
    probas = model.predict(seq_tt)
    y_test = np.zeros(probas.shape)
    for i in range(probas.shape[0]):
        if affi_tt[i, :] > 0.5:
            y_test[i, :] = 1
        else:
            y_test[i, :] = 0
    error = 0
    idx = []
    for i in range(probas.shape[0]):
        if (probas[i, :][0] >= 0.5 + wide) & (y_test[i, :][0] == 0) | (probas[i, :][0] < 0.5 - wide) & (y_test[i, :][0] == 1):
            error += 1
            idx.append(i)
    er = error / probas.shape[0]
    print(er)
    return er, idx


def de_one_hot(seq):
    raw = []
    A_oh = [1, 0, 0, 0]
    U_oh = [0, 1, 0, 0]
    C_oh = [0, 0, 1, 0]
    G_oh = [0, 0, 0, 1]
    for i in range(seq.shape[0]):
        cache = ''
        for j in range(seq.shape[1]):
            if list(seq[i, j, :]) == A_oh:
                cache += 'A'
            elif list(seq[i, j, :]) == U_oh:
                cache += 'U'
            elif list(seq[i, j, :]) == C_oh:
                cache += 'C'
            elif list(seq[i, j, :]) == G_oh:
                cache += 'G'
        raw.append(cache)
    return raw

