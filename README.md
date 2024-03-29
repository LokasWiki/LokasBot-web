LokasBot website
==========

Deploy on Toolforge
-------------------

-   ```
    webservice --backend=kubernetes python3.9 stop
    ```
    
-   ```    
    rm -fdr $HOME/www/python/src
    mkdir -p $HOME/www/python
    git clone https://github.com/loka1/LokasBot-web.git $HOME/www/python/src
    ```
    
-   ```
    webservice --backend=kubernetes python3.9 shell
    ```
    
-   ```
    python3 -m venv $HOME/www/python/venv
    source $HOME/www/python/venv/bin/activate
    ```
    
-   ```
    pip install --upgrade pip wheel
    python3 -m pip install -U pip setuptools wheel
    python -m pip install requests
    python -m pip install pyyaml
    ```
    
-   ```
    pip install -r $HOME/www/python/src/requirements.txt
    ```
    
-   ```
    exit
    ```
    
-   ```
    webservice --backend=kubernetes python3.9 start
    ```
    

Run locally
-----------
-  ```
    cd {to the project folder}
    chmod +x run_local.sh
    ./run_local.sh
   # run init-db command before first run
   {from the project folder}.venv/bin/python -m flask init-db
   
    ```