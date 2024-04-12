import streamlit as st
from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model, Model


@st.cache_resource
def load_keras_model():
    image_model = load_model('image_model.keras')
    return image_model


def import_and_predict(image_data):
    image_array = np.array(image_data)
    if image_array.shape[2] == 4:

        alpha_layer = image_array[:, :, 3]
        alpha_layer = Image.fromarray(alpha_layer).resize((28, 28))
        alpha_layer = img_to_array(alpha_layer)
        alpha_layer = alpha_layer.reshape(1, 28, 28, 1)

        # Normalize the alpha layer
        alpha_layer = alpha_layer.astype("float32") / 255
        image_data = alpha_layer

    # Load the model
    model = load_model("image_model.keras")

    # Use the model to make a prediction
    prediction = model.predict(image_data)
    return np.argmax(prediction)


st.title("Image Classifier")
st.header("Please upload an image")


uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Classifying")
    label = import_and_predict(image)
    st.write(f'The uploaded image is most likely a {label}.')
