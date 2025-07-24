from flask import Flask, render_template, request
import PyPDF2
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['resume']
    if uploaded_file.filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        doc = nlp(text)

        name = ""
        skills = []
        education = []
        experience = []

        for ent in doc.ents:
            if ent.label_ == "PERSON" and name == "":
                name = ent.text
            elif ent.label_ == "ORG":
                experience.append(ent.text)
            elif ent.label_ == "EDUCATION":
                education.append(ent.text)

        skill_keywords = ["Python", "React", "JavaScript", "C++", "Machine Learning", "SQL"]
        for skill in skill_keywords:
            if skill.lower() in text.lower():
                skills.append(skill)

        return render_template("result.html", name=name, skills=", ".join(skills),
                               education=", ".join(education), experience=", ".join(experience))

    return "Invalid file format. Please upload a PDF."

if __name__ == '__main__':
    app.run(debug=True)
