# CLI Trade Batch Report

- Generated: 2026-06-08T17:27:05.693160+00:00
- Environment: Binance Futures testnet
- Orders placed: 15

| # | Symbol | Side | Type | Qty | Price | Grade | Order ID | Status | Exit |
| --- | --- | --- | --- | ---: | ---: | --- | ---: | --- | ---: |
| 1 | BTCUSDT | BUY | MARKET | 0.001 | — | A | 14511847133 | NEW | 0 |
| 2 | ETHUSDT | SELL | LIMIT | 0.001 | 64230.5 | B | 9340453850 | NEW | 0 |
| 3 | BTCUSDT | BUY | MARKET | 0.001 | — | A | 14511851881 | NEW | 0 |
| 4 | ETHUSDT | SELL | LIMIT | 0.001 | 64231.5 | B | 9340456302 | NEW | 0 |
| 5 | BTCUSDT | BUY | MARKET | 0.001 | — | B | 14511854113 | NEW | 0 |
| 6 | ETHUSDT | SELL | LIMIT | 0.001 | 64232.5 | B | 9340457829 | NEW | 0 |
| 7 | BTCUSDT | BUY | MARKET | 0.001 | — | A | 14511857283 | NEW | 0 |
| 8 | ETHUSDT | SELL | LIMIT | 0.001 | 64233.5 | B | 9340459868 | NEW | 0 |
| 9 | BTCUSDT | BUY | MARKET | 0.001 | — | A | 14511859671 | NEW | 0 |
| 10 | ETHUSDT | SELL | LIMIT | 0.001 | 64234.5 | B | 9340461172 | NEW | 0 |
| 11 | BTCUSDT | BUY | MARKET | 0.001 | — | A | 14511861138 | NEW | 0 |
| 12 | ETHUSDT | SELL | LIMIT | 0.001 | 64235.5 | B | 9340462661 | NEW | 0 |
| 13 | BTCUSDT | BUY | MARKET | 0.001 | — | B | 14511863047 | NEW | 0 |
| 14 | ETHUSDT | SELL | LIMIT | 0.001 | 64236.5 | B | 9340464542 | NEW | 0 |
| 15 | BTCUSDT | BUY | MARKET | 0.001 | — | B | 14511865605 | NEW | 0 |

## Raw CLI Snapshots

### Trade 1

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   BTCUSDT                                                      │
│ Side:     BUY                                                          │
│ Type:     MARKET                                                       │
│ Quantity: 0.001                                                        │
│ Price:    —                                                            │
╰────────────────────────────────────────────────────────────────────────╯
                    Confidence Score                     
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                               ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 87                                  │
│ Grade           │ A                                   │
│ Recommendation  │ Excellent conditions to place order │
│ Volatility      │ 90                                  │
│ Depth           │ 91                                  │
│ Price Proximity │ 80                                  │
└─────────────────┴─────────────────────────────────────┘
    Order Request Summary    
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field     ┃ Value         ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol    │ BTCUSDT       │
│ side      │ BUY           │
│ type      │ MARKET        │
│ quantity  │ 0.001         │
│ timestamp │ 1780939602695 │
└───────────┴───────────────┘
       Order Response        
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Field       ┃ Value       ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ orderId     │ 14511847133 │
│ status      │ NEW         │
│ executedQty │ 0.0000      │
│ avgPrice    │ N/A         │
│ cumQuote    │ N/A         │
└─────────────┴─────────────┘
✅ Order placed successfully!
/Users/aditya1981/Onion Trader/.venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
... output truncated ...
```

### Trade 2

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   ETHUSDT                                                      │
│ Side:     SELL                                                         │
│ Type:     LIMIT                                                        │
│ Quantity: 0.001                                                        │
│ Price:    64230.5                                                      │
╰────────────────────────────────────────────────────────────────────────╯
                  Confidence Score                  
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                          ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 67                             │
│ Grade           │ B                              │
│ Recommendation  │ Good conditions to place order │
│ Volatility      │ 70                             │
│ Depth           │ 100                            │
│ Price Proximity │ 20                             │
└─────────────────┴────────────────────────────────┘
     Order Request Summary     
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field       ┃ Value         ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol      │ ETHUSDT       │
│ side        │ SELL          │
│ type        │ LIMIT         │
│ quantity    │ 0.001         │
│ timestamp   │ 1780939604943 │
│ price       │ 64230.5       │
│ timeInForce │ GTC           │
└─────────────┴───────────────┘
       Order Response       
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Field       ┃ Value      ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ orderId     │ 9340453850 │
│ status      │ NEW        │
│ executedQty │ 0.000      │
│ avgPrice    │ N/A        │
│ cumQuote    │ N/A        │
└─────────────┴────────────┘
... output truncated ...
```

