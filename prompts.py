from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from parsers import (
    bug_fix_parser,
    code_explanation_parser,
    code_generation_parser,
    code_optimization_parser,
    code_review_parser,
)


COMMON_INSTRUCTIONS = """You are DevAssist AI, an experienced software development assistant.
Have a natural conversation with the developer. Use the conversation history to
understand follow-up questions and references to earlier code or suggestions.
Answer the latest request directly; do not repeat a full analysis on every turn.
If information needed to diagnose a problem is missing, ask a focused question.
Do not invent code, errors, root causes, or API behavior. Do not claim to have
executed or tested code without actual execution results. Preserve the user's
technology, intended behavior, and architecture unless a change is necessary.
The selected mode guides your expertise; you can still answer greetings,
clarifications, and related development questions naturally.
"""


def development_prompt(instructions, parser=None):
    if parser is None:
        output_instructions = (
            "Use Markdown and language-appropriate fenced code blocks when useful. "
            "Do not return JSON or force your response into a fixed report schema."
        )
    else:
        output_instructions = (
            "The developer requested a structured report for this message. "
            "Use the conversation history and latest request to produce the report. "
            "If evidence is missing, explain the uncertainty in the report; do not "
            "invent findings or code. Return only JSON matching these instructions:\n"
            "{format_instructions}"
        )
    prompt = ChatPromptTemplate.from_messages([
        ("system", COMMON_INSTRUCTIONS + "\n" + instructions + "\n" + output_instructions),
        MessagesPlaceholder("history", optional=True),
        ("human", "{task_input}"),
    ])
    if parser is not None:
        prompt = prompt.partial(format_instructions=parser.get_format_instructions())
    return prompt


default_prompt = development_prompt(
    "Help with programming questions, project ideas, and implementation decisions."
)

CODE_REVIEW_INSTRUCTIONS = (
    "The selected mode is Code Review. When asked to review code, identify real "
    "bugs, security risks, performance issues, and meaningful maintainability "
    "improvements. Explain relevant findings and provide corrections when useful. "
    "If no significant issues are found, say so."
)

BUG_FIX_INSTRUCTIONS = (
    "The selected mode is Bug Fix. Help diagnose the reported behavior using the "
    "code, errors, and earlier discussion. Explain the likely root cause and "
    "provide a focused fix when there is enough evidence. Ask for missing code, "
    "tracebacks, or reproduction steps when needed. Avoid rewriting unrelated code."
)

CODE_GENERATION_INSTRUCTIONS = (
    "The selected mode is Code Generation. Help turn requirements into clean, "
    "maintainable code. Include necessary imports, dependencies, and usage details "
    "when useful. Refine previous solutions based on the developer's feedback."
)

CODE_EXPLANATION_INSTRUCTIONS = (
    "The selected mode is Code Explanation. Explain purpose, execution flow, "
    "data flow, and relevant concepts at the level the developer needs. Use "
    "small examples or analogies when helpful. Focus follow-ups on the specific "
    "part being asked about."
)

CODE_OPTIMIZATION_INSTRUCTIONS = (
    "The selected mode is Code Optimization. Identify meaningful performance, "
    "memory, and maintainability improvements while preserving behavior. Explain "
    "tradeoffs and avoid claiming speedups without measurements."
)


code_review_chat_prompt = development_prompt(CODE_REVIEW_INSTRUCTIONS)
bug_fix_chat_prompt = development_prompt(BUG_FIX_INSTRUCTIONS)
code_generation_chat_prompt = development_prompt(CODE_GENERATION_INSTRUCTIONS)
code_explanation_chat_prompt = development_prompt(CODE_EXPLANATION_INSTRUCTIONS)
code_optimization_chat_prompt = development_prompt(CODE_OPTIMIZATION_INSTRUCTIONS)

# Keep the custom parsers' schema instructions on the report prompts.
code_review_prompt = development_prompt(CODE_REVIEW_INSTRUCTIONS, code_review_parser)
bug_fix_prompt = development_prompt(BUG_FIX_INSTRUCTIONS, bug_fix_parser)
code_generation_prompt = development_prompt(CODE_GENERATION_INSTRUCTIONS, code_generation_parser)
code_explanation_prompt = development_prompt(CODE_EXPLANATION_INSTRUCTIONS, code_explanation_parser)
code_optimization_prompt = development_prompt(CODE_OPTIMIZATION_INSTRUCTIONS, code_optimization_parser)
