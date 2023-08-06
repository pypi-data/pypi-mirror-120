# Ezil Pool API Wrapper

Simple API wrapper for Ezil.me mining pool. All methods returns dict or None

## Installation
```
pip install ezil
```

## Usage
### Initialization
```
import Ezil from ezil

ezil = Ezil()
```
### Stats
```
ezil.pool_stats(WALLET_ADDRESS)
```
### History
```
ezil.pool_history(WALLET_ADDRESS)
```
### Balance
```
ezil.pool_balance(WALLET_ADDRESS)
```
### Forecast
```
ezil.pool_forecast(WALLET_ADDRESS)
```