FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y vim procps tesseract-ocr tesseract-ocr-kor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN echo "alias ls='ls --color=auto'" >> ~/.bashrc
RUN echo "alias l='ls -al'" >> ~/.bashrc
RUN echo "alias l='ls -l'" >> ~/.bashrc

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "kakaotalkchannel.py"]