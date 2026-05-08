FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["pytest", "-n", "2", "--alluredir=allure-results", "--html=report.html", "--self-contained-html"]