import os
import re
import yaml
from flask import Flask, render_template, request
import mysql.connector
import pandas as pd


app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'veer',
    'password': 'veer@945050',
    'database': 'training_app'
}




@app.route('/')
def training_ui():
    return render_template('training_ui.html')

@app.route('/train_from_excel')
def train_from_excel():
    return render_template('train_from_excel.html')


def generate_nlu_yml_from_excel_english(excel_file_path):
    df_en = pd.read_excel(excel_file_path, sheet_name='English')
    df_hi = pd.read_excel(excel_file_path, sheet_name='English')

    nlu_content = "nlu:\n"
    for index, row in df_en.iterrows():
        intent = row['Questions_In_English'].split('\n')[0].replace(" ", "_") + '_en'
        intent = intent.replace(":", "")  # Remove the colon from the intent name
        examples_hi = df_hi.iloc[index]['Questions_In_English']
        nlu_content += f"- intent: {intent}\n"
        nlu_content += f"  examples: |\n"
        for line in examples_hi.split('\n'):
            nlu_content += f"    - {line}\n"

    return nlu_content

def clean_intent_name(name):
    cleaned_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    return cleaned_name.rstrip('_') + '_ur'

def generate_domain_yml_from_excel_english(excel_file_path):
    df = pd.read_excel(excel_file_path)
    intents_responses = {}
    
    for index, row in df.iterrows():
        intent = row['Questions_In_English'].split('\n')[0]
        intent = clean_intent_name(intent)
        response_ur = row['Answers_In_English'].split('\n')[0]
        
        intents_responses[intent] = response_en

    domain_yml_content = "intents:\n"
    for intent in intents_responses:
        domain_yml_content += f"  - {intent}\n"
    
    domain_yml_content += "\nresponses:\n"
    for intent, response in intents_responses.items():
        domain_yml_content += f"  utter_{intent}:\n"
        domain_yml_content += f"    - text: |\n"
        lines = response.split('\n')
        for line in lines:
            domain_yml_content += f"        {line}\n"

    return domain_yml_content

def generate_nlu_yml_from_excel_hindi(excel_file_path):
    df_en = pd.read_excel(excel_file_path, sheet_name='English')
    df_hi = pd.read_excel(excel_file_path, sheet_name='English')

    nlu_content = "nlu:\n"
    for index, row in df_en.iterrows():
        intent = row['Questions_In_English'].split('\n')[0].replace(" ", "_") + '_hi'
        intent = intent.replace(":", "")  # Remove the colon from the intent name
        examples_hi = df_hi.iloc[index]['Questions_In_Hindi']
        nlu_content += f"- intent: {intent}\n"
        nlu_content += f"  examples: |\n"
        for line in examples_hi.split('\n'):
            nlu_content += f"    - {line}\n"

    return nlu_content

def generate_domain_yml_from_excel_hindi(excel_file_path):
    df = pd.read_excel(excel_file_path)
    intents_responses = {}
    
    for index, row in df.iterrows():
        intent = row['Questions_In_English'].split('\n')[0]
        intent = clean_intent_name(intent)
        response_ur = row['Answers_In_Hindi'].split('\n')[0]
        
        intents_responses[intent] = response_ur  # Use response_ur instead of response_hi

    domain_yml_content = "intents:\n"
    for intent in intents_responses:
        domain_yml_content += f"  - {intent}\n"
    
    domain_yml_content += "\nresponses:\n"
    for intent, response in intents_responses.items():
        domain_yml_content += f"  utter_{intent}:\n"
        domain_yml_content += f"    - text: |\n"
        lines = response.split('\n')
        for line in lines:
            domain_yml_content += f"        {line}\n"

    return domain_yml_content


