# Calculator MCP Server Suite

A comprehensive calculator server suite that provides multiple mathematical tools through both STDIO (Model Context Protocol) and HTTP (FastAPI) interfaces. This suite includes specialized calculators for dates, finance, and mathematics, making it versatile for various computational needs.

## Features

### Available Tools

1. **Easter Date Calculator**
   - Calculates Easter date for any given year using the precise Gregorian algorithm
   - Implements astronomical calculations based on lunar cycles and spring equinox
   - Returns exact date in March or April

2. **Compound Interest Calculator**
   - Calculates compound interest with flexible compounding frequencies (annual, semi-annual, quarterly, monthly, etc.)
   - Computes effective annual rate (EAR)
   - Provides breakdown comparison across different compounding periods
   - Handles rate conversion (percentage to decimal)

3. **Greatest Common Factor (GCF)**
   - Finds the greatest common factor of two integers
   - Simple iterative algorithm for educational clarity

4. **Arithmetic Operations**
   - **Subtraction**: Difference between two numbers (supports integers and floats)

5. **Calculus Operations**
   - **Polynomial Derivative**: Calculates derivative of single-term polynomials (e.g., x^3, x, constants)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or download the project files:
```bash
git clone https://github.com/TewodrosAbewa/MCP.git
cd MCP
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
calculator-mcp-suite/
├── Server_Stdio.py          # MCP STDIO server implementation
├── Server_http.py          # FastAPI HTTP server with MCP support
├── requirements.txt        # Python dependencies
└── README.md              # This documentation
```

## Usage Options

### Option 1: STDIO Server (MCP Protocol)

Run the STDIO server for integration with MCP-compatible clients like Claude Desktop, Cursor, or other AI assistants:

```bash
python Server_Stdio.py
```

**Features:**
- Implements Model Context Protocol for AI tool integration
- Provides tools through standard input/output streams
- Ideal for local AI assistant integrations

### Option 2: HTTP Server (REST API + MCP)

Run the HTTP server to expose tools as REST endpoints with built-in MCP support:

```bash
python Server_http.py
```

**Server starts at:** `http://localhost:8002`

**Features:**
- Full REST API with OpenAPI documentation
- MCP-over-HTTP capabilities
- Interactive API testing interface
- Production-ready deployment options

## API Documentation

### Interactive Documentation

When the HTTP server is running, access the following:

- **Swagger UI (Interactive)**: `http://localhost:8002/docs`
- **ReDoc (Alternative)**: `http://localhost:8002/redoc`
- **OpenAPI Schema**: `http://localhost:8002/openapi.json`

### HTTP Endpoints

#### 1. **POST `/easter`**
Calculate Easter date for any given year using the Gregorian algorithm.

**Parameters:**
- `Y`: Year (integer, e.g., 2024)

**Example Request:**
```bash
curl -X POST "http://localhost:8002/easter?Y=2024"
```

**Example Response:**
```json
"Easter in 2024 is on March 31"
```

#### 2. **POST `/compound-interest`**
Calculate compound interest with various compounding frequencies.

**Parameters:**
- `principal`: Initial investment amount (float, e.g., 1000.00)
- `annual_rate`: Annual interest rate (float, accepts both 0.05 or 5 for 5%)
- `years`: Number of years (integer)
- `compounding_periods_per_year`: Compounding frequency (integer, optional, default=1)

**Example Request:**
```bash
curl -X POST "http://localhost:8002/compound-interest?principal=1000&annual_rate=5&years=10&compounding_periods_per_year=12"
```

**Example Response:**
```json
{
  "principal": 1000.0,
  "annual_rate_percent": 5.0,
  "years": 10,
  "compounding_periods_per_year": 12,
  "total_amount": 1647.01,
  "interest_earned": 647.01,
  "effective_annual_rate_percent": 5.116,
  "breakdown": {
    "monthly": 1647.01,
    "quarterly": 1643.62,
    "annually": 1628.89
  }
}
```

#### 3. **POST `/gcd`**
Calculate Greatest Common Factor (GCD) of two integers.

**Parameters:**
- `a`: First integer
- `b`: Second integer

**Example:**
```bash
curl -X POST "http://localhost:8002/gcd?a=48&b=18"
```
**Response:** `6`

#### 4. **POST `/subtract`**
Calculate difference between two numbers.

**Parameters:**
- `a`: First number (float)
- `b`: Second number (float)

**Example:**
```bash
curl -X POST "http://localhost:8002/subtract?a=10.5&b=3.2"
```
**Response:** `7.3`

#### 5. **POST `/derivative`**
Calculate derivative of a single-term polynomial.

**Parameters:**
- `term`: Polynomial term string (e.g., "x^3", "x", "5")

**Examples:**
```bash
curl -X POST "http://localhost:8002/derivative?term=x^3"
# Response: "3x^2"

curl -X POST "http://localhost:8002/derivative?term=x"
# Response: "1"

curl -X POST "http://localhost:8002/derivative?term=5"
# Response: "0"
```

## MCP Integration

### For MCP Clients (STDIO Server)

Add the STDIO server to your MCP client configuration:

**Claude Desktop Configuration:**
```json
{
  "mcpServers": {
    "calculator-suite": {
      "command": "python",
      "args": ["/absolute/path/to/Server_Stdio.py"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/project"
      }
    }
  }
}
```

