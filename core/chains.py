from langchain_core.output_parsers import StrOutputParser

from .models import model
from core.parsers import (
    bug_fix_parser,
    code_explanation_parser,
    code_generation_parser,
    code_optimization_parser,
    code_review_parser,
)
from .prompts import (
    bug_fix_chat_prompt,
    bug_fix_prompt,
    code_explanation_chat_prompt,
    code_explanation_prompt,
    code_generation_chat_prompt,
    code_generation_prompt,
    code_optimization_chat_prompt,
    code_optimization_prompt,
    code_review_chat_prompt,
    code_review_prompt,
    default_prompt,
)


default_chain = default_prompt | model | StrOutputParser()

# Ordinary conversation and follow-ups do not require a report schema.
code_review_chat_chain = code_review_chat_prompt | model | StrOutputParser()
bug_fix_chat_chain = bug_fix_chat_prompt | model | StrOutputParser()
code_generation_chat_chain = code_generation_chat_prompt | model | StrOutputParser()
code_explanation_chat_chain = code_explanation_chat_prompt | model | StrOutputParser()
code_optimization_chat_chain = code_optimization_chat_prompt | model | StrOutputParser()

# Explicit reports retain the project's original custom parsers and schemas.
code_review_chain = code_review_prompt | model | code_review_parser
bug_fix_chain = bug_fix_prompt | model | bug_fix_parser
code_generation_chain = code_generation_prompt | model | code_generation_parser
code_explanation_chain = code_explanation_prompt | model | code_explanation_parser
code_optimization_chain = code_optimization_prompt | model | code_optimization_parser
