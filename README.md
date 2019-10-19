# Heroku-Flask-ExternalMonitoring

---

## Flask用.gitignoreの準備

* [.gitignore](https://raw.githubusercontent.com/pallets/flask/master/.gitignore) をダウンロードして、ルートディレクトリに置く。

## 仮想環境の準備

```ps
$ py -m venv emenv
```

.gitignoreに仮想環境名を追記

```gitignore
emenv

(後略)
```

```ps
$ emenv/Scripts/activate
(emenv)$ pip install flask flask_sqlalchemy psycopg2
(emenv)$ pip freeze > requirements.txt
```

---

Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.
