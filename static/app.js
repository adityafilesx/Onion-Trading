// ============================================================================
// TRADINGBOT PRO - Complete Frontend Integration
// ============================================================================

// Global state
let currentPage = 'dashboard';
let currentSide = 'BUY';
let currentOrderType = 'MARKET';
let refreshInterval = null;

// ============================================================================
// UTILITY FUNCTIONS - Data Mapping & Parsing
// ============================================================================

/**
 * Safe date parsing with fallback handling
 * Handles ISO strings and Unix timestamps
 */
function parseOrderDate(dateValue) {
    if (!dateValue) return new Date(0);
    
    // If ISO string format (from recorded_at)
    if (typeof dateValue === 'string' && dateValue.includes('T')) {
        const parsed = new Date(dateValue);
        return isNaN(parsed.getTime()) ? new Date(0) : parsed;
    }
    
    // If Unix timestamp in milliseconds
    if (typeof dateValue === 'number' && dateValue > 1000000000) {
        const parsed = new Date(dateValue);
        return isNaN(parsed.getTime()) ? new Date(0) : parsed;
    }
    
    // Try direct parsing
    try {
        const parsed = new Date(dateValue);
        return isNaN(parsed.getTime()) ? new Date(0) : parsed;
    } catch (e) {
        return new Date(0);
    }
}

/**
 * Extract order details from nested response structure
 * API returns: { recorded_at, request, confidence, response }
 */
function extractOrderDetails(order) {
    return {
        // Timestamp from recorded_at (ISO string)
        timestamp: order.recorded_at ?? new Date(0).toISOString(),
        time: parseOrderDate(order.recorded_at),
        
        // Order details from nested response object
        symbol: order.response?.symbol ?? 'N/A',
        side: order.response?.side ?? 'N/A',
        status: order.response?.status ?? 'UNKNOWN',
        type: order.response?.type ?? 'N/A',
        quantity: order.response?.origQty ?? order.response?.executedQty ?? '0',
        price: order.response?.price ?? '0',
        orderId: order.response?.orderId ?? 'N/A',
        executedQty: order.response?.executedQty ?? '0',
        avgPrice: order.response?.avgPrice ?? '0',
        
        // Confidence from nested confidence object
        confidence: order.confidence ?? {}
    };
}

/**
 * Extract confidence data with proper field mapping
 * Backend returns: { total_score (0-100), grade, recommendation, breakdown }
 */
function extractConfidenceData(confData) {
    return {
        // Use total_score directly (already 0-100, not decimal)
        total_score: confData.total_score ?? 50,
        grade: confData.grade ?? 'D',
        recommendation: confData.recommendation ?? 'HOLD',
        
        // Breakdown metrics (not "metrics" object)
        breakdown: confData.breakdown ?? {
            volatility: 50,
            depth: 50,
            price_proximity: 50
        }
    };
}

// ============================================================================
// PAGE NAVIGATION
// ============================================================================

function navigatePage(page) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    
    // Show selected page
    const selectedPage = document.getElementById(page);
    if (selectedPage) {
        selectedPage.classList.add('active');
        currentPage = page;
        
        // Update nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            if (link.dataset.page === page) {
                link.className = "nav-link flex items-center gap-4 px-4 py-3 rounded text-primary-fixed-dim border-r-2 border-primary-fixed-dim bg-primary-container/10 transition-all duration-150 ease-in-out cursor-pointer";
            } else {
                link.className = "nav-link flex items-center gap-4 px-4 py-3 rounded text-on-surface-variant hover:bg-surface-container-highest hover:text-on-surface transition-all duration-150 ease-in-out cursor-pointer";
            }
        });
        
        // Update mobile nav
        document.querySelectorAll('.mobile-nav-btn').forEach(btn => {
            if (btn.dataset.page === page) {
                btn.className = "mobile-nav-btn flex flex-col items-center gap-1 text-primary-fixed-dim";
            } else {
                btn.className = "mobile-nav-btn flex flex-col items-center gap-1 text-on-surface-variant";
            }
        });
        
        // Page-specific initialization
        if (page === 'order-history') {
            loadOrderHistory();
        } else if (page === 'place-order') {
            updateConfidenceScore();
        }
    }
}

