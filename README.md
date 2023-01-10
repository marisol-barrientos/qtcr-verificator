# QTCR Verificator


It is recommended using Python version 3.10.

Please, execute the following commands to create a virtual environment and get the requirements installed.

```
python3.10 -m venv env
source env/bin/activate
```

```
pip3 install -r /path/to/requirements.txt
```


For tagging temporal constraints it is used a [wrapped version](https://github.services.devops.takamol.support/PhilipEHausner/python_heideltime "wrapped version") of [Heideltime](https://github.com/HeidelTime/heideltime "Heideltime"). The next commands sum up its installation, please, execute them inside: ['src/heideltime/heideltime-standalone'](src/heideltime/heideltime-standalone).

```
chmod +x install_heideltime_standalone.sh
./install_heideltime_standalone.sh
```

```
python3 -m pip install .
```

More information about how to install it can be found in the [README file](/src/heideltime/README.md) of the 
Python Wrapper.

After having installed the [Heideltime Wrapper](https://github.services.devops.takamol.support/PhilipEHausner/python_heideltime "Heideltime Wrapper"), the file present here: ['src/heideltime/heideltime-standalone/heideltime-standalone/de.unihd.dbs.heideltime.standalone.jar'](src/heideltime/heideltime-standalone/heideltime-standalone/de.unihd.dbs.heideltime.standalone.jar) must be replaced with ['tmp/de.unihd.dbs.heideltime.standalone.jar'](tmp/de.unihd.dbs.heideltime.standalone.jar)




TODO: Get from compress folder
TODO: Add info about tests



