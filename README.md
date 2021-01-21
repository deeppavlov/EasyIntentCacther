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

# Screenshots
List of intents:
![210121_easyintentcatcher_intents_list](https://user-images.githubusercontent.com/2207706/105342371-55395a00-5bf1-11eb-83b8-5d2662453999.png)

Intent editing: 
![210122_easyintentcatcher_intents_edit](https://user-images.githubusercontent.com/2207706/105342390-5c606800-5bf1-11eb-8e7b-2707041d381c.png)

History of predictions:
![210123_easyintentcatcher_prediction_cases_log](https://user-images.githubusercontent.com/2207706/105342407-608c8580-5bf1-11eb-9b11-881b57d9199a.png)

History of trained models:
![210124_easyintentcatcher_trained_model](https://user-images.githubusercontent.com/2207706/105342426-65e9d000-5bf1-11eb-8ee9-eb9964e7be72.png)

Prediction API:
![210125_easyintentcatcher_prediction_API](https://user-images.githubusercontent.com/2207706/105342443-6a15ed80-5bf1-11eb-937f-097a1c997f69.png)

API Response example:
![210126_easyintentcatcher_prediction_API_response_example](https://user-images.githubusercontent.com/2207706/105342461-70a46500-5bf1-11eb-9c4b-1867671efacb.png)