### Trade 3

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   BTCUSDT                                                      │
│ Side:     BUY                                                          │
│ Type:     MARKET                                                       │
│ Quantity: 0.001                                                        │
│ Price:    —                                                            │
╰────────────────────────────────────────────────────────────────────────╯
                    Confidence Score                     
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                               ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 87                                  │
│ Grade           │ A                                   │
│ Recommendation  │ Excellent conditions to place order │
│ Volatility      │ 90                                  │
│ Depth           │ 89                                  │
│ Price Proximity │ 80                                  │
└─────────────────┴─────────────────────────────────────┘
    Order Request Summary    
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field     ┃ Value         ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol    │ BTCUSDT       │
│ side      │ BUY           │
│ type      │ MARKET        │
│ quantity  │ 0.001         │
│ timestamp │ 1780939607624 │
└───────────┴───────────────┘
       Order Response        
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Field       ┃ Value       ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ orderId     │ 14511851881 │
│ status      │ NEW         │
│ executedQty │ 0.0000      │
│ avgPrice    │ N/A         │
│ cumQuote    │ N/A         │
└─────────────┴─────────────┘
✅ Order placed successfully!
/Users/aditya1981/Onion Trader/.venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
... output truncated ...
```

### Trade 4

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   ETHUSDT                                                      │
│ Side:     SELL                                                         │
│ Type:     LIMIT                                                        │
│ Quantity: 0.001                                                        │
│ Price:    64231.5                                                      │
╰────────────────────────────────────────────────────────────────────────╯
                  Confidence Score                  
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                          ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 67                             │
│ Grade           │ B                              │
│ Recommendation  │ Good conditions to place order │
│ Volatility      │ 70                             │
│ Depth           │ 100                            │
│ Price Proximity │ 20                             │
└─────────────────┴────────────────────────────────┘
     Order Request Summary     
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field       ┃ Value         ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol      │ ETHUSDT       │
│ side        │ SELL          │
│ type        │ LIMIT         │
│ quantity    │ 0.001         │
│ timestamp   │ 1780939609939 │
│ price       │ 64231.5       │
│ timeInForce │ GTC           │
└─────────────┴───────────────┘
       Order Response       
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Field       ┃ Value      ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ orderId     │ 9340456302 │
│ status      │ NEW        │
│ executedQty │ 0.000      │
│ avgPrice    │ N/A        │
│ cumQuote    │ N/A        │
└─────────────┴────────────┘
... output truncated ...
```

