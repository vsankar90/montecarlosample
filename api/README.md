# Montecarlo Supporting REST API for web

### run

```
pip3 install -r requirements.txt
gunicorn api:app.py


```
### systemd service in linux

```
[Unit]
Description=CDP Montecarlo API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/cdp-montecarlo/api
ExecStart=/home/ubuntu/.local/bin/gunicorn  api:app
Restart=always

[Install]
WantedBy=multi-user.target
```


### API Endpoints


#### Start tests
```
curl --location --request POST 'http://localhost:8000/testcase/start' --header 'Content-Type: application/json' --data-raw '{"testName" : "test-case-4", "nThreads" : "32", "nOptions" : "128k", "pathLength" : "32k", "testBlockLength" : "1k"}'
```
#### List Tests
```
curl --location --request GET 'http://localhost:8000/testcase/list'
```

