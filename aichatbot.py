import json
import pickle
# import tflearn
# import tensorflow
import random


import nltk
import numpy

from nltk.stem.snowball import SnowballStemmer
from tensorflow.keras.models import load_model


stemmer = SnowballStemmer("english")







def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
   
    

    return numpy.array(bag)

def chat(inp):
    print("Bot is initializing!")
    try:
        
        model = load_model('model.h5')
    except:
        print("CANNOT STARTED BOT")


    with open("intents.json") as file:
        data = json.load(file)

    try:
        with open("data.pickle", "rb") as f:
            words, labels, training, output = pickle.load(f)
    except:
        print("words cant be loaded")
    inpw =numpy.asarray([bag_of_words(inp, words)])
    inpw= numpy.reshape(inpw, (inpw.shape[0],1,inpw.shape[1]))
    results = model.predict(inpw)
    results_index = numpy.argmax(results)
    print(results)
    tag = labels[results_index]

    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']


    return random.choice(responses)