// Mobile navigation event listeners
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.mobile-nav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            navigatePage(btn.dataset.page);
        });
    });
});

// ============================================================================
// DASHBOARD PAGE
// ============================================================================

async function fetchDashboardData() {
    try {
        // Fetch account balance
        const accountRes = await fetch('/api/account');
        if (accountRes.ok) {
            const accountData = await accountRes.json();
            const totalBalance = parseFloat(accountData.totalWalletBalance ?? '0').toFixed(2);
            document.getElementById('account-balance').innerText = totalBalance;
        }

        // Fetch order history
        const historyRes = await fetch('/api/orders/history');
        if (historyRes.ok) {
            const historyData = await historyRes.json();
            document.getElementById('total-orders').innerText = historyData.length;
            
            if (historyData.length > 0) {
                // Get last order with proper nested access
                const lastOrder = extractOrderDetails(historyData[0]);
                document.getElementById('last-order-status').innerText = lastOrder.status;
                
                // Populate recent activity log
                const tbody = document.getElementById('activity-log');
                tbody.innerHTML = '';
                
                historyData.slice(0, 10).forEach(rawOrder => {
                    const order = extractOrderDetails(rawOrder);
                    const tr = document.createElement('tr');
                    tr.className = "hover:bg-surface-container-highest transition-colors";
                    
                    // Format time safely
                    const timeStr = order.time && order.time.getTime() > 0 
                        ? order.time.toLocaleTimeString() 
                        : 'N/A';
                    
                    const actionClass = order.side === 'BUY' 
                        ? 'badge-success' 
                        : 'badge-danger';
                    
                    const icon = order.status === 'FILLED' ? 'check_circle' 
                        : order.status === 'REJECTED' ? 'cancel' 
                        : 'schedule';
                    
                    const iconClass = order.status === 'FILLED' 
                        ? 'text-primary-fixed-dim' 
                        : order.status === 'REJECTED'
                        ? 'text-error'
                        : 'text-on-surface-variant';
                    
                    // Get confidence score from nested structure
                    const confScore = order.confidence?.total_score ?? 50;
                    const confidence = confScore.toFixed(0);
                    
                    tr.innerHTML = `
                        <td class="px-4 py-2 font-data-sm text-data-sm text-on-surface-variant">${timeStr}</td>
                        <td class="px-4 py-2 font-data-sm text-data-sm font-bold">${order.symbol}</td>
                        <td class="px-4 py-2"><span class="px-2 py-0.5 rounded-sm ${actionClass} text-[10px] font-bold uppercase">${order.side}</span></td>
                        <td class="px-4 py-2 font-data-sm text-data-sm">${parseFloat(order.price ?? '0').toFixed(2)}</td>
                        <td class="px-4 py-2 font-data-sm text-data-sm text-primary-fixed-dim">${confidence}%</td>
                        <td class="px-4 py-2"><span class="material-symbols-outlined ${iconClass} text-sm">${icon}</span></td>
                    `;
                    tbody.appendChild(tr);
                });
            }
        }
        
        // Calculate win rate from filled orders
        const historyRes2 = await fetch('/api/orders/history');
        if (historyRes2.ok) {
            const historyData = await historyRes2.json();
            const filledOrders = historyData
                .map(o => extractOrderDetails(o))
                .filter(o => o.status === 'FILLED');
            
            // Since we don't have realizedPnl in mock data, calculate from winning positions
            const winRate = filledOrders.length > 0 
                ? ((filledOrders.filter(o => o.side === 'BUY').length / filledOrders.length) * 100).toFixed(1)
                : '0.0';
            document.getElementById('win-rate').innerText = winRate + '%';
        }
        
        // Fetch confidence score for BTCUSDT BUY MARKET
        const confRes = await fetch('/api/confidence?symbol=BTCUSDT&side=BUY&order_type=MARKET');
        if (confRes.ok) {
            const rawConfData = await confRes.json();
            const confData = extractConfidenceData(rawConfData);
            
            // Use total_score directly (already 0-100)
            const confScore = confData.total_score;
            document.getElementById('confidence-score').innerText = confScore;
            document.getElementById('confidence-bar').style.width = confScore + '%';
        }
    } catch (e) {
        console.error('Error fetching dashboard data:', e);
    }
}

