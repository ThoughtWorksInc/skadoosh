#Overview

Core engine component which does the following

* Analysis the user input
* Run through the ML algorithm

* Return the response

* Basic trainer model
* Training data set
* Test data set

* Memorize the outputs
* continuous and supervised learning via manual training on engine management process

* Simple REST API endpoint

### Requirements ###
* Python 3.5
* pip
* virtualenvwrapper (optional)
* mongodb

### Setup ###
```
git clone https://cackharot@bitbucket.org/twbhackathon/skadoosh.git
cd skadoosh
[[ -n $VIRTUAL_ENV ]] && mkvirtualenv skadoosh -p `which python3.5`
[[ -z $VIRTUAL_ENV ]] && workon skadoosh
pip install -r engine/src/requirements.txt
python -m nltk.downloader all
```

### Running the engine api ###
```
chmod +x run_api.sh
./run_api.sh
```

### Sample interactions ###
```
curl "http://localhost:4000/api/help/What's my account balance?"
```

### Training Model ###

Soon...