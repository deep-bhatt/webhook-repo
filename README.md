# Deep Bhatt

# Task - @TechStax


## 💻 How to run
<sup>*Python  v3.8.10*</sup>

* Create a pyenv envirnoment

```bash
pyenv virtualenv 3.8.10 webhook-repo # version hopefully verions 3.6+ should also work!
```

* `cd` into the webhook-repo

```bash
cd ./webhook-repo
```

* Activate the virtual env

```bash
pyenv local webhook-repo
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application

```bash
python run.py
```

* The endpoint for webhook receiver is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

* The endpoint for UI is at:

```bash
GET http://127.0.0.1:5000/webhook/display
```

## 🖼️ Example screenshot of the super minimalistic UI
![UI_SS](https://i.imgur.com/7PbJMXb.png)