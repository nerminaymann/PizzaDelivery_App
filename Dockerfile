FROM python:3.12.4-slim-bullseye
WORKDIR /PizzaDelivery_App
COPY ./PizzaDelivery_App ./

RUN pip install --upgrade pip --no-cache-dir

RUN pip install -r /PizzaDelivery_App/requirements.txt --no-cache-dir

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]



