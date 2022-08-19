ThriftSHop Nepal

# Setup

1. Create virtual Environment
   
    ```bash 
    python3.7 -m venv env
    ```

2. Activate `venv`

   ```bash 
   source env/bin/activate
   ```

3. install python dependencies

 ```bash 
 pip install -r requirements.txt
 ```

4. Run app

```bash 
flask run
```

# Setup using docker

1. `docker-compose build`
2. `docker-compose up`

# Populate data to db 

1. Populate User `python3 utils/populate_user.py`
2. Populate Goods or Products `python3 utils/populate_product.py`

