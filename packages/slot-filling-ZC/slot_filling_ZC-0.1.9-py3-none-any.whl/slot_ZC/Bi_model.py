import torch
import numpy as np
import random
import torch 
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
import pickle
import json
import re
import os
from math import floor

#read annotation json file
def read_slot(raw_data_path='admin.json',
              ratio=0.7):
    dataset_path='dataset.txt'          
    #load raw data
    data = []
    with open(raw_data_path) as f:
        for line in f:
            data.append(json.loads(line))

    #read slot
    dataset=[]
    for item in data:
        sentence=item['data']
        label=item['label']
        # initializing string
        test_str = sentence
        test_entity = label
        # regex to get words, loop to get each start and end index
        res = [(ele.start(), ele.end() - 1) for ele in re.finditer(r'\S+', test_str)]
        words = test_str.split()

        entity_res = [(label[0],label[1]-1) for label in test_entity]
        entity_name = [label[2] for label in test_entity ]
        # printing result
        # write slot entities
        line=[]
        for i in res:
            key=sentence[i[0]:i[1]+1]
            if i in entity_res:
                for j in test_entity:
                    if i[0]==j[0]:
                        value=j[2]
                        line.append(key+':'+value+' ')
            else:
                line.append(key+':O ')
        dataset.append(line)

    #save 
    textfile = open(dataset_path, "w")
    for sentence in dataset:
        for word in sentence[:-2]:
            textfile.write(word)
        textfile.write("<=> ")
        textfile.write(sentence[-1][7:])
        textfile.write("\n")

    textfile.close()

    #split
    file = open(dataset_path, 'r')
    Lines = file.readlines()
    split = ratio
    split_index = floor(len(Lines) * split)
    training = Lines[:split_index]
    test = Lines[split_index:]

    trainfile=open("train_dev.txt", "w")
    for element in training:
        trainfile.write(element)
    trainfile.close()

    testfile=open("test.txt", "w")
    for element in test:
        testfile.write(element)
    testfile.close()

#make dict
#func1
def convert_int(arr):
    try:
        a = int(arr)
    except:
        return None
    return a

# Make words dict
def make_word_dict(train_file):
    #create a word list	
    words = []
    with open(train_file) as f:
        for line in f.readlines():
            line = line.strip().lower().split()

            for item in enumerate(line):
                word = item.split(':')[0]
                if word == '<=>':
                    break
                if convert_int(word) is not None:
                    words.append('DIGIT' * len(word))
                else:        
                    words.append(word)
    #create a word dict
    words_vocab = sorted(set(words))
    word_dict = {'UNK': 0, 'PAD': 1}
    for i, item in enumerate(words_vocab):
        word_dict[item] = i + 2
    return word_dict


# Make slot tag dict 
def make_slot_dict(vocab_slot_file):
    slot_dict = {}
    with open(vocab_slot_file) as f:
        for i, line in enumerate(f.readlines()):
            slot_dict[line.strip()] = i
    return slot_dict


#make intent dict
def make_intent_dict(vocab_intent_file):
    intent_dict = {}
    with open(vocab_intent_file) as f:
        for i, line in enumerate(f.readlines()):
            intent_dict[line.strip()] = i
    return intent_dict

#use of make_dict
#initialize
def make_all_dict(train_file,
                  vocab_intent_file,
                  vocab_slot_file):
    word_dict=make_word_dict(train_file)
    slot_dict=make_slot_dict(vocab_slot_file)
    intent_dict=make_intent_dict(vocab_intent_file)
    num_intent=len(intent_dict)
    return word_dict, slot_dict, intent_dict, num_intent

