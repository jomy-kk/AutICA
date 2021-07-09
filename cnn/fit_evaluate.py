####################################
#
#  PDSB Project 2021
#
#  Module: Classification with Convolutional Neural Networks (CNN)
#  File: fit_evaluate
#
#  Created on May 30, 2021
#
#  Code rights reserved to João Saraiva
#
####################################

import tensorflow as tf
from sklearn.metrics import f1_score
from matplotlib import pyplot as plt
import numpy as np


def object_classification(model, weights, test_inputs, events, target_objects_per_block):

    # Make predictions
    model.load_weights(weights)
    ypred = model.predict(test_inputs)

    correctly_predicted_blocks = 0
    total_blocks = len(target_objects_per_block)

    # Split in blocks
    ypred_by_blocks = np.array_split(ypred, total_blocks, axis=0)
    events_by_blocks = np.array_split(events, total_blocks, axis=0)
    for these_preds, these_events, i in zip(ypred_by_blocks, events_by_blocks, range(total_blocks)):
        these_averages = np.empty((8, 2))
        for event_num in range(1, 9):  # [1, 8]
            indices = np.where(these_events == event_num)
            these_averages[event_num - 1] = np.mean(these_preds[indices], axis=0)

        object_prediction = these_averages.argmax(axis=0)[1] + 1  # index + 1
        true_object = target_objects_per_block[i]
        if object_prediction == true_object:
            correctly_predicted_blocks += 1

    return correctly_predicted_blocks / total_blocks


def evaluate_model(model, weights, test_inputs, test_targets, show=False):
    """
    Evaluates a given model with the given weights. Prints the test accuracy and loss.
    Provide the following:
    :param model: A valid already trained classification model, such as a CNN.
    :param weights: Weight vectors of the model after training. Give the best.
    :param test_inputs: Input vectors reserved for testing.
    :param test_targets: Target vectors reserved for testing -- growth truth.
    """
    model.load_weights(weights)
    loss, acc = model.evaluate(test_inputs, test_targets)

    # F1-score
    ypred = model.predict(test_inputs)
    ypred = ypred.argmax(axis=-1)
    f1 = f1_score(test_targets, ypred)

    if show:
        print('Pred\tTrue')
        for pred, true in zip(ypred, test_targets):
            print(pred, '\t', true)

    return loss, acc, f1


def fit_model(model, train_inputs, train_targets,
                           loss_function='sparse_categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
                           metrics=('accuracy', ), epochs=10000, batch_size=64, patience=10, validation_split=.2,
                           verbose=True, class_weights={0:1, 1:1}):

    model.compile(loss=loss_function, optimizer=optimizer, metrics=metrics)
    if(verbose):
        model.summary()

    earlystop = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=patience, verbose=verbose)
    checkpoint = tf.keras.callbacks.ModelCheckpoint('best.h5', monitor='val_accuracy', verbose=verbose, save_best_only=True)
    model_train = model.fit(train_inputs, train_targets, validation_split=validation_split,
                            callbacks=[earlystop, checkpoint], epochs=epochs, batch_size=batch_size, shuffle=True,
                            verbose=verbose, class_weight=class_weights)

    return model_train


def fit_and_evaluate_model(model, train_inputs, train_targets, test_inputs, test_targets,
                           loss_function='sparse_categorical_crossentropy', optimizer='adam',
                           metrics=('accuracy', ), epochs=10000, batch_size=64, patience=10, validation_split=.2,
                           class_weights=None):
    """
    Trains a given model with the given optimization and loss functions for the given number of epochs.
    Stops based on the accuracy metric. An early stop is defined with a convergence patience set by patience.
    A checkpoint is defined to save only the weights from the best model, based on the validation accuracy.
    A percentage of the training examples given by validation_split is used only for validation.
    It plots the training accuracy and loss and the validation accuracy and loss against the number of epochs,
    and evaluates the best model for the given dataset.
    """

    model_train = fit_model(model, train_inputs, train_targets,
                               loss_function=loss_function, optimizer=optimizer,
                               metrics=metrics, epochs=epochs, batch_size=batch_size,
                               patience=patience, validation_split=validation_split,
                               class_weights=class_weights if class_weights is not None else {0:1, 1:1})

    fig, (loss_ax, acc_ax) = plt.subplots(1, 2, figsize=(20, 7))

    loss_ax.set_title('Loss')
    loss_ax.plot(model_train.history['loss'], '-r', label='Train')
    loss_ax.plot(model_train.history['val_loss'], '-g', label='Validation')

    acc_ax.set_title('Accuracy')
    acc_ax.plot(model_train.history['accuracy'], '-r', label='Train')
    acc_ax.plot(model_train.history['val_accuracy'], '-g', label='Validation')

    plt.legend(loc=4)
    plt.show()

    loss, acc, f1, = evaluate_model(model, 'best.h5', test_inputs, test_targets)

    print('\nAccuracy: {}'.format(acc))
    print('Loss: {}'.format(loss))
    print('F1-score: {}'.format(f1))


def do_experiment(model, train_inputs, train_targets, test_inputs, test_targets,
                           loss_function='sparse_categorical_crossentropy', optimizer='adam',
                           metrics=('accuracy', ), epochs=10000, batch_size=32, patience=10, validation_split=.2):

    val_accuracies, val_losses, test_accuracies, test_losses, test_f1s = 0, 0, 0, 0, 0

    for i in range(10):
        print("Run", i)
        model_train = fit_model(model, train_inputs, train_targets,
                               loss_function=loss_function, optimizer=optimizer,
                               metrics=metrics, epochs=epochs, batch_size=batch_size,
                               patience=patience, validation_split=validation_split, verbose=False)

        #val_accuracies += np.max(model_train.history['accuracy'])
        #val_losses += np.min(model_train.history['loss'])

        loss, acc, f1 = evaluate_model(model, 'best.h5', test_inputs, test_targets, show_predictions=True)
        test_losses += loss
        test_accuracies += acc
        test_f1s += f1

    val_accuracies, val_losses, test_accuracies, test_losses, test_f1s =\
        val_accuracies/10, val_losses/10, test_accuracies/10, test_losses/10, test_f1s/10

    #print('\nValidation Accuracy: {}'.format(val_accuracies))
    #print('Validation Loss: {}'.format(val_losses))
    print('\nTest Accuracy: {}'.format(test_accuracies))
    print('Test Loss: {}'.format(test_losses))
    print('F1-score: {}'.format(test_f1s))
