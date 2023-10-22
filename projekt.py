import csv
import pandas as pd
import matplotlib.pyplot as plt

def load_data(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def validate_email(email):
    while "@" not in email or "." not in email:
        print("Invalid email address. Please include '@' and '.' in the email address.")
        email = input("Enter the corrected email address: ")
    return email

def validate_phone(phone):
    while not phone.startswith("+") or len(phone) != 13 or not phone[1:].isdigit():
        print("Phone number must start with '+' and contain 12 digits (e.g., +421123456789).")
        phone = input("Enter the corrected phone number: ")
    return phone

def validate_person_id(person_id, existing_ids):
    while len(person_id) != 7 or not person_id[:2].isalpha() or not person_id[2:].isdigit() or person_id in existing_ids:
        if person_id in existing_ids:
            print("Person ID already exists. Please enter a unique Person ID.")
        else:
            print("Person ID must start with 2 letters followed by 5 numbers (e.g., AB12345).")
        person_id = input("Enter the corrected Person ID: ")
    return person_id

def check_for_duplicates(data, new_data):
    existing_ids = set()
    existing_emails = set()
    existing_phones = set()

    for record in data:
        existing_ids.add(record['Person ID'])
        existing_emails.add(record['Person Mail Address'])
        existing_phones.add(record['Telephone Number'])

    while new_data['Person ID'] in existing_ids or new_data['Person Mail Address'] in existing_emails or new_data['Telephone Number'] in existing_phones:
        print("Duplicate ID, email, or phone number found. Please enter unique information.")
        new_data['Person ID'] = validate_person_id(input("Enter the corrected Person ID: "), existing_ids)
        new_data['Person Mail Address'] = validate_email(input("Enter the corrected email address: "))
        new_data['Telephone Number'] = validate_phone(input("Enter the corrected phone number: "))

def insert_record(data):
    name = input("Enter the customer's Name: ")
    surname = input("Enter the customer's Surname: ")
    email = validate_email(input("Enter the customer's Person Mail Address: "))
    phone = validate_phone(input("Enter the customer's Telephone Number (e.g., +421123456789): "))
    person_id = validate_person_id(input("Enter the customer's Person ID (e.g., AB12345): "), {record['Person ID'] for record in data})
    
    gender = input("Enter the customer's Gender (M for Man, W for Woman): ")
    while gender not in ['M', 'W']:
        print("Invalid input. Please enter 'M' for Man or 'W' for Woman.")
        gender = input("Enter the corrected Gender (M for Man, W for Woman): ")
    
    new_record = {'Name Surname': f"{name} {surname}", 'Person ID': person_id, 'Person Mail Address': email, 'Telephone Number': phone, 'Gender': gender}
    check_for_duplicates(data, new_record)
    data.append(new_record)
    return data

def save_data(filename, data):
    with open(filename, 'w', newline='') as file:
        fieldnames = ['Name Surname', 'Person ID', 'Person Mail Address', 'Telephone Number', 'Gender']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def display_customer_data(data):
    print("\nCustomer Data:")
    for record in data:
        print(f"Name: {record['Name Surname']}")
        print(f"Person ID: {record['Person ID']}")
        print(f"Email Address: {record['Person Mail Address']}")
        print(f"Phone Number: {record['Telephone Number']}")
        print(f"Gender: {record['Gender']}")
        print("-" * 30)

def search_customer(data):
    query = input("Enter a name, surname, ID, or phone number to search: ").lower()
    found = False
    for record in data:
        if query in record['Name Surname'].lower() or query in record['Person ID'].lower() or query in record['Telephone Number']:
            print("\nMatch Found:")
            print(f"Name: {record['Name Surname']}")
            print(f"Person ID: {record['Person ID']}")
            print(f"Email Address: {record['Person Mail Address']}")
            print(f"Phone Number: {record['Telephone Number']}")
            print(f"Gender: {record['Gender']}")
            print("-" * 30)
            found = True
    if not found:
        print("\nNo matches found for the provided query.")

def analyze_data():
    data = load_data('customer_data.csv')  # Load data afresh from the CSV
    df = pd.DataFrame(data)

    # ... rest of the function as before ...


    if 'Gender' not in df.columns:
        print("The data does not have a 'Gender' column.")
        return
    
    gender_counts = df['Gender'].value_counts()

    if gender_counts.empty:
        print("No gender data available for analysis.")
        return

    # Adjust explode based on the length of gender_counts
    explode_values = (0.1,) * len(gender_counts)

    plt.figure(figsize=(10, 6))
    gender_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['skyblue', 'pink'], explode=explode_values)
    plt.title('Distribution of Customers by Gender')
    plt.ylabel('')
    plt.show()

def delete_customer(data):
    # Input the ID of the customer to be deleted
    person_id = input("Enter the Person ID of the customer to be deleted: ")

    # Check if there's a customer with that ID
    customer_to_delete = None
    for record in data:
        if record['Person ID'] == person_id:
            customer_to_delete = record
            break

    # If found, delete the customer
    if customer_to_delete:
        data.remove(customer_to_delete)
        print(f"Customer with ID {person_id} has been deleted.")
    else:
        print(f"No customer found with ID {person_id}.")
    
    return data


def main_menu():
    print("\nMain Menu:")
    print("1. Add a New Customer")
    print("2. Display Customer Data")
    print("3. Save Data")
    print("4. Search Customer")
    print("5. Analyze and Visualize Data")
    print("6. Exit")
    
    choice = input("Enter your choice (1/2/3/4/5/6): ")

    return choice

def main_menu():
    print("\nMain Menu:")
    print("1. Add a New Customer")
    print("2. Display Customer Data")
    print("3. Save Data")
    print("4. Search Customer")
    print("5. Analyze and Visualize Data")
    print("6. Delete Customer by ID")  # New option added
    print("7. Exit")
    
    choice = input("Enter your choice (1/2/3/4/5/6/7): ")

    return choice

if __name__ == "__main__":
    data = load_data('customer_data.csv')

    while True:
        choice = main_menu()
        
        if choice == '1':
            data = insert_record(data)
        elif choice == '2':
            display_customer_data(data)
        elif choice == '3':
            save_data('customer_data.csv', data)
            print("Data saved.")
        elif choice == '4':
            search_customer(data)
        elif choice == '5':
            analyze_data()
        elif choice == '6':
            data = delete_customer(data)
        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option (1/2/3/4/5/6/7).")