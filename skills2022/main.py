import pickle

import numpy as np
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

EXPERIENCE = [('Less than year', 'noExperience'), ('1-3 years', 'between1And3'), ('3-6 years', 'between3And6'),
              ('More than 6 years', 'moreThan6')]
with open('cities', encoding='utf-8') as f:
    CITIES = f.read().splitlines()
with open('skills', encoding='utf-8') as f:
    SKILLS = f.read().splitlines()
VACANCIES = pd.read_csv('searcher.csv')


@app.route('/')
def index():
    return render_template('index.html', experience=EXPERIENCE, cities=CITIES, skills=SKILLS, vacancies={})


def salary_predictor(to_predict):
    to_predict = np.resize(np.array(to_predict), (1, 11))
    loaded_model = pickle.load(open("model.pkl", "rb"))
    result = loaded_model.predict(to_predict)
    return int(result[0])


def compare_skills(applicant, vacancy):
    applicant_set = set(applicant)
    vacancy_set = set(vacancy)
    more = applicant_set - vacancy_set
    less = vacancy_set - applicant_set
    return len(less) + len(more)


def search(applicant):
    if len(applicant) == 2: applicant.append('None')
    vac = VACANCIES[(VACANCIES.location == applicant[0]) * (VACANCIES.experience == applicant[1])]
    vac['srt'] = vac['key_skills'].apply(lambda skills: compare_skills(applicant[2:], skills))
    return vac.sort_values(by='srt')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        from_client = request.form.to_dict()
        skills = from_client.get('skills').split()
        applicant = [str(from_client.get('city')), str(from_client.get('experience'))] + skills
        salary = salary_predictor(applicant)

        return render_template("index.html", experience=EXPERIENCE, cities=CITIES, prediction=str(salary) + '₽',
                               skills=SKILLS, vacancies=search(applicant).to_dict(orient='records'))
    else:
        return index()


if __name__ == '__main__':
    app.run(debug=1)
