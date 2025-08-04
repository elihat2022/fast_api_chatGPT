from pydantic_ai import Agent

# Agent configuration using pydantic_ai
agent = Agent(
    'openai:gpt-4o',
    system_prompt=(
        "You are a helpful assistant that can search the web to answer user queries. "
        "When the user asks for information that you don't know or need current information about, "
        "use the search_query tool to perform a web search and provide a concise and accurate "
        "response based on the search results."
    ),
)