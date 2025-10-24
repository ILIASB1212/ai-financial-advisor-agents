from pydantic import BaseModel, Field
from crewai.tools import tool

@tool("Markdown Generator Tool")
def markdown_generator_tool_function(report_content: str, file_name: str) -> str:
    """
    Formats raw text content into professional Markdown and returns it directly.
    The file_name parameter is accepted but ignored, as no file is saved.
    """
    
    class MarkdownGeneratorToolSchema(BaseModel):
        """Input schema for the Markdown Generator Tool."""
        report_content: str = Field(
            description="The full text content of the final report, ready for formatting."
        )
        file_name: str = Field(
            description="The desired output file name (now ignored)."
        )
    return report_content
