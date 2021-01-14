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
  

Requirements:
 - python 3.7.9

Make local.py file
How to setup:

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
python manage.py createsuperuser


pip install -U "celery[redis]"

```

# Run worker for training task:
```
python manage.py runserver 0.0.0.0:8000
EasyIntentCatcher/ic_dataset$ celery -A tasks worker --loglevel=INFO

```

# Useful commands for work with IntentCatcher
TODO update with DeepPavlov
```
python ic_dataset/from_db_2_icjson.py
python data/create_data_and_train_model.py --intent_phrases_path data/intent_phrases_export.json
python data/create_data_and_train_model.py --intent_phrases_path data/intent_phrases_export.json --model_path data/models/my_model
```

# TODO: write system reqiurements.
- RAM requiements
- Video Memory Requirements
 (for base config) 