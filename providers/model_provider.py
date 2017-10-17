from keras.models import model_from_json
print('TensorFlow initiated')

def load():
    with open('model/model.json', 'r') as model_json:
        loaded_model_json = model_json.read()
        model = model_from_json(loaded_model_json)
        model.load_weights("model/model.h5")
        print("loaded model from disk")
        return model
