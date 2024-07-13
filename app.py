from flask import Flask, render_template, request
from scraper import scrape_tripadvisor
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        df = scrape_tripadvisor(url)
        
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
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)