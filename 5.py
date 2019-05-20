
# Import necessary modules
import sys

from rasa_nlu.converters import load_data
#from rasa_nlu.config import RasaNLUConfig
#from rasa_nlu.model import Trainer


# Create args dictionary
args = {"pipeline": "spacy_sklearn"}

# Create a configuration and trainer
config = rasa_nlu.config.RasaNLUConfig(cmdline_args=args)


trainer = Trainer(config)

# Load the training data
training_data = load_data("./training_data.json")

# Create an interpreter by training the model
interpreter = trainer.train(training_data)

# Test the interpreter
interpreter.parse("I'm looking for a Mexican restaurant")
