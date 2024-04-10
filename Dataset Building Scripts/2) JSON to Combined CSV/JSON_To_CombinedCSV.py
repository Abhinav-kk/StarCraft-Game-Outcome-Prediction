import json
import csv
import os


# Function to flatten nested dictionaries
def flatten_dict(d, parent_key="", sep="."):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# Function to flatten the 'Players' field
def flatten_players(players, sep="."):
    flattened_players = {}
    for i, player in enumerate(players):
        prefix = f"Player{i+1}"
        if i + 1 > 2:
            break
        for k, v in player.items():
            # Simplify 'Color', 'Race', and 'Type' to just 'Name'
            if k == "Color" or k == "Race" or k == "Type":
                v = v.get("Name", "")
            flattened_players[f"{prefix}{sep}{k}"] = v
    return flattened_players


# Function to flatten the 'PlayerDescs' field
def flatten_player_descs(player_descs, sep="."):
    flattened_player_descs = {}
    for i, desc in enumerate(player_descs):
        prefix = f"Player{i+1}"
        if i + 1 > 2:
            break
        for k, v in desc.items():
            flattened_player_descs[f"{prefix}{sep}{k}"] = v
    return flattened_player_descs


# Function to extract leaveGameCmds information
def extract_leave_game_cmds(computed_info, sep="."):
    leave_game_cmds_info = computed_info.get("LeaveGameCmds", [])
    if leave_game_cmds_info is not None:
        leave_game_cmd_frame = [cmd.get("Frame", None)
                                for cmd in leave_game_cmds_info]
        leave_game_player_id = [
            cmd.get("PlayerID", None) for cmd in leave_game_cmds_info
        ]
    else:
        leave_game_cmd_frame = []
        leave_game_player_id = []
    return leave_game_cmd_frame, leave_game_player_id


# Get a list of all JSON files in the current directory
json_files = [file for file in os.listdir() if file.endswith(".json")]

# Create a list to store the flattened extracted data
all_data = []

# Set to store unique field names
fieldnames_set = set()

# Loop through each JSON file
for json_file in json_files:
    # Create the full path for the JSON file
    json_file_path = os.path.join(os.getcwd(), json_file)

    # Open and load the JSON data
    with open(json_file_path, encoding="utf-8") as json_data:
        data = json.load(json_data)

    # Extract the specific information needed from the 'Header' key and flatten nested objects
    header_info = data.get("Header", {})
    flat_header = flatten_dict(header_info)

    # Flatten the 'Players' field
    players_info = header_info.get("Players", [])
    flat_players = flatten_players(players_info)

    # Flatten the 'Computed' field
    computed_info = data.get("Computed", {})
    flat_computed = flatten_dict(computed_info)

    # Flatten the 'PlayerDescs' field
    player_descs_info = computed_info.get("PlayerDescs", [])
    flat_player_descs = flatten_player_descs(player_descs_info)

    # Extract leaveGameCmds information
    leave_game_cmd_frame, leave_game_player_id = extract_leave_game_cmds(
        computed_info)

    # Combine flattened header, players, computed, and player_descs
    combined_data = {
        "ReplayID": json_file[:-5],
        **flat_header,
        **flat_players,
        **flat_computed,
        **flat_player_descs,
        "leaveGameCmdFrame": leave_game_cmd_frame,
        "leaveGamePlayerId": leave_game_player_id,
    }

    # Remove 'Players', 'Computed', and 'PlayerDescs' fields from combined data
    combined_data.pop("Players", None)
    combined_data.pop("PlayerDescs", None)
    combined_data.pop("ChatCmds", None)
    combined_data.pop("Computed", None)
    combined_data.pop("LeaveGameCmds", None)

    # Update fieldnames_set with keys from the current record
    fieldnames_set.update(key for key in combined_data.keys())

    # Append the combined data to the list
    all_data.append(combined_data)

    print(f"Data added to CSV file for '{json_file}'.")


# Define the CSV file path
csv_file_path = "all_replays_data.csv"

# Convert set to list and sort it
fieldnames = sorted(list(fieldnames_set))

# Write the flattened extracted data to the CSV file
with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
    # Create a CSV writer
    csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header
    csv_writer.writeheader()

    # Write each record as a new row
    for record in all_data:
        # Convert lists to strings for 'leaveGameCmdFrame' and 'leaveGamePlayerId'
        record["leaveGameCmdFrame"] = ", ".join(
            map(str, record.get("leaveGameCmdFrame", []))
        )
        record["leaveGamePlayerId"] = ", ".join(
            map(str, record.get("leaveGamePlayerId", []))
        )

        csv_writer.writerow(record)

print(f"CSV file '{csv_file_path}' created successfully.")
