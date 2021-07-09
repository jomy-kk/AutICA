from load_dataset import prepare_dataset
from create_model import create_model
from fit_evaluate import fit_and_evaluate_model, object_classification

trainX, trainY, testX, testY, input_shape, event_objects, target_objects =\
    prepare_dataset('SBJ04', 'S07', objects=True,
                    ica_algorithm_pruned='picard')

model = create_model("Pilot", input_shape)

class_weights = {0:1, 1:7}

fit_and_evaluate_model(model, trainX, trainY, testX, testY, batch_size=256, patience=30,
                       class_weights=class_weights)

# 8-way object classification accuracy (i.e. accuracy in the competition)
acc = object_classification(model, 'best.h5', testX, event_objects, target_objects)
print("Object accuracy:", acc)


