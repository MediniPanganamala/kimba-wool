import sqlite3

# Open a connection to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Insert sample data into the products table
cursor.execute("INSERT INTO products (product_name, price, image_url) VALUES (?, ?, ?)", ('shirt',699, '/static/images/product-4.jpg'))
cursor.execute("INSERT INTO products (product_name, price, image_url) VALUES (?, ?, ?)", ('innerwares',1100, '/static/images/new5.jpg'))
cursor.execute("INSERT INTO products (product_name, price, image_url) VALUES (?, ?, ?)", ('kids',2800, '/static/images/new3.jpg'))
cursor.execute("INSERT INTO products (product_name, price, image_url) VALUES (?, ?, ?)", ('womenpants',3500, '/static/images/new4.jpg'))
cursor.execute("INSERT INTO products (product_name, price, image_url) VALUES (?, ?, ?)", ('tops',350, '/static/images/new2.jpg'))

# Add more products as needed
print("inserted")
# Commit the changes and close the connection
conn.commit()
conn.close()

#add info:
# 1	tshirt	699.0	/static/images/ts.jpg
# 2	handbags	1100.0	/static/images/product-2.jpg
# 3	coat	2800.0	/static/images/p1.jpg
# 4	watch	3500.0	/static/images/wa.jpg
# 5	pants	350.0	/static/images/product-8.jpg
# 6	shirts	599.0	/static/images/product-7.jpg
# 7	comboshirt	1500.0	/static/images/product-6.jpg
# 8	jacket	7000.0	/static/images/p2.jpg
# 9	combopack	1200.0	/static/images/a1.jpg
# 10	coats	699.0	/static/images/new1.jpg
# 11	innerwares	1100.0	/static/images/new5.jpg
# 12	kids	2800.0	/static/images/new3.jpg
# 13	womenpants	3500.0	/static/images/new4.jpg
# 14	tops	350.0	/static/images/new2.jpg