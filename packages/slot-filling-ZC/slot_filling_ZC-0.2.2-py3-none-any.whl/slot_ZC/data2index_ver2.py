from slot_ZC.make_dict import word_dict, intent_dict, slot_dict
from slot_ZC.make_dict import convert_int
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


train_data = makeindex(train_file)
test_data = makeindex(test_file)

index2slot_dict = {}
for key in slot_dict:
    index2slot_dict[slot_dict[key]] = key


print('Number of training samples: ', len(train_data))
print('Number of test samples: ', len(test_data))
print('Number of words: ', len(word_dict))
print('Number of intent labels: ', len(intent_dict))
print('Number of slot labels', len(slot_dict))

