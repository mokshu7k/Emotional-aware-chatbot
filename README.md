# Emotional-aware-chatbot
This project aims to create a Real-Time Emotion-Aware Video Chatbot that dynamically adapts its conversational tone based on the user's detected emotional state. By integrating cutting-edge computer vision and machine learning techniques, the chatbot will provide a more empathetic and natural interaction experience.

# Project Goal
The primary goal is to develop a system that can accurately detect a user's emotions in real-time through video and audio analysis, and subsequently adjust the chatbot's responses to be more appropriate and sensitive to those emotions.

# Key Components & Contributions
This project is divided into two main components, with distinct contributions from the team members:

1. Real-Time Facial Emotion Detection (Vedika Kodgire)
This component focuses on visually analyzing the user's face to identify their emotional state.

Technology: Primarily utilizes OpenCV for video processing.

Functionality:

Face Detection: Identifies the presence and location of a human face in the video stream.

Emotion Detection: Analyzes facial expressions to classify emotions. This will be achieved using either the FER+ dataset for training a robust model or a custom Convolutional Neural Network (CNN) specifically designed for this task.

Contribution: Vedika Kodgire is responsible for the implementation and optimization of the OpenCV-based face and emotion detection module, ensuring accurate and real-time performance.

2. Speech Emotion Detection & Chatbot Logic (Mokshita Kochhar)
This component handles the auditory analysis of the user's speech and the core conversational intelligence of the chatbot.

Technology: Leverages Machine Learning (ML) models for audio processing and natural language understanding.

Functionality:

Speech Emotion Detection: Processes the user's spoken input to identify underlying emotional tones. This involves training a sentiment classifier on speech data.

Chatbot Core: Manages the conversational flow, processes user queries, and generates responses.

Tone Adaptation: Integrates the emotional insights from both facial and speech detection to modify the chatbot's tone, making its responses more empathetic, supportive, or appropriate to the user's emotional state.

Contribution: Mokshita Kochhar is responsible for developing the speech emotion detection model, designing and implementing the chatbot's conversational logic, and ensuring the seamless integration of emotion awareness into the chatbot's responses.

How it Works (High-Level)
The system captures real-time video and audio input from the user.

Vedika's module processes the video to detect faces and their corresponding emotions.

Mokshita's module analyzes the audio for speech and its emotional content.

Vedika's combined emotional data (facial + speech) is fed into the chatbot.

Mokshita's chatbot logic uses this emotional context to generate a response with an appropriate tone.

The chatbot's response is delivered to the user, creating an emotionally intelligent interaction.

This project represents a significant step towards creating more human-like and understanding AI conversational agents.