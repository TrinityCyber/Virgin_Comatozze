import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, jsonify, request
from flask_cors import CORS 

app = Flask(__name__)

CORS(app) 
analyzer = SentimentIntensityAnalyzer()

try:
    df = pd.read_csv('extracted.csv') 
    
    comments = df['Comment'].tolist()

except FileNotFoundError:
    
    comments = ["Error: Could not find extracted.csv.", "Please make sure the file is in the same folder as app.py."]
except KeyError:

    comments = ["Error: Found 'extracted.csv', but could not find a column named 'Comment'.", "Please check your CSV file's column headers."]
except Exception as e:

    comments = [f"An unexpected error occurred: {e}"]



def analyze_comments(comment_list):
    """Analyzes a list of comments and calculates overall sentiment."""
    positive_count = 0
    total_comments = len(comment_list)

    if total_comments == 0:
        return 0.0, 0.0, 0.0 

    for comment in comment_list:
    
        vs = analyzer.polarity_scores(str(comment)) 
        
        if vs['compound'] >= 0.05:
            positive_count += 1
    
    sentiment_percentage = (positive_count / total_comments) * 100
    
    engagement_rate = sentiment_percentage * 0.95 + 5 
    engagement_rate = min(engagement_rate, 99.9) 
    
    return sentiment_percentage, engagement_rate

@app.route('/analyze', methods=['GET'])
def get_analysis():
    """Returns the analysis results as JSON."""
    
    sentiment_pct, engagement_pct = analyze_comments(comments)

    if sentiment_pct >= 70:
        reception = 'positive'
        title = 'Highly Positive Reception'
        icon = 'fa-smile-beam'
    elif sentiment_pct >= 40:
        reception = 'mixed'
        title = 'Mixed Audience Opinion'
        icon = 'fa-meh'
    else:
        reception = 'negative'
        title = 'Negative Reception'
        icon = 'fa-frown'

    result = {
        'type': reception,
        'icon': icon,
        'title': title,
        'description': f'Analysis based on {len(comments)} sample comments.',
        'sentiment': round(sentiment_pct, 1),
        'engagement': round(engagement_pct, 1),
        'likes': 1500, 
        'views': 25000 
    }

    return jsonify(result)

# --- Run Server ---
if __name__ == '__main__':

    app.run(debug=True)