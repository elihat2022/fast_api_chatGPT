# FastAPI and MCP Integration

This project implements a simple integration of the MCP protocol using Pydantic AI to create an agent capable of interacting with various tools based on the AI agent's determination of relevance.

## Why This Project?

This project simplifies the integration of AI agents that can dynamically interact with tools like Tavily, all through FastAPI’s high-performance endpoints. It’s perfect for developers looking to explore AI-driven APIs or enhance their web applications with intelligent automation.

## Example Use Case

The AI agent can select tools to perform tasks like retrieving real-time web data (via Tavily) or generating responses (via OpenAI/ Gemini).

## Installation

- Create a virtual environment:
  `python -m venv env`
- Activate the virtual environment.

- Install the required packages:
  `pip install -r requirements.txt`

- Add the required API keys to the .env file:

```
OPENAI_API_KEY=sk-*******
GEMINI_API_KEY=AI*******
TVLY=tvly-*******
FILESYSTEM_PATH=Path for handle files
```

## API Keys Setup

### Required API Keys:

- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Tavily API Key**: Get from [Tavily](https://tavily.com/)

## Ejecute el proyecto

```
python main.py
```

### Support

If you encounter issues:

1. Check the console logs for detailed error messages
2. Verify all dependencies are installed correctly
3. Ensure API keys have sufficient permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
