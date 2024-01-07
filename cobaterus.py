from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

pickle_in = open("model1.pkl", "rb")
loaded_rules = pickle.load(pickle_in)

data = pd.read_csv("data2.csv")
data = data.T.drop_duplicates(keep='first').T
data_product = data.columns[1:].tolist()

# print(data_product)

def recommend(item_input):
    # Filter aturan yang memiliki item input di antecedents
    recommendations = loaded_rules[loaded_rules['antecedents'].apply(lambda x: item_input in x)]
    
    # Sortir berdasarkan confidence atau lift
    recommendations = recommendations[(recommendations.support > 0.02) & (recommendations.confidence > 0.02)].sort_values(by='confidence', ascending=False)
    
    # item_names = recommendations['consequents'].apply(lambda x: next(iter(x))).tolist()
    
    # return item_names
    # Mengambil hanya nama item dari consequents dan mengubahnya menjadi list
    recommendation_info = []
    recommendation_info = []
    for _, row in recommendations.iterrows():
        item = next(iter(row['consequents']))
        support = row['support'] * 100
        confidence = row['confidence'] * 100
        recommendation_info.append(f"{item} dengan nilai Support: {support:.1f}% dan Confidence: {confidence:.1f}%")

    return ', '.join(recommendation_info)

@app.route('/')
@app.route('/home')
def home():
    return render_template('homelama.html',products=data_product)

@app.route('/hasil', methods=['GET', 'POST'])
def hasil():
    try:
        if request.method == 'POST':
            # Replace 'input_name' with your actual form input name
            user_input = request.form['product']
            
            # Process the input with your model here
            results = recommend(user_input)

            if(results==""):
                results="Tidak ada rekomendasi"
                print(results)
            
            print(results)
            
            # Pass the results to the "hasil.html" template
            return render_template("hasil.html", prediction=results)
        return render_template("hasil.html")
    except Exception as e:
        # Render an error page with the error message
        return render_template("error.html", error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in a production environment
