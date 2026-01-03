# app.py - Simple version: Manual Input + Dataset Upload (NO CHARTS)
from flask import Flask, request, render_template, flash
import pandas as pd
import numpy as np
import os
from werkzeug.utils import secure_filename
from heart_disease_fuzzy import predict_risk

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# فقط پوشه آپلود رو بساز (پوشه charts لازم نیست)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_dataset(df):
    if df.empty:
        return None, "<p>The dataset is empty.</p>"

    # رفع مشکل دیتاست Cleveland (جایگزینی ? با NaN و تبدیل به عدد)
    df = df.replace('?', np.nan)
    numeric_cols = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'fbs', 'cp']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # حذف ردیف‌های نامعتبر
    df = df.dropna(subset=['age', 'cp', 'trestbps', 'chol', 'thalach', 'fbs'])

    # مپینگ ورودی‌ها بر اساس مقاله
    df['chest_pain_mapped'] = df['cp'].map({1: 7, 2: 5, 3: 3, 4: 1}).fillna(1)
    df['hba1c'] = np.where(df['fbs'] == 1, 9.0, 5.5)
    df['hdl'] = df['chol'] * 0.25
    df['ldl'] = df['chol'] * 0.45
    df['heart_rate'] = df['thalach']
    df['age_mapped'] = df['age']
    df['bp_mapped'] = df['trestbps']

    # پیش‌بینی ریسک
    risks = []
    levels = []
    for _, row in df.iterrows():
        try:
            risk_val = predict_risk(
                float(row['chest_pain_mapped']),
                float(row['hba1c']),
                float(row['hdl']),
                float(row['ldl']),
                float(row['heart_rate']),
                float(row['age_mapped']),
                float(row['bp_mapped'])
            )
            risk_val = round(risk_val, 2)
            risks.append(risk_val)
            level = ("Healthy" if risk_val < 4 else
                     "Low Risk" if risk_val < 6 else
                     "Medium Risk" if risk_val < 8 else "High Risk")
            levels.append(level)
        except:
            risks.append(None)
            levels.append("Error")

    df['predicted_risk'] = risks
    df['risk_level'] = levels

    # آمار خلاصه
    valid_count = df['predicted_risk'].notna().sum()
    stats = {
        'total': len(df),
        'valid_predictions': valid_count,
        'avg_risk': round(df['predicted_risk'].mean(), 2) if valid_count > 0 else 0,
        'high_risk_count': (df['risk_level'] == 'High Risk').sum(),
        'high_risk_percent': round(((df['risk_level'] == 'High Risk').sum() / len(df)) * 100, 1)
    }

    # جدول نمونه
    display_cols = ['age', 'cp', 'trestbps', 'chol', 'thalach', 'predicted_risk', 'risk_level']
    summary_html = pd.concat([df.head(10), df.tail(10)])[display_cols].to_html(
        classes='table table-striped', index=False, na_rep='N/A')

    return stats, summary_html

@app.route('/', methods=['GET', 'POST'])
def index():
    manual_result = None
    manual_score = None
    manual_level = None
    uploaded_stats = None
    uploaded_table = "<p>No dataset uploaded yet.</p>"

    # ورودی دستی
    if request.method == 'POST' and 'chest_pain' in request.form:
        try:
            inputs = {
                'cp': float(request.form['chest_pain']),
                'hba': float(request.form['hba1c']),
                'hd': float(request.form['hdl']),
                'ld': float(request.form['ldl']),
                'hr': float(request.form['heart_rate']),
                'ag': float(request.form['age']),
                'bp': float(request.form['blood_pressure'])
            }
            risk_value = round(predict_risk(**inputs), 2)
            level = ("Healthy" if risk_value < 4 else
                     "Low Risk" if risk_value < 6 else
                     "Medium Risk" if risk_value < 8 else "High Risk")
            manual_result = "success"
            manual_score = risk_value
            manual_level = level
        except:
            manual_result = "error"
            manual_level = "Please enter valid numeric values."

    # آپلود دیتاست
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            flash('No file selected.', 'danger')
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                # تشخیص خودکار فرمت Cleveland
                if 'cleveland' in filename.lower():
                    df = pd.read_csv(filepath, header=None, na_values='?')
                    df.columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach',
                                  'exang', 'oldpeak', 'slope', 'ca', 'thal', 'num']
                else:
                    df = pd.read_csv(filepath, na_values='?')

                uploaded_stats, uploaded_table = process_dataset(df)
                flash('Dataset analyzed successfully!', 'success')
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'danger')
        else:
            flash('Only CSV files are allowed.', 'danger')

    return render_template('index.html',
                           manual_result=manual_result,
                           manual_score=manual_score,
                           manual_level=manual_level,
                           uploaded_stats=uploaded_stats,
                           uploaded_table=uploaded_table)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)