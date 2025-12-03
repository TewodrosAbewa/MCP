from fastmcp import FastMCP
from typing import Optional, List

mcp_stdio = FastMCP(name="Calculator Suite")

@mcp_stdio.tool(name="calculate_easter", description="Calculate Easter date for a given year using Gregorian algorithm")
def get_easter(Y: int) -> str:
    """Calculate Easter date for a given year"""
    C = Y // 100
    m = (15 + C - (C // 4) - ((8 * C + 13) // 25)) % 30
    n = (4 + C - (C // 4)) % 7
    a = Y % 4
    b = Y % 7
    c = Y % 19
    d = (19 * c + m) % 30
    e = (2 * a + 4 * b + 6 * d + n) % 7

    if d == 26 and e == 6:
        return f"Easter in {Y} is on April 19"
    if d == 28 and e == 6 and m in {2, 5, 10, 13, 16, 21, 24, 39}:
        return f"Easter in {Y} is on April 18"

    day = 22 + d + e
    if day <= 31:
        return f"Easter in {Y} is on March {day}"
    else:
        return f"Easter in {Y} is on April {day - 31}"

@mcp_stdio.tool(name="calculate_compound_interest", description="Calculate compound interest with various compounding frequencies")
def calculate_compound_interest(
    principal: float,
    annual_rate: float,
    years: int,
    compounding_periods_per_year: Optional[int] = 1
) -> str:
    """
    Calculate compound interest and total amount.
    
    Args:
        principal: Initial investment amount
        annual_rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
        years: Number of years
        compounding_periods_per_year: How many times interest is compounded per year (default: 1)
    
    Returns:
        String with detailed calculation results
    """
    if compounding_periods_per_year <= 0:
        return "Error: Compounding periods must be greater than 0"
    
    if years < 0:
        return "Error: Years must be non-negative"
    
    # Convert rate to decimal if it looks like a percentage (e.g., 5 instead of 0.05)
    if annual_rate > 1:
        annual_rate = annual_rate / 100
    
    # Calculate compound interest
    rate_per_period = annual_rate / compounding_periods_per_year
    total_periods = compounding_periods_per_year * years
    
    # A = P(1 + r/n)^(nt)
    total_amount = principal * (1 + rate_per_period) ** total_periods
    interest_earned = total_amount - principal
    
    # Format results
    result = f"""
    Compound Interest Calculation:
    ──────────────────────────────
    Principal: ${principal:,.2f}
    Annual Rate: {annual_rate*100:.2f}%
    Years: {years}
    Compounding Frequency: {compounding_periods_per_year} times per year
    
    Results:
    • Total Amount: ${total_amount:,.2f}
    • Interest Earned: ${interest_earned:,.2f}
    • Effective Annual Rate: {((1 + rate_per_period) ** compounding_periods_per_year - 1)*100:.3f}%
    
    Breakdown:
    - Monthly (n=12): ${principal * (1 + annual_rate/12) ** (12*years):,.2f}
    - Quarterly (n=4): ${principal * (1 + annual_rate/4) ** (4*years):,.2f}
    - Annually (n=1): ${principal * (1 + annual_rate) ** years:,.2f}
    """

    return result

@mcp_stdio.tool()
def calculate_scores(scores: List[float]):
    """
    Accepts a list of scores and returns the number of A's and the average.
    """
    valid_scores = [s for s in scores if 0 <= s <= 100]

    if not valid_scores:
        return {"num_as": 0, "average": 0, "message": "No valid scores entered"}

    num_as = sum(1 for s in valid_scores if s >= 90)
    average = sum(valid_scores) / len(valid_scores)

    return {
        "num_as": num_as,
        "average": average
    }


if __name__ == "__main__":
    mcp_stdio.run()