def generate_nlu_yml_from_excel_urdu(excel_file_path):
    df_en = pd.read_excel(excel_file_path, sheet_name='English')
    df_hi = pd.read_excel(excel_file_path, sheet_name='English')

    nlu_content = "nlu:\n"
    for index, row in df_en.iterrows():
        intent = row['Questions_In_English'].split('\n')[0].replace(" ", "_") + '_ur'
        intent = intent.replace(":", "")  # Remove the colon from the intent name
        examples_hi = df_hi.iloc[index]['Questions_In_Urdu']
        nlu_content += f"- intent: {intent}\n"
        nlu_content += f"  examples: |\n"
        for line in examples_hi.split('\n'):
            nlu_content += f"    - {line}\n"

    return nlu_content

def generate_domain_yml_from_excel_urdu(excel_file_path):
    df = pd.read_excel(excel_file_path)
    intents_responses = {}
    
    for index, row in df.iterrows():
        intent = row['Questions_In_English'].split('\n')[0]
        intent = clean_intent_name(intent)
        response_ur = row['Answers_In_Urdu'].split('\n')[0]
        
        intents_responses[intent] = response_ur

    domain_yml_content = "intents:\n"
    for intent in intents_responses:
        domain_yml_content += f"  - {intent}\n"
    
    domain_yml_content += "\nresponses:\n"
    for intent, response in intents_responses.items():
        domain_yml_content += f"  utter_{intent}:\n"
        domain_yml_content += f"    - text: |\n"
        lines = response.split('\n')
        for line in lines:
            domain_yml_content += f"        {line}\n"

    return domain_yml_content

def generate_stories_yml_from_yml_english(domain_file_path):
    stories_data = {"version": "3.1", "stories": []}

    with open(domain_file_path, "r") as domain_file:
        domain_data = yaml.safe_load(domain_file)

    for intent in domain_data.get("intents", []):
        intent_name = intent.strip()
        action_name = f"utter_{intent_name}"

        story = {
            "story": f"{intent_name} en",
            "steps": [
                {"intent": intent_name, "action": action_name}
            ],
        }

        stories_data["stories"].append(story)

    return stories_data


def generate_stories_yml_from_yml_hindi(domain_file_path):
    stories_data = {"version": "3.1", "stories": []}

    with open(domain_file_path, "r") as domain_file:
        domain_data = yaml.safe_load(domain_file)

    for intent in domain_data.get("intents", []):
        intent_name = intent.strip()
        action_name = f"utter_{intent_name}"

        story = {
            "story": f"{intent_name} hi",
            "steps": [
                {"intent": intent_name, "action": action_name}
            ],
        }

        stories_data["stories"].append(story)

    return stories_data

def generate_stories_yml_from_yml_urdu(domain_file_path):
    stories_data = {"version": "3.1", "stories": []}

    with open(domain_file_path, "r") as domain_file:
        domain_data = yaml.safe_load(domain_file)

    for intent in domain_data.get("intents", []):
        intent_name = intent.strip()
        action_name = f"utter_{intent_name}"

        story = {
            "story": f"{intent_name} ur",
            "steps": [
                {"intent": intent_name, "action": action_name}
            ],
        }

        stories_data["stories"].append(story)

    return stories_data

@app.route('/generate_nlu_english', methods=['POST'])
def generate_nlu_route_english():
    if 'nluFile' not in request.files:
        return "No file part"

    nlu_file = request.files['nluFile']

    if nlu_file.filename == '':
        return "No selected file"

    if nlu_file:
        excel_file_name = os.path.splitext(nlu_file.filename)[0]  # Corrected indentation
        # Save the uploaded Excel file to a temporary location
        excel_file_path = 'temp.xlsx'
        nlu_file.save(excel_file_path)

        # Generate NLU content from the uploaded Excel file
        nlu_yml_content = generate_nlu_yml_from_excel_english(excel_file_path)

        # Save the generated nlu.yml content to a file
        nlu_filename = f"{excel_file_name}_nlu_english.yml"
        with open(nlu_filename, "w") as nlu_file:
            nlu_file.write(nlu_yml_content)

        return "NLU File generated!"



