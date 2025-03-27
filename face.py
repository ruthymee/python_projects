import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Streamlit App Title
st.title("Face Detection App using Viola-Jones Algorithm")

# Instructions for Users
st.markdown("""
### Instructions:
1. Upload an image.
2. Adjust the **Scale Factor** and **Min Neighbors** to fine-tune face detection.
3. Select the color of the detection rectangle.
4. Download the image with detected faces.
""")

# File Upload
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Convert uploaded image to OpenCV format
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    
    # User-adjustable parameters
    scale_factor = st.slider("Scale Factor", 1.1, 2.0, 1.3, 0.1)
    min_neighbors = st.slider("Min Neighbors", 1, 10, 5, 1)
    rect_color = st.color_picker("Pick a Rectangle Color", "#FF0000")
    
    # Convert hex color to BGR format
    rect_color_rgb = tuple(int(rect_color[i:i+2], 16) for i in (1, 3, 5))
    rect_color_bgr = rect_color_rgb[::-1]  # Convert RGB to BGR for OpenCV
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors)
    
    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image_np, (x, y), (x + w, y + h), rect_color_bgr, 2)
    
    # Display detected faces
    st.image(image_np, caption="Detected Faces", use_column_width=True)
    
    # Save the processed image
    save_path = "detected_faces.png"
    cv2.imwrite(save_path, cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
    
    # Download Button
    with open(save_path, "rb") as file:
        st.download_button(label="Download Image", data=file, file_name="detected_faces.png", mime="image/png")
