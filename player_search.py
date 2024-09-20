import pandas as pd
from chatgpt import ChatGPT

chat_gpt = ChatGPT()

class PlayerSearch:
    def __init__(self, csv_path):
        self.players = pd.read_csv(csv_path, low_memory=False)
        # Remove espaços em branco e caracteres especiais dos nomes das colunas
        self.players.columns = self.players.columns.str.strip()  # Remove espaços em branco
        self.players.columns = self.players.columns.str.replace(r'\s+', '_', regex=True)  # Substitui espaços por underscore
        self.column_counts = self.players.columns.value_counts()


    
    @staticmethod
    def convert_market_value(value):
        value = value.replace('€', '')
        if isinstance(value, (int, float)):
            return value
        if not isinstance(value, str):
            return float('nan')
        if 'K' in value:
            return float(value.replace('K', '')) * 1000
        elif 'M' in value:
            return float(value.replace('M', '')) * 1000000
        elif 'B' in value:
            return float(value.replace('B', '')) * 1000000000
        else:
            return float(value)
        
    def format_value(self, value):
        if value > 1000000:
            return f"€{value/1000000:.1f}M"
        elif value > 100000:
            return f"€{value/1000:.0f}K"
        elif value > 1000:
            return f"€{value/1000:.1f}K"
        

    # Function to search for players based on multiple criteria
    def search_players_by_multiple_criteria(self, criteria):
        query = self.players  # Start with the full dataframe

        for criterion, value in criteria.items():
            if criterion in self.players.columns:
                if criterion in ["value", "release_clause", "wage"]:
                    # Convert the market value to a numeric format
                    query.loc[:, criterion] = query[criterion].apply(self.convert_market_value)

                # Check if the value is a list or if the criterion is 'positions'
                if isinstance(value, list):
                    if criterion == "positions":             
                        # Apply a filter for each position in the list
                        filtered_query = query[query[criterion].apply(lambda x: any(pos in x.split(',') for pos in value))]                        
                        # Update the query with the filtered results
                        query = filtered_query
                    else:
                        # Check if any value in the list matches the criterion exactly
                        query = query[query[criterion].isin(value)]

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
            return False

        # Get the unique keys from the criteria and add the default keys
        criteria_keys = list(dict.fromkeys(["name", "positions", "overall_rating"] + list(criteria.keys())))

        # Return the results as a list of dictionaries
        return query[criteria_keys].to_dict(orient='records')



    # Main function that processes the user's query
    def answer_query(self, query):
        # Identify the criteria mentioned by GPT
        criteria = chat_gpt.output(query)
        print(f"GPT Output: {criteria}")

        if criteria:
            # Search the CSV for players based on multiple criteria
            found_players = self.search_players_by_multiple_criteria(criteria)
            return found_players, list(criteria.keys())
        else:
            return "Sorry, I couldn't identify the requested criteria."

    # Function to format players in a nicer way
    def formatted_response(self, players, requested_criteria):
        formatted_players = []

        if players:
            for player in players:
                player_formatted = f"Name: {player['name']}\n"
                player_formatted += f"Position: {player['positions']}\n"
                player_formatted += f"Overall Rating: {player['overall_rating']}\n"

                added_criteria = {'name', 'positions', 'overall_rating'}

                # Add the criteria used for the search
                for criterion in requested_criteria:
                    if criterion in player and criterion not in added_criteria:
                        # Formatar o valor de mercado
                        if criterion in ["value", "release_clause", "wage"]:
                            player[criterion] = self.format_value(player[criterion])
                        player_formatted += f"{criterion.capitalize()}: {player[criterion]}\n"
                player_formatted += "-" * 30
                formatted_players.append(player_formatted)
        else:
            return "No players found with the provided criteria."
        return "\n\n".join(formatted_players)
