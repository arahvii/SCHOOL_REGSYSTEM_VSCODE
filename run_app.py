import sys
import os
from schoolreg_guiproject import create_app

# This block helps the VS Code linter and Python resolve the 'schoolreg_guiproject' package 
# when run from the root directory.
# It ensures that 'from schoolreg_guiproject import create_app' works correctly.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = create_app()

if __name__ == '__main__':
    # Running the application.
    app.run(debug=True)
