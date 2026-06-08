# Onion Trader — CLI Commands Reference Guide

**Quick Start for Production Testing**

---

## Setup & Activation

### 1. Navigate to Project
```bash
cd "/Users/aditya1981/Onion Trader"
```

### 2. Activate Virtual Environment
```bash
source .venv/bin/activate
```

### 3. Verify Setup
```bash
python cli.py status
```

Output:
```
Trading bot is ready.
```

---

## Account Management Commands

### Get Current Account Balance
```bash
python cli.py account-info
```

**Output:**
```
│ Asset        │ Wallet Balance │ Unrealized PnL │
├──────────────┼────────────────┼────────────────┤
│ USDT         │ 4999.95        │ 0.00           │
│ BTC          │ 0.001          │ 125.50         │
│ ETH          │ 0.1            │ 45.75          │
└──────────────┴────────────────┴────────────────┘
```

### Get Account Info with Debug Logging
```bash
python cli.py --verbose account-info
```

---

## Market Order Commands

### Market Buy Order
```bash
# Buy 0.001 BTC at market price
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**What Happens:**
1. Validates symbol, side, type, quantity
2. Calculates confidence score
3. Displays confidence analysis
4. Executes order at market price
5. Captures order ID and status
6. Logs to `logs/trading.log`
7. Saves to `logs/orders_history.json`

**Example Output:**
```
Confidence Score: A (91)
- Volatility: 90/100
- Order Book Depth: 100/100
- Price Proximity: 80/100
Recommendation: Excellent conditions to place order

Order placed successfully!
Order ID: 14507218573
Status: NEW
```

### Market Sell Order
```bash
# Sell 0.001 BTC at market price
python cli.py place-order --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

### Market Order with Verbose Output
```bash
python cli.py --verbose place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

Shows all HTTP requests, signatures, and API responses.

---

## Limit Order Commands

### Limit Buy Order (Below Market)
```bash
# Buy 0.001 BTC at $62,000 limit price
python cli.py place-order --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 62000
```

**Features:**
- Creates Good Till Cancelled (GTC) order
- Order remains active until executed or cancelled
- Can set limit price below market
- Good for cost averaging

### Limit Sell Order (Above Market)
```bash
# Sell 0.001 BTC at $65,000 limit price
python cli.py place-order --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 65000
```

**Features:**
- Profit-taking orders
- Set limit price above market
- Triggers when price reaches limit

### Calculate Limit Price (2% Below Market)
```bash
# Get order book and calculate 2% discount
python cli.py --verbose place-order --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 62640.77
```

Current market: ~$63,919  
2% discount: ~$62,641

---

## Testing Commands

### Dry-Run Mode (Validate Without Executing)
```bash
# Test order validation without actually placing it
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --dry-run
```

**Use Cases:**
- Test order parameters
- Verify confidence scoring
- Check validation logic
- No actual orders placed

**Output:**
```
[DRY RUN] Order NOT submitted.
Validation: PASSED
Confidence Score: A (91)
```

### Debug Mode with Verbose Output
```bash
python cli.py --verbose place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

Shows:
- HTTP requests and signatures
- API responses
- Confidence scoring breakdown
- Order parameters
- Execution time

### Combined: Dry-Run + Verbose
```bash
python cli.py --verbose place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --dry-run
```

Perfect for testing and debugging without placing orders.

---

## Advanced Commands

### Start API Server (FastAPI)
```bash
# Start server on localhost:8000
python cli.py serve
```

Visit: http://localhost:8000/docs

### Start Server with Custom Port
```bash
python cli.py serve --port 9000
```

### Start Server with Auto-Reload (Development)
```bash
python cli.py serve --reload
```

### Start Server on All Interfaces
```bash
python cli.py serve --host 0.0.0.0 --port 8000
```

---

## Order Examples by Symbol

### Bitcoin (BTC)
```bash
# Market buy 0.001 BTC
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Limit buy 0.001 BTC at $60,000
python cli.py place-order --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 60000
```

### Ethereum (ETH)
```bash
# Market buy 0.1 ETH
python cli.py place-order --symbol ETHUSDT --side BUY --type MARKET --quantity 0.1

# Limit sell 0.1 ETH at $2,500
python cli.py place-order --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 2500
```

### Binance Coin (BNB)
```bash
# Market buy 1 BNB
python cli.py place-order --symbol BNBUSDT --side BUY --type MARKET --quantity 1

# Limit buy 1 BNB at $600
python cli.py place-order --symbol BNBUSDT --side BUY --type LIMIT --quantity 1 --price 600
```

---

## Complete Test Execution

### Run Full Test Suite
```bash
# Activate venv first
source .venv/bin/activate

# Run all tests
cd /Users/aditya1981/Onion\ Trader
/Users/aditya1981/Onion\ Trader/.venv/bin/python3 direct_test.py
```

