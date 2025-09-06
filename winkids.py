import csv
from datetime import datetime

# Function to load contacts from CSV file
def load_contacts(filename):
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print("The contacts file does not exist. Creating a new one.")
        return []

def reset_ids(contacts):
    for id,contact in enumerate(contacts, start=1):
        contact['ID'] = str(id)

# Function to save contacts to CSV file
def save_contacts(filename, contacts):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["ID","Teacher_1","Teacher_2", "Date", "Subject","Remarks"])
        writer.writeheader()
        writer.writerows(contacts)

# Function to display contacts
def display_contacts(contacts):
    print("\n{:<10} {:<15} {:<15} {:<12} {:<80} {:<20}".format("ID", "Teacher_1","Teacher_2", "Date" , "Subject", "Remarks"))
    print("-" * 150)
    for contact in contacts:
        print("{:<10} {:<15} {:<15} {:<12} {:<80} {:<20}".format(contact['ID'],contact['Teacher_1'],contact['Teacher_2'], contact['Date'], contact['Subject'], contact['Remarks'])) #add address

# Function to add a new contact
def add_contact(contacts):
    teacher_id = str(len(contacts) + 1)  # Generate a new ID based on the current number of contacts
    name1 = input("Enter 1st Teacher: ")
    name2 = input("Enter 2nd Teacher: ")
    date = input("Enter Assigned Date (MM-DD-YY) format: ")
    subject = input("What subject are they teaching?: ")
    #address = input ("Enter city: ") #add address
    contacts.append({"ID": teacher_id,"Teacher_1": name1,"Teacher_2":name2, "Date": date, "Subject": subject,"Remarks": ""})  # Initialize Remarks as empty

def set_teacher_remarks(contacts):
    teachers_id = input("Enter Teacher's ID to set remarks: ")
    found = False
    for contact in contacts:
        if contact['ID'] == teachers_id:
            remarks = input(f"Enter remarks for Teacher with ID {teachers_id}: ")
            contact['Remarks'] = remarks
            found = True
            print(f"Remarks for Teacher with ID '{teachers_id}' are set successfully.")
            break
    if not found:
        print("Teacher's ID is not found.")
        
def quick_search(contacts):
    target_date = input("Enter the date to search for (DD-Mon ex: 12-Oct): ")
    found = False
    print("\n{:<10} {:<15} {:<15} {:<12} {:<80} {:<20}".format("ID", "Teacher_1","Teacher_2", "Date" , "Subject", "Remarks"))
    print("-" * 150)
    for contact in contacts:
        if contact['Date'].lower() == target_date.lower():
            print("{:<10} {:<15} {:<15} {:<12} {:<80} {:<20}".format(contact['ID'],contact['Teacher_1'],contact['Teacher_2'], contact['Date'], contact['Subject'], contact['Remarks']))
            found = True
    if not found:
        print(f"No teachers found for the date {target_date}.")

# Update teacher using teachers ID
def update_contact(contacts):
    teachers_id = input("Enter Teacher's ID to update: ")
    found = False
    for contact in contacts:
        if contact['ID'] == teachers_id:
            found = True
            response = input("Update the teacher's name? (Y or N): ")
            if response.lower() == 'y':
                teacher_num = input("Which teacher do you want to update? (1 or 2 or Both): ")
                if teacher_num == '1':
                    contact['Teacher_1'] = input(f"Enter the updated 1st teacher name for ID {teachers_id}: ")
                elif teacher_num == '2':
                    contact['Teacher_2'] = input(f"Enter the updated 2nd teacher name for ID {teachers_id}: ")
                elif teacher_num.lower() == 'both':
                    contact['Teacher_1'] = input(f"Enter the updated 1st teacher name for ID {teachers_id}: ")
                    contact['Teacher_2'] = input(f"Enter the updated 2nd teacher name for ID {teachers_id}: ")
                else:
                    print("Invalid option. No name updated.")

            teacher_date = input("Update the date assigned? (Y or N): ")
            if teacher_date.lower() == 'y':
                contact['Date'] = input(f"Enter the new date assigned for ID {teachers_id}: ")
            else:
                print("Date not updated.")

            teacher_subject = input("Update the subject assigned? (Y or N): ")
            if teacher_subject.lower() == 'y':
                contact['Subject'] = input(f"Enter the new subject assigned for ID {teachers_id}: ")
            else:
                print("Subject not updated.")

            print(f"Teacher tasks with ID '{teachers_id}' are updated successfully.")
            break
    if not found:
        print("Teacher's ID is not found.")
# Function to delete a contact using 'remove'
def delete_contact(contacts):
    #name = input("Enter the name of the teacher to delete: ")
    teachers_id = input("Enter teacher's name to update: ")
    for contact in contacts:
        #if contact['Teacher'].lower() == name.lower():
        if contact['ID'] == teachers_id:
            contacts.remove(contact)
            reset_ids(contacts)  # Reset IDs after deletion
            print(f"Teachers with ID '{teachers_id}' is deleted successfully.")
            return
    print("Teacher's name is not found.")

# Main function to run the contact management system
def run_contact_manager():
    contacts_file = 'winkids.csv'
    contacts = load_contacts(contacts_file)

    while True:
        print("\nWinkids Teachers")
        print("1. Display Teachers")
        print("2. Add a new Teacher")
        print("3. Update Teacher Details")
        print("4. Remove a Teacher")
        print("5. Set Teacher Remarks")
        print("6. Quick Search by Date")
        print("7. Exit")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            display_contacts(contacts)
        elif choice == '2':
            add_contact(contacts)
            save_contacts(contacts_file, contacts)
        elif choice == '3':
            display_contacts(contacts)
            update_contact(contacts)
            save_contacts(contacts_file, contacts)
        elif choice == '4':
            delete_contact(contacts)
            save_contacts(contacts_file, contacts)
        elif choice == '5':
            set_teacher_remarks(contacts)
            save_contacts(contacts_file, contacts)
        elif choice == '6':
            quick_search(contacts)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

# Running the contact manager
run_contact_manager()
