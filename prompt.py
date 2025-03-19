agent = Agent(
    model=Ollama(id="llama3.2:1b",options={"temperature":0.1}),
    description="you are a Answer bot. If Plan in user query use tools get_nlq and if not use knowledge base.",
    instructions=[
        "Search your knowledge base for Privacy, Return Policy, Warrenty, Policy. Privacy queries and General Terms and conditions",
            "Search your get_NLQ tool for PLAN related queries",
        "if plan keyword is present in query then use only the tools to answer."
    ],
    knowledge=knowledge_base,
    tools=[get_nlq],
    show_tool_calls=True,
    markdown=True,
    search_knowledge=True,
    add_history_to_messages=True,
    num_history_responses=3,
    storage=SqliteAgentStorage(table_name="agent_tools", db_file="tmp/tupdate.db")
)
