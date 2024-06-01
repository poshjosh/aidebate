FROM python:3.9.5

WORKDIR /aidebate

COPY . .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "main.py" ]
