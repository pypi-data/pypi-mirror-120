from slot_ZC.make_dict import word_dict, intent_dict, slot_dict
import torch 
import torch.nn as nn
import torch.nn.functional as F
import json
from pkg_resources import resource_stream
config = json.load(resource_stream('slot_ZC', 'config.json'))
# with open('config.json') as config_file:
#     config = json.load(config_file)

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
		
		
