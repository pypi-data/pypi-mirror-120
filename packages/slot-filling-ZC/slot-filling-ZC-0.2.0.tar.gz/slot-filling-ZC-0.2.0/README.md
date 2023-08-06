Intent and Slot Filling Bi-Model

train(train_file = "data/train_dev",
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
       lstm_hidden_size = 200)

5 files would be generated after training:
model_intent_best.pt
model_slot_best.pt
word_dict.pickle
slot_dict.pickle
intent_dict.pickle

predict(sentence="find nonstop flights from salt lake city to new york on saturday april ninth.",
            data_path="/Users/chenzichu/Desktop/slot-filling/package/slot_ZC",
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
            max_len = 50,
            batch = 16,
            DROPOUT = 0.2,
            embedding_size = 300,
            lstm_hidden_size = 200)