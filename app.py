from flask import Flask, render_template, request
from scraper import get_restaurant_data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os

app = Flask(__name__)

# Replace this with your actual Yelp API key
YELP_API_KEY = '40-tLJfidP6zxC6RN7piHMDw7P1FIXEiE4oDmUBKKjSkYWyCnPsjkNW5REZE8nAAD5JQWZ0xzMBm_gbahAY6WmfnDJq0gAC16x_oXNl1zC47pBjecBr6XeQXcr-SZnYx'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form['location']
        try:
            df = get_restaurant_data(YELP_API_KEY, location)
            
            if df.empty:
                return render_template('index.html', error="No data could be retrieved for the provided location. Please try a different location.")

            # Generate some basic visualizations
            plt.figure(figsize=(10,6))
            sns.histplot(df['rating'], kde=True)
            plt.title('Distribution of Ratings')
            
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            return render_template('results.html', 
                                   tables=[df.to_html(classes='data')], 
                                   titles=df.columns.values,
                                   plot_url=plot_url)
        except Exception as e:
            return render_template('index.html', error=f"An error occurred: {str(e)}")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)