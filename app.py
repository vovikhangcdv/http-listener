import flask, json, time, os
from flask import request, jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False
LOG_FILE_NAME = "log.txt"
MAX_LOG_FILE_SIZE = 5 * 1024 * 1024

@app.route('/', methods=['GET', 'POST'])
def home():
    data = {}
    request_data = {}
    request_data.update(request.form)
    request_data.update(request.args)
    try:
        if os.path.getsize(LOG_FILE_NAME) > MAX_LOG_FILE_SIZE:
            os.remove(LOG_FILE_NAME)
        with open(LOG_FILE_NAME, "r") as file_log:
            data = json.load(file_log)
    except:
        data = {}
    if request_data:
        new_data = {}
        current_time = time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())
        for key, value in request_data.items():
            new_data[key] = value
        sorted_data = {current_time: new_data}
        sorted_data.update(data)
        data = sorted_data
        with open(LOG_FILE_NAME, 'w') as outfile:
            json.dump(data, outfile)
    return jsonify(data)

@app.route('/delete')
def delete_log():
    return jsonify({"success": os.remove(LOG_FILE_NAME)})
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)