# SmartPaddy - AI Powered Paddy Grain Identification and Farming Assistant

SmartPaddy is a Streamlit-based application that combines paddy grain image identification with a RAG-based farming assistant.

## Main Features

- Paddy grain image upload and camera/scan input
- Image preprocessing using OpenCV
- Grain segmentation and individual grain detection
- Grain measurement and feature extraction
- Paddy variety classification using the saved Random Forest model
- Four supported varieties:
  - Sannalu — MTU 1010
  - Bondalu — PLA 1100
  - RNR 15048 — Telangana Sona
  - Swarna — MTU 7029
- Grain measurements such as length, width, area, perimeter and RGB values
- PaddyMitra RAG-based farming assistant
- Cultivation planning using the existing RAG pipeline
- FAISS-based similarity retrieval
- English, Telugu and Hindi interface support
- Streamlit web interface

## Project Structure

```text
smart_grain_grading/
├── app/
│   ├── app.py
│   ├── model_utils.py
│   ├── translations.py
│   ├── ui_theme.py
│   └── assets/
│       ├── paddy_background.jpg
│       ├── planner_rice.jpg
│       └── logo.png
│
├── models/
│   └── paddy_variety_classifier.pkl
│
├── rag/
│   ├── chatbot.py
│   ├── chunking.py
│   ├── config.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── metadata.py
│   ├── planner.py
│   ├── retriever.py
│   └── validator.py
│
├── rag_data/
│   ├── chunks.json
│   ├── index.faiss
│   └── faiss_index/
│
├── RAG_DOCUMENTS/
│   ├── bondalu_information.docx
│   ├── COMMON RICE CULTIVATION.docx
│   ├── FERTILIZER.docx
│   ├── PEST.docx
│   ├── rnr_information.docx
│   ├── sannalu_information.docx
│   ├── swarna_information.docx
│   └── WATER MANAGEMENT.docx
│
├── .streamlit/
│   └── config.toml
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Technologies Used

- Python
- Streamlit
- OpenCV
- NumPy
- Pandas
- Scikit-learn
- Random Forest
- Joblib
- FAISS
- RAG
- Python-docx
- PyPDF

## Image Identification Flow

```text
Upload / Scan Image
        ↓
Image Preprocessing
        ↓
Grayscale Conversion
        ↓
Otsu Thresholding
        ↓
Morphological Processing
        ↓
Grain Mask
        ↓
Contour Detection
        ↓
Individual Grain Filtering
        ↓
Length / Width / Area / Perimeter / RGB
        ↓
Feature Aggregation
        ↓
Random Forest Model
        ↓
Paddy Variety Prediction
```

The image-processing pipeline uses Otsu thresholding, so a fixed manual threshold value is not required.

## Model Features

The saved classifier receives these eight features:

1. Valid grain count
2. Average length
3. Average width
4. Average area
5. Average perimeter
6. Average R
7. Average G
8. Average B

The current measurements are image-based pixel measurements unless a separate physical calibration is added.

## RAG / PaddyMitra Flow

```text
User Question
      ↓
Document / Vector Retrieval
      ↓
Relevant Knowledge Chunks
      ↓
Context and Prompt
      ↓
Language Model
      ↓
PaddyMitra Response
```

The project knowledge base contains agriculture documents for paddy varieties, cultivation, fertilizer, pests and water management.

## Installation

Use Python 3.12 for the most consistent environment with the project.

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

### 2. Activate it

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the application

```powershell
python -m streamlit run app\app.py
```

The same command can be used locally before deploying.

## GitHub Upload

Do not upload:

- `.venv/`
- `__pycache__/`
- `.pyc` files
- `.ipynb_checkpoints/`
- `.env`
- API keys, passwords or other secrets

The `.gitignore` file in this repository is provided for these exclusions.

## Streamlit Deployment

This project can be deployed as a Streamlit application.

1. Push the complete project to a GitHub repository.
2. Open Streamlit Community Cloud.
3. Create a new app from the GitHub repository.
4. Select the repository and branch.
5. Set the main file to:

```text
app/app.py
```

6. Deploy the application.
7. If the existing RAG language-model backend requires a secret/API key, add that secret through the deployment platform's Secrets settings. Do not place the key inside source code or GitHub.

Make sure the folders used by the application, especially `models/`, `rag/`, `rag_data/`, `RAG_DOCUMENTS/` and `app/assets/`, are included in the GitHub repository.

## Running Locally

```powershell
cd smart_grain_grading
.venv\Scripts\activate
python -m streamlit run app\app.py
```

## Project Goal

The goal of SmartPaddy is to provide a single user-friendly application for paddy grain identification and agriculture-related information support.

## Team

- V. Shaharsha
- M. Ankitha
- Ch. Mounika
- V. Shanmitha

Guide: Abdul Aziz Md
