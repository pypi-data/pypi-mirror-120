import json
from pkg_resources import resource_stream
config = json.load(resource_stream('slot_ZC', 'config.json'))
# with open('config.json') as config_file:
#     config = json.load(config_file)



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


def convert_int(arr):
    try:
        a = int(arr)
    except:
        return None
    return a

# Make words dict	
words = []
with resource_stream('slot_ZC', train_file) as f:
    for line in f.readlines():
        line = line.strip().lower().split()

        for index, item in enumerate(line):
            word = item.split(':')[0]
            if word == '<=>':
                break
            if convert_int(word) is not None:
                words.append('DIGIT' * len(word))
            else:        
                words.append(word)

words_vocab = sorted(set(words))
word_dict = {'UNK': 0, 'PAD': 1}

for i, item in enumerate(words_vocab):
    word_dict[item] = i + 2

# Make slot tag dict 
slot_dict = {}

with open(vocab_slot_file) as f:

    for i, line in enumerate(f.readlines()):
        slot_dict[line.strip()] = i


# print(slot_dict)

# Make intent dict 
intent_dict = {}

with open(vocab_intent_file) as f:
    for i, line in enumerate(f.readlines()):
        intent_dict[line.strip()] = i

num_intent=len(intent_dict)
# print(intent_dict)


