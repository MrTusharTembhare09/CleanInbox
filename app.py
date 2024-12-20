import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

# Initializing the stemmer
ps = PorterStemmer()

# Preprocessing function
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

# Loading the fitted vectorizer and trained model
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))  # Fitted TfidfVectorizer
model = pickle.load(open('model.pkl', 'rb'))       # Trained MultinomialNB model

# Streamlit UI
st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

if st.button('Predict'):
    # Preprocessing the input text
    transformed_sms = transform_text(input_sms)
    # Vectorizing the preprocessed text
    vector_input = tfidf.transform([transformed_sms])  # Transforming using fitted TfidfVectorizer
    # Predicting using the trained model
    result = model.predict(vector_input)[0]
    # Displaying the result
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")
