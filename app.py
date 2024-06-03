
from flask import Flask, request, render_template,jsonify
from flask import Flask, request, render_template_string

from matching_and_ranking import Matching_and_ranking    
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def upload_csv():
    result=None
    if request.method == 'POST':
        file = request.files['file']
        query = request.form['query']
        if file and file.filename.endswith('.csv'):
            result=Matching_and_ranking(query,file)
            return jsonify({'result':result})
        else:
            return jsonify({'error':'missing'}),400
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <title>Search engine</title>
        </head>
        <body>
          <h1>searsh engin</h1>
          <form method="post" action="/" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="text" name="query" placeholder="enter text for search" required>
            <input type="submit" value="search">
          </form>
          {% if result is not none %}
          <h2>النتيجة: {{ result }}</h2>
          {% endif %}
        </body>
        </html>
    ''', result=result)
if __name__ == '__main__':
    app.run()