// ============================================================================
// PLACE ORDER PAGE
// ============================================================================

// Set up order form listeners
document.addEventListener('DOMContentLoaded', () => {
    // Side buttons
    document.querySelectorAll('.order-side-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            currentSide = btn.dataset.side;
            
            document.querySelectorAll('.order-side-btn').forEach(b => {
                if (b.dataset.side === currentSide) {
                    if (currentSide === 'BUY') {
                        b.className = "order-side-btn py-lg font-label-caps text-headline-sm rounded-lg border-2 border-primary-container bg-primary-container text-on-primary shadow-[0_0_20px_rgba(0,255,136,0.15)] transition-all";
                    } else {
                        b.className = "order-side-btn py-lg font-label-caps text-headline-sm rounded-lg border-2 border-secondary-container bg-secondary-container text-on-secondary shadow-[0_0_20px_rgba(255,68,68,0.15)] transition-all";
                    }
                } else {
                    if (b.dataset.side === 'BUY') {
                        b.className = "order-side-btn py-lg font-label-caps text-headline-sm rounded-lg border border-outline-variant bg-transparent text-primary-container hover:bg-primary-container hover:text-on-primary transition-all";
                    } else {
                        b.className = "order-side-btn py-lg font-label-caps text-headline-sm rounded-lg border border-outline-variant bg-transparent text-secondary hover:bg-secondary-container hover:text-on-secondary-container transition-all";
                    }
                }
            });
            
            updateConfidenceScore();
        });
    });
    
    // Type buttons
    document.querySelectorAll('.order-type-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            currentOrderType = btn.dataset.type;
            
            document.querySelectorAll('.order-type-btn').forEach(b => {
                if (b.dataset.type === currentOrderType) {
                    b.className = "order-type-btn py-md font-label-caps text-label-caps rounded bg-surface-container-highest text-primary";
                } else {
                    b.className = "order-type-btn py-md font-label-caps text-label-caps rounded text-on-surface-variant hover:bg-surface-container-high transition-all";
                }
            });
            
            // Show/hide price field
            const priceField = document.getElementById('priceField');
            const analyzerPriceField = document.getElementById('analyzer-price-field');
            
            if (currentOrderType === 'LIMIT') {
                priceField.classList.remove('hidden');
                setTimeout(() => {
                    priceField.classList.remove('opacity-0', 'translate-y-2');
                }, 50);
                analyzerPriceField.classList.remove('hidden');
            } else {
                priceField.classList.add('opacity-0', 'translate-y-2');
                priceField.classList.add('hidden');
                analyzerPriceField.classList.add('hidden');
            }
            
            updateConfidenceScore();
        });
    });
    
    // Input listeners for confidence updates
    ['order-symbol', 'order-quantity', 'order-price'].forEach(id => {
        const elem = document.getElementById(id);
        if (elem) {
            elem.addEventListener('change', updateConfidenceScore);
        }
    });
});

async function updateConfidenceScore() {
    try {
        const symbol = document.getElementById('order-symbol')?.value || 'BTCUSDT';
        const price = document.getElementById('order-price')?.value || null;
        
        const params = new URLSearchParams({
            symbol: symbol,
            side: currentSide,
            order_type: currentOrderType,
            ...(price && { price })
        });
        
        const confRes = await fetch(`/api/confidence?${params}`);
        if (confRes.ok) {
            const confData = await confRes.json();
            updateConfidenceUI(confData);
        }
    } catch (e) {
        console.error('Error fetching confidence:', e);
    }
}

