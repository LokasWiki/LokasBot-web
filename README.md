LokasBot website
==========

Deploy on Toolforge
-------------------
Your tool will need a service account with rights to query across namespaces.

-   ```
    $ ssh dev.toolforge.org
    $ become $TOOL_NAME
    ```
-   ```
    webservice --backend=kubernetes python3.9 stop
    rm -fdr $HOME/www/python/src
    mkdir -p $HOME/www/python
    git clone https://github.com/loka1/LokasBot-web.git $HOME/www/python/src
    webservice --backend=kubernetes python3.9 shell
    python3 -m venv $HOME/www/python/venv
    source $HOME/www/python/venv/bin/activate
    pip install --upgrade pip wheel
    python3 -m pip install -U pip setuptools wheel
    python -m pip install requests
    python -m pip install pyyaml
    pip install -r $HOME/www/python/src/requirements.txt
    exit
    ```
    
-   ```
    webservice --backend=kubernetes python3.9 start
    ```
    
