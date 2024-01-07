from flask import Flask, request, render_template
import pickle
from mlxtend.frequent_patterns import association_rules

app = Flask(__name__)

# Load your trained Apriori model
model_path = 'model1.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form.get('item')
    
    # Find frequent itemsets and rules generated by the model
    frequent_itemsets = model[0]  # Assuming the first element is the frequent itemsets
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.01)
    
    # Filter rules based on the user's input
    recommendations = rules[rules['antecedents'].apply(lambda x: user_input in str(x))]
    
    # Extract recommended items
    recommended_items = recommendations['consequents'].tolist()
    
    return render_template('home.html', recommendations=recommended_items)

if __name__ == '__main__':
    app.run(debug=True)
