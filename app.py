from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

lr = LinearRegression()

lr.coef_ = np.array([88.28378339070616, 6.17510103558709, -3.3259504524923846, 715.1315081390832, 2.4911388839679147])
lr.intercept_ = -803

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        gender = request.form["gender"]
        weight = float(request.form["weight"])
        height = float(request.form["height"])
        avg_bpm = float(request.form["avg_bpm"])
        age = int(request.form["age"])
        session_duration = float(request.form["session_duration"])
        experience_level = int(request.form["experience_level"])
    
        if gender.lower() == "male":
            gender = 0
        elif gender.lower() == "female":
            gender = 1
        else: 
            return "Invalid gender input. Please enter 'Male' or 'Female'."
        if weight <= 0:
            return "Invalid weight input. Please enter positive weight."
        if height <= 0:
            return "Invalid height input. Please enter positive height."
        if avg_bpm <= 0:
            return "Invalid average BPM input. Please enter positive average BPM."
        if age <= 0:
            return "Invalid age input. Please enter positive age."
        if session_duration <= 0:
            return "Invalid session duration input. Please enter positive session duration."
        if  experience_level < 1 or experience_level > 3:
            return "Invalid experience level input. Please enter correct experience level."
            

        input_data = pd.DataFrame([[gender, avg_bpm, age, session_duration, experience_level]],
                                  columns=['Gender', 'Avg_BPM', 'Age', 'Session_Duration (hours)', 'Experience_Level'])

        predicted_calories = lr.predict(input_data)
        predicted_calories_rounded = [round(cal, 2) for cal in predicted_calories]
        return render_template("index.html", prediction=predicted_calories_rounded[0])

    return render_template("index.html", prediction=None)

if __name__ == "__main__":
    app.run(debug=True)
