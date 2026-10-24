from langchain_core.runnables import RunnableBranch
from chains import (
    bug_fix_chain,
    bug_fix_chat_chain,
    code_explanation_chain,
    code_explanation_chat_chain,
    code_generation_chain,
    code_generation_chat_chain,
    code_optimization_chain,
    code_optimization_chat_chain,
    code_review_chain,
    code_review_chat_chain,
    default_chain,
)


chat_router = RunnableBranch(
    (lambda x: x["mode"] == "Code Review", code_review_chat_chain),
    (lambda x: x["mode"] == "Bug Fix", bug_fix_chat_chain),
    (lambda x: x["mode"] == "Code Generation", code_generation_chat_chain),
    (lambda x: x["mode"] == "Code Explanation", code_explanation_chat_chain),
    (lambda x: x["mode"] == "Code Optimization", code_optimization_chat_chain),
    default_chain,
)

report_router = RunnableBranch(
    (lambda x: x["mode"] == "Code Review", code_review_chain),
    (lambda x: x["mode"] == "Bug Fix", bug_fix_chain),
    (lambda x: x["mode"] == "Code Generation", code_generation_chain),
    (lambda x: x["mode"] == "Code Explanation", code_explanation_chain),
    (lambda x: x["mode"] == "Code Optimization", code_optimization_chain),
    default_chain,
)

router = RunnableBranch(
    (lambda x: x.get("response_format") == "structured", report_router),
    chat_router,
)