@app.route('/generate_nlu_hindi', methods=['POST'])
def generate_nlu_route_hindi():
    if 'nluFile' not in request.files:
        return "No file part"

    nlu_file = request.files['nluFile']

    if nlu_file.filename == '':
        return "No selected file"

    if nlu_file:
        excel_file_name = os.path.splitext(nlu_file.filename)[0]  # Corrected indentation
        # Save the uploaded Excel file to a temporary location
        excel_file_path = 'temp.xlsx'
        nlu_file.save(excel_file_path)

        # Generate NLU content from the uploaded Excel file
        nlu_yml_content = generate_nlu_yml_from_excel_hindi(excel_file_path)

        # Save the generated nlu.yml content to a file
        nlu_filename = f"{excel_file_name}_nlu_hindi.yml"
        with open(nlu_filename, "w") as nlu_file:
            nlu_file.write(nlu_yml_content)

        return "NLU File generated!"



@app.route('/generate_nlu_urdu', methods=['POST'])
def generate_nlu_route_urdu():
    if 'nluFile' not in request.files:
        return "No file part"

    nlu_file = request.files['nluFile']

    if nlu_file.filename == '':
        return "No selected file"


    if nlu_file:
        excel_file_name = os.path.splitext(nlu_file.filename)[0]  # Corrected indentation
        # Save the uploaded Excel file to a temporary location
        excel_file_path = 'temp.xlsx'
        nlu_file.save(excel_file_path)

        # Generate NLU content from the uploaded Excel file
        nlu_yml_content = generate_nlu_yml_from_excel_urdu(excel_file_path)

        # Save the generated nlu.yml content to a file
        nlu_filename = f"{excel_file_name}_nlu_urdu.yml"
        with open(nlu_filename, "w") as nlu_file:
            nlu_file.write(nlu_yml_content)

        return "NLU File generated!"



@app.route('/generate_domain_english', methods=['POST'])
def generate_domain_route_english():
    if 'domainFile' not in request.files:
        return "No file part"

    domain_file = request.files['domainFile']

    if domain_file.filename == '':
        return "No selected file"

    if domain_file:
        excel_file_name = os.path.splitext(domain_file.filename)[0]

        # Save the uploaded Excel file to a temporary location
        excel_file_path = 'temp.xlsx'
        domain_file.save(excel_file_path)

        # Generate Domain content from the uploaded Excel file
        domain_yml_content = generate_domain_yml_from_excel_english(excel_file_path)
        domain_filename = f"{excel_file_name}_domain_english.yml"

        # Save the generated domain.yml content to a file
        with open(domain_filename, "w") as domain_file:
            domain_file.write(domain_yml_content)

        return "Domain English File generated!"


@app.route('/generate_domain_hindi', methods=['POST'])
def generate_domain_route_hindi():
    if 'domainFile' not in request.files:
        return "No file part"

    domain_file = request.files['domainFile']

    if domain_file.filename == '':
        return "No selected file"

    if domain_file:
        excel_file_name = os.path.splitext(domain_file.filename)[0]

        # Save the uploaded Excel file to a temporary location
        excel_file_path = 'temp.xlsx'
        domain_file.save(excel_file_path)

        # Generate Domain content from the uploaded Excel file
        domain_yml_content = generate_domain_yml_from_excel_hindi(excel_file_path)
        domain_filename = f"{excel_file_name}_domain_hindi.yml"

        # Save the generated domain.yml content to a file
        with open(domain_filename, "w") as domain_file:
            domain_file.write(domain_yml_content)

        return "Domain Hindi File generated!"

@app.route('/generate_domain_urdu', methods=['POST'])
def generate_domain_route_urdu():
    if 'domainFile' not in request.files:
        return "No file part"

    domain_file = request.files['domainFile']

    if domain_file.filename == '':
        return "No selected file"

    if domain_file:
        excel_file_name = os.path.splitext(domain_file.filename)[0]

        # Save the uploaded Excel file to a temporary location
        excel_file_path = 'temp.xlsx'
        domain_file.save(excel_file_path)

        # Generate Domain content from the uploaded Excel file
        domain_yml_content = generate_domain_yml_from_excel_urdu(excel_file_path)
        domain_filename = f"{excel_file_name}_domain_urdu.yml"

        # Save the generated domain.yml content to a file
        with open(domain_filename, "w") as domain_file:
            domain_file.write(domain_yml_content)

        return "Domain Urdu File generated!"


