import tensorflow as tf
import numpy as np
import streamlit as st
import cv2
from tensorflow.keras.models import load_model

# Load the model
model = load_model('Brain_tumor.h5')

# Class names
CLASS_NAMES = ['glioma', 'meningioma', 'notumor', 'pituitary']

# Setting title of the app
st.title("Brain Tumor Prediction Model")
st.markdown("Upload an image of the Tumor")

# Uploading the leaf image
tumor = st.file_uploader("Choose an image...", type="png")
submit = st.button('Predict')

# On predict button click
if submit:
    if tumor is not None:
        # Convert the file to an OpenCV image
        file_bytes = np.asarray(bytearray(tumor .read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Displaying the image
        st.image(opencv_image, channels="BGR")

        # Resize and preprocess the image
        opencv_image = cv2.resize(opencv_image, (256, 256))
        opencv_image = np.expand_dims(opencv_image, axis=0)  # Add batch dimension

        # Make prediction
        Y_pred = model.predict(opencv_image)

        # Display prediction result
        predicted_class = CLASS_NAMES[np.argmax(Y_pred)]
        st.title(f"The Tumor is {predicted_class}")