### Trade 5

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   BTCUSDT                                                      │
│ Side:     BUY                                                          │
│ Type:     MARKET                                                       │
│ Quantity: 0.001                                                        │
│ Price:    —                                                            │
╰────────────────────────────────────────────────────────────────────────╯
                  Confidence Score                  
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                          ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 79                             │
│ Grade           │ B                              │
│ Recommendation  │ Good conditions to place order │
│ Volatility      │ 90                             │
│ Depth           │ 69                             │
│ Price Proximity │ 80                             │
└─────────────────┴────────────────────────────────┘
    Order Request Summary    
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field     ┃ Value         ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol    │ BTCUSDT       │
│ side      │ BUY           │
│ type      │ MARKET        │
│ quantity  │ 0.001         │
│ timestamp │ 1780939611223 │
└───────────┴───────────────┘
       Order Response        
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Field       ┃ Value       ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ orderId     │ 14511854113 │
│ status      │ NEW         │
│ executedQty │ 0.0000      │
│ avgPrice    │ N/A         │
│ cumQuote    │ N/A         │
└─────────────┴─────────────┘
✅ Order placed successfully!
/Users/aditya1981/Onion Trader/.venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
... output truncated ...
```

### Trade 6

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   ETHUSDT                                                      │
│ Side:     SELL                                                         │
│ Type:     LIMIT                                                        │
│ Quantity: 0.001                                                        │
│ Price:    64232.5                                                      │
╰────────────────────────────────────────────────────────────────────────╯
                  Confidence Score                  
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                          ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 67                             │
│ Grade           │ B                              │
│ Recommendation  │ Good conditions to place order │
│ Volatility      │ 70                             │
│ Depth           │ 100                            │
│ Price Proximity │ 20                             │
└─────────────────┴────────────────────────────────┘
     Order Request Summary     
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field       ┃ Value         ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol      │ ETHUSDT       │
│ side        │ SELL          │
│ type        │ LIMIT         │
│ quantity    │ 0.001         │
│ timestamp   │ 1780939612881 │
│ price       │ 64232.5       │
│ timeInForce │ GTC           │
└─────────────┴───────────────┘
       Order Response       
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Field       ┃ Value      ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ orderId     │ 9340457829 │
│ status      │ NEW        │
│ executedQty │ 0.000      │
│ avgPrice    │ N/A        │
│ cumQuote    │ N/A        │
└─────────────┴────────────┘
... output truncated ...
```

### Trade 7

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   BTCUSDT                                                      │
│ Side:     BUY                                                          │
│ Type:     MARKET                                                       │
│ Quantity: 0.001                                                        │
│ Price:    —                                                            │
╰────────────────────────────────────────────────────────────────────────╯
                    Confidence Score                     
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                               ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 86                                  │
│ Grade           │ A                                   │
│ Recommendation  │ Excellent conditions to place order │
│ Volatility      │ 90                                  │
│ Depth           │ 88                                  │
│ Price Proximity │ 80                                  │
└─────────────────┴─────────────────────────────────────┘
    Order Request Summary    
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field     ┃ Value         ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol    │ BTCUSDT       │
│ side      │ BUY           │
│ type      │ MARKET        │
│ quantity  │ 0.001         │
│ timestamp │ 1780939614101 │
└───────────┴───────────────┘
       Order Response        
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Field       ┃ Value       ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ orderId     │ 14511857283 │
│ status      │ NEW         │
│ executedQty │ 0.0000      │
│ avgPrice    │ N/A         │
│ cumQuote    │ N/A         │
└─────────────┴─────────────┘
✅ Order placed successfully!
/Users/aditya1981/Onion Trader/.venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
... output truncated ...
```

### Trade 8

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   ETHUSDT                                                      │
│ Side:     SELL                                                         │
│ Type:     LIMIT                                                        │
│ Quantity: 0.001                                                        │
│ Price:    64233.5                                                      │
╰────────────────────────────────────────────────────────────────────────╯
                  Confidence Score                  
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                          ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 67                             │
│ Grade           │ B                              │
│ Recommendation  │ Good conditions to place order │
│ Volatility      │ 70                             │
│ Depth           │ 100                            │
│ Price Proximity │ 20                             │
└─────────────────┴────────────────────────────────┘
     Order Request Summary     
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field       ┃ Value         ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol      │ ETHUSDT       │
│ side        │ SELL          │
│ type        │ LIMIT         │
│ quantity    │ 0.001         │
│ timestamp   │ 1780939615970 │
│ price       │ 64233.5       │
│ timeInForce │ GTC           │
└─────────────┴───────────────┘
       Order Response       
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Field       ┃ Value      ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ orderId     │ 9340459868 │
│ status      │ NEW        │
│ executedQty │ 0.000      │
│ avgPrice    │ N/A        │
│ cumQuote    │ N/A        │
└─────────────┴────────────┘
... output truncated ...
```

