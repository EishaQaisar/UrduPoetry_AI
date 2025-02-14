import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.text import Tokenizer

# Set page config
st.set_page_config(page_title="Urdu Shayari with AI", page_icon="🌙", layout="wide")

# Custom CSS for consistent theme
st.markdown(
    """
    <style>
        body {
            background-color: #0D1B2A;;
            color: #EAEAEA;
            font-family: 'Georgia', serif;
        }
        .stApp {
            background-color: #0D1B2A;;
        }
        .main-header {
            text-align: center;
            font-size: 3em;
            font-weight: bold;
            color: #FFFFFF !important;
            text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5);
        }
        .main-header2 {
            text-align: left;
            font-size: 2em;
            font-weight: bold;
            color: #FFFFFF !important;
            text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5);
        }
        .sub-header {
            text-align: center;
            font-size: 1.4em;
            font-style: italic;
            color: #FFA500;
        }
        .info-box, .poetry-output {
            background: linear-gradient(135deg, #14213D, #1B263B);

            border-radius: 15px;
            padding: 20px;
            color: #E0E1DD;
            border: 2px solid #FFA500;
            text-align: center;
            margin: auto;
            width: 90%;
            box-shadow: 2px 2px 10px rgba(255, 215, 0, 0.2);
            margin-bottom:20px
        }
        .stTextInput > div > div > input {
            background-color:1B263B;
            color: #000000;
            border: 2px solid #FFA500;
            border-radius: 8px;
            padding: 10px;
        }
        .stButton > button {
            background: linear-gradient(135deg, #14213D, #1B263B);
            color: #F4A261;
            font-weight: bold;
            border-radius: 12px;
            padding: 12px;
            box-shadow: 2px 2px 8px rgba(255, 165, 0, 0.3);
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #FFD700, #FFA500);
        }
        .download-button-container {
        display: flex;
        justify-content: center;
        align-items:center;
        margin-top: 10px;
        text-align:center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load model and tokenizer
@st.cache_resource
def load_model_and_tokenizer():
    model = tf.keras.models.load_model("lstm_poetry_model.h5")
    model.compile(loss="sparse_categorical_crossentropy", optimizer=Adam(learning_rate=0.001), metrics=["accuracy"])
    
    df = pd.read_csv("Roman-Urdu-Poetry.csv")
    all_poetry = " ".join(df["Poetry"].astype(str).tolist()).lower()
    
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([all_poetry])
    
    return model, tokenizer

model, tokenizer = load_model_and_tokenizer()

# Poetry generation function
def generate_poetry(seed_text, next_words, model, tokenizer, sequence_length, temperature=1.0):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=sequence_length, padding='pre')
        predicted_probs = model.predict(token_list, verbose=0)[0]
        predicted_probs = np.log(predicted_probs + 1e-8) / temperature
        predicted_probs = np.exp(predicted_probs) / np.sum(np.exp(predicted_probs))
        predicted_word_index = np.random.choice(len(predicted_probs), p=predicted_probs)
        next_word = [word for word, index in tokenizer.word_index.items() if index == predicted_word_index]
        if not next_word:
            continue
        seed_text += " " + next_word[0]
    return seed_text

# Sidebar for user input
st.sidebar.header("🔧 Customize Your Poetry")
seed_text = st.sidebar.text_input("Enter a seed word or phrase:", value="mohabbat")
next_words = st.sidebar.slider("Verse Length:", min_value=10, max_value=100, value=50, step=5)
temperature = st.sidebar.slider("Creativity Level:", min_value=0.1, max_value=1.5, value=0.8, step=0.1)

st.markdown('<h1 class="main-header"> Urdu Shayari with AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">"Where AI crafts the soul of poetry"</p>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="info-box">
        Welcome to <strong>Urdu Shayari with AI</strong> – a harmonious blend of art and technology.
        Enter a seed phrase in <em>Roman Urdu</em>, choose your poetic preferences, and let AI create mesmerizing Urdu verses for you.
    </div>
    """,
    unsafe_allow_html=True
)

if st.sidebar.button("✨ Craft Poetry ✨"):
    with st.spinner("Weaving the tapestry of words..."):
        generated_poetry = generate_poetry(seed_text, next_words, model, tokenizer, sequence_length=10, temperature=temperature)
    
    st.markdown('<h4>  📜 Your Poetic Masterpiece </h4>',unsafe_allow_html=True)
    st.markdown(f'<div class="poetry-output">{generated_poetry}</div>', unsafe_allow_html=True)
    st.markdown('<div class="download-button-container">', unsafe_allow_html=True)

    
    st.download_button(
        label="📩 Save Your Poetry",
        data=generated_poetry,
        file_name="urdu_poetry.txt",
        mime="text/plain"
    )
    st.markdown('</div>', unsafe_allow_html=True)


st.markdown("---")
st.markdown('<p style="text-align: center; color: #FFA500;">💛 Crafted with passion for poetry & AI 💛</p>', unsafe_allow_html=True)