import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle

nltk.download('punkt')

stemmer = LancasterStemmer()

# OPEN JSON FILE

with open("intents.json") as file:
    data = json.load(file)

# DATA PRE-PROCESSING

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_a = []
    docs_b = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_a.append(wrds)
            docs_b.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    empty_ouput = [0 for x in range(len(labels))]

    for a, doc in enumerate(docs_a):
        bag_of_words = []

        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag_of_words.append(1)
            else:
                bag_of_words.append(0)

        output_row = empty_ouput[:]
        output_row[labels.index(docs_b[a])] = 1

        training.append(bag_of_words)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    # SAVE FILE

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tf.compat.v1.reset_default_graph()

# AI MODEL

neural_network = tflearn.input_data(shape=[None, len(training[0])])
neural_network = tflearn.fully_connected(neural_network, 8)
neural_network = tflearn.fully_connected(neural_network, 8)
neural_network = tflearn.fully_connected(neural_network, len(output[0]), activation="softmax")
neural_network = tflearn.regression(neural_network)

model = tflearn.DNN(neural_network)

# LOAD DATA

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def list_of_words(s, words):
    bag_of_words = [0 for _ in range(len(words))]

    sentence_in_words = nltk.word_tokenize(s)
    sentence_in_words = [stemmer.stem(word.lower()) for word in sentence_in_words]

    for sentence in sentence_in_words:
        for i, w in enumerate(words):
            if w == sentence:
                bag_of_words[i] = 1

    return np.array(bag_of_words)


def chat():
    print("Chat with bot! Type 'quit' when you are done")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        result = model.predict([list_of_words(inp, words)])[0]
        result_index = np.argmax(result)
        tag = labels[result_index]

        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg["tag"] == tag:
                    responses = tg["responses"]
            print(random.choice(responses))
        else:
            print("I didn't get that, please ask a different question")

chat()
