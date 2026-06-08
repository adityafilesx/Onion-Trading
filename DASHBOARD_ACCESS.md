# 🎨 Trading Dashboard — Access & Setup Guide

**Status:** ✅ Dashboard Server Running  
**URL:** http://127.0.0.1:8000  
**Mode:** Testnet (Binance Futures Testnet)

---

## 🚀 Quick Access

### Main Dashboard URL
```
http://127.0.0.1:8000
```

### API Endpoints
```
GET    http://127.0.0.1:8000/api/health           - Server health check
GET    http://127.0.0.1:8000/api/account          - Account information
GET    http://127.0.0.1:8000/api/account/balance  - Current balance
GET    http://127.0.0.1:8000/api/orders/history   - Order history
GET    http://127.0.0.1:8000/api/confidence       - Confidence scoring
POST   http://127.0.0.1:8000/api/orders           - Place new order
```

### Swagger API Documentation
```
http://127.0.0.1:8000/docs
```

---

## 📊 Dashboard Features

### Main Sections

#### 1. **Dashboard Overview**
- Total orders placed today
- Win rate analysis
- Last order status
- Average confidence score
- Recent activity log (real-time)

#### 2. **Execution Terminal**
- Place market orders
- Place limit orders
- Dry-run mode (test without executing)
- Confidence score visualization
- Live order book data
- Position sizing tools

#### 3. **Order History**
- Complete order execution history
- Timestamp and price information
- Confidence scores for each order
- Order status tracking
- P&L calculations

#### 4. **Confidence Analyzer**
- Real-time market analysis
- Volatility measurements
- Order book depth analysis
- Price proximity scoring
- Grade calculations (A/B/C/D)

---

## 🎯 How to Use the Dashboard

### Step 1: Open Dashboard
```
1. Open browser
2. Navigate to: http://127.0.0.1:8000
3. You'll see TradingBot Pro dashboard
```

### Step 2: Check Account Status
- Top right corner shows: **Account Balance**
- Display: Current USDT balance in testnet
- Updates in real-time from Binance API

### Step 3: Place a Market Order
```
1. Click "Place Order" in sidebar
2. Symbol: BTCUSDT (pre-filled)
3. Side: Select BUY or SELL
4. Type: MARKET (or LIMIT)
5. Quantity: 0.001 BTC
6. Dry Run: Toggle ON to test without executing
7. Click "PLACE ORDER"
```

### Step 4: View Confidence Score
- Real-time circular gauge shows:
  - Current confidence (0-100)
  - Grade (A/B/C/D)
  - Recommendation text
  - Market conditions breakdown

### Step 5: Monitor Orders
- Click "Order History"
- See all executed orders
- View timestamps, prices, confidence scores
- Check P&L for each trade

---

## 🔧 Dashboard Capabilities

### Real-Time Features
✅ Live account balance updates  
✅ Market data streaming  
✅ Order execution monitoring  
✅ Confidence score calculations  
✅ Activity log (auto-refresh)  

### Order Execution
✅ Market buy/sell  
✅ Limit buy/sell  
✅ Dry-run mode (practice)  
✅ Order history tracking  
✅ Execution status display  

### Analysis Tools
✅ Confidence scoring (A/B/C/D grades)  
✅ Volatility analysis  
✅ Order book depth visualization  
✅ Win rate calculation  
✅ Performance metrics  

### Security Features
✅ Testnet-only mode  
✅ CORS protection  
✅ Input validation  
✅ Error handling  
✅ Activity logging  

---

## 📱 Dashboard Layout

### Header (Top)
- Logo: TradingBot Pro
- Badge: TESTNET MODE (yellow)
- Account Balance: XXXX.XX USDT
- Quick actions: Wallet, Notifications, Settings

### Sidebar (Left - Desktop)
- Navigation menu
- Dashboard (active by default)
- Place Order
- Order History
- Confidence Analyzer
- Connect API button
- Support & Sign Out

### Main Content Area
- Page-specific content
- Charts and visualizations
- Forms and controls
- Real-time data tables

---

## 🎨 Dashboard Design

