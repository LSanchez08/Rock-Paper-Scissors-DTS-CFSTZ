# Rock-Paper-Scissors-DTS-CFSTZ

First time run:
1. Make sure to be on powershell or cmd as administrator(For windows).
2. On root folder execute the following commands:
  - pip install virtualenv
  - Add to path
  - Restart the computer
  - virtualenv venv
  - venv\Scripts\activate
  - pip install -r requirements.txt
3. Substitute the file venv/Lib/site-packages/keras_squeezenet/squeezenet.py for substitute/squeezenet.py

Capture mode:
- python src\gather_images.py ${rock, paper, scissors or none} ${number of captures}
- Press "o" to start capture.
- Press "q" to exit.

Trainning mode:
- python src\train.py

Game:
- python src\play.py
- Press "q" to exit.

