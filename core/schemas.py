from pydantic import BaseModel, Field
from typing import Optional, Literal




class CodeGeneration(BaseModel):
    title: str = Field(description="Short title describing the generated solution")

    approach: str = Field(
        description="Brief explanation of the approach used to solve the requirement."
        "Make a mental model also"
        )

    generated_code: str = Field(description="Complete generated source code")

    explanation: str = Field(description="Explanation of how the generated code works")

    dependencies: list[str] = Field(description="Required packages, libraries, or dependencies")

    usage_instructions: list[str] = Field(description="Steps explaining how to use or run the generated code")



class CodeExplanation(BaseModel):
    summary: str = Field(description="Short summary explaining what the code does")

    purpose: str = Field(description="Main purpose of the provided code")

    execution_flow: list[str] = Field(
        description="Step-by-step explanation of how the code executes by give showing block of code"
    )

    important_concepts: list[str] = Field(
        description="Programming concepts or patterns used in the code"
    )

    complexity: Optional[str] = Field(
        default=None,
        description="Explanation of relevant time and space complexity when applicable"
    )

    simplified_explanation: str = Field(
        description="Beginner-friendly explanation of the code. Use a simple analogy for better understanding"
    )



class CodeOptimizationResult(BaseModel):
    summary: str = Field(description="Summary of the optimization analysis")

    performance_issues: list[str] = Field(description="Performance-related problems found in the code")

    code_quality_issues: list[str] = Field(description="Readability, maintainability, duplication, or design issues")

    memory_issues: list[str] = Field(description="Potential memory usage or resource management issues")

    optimization_suggestions: list[str] = Field(description="Recommended optimization improvements")

    optimized_code: str = Field(description="Improved and optimized version of the original code")

    changes_made: list[str] = Field(description="List of important changes made in the optimized version")



class CodeReview(BaseModel):
    summary: str = Field(
        description=(
            "Provide a concise overall review of the submitted code. "
            "Mention the general code quality, readability, structure, "
            "and the most important findings."
        )
    )

    bugs: Optional[list[str]] = Field(
        default=None,
        description=(
            "Identify actual or potential bugs in the code. "
            "Explain each bug clearly and mention why it may cause incorrect behavior. "
            "If no bugs are found, return None. "
            "Do not invent bugs."
        )
    )
    
    security_issues: Optional[list[str]] = Field(
        default=None,
        description=(
            "Identify possible security vulnerabilities or unsafe coding practices, "
            "such as injection risks, exposed secrets, insecure authentication, "
            "unsafe input handling, or improper data validation."
            
        )
    )

    performance_issues:  Optional[list[str]] = Field(
        description=(
            "Identify performance problems such as unnecessary loops, repeated operations, "
            "inefficient database queries, excessive memory usage, blocking operations, "
            "or other unnecessary computational costs."
        )
    )

    improvements: list[str] = Field(
        description=(
            "Suggest practical improvements related to code readability, maintainability, "
            "architecture, naming, error handling, best practices, and overall code quality."
        )
    )

    corrected_code: Optional[str] = Field(
        description=(
            "Provide a corrected or improved version of the code only when meaningful changes "
            "are necessary. Preserve the original functionality unless fixing an identified issue. "
            "Return None if no corrected version is needed."
        )
    )



class BugFixResult(BaseModel):

    root_cause: str = Field(
        description=(
            "Identify the main root cause of the bug or error. "
            "Explain what is causing the problem rather than only describing the error message."
        )
    )

    explanation: str = Field(
        description=(
            "Explain the bug in clear developer-friendly language. "
            "Describe why it happens and how the proposed fix resolves it."
        )
    )

    fixed_code: str = Field(
        description=(
            "Provide the corrected version of the relevant code as a senior programer "
            "Fix the reported issue while avoiding unnecessary changes to unrelated parts."
        )
    )

    changes: list[str] = Field(
        description=(
            "List the important modifications made to fix the issue. "
            "Each item should briefly explain what was changed and why."
        )
    )