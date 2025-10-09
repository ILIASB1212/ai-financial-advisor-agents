# markdown_generator_tool.py (FINAL CORRECT VERSION for TypeError)

from pydantic import BaseModel, Field
from crewai.tools import tool # Confirmed: This import works in your environment

# --------------------------------------------------------------------
# 1. Define the Tool Function using the @tool decorator
#    CRITICAL CHANGE: Removed 'args_schema=MarkdownInput'
# --------------------------------------------------------------------
@tool("Markdown Generator Tool")
def markdown_generator_tool_function(report_content: str, file_name: str) -> str:
    """Formats raw text content into professional Markdown with proper headings and tables, and saves it to a file."""
    
    # CRITICAL FIX: The input schema must be defined as a NESTED class 
    # for the @tool decorator to automatically recognize it in this syntax.
    class MarkdownGeneratorToolSchema(BaseModel):
        """Input schema for the Markdown Generator Tool."""
        report_content: str = Field(description="The full text content of the final report, ready for formatting.")
        file_name: str = Field(description="The desired output file name (e.g., 'Final_Investment_Report.md').")
    
    # NOTE: This implementation writes to the local file system where the crew is running.
    try:
        # Write the content to the specified file name
        with open(file_name, "w") as f:
            f.write(report_content)
        
        # Confirmation message for the LLM
        lines = report_content.count('\n') + 1
        return f"SUCCESS: Generated final report '{file_name}' ({lines} lines of content) and saved it in clean Markdown format."
        
    except Exception as e:
        return f"ERROR generating Markdown file: {e}"