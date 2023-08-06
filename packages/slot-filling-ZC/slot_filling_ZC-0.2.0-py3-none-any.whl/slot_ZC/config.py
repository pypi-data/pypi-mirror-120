#%%
import torch
import json

with open("config.json") as config_file:
    config = json.load(config_file)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
total_epoch = config['total_epoch']
max_len = config['max_len']
batch = config['batch']
learning_rate = config['learning_rate']
DROPOUT = config['DROPOUT']

embedding_size = config['embedding_size']
lstm_hidden_size = config['lstm_hidden_size']

#change data path
train_file = config['train_file']
test_file = config['test_file']

vocab_intent_file = config['vocab_intent_file']
vocab_slot_file = config['vocab_slot_file']

