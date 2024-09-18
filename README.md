# ⚽ EA FC Player Scout

**EA FC Player Scout** is an interactive chatbot that helps you find football players from the *EA FC* game based on multiple criteria like position, preferred foot, skill moves, and more. Using the OpenAI API, this bot understands your queries in natural language and performs detailed searches through a comprehensive player dataset.

## 🚀 Features

- 🔍 **Custom Player Search**: Filter players by position, skills (e.g., skill moves), attributes (e.g., passing, speed), and preferences (e.g., preferred foot).
- 🗣️ **Natural Language Interaction**: The chatbot understands various ways of asking and provides responses that fit your query.
- 🎯 **Advanced Filtering**: Use detailed criteria to find the perfect players based on *EA FC* attributes.

## 🛠️ Technologies Used

- 🐍 **Python**: Core language for the application.
- 🤖 **OpenAI API**: For natural language processing.
- 📊 **Pandas**: For data manipulation and player data analysis.

## 📝 How to Run the Project Locally

### Prerequisites

- **Python 3.7+** 🐍
- **OpenAI API key** 🔑
- **Pandas** (installed via pip) 📊

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/viney1907/EA-FC-Scout.git
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Add your OpenAI API key** to the `.env` file:

   Create a `.env` file in the root directory with the following content:

   ```bash
   OPENAI_API_KEY=your_openai_api_key
   ```

4. **Run the project**:

   ```bash
   python app.py
   ```

5. The chatbot will be ready to interact and find players based on the requested criteria.

## 💬 Usage Examples

You can ask questions like:

- *"I want a right-footed left winger with 5 skill moves."* 🦵⭐️⭐️⭐️⭐️⭐️
- *"Find a center-back with over 90 interceptions and a real face."* 🔍🙋‍♂️

The chatbot will process your request and return a list of players matching the criteria.

## 🤝 Contributions

Contributions are welcome! Feel free to open an **issue** or submit a **pull request** with new features, improvements, or bug fixes. Let’s make this even better together! 💡👨‍💻👩‍💻

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
