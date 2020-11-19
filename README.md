# EasyIntentCatcher
Administrative tool for managing datasets of IntentCacther

# Feataures:
- IntentCatcher dataset management: view, edit, create new training samples from WEB UI
- Automatically prepares model for updated dataset

TODO add screenshots:
  - intents list intent details
  - predictions log
  - prediction api
  

# Run worker for training task:
```
python manage.py runserver 0.0.0.0:8000
EasyIntentCatcher/ic_dataset$ celery -A tasks worker --loglevel=INFO

```

How to setup:

```

pip install -U "celery[redis]"
pip install -r requirements.txt
python manage.py runserver 0.0.0.0:8000

```

# Useful commands
```
python ic_dataset/from_db_2_icjson.py
python data/create_data_and_train_model.py --intent_phrases_path data/intent_phrases_export.json
```

# TODO: write system reqiurements.
- RAM requiements
- Video Memory Requirements
 (for base config) 