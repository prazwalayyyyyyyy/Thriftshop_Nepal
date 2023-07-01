rm app.db
rm -r migrations
flask db init
flask db migrate
flask db upgrade

python utils/populate_user.py

python utils/populate_product.py

