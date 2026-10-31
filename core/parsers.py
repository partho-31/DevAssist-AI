from langchain_core.output_parsers import PydanticOutputParser
from core.schemas import BugFixResult, CodeExplanation, CodeGeneration, CodeOptimizationResult, CodeReview




code_review_parser = PydanticOutputParser(pydantic_object=CodeReview)

bug_fix_parser = PydanticOutputParser(pydantic_object=BugFixResult)

code_generation_parser = PydanticOutputParser(pydantic_object=CodeGeneration)

code_explanation_parser = PydanticOutputParser(pydantic_object=CodeExplanation)

code_optimization_parser = PydanticOutputParser(pydantic_object=CodeOptimizationResult)