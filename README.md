## **Accent Classifier**

### **I. Introduction**

This project is a proof-of-concept tool designed to evaluate English-speaking candidates by classifying their accent and providing a confidence score. It allows HR teams or technical screeners to analyze spoken audio (from videos) and determine whether the speaker exhibits traits of specific English accents.

### **II. The Challenge**

The task is to build a working tool that:

Accepts a public video URL (e.g., YouTube or direct MP4 link).

Extracts audio from the video.

Analyzes the speaker's accent to identify English language proficiency.

#### Outputs:

Classification of the accent (e.g., British, American, Australian, etc.)

A confidence score (e.g., 0–100%)

(Optional) Short summary or explanation

This tool is intended for internal use to assist in hiring processes.

What We're Looking For

Practicality: The tool must work reliably.

Creativity: Smart or resourceful implementations are appreciated.

Technical Execution: Code must be clean, testable, and logically structured.

#### Allowed Tools

Any programming language, no-code tools, or open-source APIs can be used.

#### Deliverables

A working script, notebook, or small web app

A live deployment with a simple UI

Submission link: Submit your work

#### Time Expectation

Please do not spend more than 4–6 hours. We are looking for a proof-of-concept.

### **III. Tech Stack Used**

#### Backend

Python with RunPod serverless backend

TorchAudio, SpeechBrain, and yt-dlp for downloading, extracting, and processing audio

Model hosted on HuggingFace: Jzuluaga/accent-id-commonaccent_xlsr-en-english

Why RunPod?: Cost-effective serverless infrastructure. It may have slow cold starts, but performance improves after initial warming.

#### Frontend

HTML, CSS, JavaScript: Lightweight static UI with no frameworks

UI polls the backend for job status using Fetch API and displays real-time results including a confidence score with color-coded accuracy.

### **IV. How Accent Detection Works**

Audio extraction: yt-dlp downloads audio from the given video URL.

Audio preprocessing: Re-sampled to 16kHz and converted to mono.

Model: A Wav2Vec2-based classifier predicts the accent class and provides a confidence score.

Output: Accent label and confidence percentage.

### **V. How to Use the App**

Open the app in the browser.

Paste a public YouTube or .mp4 link.

Click Classify Accent.

Wait for the result. A confidence percentage and accent type will appear.

### **VI. Limitations**

Supported Languages:

- us, england, australia, indian, canada, bermuda,

- scotland, african, ireland, newzealand, wales,

- malaysia, philippines, singapore, hongkong, southatlandtic

Audio Duration: Best results on samples 10–30 seconds long.

#### Model Accuracy:

Errors still occur, especially on low-quality or mixed-language audio.

Background noise may affect results.

### **VII. Recommendations**

Fine-tune the model further using high-quality, domain-specific audio.

Apply chunking and voice activity detection (VAD) to isolate valid speech segments.

Consider adding SVN filtering, noise suppression, or using a hybrid ASR + accent model approach for robustness.

Created as part of a technical challenge to demonstrate applied machine learning and serverless deployment skills.

