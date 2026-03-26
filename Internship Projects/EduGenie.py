from boltiotai import openai
import os
from flask import Flask, render_template_string, request

openai.api_key = os.environ['OPENAI_API_KEY']

def generate_tutorial(topic):

 response = openai.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[{
   "role": "system",
   "content": "You are a helpful assistant"
  }, {
   "role":
   "user",
   "content":
   f"Generate educational content, including a course objective,sample syllabus,three learning outcomes,assesment methods, and recommended readings based on the available topic.Make sure every section should listed with bullwt points.Add a motivational quote at the end.Here is the  available topic: {topic}"
  }])
 return response['choices'][0]['message']['content']

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def hello():
 output = ""
 if request.method == 'POST':
  topic= request.form['topic']
  output = generate_tutorial(topic)
# This is a HTML template for a Custom  educational content Generator web page. It includes a form for users to input a topic they have, and two JavaScript functions for generating a content based on the input and copying the output to the clipboard. The template uses the Bootstrap CSS framework for styling.
 return render_template_string('''

<!DOCTYPE html>
<html>
  <head>
    <title>AI Content Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-LN+7fdVzj6u52u30Kp6M/trliBMCMKTyK833zpbD+pXdCLuTusPj697FH4R/5mcr" crossorigin="anonymous">
    <script>
      async function generateTutorial() {
        const topic = document.querySelector("#topic").value;
        const output = document.querySelector("#output");
        output.textContent = "Generating an educational content for you...";
        const response = await fetch("/generate", {
          method: "POST",
          body: new FormData(document.querySelector("#tutorial-form")),
        });
        const newOutput = await response.text();
        output.textContent = newOutput;
      }
      function copyToClipboard() {
        const output = document.querySelector("#output");
        const textarea = document.createElement("textarea");
        textarea.value = output.textContent;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
        alert("Text copied to clipboard");
      }
    </script>
  </head>

  <body>
    <div class="container">
      <p class="name" style="color: blue;font-size: 50px;font-weight: bold;font-family:  Arial, sans-serif;">EduGenie: AI-Powered<br>
       Educational Content Creator</p>
      <form
        id="tutorial-form"
        onsubmit="event.preventDefault(); generateTutorial();"
        class="mb-3"
      >
        <div class="mb-3">
          <label for="topic" class="form-label"
            ><b>Course Title: </b></label
          >
          <input
            type="text"
            class="form-control"
            id="topic"
            name="topic"
            placeholder="Enter the topic "
            required
            />
        </div>
        <button type="submit" class="btn btn-primary" style="background-color:black;color:white;border:1px solid grey;margin-bottom:20px;">
          Generate Content
        </button>
        <p>Generating content, please wait...</p>
      </form>
      <div class="card">
        <div style="background-color:blue;color:white;"
          class="card-header d-flex justify-content-between align-items-center"
        >
          <b>Output:</b>
          <button class="btn btn-secondary btn-sm" onclick="copyToClipboard()">
            Copy
          </button>
        </div>
        <div class="card-body">
          <pre id="output" class="mb-0" style="white-space: pre-wrap">
{{ output }}</pre
          >
        </div>
      </div>
    </div>
  </body>
</html>

''',
                output=output)

@app.route('/generate', methods=['POST'])

def generate():
 topic = request.form['topic']
 return generate_tutorial(topic)

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=8080)
