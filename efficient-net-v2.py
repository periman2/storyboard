import tensorflow_hub as hub
import tensorflow as tf

model = hub.KerasLayer('https://tfhub.dev/google/imagenet/efficientnet_v2_imagenet1k_b0/feature_vector/2')

image = tf.keras.preprocessing.image.load_img('resources/beach.png', target_size=(224, 224))
image = tf.keras.preprocessing.image.img_to_array(image)
image = tf.keras.applications.efficientnet.preprocess_input(image)

prediction = model.predict(image[tf.newaxis, ...])
print(prediction)