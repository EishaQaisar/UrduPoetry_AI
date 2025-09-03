# ✍️ Roman Urdu Poetry Generator (LSTM)

An **LSTM-based deep learning model** trained on thousands of Roman-Urdu poetry lines scraped from the web.  
This project generates verses inspired by classical poets in real time based on a **user-provided seed phrase**.

---

## 🚀 Features

- 🧹 **Data Cleaning** – Removed Urdu punctuation, diacritics, and special characters.
- 🔡 **Tokenization & Sequence Preparation** – Converted text into numerical sequences for LSTM training.
- 🧠 **Deep Learning Model** – Implemented a 2-layer LSTM network with embedding layer and dense output.
- 🎛️ **Temperature Tuning** – Added randomness control for more creative or deterministic verse generation.
- 🎤 **Interactive Generation** – Users can input a seed phrase to generate new poetry lines.
- 🌐 **Deployment Ready** – Can be easily deployed as a **Streamlit app** for real-time text generation.

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **Pandas** – Data loading & cleaning  
- **Regular Expressions (re)** – Removing diacritics/punctuation  
- **TensorFlow / Keras** – LSTM model training  
- **NumPy** – Array operations  
- **Scikit-learn** – Train/validation/test splitting  
- **Streamlit** (optional) – For interactive web-based generation

---

## 📂 Project Workflow

1. **Load Dataset**  
   - Read `Roman-Urdu-Poetry.csv` and extract only the `Poetry` column.

2. **Data Cleaning**  
   - Remove Urdu punctuation and diacritics using regex.

3. **Preprocessing & Tokenization**  
   - Tokenize text and create input-output sequences.
   - Pad sequences to equal length for LSTM training.

4. **Train-Test-Validation Split**  
   - 80% training, 10% validation, 10% test.

5. **Model Architecture**
   - `Embedding` layer → `LSTM (150 units)` → `LSTM (150 units)` → `Dense (ReLU)` → `Dense (Softmax)`

6. **Training**
   - Optimizer: Adam (`lr=0.001`)
   - Loss: Sparse Categorical Crossentropy
   - Trained for **55 epochs**

7. **Generation**
   - Use a seed phrase and generate poetry word-by-word with **temperature-based sampling**.

---

## 📸 Screenshot

```text
📝 Generated Poetry:
muj se pehli se mohabbat sunā hai hī paanī haiñ kaam husn jis ye se ko ki nahīñ gayā maiñ āzād thī kī nigāh bhī supurd aur 'farāz' firāq e vo jāntā uchatte