### Trade 9

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   BTCUSDT                                                      │
│ Side:     BUY                                                          │
│ Type:     MARKET                                                       │
│ Quantity: 0.001                                                        │
│ Price:    —                                                            │
╰────────────────────────────────────────────────────────────────────────╯
                    Confidence Score                     
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                               ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 80                                  │
│ Grade           │ A                                   │
│ Recommendation  │ Excellent conditions to place order │
│ Volatility      │ 90                                  │
│ Depth           │ 72                                  │
│ Price Proximity │ 80                                  │
└─────────────────┴─────────────────────────────────────┘
    Order Request Summary    
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field     ┃ Value         ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol    │ BTCUSDT       │
│ side      │ BUY           │
│ type      │ MARKET        │
│ quantity  │ 0.001         │
│ timestamp │ 1780939617228 │
└───────────┴───────────────┘
       Order Response        
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Field       ┃ Value       ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ orderId     │ 14511859671 │
│ status      │ NEW         │
│ executedQty │ 0.0000      │
│ avgPrice    │ N/A         │
│ cumQuote    │ N/A         │
└─────────────┴─────────────┘
✅ Order placed successfully!
/Users/aditya1981/Onion Trader/.venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
... output truncated ...
```

### Trade 10

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   ETHUSDT                                                      │
│ Side:     SELL                                                         │
│ Type:     LIMIT                                                        │
│ Quantity: 0.001                                                        │
│ Price:    64234.5                                                      │
╰────────────────────────────────────────────────────────────────────────╯
                  Confidence Score                  
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                          ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 67                             │
│ Grade           │ B                              │
│ Recommendation  │ Good conditions to place order │
│ Volatility      │ 70                             │
│ Depth           │ 100                            │
│ Price Proximity │ 20                             │
└─────────────────┴────────────────────────────────┘
     Order Request Summary     
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field       ┃ Value         ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol      │ ETHUSDT       │
│ side        │ SELL          │
│ type        │ LIMIT         │
│ quantity    │ 0.001         │
│ timestamp   │ 1780939618566 │
│ price       │ 64234.5       │
│ timeInForce │ GTC           │
└─────────────┴───────────────┘
       Order Response       
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Field       ┃ Value      ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ orderId     │ 9340461172 │
│ status      │ NEW        │
│ executedQty │ 0.000      │
│ avgPrice    │ N/A        │
│ cumQuote    │ N/A        │
└─────────────┴────────────┘
... output truncated ...
```

### Trade 11

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   BTCUSDT                                                      │
│ Side:     BUY                                                          │
│ Type:     MARKET                                                       │
│ Quantity: 0.001                                                        │
│ Price:    —                                                            │
╰────────────────────────────────────────────────────────────────────────╯
                    Confidence Score                     
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                               ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 80                                  │
│ Grade           │ A                                   │
│ Recommendation  │ Excellent conditions to place order │
│ Volatility      │ 90                                  │
│ Depth           │ 72                                  │
│ Price Proximity │ 80                                  │
└─────────────────┴─────────────────────────────────────┘
    Order Request Summary    
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field     ┃ Value         ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol    │ BTCUSDT       │
│ side      │ BUY           │
│ type      │ MARKET        │
│ quantity  │ 0.001         │
│ timestamp │ 1780939619692 │
└───────────┴───────────────┘
       Order Response        
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Field       ┃ Value       ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ orderId     │ 14511861138 │
│ status      │ NEW         │
│ executedQty │ 0.0000      │
│ avgPrice    │ N/A         │
│ cumQuote    │ N/A         │
└─────────────┴─────────────┘
✅ Order placed successfully!
/Users/aditya1981/Onion Trader/.venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
... output truncated ...
```

### Trade 12

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   ETHUSDT                                                      │
│ Side:     SELL                                                         │
│ Type:     LIMIT                                                        │
│ Quantity: 0.001                                                        │
│ Price:    64235.5                                                      │
╰────────────────────────────────────────────────────────────────────────╯
                  Confidence Score                  
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                          ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 67                             │
│ Grade           │ B                              │
│ Recommendation  │ Good conditions to place order │
│ Volatility      │ 70                             │
│ Depth           │ 100                            │
│ Price Proximity │ 20                             │
└─────────────────┴────────────────────────────────┘
     Order Request Summary     
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field       ┃ Value         ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol      │ ETHUSDT       │
│ side        │ SELL          │
│ type        │ LIMIT         │
│ quantity    │ 0.001         │
│ timestamp   │ 1780939621132 │
│ price       │ 64235.5       │
│ timeInForce │ GTC           │
└─────────────┴───────────────┘
       Order Response       
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Field       ┃ Value      ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ orderId     │ 9340462661 │
│ status      │ NEW        │
│ executedQty │ 0.000      │
│ avgPrice    │ N/A        │
│ cumQuote    │ N/A        │
└─────────────┴────────────┘
... output truncated ...
```

