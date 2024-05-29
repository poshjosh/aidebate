FROM python:3.9.5

WORKDIR /aidebate

COPY requirements.txt ./

RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Even though module `pyu` is in requirments.txt, we got ->
# ModuleNotFoundError: No module named 'pyu'
# We solved the above error by installing the module separately here
RUN python3 -m pip install "pyu @ git+https://github.com/poshjosh/pyu@v0.1.2"

COPY . .

CMD [ "python3", "main.py" ]
