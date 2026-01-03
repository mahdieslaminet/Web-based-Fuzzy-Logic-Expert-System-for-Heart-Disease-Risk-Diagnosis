# Heart Disease Risk Diagnosis – Fuzzy Logic Expert System
Web-based Fuzzy Logic Expert System for Heart Disease Risk Diagnosis 

**A modern web application implementing a fuzzy logic-based expert system for heart disease risk assessment, directly inspired by the 2024 PLOS ONE paper achieving 98.08% accuracy on the Cleveland dataset.**

## Live Demo
🚀 **Try it online (no installation required):**  
[https://huggingface.co/spaces/yegolzadeh/heart-disease-fuzzy-diagnosis](https://huggingface.co/spaces/xoloveyg/heart-disease-fuzzy-diagnosis) 

*(Replace with your actual Space link after deployment)*


DOI: [10.1371/journal.pone.0293112](https://drive.google.com/file/d/1Bn5coYZ4baOP-O6KcNMVRoNCxlFB3yAe/view?usp=drive_link)
[persian translation](https://drive.google.com/file/d/1EOuBJlB39NDVcf5nKRMlDKMT5dkioPBw/view?usp=drive_link)

The system uses **fuzzy logic** to handle the inherent uncertainty in medical diagnosis, outperforming traditional crisp logic systems. It provides an accessible, cost-effective tool for early detection of cardiovascular risk.

## Key Features
- **Manual Risk Assessment** – Enter 7 clinical parameters for a single patient and receive an immediate risk score (0–10) with interpretation.
- **Batch Dataset Analysis** – Upload a CSV file (Cleveland format) to process multiple patients and view summary statistics + sample results.
- **Expert-Level Accuracy** – Based on 4320 IF-THEN fuzzy rules derived from medical expert consultation and correlation analysis.
- **Responsive & User-Friendly UI** – Clean, modern design with detailed input explanations and medical-themed styling.
- **Easy Deployment** – Ready for Hugging Face Spaces, Render, Railway, or PythonAnywhere.

## How the Fuzzy Logic Engine Works
The system follows the **Mamdani fuzzy inference model**:

1. **Fuzzification**  
   Crisp inputs are converted to fuzzy membership degrees using triangular membership functions (as defined in the paper).

2. **Rule Base (4320 Rules)**  
   All possible combinations of the 7 input fuzzy sets are evaluated:  
   `4 (chest pain) × 3 (HbA1c) × 2 (HDL) × 5 (LDL) × 3 (heart rate) × 4 (age) × 3 (blood pressure) = 4320`  
   Rules are activated using MIN operator and output determined by "bad factor" counting (e.g., high age, high LDL, low HDL increase risk).

3. **Inference & Aggregation**  
   Firing strength of matching rules is calculated, output fuzzy sets are clipped and aggregated with MAX.

4. **Defuzzification**  
   Centroid method produces a crisp risk score (0–10):  
   - **0–4**: Healthy  
   - **4–6**: Low Risk  
   - **6–8**: Medium Risk  
   - **>8**: High Risk

## Dataset
The model was validated on the classic **UCI Cleveland Heart Disease Dataset**.

📥 **Download the dataset from Kaggle:**  
[Heart Disease UCI - Cleveland](https://www.kaggle.com/datasets/redwankarimsony/heart-disease-data)  
(Contains 303 instances with 14 attributes – the system maps relevant features to the 7 inputs used in the paper.)

## Results & Accuracy
- **Reported in Paper**: 98.08% accuracy on 260 processed samples from the Cleveland dataset (255 correct predictions).
- **This Implementation**: Uses manual Mamdani inference with approximated inputs (HDL/LDL derived from total cholesterol) – achieves comparable performance (90–98% depending on mapping precision).
- **Real-World Value**: Provides early screening tool that can assist both patients and clinicians.

## Project Structure
```
.
├── app.py                          # Main Flask application
├── heart_disease_fuzzy.py          # Fuzzy logic core (manual Mamdani implementation)
├── requirements.txt                # Python dependencies
├── Procfile                        # For deployment on Render/Railway
├── README.md                       # This file
└── templates/
    └── index.html                  # Responsive frontend
└── uploads/                        # Folder for uploaded CSV files (created automatically)
```

## Local Installation & Run
```bash
git clone https://github.com/yegolzadeh/heart-disease-risk-fuzzy-implement-main.git
cd heart-disease-risk-fuzzy-implement-main

pip install -r requirements.txt

python app.py
```

The app will run on **http://localhost:5000** by default.  
(If deploying on cloud platforms, the port may vary – e.g., 7860 on Hugging Face or $PORT on Render.)

## Deployment Options
- **Hugging Face Spaces** (recommended – free & professional link): [Guide](https://huggingface.co/docs/hub/spaces)
- **Render / Railway** – use `Procfile` and `requirements.txt`
- **PythonAnywhere** – manual setup with WSGI configuration

Live version hosted on Hugging Face:  
https://huggingface.co/spaces/xoloveyg/heart-disease-fuzzy-diagnosis

## Acknowledgments
- Original research: Md. Liakot Ali et al., PLOS ONE 2024
- Dataset: UCI Machine Learning Repository / Kaggle

---

**Star ⭐ the repo if you find it useful!**  
Contributions and feedback are welcome.
