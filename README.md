# Projet_E5
Projet E5 de la certification simplon

### Install vips on linux
```sh 
sudo apt install libvips-dev --no-install-recommends
```

### Create environnement
```sh
python -m venv env && . env/bin/activate
```
```sh
pip install -r requirements.txt
```

### Launch flask server (en mode debug)
```sh
python app.py
```

### Launch monitor program (start on a different terminal window)
```sh
python monitor.py
```

### Launch benchmark
```sh
python benchmark.py
```

### Launch memory profiler
```sh
mprof run benchmark.py && mrpof plot 
```
