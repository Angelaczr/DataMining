# Import the Flask module from the flask package
from flask import Flask,render_template
import pandas as pd

data = pd.read_csv("data2.csv")
data = data.T.drop_duplicates(keep='first').T
data_product = data.columns[1:].tolist()

print(data_product)
# Create an instance of the Flask class. This instance will be the WSGI application.
app = Flask(__name__)

# Define the basic route '/' and its corresponding request handler
@app.route('/home')
def home():
    return render_template("home.html",products=data_product)

@app.route('/hasil')
def hasil():
    return render_template("hasil.html")
# Check if the executed file is the main program and run the app
if __name__ == '__main__':
    # Start the Flask application on the local development server
    app.run(host="0.0.0.0",debug=True)