### Trade 13

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   BTCUSDT                                                      │
│ Side:     BUY                                                          │
│ Type:     MARKET                                                       │
│ Quantity: 0.001                                                        │
│ Price:    —                                                            │
╰────────────────────────────────────────────────────────────────────────╯
                  Confidence Score                  
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                          ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 76                             │
│ Grade           │ B                              │
│ Recommendation  │ Good conditions to place order │
│ Volatility      │ 90                             │
│ Depth           │ 62                             │
│ Price Proximity │ 80                             │
└─────────────────┴────────────────────────────────┘
    Order Request Summary    
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field     ┃ Value         ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol    │ BTCUSDT       │
│ side      │ BUY           │
│ type      │ MARKET        │
│ quantity  │ 0.001         │
│ timestamp │ 1780939622233 │
└───────────┴───────────────┘
       Order Response        
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Field       ┃ Value       ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ orderId     │ 14511863047 │
│ status      │ NEW         │
│ executedQty │ 0.0000      │
│ avgPrice    │ N/A         │
│ cumQuote    │ N/A         │
└─────────────┴─────────────┘
✅ Order placed successfully!
/Users/aditya1981/Onion Trader/.venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
... output truncated ...
```

### Trade 14

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   ETHUSDT                                                      │
│ Side:     SELL                                                         │
│ Type:     LIMIT                                                        │
│ Quantity: 0.001                                                        │
│ Price:    64236.5                                                      │
╰────────────────────────────────────────────────────────────────────────╯
                  Confidence Score                  
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                          ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 67                             │
│ Grade           │ B                              │
│ Recommendation  │ Good conditions to place order │
│ Volatility      │ 70                             │
│ Depth           │ 100                            │
│ Price Proximity │ 20                             │
└─────────────────┴────────────────────────────────┘
     Order Request Summary     
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field       ┃ Value         ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol      │ ETHUSDT       │
│ side        │ SELL          │
│ type        │ LIMIT         │
│ quantity    │ 0.001         │
│ timestamp   │ 1780939623641 │
│ price       │ 64236.5       │
│ timeInForce │ GTC           │
└─────────────┴───────────────┘
       Order Response       
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Field       ┃ Value      ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ orderId     │ 9340464542 │
│ status      │ NEW        │
│ executedQty │ 0.000      │
│ avgPrice    │ N/A        │
│ cumQuote    │ N/A        │
└─────────────┴────────────┘
... output truncated ...
```

### Trade 15

```text
╭───────────────────────────── Onion Trader ─────────────────────────────╮
│ Symbol:   BTCUSDT                                                      │
│ Side:     BUY                                                          │
│ Type:     MARKET                                                       │
│ Quantity: 0.001                                                        │
│ Price:    —                                                            │
╰────────────────────────────────────────────────────────────────────────╯
                  Confidence Score                  
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value                          ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Score     │ 76                             │
│ Grade           │ B                              │
│ Recommendation  │ Good conditions to place order │
│ Volatility      │ 90                             │
│ Depth           │ 63                             │
│ Price Proximity │ 80                             │
└─────────────────┴────────────────────────────────┘
    Order Request Summary    
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Field     ┃ Value         ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ symbol    │ BTCUSDT       │
│ side      │ BUY           │
│ type      │ MARKET        │
│ quantity  │ 0.001         │
│ timestamp │ 1780939624954 │
└───────────┴───────────────┘
       Order Response        
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Field       ┃ Value       ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ orderId     │ 14511865605 │
│ status      │ NEW         │
│ executedQty │ 0.0000      │
│ avgPrice    │ N/A         │
│ cumQuote    │ N/A         │
└─────────────┴─────────────┘
✅ Order placed successfully!
/Users/aditya1981/Onion Trader/.venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
... output truncated ...
```
