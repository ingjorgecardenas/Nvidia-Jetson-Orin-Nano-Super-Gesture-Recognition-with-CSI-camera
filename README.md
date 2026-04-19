Gesture Recognition with CSI Camera (Jetson Orin Nano)
Hello! This Python script was created to use a CSI camera for hand gesture recognition, based on the following guide:

[Tutorial: Nvidia Jetson Orin Nano Gesture Recognition](https://www.cytron.io/tutorial/nvidia-jetson-orin-nano-super-gesture-recognition?srsltid=AfmBOoorDbVyEyDf2iOANRSllD6uSh_iCBy4v3ODsrRTdeO-enNELqL-)

Hardware & Environment
Device: NVIDIA Jetson Orin Nano

JetPack Version: 6.2.2

Camera: IMX219 (CSI)

Drivers: Setup using official NVIDIA camera drivers.

OpenCV Custom Build
The default OpenCV version provided with JetPack 6.2.2 does not include built-in support for CUDA and GStreamer. To fix this, I compiled OpenCV from source following this guide:

[Step-by-Step: Build OpenCV with GStreamer on Jetson Orin Nano](https://medium.com/@erencanbulut/step-by-step-build-opencv-with-gstreamer-on-jetson-orin-nano-ubuntu-22-04-08edfb373c78)

Run it with command:
python3 hand-gesture.py

Hope this helps you in your AI journey. Take care!