@app.route('/generate_stories_english', methods=['POST'])
def generate_stories_route_english():
    if 'storiesFile' not in request.files:
        return "No file part"

    stories_file = request.files['storiesFile']

    if stories_file.filename == '':
        return "No selected file"

    if stories_file:
        yml_file_name = os.path.splitext(stories_file.filename)[0]

        # Save the uploaded YAML file to a temporary location
        yml_file_path = 'temp.yml'
        stories_file.save(yml_file_path)

        # Generate stories YAML content from the uploaded YAML file
        stories_yml_content = generate_stories_yml_from_yml_english(yml_file_path)
        stories_filename = f"{yml_file_name}_stories_english.yml"

        # Save the generated stories YAML content to a file
        with open(stories_filename, "w") as stories_file:
            yaml.dump(stories_yml_content, stories_file)

        return "Stories English File generated!"
    else:
        return "Invalid file format. Only YAML files are allowed."



@app.route('/generate_stories_hindi', methods=['POST'])
def generate_stories_route_hindi():
    if 'storiesFile' not in request.files:
        return "No file part"

    stories_file = request.files['storiesFile']

    if stories_file.filename == '':
        return "No selected file"

    if stories_file:
        yml_file_name = os.path.splitext(stories_file.filename)[0]

        # Save the uploaded YAML file to a temporary location
        yml_file_path = 'temp.yml'
        stories_file.save(yml_file_path)

        # Generate stories YAML content from the uploaded YAML file
        stories_yml_content = generate_stories_yml_from_yml_hindi(yml_file_path)
        stories_filename = f"{yml_file_name}_stories_hindi.yml"

        # Save the generated stories YAML content to a file
        with open(stories_filename, "w") as stories_file:
            yaml.dump(stories_yml_content, stories_file)

        return "Stories Hindi File generated!"
    else:
        return "Invalid file format. Only YAML files are allowed."

@app.route('/generate_stories_urdu', methods=['POST'])
def generate_stories_route_urdu():
    if 'storiesFile' not in request.files:
        return "No file part"

    stories_file = request.files['storiesFile']

    if stories_file.filename == '':
        return "No selected file"

    if stories_file:
        yml_file_name = os.path.splitext(stories_file.filename)[0]

        # Save the uploaded YAML file to a temporary location
        yml_file_path = 'temp.yml'
        stories_file.save(yml_file_path)

        # Generate stories YAML content from the uploaded YAML file
        stories_yml_content = generate_stories_yml_from_yml_urdu(yml_file_path)
        stories_filename = f"{yml_file_name}_stories_urdu.yml"

        # Save the generated stories YAML content to a file
        with open(stories_filename, "w") as stories_file:
            yaml.dump(stories_yml_content, stories_file)

        return "Stories Urdu File generated!"
    else:
        return "Invalid file format. Only YAML files are allowed."



@app.route('/add_training_latest', methods=['POST'])
def add_training_latest():
    try:
        intent = request.form.get('intent')
        examples = request.form.getlist('example[]')
        response_heading = request.form.get('response_heading')
        response_text = request.form.get('response_text')

        # Update nlu.yml
        nlu_path = os.path.join('test_data', 'nlu.yml')
        with open(nlu_path, 'a') as nlu_file:
            nlu_file.write(f'\n- intent: {intent}\n  examples:\n')
            for example in examples:
                nlu_file.write(f'    - {example}\n')

        # Update domain.yml
        domain_path = os.path.join('test_data', 'domain.yml')
        with open(domain_path, 'a') as domain_file:
            domain_file.write(f'\nresponses:\n  utter_{response_heading}_response:\n    - text: "{response_text}"')

        # Update stories.yml
        stories_path = os.path.join('test_data', 'stories.yml')
        with open(stories_path, 'a') as stories_file:
            stories_file.write(f'\n- story: {intent}_story\n  steps:\n    - intent: {intent}\n      user: |-\n')
            for example in examples:
                stories_file.write(f'        {example}\n')

        # Return success message
        return "Training data and intent data added successfully!"
    except Exception as e:
        return f"An error occurred: {e}"


