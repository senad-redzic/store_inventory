from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv
from datetime import datetime

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True)
    product_name = Column('Name', String)
    product_quantity = Column('Quantity', Integer)
    product_price = Column('Price', Integer)
    date_updated = Column('Date', Date)


def add_to_database(products):
      for product in products:
          new_product = Product(
              product_name=product['product_name'],
              product_quantity=product['product_quantity'],
              product_price=product['product_price'],
              date_updated=product['date_updated']
          )
          session.add(new_product)
      session.commit()

def display_menu():
    while True:
        print("\nSTORE INVENTORY:")
        print("\nMenu options:")
        print("v: Display product")
        print("a: Add product")
        print("b: Make backup")
        print("q: Exit")
        menu_option = input("Enter the choice: ").lower()

        if menu_option == 'v':
            display_product()
        elif menu_option == 'a':
            add_new_product()
        elif menu_option == 'b':
            make_backup()
        elif menu_option == 'q':
            print("Bye.")
            break
        else:
            print("Allowed options are v,a,b or q.")

def display_product():
    product_id = int(input("What is the product ID?: "))
    product = session.query(Product).filter(Product.product_id == product_id).first()
    if product:
      print(f"\n\nID: {product.product_id}")
      print(f"Product Name: {product.product_name}")
    else:
        print("\n\nProduct with this ID does not exist.")

def add_new_product():
    product_name = input("What is the product name?: ").strip()
    product_quantity = int(input("What is the product quantity?: "))
    product_price = int(float(input("What is the product price?: ")))

    add_product = Product(
        product_name=product_name,
        product_quantity=product_quantity,
        product_price=product_price,
    )
    session.add(add_product)
    session.commit()
    print("\n\nProduct added.")

def make_backup():
    with open('backup.csv', 'w', newline='') as file:
        fields = ['product_id', 'product_name', 'product_quantity', 'product_price', 'date_updated']
        writer = csv.DictWriter(file, fieldnames=fields)

        writer.writeheader()
        products = session.query(Product).all()
        for product in products:
            writer.writerow({
                'product_id': product.product_id,
                'product_name': product.product_name,
                'product_quantity': product.product_quantity,
                'product_price': product.product_price,
                'date_updated': product.date_updated
            })

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    products = []

    with open('inventory.csv', 'r') as file:
        reader = csv.DictReader(file)
        products = []
        for row in reader:
          product_name = row['product_name'].strip()
          product_quantity = int(row['product_quantity'])
          product_price = int(float(row['product_price'].replace('$', '').replace(',', '')))
          date_updated = datetime.strptime(row['date_updated'], '%m/%d/%Y').date()

          product_dictionary = {
              'product_name': product_name,
              'product_quantity': product_quantity,
              'product_price': product_price,
              'date_updated': date_updated
          }

          products.append(product_dictionary)

    add_to_database(products)
    display_menu()

