from langchain_core.runnables import RunnableBranch
from chains import (code_explanation_chain, code_generation_chain, 
                    code_review_chain, code_optimization_chain, bug_fix_chain, default_chain)

 


router = RunnableBranch(
    (lambda x: x["mode"] == "Code Review", code_review_chain),
    (lambda x: x["mode"] == "Bug Fix", bug_fix_chain),
    (lambda x: x["mode"] == "Code Generation", code_generation_chain),
    (lambda x: x["mode"] == "Code Explanation", code_explanation_chain),
    (lambda x: x["mode"] == "Optimization", code_optimization_chain),
    default_chain
)