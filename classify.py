import os
import math
from collections import Counter

def create_vocabulary(training_directory, cutoff):
    all_voc = []
    list = os.listdir(training_directory)

    list.remove('.DS_Store') # could remove this line if error happens
    for i in list:
        path = os.path.join(training_directory, i)
        path_list = os.listdir(path)
        for file in path_list:

            f = open(os.path.join(path, file), "r")
            lines = f.read().splitlines()
            for line in lines:
                all_voc.append(line)
            f.close()
    voc_dict = Counter(all_voc)
    voc = []
    for key in voc_dict.keys():
        if voc_dict[key] >= cutoff:
            voc.append(key)
    return voc

def create_bow(vocab, filepath):
    file_voc = []
    f = open(filepath,"r")
    lines = f.read().splitlines()
    for line in lines:
       file_voc.append(line)
    f.close()
    file_dict = Counter(file_voc)
    num_none = 0
    for key, value in file_dict.items():
        if key not in vocab:
            num_none = num_none + value
    if num_none != 0:
        file_dict[None] = num_none
    file_dict = dict(Counter(file_dict))
    return file_dict

def load_training_data(vocab, directory):
    data_list = []
    list = os.listdir(directory)

    list.remove('.DS_Store') # could remove this line if error happens
    for i in list:
        path = os.path.join(directory, i)
        path_list = os.listdir(path)
        for file in path_list:
            bow = create_bow(vocab, os.path.join(path, file))
            data = {}
            data['label'] = i
            data['bow'] = bow
            data_list.append(data)
    return data_list

def prior(training_data, label_list):
    num_1 = 0
    num_2 = 0
    for data in training_data:
        if data['label'] == label_list[0]:
            num_1 = num_1 + 1
        if data['label'] == label_list[1]:
            num_2 = num_2 + 1
    num_all = len(training_data)
    log_1 = math.log(num_1) - math.log(num_all)
    log_2 = math.log(num_2) - math.log(num_all)
    prior_dict = {}
    prior_dict[label_list[0]] = log_1
    prior_dict[label_list[1]] = log_2
    return prior_dict

def p_word_given_label(vocab, training_data, label):
    p = {}
    data_all = []
    p_none = 0

    for data in training_data:
        if data['label'] == label:
            data_all.append(data)

    vocab_size = len(vocab)

    for word in vocab:
        word_all = 0
        for i in data_all:

            if word in i['bow'].keys():
                word_all = word_all + i['bow'][word]
                p[word] = word_all

    for j in data_all:
        if None in j['bow'].keys():
            p_none = p_none + j['bow'][None]
    p[None] = p_none

    data_num = sum(p.values())
    for key, value in p.items():
        p[key] = math.log(value + 1) - math.log(data_num + vocab_size + 1)
    return p

def train(training_directory, cutoff):
    train_dict = {}
    vocab = create_vocabulary(training_directory, cutoff)
    train_dict['vocabulary'] = vocab
    training_data = load_training_data(vocab, training_directory)
    train_dict['log prior'] = prior(training_data, ['2020', '2016'])
    train_dict['log p(w|y=2016)'] = p_word_given_label(vocab, training_data, '2016')
    train_dict['log p(w|y=2020)'] = p_word_given_label(vocab, training_data, '2020')
    return train_dict

def classify(model, filepath):
    vocab = model['vocabulary']
    bow = create_bow(vocab, filepath)
    prior = model['log prior']
    prior_2016 = prior['2016']
    label_2016 = model['log p(w|y=2016)']
    prob_word = 0
    for key in label_2016.keys():
        prob = 0
        if key in bow.keys():
            prob = bow[key] * label_2016[key]
            prob_word = prob_word + prob
    prob_2016 = prob_word + prior_2016

    prior_2020 = prior['2020']
    label_2020 = model['log p(w|y=2020)']
    prob_word2 = 0
    for key in label_2020.keys():
        prob = 0
        if key in bow.keys():
            prob = bow[key] * label_2020[key]
            prob_word2 = prob_word2 + prob
    prob_2020 = prob_word + prior_2020

    prob_dict = {}
    prob_dict['log p(y=2020|x)'] = prob_2020
    prob_dict['log p(y=2016|x)'] = prob_2016
    if prob_2020 > prob_2016:
        prob_dict['predicted y'] = 2020
    else:
        prob_dict['predicted y'] = 2016
    return prob_dict




