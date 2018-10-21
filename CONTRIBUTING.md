The Flask application is based on Python 3.7 and MySQL 5.5.61, but is running on a Python 3.6 AWS EBS environment.

1) Set up Python3.7
2) Clone the repo, and cd into the root of the project
3) Load virtual environment `source virt/bin/activate`
4) run `pip install -r requirements.txt`

Do <b>NOT</b> change the file name of `application.py`, nor the variable `application` inside it. EBS relies on that to run properly. Other than that, feel free to modify.