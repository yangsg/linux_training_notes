

https://docs.python.org/3/tutorial/venv.html


python3 -m venv tutorial-env
source tutorial-env/bin/activate



pip search astronomy
pip install novas
pip install --upgrade pip
pip install requests==2.6.0
pip install --upgrade requests
pip show requests
pip uninstall requests
pip list           # pip list will display all of the packages installed in the virtual environment:

pip freeze will produce a similar list of the installed packages, but the output uses the format that pip
install expects. A common convention is to put this list in a requirements.txt file:

pip freeze > requirements.txt
pip install -r requirements.txt

pip –help

https://www.python.org/
https://docs.python.org/3/
https://pypi.org/
https://code.activestate.com/recipes/langs/python/
http://www.pyvideo.org
https://scipy.org/





















