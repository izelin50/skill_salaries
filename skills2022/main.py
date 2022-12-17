import os
import numpy as np
import flask
import pickle
from flask import Flask, render_template, request


app=Flask(__name__)

@app.route('/')
def infex():
    return render_template('index.html')



# prediction function
def salary_predictor(to_predict):
    to_predict = np.resize(np.array(to_predict),(1,11))
    loaded_model = pickle.load(open("model.pkl", "rb"))
    result = loaded_model.predict(to_predict)
    return int(result[0])


@app.route('/result', methods=['POST','GET'])
def result():
    if request.method == 'POST':
        to_predict=request.form.to_dict()
        skills=to_predict.get('skills').split()
        skills=[str(to_predict.get('city')),str(to_predict.get('experience'))]+skills
        salary = salary_predictor(skills)

        return render_template("index.html", prediction=str(salary)+'₽')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

