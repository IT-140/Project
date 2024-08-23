import os

# Define the room dictionary and other global variables
rooms = {
    'Entrance to the Crypt': {'North': 'Research Room'},
    'Research Room': {'North': 'Chamber of Shadows',
                      'East': 'Bed Chambers',
                      'West': 'Treasury',
                      'South': 'Entrance to the Crypt',
                      'Item': 'Tome of Dark Incantations'},
    'Treasury': {'East': 'Research Room',
                 'Item': 'Amulet of Undead Warding'},
    'Bed Chambers': {'West': 'Research Room',
                     'Item': 'Phylactery Orb'},
    'Chamber of Shadows': {'East': 'Armory',
                           'North': 'Throne Room',
                           'South': 'Research Room',
                           'Item': 'Orb of Shadow Veil'},
    'Armory': {'West': 'Chamber of Shadows',
               'Item': 'Soul Reaper Scythe'},
    'Throne Room': {'South': 'Chamber of Shadows',
                    'West': 'Ritual Sanctum',
                    'Item': 'Cursed Crown of Dominion'},
    'Ritual Sanctum': {'East': 'Throne Room'}
}

# Global variables
current_room = 'Entrance to the Crypt'
player_inventory = []
Lich_King_room = 'Ritual Sanctum'


# Function to clear the screen based on the operating system
def clear_screen():
    # Check the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')


# Define the get_new_state function
def get_new_state(direction_from_user, current_room_param):  # Function to get the new state based on player's direction
    global player_inventory  # Access the global variable for player's inventory
    global rooms   # Access the global variable for rooms

    # Check if the direction entered by the player is valid for the current room
    if direction_from_user in rooms[current_room_param]:
        new_room = rooms[current_room_param][direction_from_user]   # Get the new room based on the direction
        print("You moved to", new_room)  # Print a message indicating the player's movement

        # Check if there is an item in the new room
        if 'Item' in rooms[new_room]:
            item = rooms[new_room]['Item']  # Get the item in the new room
            print("You found an item:", item)  # Print a message indicating the item found in the new room

        return new_room
    else:
        print("You can't go that way.")
        return current_room_param  # Return the current room if the player cannot move


# Function to display game instructions
def show_instructions():
    instructions = (
        "The Lich King's Terror!\n"
        "Collect 6 items to win the game.\n"
        "Move commands: go North, go South, go East, go West\n"
        "Get item command: get [item name]\n"
        "Check status command: status\n"
        "To Quit: quit\n"
        "You are now in the Entrance to the Crypt"
    )
    print(instructions)


# Function to show current status
def show_status():
    global current_room  # Access the global variable directly
    print("Current Room:", current_room)

    if 'Item' in rooms[current_room]:  # Checks if there is an item in current room
        print("Item in Room:", rooms[current_room]['Item'])  # Print the item
    else:
        print("No item in this room.")  # No item message

    print("Inventory:", player_inventory)  # Print player inventory

    print("Available Directions:")   # Print available directions for movement
    available_directions = rooms[current_room].keys()  # Get available directions from the current room
    available_directions = [direction for direction in available_directions if direction != 'Item']
    print(", ".join(available_directions))  # Print available directions separated by comma


# Main function containing the gameplay loop
def main():
    show_instructions()

    global current_room  # Declare current_room as global
    current_room = 'Entrance to the Crypt'  # Initialize current room here
    while True:  # Start the loop
        command = input('Enter a command: ').lower()  # User input for the command
        action, *params = command.split()  # Split the input into action and parameters

        clear_screen()  # Keep the interface clean

        if action == 'go':  # Handle movements
            direction = params[0].capitalize()  # Capitalize for consistency
            if direction in rooms[current_room]:  # Check for valid direction
                current_room = get_new_state(direction, current_room)  # Pass current_room as parameter
            else:
                print('That is a wall... try again')  # Wrong direction
        elif action == 'get':  # Collection
            if len(params) == 0:
                print('Please specify the item name.')  # Prompt the user for the item
            else:
                item_name = ' '.join(params).lower()  # Join the parameters and convert to lowercase
                if 'Item' in rooms[current_room]:   # Check if there is an item in the current room
                    room_item = rooms[current_room]['Item']  # Get the item name from the room
                    if item_name.lower() == room_item.lower():  # Compare the entered item name with the room item name
                        player_inventory.append(room_item)   # Add the item to the player's inventory
                        del rooms[current_room]['Item']   # Remove the item from the room
                        print(f'You obtained the {room_item} from this room.')  # Player has the item now
                    else:
                        print('Item not found in this room.')  # Inform the player if the item is not in the room
                else:
                    print('No item in this room.')  # No item in the room
        elif action == 'status':
            show_status()  # Call show_status without passing current_room
        elif action == 'quit':
            break
        else:
            print('Uh... What kind of command was that?')  # Unknown command prompt response

        if len(player_inventory) == 6 and current_room == Lich_King_room:  # Good ending
            print('After meticulously collecting the items needed to defeat the Lich King, you had an epic fight\n'
                  'with the undead calamity. You somehow emerged victorious.\n'
                  'Congratulations!\n'
                  'You collected all items and defeated the Lich King.\n'
                  'You have saved the world!\n'
                  'You win!')
            break

        if current_room == Lich_King_room and len(player_inventory) < 6:  # Bad ending
            print("You encounter the Lich King, but you don't have all the required items to stop his treachery.\n"
                  'You lose!\n'
                  "Don't worry, you'll still live on in his undead army.")
            break


if __name__ == "__main__":
    main()
    # This is for terminal users. I realized that you couldn't read the ending since it auto closes the program
    input("Press Enter to exit...")
