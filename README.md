# Review Sentiment Analysis

This project contains a simple web page that uses a saved scikit-learn sentiment model to classify user-entered text as Negative, Neutral, or Positive.

## Project files

- `index.html` - the frontend interface for entering sentences and displaying results
- `app.py` - a small local server that serves the page and runs predictions with the saved model
- `sentiment_analysis_model.pkl` - the trained sentiment analysis model
- `sentiment.ipynb` - the notebook used to train and export the model

## Requirements

Make sure Python is installed and the project dependencies are available.

The project uses:
- Python 3
- scikit-learn
- joblib

## Run the app locally

From the project folder, run:

```bash
python app.py
```

Then open your browser at:

```text
http://127.0.0.1:8000
```

## How to use it

1. Open the web page in your browser.
2. Type a sentence into the input box.
3. Click "Analyze Sentiment".
4. The app will display the predicted sentiment label.

## Notes

The model was trained in the notebook and exported as a pickle file. The web app loads that file directly and uses it for predictions.