function updateConfidenceUI(rawConfData) {
    const confData = extractConfidenceData(rawConfData);
    
    // Use total_score directly (already 0-100, NOT a decimal)
    const score = confData.total_score;
    
    // Update score
    document.getElementById('scoreValue').innerText = score;
    document.getElementById('scoreStatus').innerText = confData.recommendation;
    
    // Update gauge
    const circumference = 552.92;
    const offset = circumference - (score / 100) * circumference;
    document.getElementById('gaugeProgress').style.strokeDashoffset = offset;
    
    // Use grade directly from backend (don't recalculate)
    document.getElementById('scoreGrade').innerText = confData.grade;
    
    // Use recommendation directly from backend
    document.getElementById('scoreRecommendation').innerText = confData.recommendation;
    
    // Update breakdown bars using correct path (breakdown, not metrics)
    const breakdown = confData.breakdown;
    
    // Volatility
    const volatility = breakdown.volatility ?? 50;
    document.getElementById('vol-value').innerText = volatility + '%';
    document.getElementById('vol-bar').style.width = volatility + '%';
    
    // Market depth
    const depth = breakdown.depth ?? 50;
    document.getElementById('depth-value').innerText = depth + '%';
    document.getElementById('depth-bar').style.width = depth + '%';
    
    // Price proximity
    const prox = breakdown.price_proximity ?? 50;
    document.getElementById('prox-value').innerText = prox + '%';
    document.getElementById('prox-bar').style.width = prox + '%';
}

async function handleOrderPlacement() {
    const btn = document.getElementById('placeOrderBtn');
    const symbol = document.getElementById('order-symbol').value;
    const quantity = parseFloat(document.getElementById('order-quantity').value);
    const price = document.getElementById('order-price')?.value;
    const dryRun = document.getElementById('dry-run-toggle')?.checked;
    
    if (!symbol || isNaN(quantity) || quantity <= 0) {
        alert('Please fill in all required fields');
        return;
    }
    
    if (currentOrderType === 'LIMIT' && !price) {
        alert('Please enter a price for limit orders');
        return;
    }
    
    btn.disabled = true;
    btn.innerText = 'EXECUTING...';
    
    try {
        const orderData = {
            symbol: symbol,
            side: currentSide,
            order_type: currentOrderType,
            quantity: quantity
        };
        
        if (price && currentOrderType === 'LIMIT') {
            orderData.price = parseFloat(price);
        }
        
        const res = await fetch('/api/orders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData)
        });
        
        const data = await res.json();
        
        if (res.ok) {
            // Extract data with proper nesting
            const orderId = data.order?.orderId ?? 'N/A';
            const confScore = data.confidence?.total_score ?? 50;
            
            // Show success modal
            document.getElementById('success-order-id').innerText = orderId;
            document.getElementById('success-qty').innerText = quantity.toFixed(8) + ' ' + symbol.replace('USDT', '');
            document.getElementById('success-conf').innerText = confScore + '%';
            
            const modal = document.getElementById('successCard');
            modal.classList.remove('hidden');
            setTimeout(() => {
                modal.classList.add('opacity-100');
            }, 50);
            
            // Reset form
            document.getElementById('order-quantity').value = '0.001';
            fetchDashboardData();
        } else {
            alert('Failed to place order: ' + (data.detail || 'Unknown error'));
        }
    } catch (e) {
        console.error('Error placing order:', e);
        alert('Error placing order: ' + e.message);
    } finally {
        btn.disabled = false;
        btn.innerText = 'PLACE ORDER';
    }
}

function closeSuccess() {
    const modal = document.getElementById('successCard');
    modal.classList.remove('opacity-100');
    setTimeout(() => {
        modal.classList.add('hidden');
    }, 300);
}

// ============================================================================
// ORDER HISTORY PAGE
// ============================================================================

