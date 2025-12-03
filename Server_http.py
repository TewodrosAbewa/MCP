from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from typing import Optional

app = FastAPI(title="Calculator API Suite")

@app.post("/easter", description="Calculate Easter date for a given year using Gregorian algorithm")
def get_easter(Y: int):
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

@app.post("/compound-interest", description="Calculate compound interest with various compounding frequencies")
def calculate_compound_interest(
    principal: float,
    annual_rate: float,
    years: int,
    compounding_periods_per_year: Optional[int] = 1
):
    """
    Calculate compound interest and total amount.
    
    Args:
        principal: Initial investment amount
        annual_rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
        years: Number of years
        compounding_periods_per_year: How many times interest is compounded per year
    
    Returns:
        Dictionary with calculation results
    """
    if compounding_periods_per_year <= 0:
        raise HTTPException(status_code=400, detail="Compounding periods must be greater than 0")
    
    if years < 0:
        raise HTTPException(status_code=400, detail="Years must be non-negative")
    
    # Convert rate to decimal if it looks like a percentage
    if annual_rate > 1:
        annual_rate = annual_rate / 100
    
    # Calculate compound interest
    rate_per_period = annual_rate / compounding_periods_per_year
    total_periods = compounding_periods_per_year * years
    
    total_amount = principal * (1 + rate_per_period) ** total_periods
    interest_earned = total_amount - principal
    effective_annual_rate = ((1 + rate_per_period) ** compounding_periods_per_year - 1) * 100
    
    return {
        "principal": principal,
        "annual_rate_percent": annual_rate * 100,
        "years": years,
        "compounding_periods_per_year": compounding_periods_per_year,
        "total_amount": round(total_amount, 2),
        "interest_earned": round(interest_earned, 2),
        "effective_annual_rate_percent": round(effective_annual_rate, 3),
        "breakdown": {
            "monthly": round(principal * (1 + annual_rate/12) ** (12*years), 2),
            "quarterly": round(principal * (1 + annual_rate/4) ** (4*years), 2),
            "annually": round(principal * (1 + annual_rate) ** years, 2)
        }
    }

@app.post("/gcd", description="Calculate Greatest Common Factor of two integers")
def gcd(a: int, b: int) -> int:
    """Calculate Greatest Common Factor (GCD) of two integers"""
    smaller = min(a, b)
    result = 1
    
    for i in range(1, smaller + 1):
        if a % i == 0 and b % i == 0:
            result = i

    return result

@app.post("/subtract", description="Calculate difference between two numbers")
def subtract(a: float, b: float) -> float:
    """Difference of two numbers"""
    return a - b

@app.post("/derivative", description="Calculate derivative of a single-term polynomial")
def derivative(term: str):
    """
    Calculate the derivative of a single-term polynomial like x^n.
    
    Args:
        term: string, e.g., "x^3", "x", or a constant like "5"
    
    Returns:
        String representing the derivative
    """
    term = term.strip()
    
    if '^' in term:
        base, exponent = term.split('^')
        exponent = int(exponent)
        return f"{exponent}x^{exponent - 1}"
    elif term == 'x':
        return "1"
    else:
        return "0"


# Initialize MCP integration
mcp = FastApiMCP(app, name="Calculator MCP")
mcp.mount_http()

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8002)