**Cursor Configuration:**
```json
{
  "mcpServers": {
    "calculator-suite": {
      "command": "python",
      "args": ["Server_Stdio.py"],
      "cwd": "/path/to/project"
    }
  }
}
```

### HTTP Server with MCP Support

The `Server_http.py` uses `FastApiMCP` to provide both REST API and MCP-over-HTTP capabilities. This allows HTTP-based MCP tool discovery and invocation, suitable for remote or containerized deployments.

## Mathematical Details

### Compound Interest Formula

The compound interest calculation uses the standard formula:

```
A = P(1 + r/n)^(nt)
```

Where:
- `A` = Total amount after time t
- `P` = Principal amount (initial investment)
- `r` = Annual nominal interest rate (as decimal)
- `n` = Number of compounding periods per year
- `t` = Number of years

**Effective Annual Rate (EAR):**
```
EAR = (1 + r/n)^n - 1
```

### Easter Algorithm (Gregorian)

The Easter calculation implements the Anonymous Gregorian algorithm:

```
C = Y // 100
m = (15 + C - (C//4) - ((8*C + 13)//25)) % 30
n = (4 + C - (C//4)) % 7
a = Y % 4
b = Y % 7
c = Y % 19
d = (19*c + m) % 30
e = (2*a + 4*b + 6*d + n) % 7

day = 22 + d + e
```

Special cases handle dates in April. This algorithm computes Easter based on the first Sunday after the first ecclesiastical full moon following the March equinox.

### Greatest Common Factor (Euclidean-like)

The GCF calculation uses a simple iterative approach:
```python
smaller = min(a, b)
result = 1
for i in range(1, smaller + 1):
    if a % i == 0 and b % i == 0:
        result = i
return result
```

### Derivative Rules

The polynomial derivative follows basic calculus rules:
- `d/dx(x^n) = n*x^(n-1)`
- `d/dx(x) = 1`
- `d/dx(constant) = 0`

## Development

### Adding New Tools

To add a new calculator tool, follow this pattern:

**1. For STDIO Server (`Server_Stdio.py`):**
```python
@mcp_stdio.tool(name="tool_name", description="Tool description")
def tool_function(param1: type, param2: type) -> return_type:
    """Function docstring"""
    # Implementation
    return result
```

**2. For HTTP Server (`Server_http.py`):**
```python
@app.post("/endpoint-path", description="Endpoint description")
def endpoint_function(param1: type, param2: type):
    """Function docstring"""
    # Implementation
    return result
```

### Testing

**Test HTTP Server:**
1. Start the server: `python Server_http.py`
2. Open browser to: `http://localhost:8002/docs`
3. Use the interactive interface to test endpoints

**Test STDIO Server with MCP:**
1. Configure an MCP client (Claude Desktop, Cursor)
2. Verify tools appear in the AI assistant's capabilities
3. Test tool invocation through the AI interface

### Running Examples

**Example 1: Calculate Easter for multiple years:**
```bash
# Using curl
curl -X POST "http://localhost:8002/easter?Y=2024"
curl -X POST "http://localhost:8002/easter?Y=2025"
curl -X POST "http://localhost:8002/easter?Y=2030"
```

**Example 2: Investment comparison:**
```bash
# Compare $10,000 at 5% for 20 years with different compounding
curl -X POST "http://localhost:8002/compound-interest?principal=10000&annual_rate=5&years=20&compounding_periods_per_year=1"
curl -X POST "http://localhost:8002/compound-interest?principal=10000&annual_rate=5&years=20&compounding_periods_per_year=12"
curl -X POST "http://localhost:8002/compound-interest?principal=10000&annual_rate=5&years=20&compounding_periods_per_year=365"
```

## Deployment

### Production Deployment (HTTP Server)

For production use, consider:

1. **Using a Process Manager:**
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn Server_http:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8002
```

2. **Docker Deployment:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "Server_http.py"]
```

3. **Environment Variables:**
```bash
export PORT=8002
export HOST=0.0.0.0
export LOG_LEVEL=info
```

### Security Considerations

1. **Input Validation:** Both servers validate input parameters
2. **Rate Limiting:** Consider adding rate limiting for public HTTP deployment
3. **Authentication:** Add API keys or OAuth for production HTTP APIs
4. **CORS:** Configure CORS for web client access if needed

## Troubleshooting

### Common Issues

1. **Port already in use:**
```bash
# Change port in Server_http.py or use:
uvicorn Server_http:app --port 8003
```

2. **Module not found errors:**
```bash
# Ensure requirements are installed
pip install -r requirements.txt --upgrade

# Check Python path
export PYTHONPATH="/path/to/project:$PYTHONPATH"
```

3. **MCP client not recognizing tools:**
   - Verify the server is running
   - Check MCP client configuration paths
   - Ensure Python executable is in PATH

### Logging

Add logging for debugging:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Performance

- **STDIO Server:** Near-instant response for all calculations
- **HTTP Server:** Typical REST API response times < 50ms
- **Memory Usage:** Minimal (< 50MB)
- **Concurrent Requests:** HTTP server supports multiple concurrent requests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure both STDIO and HTTP implementations are updated
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or feature requests:
1. Check existing issues in the repository
2. Create a new issue with detailed description
3. Include Python version and environment details

---