@app.route('/add_training', methods=['POST'])
def add_training():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        intent = request.form.get('intent')
        examples = request.form.getlist('example[]')
        response_heading = request.form.get('response_heading')
        response_text = request.form.get('response_text')

        # Insert training data into the database
        insert_query = "INSERT INTO training_data (intent, response) VALUES (%s, %s)"
        cursor.execute(insert_query, (intent, response_text))
        connection.commit()

        # Update nlu.yml and domain.yml
        nlu_path = 'data/nlu.yml'
        domain_path = 'domain.yml'
        stories = 'data/stories.yml'

        with open(nlu_path, 'a') as nlu_file:
            nlu_file.write(f'\n- intent: {intent}\n  examples:\n    - {examples[0]}\n    - {examples[1]}\n    - {examples[2]}')

        with open(domain_path, 'a') as domain_file:
            domain_file.write(f'\nresponses:\n  utter_{response_heading}_response:\n    - text: "{response_text}"')


        cursor.close()
        connection.close()

        return "Training data and intent data added successfully!"
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/submit_intent', methods=['POST'])
def submit_intent_data():
    intent_heading = request.form.get('intent_heading')
    examples = request.form.getlist('example')
    response_heading = request.form.get('response_heading')
    response_text = request.form.get('response_text')

    # Update nlu.yml and domain.yml
    nlu_path = 'data/nlu.yml'
    domain_path = 'domain.yml'

    with open(nlu_path, 'a') as nlu_file:
        nlu_file.write(f'\n- intent: {intent_heading}\n  examples:\n    - {examples[0]}\n    - {examples[1]}\n    - {examples[2]}')

    with open(domain_path, 'a') as domain_file:
        domain_file.write(f'\nresponses:\n  utter_{response_heading}_response:\n    - text: "{response_text}"')

    # Train the model
    # subprocess.run(['rasa', 'train'])

    return "Intent data submitted successfully!"


# @app.route('/submit_intent', methods=['POST'])
# def submit_intent():
#     intent_heading = request.form.get('intent_heading')
#     examples = request.form.get('examples')
#     responses = request.form.get('responses')

#     # Update nlu.yml and domain.yml
#     nlu_path = 'path_to_your_nlu.yml'
#     domain_path = 'path_to_your_domain.yml'

#     with open(nlu_path, 'a') as nlu_file:
#         nlu_file.write(f'\n- intent: {intent_heading}\n  examples: |\n    - {examples}')

#     with open(domain_path, 'a') as domain_file:
#         domain_file.write(f'\nresponses:\n  utter_{intent_heading}_response:\n    - text: "{responses}"')

#     # Train the model
#     # subprocess.run(['rasa', 'train'])

#     return "Intent data submitted successfully!"

# @app.route('/submit_training_chatbot_form', methods=['POST'])
# def submit_intent():
#     intent_heading = request.form.get('intent_heading')
#     examples = request.form.get('examples')
#     responses = request.form.get('responses')

#     # Update nlu.yml and domain.yml
#     nlu_path = 'path_to_your_nlu.yml'
#     domain_path = 'path_to_your_domain.yml'

#     with open(nlu_path, 'a') as nlu_file:
#         nlu_file.write(f'\n- intent: {intent_heading}\n  examples: |\n    - {examples}')

#     with open(domain_path, 'a') as domain_file:
#         domain_file.write(f'\nresponses:\n  utter_{intent_heading}_response:\n    - text: "{responses}"')

#     # Train the model
#     # subprocess.run(['rasa', 'train'])

#     return "Intent data submitted successfully!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=59410)

