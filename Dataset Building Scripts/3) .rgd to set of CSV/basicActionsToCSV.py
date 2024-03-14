import os
import pandas as pd


def parse_rgd_file(rgd_content, replay_id):
    actions = []
    resources = []
    destroyed = []
    attacked = []
    for line in rgd_content:
        action_info = line.strip().split(",")
        try:
            if (
                action_info[2].strip() == "Created"
                and int(action_info[1].strip()) != -1
            ):
                actions.append(
                    {
                        "Frame": int(action_info[0].strip()),
                        "PlayerID": int(action_info[1].strip()) + 1,
                        "ActionType": action_info[2].strip(),
                        "UnitID": action_info[3].strip(),
                        "UnitType": action_info[4].strip(),
                        "PositionX": action_info[5].strip().replace("(", ""),
                        "PositionY": action_info[6].strip().replace(")", ""),
                        "ReplayID": replay_id,
                    }
                )
            elif action_info[2].strip() == "R":
                resources.append(
                    {
                        "Frame": int(action_info[0].strip()),
                        "PlayerID": int(action_info[1].strip()) + 1,
                        "R": action_info[2].strip(),
                        "Minerals": int(action_info[3].strip()),
                        "Gas": int(action_info[4].strip()),
                        "GatheredMinerals": int(action_info[5].strip()),
                        "GatheredGas": int(action_info[6].strip()),
                        "SupplyUsed": int(action_info[7].strip()),
                        "SupplyTotal": int(action_info[8].strip()),
                        "ReplayID": replay_id,
                    }
                )
            elif action_info[2].strip() == "Destroyed":
                destroyed.append(
                    {
                        "Frame": int(action_info[0].strip()),
                        "PlayerID": int(action_info[1].strip()) + 1,
                        "ActionType": action_info[2].strip(),
                        "UnitID": action_info[3].strip(),
                        "UnitType": action_info[4].strip(),
                        "PositionX": action_info[5].strip().replace("(", ""),
                        "PositionY": action_info[6].strip().replace(")", ""),
                        "ReplayID": replay_id,
                    }
                )
        except:
            continue

    return actions, resources, destroyed


# Get a list of all .rgd files in the directory
rgd_files = [file for file in os.listdir() if file.endswith(".rgd")]

# Process each .rgd file
for rgd_file_name in rgd_files:
    print(f"Processing file: {rgd_file_name}")

    with open(rgd_file_name, "r") as rgd_file:
        rgd_content = rgd_file.readlines()

    # Update ReplayID with the current file name (without extension)
    replay_id = os.path.splitext(rgd_file_name)[0]
    replay_name = replay_id.split(".")[0]
    actions, resources, destroyed = parse_rgd_file(rgd_content, replay_name)

    # Sample code for creating DataFrames
    actions_df = pd.DataFrame(actions)
    resources_df = pd.DataFrame(resources)
    destroyed_df = pd.DataFrame(destroyed)

    # Save DataFrames to CSV files
    actions_df.to_csv(f"{replay_name}_actions.csv", index=False)
    resources_df.to_csv(f"{replay_name}_resources.csv", index=False)
    destroyed_df.to_csv(f"{replay_name}_destroyed.csv", index=False)

    print(f"File {rgd_file_name} processed.\n")
