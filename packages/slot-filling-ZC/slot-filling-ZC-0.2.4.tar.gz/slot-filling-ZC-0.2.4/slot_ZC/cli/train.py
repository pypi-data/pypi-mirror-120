#%%
import click
from slot_ZC import Bi_model
import os
import json

@click.command()
@click.option("--model_config", prompt="config_file")
@click.option("--model_name", prompt="model_name")
@click.option("--model_version", prompt="version")
@click.option("--model_saved_base_dir", prompt="Directory to save model")
@click.option("--dataset_file_path", prompt="Data directory")
def train(model_config,model_name,model_version,model_saved_base_dir,dataset_file_path):
    """Simple program that greets NAME for a total of COUNT times."""
    #convert input to string
    model_config=f"{model_config}"
    model_saved_base_dir=f"{model_saved_base_dir}"
    dataset_file_path=f"{dataset_file_path}"
    #create model folder
    model_saved_base_dir=model_saved_base_dir+"/"+f"{model_name}"+f"{model_version}"
    try:
        if not os.path.exists(model_saved_base_dir):
            os.makedirs(model_saved_base_dir)
        else:
            print("version or model name already exist")
    except OSError:
        print('Error: Creating directory. '+model_saved_base_dir)
    #data path for training
    train_file = os.path.join(dataset_file_path,'train_dev')
    test_file = os.path.join(dataset_file_path,'test')
    vocab_intent_file = os.path.join(dataset_file_path,'vocab.intent')
    vocab_slot_file = os.path.join(dataset_file_path,'vocab.slot')
    #data configs
    f=open(model_config)
    configs = json.load(f)
    total_epoch = configs['total_epoch']
    max_len=configs['max_len']
    batch = configs['batch']
    learning_rate = configs['learning_rate']
    DROPOUT = configs['DROPOUT']
    embedding_size = configs['embedding_size']
    lstm_hidden_size = configs['lstm_hidden_size']
    #train
    Bi_model.train(train_file=train_file,
                   test_file=test_file,
                   vocab_intent_file=vocab_intent_file,
                   vocab_slot_file=vocab_slot_file,
                   model_path=model_saved_base_dir,
                   total_epoch = total_epoch,
                   max_len = max_len,
                   batch = batch,
                   learning_rate = learning_rate,
                   DROPOUT = DROPOUT,
                   embedding_size = embedding_size,
                   lstm_hidden_size = lstm_hidden_size)

if __name__ == '__main__':
    train()
# %%
