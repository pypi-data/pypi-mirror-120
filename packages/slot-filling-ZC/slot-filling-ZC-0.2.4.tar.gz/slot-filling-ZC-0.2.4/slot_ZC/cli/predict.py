import click
from slot_ZC import Bi_model

@click.command()
# @click.option("--model_path", prompt="Model path")
# @click.option("--sentence", prompt="Sentence to predict")
def predict():
    """Simple program that greets NAME for a total of COUNT times."""
    model_path=click.prompt("Model path")
    model=Bi_model.ModelClient(model_path=f"{model_path}")
    while True:
        sentence=click.prompt("Sentence to predict")
        prediction=model.predict(sentence=f"{sentence}")
        print(prediction)

if __name__ == '__main__':
    predict()