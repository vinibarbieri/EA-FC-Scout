from player_search import PlayerSearch

def main():
    search = PlayerSearch('player-data-full.csv')
    print("\nWelcome to the best EA FC scout!")
    print("You can ask to find players based on multiple criteria. To exit, type 'exit'.")

    while True:
        query = input("\nPlease enter your request: ")
        print("-"*100)

        if query.lower() in ['exit', 'quit','sair', '0']:
            print("Goodbye!")
            break

        response, requested_criteria = search.answer_query(query)

        print("\nFound players:\n")
        print(search.formatted_response(response, requested_criteria))

if __name__ == "__main__":
    main()
