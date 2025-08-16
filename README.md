# SignEase - ISL and ASL Gesture Recognition

SignEase is a real-time system that converts **Indian Sign Language (ISL)** and **American Sign Language (ASL)**
gestures into text using deep learning and computer vision.

##📌 Overview

Communication is one of the most fundamental human needs. For the hearing- and speech-impaired community, sign language serves as the primary medium of interaction. However, in environments where others may not understand sign language, communication becomes a major challenge.

This project introduces a real-time sign language recognition system that can translate:

Static hand gestures of American Sign Language (ASL) and Indian Sign Language (ISL) into text.

Text to sign gestures (reverse translation).

Dynamic motion-based gestures using finger movement recognition.

By integrating ASL and ISL in a single application, the system ensures broader accessibility and usability for diverse users.

##🚀 Features

✅ Real-time static gesture recognition for ASL & ISL.

✅ Dynamic gesture recognition using finger tracking and motion detection.

✅ Bidirectional translation (Gestures → Text & Text → Gestures).

✅ High accuracy classifier trained on large-scale datasets.

✅ Expandable & language-neutral framework for adding more sign languages in the future.

##📊 Datasets & Model

Indian Sign Language (ISL) Dataset

Total samples: 29,373

Training: 23,498 (80%)

Testing: 5,875 (20%)

American Sign Language (ASL) Dataset

Total samples: 8,451

Training: 6,760 (80%)

Testing: 1,691 (20%)

Classifier Used: Random Forest Classifier

Performance:

ASL Recognition Accuracy → 99.53%

ISL Recognition Accuracy → 99.97%

##🛠️ Tech Stack

Programming Language: Python

Libraries & Frameworks:

OpenCV – Real-time computer vision

MediaPipe – Hand tracking & keypoint detection

Scikit-learn – Random Forest Classifier

NumPy, Pandas – Data preprocessing

Matplotlib – Visualization


## 🎯 Future Scope
- Add speech synthesis (gesture → voice)
- Support dynamic sign sequences
- Deploy as a mobile & web app
