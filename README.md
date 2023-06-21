# Handwritten Assignment Plagiarism Checker
#### Final Year B.Tech project at Rajagiri School of Engineering & Technology
## Project Title: Handwritten Assignment Plagiarism Checker
## Team Members:
- Aditya S Nair
- Emmanuel Joseph
- Faiz Ameer
- Peter Johnosn

## Basic Overview
This is Handwritten Assignment Plagiarism Checker built based on a CNN based machine learning model which is trained using the IAM dataset.
This software takes n number of handwriiten assignments as input from the user, segments the each assignments and creates a pipeline where
each of the segmented image is sent to the model for prediction. Once the model predicts the word it's immediately appended onto a text file.
This cycle continutes for the entire segmented words and in the end this text file is deployed onto to predicted text directory. From this 
directory the plagiarism model performs the comparision to see if any assignments are plagiarised or not.
