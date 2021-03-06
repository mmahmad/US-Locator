The Flask application is based on Python 3.7 and MySQL 5.5.61, but is running on a Python 3.6 AWS EBS environment.

<h3> Prerequisites </h3>

1) Set up Python3.7, and add it to your PATH variable. Running `python3` in the terminal/cmd should open the Python 3.7 interpreter.
2) Install `pip`
3) Install virtualenv `pip3 install virtualenv` 

<h3> Development Setup </h3>

1) Clone the repo, and cd into the root of the project
2) Load virtual environment `source virt/bin/activate`
3) run `pip3 install -r requirements.txt`
4) running `python3 application.py` should start a local server, with the project's localhost URL:port printed on the terminal

Do <b>NOT</b> change the file name of `application.py`, nor the variable `application` inside it. EBS relies on that to run properly. Other than that, feel free to modify.