import warnings
from finance.crew import Finance
from dotenv import load_dotenv
import os
import json
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

load_dotenv()  
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["AV_API_KEY"]= os.getenv("AV_API_KEY")
os.environ["GOOGLE_API_KEY"]= os.getenv("GOOGLE_API_KEY")
os.environ["SERPER_API_KEY"]= os.getenv("SERPER_API_KEY")  # Make sure this is set!

def validate_output_files():
    """Validate that output files contain expected content."""
    output_dir = "output"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✓ Created output directory: {output_dir}")
    
    # Check for required output files
    required_files = [
        'compliance_report.md',
        'market_research_report.md',
        'quantitative_stock_filtering_report.md',
        'risk_assessment_report.md',
        'portfolio_allocation_report.md',
        'final_report.md'
    ]
    
    print("\n=== OUTPUT FILE VALIDATION ===")
    for file in required_files:
        filepath = os.path.join(output_dir, file)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✓ {file}: {size} bytes")
            
            # Validate content
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content.strip()) < 100:
                    print(f"  ⚠️  WARNING: File appears too short (< 100 chars)")
        else:
            print(f"✗ {file}: NOT FOUND")


def run():
    """
    Run the financial analysis crew with enhanced input validation.
    """
    
    # Enhanced prompt with clearer structure
    prompt = """
    **Investment Profile:**
    
    - **Total Capital:** $1,000,000 USD
    - **Investment Timeline:** 15 years (long-term)
    - **Dollar-Cost Averaging:** $333,333 per year for first 3 years
    - **Risk Tolerance:** Moderate to High (7/10)
    
    **Investment Goals:**
    - Primary: Aggressive wealth accumulation through capital appreciation
    - Secondary: Some dividend income generation
    - Balance between growth and stability
    
    **Sector Preferences:**
    - Technology (AI/Machine Learning companies)
    - Semiconductors
    - Partial allocation to broad market ETFs for stability
    
    **Investment Strategy:**
    - Growth-focused portfolio with some defensive positions
    - Willing to accept higher volatility for long-term gains
    - Want exposure to innovative tech leaders
    - Interested in both established giants and emerging leaders
    
    **Specific Requirements:**
    - Must include detailed risk analysis for each recommendation
    - Provide specific stock tickers and allocation percentages
    - Justify each selection with quantitative metrics
    - Consider current market conditions and economic factors
    """
    
    inputs = {
        'goal': prompt,
    }
    
    print("\n" + "="*80)
    print("🚀 STARTING FINANCIAL ANALYSIS CREW")
    print("="*80)
    print(f"\n📋 Client Goal Summary:")
    print(f"   • Capital: $1,000,000")
    print(f"   • Timeline: 15 years")
    print(f"   • Risk: Moderate-High (7/10)")
    print(f"   • Focus: Technology, AI, Semiconductors + ETFs")
    print("\n" + "="*80 + "\n")

    try:
        # Create and run the crew
        result = Finance().crew().kickoff(inputs=inputs)
        
        print("\n\n" + "="*80)
        print("✅ CREW EXECUTION COMPLETED")
        print("="*80)
        
        # Validate outputs
        validate_output_files()
        
        print("\n\n" + "="*80)
        print("📊 FINAL INVESTMENT RECOMMENDATION REPORT")
        print("="*80 + "\n")
        
        # Print the final result
        if hasattr(result, 'raw'):
            print(result.raw)
        else:
            print(str(result))
        
        print("\n\n" + "="*80)
        print("💾 Output files have been saved to the 'output/' directory")
        print("="*80)
        
        # Additional validation for final report
        final_report_path = "output/final_report.md"
        if os.path.exists(final_report_path):
            with open(final_report_path, 'r', encoding='utf-8') as f:
                final_content = f.read()
                
            # Check for critical sections
            required_sections = [
                "Executive Summary",
                "Strategic Rationale",
                "Portfolio Recommendation",
                "Security Justifications"
            ]
            
            print("\n=== FINAL REPORT CONTENT VALIDATION ===")
            for section in required_sections:
                if section in final_content:
                    print(f"✓ {section}: FOUND")
                else:
                    print(f"✗ {section}: MISSING")
            
            # Check for table
            if "|" in final_content and "Ticker" in final_content:
                print("✓ Allocation Table: FOUND")
            else:
                print("✗ Allocation Table: MISSING")
                
            print(f"\n📏 Total Report Length: {len(final_content)} characters")
            
        return result
        
    except Exception as e:
        print("\n\n" + "="*80)
        print("❌ ERROR DURING CREW EXECUTION")
        print("="*80)
        print(f"\nError details: {str(e)}")
        print("\nPlease check:")
        print("  1. All API keys are set correctly in .env")
        print("  2. Required packages are installed")
        print("  3. Internet connection is stable")
        print("  4. API rate limits haven't been exceeded")
        raise


if __name__ == "__main__":
    run()
