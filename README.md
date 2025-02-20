# AI FAQs Chatbot

An AI-powered chatbot designed to answer frequently asked questions (FAQs) about various topics using natural language processing (NLP).

## Features
- Handles common FAQs efficiently
- Supports conversational AI responses
- Can be integrated into websites, apps, or messaging platforms
- API support for seamless integration

## Installation

### Prerequisites
- Python 3.x
- Required libraries: `flask`, `requests`, `transformers`, `torch`

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/ai-faqs-chatbot.git
   cd ai-faqs-chatbot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the chatbot server:
   ```sh
   python app.py
   ```

## Usage
### API Usage
Send a request to the chatbot API:
```sh
curl -X POST "http://localhost:5000/chat" -H "Content-Type: application/json" -d '{"question": "What is AI?"}'
```

Example response:
```json
{
  "answer": "AI stands for Artificial Intelligence, which is the simulation of human intelligence in machines."
}
```

### Terminal Mode
Run the chatbot in interactive mode:
```sh
python chatbot.py
```
Then enter your questions directly.

## Deployment
To deploy the chatbot on a cloud server or containerized environment:
1. **Docker (Optional)**
   ```sh
   docker build -t ai-faqs-chatbot .
   docker run -p 5000:5000 ai-faqs-chatbot
   ```
2. **Deploy on Heroku or AWS (Optional)**
   - Use `Procfile` for Heroku deployment.
   - Set up an EC2 instance or Lambda function for AWS.

## Future Enhancements
- Integrate with a UI for better user interaction
- Add support for multiple languages
- Improve NLP model with custom training

## Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

