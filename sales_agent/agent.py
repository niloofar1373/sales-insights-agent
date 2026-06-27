from google.adk.agents.llm_agent import Agent

try:
    from sales_agent import data_loader
except ImportError:
    import data_loader

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='An expert sales insights assistant that helps analyze e-commerce transaction data.',
    instruction=(
        'You are an expert sales insights assistant. Your job is to answer user questions about the '
        'e-commerce retail dataset. Use the provided tools to query the data and answer user questions accurately. '
        'Always cite figures and names directly returned by the tools. '
        'When asked for an insights report or analysis report, first call draft_insights_report for the requested '
        'topic/date range and show the full draft to the user in the chat, then ask: "Do you approve this report, or '
        'would you like changes?" '
        'You MUST ONLY call finalize_insights_report after the user explicitly approves it or provides edits.'
    ),
    tools=[
        data_loader.get_dataset_summary,
        data_loader.get_top_products,
        data_loader.get_top_customers,
        data_loader.get_sales_by_country,
        data_loader.query_sales_by_date_range,
        data_loader.search_products,
        data_loader.draft_insights_report,
        data_loader.finalize_insights_report,
    ]
)