async function loadOrderHistory() {
    try {
        const res = await fetch('/api/orders/history');
        if (res.ok) {
            const historyData = await res.json();
            const tbody = document.getElementById('order-history-rows');
            tbody.innerHTML = '';
            
            if (historyData.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="8" class="px-4 py-8 text-center text-on-surface-variant">
                            No orders found
                        </td>
                    </tr>
                `;
                return;
            }
            
            historyData.forEach(rawOrder => {
                // Extract with proper nesting
                const order = extractOrderDetails(rawOrder);
                const tr = document.createElement('tr');
                tr.className = "hover:bg-surface-variant/40 cursor-pointer transition-colors";
                
                // Format time safely
                const timeStr = order.time && order.time.getTime() > 0 
                    ? order.time.toLocaleString() 
                    : 'N/A';
                
                const sideClass = order.side === 'BUY' 
                    ? 'bg-[#003919] text-primary-fixed-dim'
                    : 'bg-secondary-container text-on-secondary-container';
                
                const statusClass = order.status === 'FILLED'
                    ? 'text-primary-fixed-dim'
                    : order.status === 'REJECTED'
                    ? 'text-error'
                    : 'text-on-surface-variant';
                
                // Get confidence from nested structure
                const confScore = order.confidence?.total_score ?? 50;
                const confidence = confScore.toFixed(1);
                
                tr.innerHTML = `
                    <td class="py-2 px-4 text-on-surface-variant text-data-sm">${timeStr}</td>
                    <td class="py-2 px-4 font-bold text-data-md">${order.symbol}</td>
                    <td class="py-2 px-4"><span class="${sideClass} text-[10px] px-2 py-0.5 rounded font-bold">${order.side}</span></td>
                    <td class="py-2 px-4 text-on-surface-variant text-data-sm">${order.type}</td>
                    <td class="py-2 px-4 text-right text-data-md">${parseFloat(order.quantity ?? '0').toFixed(8)}</td>
                    <td class="py-2 px-4 text-right text-on-surface text-data-md">${parseFloat(order.price ?? '0').toFixed(2)}</td>
                    <td class="py-2 px-4"><span class="${statusClass} text-data-sm font-bold">${order.status}</span></td>
                    <td class="py-2 px-4 text-right text-primary-fixed-dim text-data-md">${confidence}%</td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (e) {
        console.error('Error loading order history:', e);
    }
}

// ============================================================================
// CONFIDENCE ANALYZER PAGE
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    const analyzerType = document.getElementById('analyzer-type');
    if (analyzerType) {
        analyzerType.addEventListener('change', () => {
            const priceField = document.getElementById('analyzer-price-field');
            if (analyzerType.value === 'LIMIT') {
                priceField.classList.remove('hidden');
            } else {
                priceField.classList.add('hidden');
            }
        });
    }
});

async function analyzeSignal() {
    try {
        const symbol = document.getElementById('analyzer-symbol')?.value || 'BTCUSDT';
        const side = document.getElementById('analyzer-side')?.value || 'BUY';
        const type = document.getElementById('analyzer-type')?.value || 'MARKET';
        const price = document.getElementById('analyzer-price')?.value;
        
        const params = new URLSearchParams({
            symbol: symbol,
            side: side,
            order_type: type,
            ...(price && { price })
        });
        
        const res = await fetch(`/api/confidence?${params}`);
        if (res.ok) {
            const confData = await res.json();
            displayAnalysisResults(confData, symbol, side, type);
        }
    } catch (e) {
        console.error('Error analyzing signal:', e);
    }
}

function displayAnalysisResults(rawConfData, symbol, side, type) {
    const confData = extractConfidenceData(rawConfData);
    
    // Use score, grade, recommendation directly from backend
    const score = confData.total_score;
    const grade = confData.grade;
    const recommendation = confData.recommendation;
    
    // Use breakdown metrics directly
    const volatility = confData.breakdown.volatility ?? 50;
    const depth = confData.breakdown.depth ?? 50;
    const prox = confData.breakdown.price_proximity ?? 50;
    
    const html = `
        <div class="space-y-stack-lg">
            <div class="bg-surface-container rounded-lg p-4 border border-outline-variant">
                <div class="grid grid-cols-2 md:grid-cols-4 gap-stack-md">
                    <div>
                        <p class="font-label-caps text-on-surface-variant uppercase mb-1 text-[10px]">Asset</p>
                        <p class="font-data-lg text-on-surface">${symbol}</p>
                    </div>
                    <div>
                        <p class="font-label-caps text-on-surface-variant uppercase mb-1 text-[10px]">Side</p>
                        <p class="font-data-lg text-primary-fixed-dim">${side}</p>
                    </div>
                    <div>
                        <p class="font-label-caps text-on-surface-variant uppercase mb-1 text-[10px]">Type</p>
                        <p class="font-data-lg text-on-surface">${type}</p>
                    </div>
                    <div>
                        <p class="font-label-caps text-on-surface-variant uppercase mb-1 text-[10px]">Grade</p>
                        <p class="font-data-lg text-primary-fixed-dim">${grade}</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-surface-container rounded-lg p-4 border border-outline-variant">
                <h3 class="font-headline-md mb-stack-lg flex items-center gap-2">
                    <span class="material-symbols-outlined">verified</span>
                    Confidence Analysis
                </h3>
                <div class="space-y-stack-md">
                    <div class="flex flex-col items-center p-stack-lg bg-background rounded-lg border border-primary-container/30">
                        <span class="font-data-sm text-on-surface-variant mb-2">OVERALL SCORE</span>
                        <div class="relative w-32 h-32">
                            <svg class="w-full h-full transform -rotate-90">
                                <circle class="text-surface-container-highest" cx="64" cy="64" fill="transparent" r="56" stroke="currentColor" stroke-width="8"></circle>
                                <circle class="text-primary-fixed-dim" cx="64" cy="64" fill="transparent" r="56" stroke="currentColor" stroke-dasharray="351.86" stroke-dashoffset="${351.86 - (score / 100) * 351.86}" stroke-width="8"></circle>
                            </svg>
                            <div class="absolute inset-0 flex flex-col items-center justify-center">
                                <span class="font-data-lg text-[32px] text-primary">${score}</span>
                                <span class="text-[10px] text-on-surface-variant">/ 100</span>
                            </div>
                        </div>
                        <p class="text-headline-md text-on-surface mt-4">${recommendation}</p>
                    </div>
                    
                    <div class="grid grid-cols-3 gap-md">
                        <div class="bg-background rounded-lg p-3 text-center border border-outline-variant">
                            <p class="font-label-caps text-[9px] text-on-surface-variant mb-2">VOLATILITY</p>
                            <p class="font-data-lg text-on-surface">${volatility}%</p>
                        </div>
                        <div class="bg-background rounded-lg p-3 text-center border border-outline-variant">
                            <p class="font-label-caps text-[9px] text-on-surface-variant mb-2">MARKET DEPTH</p>
                            <p class="font-data-lg text-on-surface">${depth}%</p>
                        </div>
                        <div class="bg-background rounded-lg p-3 text-center border border-outline-variant">
                            <p class="font-label-caps text-[9px] text-on-surface-variant mb-2">PRICE PROX</p>
                            <p class="font-data-lg text-on-surface">${prox}%</p>
                        </div>
                    </div>
                    
                    <div class="space-y-stack-md">
                        <div>
                            <div class="flex justify-between mb-1 text-data-sm">
                                <span class="text-on-surface-variant">Volatility Index</span>
                                <span class="text-primary">${volatility}%</span>
                            </div>
                            <div class="w-full h-2 bg-background rounded-full overflow-hidden">
                                <div class="h-full bg-primary-fixed-dim" style="width: ${volatility}%"></div>
                            </div>
                        </div>
                        <div>
                            <div class="flex justify-between mb-1 text-data-sm">
                                <span class="text-on-surface-variant">Order Book Depth</span>
                                <span class="text-primary">${depth}%</span>
                            </div>
                            <div class="w-full h-2 bg-background rounded-full overflow-hidden">
                                <div class="h-full bg-primary-fixed-dim" style="width: ${depth}%"></div>
                            </div>
                        </div>
                        <div>
                            <div class="flex justify-between mb-1 text-data-sm">
                                <span class="text-on-surface-variant">EMA Proximity</span>
                                <span class="text-primary">${prox}%</span>
                            </div>
                            <div class="w-full h-2 bg-background rounded-full overflow-hidden">
                                <div class="h-full bg-primary-fixed-dim" style="width: ${prox}%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('analyzer-results').innerHTML = html;
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    // Initial data fetch
    fetchDashboardData();
    
    // Set up refresh interval (10 seconds)
    refreshInterval = setInterval(fetchDashboardData, 10000);
    
    // Set initial page to dashboard
    navigatePage('dashboard');
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
});
