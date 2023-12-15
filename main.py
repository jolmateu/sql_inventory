from inventory import Inventory

""" Display options menu """
def menu():
    print("\nWelcome to the Inventory System")
    print("1. Add Item")
    print("2. Delete Item")
    print("3. Sell Item")
    print("4. Show inventory")
    print("5. Exit")
    return input("Select an option: ")

if __name__ == "__main__":

    """ Create an Inventory instance """
    inventory = Inventory()
    inventory.create_tables()

    """ Loop for options menu """
    while True:
        option = menu()

        if option == "1":
            name = input("Enter the name of the item: ")
            price = float(input("Enter the price: "))
            inventory.add_article(name, price)

        elif option == "2":
            item_id = input("Enter the ID of the item to delete: ")
            inventory.del_article(item_id)

        elif option == "3":
            item_id = int(input("Enter the ID of the item: "))
            sell_quantity = int(input("Enter the quantity to sell: "))
            inventory.sale_item(item_id, sell_quantity)

        elif option == "4":
            inventory.shw_inventory()

        elif option == "5":
            inventory.close_conn()
            break

        else:
            print("Invalid option. Please select a valid option.")
