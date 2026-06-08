# TradingBot Pro - Setup & Launch Guide

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
cd "/Users/aditya1981/Onion Trader"

# Activate virtual environment
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Environment
Create or update `.env` file:
```bash
cat > .env << 'EOF'
BASE_URL=https://testnet.binancefuture.com
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_api_secret
EOF
```

### 3. Start the Backend Server
```bash
python3 -m uvicorn api.server:app --host 127.0.0.1 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 4. Open in Browser
Navigate to: **http://127.0.0.1:8000**

The complete frontend is now loaded with all pages!

---

## What's Included

✅ **Complete Multi-Page Dashboard**
- Dashboard with live data
- Place Order page with confidence scoring
- Order History with full details
- Confidence Analyzer

✅ **Full API Integration**
- Account balance fetching
- Order placement
- Order history retrieval
- Real-time confidence scoring

✅ **Professional UI/UX**
- Dark mode trading interface
- Responsive mobile design
- Smooth animations
- Real-time indicators

✅ **Advanced Features**
- Live market data updates (10s refresh)
- Confidence gauge with breakdown metrics
- Order status tracking
- Win rate calculation

---

## Navigation Guide

### Desktop
- **Left Sidebar**: Main navigation menu
- **Top Bar**: Account balance and settings
- **Active Link**: Highlighted in neon green

### Mobile
- **Bottom Navigation**: 4 main tabs
- **Full-Screen Pages**: Optimized layout
- **Touch-Friendly**: Large tap targets

### Pages

| Page | URL | Features |
|------|-----|----------|
| Dashboard | `/` | Account overview, live stats, activity log |
| Place Order | `/place-order` | Order form, confidence gauge, execution |
| Order History | `/order-history` | Order list, filters, export |
| Analyzer | `/confidence` | Signal analysis, detailed metrics |

---

## Testing the Frontend

### Test the Dashboard
1. Go to Dashboard page
2. See live account balance from API
3. View recent orders and statistics
4. Auto-refresh every 10 seconds

### Test Place Order
1. Go to Place Order page
2. Enter symbol (e.g., BTCUSDT)
3. Select BUY or SELL
4. Choose MARKET or LIMIT type
5. Enter quantity
6. Watch confidence score update in real-time
7. Click "PLACE ORDER"
8. See success modal with order details

### Test Order History
1. Go to Order History page
2. View all executed orders
3. See status, confidence, and details
4. Check auto-refresh indicator

### Test Analyzer
1. Go to Confidence Analyzer page
2. Change trading parameters
3. Click "ANALYZE SIGNAL"
4. View detailed breakdown and recommendations

---

## Troubleshooting

### Port 8000 Already in Use
```bash
# Find and kill process using port 8000
lsof -i :8000
kill -9 <PID>

# Or use a different port
python3 -m uvicorn api.server:app --host 127.0.0.1 --port 8001
```

### Module Not Found Errors
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### API Connection Errors
1. Verify backend is running (check console output)
2. Check browser console (F12) for error messages
3. Verify `.env` file has correct API credentials
4. Test API health: `curl http://127.0.0.1:8000/api/health`

### Frontend Not Updating
- Clear browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)
- Hard refresh (Ctrl+F5 or Cmd+Shift+R)
- Check browser console for JavaScript errors

---

## Key Features Explained

### Confidence Score
- **Score Range**: 0-100
- **Grade System**: A+ (90+), A (80+), B (70+), C (60+), D (50+), F (<50)
- **Recommendations**: Strong Buy, Buy, or Hold
- **Updated**: Every time you change order parameters

### Dashboard Stats
- **Total Orders**: Count of all executed orders today
- **Win Rate**: Percentage of profitable trades
- **Last Order Status**: Most recent order state
- **Confidence Score**: Average confidence of recent trades

### Order History
- **Status**: FILLED (complete), REJECTED (failed), NEW (pending)
- **Confidence %**: Score at time of order
- **Filters**: By symbol, side, status (extensible)
- **Export**: CSV download functionality

### Live Updates
- Dashboard refreshes every **10 seconds**
- Order history updates on page load
- Confidence recalculates on input change
- Auto-refresh indicator on Order History

---

## API Endpoints Reference

### Get Account Info
```bash
curl http://127.0.0.1:8000/api/account
```

### Get Order History
```bash
curl http://127.0.0.1:8000/api/orders/history
```

### Get Confidence Score
```bash
curl "http://127.0.0.1:8000/api/confidence?symbol=BTCUSDT&side=BUY&order_type=MARKET"
```

### Place Order
```bash
curl -X POST http://127.0.0.1:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTCUSDT",
    "side": "BUY",
    "order_type": "MARKET",
    "quantity": 0.001
  }'
```

### Health Check
```bash
curl http://127.0.0.1:8000/api/health
```

---

## File Changes Summary

### Created/Modified Files
- ✅ `/static/index.html` - Unified multi-page application
- ✅ `/static/app.js` - Complete JavaScript functionality
- ✅ `/FRONTEND_INTEGRATION.md` - Detailed documentation
- ✅ `/SETUP_GUIDE.md` - This guide

### Backend (No changes needed)
- API endpoints working as-is
- All validations in place
- Confidence scoring functional
- Order management operational

---

## Development Tips

### Add New Features
1. Add new page div in HTML (e.g., `<div id="new-page" class="page">`)
2. Add navigation link in sidebar
3. Add JavaScript function to handle page logic
4. Update `navigatePage()` to support new page

### Modify Styling
1. Tailwind classes are inline in HTML
2. Custom styles in `<style>` tag
3. Colors defined in tailwind config object
4. Responsive breakpoints: sm, md, lg

### Debug API Issues
1. Open browser DevTools (F12)
2. Go to Network tab
3. Make API call from UI
4. Check request/response in Network tab
5. Look for error messages in Console

### Check Logs
```bash
tail -f logs/trading.log
```

---

## Performance Tips

### Reduce API Calls
- Dashboard refresh is 10 seconds (adjustable in app.js)
- Order History loads on page visit
- Confidence updates on user input

### Optimize Frontend
- Page transitions use CSS animations
- Minimal DOM updates
- Event delegation for multiple elements
- Lazy loading of data

### Monitor Backend
- Check logs for slow queries
- Monitor API response times
- Verify Binance API rate limits

---

## Next Steps

1. ✅ Frontend fully integrated
2. ✅ API endpoints ready
3. ✅ Test with real/testnet account
4. ✅ Configure trading parameters
5. ⏭️ Set up automated trading bot (CLI)
6. ⏭️ Add WebSocket for real-time updates
7. ⏭️ Deploy to production server

---

## Support Resources

- **Backend Issues**: Check `/logs/trading.log`
- **Frontend Issues**: Check browser console (F12)
- **API Issues**: Review network requests in DevTools
- **Documentation**: See `FRONTEND_INTEGRATION.md`

---

**Version**: 2.5.0  
**Last Updated**: 2024  
**Status**: Ready to Use
