from flask import Flask, render template
app = Flask(__name__)

#define rout for HTML page 
@app.route("/")
def index():
    return render_template("index.html")

#route to run motor script 
@app.route("/run_motor_script")

return "Motor script activated"

if __name__ == "__main__":
    app.run(debug=True)