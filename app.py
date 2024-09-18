import os
from dotenv import load_dotenv
import pandas as pd
from openai import OpenAI
import json

load_dotenv()
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

players = pd.read_csv('player-data-full.csv', low_memory=False)

valid_attributes = ["player_id", "name", "full_name", "description", "image", "height_cm", "weight_kg", "dob", "positions",
                    "overall_rating", "potential", "value", "wage", "preferred_foot", "weak_foot", "skill_moves", "international_reputation",
                    "work_rate", "body_type", "real_face", "release_clause", "specialities", "club_id", "club_name", "club_league_id",
                    "club_league_name", "club_logo", "club_rating", "club_position", "club_kit_number", "club_joined", "club_contract_valid_until",
                    "country_id", "country_name", "country_league_id", "country_league_name", "country_flag", "country_rating", "country_position",
                    "country_kit_number", "crossing", "finishing", "heading_accuracy", "short_passing", "volleys", "dribbling", "curve", "fk_accuracy",
                    "long_passing", "ball_control", "acceleration", "sprint_speed", "agility", "reactions", "balance", "shot_power", "jumping",
                    "stamina", "strength", "long_shots", "aggression", "interceptions", "positioning", "vision", "penalties", "composure",
                    "defensive_awareness", "standing_tackle", "sliding_tackle", "gk_diving", "gk_handling", "gk_kicking", "gk_positioning", "gk_reflexes", "play_styles"]

# Function to handle user queries
def handle_query(query):
    skills = ['skill stars', 'dribbling stars', 'skill moves', 'skills', 'estrelas de drible', 'estrelas de habilidade']
    weak_foot = ['weak foot stars', 'estrelas de pé fraco', 'estrelas de perna ruim']
    for skill in skills:
        if skill in query:
            query = query.replace(skill, "skill_moves")
    for weak_foot in query:
        if weak_foot in query:
            query = query.replace('weak foot stars', 'weak_foot')
    return query

def replace_bool_with_yes_no(criteria):
    for key, value in criteria.items():
        if value == True or value == 'true':
            criteria[key] = 'Yes'
        elif value == False or value == 'false':
            criteria[key] = 'No'
    return criteria

# Function to identify the criteria requested by the user
def identify_criteria(query):
    query = handle_query(query)

    prompt = f"""
    You have the following list of football player attributes: {', '.join(valid_attributes)}.
    The user asked the following question: '{query}'.
    Identify which of these attributes they are requesting, if any. If they don't directly mention attributes, use your best judgment to suggest relevant attributes.
    Return a json with the identified criteria or ones that could be useful, along with the requested value (e.g. "short_passing": >80, ...), without further explanation.
    """
    
    completion = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}
        ],
        max_tokens=150
    )
    
    gpt_response = completion.choices[0].message.content.strip()

    # Remove code blocks if any
    gpt_response = gpt_response.replace("```json", "").replace("```", "").strip()

    # Try to convert the response to a dictionary
    try:
        response_dict = json.loads(gpt_response)
    except json.JSONDecodeError as e:
        print(f"Error decoding GPT response: {e}")
        return None
    
    return response_dict

# Function to search for players based on multiple criteria
def search_players_by_multiple_criteria(criteria):
    query = players  # Start with the full dataframe

    for criterion, value in criteria.items():
        if criterion in players.columns:
            if isinstance(value, list) or criterion == "positions":
                # Check if the DataFrame value is contained in the list
                query = query[query[criterion].apply(lambda x: any(pos in x for pos in value))]
            # Check if the value contains an operator
            elif isinstance(value, str) and (value.startswith(">") or value.startswith("<") or value.startswith("=")):
                operator = value[0]
                value_num = float(value[1:])  # Convert the numeric part of the string
                
                # Apply the correct operator
                if operator == ">":
                    query = query[query[criterion] > value_num]
                elif operator == "<":
                    query = query[query[criterion] < value_num]
                elif operator == "=":
                    query = query[query[criterion] == value_num]
            else:
                # If no operator, treat as an exact match
                query = query[query[criterion] == value]
        else:
            print(f"The criterion '{criterion}' was not found in the CSV file.")
    
    if query.empty:
        return "No players found with the provided criteria."
    
    # Return the top 5 players found
    return query[["name", "positions", "overall_rating"] + list(criteria.keys())].to_dict(orient='records')

# Main function that processes the user's query
def answer_query(query):
    # Identify the criteria mentioned by GPT
    criteria = identify_criteria(query)
    
    if criteria:
        criteria = replace_bool_with_yes_no(criteria)

        # Search the CSV for players based on multiple criteria
        found_players = search_players_by_multiple_criteria(criteria)
        return found_players, list(criteria.keys())
    else:
        return "Sorry, I couldn't identify the requested criteria."

        
# Function to format players in a nicer way
def formatted_response(players, requested_criteria):
    formatted_players = []
    for player in players:
        player_formatted = f"Name: {player['name']}\n"
        player_formatted += f"Position: {player['positions']}\n"
        player_formatted += f"Overall Rating: {player['overall_rating']}\n"
        # Add the criteria used for the search
        for criterion in requested_criteria:
            if criterion in player:
                player_formatted += f"{criterion.capitalize()}: {player[criterion]}\n"
        player_formatted += "-" * 30
        formatted_players.append(player_formatted)
    return "\n\n".join(formatted_players)


def main():
    print("\nWelcome to the best EA FC scout!")
    print("You can ask to find players based on multiple criteria. To exit, type 'exit'.")

    while True:
        query = input("\nPlease enter your request: ")

        if query.lower() in ['exit', 'quit','sair', '0']:
            print("Goodbye!")
            break

        response, requested_criteria = answer_query(query)

        print("\nFound players:\n")
        print(formatted_response(response, requested_criteria))

if __name__ == "__main__":
    main()
