from flask import Flask

app=Flask (__name__)
@app.route("/")
def home ():
    return """
    <h1>My supply Chain Project</h1>
    <p>Welcome to our Inventory monitoring system!</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
