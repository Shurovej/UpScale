import pickle
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.models import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint as ChPt

with open('./x_train.pickle', 'rb') as f:
    x_train = pickle.load( f)
with open('./y_train.pickle', 'rb') as f:
    y_train = pickle.load( f)
    
model = Sequential([
    Dense(3, input_shape=(32,32,3) ,activation='linear'),
    UpSampling2D(size=(2), data_format=None),
    Conv2D(3, (3, 3), activation='relu', padding='same'),
])

model.compile(loss='mse', optimizer=Adam(learning_rate=0.00002),metrics=['accuracy'])

#print(model.summary())   
 
best_w=ChPt('./fcn_best.h5',
            monitor='val_accuracy',
            verbose=1,
            save_best_only=True,
            save_weights_only=True,
            mode='auto',
            save_freq='epoch')
last_w=ChPt('./fcn_last.h5',
            monitor='val_accuracy',
            verbose=1,
            save_best_only=False,
            save_weights_only=True,
            mode='auto',
            save_freq='epoch')
callbacks=[best_w, last_w]

model.fit(x_train, y_train ,
          steps_per_epoch=80,
          callbacks=callbacks,
          validation_split=0.25,
          batch_size=9, epochs=99,
          verbose=1, shuffle=True, 
          use_multiprocessing=True )