### Color Scheme
- **Primary:** Green (#00e479)
- **Secondary:** Red (#ff4444)
- **Background:** Dark (#0d1117)
- **Text:** Light gray (#dfe2eb)

### Typography
- Headlines: 32px bold
- Labels: 11px uppercase
- Data: 24px monospace
- Body: 14px regular

### Theme
- Dark mode (default)
- Modern glassmorphism design
- Tailwind CSS styling
- Material Design icons
- Smooth animations

---

## 🔌 Starting the Dashboard Server

### Method 1: Direct Command (Recommended)
```bash
cd /Users/aditya1981/Onion\ Trader
/Users/aditya1981/Onion\ Trader/.venv/bin/python3 -m uvicorn api.server:app --host 127.0.0.1 --port 8000
```

### Method 2: Using CLI
```bash
cd /Users/aditya1981/Onion\ Trader
source .venv/bin/activate
python cli.py serve
```

### Method 3: Custom Port
```bash
python -m uvicorn api.server:app --host 127.0.0.1 --port 9000
```

### Method 4: External Access
```bash
python -m uvicorn api.server:app --host 0.0.0.0 --port 8000
```

---

## ✅ Verify Server is Running

### Check Health Endpoint
```bash
curl http://127.0.0.1:8000/api/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "testnet": true,
  "server_time": 1780936000000
}
```

### Check Account
```bash
curl http://127.0.0.1:8000/api/account
```

**Expected Response:**
```json
{
  "assets": [
    {
      "asset": "USDT",
      "walletBalance": "4999.95",
      "unrealizedProfit": "0.00"
    }
  ],
  "totalWalletBalance": "4999.95",
  "totalUnrealizedProfit": "0.00"
}
```

---

## 📊 API Usage Examples

### Get Confidence Score
```bash
curl "http://127.0.0.1:8000/api/confidence?symbol=BTCUSDT&side=BUY&order_type=MARKET"
```

### Place Market Order
```bash
curl -X POST "http://127.0.0.1:8000/api/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTCUSDT",
    "side": "BUY",
    "order_type": "MARKET",
    "quantity": 0.001
  }'
```

### Get Order History
```bash
curl http://127.0.0.1:8000/api/orders/history
```

### Place Limit Order
```bash
curl -X POST "http://127.0.0.1:8000/api/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTCUSDT",
    "side": "BUY",
    "order_type": "LIMIT",
    "quantity": 0.001,
    "price": 62640.77
  }'
```

---

## 🔐 Security Notes

### Dashboard Security
- ✅ CORS enabled (all origins)
- ✅ Input validation on all endpoints
- ✅ Error handling for network issues
- ✅ Testnet-only (no mainnet data)
- ✅ API key in environment variables

### Best Practices
1. Keep server running only when needed
2. Don't expose to internet without authentication
3. Use environment variables for secrets
4. Monitor logs for errors
5. Test with dry-run first

---

## 🐛 Troubleshooting

### Dashboard Not Loading
```bash
# Check if server is running
curl http://127.0.0.1:8000/api/health

# If error, restart server
kill <process_id>
python -m uvicorn api.server:app --host 127.0.0.1 --port 8000
```

### API Requests Failing
```bash
# Check API logs
tail -f logs/trading.log

# Verify API keys in .env
cat .env

# Test connectivity
python cli.py account-info
```

### Orders Not Showing
```bash
# Check order history file
cat logs/orders_history.json | jq '.'

# Verify API connection
curl http://127.0.0.1:8000/api/account
```

### Confidence Score Not Updating
```bash
# Test confidence endpoint
curl "http://127.0.0.1:8000/api/confidence?symbol=BTCUSDT&side=BUY&order_type=MARKET"

# Check for API errors
tail -20 logs/trading.log
```

---

## 📈 Dashboard Workflow

### Typical Trading Session

```
1. Open Dashboard
   └─ http://127.0.0.1:8000

2. Verify Account
   └─ Check balance in top right
   └─ Go to Account menu

3. Analyze Market
   └─ Click "Confidence Analyzer"
   └─ Review confidence score
   └─ Check market conditions

4. Place Order (Dry-Run)
   └─ Click "Place Order"
   └─ Toggle "Dry Run" ON
   └─ Enter order parameters
   └─ Click "PLACE ORDER"
   └─ Review output

5. Execute Live Order (if satisfied)
   └─ Toggle "Dry Run" OFF
   └─ Click "PLACE ORDER"
   └─ Monitor in "Recent Activity"

6. Review History
   └─ Click "Order History"
   └─ See executed trades
   └─ Check confidence scores
```

---

## 🎯 Next Steps

### Immediate (Right Now)
1. ✅ Dashboard is running at http://127.0.0.1:8000
2. ✅ Open in browser
3. ✅ Check account balance
4. ✅ Test dry-run order

### Short Term (Today)
1. Execute a test market order
2. View order in history
3. Review confidence scoring
4. Test limit orders
5. Monitor real-time updates

### Medium Term (This Week)
1. Place multiple test orders
2. Track P&L performance
3. Test different symbols
4. Verify order execution
5. Document findings

---

## 📚 Resources

### Dashboard Files
- `static/index.html` - Web UI (756 lines)
- `api/server.py` - FastAPI backend
- `logs/trading.log` - Application logs

### API Documentation
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Related Documentation
- `README.md` - Project overview
- `CLI_COMMANDS_REFERENCE.md` - CLI commands
- `TEST_RESULTS.md` - Test results

---

## 🎉 Summary

### Dashboard is Live!
✅ **URL:** http://127.0.0.1:8000  
✅ **Status:** Running and ready  
✅ **Features:** Full trading interface  
✅ **Testnet:** Connected and verified  

### You Can Now:
✅ View real-time account balance  
✅ Place market orders  
✅ Place limit orders  
✅ Analyze confidence scores  
✅ View order history  
✅ Monitor market conditions  
✅ Use API endpoints  

### Quick Start:
1. Open: http://127.0.0.1:8000
2. Check balance in top right
3. Click "Place Order" in sidebar
4. Enter parameters and test with dry-run
5. Review results in order history

---

**Dashboard Status:** ✅ Live and Running  
**URL:** http://127.0.0.1:8000  
**API Docs:** http://127.0.0.1:8000/docs  
**Testnet:** Connected & Verified  

🚀 **Your trading dashboard is ready to use!**