#train
def train(train_file = "data/train_dev",
          test_file = "data/test",
          vocab_intent_file = "data/vocab.intent",
          vocab_slot_file = "data/vocab.slot",
          device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
          total_epoch = 50,
          max_len = 50,
          batch = 16,
          learning_rate = 0.001,
          DROPOUT = 0.2,
          embedding_size = 300,
          lstm_hidden_size = 200):
    #save configs for prediction
    configs={}
    configs['max_len'] = max_len
    configs['batch'] = batch
    configs['DROPOUT'] = DROPOUT
    configs['embedding_size'] = embedding_size
    configs['lstm_hidden_size'] = lstm_hidden_size
    with open('predict_config.json', 'w') as filehandle:
        json.dump(configs, filehandle)


    #make dict
    word_dict=make_word_dict(train_file)
    slot_dict=make_slot_dict(vocab_slot_file)
    intent_dict=make_intent_dict(vocab_intent_file)
    num_intent=len(intent_dict)

    #save dict
    with open('word_dict.pickle', 'wb') as handle:
        pickle.dump(word_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('slot_dict.pickle', 'wb') as handle:
        pickle.dump(slot_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('intent_dict.pickle', 'wb') as handle:
        pickle.dump(intent_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


    #utils
    word_dict, slot_dict, intent_dict, num_intent=make_all_dict(train_file,vocab_intent_file,vocab_slot_file)
    #utils functions
    #make mask
    def make_mask(real_len, max_len=max_len, label_size=len(slot_dict), batch=batch):
        mask = torch.zeros(batch, max_len, label_size)
        for index, item in enumerate(real_len):
            mask[index, :item, :] = 1.0
        return mask


    def masked_log_softmax(vector: torch.Tensor, mask: torch.Tensor, dim: int = -1) -> torch.Tensor:
        if mask is not None:
            mask = mask.float()
            while mask.dim() < vector.dim():
                mask = mask.unsqueeze(1)

            vector = vector + (mask + 1e-45).log()
        return torch.nn.functional.log_softmax(vector, dim=dim)


    def one_hot(array, Num=len(slot_dict), maxlen=max_len):

        shape = array.size()
        batch = shape[0]
        if len(shape) == 1:
            res = torch.zeros(batch, Num)
            for i in range(batch):
                res[i][array[i]] = 1
        else:
            res = torch.zeros(batch, maxlen, Num)
            for i in range(batch):
                for j in range(maxlen):
                    if array[i, j] == Num:
                        pass
                    else:
                        res[i][j][array[i, j]] = 1

        return res

    def get_batch(data, batch_size=batch):
        random.shuffle(data)
        sindex = 0
        eindex = batch_size
        while eindex < len(data):

            sentence = []
            real_len = []
            slot_label = []
            intent_label = []
            
            batch = data[sindex:eindex]
            for m in range(sindex, eindex):
                sentence.append(data[m][0])
                real_len.append(data[m][1])
                slot_label.append(data[m][2])
                intent_label.append(data[m][3])

            temp = eindex
            eindex = eindex + batch_size
            sindex = temp

            yield (sentence, real_len, slot_label, intent_label)

    def get_chunks(labels):
        chunks = []
        start_idx,end_idx = 0,0
        for idx in range(1,len(labels)-1):
            chunkStart, chunkEnd = False,False
            if labels[idx-1] not in ('O', '<pad>', '<unk>', '<s>', '</s>', '<STOP>', '<START>'):
                prevTag, prevType = labels[idx-1][:1], labels[idx-1][2:]
            else:
                prevTag, prevType = 'O', 'O'
            if labels[idx] not in ('O', '<pad>', '<unk>', '<s>', '</s>', '<STOP>', '<START>'):
                Tag, Type = labels[idx][:1], labels[idx][2:]
            else:
                Tag, Type = 'O', 'O'
            if labels[idx+1] not in ('O', '<pad>', '<unk>', '<s>', '</s>', '<STOP>', '<START>'):
                nextTag, nextType = labels[idx+1][:1], labels[idx+1][2:]
            else:
                nextTag, nextType = 'O', 'O'

            if (Tag == 'B' and prevTag in ('B', 'I', 'O')) or (prevTag, Tag) in [('O', 'I'), ('E', 'E'), ('E', 'I'), ('O', 'E')]:
                chunkStart = True
            if Tag != 'O' and prevType != Type:
                chunkStart = True

            if (Tag in ('B','I') and nextTag in ('B','O')) or (Tag == 'E' and nextTag in ('E', 'I', 'O')):
                chunkEnd = True
            if Tag != 'O' and Type != nextType:
                chunkEnd = True

            if chunkStart:
                start_idx = idx
            if chunkEnd:
                end_idx = idx
                chunks.append((start_idx,end_idx,Type))
                start_idx,end_idx = 0,0
        return chunks

    #Model
    # Bi-model 
    class slot_enc(nn.Module):
        def __init__(self, embedding_size, lstm_hidden_size, vocab_size=len(word_dict)):
            super(slot_enc, self).__init__()

            self.embedding = nn.Embedding(vocab_size, embedding_size).to(device)
            self.lstm = nn.LSTM(input_size=embedding_size, hidden_size=lstm_hidden_size, num_layers=2,\
                                bidirectional= True, batch_first=True) #, dropout=DROPOUT)

        def forward(self, x):
            x = self.embedding(x)
            x = F.dropout(x, DROPOUT)       
            x, _ = self.lstm(x)
            x = F.dropout(x, DROPOUT)
            return x 


    class slot_dec(nn.Module):
        def __init__(self, lstm_hidden_size, label_size=len(slot_dict)):
            super(slot_dec, self).__init__()
            self.lstm = nn.LSTM(input_size=lstm_hidden_size*5, hidden_size=lstm_hidden_size, num_layers=1)
            self.fc = nn.Linear(lstm_hidden_size, label_size)
            self.hidden_size = lstm_hidden_size

        def forward(self, x, hi):
            batch = x.size(0)
            length = x.size(1)
            dec_init_out = torch.zeros(batch, 1, self.hidden_size).to(device)
            hidden_state = (torch.zeros(1, 1, self.hidden_size).to(device), \
                            torch.zeros(1, 1, self.hidden_size).to(device))
            x = torch.cat((x, hi), dim=-1)

            x = x.transpose(1, 0)  # 50 x batch x feature_size
            x = F.dropout(x, DROPOUT)
            all_out = []
            for i in range(length):
                if i == 0:
                    out, hidden_state = self.lstm(torch.cat((x[i].unsqueeze(1), dec_init_out), dim=-1), hidden_state)
                else:
                    out, hidden_state = self.lstm(torch.cat((x[i].unsqueeze(1), out), dim=-1), hidden_state)
                all_out.append(out)
            output = torch.cat(all_out, dim=1) # 50 x batch x feature_size
            x = F.dropout(x, DROPOUT)
            res = self.fc(output)
            return res 

    class intent_enc(nn.Module):
        def __init__(self, embedding_size, lstm_hidden_size, vocab_size=len(word_dict)):
            super(intent_enc, self).__init__()
            
            self.embedding = nn.Embedding(vocab_size, embedding_size).to(device)
            # self.embedding.weight.data.uniform_(-1.0, 1.0)
            self.lstm = nn.LSTM(input_size=embedding_size, hidden_size= lstm_hidden_size, num_layers=2,\
                                bidirectional= True, batch_first=True, dropout=DROPOUT)
        
        def forward(self, x):
            x = self.embedding(x)
            x = F.dropout(x, DROPOUT)
            x, _ = self.lstm(x)
            x = F.dropout(x, DROPOUT)
            return x

    class intent_dec(nn.Module):
        def __init__(self, lstm_hidden_size, label_size=len(intent_dict)):
            super(intent_dec, self).__init__()
            self.lstm = nn.LSTM(input_size=lstm_hidden_size*4, hidden_size=lstm_hidden_size, batch_first=True, num_layers=1)#, dropout=DROPOUT)
            self.fc = nn.Linear(lstm_hidden_size, label_size)
            
        def forward(self, x, hs, real_len):
            batch = x.size()[0]
            real_len = torch.tensor(real_len).to(device)
            x = torch.cat((x, hs), dim=-1)
            x = F.dropout(x, DROPOUT)
            x, _ = self.lstm(x)
            x = F.dropout(x, DROPOUT)

            index = torch.arange(batch).long().to(device)
            state = x[index, real_len-1, :]
            
            res = self.fc(state.squeeze())
            return res
            
    class Intent(nn.Module):
        def __init__(self):
            super(Intent, self).__init__()
            self.enc = intent_enc(embedding_size, lstm_hidden_size).to(device)
            self.dec = intent_dec(lstm_hidden_size).to(device)
            self.share_memory = torch.zeros(batch, max_len, lstm_hidden_size * 2).to(device)
        

    class Slot(nn.Module):
        def __init__(self):
            super(Slot, self).__init__()
            self.enc = slot_enc(embedding_size, lstm_hidden_size).to(device)
            self.dec = slot_dec(lstm_hidden_size).to(device)
            self.share_memory = torch.zeros(batch, max_len, lstm_hidden_size * 2).to(device)
            
    #Index function
    def makeindex(filename):
        train_data = []
        with open(filename) as f:
            for line in f.readlines():
                line = line.strip().split()
                sample_sentence = []
                sample_slot = []
                for index, item in enumerate(line):
                    word = item.split(':')[0] 

                    if word == '<=>':
                        real_length = index
                        break
                    if convert_int(word) is not None:
                        word =  'DIGIT' * len(word)
                    else:
                        pass
                    slot = item.rsplit(':',1)[1]

                    if word in word_dict:
                        sample_sentence.append(word_dict[word])
                    else:
                        sample_sentence.append(word_dict['UNK'])

                    sample_slot.append(slot_dict[slot])

                    train_intent = intent_dict[ line[-1].split(';')[0] ]

                while len(sample_sentence) < max_len:
                    sample_sentence.append(word_dict['PAD'])
                while len(sample_slot) < max_len:
                    sample_slot.append(slot_dict['O'])

                train_data.append([sample_sentence, real_length, sample_slot, train_intent])
        return train_data

    #prepare index
    train_data = makeindex(train_file)
    test_data = makeindex(test_file)
    #make index2slot dict
    index2slot_dict = {}
    for key in slot_dict:
        index2slot_dict[slot_dict[key]] = key

    print('Number of training samples: ', len(train_data))
    print('Number of test samples: ', len(test_data))
    print('Number of words: ', len(word_dict))
    print('Number of intent labels: ', len(intent_dict))
    print('Number of slot labels', len(slot_dict))

    #define some parameters
    epoch_num = total_epoch
    slot_model = Slot().to(device)
    intent_model = Intent().to(device)

    print(slot_model)
    print(intent_model)

    slot_optimizer = optim.Adam(slot_model.parameters(), lr=learning_rate)       # optim.Adamax
    intent_optimizer = optim.Adam(intent_model.parameters(), lr=learning_rate)   # optim.Adamax

    best_correct_num = 0
    best_epoch = -1
    best_F1_score = 0.0
    best_epoch_slot = -1
    #start training
    for epoch in range(epoch_num):
        slot_loss_history = []
        intent_loss_history = []
        for batch_index, data in enumerate(get_batch(train_data)):

            # Preparing data
            sentence, real_len, slot_label, intent_label = data

            mask = make_mask(real_len).to(device)
            x = torch.tensor(sentence).to(device)
            y_slot = torch.tensor(slot_label).to(device)
            y_slot = one_hot(y_slot).to(device)
            y_intent = torch.tensor(intent_label).to(device)
            y_intent = one_hot(y_intent, Num=num_intent).to(device)

            # Calculate compute graph
            slot_optimizer.zero_grad()
            intent_optimizer.zero_grad()
            
            hs = slot_model.enc(x)
            slot_model.share_memory = hs.clone()

            hi = intent_model.enc(x)
            intent_model.share_memory = hi.clone()
            
            
            slot_logits = slot_model.dec(hs, intent_model.share_memory.detach())
            log_slot_logits = masked_log_softmax(slot_logits, mask, dim=-1)
            slot_loss = -1.0*torch.sum(y_slot*log_slot_logits)
            slot_loss_history.append(slot_loss.item())
            slot_loss.backward()
            torch.nn.utils.clip_grad_norm_(slot_model.parameters(), 5.0)
            slot_optimizer.step()

            # Asynchronous training
            intent_logits = intent_model.dec(hi, slot_model.share_memory.detach(), real_len)
            log_intent_logits = F.log_softmax(intent_logits, dim=-1)
            intent_loss = -1.0*torch.sum(y_intent*log_intent_logits)
            intent_loss_history.append(intent_loss.item())
            intent_loss.backward()
            torch.nn.utils.clip_grad_norm_(intent_model.parameters(), 5.0)
            intent_optimizer.step()
            
            # Log
            if batch_index % 100 == 0 and batch_index > 0:
                print('Slot loss: {:.4f} \t Intent loss: {:.4f}'.format(sum(slot_loss_history[-100:])/100.0, \
                    sum(intent_loss_history[-100:])/100.0))

        # Evaluation 
        total_test = len(test_data)
        correct_num = 0
        TP, FP, FN = 0, 0, 0
        for batch_index, data_test in enumerate(get_batch(test_data, batch_size=1)):
            sentence_test, real_len_test, slot_label_test, intent_label_test = data_test
            # print(sentence[0].shape, real_len.shape, slot_label.shape)
            x_test = torch.tensor(sentence_test).to(device)

            mask_test = make_mask(real_len_test, batch=1).to(device)
            # Slot model generate hs_test and intent model generate hi_test
            hs_test = slot_model.enc(x_test)
            hi_test = intent_model.enc(x_test)

            # Slot
            slot_logits_test = slot_model.dec(hs_test, hi_test)
            log_slot_logits_test = masked_log_softmax(slot_logits_test, mask_test, dim=-1)
            slot_pred_test = torch.argmax(log_slot_logits_test, dim=-1)
            # Intent
            intent_logits_test = intent_model.dec(hi_test, hs_test, real_len_test)
            log_intent_logits_test = F.log_softmax(intent_logits_test, dim=-1)
            res_test = torch.argmax(log_intent_logits_test, dim=-1)
            

            if res_test.item() == intent_label_test[0]:
                correct_num += 1
            if correct_num > best_correct_num:
                best_correct_num = correct_num
                best_epoch = epoch
                
                # Save and load the entire model.
                torch.save(intent_model.state_dict(), 'model_intent_best.pt')
                torch.save(slot_model.state_dict(), 'model_slot_best.pt')
        
            # Calc slot F1 score
            
            slot_pred_test = slot_pred_test[0][:real_len_test[0]]
            slot_label_test = slot_label_test[0][:real_len_test[0]]

            slot_pred_test = [int(item) for item in slot_pred_test]
            slot_label_test = [int(item) for item in slot_label_test]

            slot_pred_test = [index2slot_dict[item] for item in slot_pred_test]
            slot_label_test = [index2slot_dict[item] for item in slot_label_test]

            pred_chunks = get_chunks(['O'] + slot_pred_test + ['O'])
            label_chunks = get_chunks(['O'] + slot_label_test + ['O'])
            for pred_chunk in pred_chunks:
                if pred_chunk in label_chunks:
                    TP += 1
                else:
                    FP += 1
            for label_chunk in label_chunks:
                if label_chunk not in pred_chunks:
                    FN += 1

        F1_score = 100.0*2*TP/(2*TP+FN+FP)
        if F1_score > best_F1_score:
            best_F1_score = F1_score
            best_epoch_slot = epoch
        print('*'*20)
        print('Epoch: [{}/{}], Intent Val Acc: {:.4f} \t Slot F1 score: {:.4f}'.format(epoch+1, epoch_num, 100.0*correct_num/total_test, F1_score))
        print('*'*20)
        
        print('Best Intent Acc: {:.4f} at Epoch: [{}]'.format(100.0*best_correct_num/total_test, best_epoch+1))
        print('Best F1 score: {:.4f} at Epoch: [{}]'.format(best_F1_score, best_epoch_slot+1))

def fine_tune(train_file = "data/train_dev",
              test_file = "data/test",
              vocab_intent_file = "data/vocab.intent",
              vocab_slot_file = "data/vocab.slot",
              slot_model_path="model_slot_best.pt",
              intent_model_path="model_intent_best.pt",
              device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
              total_epoch = 50,
              max_len = 50,
              batch = 16,
              learning_rate = 0.001,
              DROPOUT = 0.2,
              embedding_size = 300,
              lstm_hidden_size = 200):
    #updata training data
    word_dict=make_word_dict(train_file)
    slot_dict=make_slot_dict(vocab_slot_file)
    intent_dict=make_intent_dict(vocab_intent_file)
    num_intent=len(intent_dict)

    #save dict
    with open('word_dict.pickle', 'wb') as handle:
        pickle.dump(word_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('slot_dict.pickle', 'wb') as handle:
        pickle.dump(slot_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('intent_dict.pickle', 'wb') as handle:
        pickle.dump(intent_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #utils
    word_dict, slot_dict, intent_dict, num_intent=make_all_dict(train_file,vocab_intent_file,vocab_slot_file)
    #utils functions
    #make mask
    def make_mask(real_len, max_len=max_len, label_size=len(slot_dict), batch=batch):
        mask = torch.zeros(batch, max_len, label_size)
        for index, item in enumerate(real_len):
            mask[index, :item, :] = 1.0
        return mask


    def masked_log_softmax(vector: torch.Tensor, mask: torch.Tensor, dim: int = -1) -> torch.Tensor:
        if mask is not None:
            mask = mask.float()
            while mask.dim() < vector.dim():
                mask = mask.unsqueeze(1)

            vector = vector + (mask + 1e-45).log()
        return torch.nn.functional.log_softmax(vector, dim=dim)


    def one_hot(array, Num=len(slot_dict), maxlen=max_len):

        shape = array.size()
        batch = shape[0]
        if len(shape) == 1:
            res = torch.zeros(batch, Num)
            for i in range(batch):
                res[i][array[i]] = 1
        else:
            res = torch.zeros(batch, maxlen, Num)
            for i in range(batch):
                for j in range(maxlen):
                    if array[i, j] == Num:
                        pass
                    else:
                        res[i][j][array[i, j]] = 1

        return res

    def get_batch(data, batch_size=batch):
        random.shuffle(data)
        sindex = 0
        eindex = batch_size
        while eindex < len(data):

            sentence = []
            real_len = []
            slot_label = []
            intent_label = []
            
            batch = data[sindex:eindex]
            for m in range(sindex, eindex):
                sentence.append(data[m][0])
                real_len.append(data[m][1])
                slot_label.append(data[m][2])
                intent_label.append(data[m][3])

            temp = eindex
            eindex = eindex + batch_size
            sindex = temp

            yield (sentence, real_len, slot_label, intent_label)

    def get_chunks(labels):
        chunks = []
        start_idx,end_idx = 0,0
        for idx in range(1,len(labels)-1):
            chunkStart, chunkEnd = False,False
            if labels[idx-1] not in ('O', '<pad>', '<unk>', '<s>', '</s>', '<STOP>', '<START>'):
                prevTag, prevType = labels[idx-1][:1], labels[idx-1][2:]
            else:
                prevTag, prevType = 'O', 'O'
            if labels[idx] not in ('O', '<pad>', '<unk>', '<s>', '</s>', '<STOP>', '<START>'):
                Tag, Type = labels[idx][:1], labels[idx][2:]
            else:
                Tag, Type = 'O', 'O'
            if labels[idx+1] not in ('O', '<pad>', '<unk>', '<s>', '</s>', '<STOP>', '<START>'):
                nextTag, nextType = labels[idx+1][:1], labels[idx+1][2:]
            else:
                nextTag, nextType = 'O', 'O'

            if (Tag == 'B' and prevTag in ('B', 'I', 'O')) or (prevTag, Tag) in [('O', 'I'), ('E', 'E'), ('E', 'I'), ('O', 'E')]:
                chunkStart = True
            if Tag != 'O' and prevType != Type:
                chunkStart = True

            if (Tag in ('B','I') and nextTag in ('B','O')) or (Tag == 'E' and nextTag in ('E', 'I', 'O')):
                chunkEnd = True
            if Tag != 'O' and Type != nextType:
                chunkEnd = True

            if chunkStart:
                start_idx = idx
            if chunkEnd:
                end_idx = idx
                chunks.append((start_idx,end_idx,Type))
                start_idx,end_idx = 0,0
        return chunks
    #load model
    # Bi-model 
    class slot_enc(nn.Module):
        def __init__(self, embedding_size, lstm_hidden_size, vocab_size=len(word_dict)):
            super(slot_enc, self).__init__()

            self.embedding = nn.Embedding(vocab_size, embedding_size).to(device)
            self.lstm = nn.LSTM(input_size=embedding_size, hidden_size=lstm_hidden_size, num_layers=2,\
                                bidirectional= True, batch_first=True) #, dropout=DROPOUT)

        def forward(self, x):
            x = self.embedding(x)
            x = F.dropout(x, DROPOUT)       
            x, _ = self.lstm(x)
            x = F.dropout(x, DROPOUT)
            return x 


    class slot_dec(nn.Module):
        def __init__(self, lstm_hidden_size, label_size=len(slot_dict)):
            super(slot_dec, self).__init__()
            self.lstm = nn.LSTM(input_size=lstm_hidden_size*5, hidden_size=lstm_hidden_size, num_layers=1)
            self.fc = nn.Linear(lstm_hidden_size, label_size)
            self.hidden_size = lstm_hidden_size

        def forward(self, x, hi):
            batch = x.size(0)
            length = x.size(1)
            dec_init_out = torch.zeros(batch, 1, self.hidden_size).to(device)
            hidden_state = (torch.zeros(1, 1, self.hidden_size).to(device), \
                            torch.zeros(1, 1, self.hidden_size).to(device))
            x = torch.cat((x, hi), dim=-1)

            x = x.transpose(1, 0)  # 50 x batch x feature_size
            x = F.dropout(x, DROPOUT)
            all_out = []
            for i in range(length):
                if i == 0:
                    out, hidden_state = self.lstm(torch.cat((x[i].unsqueeze(1), dec_init_out), dim=-1), hidden_state)
                else:
                    out, hidden_state = self.lstm(torch.cat((x[i].unsqueeze(1), out), dim=-1), hidden_state)
                all_out.append(out)
            output = torch.cat(all_out, dim=1) # 50 x batch x feature_size
            x = F.dropout(x, DROPOUT)
            res = self.fc(output)
            return res 

    class intent_enc(nn.Module):
        def __init__(self, embedding_size, lstm_hidden_size, vocab_size=len(word_dict)):
            super(intent_enc, self).__init__()
            
            self.embedding = nn.Embedding(vocab_size, embedding_size).to(device)
            # self.embedding.weight.data.uniform_(-1.0, 1.0)
            self.lstm = nn.LSTM(input_size=embedding_size, hidden_size= lstm_hidden_size, num_layers=2,\
                                bidirectional= True, batch_first=True, dropout=DROPOUT)
        
        def forward(self, x):
            x = self.embedding(x)
            x = F.dropout(x, DROPOUT)
            x, _ = self.lstm(x)
            x = F.dropout(x, DROPOUT)
            return x

    class intent_dec(nn.Module):
        def __init__(self, lstm_hidden_size, label_size=len(intent_dict)):
            super(intent_dec, self).__init__()
            self.lstm = nn.LSTM(input_size=lstm_hidden_size*4, hidden_size=lstm_hidden_size, batch_first=True, num_layers=1)#, dropout=DROPOUT)
            self.fc = nn.Linear(lstm_hidden_size, label_size)
            
        def forward(self, x, hs, real_len):
            batch = x.size()[0]
            real_len = torch.tensor(real_len).to(device)
            x = torch.cat((x, hs), dim=-1)
            x = F.dropout(x, DROPOUT)
            x, _ = self.lstm(x)
            x = F.dropout(x, DROPOUT)

            index = torch.arange(batch).long().to(device)
            state = x[index, real_len-1, :]
            
            res = self.fc(state.squeeze())
            return res
            
    class Intent(nn.Module):
        def __init__(self):
            super(Intent, self).__init__()
            self.enc = intent_enc(embedding_size, lstm_hidden_size).to(device)
            self.dec = intent_dec(lstm_hidden_size).to(device)
            self.share_memory = torch.zeros(batch, max_len, lstm_hidden_size * 2).to(device)
        

    class Slot(nn.Module):
        def __init__(self):
            super(Slot, self).__init__()
            self.enc = slot_enc(embedding_size, lstm_hidden_size).to(device)
            self.dec = slot_dec(lstm_hidden_size).to(device)
            self.share_memory = torch.zeros(batch, max_len, lstm_hidden_size * 2).to(device)

    slot_model = Slot().to(device)
    intent_model = Intent().to(device) 


    slot_model.load_state_dict(torch.load(slot_model_path), strict=False)

    intent_model.load_state_dict(torch.load(intent_model_path), strict=False)

    #Index function
    def makeindex(filename):
        train_data = []
        with open(filename) as f:
            for line in f.readlines():
                line = line.strip().split()
                sample_sentence = []
                sample_slot = []
                for index, item in enumerate(line):
                    word = item.split(':')[0] 

                    if word == '<=>':
                        real_length = index
                        break
                    if convert_int(word) is not None:
                        word =  'DIGIT' * len(word)
                    else:
                        pass
                    slot = item.rsplit(':',1)[1]

                    if word in word_dict:
                        sample_sentence.append(word_dict[word])
                    else:
                        sample_sentence.append(word_dict['UNK'])

                    sample_slot.append(slot_dict[slot])

                    train_intent = intent_dict[ line[-1].split(';')[0] ]

                while len(sample_sentence) < max_len:
                    sample_sentence.append(word_dict['PAD'])
                while len(sample_slot) < max_len:
                    sample_slot.append(slot_dict['O'])

                train_data.append([sample_sentence, real_length, sample_slot, train_intent])
        return train_data

    #prepare index
    train_data = makeindex(train_file)
    test_data = makeindex(test_file)
    #make index2slot dict
    index2slot_dict = {}
    for key in slot_dict:
        index2slot_dict[slot_dict[key]] = key

    print('Number of training samples: ', len(train_data))
    print('Number of test samples: ', len(test_data))
    print('Number of words: ', len(word_dict))
    print('Number of intent labels: ', len(intent_dict))
    print('Number of slot labels', len(slot_dict))

    #define some parameters
    epoch_num = total_epoch
    slot_model = Slot().to(device)
    intent_model = Intent().to(device)

    print(slot_model)
    print(intent_model)

    slot_optimizer = optim.Adam(slot_model.parameters(), lr=learning_rate)       # optim.Adamax
    intent_optimizer = optim.Adam(intent_model.parameters(), lr=learning_rate)   # optim.Adamax

    best_correct_num = 0
    best_epoch = -1
    best_F1_score = 0.0
    best_epoch_slot = -1
    #start training
    for epoch in range(epoch_num):
        slot_loss_history = []
        intent_loss_history = []
        for batch_index, data in enumerate(get_batch(train_data)):

            # Preparing data
            sentence, real_len, slot_label, intent_label = data

            mask = make_mask(real_len).to(device)
            x = torch.tensor(sentence).to(device)
            y_slot = torch.tensor(slot_label).to(device)
            y_slot = one_hot(y_slot).to(device)
            y_intent = torch.tensor(intent_label).to(device)
            y_intent = one_hot(y_intent, Num=num_intent).to(device)

            # Calculate compute graph
            slot_optimizer.zero_grad()
            intent_optimizer.zero_grad()
            
            hs = slot_model.enc(x)
            slot_model.share_memory = hs.clone()

            hi = intent_model.enc(x)
            intent_model.share_memory = hi.clone()
            
            
            slot_logits = slot_model.dec(hs, intent_model.share_memory.detach())
            log_slot_logits = masked_log_softmax(slot_logits, mask, dim=-1)
            slot_loss = -1.0*torch.sum(y_slot*log_slot_logits)
            slot_loss_history.append(slot_loss.item())
            slot_loss.backward()
            torch.nn.utils.clip_grad_norm_(slot_model.parameters(), 5.0)
            slot_optimizer.step()

            # Asynchronous training
            intent_logits = intent_model.dec(hi, slot_model.share_memory.detach(), real_len)
            log_intent_logits = F.log_softmax(intent_logits, dim=-1)
            intent_loss = -1.0*torch.sum(y_intent*log_intent_logits)
            intent_loss_history.append(intent_loss.item())
            intent_loss.backward()
            torch.nn.utils.clip_grad_norm_(intent_model.parameters(), 5.0)
            intent_optimizer.step()
            
            # Log
            if batch_index % 100 == 0 and batch_index > 0:
                print('Slot loss: {:.4f} \t Intent loss: {:.4f}'.format(sum(slot_loss_history[-100:])/100.0, \
                    sum(intent_loss_history[-100:])/100.0))

        # Evaluation 
        total_test = len(test_data)
        correct_num = 0
        TP, FP, FN = 0, 0, 0
        for batch_index, data_test in enumerate(get_batch(test_data, batch_size=1)):
            sentence_test, real_len_test, slot_label_test, intent_label_test = data_test
            # print(sentence[0].shape, real_len.shape, slot_label.shape)
            x_test = torch.tensor(sentence_test).to(device)

            mask_test = make_mask(real_len_test, batch=1).to(device)
            # Slot model generate hs_test and intent model generate hi_test
            hs_test = slot_model.enc(x_test)
            hi_test = intent_model.enc(x_test)

            # Slot
            slot_logits_test = slot_model.dec(hs_test, hi_test)
            log_slot_logits_test = masked_log_softmax(slot_logits_test, mask_test, dim=-1)
            slot_pred_test = torch.argmax(log_slot_logits_test, dim=-1)
            # Intent
            intent_logits_test = intent_model.dec(hi_test, hs_test, real_len_test)
            log_intent_logits_test = F.log_softmax(intent_logits_test, dim=-1)
            res_test = torch.argmax(log_intent_logits_test, dim=-1)
            

            if res_test.item() == intent_label_test[0]:
                correct_num += 1
            if correct_num > best_correct_num:
                best_correct_num = correct_num
                best_epoch = epoch
                
                # Save and load the entire model.
                torch.save(intent_model.state_dict(), 'model_intent_best.pt')
                torch.save(slot_model.state_dict(), 'model_slot_best.pt')
        
            # Calc slot F1 score
            
            slot_pred_test = slot_pred_test[0][:real_len_test[0]]
            slot_label_test = slot_label_test[0][:real_len_test[0]]

            slot_pred_test = [int(item) for item in slot_pred_test]
            slot_label_test = [int(item) for item in slot_label_test]

            slot_pred_test = [index2slot_dict[item] for item in slot_pred_test]
            slot_label_test = [index2slot_dict[item] for item in slot_label_test]

            pred_chunks = get_chunks(['O'] + slot_pred_test + ['O'])
            label_chunks = get_chunks(['O'] + slot_label_test + ['O'])
            for pred_chunk in pred_chunks:
                if pred_chunk in label_chunks:
                    TP += 1
                else:
                    FP += 1
            for label_chunk in label_chunks:
                if label_chunk not in pred_chunks:
                    FN += 1

        F1_score = 100.0*2*TP/(2*TP+FN+FP)
        if F1_score > best_F1_score:
            best_F1_score = F1_score
            best_epoch_slot = epoch
        print('*'*20)
        print('Epoch: [{}/{}], Intent Val Acc: {:.4f} \t Slot F1 score: {:.4f}'.format(epoch+1, epoch_num, 100.0*correct_num/total_test, F1_score))
        print('*'*20)
        
        print('Best Intent Acc: {:.4f} at Epoch: [{}]'.format(100.0*best_correct_num/total_test, best_epoch+1))
        print('Best F1 score: {:.4f} at Epoch: [{}]'.format(best_F1_score, best_epoch_slot+1))

def load_model(data_path="/Users/chenzichu/Desktop/slot-filling/package/slot_ZC",
               device = torch.device("cuda" if torch.cuda.is_available() else "cpu")):
    #file path
    slot_model_path=os.path.join(data_path,"model_slot_best.pt")
    intent_model_path=os.path.join(data_path,"model_intent_best.pt")
    word_dict_path=os.path.join(data_path,"word_dict.pickle")
    slot_dict_path=os.path.join(data_path,"slot_dict.pickle")
    intent_dict_path=os.path.join(data_path,"intent_dict.pickle")
    config_path=os.path.join(data_path,"predict_config.json")
    #load dicts
    with open(word_dict_path, 'rb') as handle:
        word_dict = pickle.load(handle)
    with open(slot_dict_path, 'rb') as handle:
        slot_dict = pickle.load(handle)
    with open(intent_dict_path, 'rb') as handle:
        intent_dict = pickle.load(handle)
    intent_dict=intent_dict
    index2slot_dict = {}
    for key in slot_dict:
        index2slot_dict[slot_dict[key]] = key
    #load configs
    f=open(config_path)
    configs = json.load(f)
    max_len=configs['max_len']
    batch=configs['batch']
    DROPOUT=configs['DROPOUT']
    embedding_size=configs['embedding_size']
    lstm_hidden_size=configs['lstm_hidden_size']
     #load model
    # Bi-model 
    class slot_enc(nn.Module):
        def __init__(self, embedding_size, lstm_hidden_size, vocab_size=len(word_dict)):
            super(slot_enc, self).__init__()

            self.embedding = nn.Embedding(vocab_size, embedding_size).to(device)
            self.lstm = nn.LSTM(input_size=embedding_size, hidden_size=lstm_hidden_size, num_layers=2,\
                                bidirectional= True, batch_first=True) #, dropout=DROPOUT)

        def forward(self, x):
            x = self.embedding(x)
            x = F.dropout(x, DROPOUT)       
            x, _ = self.lstm(x)
            x = F.dropout(x, DROPOUT)
            return x 


    class slot_dec(nn.Module):
        def __init__(self, lstm_hidden_size, label_size=len(slot_dict)):
            super(slot_dec, self).__init__()
            self.lstm = nn.LSTM(input_size=lstm_hidden_size*5, hidden_size=lstm_hidden_size, num_layers=1)
            self.fc = nn.Linear(lstm_hidden_size, label_size)
            self.hidden_size = lstm_hidden_size

        def forward(self, x, hi):
            batch = x.size(0)
            length = x.size(1)
            dec_init_out = torch.zeros(batch, 1, self.hidden_size).to(device)
            hidden_state = (torch.zeros(1, 1, self.hidden_size).to(device), \
                            torch.zeros(1, 1, self.hidden_size).to(device))
            x = torch.cat((x, hi), dim=-1)

            x = x.transpose(1, 0)  # 50 x batch x feature_size
            x = F.dropout(x, DROPOUT)
            all_out = []
            for i in range(length):
                if i == 0:
                    out, hidden_state = self.lstm(torch.cat((x[i].unsqueeze(1), dec_init_out), dim=-1), hidden_state)
                else:
                    out, hidden_state = self.lstm(torch.cat((x[i].unsqueeze(1), out), dim=-1), hidden_state)
                all_out.append(out)
            output = torch.cat(all_out, dim=1) # 50 x batch x feature_size
            x = F.dropout(x, DROPOUT)
            res = self.fc(output)
            return res 

    class intent_enc(nn.Module):
        def __init__(self, embedding_size, lstm_hidden_size, vocab_size=len(word_dict)):
            super(intent_enc, self).__init__()
            
            self.embedding = nn.Embedding(vocab_size, embedding_size).to(device)
            # self.embedding.weight.data.uniform_(-1.0, 1.0)
            self.lstm = nn.LSTM(input_size=embedding_size, hidden_size= lstm_hidden_size, num_layers=2,\
                                bidirectional= True, batch_first=True, dropout=DROPOUT)
        
        def forward(self, x):
            x = self.embedding(x)
            x = F.dropout(x, DROPOUT)
            x, _ = self.lstm(x)
            x = F.dropout(x, DROPOUT)
            return x

    class intent_dec(nn.Module):
        def __init__(self, lstm_hidden_size, label_size=len(intent_dict)):
            super(intent_dec, self).__init__()
            self.lstm = nn.LSTM(input_size=lstm_hidden_size*4, hidden_size=lstm_hidden_size, batch_first=True, num_layers=1)#, dropout=DROPOUT)
            self.fc = nn.Linear(lstm_hidden_size, label_size)
            
        def forward(self, x, hs, real_len):
            batch = x.size()[0]
            real_len = torch.tensor(real_len).to(device)
            x = torch.cat((x, hs), dim=-1)
            x = F.dropout(x, DROPOUT)
            x, _ = self.lstm(x)
            x = F.dropout(x, DROPOUT)

            index = torch.arange(batch).long().to(device)
            state = x[index, real_len-1, :]
            
            res = self.fc(state.squeeze())
            return res
            
    class Intent(nn.Module):
        def __init__(self):
            super(Intent, self).__init__()
            self.enc = intent_enc(embedding_size, lstm_hidden_size).to(device)
            self.dec = intent_dec(lstm_hidden_size).to(device)
            self.share_memory = torch.zeros(batch, max_len, lstm_hidden_size * 2).to(device)
        

    class Slot(nn.Module):
        def __init__(self):
            super(Slot, self).__init__()
            self.enc = slot_enc(embedding_size, lstm_hidden_size).to(device)
            self.dec = slot_dec(lstm_hidden_size).to(device)
            self.share_memory = torch.zeros(batch, max_len, lstm_hidden_size * 2).to(device)

    slot_model = Slot().to(device)
    intent_model = Intent().to(device) 
    slot_model.load_state_dict(torch.load(slot_model_path), strict=False)
    intent_model.load_state_dict(torch.load(intent_model_path), strict=False)
    return slot_model,intent_model

def predict(sentence,
            slot_model,
            intent_model,
            data_path="/Users/chenzichu/Desktop/slot-filling/package/slot_ZC",
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")):
    #file path
    word_dict_path=os.path.join(data_path,"word_dict.pickle")
    slot_dict_path=os.path.join(data_path,"slot_dict.pickle")
    intent_dict_path=os.path.join(data_path,"intent_dict.pickle")
    config_path=os.path.join(data_path,"predict_config.json")
    #load dicts
    with open(word_dict_path, 'rb') as handle:
        word_dict = pickle.load(handle)
    with open(slot_dict_path, 'rb') as handle:
        slot_dict = pickle.load(handle)
    with open(intent_dict_path, 'rb') as handle:
        intent_dict = pickle.load(handle)
    intent_dict=intent_dict
    index2slot_dict = {}
    for key in slot_dict:
        index2slot_dict[slot_dict[key]] = key
    #max_len
    #load configs
    f=open(config_path)
    configs = json.load(f)
    max_len=configs['max_len']
    #functions
    def makeoneindex(line):
        predict_data = []
        line = line.strip().split()
        sample_sentence = []
        real_length=0
        print(line)
        for item in line:
            real_length+=1
            word = item.split(' ')[0] 
            if convert_int(word) is not None:
                word =  'DIGIT' * len(word)
            else:
                pass

            if word in word_dict:
                sample_sentence.append(word_dict[word])
            else:
                sample_sentence.append(word_dict['UNK'])

        while len(sample_sentence) < max_len:
            sample_sentence.append(word_dict['PAD'])
        predict_data.append(sample_sentence)
        return predict_data
    
    def make_mask(real_len, max_len, label_size, batch=1):
        mask = torch.zeros(batch, max_len, label_size)
        for index, item in enumerate(real_len):
            mask[index, :item, :] = 1.0
        return mask

    def masked_log_softmax(vector: torch.Tensor, mask: torch.Tensor, dim: int = -1) -> torch.Tensor:
            if mask is not None:
                mask = mask.float()
                while mask.dim() < vector.dim():
                    mask = mask.unsqueeze(1)

                vector = vector + (mask + 1e-45).log()
            return torch.nn.functional.log_softmax(vector, dim=dim)

    def get_chunks(labels):
            chunks = []
            start_idx,end_idx = 0,0
            for idx in range(1,len(labels)-1):
                chunkStart, chunkEnd = False,False
                if labels[idx-1] not in ('O', '<pad>', '<unk>', '<s>', '</s>', '<STOP>', '<START>'):
                    prevTag, prevType = labels[idx-1][:1], labels[idx-1][2:]
                else:
                    prevTag, prevType = 'O', 'O'
                if labels[idx] not in ('O', '<pad>', '<unk>', '<s>', '</s>', '<STOP>', '<START>'):
                    Tag, Type = labels[idx][:1], labels[idx][2:]
                else:
                    Tag, Type = 'O', 'O'
                if labels[idx+1] not in ('O', '<pad>', '<unk>', '<s>', '</s>', '<STOP>', '<START>'):
                    nextTag, nextType = labels[idx+1][:1], labels[idx+1][2:]
                else:
                    nextTag, nextType = 'O', 'O'

                if (Tag == 'B' and prevTag in ('B', 'I', 'O')) or (prevTag, Tag) in [('O', 'I'), ('E', 'E'), ('E', 'I'), ('O', 'E')]:
                    chunkStart = True
                if Tag != 'O' and prevType != Type:
                    chunkStart = True

                if (Tag in ('B','I') and nextTag in ('B','O')) or (Tag == 'E' and nextTag in ('E', 'I', 'O')):
                    chunkEnd = True
                if Tag != 'O' and Type != nextType:
                    chunkEnd = True

                if chunkStart:
                    start_idx = idx
                if chunkEnd:
                    end_idx = idx
                    chunks.append((start_idx,end_idx,Type))
                    start_idx,end_idx = 0,0
            return chunks
    #prepare for prediction
    sentence_predict=makeoneindex(sentence)
    real_len_predict=[len(sentence.split())]

    #predict
    x_predict = torch.tensor(sentence_predict).to(device)
    mask_predict = make_mask(real_len_predict,max_len=max_len, label_size=len(slot_dict), batch=1).to(device)
    # Slot model generate hs_predict and intent model generate hi_predict
    hs_predict = slot_model.enc(x_predict)
    hi_predict = intent_model.enc(x_predict)
    #slot
    slot_logits_predict = slot_model.dec(hs_predict, hi_predict)
    log_slot_logits_predict = masked_log_softmax(slot_logits_predict, mask_predict, dim=-1)
    slot_pred_predict = torch.argmax(log_slot_logits_predict, dim=-1)

    slot_pred_predict = slot_pred_predict[0][:real_len_predict[0]]
    slot_pred_predict = [int(item) for item in slot_pred_predict]
    slot_pred_predict = [index2slot_dict[item] for item in slot_pred_predict]

    #chunk
    pred_chunks = get_chunks(['O'] + slot_pred_predict + ['O'])

    #intent
    intent_logits_predict = intent_model.dec(hi_predict, hs_predict, real_len_predict)
    log_intent_logits_predict = F.log_softmax(intent_logits_predict, dim=-1)
    res_predict = torch.argmax(log_intent_logits_predict, dim=-1)
    for intent, num in intent_dict.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if res_predict == num:
            intent_predict=intent
    return pred_chunks,intent_predict

class ModelClient:
    def __init__(self,model_path="/Users/chenzichu/Desktop/slot-filling/package/slot_ZC"):
        self.slot_model,self.intent_model=load_model(data_path=model_path)
        self.model_path=model_path

    def predict(self,sentence):
        pred_chunks,pred_intent=predict(sentence,slot_model=self.slot_model,intent_model=self.intent_model,data_path=self.model_path)
        return pred_chunks,pred_intent

