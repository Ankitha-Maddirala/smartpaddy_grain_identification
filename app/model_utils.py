from pathlib import Path

import cv2
import joblib
import numpy as np
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "models" / "paddy_variety_classifier.pkl"


# ============================================================
# MODEL FEATURE ORDER
# ============================================================

ML_FEATURES = [
    "Valid_Grain_Count",
    "Average_Length_px",
    "Average_Width_px",
    "Average_Area_px2",
    "Average_Perimeter_px",
    "Average_R",
    "Average_G",
    "Average_B",
]


# ============================================================
# DISPLAY NAME MAPPING
# ============================================================

DISPLAY_NAMES = {
    "Sannalu_MTU1010": "Sannalu — MTU 1010",
    "Bondalu_PLA1100": "Bondalu — PLA 1100",
    "RNR_15048": "RNR 15048 — Telangana Sona",
    "Swarna_MTU7029": "Swarna — MTU 7029",
    "Sannalu": "Sannalu — MTU 1010",
    "Bondalu": "Bondalu — PLA 1100",
    "RNR": "RNR 15048 — Telangana Sona",
    "Swarna": "Swarna — MTU 7029",
}


# ============================================================
# LOAD SAVED MODEL
# ============================================================

def load_model():
    """
    Load the trained paddy variety classification model.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found:\n{MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

def preprocess_image(image):
    """
    Basic preprocessing used before grain segmentation.
    """

    blurred = cv2.GaussianBlur(
        image,
        (5, 5),
        0,
    )

    gray = cv2.cvtColor(
        blurred,
        cv2.COLOR_BGR2GRAY,
    )

    hsv = cv2.cvtColor(
        blurred,
        cv2.COLOR_BGR2HSV,
    )

    return blurred, gray, hsv


# ============================================================
# CREATE GRAIN MASK
# ============================================================

def create_grain_mask(image):
    """
    Create a binary mask for detecting individual grains.
    """

    _, gray, _ = preprocess_image(image)

    _, mask = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )

    # Check the border pixels.
    # If the background is detected as foreground,
    # invert the mask.
    border_pixels = np.concatenate(
        [
            mask[0, :],
            mask[-1, :],
            mask[:, 0],
            mask[:, -1],
        ]
    )

    if np.mean(border_pixels) > 127:
        mask = cv2.bitwise_not(mask)

    # Remove small noise.
    kernel = np.ones(
        (3, 3),
        np.uint8,
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel,
        iterations=1,
    )

    # Close small gaps inside grains.
    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=1,
    )

    return mask


# ============================================================
# FIND GRAIN CONTOURS
# ============================================================

def find_grain_contours(mask):
    """
    Find external contours representing possible grains.
    """

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    return contours


# ============================================================
# VALIDATE SINGLE GRAIN
# ============================================================

def is_complete_single_grain(contour, image_shape):
    """
    Check whether a contour looks like a complete
    individual grain.
    """

    height, width = image_shape[:2]

    area_px = cv2.contourArea(contour)

    if area_px <= 0:
        return False

    x, y, w, h = cv2.boundingRect(contour)

    # Ignore grains touching the image border.
    if (
        x <= 1
        or y <= 1
        or x + w >= width - 1
        or y + h >= height - 1
    ):
        return False

    # Ignore very small objects/noise.
    if area_px < 150:
        return False

    perimeter_px = cv2.arcLength(
        contour,
        True,
    )

    if perimeter_px <= 0:
        return False

    # Solidity check.
    hull = cv2.convexHull(contour)

    hull_area = cv2.contourArea(hull)

    if hull_area <= 0:
        return False

    solidity = area_px / hull_area

    if solidity < 0.75:
        return False

    # Minimum-area rotated rectangle.
    rect = cv2.minAreaRect(contour)

    (_, _), (rw, rh), _ = rect

    if rw <= 0 or rh <= 0:
        return False

    length_px = max(rw, rh)
    width_px = min(rw, rh)

    if width_px <= 0:
        return False

    aspect_ratio = length_px / width_px

    # Paddy grain shape filter.
    if aspect_ratio < 1.2 or aspect_ratio > 6.0:
        return False

    bounding_area = w * h

    if bounding_area <= 0:
        return False

    extent = area_px / bounding_area

    if extent < 0.20:
        return False

    return True


# ============================================================
# CALCULATE MEAN RGB
# ============================================================

def calculate_mean_rgb(image, contour):
    """
    Calculate the average RGB values inside a grain contour.
    """

    grain_mask = np.zeros(
        image.shape[:2],
        dtype=np.uint8,
    )

    cv2.drawContours(
        grain_mask,
        [contour],
        -1,
        255,
        thickness=-1,
    )

    grain_pixels = image[
        grain_mask == 255
    ]

    if len(grain_pixels) == 0:
        return np.nan, np.nan, np.nan

    # OpenCV stores images as BGR.
    mean_b = np.mean(
        grain_pixels[:, 0]
    )

    mean_g = np.mean(
        grain_pixels[:, 1]
    )

    mean_r = np.mean(
        grain_pixels[:, 2]
    )

    return mean_r, mean_g, mean_b


# ============================================================
# MEASURE ONE GRAIN
# ============================================================

def measure_grain(image, contour):
    """
    Measure geometric and color properties of one grain.
    """

    area_px = cv2.contourArea(
        contour
    )

    perimeter_px = cv2.arcLength(
        contour,
        True,
    )

    rect = cv2.minAreaRect(
        contour
    )

    (_, _), (rw, rh), _ = rect

    length_px = max(
        rw,
        rh,
    )

    width_px = min(
        rw,
        rh,
    )

    mean_r, mean_g, mean_b = calculate_mean_rgb(
        image,
        contour,
    )

    return {
        "Length_px": length_px,
        "Width_px": width_px,
        "Area_px2": area_px,
        "Perimeter_px": perimeter_px,
        "Mean_R": mean_r,
        "Mean_G": mean_g,
        "Mean_B": mean_b,
    }


# ============================================================
# EXTRACT INDIVIDUAL GRAIN ROWS
# ============================================================

def extract_grain_rows(image):
    """
    Detect and measure valid individual grains
    from the uploaded/captured image.
    """

    mask = create_grain_mask(
        image
    )

    contours = find_grain_contours(
        mask
    )

    rows = []

    for contour in contours:

        if not is_complete_single_grain(
            contour,
            image.shape,
        ):
            continue

        rows.append(
            measure_grain(
                image,
                contour,
            )
        )

    return rows


# ============================================================
# BUILD MODEL FEATURES
# ============================================================

def build_prediction_features(grain_rows):
    """
    Convert individual grain measurements into the
    exact feature structure expected by the saved model.
    """

    if not grain_rows:
        raise ValueError(
            "No valid individual grains detected. "
            "Please use a clear paddy image."
        )

    df = pd.DataFrame(
        grain_rows
    )

    features = pd.DataFrame(
        {
            "Valid_Grain_Count": [
                len(df)
            ],

            "Average_Length_px": [
                df["Length_px"].mean()
            ],

            "Average_Width_px": [
                df["Width_px"].mean()
            ],

            "Average_Area_px2": [
                df["Area_px2"].mean()
            ],

            "Average_Perimeter_px": [
                df["Perimeter_px"].mean()
            ],

            "Average_R": [
                df["Mean_R"].mean()
            ],

            "Average_G": [
                df["Mean_G"].mean()
            ],

            "Average_B": [
                df["Mean_B"].mean()
            ],
        }
    )

    # IMPORTANT:
    # Keep the feature order exactly the same as the model.
    return features[
        ML_FEATURES
    ]


# ============================================================
# CONVERT MODEL OUTPUT TO USER-FRIENDLY NAME
# ============================================================

def _display_name(raw_prediction):
    """
    Convert the model's internal class name into the
    name displayed in SmartPaddy.
    """

    raw = str(
        raw_prediction
    )

    # Direct mapping.
    if raw in DISPLAY_NAMES:
        return DISPLAY_NAMES[raw]

    # Normalize common formatting differences.
    normalized = (
        raw
        .replace("-", "_")
        .replace(" ", "_")
    )

    for key, value in DISPLAY_NAMES.items():

        if normalized.lower() == key.lower():
            return value

    # Additional matching for known varieties.
    if (
        "Sannalu" in raw
        or "MTU1010" in normalized
    ):
        return "Sannalu — MTU 1010"

    if (
        "Bondalu" in raw
        or "PLA1100" in normalized
    ):
        return "Bondalu — PLA 1100"

    if (
        "RNR" in raw
        or "15048" in raw
    ):
        return "RNR 15048 — Telangana Sona"

    if (
        "Swarna" in raw
        or "MTU7029" in normalized
    ):
        return "Swarna — MTU 7029"

    return raw


# ============================================================
# MAIN PREDICTION FUNCTION
# ============================================================

def predict_paddy_image_bytes(image_bytes):
    """
    Main prediction function used by both:

    1. Upload Image
    2. Scan Grain / Camera

    Both methods use exactly the same prediction pipeline.
    """

    # Convert uploaded bytes into a NumPy image array.
    array = np.frombuffer(
        image_bytes,
        dtype=np.uint8,
    )

    # Decode image using OpenCV.
    image = cv2.imdecode(
        array,
        cv2.IMREAD_COLOR,
    )

    if image is None:
        raise ValueError(
            "The selected file is not a valid image."
        )

    # Detect individual grains.
    grain_rows = extract_grain_rows(
        image
    )

    # Convert measurements into model features.
    features = build_prediction_features(
        grain_rows
    )

    # Load trained model.
    model = load_model()

    # Predict variety.
    raw_prediction = model.predict(
        features
    )[0]

    prediction = _display_name(
        raw_prediction
    )

    # Calculate confidence when supported
    # by the saved model.
    confidence = None

    if hasattr(
        model,
        "predict_proba",
    ):
        probabilities = model.predict_proba(
            features
        )[0]

        confidence = float(
            np.max(probabilities) * 100
        )

    return {
        "prediction": prediction,
        "confidence": confidence,
        "grain_count": len(grain_rows),
    }