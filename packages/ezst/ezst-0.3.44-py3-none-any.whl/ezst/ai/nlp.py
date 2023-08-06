
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer


class CNN:
    pass

cnn = CNN()


class CustomCallback(keras.callbacks.Callback):
    def on_train_begin(self, logs=None):
        print("훈련을 시작합니다.")

    def on_train_end(self, logs=None):
        print("훈련을 종료합니다.")

    def on_epoch_end(self, epoch, logs=None):
        keys = list(logs.keys())

        log_string = ''
        for key in keys:
            if key is 'accuracy':
                log_string = f"[정확도: {round(logs[key], 4)}]"

        print(f"반복 훈련 종료 : {epoch}/{cnn.repeat} {log_string}")


def to_str(sentence):
    return str(sentence)


def train(dataset, repeat=5):

    index_word = {}
    train_data = []
    train_labels = []
    for index, label in enumerate(dataset.keys()):
      index_word[str(index)] = label

      for data in np.array(dataset[label]):
        if data:
          train_data.append(data)
          train_labels.append(index)

    cnn.repeat = repeat

    train_data = pd.Series(train_data)
    train_labels = pd.Series(train_labels)

    train_data = train_data.str.replace('[^A-Za-z가-힣]', '', regex=True)
    train_data = train_data.apply(to_str)
    

    tokenizer = Tokenizer(char_level=True)
    tokenizer.fit_on_texts(train_data)

    train_data = tokenizer.texts_to_sequences(train_data)

    maxlen = 50
    train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                            value=0,
                                                            padding='post',
                                                            maxlen=maxlen)
    vocab_size = len(tokenizer.word_counts)+1

    cate_num = len(index_word)
    model = Sequential([
        layers.Embedding(vocab_size, maxlen, input_shape=(None,)),
        layers.Reshape((maxlen, maxlen, 1)),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense( cate_num, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(train_data,
                        train_labels,
                        epochs=repeat,
                        shuffle=True,
                        callbacks=[CustomCallback()],
                        verbose=0,
                        batch_size=1024)

    cnn.model = model
    cnn.maxlen = maxlen
    cnn.tokenizer = tokenizer
    cnn.repeat = repeat
    cnn.index_word = index_word

    return history


def predict(sentence):
    # 정수화
    sentence = cnn.tokenizer.texts_to_sequences([sentence])

    # 패딩
    sentence = keras.preprocessing.sequence.pad_sequences(sentence,
                                                          value=0,
                                                          padding='post',
                                                          maxlen=cnn.maxlen)

    result = cnn.model.predict(sentence)

    print(cnn.index_word[str(np.argmax(result[0]))])

