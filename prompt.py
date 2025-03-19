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



agent = Agent(
    model=Ollama(id="llama3.2:1b", options={"temperature": 0.1}),
    description="You are an Answer Bot specializing in providing information about plans and policies.",
    instructions=[
        "- For queries related to Privacy, Return Policy, Warranty, and General Terms and Conditions, search the knowledge base.",
        "- For queries that contain the keyword 'plan', exclusively use the 'get_NLQ' tool to generate responses.",
        "- Ensure that if a query involves both plans and other policies, prioritize using the correct tool as per context."
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


import json

def generate_plan_data():
    plans = [
        {
            "name": "Silver Plan",
            "price": "$30",
            "data": "20GB 5G",
            "hotspot": "No Hotspot",
            "features": ["Basic Streaming", "Unlimited Calls", "100 SMS"]
        },
        {
            "name": "Golden Plan",
            "price": "$25",
            "data": "10GB 5G",
            "hotspot": "No Hotspot",
            "features": ["Standard Streaming", "Unlimited Calls", "500 SMS"]
        },
        {
            "name": "Platinum Plan",
            "price": "$45",
            "data": "Unlimited 5G",
            "hotspot": "Unlimited Hotspot",
            "features": ["Premium Streaming", "Unlimited Calls", "Unlimited SMS", "International Roaming"]
        }
    ]
    return json.dumps(plans, indent=4)

print(generate_plan_data())