**Tests Executed:**
1. Environment verification
2. Dependency check
3. Binance connectivity
4. Account info retrieval
5. Market buy order
6. Market sell order
7. Limit buy order
8. Limit sell order

**Output:**
```
================================================================================
VALIDATION SUMMARY
================================================================================
Environment:   ✅ PASS
Dependencies:  ✅ PASS
Connectivity:  ✅ PASS
Account Info:  ✅ PASS
Order Tests:   4/4 PASSED
================================================================================
🎉 ALL TESTS PASSED - Bot is production-ready for testnet trading!
```

---

## Monitoring & Logs

### View Live Application Log
```bash
tail -f logs/trading.log
```

### View JSON-Formatted Log
```bash
cat logs/trading.log | jq '.'
```

### View Order History
```bash
cat logs/orders_history.json | jq '.'
```

### View Recent Orders
```bash
cat logs/orders_history.json | jq '.[-5:]'  # Last 5 orders
```

### Watch Log Updates in Real-Time
```bash
# Using watch command
watch -n 1 'tail -20 logs/trading.log'

# Or using tail
tail -f logs/trading.log | grep -E "Request|Response|Order"
```

---

## Common Use Cases

### Scenario 1: Quick Market Buy
```bash
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Scenario 2: Test Order First, Then Execute
```bash
# Step 1: Dry-run to validate
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --dry-run

# Step 2: Execute for real
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Scenario 3: Debug Order Placement
```bash
# Get detailed output including all API calls
python cli.py --verbose place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Scenario 4: Check Account Before Trading
```bash
# View current balances
python cli.py account-info

# View debug info
python cli.py --verbose account-info
```

### Scenario 5: Set Limit Orders at Market ±2%
```bash
# Market mid price: ~$63,919
# Buy 2% below market
python cli.py place-order --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 62640.77

# Sell 2% above market
python cli.py place-order --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 65197.53
```

---

## Troubleshooting

### Command Not Found
**Problem:** `python: command not found`  
**Solution:** Use full path to Python in venv
```bash
/Users/aditya1981/Onion\ Trader/.venv/bin/python3 cli.py account-info
```

### API Key Invalid
**Problem:** `Binance API error: 401 Unauthorized`  
**Solution:** Check `.env` file
```bash
cat .env
# Verify BINANCE_API_KEY and BINANCE_SECRET_KEY are set
```

### Testnet Connection Failed
**Problem:** `Network error during GET /fapi/v1/time`  
**Solution:** Check internet connection and BASE_URL
```bash
curl https://testnet.binancefuture.com/fapi/v1/time
```

### Order Validation Error
**Problem:** `symbol must end with USDT or BUSD`  
**Solution:** Use correct symbol format
```bash
# ❌ Wrong
python cli.py place-order --symbol BTC ...

# ✅ Correct
python cli.py place-order --symbol BTCUSDT ...
```

### Missing Price for Limit Order
**Problem:** `price is required for LIMIT orders`  
**Solution:** Add `--price` parameter
```bash
python cli.py place-order --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 60000
```

---

## Performance Tips

### For Fast Execution
```bash
# No verbose output (faster)
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### For Detailed Debugging
```bash
# With verbose output (slower but informative)
python cli.py --verbose place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Batch Operations
```bash
# Place multiple orders
for i in {1..5}; do
    python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --dry-run
done
```

---

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `BINANCE_API_KEY` | API key for authentication | `uQh6U8zOynmUbC5I80YZ4...` |
| `BINANCE_SECRET_KEY` | Secret for request signing | `UORLRdewtLKRit4fij72eL...` |
| `BASE_URL` | Binance endpoint | `https://testnet.binancefuture.com` |

All set in `.env` file (loaded automatically).

---

## Quick Reference Cheat Sheet

```bash
# Account
python cli.py account-info

# Market Buy
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Market Sell
python cli.py place-order --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001

# Limit Buy
python cli.py place-order --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 60000

# Limit Sell
python cli.py place-order --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000

# Dry Run (no execution)
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --dry-run

# Debug Mode
python cli.py --verbose place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Server
python cli.py serve

# Status
python cli.py status

# View Logs
tail -f logs/trading.log
```

---

## Support & Documentation

### Project Files
- `README.md` — Project overview
- `cli.py` — CLI interface code
- `bot/client.py` — Binance API client
- `bot/orders.py` — Order management
- `bot/confidence.py` — Confidence scoring
- `bot/validators.py` — Input validation

### Test Evidence
- `TEST_RESULTS.md` — Detailed test results
- `PRODUCTION_TEST_EVIDENCE.md` — Complete validation report

### Logs
- `logs/trading.log` — Main application log
- `logs/orders_history.json` — Order history

---

**Last Updated:** June 8, 2026  
**Status:** ✅ Production Ready  
**Version:** 1.0

