FROM python:3

WORKDIR /opt/backend
COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000 5000
CMD ["python", "routes.py"]
