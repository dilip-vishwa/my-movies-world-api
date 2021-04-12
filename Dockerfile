FROM python:3.8
RUN mkdir -p /app
ADD requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
ADD . /app
CMD ["python", "app.py"]
