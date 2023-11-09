# CONNECTED
## TO RUN:

``Install Python on your computer``
## RUN: 
`pip install -r requirements.txt`

## COPY 
``CONTENT OF .env.example to .env``

## CHANGE ONLY THE FOLLOWIG FIELDS WITH YOURS:
``DATABASE_URI=changing this is optional``

``OPENAI_API_KEY``

``VECTARA_CUSTOMER_ID``

``VECTARA_API_KEY``

## RUN: 
`export FLASK_APP=main.py OR set FLASK_APP=main.py`
## RUN MIGRATION: 
`flask db upgrade`
## RUN: 
`flask run`