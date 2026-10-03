from models import model
from langchain_core.output_parsers import StrOutputParser
from prompts import (
    code_review_prompt,
    bug_fix_prompt,
    code_generation_prompt,
    code_explanation_prompt,
    code_optimization_prompt,
    default_prompt
)

from parsers import (
    code_review_parser,
    bug_fix_parser,
    code_generation_parser,
    code_explanation_parser,
    code_optimization_parser,
)


default_chain = default_prompt| model| StrOutputParser()

code_review_chain = code_review_prompt| model| code_review_parser

bug_fix_chain = bug_fix_prompt| model| bug_fix_parser

code_generation_chain = code_generation_prompt| model| code_generation_parser

code_explanation_chain = code_explanation_prompt| model| code_explanation_parser

code_optimization_chain = code_optimization_prompt | model| code_optimization_parser 