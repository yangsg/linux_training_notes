#// https://docs.python.org/3.6/tutorial/stdlib.html

import os

cwd = os.getcwd()      # Return the current working directory
print(cwd)
os.chdir('/tmp')   # Change current working directory
os.system('mkdir today')   # Run the command mkdir in the system shell


