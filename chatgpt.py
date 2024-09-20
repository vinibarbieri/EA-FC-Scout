import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

class ChatGPT:
    def __init__(self):
        valid_attributes = ["player_id","name","full_name","description","height_cm","weight_kg","dob","positions","overall_rating","potential","value","wage","preferred_foot","weak_foot","skill_moves","international_reputation","work_rate","body_type","real_face","release_clause","specialities","club_name","club_league_name","club_rating","club_kit_number","club_joined","club_contract_valid_until","country_name","country_league_name","country_rating","country_position","crossing","finishing","heading_accuracy","short_passing","volleys","dribbling","curve","fk_accuracy","long_passing","ball_control","acceleration","sprint_speed","agility","reactions","balance","shot_power","jumping","stamina","strength","long_shots","aggression","interceptions","positioning","vision","penalties","composure","defensive_awareness","standing_tackle","sliding_tackle","gk_diving","gk_handling","gk_kicking","gk_positioning","gk_reflexes","play_styles"]
        self.valid_attributes = valid_attributes

    def output(self, query):
        output = self.identify_criteria(query)
        output = self.replace_bool_with_yes_no(output)
        output = self.convert_market_value(output)
        output = self.convert_positions_to_list(output)
        return output
    
    # Function to identify the criteria requested by the user
    def identify_criteria(self, query):
        query = self.handle_query(query)

        prompt = f"""
        You have the following list of football player attributes: {', '.join(self.valid_attributes)}.
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

    # Function to handle user queries
    def handle_query(self, query):
        skills = ['skill stars', 'dribbling stars', 'skill moves', 'skills', 'estrelas de drible', 'estrelas de habilidade']
        weak_foot = ['weak foot stars', 'estrelas de pé fraco', 'estrelas de perna ruim']
        for skill in skills:
            if skill in query:
                query = query.replace(skill, "skill_moves")
        for weak_foot in query:
            if weak_foot in query:
                query = query.replace('weak foot stars', 'weak_foot')
        return query

    # Function to replace boolean values with Yes or No
    def replace_bool_with_yes_no(self, criteria):
        for key, value in criteria.items():
            if value == True or value == 'true':
                criteria[key] = 'Yes'
            elif value == False or value == 'false':
                criteria[key] = 'No'
        return criteria
    
    def convert_positions_to_list(self, criteria):
        if 'positions' in criteria and isinstance(criteria['positions'], str):
            criteria['positions'] = criteria['positions'].split(',')
        return criteria

    # Function to convert the market value to a numeric format from chat output
    def convert_market_value(self, output):
        for key, value in output.items():
            if key in ['value', 'wage', 'release_clause']:
                value = value.replace('€', '')
                if isinstance(value, (int, str)):
                    output[key] = value
                if not isinstance(value, str):
                    output[key] = str('nan')
                if 'K' in value:
                    output[key] = str(value.replace('K', '')) * 1000
                elif 'M' in value:
                    output[key] = str(value.replace('M', '')) * 1000000
                elif 'B' in value:
                    output[key] = str(value.replace('B', '')) * 1000000000
                else:
                    output[key] = str(value)
        return output
