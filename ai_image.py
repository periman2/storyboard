from config import IMAGE_MODEL_IMAGE_SIZE, IMAGE_MODEL_URL, LABELS_MAP_PATH
import tensorflow_hub as hub
import tensorflow as tf
from typing import List

#initializing tensorflow model (singleton for all the server for now)
tf.keras.backend.clear_session()
m = tf.keras.Sequential([
    hub.KerasLayer(IMAGE_MODEL_URL) #TODO: add to config
])
m.build([None, IMAGE_MODEL_IMAGE_SIZE, IMAGE_MODEL_IMAGE_SIZE, 3])

#main functions
def getDescriptionsOfImage(image_file_path: str, max_desc_number: int = 5):

  image = tf.keras.preprocessing.image.load_img(image_file_path, target_size=(IMAGE_MODEL_IMAGE_SIZE, IMAGE_MODEL_IMAGE_SIZE))
  print(image)
  image = tf.keras.preprocessing.image.img_to_array(image)
  image = (image - 128.) / 128.
  logits = m(tf.expand_dims(image, 0), False)

  labels_map = LABELS_MAP_PATH #TODO: add to config

  pred = tf.keras.activations.sigmoid(logits)
  idx = tf.argsort(logits[0])[::-1][:20].numpy()

  classes = get_imagenet_labels(labels_map)
  
  results: List[str] = []

  for i, id in enumerate(idx):
    if(len(results) < max_desc_number):
      results.append(classes[id])
    else:
      break
    
  return results

#Helper functions
def get_imagenet_labels(filename):
  labels = []
  with open(filename, 'r') as f:
    for line in f:
      labels.append(line.split('\t')[1][:-1]) 
  return labels
from config import IMAGE_MODEL_IMAGE_SIZE, IMAGE_MODEL_URL, LABELS_MAP_PATH
import tensorflow_hub as hub
import tensorflow as tf
from typing import List

#initializing tensorflow model (singleton for all the server for now)
tf.keras.backend.clear_session()
m = tf.keras.Sequential([
    hub.KerasLayer(IMAGE_MODEL_URL) #TODO: add to config
])
m.build([None, IMAGE_MODEL_IMAGE_SIZE, IMAGE_MODEL_IMAGE_SIZE, 3])

#main functions
def getDescriptionsOfImage(image_file_path: str, max_desc_number: int = 5):

  image = tf.keras.preprocessing.image.load_img(image_file_path, target_size=(IMAGE_MODEL_IMAGE_SIZE, IMAGE_MODEL_IMAGE_SIZE))
  print(image)
  image = tf.keras.preprocessing.image.img_to_array(image)
  image = (image - 128.) / 128.
  logits = m(tf.expand_dims(image, 0), False)

  labels_map = LABELS_MAP_PATH #TODO: add to config

  pred = tf.keras.activations.sigmoid(logits)
  idx = tf.argsort(logits[0])[::-1][:20].numpy()

  classes = get_imagenet_labels(labels_map)
  
  results: List[str] = []

  for i, id in enumerate(idx):
    if(len(results) < max_desc_number):
      results.append(classes[id])
    else:
      break
    
  return results

#Helper functions
def get_imagenet_labels(filename):
  labels = []
  with open(filename, 'r') as f:
    for line in f:
      labels.append(line.split('\t')[1][:-1]) 
  return labels