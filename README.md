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
touch engine/src/api/application.cfg
```
Enter the below 2 lines in *application.cfg* file (donot forget to modify the SECRET_KEY value :P)
```
SECRET_KEY   = "some secret key[edit]"
MONGO_DBNAME = "skadooshCoreDb"
```

### Running the engine api ###
```
chmod +x run.sh
./run.sh
```
Let this terminal and open a new terminal tab/session
navigate to repo directory and do a `workon skadoosh`

Note: Whenever you want to run the app in new terminal tab/session
you need to execute once `workon skadoosh`

*Integration Tests*
```
chmod +x tests.sh
./tests.sh
```

### Sample interactions ###
```
curl "http://localhost:4000/api/help" -d text="what's my account balance?"
```

### Training Model ###

Soon...