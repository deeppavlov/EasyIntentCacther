# EasyIntentCatcher
Administrative tool for managing datasets of IntentCacther

# Features:
- IntentCatcher dataset management: view, edit, create new training samples from WEB UI
- Train IntentCacther models from UI
- Test and Analyze predictions of the trained model
- Export trained models to remote SSH Server 
- Automatically prepares model for updated dataset

TODO add screenshots:
  - intents list intent details
  - predictions log
  - prediction api
  

# Requirements:
Assure your server fit following requirements:
 - python 3.7.9
   - conda -N new_env python=3.7
 - redis-server
   -   sudo apt-get install redis-server

# Set Up
How to setup:

```
git clone https://github.com/deepmipt/EasyIntentCacther
cd EasyIntentCacther
pip install -r requirements.txt
python manage.py migrate
```
Now you need to launch worker for training tasks and web server for managing dataset and training system.

# Run worker for training task execution:
```
celery  -A EasyIntentCatcher worker -l INFO
```


# Run server for web-administration tool
```
python manage.py runserver 0.0.0.0:8000
```

Now you can browse your intents, train a model, export to SSH server and use it for predictions!

# Useful commands for work with IntentCatcher on lowel level interface

Generate IntentCather JSON dataset specification from Database contents:
```
python ic_dataset/from_db_2_icjson.py
```

Train model from IntentCather JSON dataset specification with specification of target path for model:
```
python data/create_data_and_train_model.py --intent_phrases_path data/intent_phrases_export.json --model_path data/models/my_model
```
