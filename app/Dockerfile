FROM python:3.11

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    python3-dev \
    build-essential \
    libssl-dev \
    libc6-dev

WORKDIR /usr/src/app

COPY . .


RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 80
EXPOSE 3306

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]
