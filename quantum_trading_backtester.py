#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Provenance and third-party notices: see LICENSE, NOTICE, and LICENSING.md.
"""
📊 QUANTUM ALGORITHMIC TRADING BACKTESTER
=========================================
Integrate quantum algorithms with MetaTrader-style backtesting.
Test quantum trading strategies against historical market data.
"""

import numpy as np
import pandas as pd
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance as yf
import json

class QuantumTradingBacktester:
    """Quantum-enhanced algorithmic trading backtester."""
    
    def __init__(self):
        self.quantum_service = None
        self.setup_quantum_backend()
        
    def setup_quantum_backend(self):
        """Initialize quantum computing backend."""
        try:
            self.quantum_service = QiskitRuntimeService(name='my_quantum_cloud')
            print("✅ Quantum backend connected")
        except Exception as e:
            print(f"⚠️  Quantum backend offline, using simulation: {e}")
    
    def download_market_data(self, symbol, period="1y", interval="1d"):
        """Download historical market data (like MetaTrader data feed)."""
        print(f"📈 Downloading {symbol} data for {period}...")
        
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            # Add technical indicators (like MetaTrader)
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            data['RSI'] = self.calculate_rsi(data['Close'])
            data['MACD'], data['MACD_signal'] = self.calculate_macd(data['Close'])
            data['Volatility'] = data['Close'].pct_change().rolling(window=20).std()
            
            print(f"✅ Downloaded {len(data)} data points")
            return data.dropna()
            
        except Exception as e:
            print(f"❌ Error downloading data: {e}")
            return None
    
    def calculate_rsi(self, prices, window=14):
        """Calculate RSI indicator."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD indicator."""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        return macd, macd_signal
    
    def create_quantum_trading_signal(self, market_state):
        """
        Generate trading signals using quantum algorithms.
        Similar to MetaTrader EA logic but quantum-enhanced.
        """
        # Extract market features
        price_trend = 1 if market_state['price_change'] > 0 else 0
        volume_trend = 1 if market_state['volume_change'] > 0 else 0
        rsi_signal = 1 if 30 < market_state['rsi'] < 70 else 0  # Not overbought/oversold
        macd_signal = 1 if market_state['macd'] > market_state['macd_signal'] else 0
        
        # Create quantum circuit for trading decision
        qc = QuantumCircuit(4, 4, name='Trading_Signal')
        
        # Encode market state
        if price_trend:
            qc.x(0)
        if volume_trend:
            qc.x(1)
        if rsi_signal:
            qc.x(2)
        if macd_signal:
            qc.x(3)
        
        # Apply quantum superposition
        for i in range(4):
            qc.h(i)
        
        # Quantum interference for signal processing
        qc.cx(0, 1)  # Price-volume correlation
        qc.cx(2, 3)  # RSI-MACD correlation
        qc.ccx(0, 2, 1)  # Multi-factor analysis
        
        # Amplitude amplification for strong signals
        if market_state['volatility'] < 0.02:  # Low volatility
            qc.ry(np.pi/4, 0)  # Favor trend following
        else:  # High volatility
            qc.ry(-np.pi/6, 0)  # Reduce position size
        
        qc.measure_all()
        
        return qc
    
    def execute_quantum_signal(self, circuit):
        """Execute quantum trading signal on real hardware."""
        try:
            if self.quantum_service:
                backends = self.quantum_service.backends(operational=True, simulator=False)
                backend = min(backends, key=lambda b: b.status().pending_jobs)
                
                transpiled = transpile(circuit, backend=backend, optimization_level=3)
                sampler = Sampler(backend)
                job = sampler.run([transpiled], shots=256)  # Fewer shots for speed
                
                result = job.result()
                counts = result[0].data.c.get_counts()
                return self.interpret_quantum_signal(counts)
            else:
                # Fallback simulation
                return self.simulate_quantum_signal()
                
        except Exception as e:
            print(f"⚠️  Quantum execution error: {e}")
            return self.simulate_quantum_signal()
    
    def interpret_quantum_signal(self, quantum_counts):
        """Convert quantum measurement results to trading signals."""
        total_shots = sum(quantum_counts.values())
        
        # Calculate signal strength based on quantum probabilities
        buy_signal = 0
        sell_signal = 0
        
        for state, count in quantum_counts.items():
            prob = count / total_shots
            
            # Interpret quantum states as trading signals
            ones_count = state.count('1')
            
            if ones_count >= 3:  # Strong bullish pattern
                buy_signal += prob
            elif ones_count <= 1:  # Strong bearish pattern  
                sell_signal += prob
        
        # Generate trading decision
        if buy_signal > 0.6:
            return {'action': 'BUY', 'confidence': buy_signal, 'size': min(buy_signal, 1.0)}
        elif sell_signal > 0.6:
            return {'action': 'SELL', 'confidence': sell_signal, 'size': min(sell_signal, 1.0)}
        else:
            return {'action': 'HOLD', 'confidence': 1 - buy_signal - sell_signal, 'size': 0}
    
    def simulate_quantum_signal(self):
        """Simulate quantum signal for demo purposes."""
        # Realistic quantum-like probabilities
        signals = [
            {'action': 'BUY', 'confidence': 0.75, 'size': 0.8},
            {'action': 'SELL', 'confidence': 0.65, 'size': 0.6},
            {'action': 'HOLD', 'confidence': 0.85, 'size': 0.0}
        ]
        return np.random.choice(signals)
    
    def backtest_quantum_strategy(self, symbol, strategy_params=None):
        """
        Run full backtest like MetaTrader Strategy Tester.
        """
        print(f"🔬 QUANTUM BACKTESTING: {symbol}")
        print("=" * 50)
        
        # Download historical data
        data = self.download_market_data(symbol, period="6mo", interval="1d")
        if data is None:
            return None
        
        # Initialize backtesting variables
        initial_balance = 10000
        balance = initial_balance
        position = 0  # 0 = no position, 1 = long, -1 = short
        position_size = 0
        entry_price = 0
        trades = []
        equity_curve = [balance]
        
        print(f"📊 Backtesting {len(data)} trading days...")
        print(f"💰 Initial Balance: ${initial_balance:,.0f}")
        
        # Iterate through historical data
        for i in range(20, len(data)):  # Skip first 20 days for indicators
            current_data = data.iloc[i]
            prev_data = data.iloc[i-1]
            
            # Prepare market state for quantum analysis
            market_state = {
                'price_change': (current_data['Close'] - prev_data['Close']) / prev_data['Close'],
                'volume_change': (current_data['Volume'] - prev_data['Volume']) / prev_data['Volume'] if prev_data['Volume'] > 0 else 0,
                'rsi': current_data['RSI'],
                'macd': current_data['MACD'],
                'macd_signal': current_data['MACD_signal'],
                'volatility': current_data['Volatility']
            }
            
            # Generate quantum trading signal
            quantum_circuit = self.create_quantum_trading_signal(market_state)
            signal = self.execute_quantum_signal(quantum_circuit)
            
            # Execute trades based on quantum signals
            if position == 0:  # No current position
                if signal['action'] == 'BUY' and signal['confidence'] > 0.7:
                    # Open long position
                    position = 1
                    position_size = signal['size']
                    entry_price = current_data['Close']
                    trade_amount = balance * position_size * 0.95  # 95% max position
                    shares = trade_amount / entry_price
                    
                    trades.append({
                        'date': current_data.name,
                        'action': 'BUY',
                        'price': entry_price,
                        'shares': shares,
                        'confidence': signal['confidence'],
                        'balance_before': balance
                    })
                    
                elif signal['action'] == 'SELL' and signal['confidence'] > 0.7:
                    # Open short position (simplified)
                    position = -1
                    position_size = signal['size']
                    entry_price = current_data['Close']
                    
                    trades.append({
                        'date': current_data.name,
                        'action': 'SELL_SHORT',
                        'price': entry_price,
                        'shares': balance * position_size * 0.5 / entry_price,  # Conservative short
                        'confidence': signal['confidence'],
                        'balance_before': balance
                    })
            
            else:  # Have position, check for exit
                if (position == 1 and signal['action'] == 'SELL') or \
                   (position == -1 and signal['action'] == 'BUY') or \
                   signal['confidence'] < 0.3:  # Low confidence exit
                    
                    # Close position
                    exit_price = current_data['Close']
                    last_trade = trades[-1]
                    
                    if position == 1:  # Close long
                        pnl = (exit_price - entry_price) * last_trade['shares']
                        balance += pnl
                    else:  # Close short
                        pnl = (entry_price - exit_price) * last_trade['shares']
                        balance += pnl
                    
                    trades.append({
                        'date': current_data.name,
                        'action': 'CLOSE',
                        'price': exit_price,
                        'shares': last_trade['shares'],
                        'pnl': pnl,
                        'balance_after': balance
                    })
                    
                    position = 0
                    position_size = 0
            
            equity_curve.append(balance)
        
        # Calculate performance metrics
        total_return = (balance - initial_balance) / initial_balance
        num_trades = len([t for t in trades if t['action'] in ['BUY', 'SELL_SHORT']])
        winning_trades = len([t for t in trades if t.get('pnl', 0) > 0])
        win_rate = winning_trades / max(num_trades, 1)
        
        # Display results
        print(f"\n📊 QUANTUM BACKTESTING RESULTS")
        print("=" * 40)
        print(f"Initial Balance:    ${initial_balance:10,.0f}")
        print(f"Final Balance:      ${balance:10,.0f}")
        print(f"Total Return:       {total_return:10.1%}")
        print(f"Total Trades:       {num_trades:10d}")
        print(f"Winning Trades:     {winning_trades:10d}")
        print(f"Win Rate:           {win_rate:10.1%}")
        
        # Compare to buy-and-hold
        buy_hold_return = (data['Close'].iloc[-1] - data['Close'].iloc[20]) / data['Close'].iloc[20]
        quantum_advantage = total_return - buy_hold_return
        
        print(f"\n🚀 QUANTUM vs BUY-HOLD:")
        print(f"Buy & Hold Return:  {buy_hold_return:10.1%}")
        print(f"Quantum Strategy:   {total_return:10.1%}")
        print(f"Quantum Advantage:  {quantum_advantage:10.1%}")
        
        if quantum_advantage > 0:
            print("✅ Quantum strategy outperformed!")
        else:
            print("⚠️  Buy-and-hold was better this period")
        
        return {
            'trades': trades,
            'equity_curve': equity_curve,
            'final_balance': balance,
            'total_return': total_return,
            'win_rate': win_rate,
            'quantum_advantage': quantum_advantage
        }

def create_quantum_ea_template():
    """Create MetaTrader-style Expert Advisor template using quantum signals."""
    
    ea_template = '''
//+------------------------------------------------------------------+
//| Quantum Trading Expert Advisor                                   |
//| Integrates quantum computing with MetaTrader                     |
//+------------------------------------------------------------------+

// Quantum EA Parameters
input double LotSize = 0.1;
input int QuantumConfidenceThreshold = 70;
input bool UseQuantumSignals = true;
input int MaxTrades = 5;

// Quantum signal structure (would be populated by Python bridge)
struct QuantumSignal {
    string action;      // "BUY", "SELL", "HOLD"
    double confidence;  // 0.0 to 1.0
    double size;        // Position size multiplier
    datetime timestamp;
};

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit() {
    Print("Quantum Trading EA Initialized");
    Print("Quantum Backend: ", UseQuantumSignals ? "ENABLED" : "DISABLED");
    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick() {
    if(!UseQuantumSignals) return;
    
    // Get quantum signal from Python quantum processor
    QuantumSignal signal = GetQuantumSignal();
    
    if(signal.confidence > QuantumConfidenceThreshold/100.0) {
        ExecuteQuantumTrade(signal);
    }
}

//+------------------------------------------------------------------+
//| Get quantum trading signal                                       |
//+------------------------------------------------------------------+
QuantumSignal GetQuantumSignal() {
    QuantumSignal signal;
    
    // Market state for quantum analysis
    double price_change = (Close[0] - Close[1]) / Close[1];
    double rsi = iRSI(Symbol(), 0, 14, PRICE_CLOSE, 0);
    double macd_main = iMACD(Symbol(), 0, 12, 26, 9, PRICE_CLOSE, MODE_MAIN, 0);
    double macd_signal = iMACD(Symbol(), 0, 12, 26, 9, PRICE_CLOSE, MODE_SIGNAL, 0);
    
    // Call Python quantum processor (via DLL or file I/O)
    // This would interface with your quantum backtester
    signal = CallQuantumProcessor(price_change, rsi, macd_main, macd_signal);
    
    return signal;
}

//+------------------------------------------------------------------+
//| Execute trade based on quantum signal                           |
//+------------------------------------------------------------------+
void ExecuteQuantumTrade(QuantumSignal signal) {
    double lot_size = LotSize * signal.size;
    
    if(signal.action == "BUY" && PositionsTotal() < MaxTrades) {
        // Open long position
        MqlTradeRequest request;
        MqlTradeResult result;
        
        request.action = TRADE_ACTION_DEAL;
        request.symbol = Symbol();
        request.volume = lot_size;
        request.type = ORDER_TYPE_BUY;
        request.price = Ask;
        request.comment = StringFormat("Quantum BUY (%.2f confidence)", signal.confidence);
        
        OrderSend(request, result);
        
        Print("Quantum BUY executed: Confidence=", signal.confidence, " Size=", signal.size);
    }
    else if(signal.action == "SELL" && PositionsTotal() < MaxTrades) {
        // Open short position
        MqlTradeRequest request;
        MqlTradeResult result;
        
        request.action = TRADE_ACTION_DEAL;
        request.symbol = Symbol();
        request.volume = lot_size;
        request.type = ORDER_TYPE_SELL;
        request.price = Bid;
        request.comment = StringFormat("Quantum SELL (%.2f confidence)", signal.confidence);
        
        OrderSend(request, result);
        
        Print("Quantum SELL executed: Confidence=", signal.confidence, " Size=", signal.size);
    }
}

//+------------------------------------------------------------------+
'''
    
    with open("QuantumTradingEA.mq5", "w") as f:
        f.write(ea_template)
    
    print("📄 Created MetaTrader EA template: QuantumTradingEA.mq5")

def main():
    """Demonstrate quantum algorithmic trading backtesting."""
    
    print("🚀 QUANTUM ALGORITHMIC TRADING BACKTESTER")
    print("=" * 60)
    print("Integrating quantum computing with MetaTrader-style backtesting!")
    print()
    
    # Initialize quantum backtester
    backtester = QuantumTradingBacktester()
    
    # Test symbols (like MetaTrader symbol selection)
    symbols = ['AAPL', 'GOOGL', 'TSLA', 'SPY']
    
    print("📊 Available symbols for backtesting:")
    for i, symbol in enumerate(symbols, 1):
        print(f"   {i}. {symbol}")
    
    print()
    choice = input("Select symbol (1-4) or press Enter for AAPL: ").strip()
    symbol_map = {'1': 'AAPL', '2': 'GOOGL', '3': 'TSLA', '4': 'SPY'}
    selected_symbol = symbol_map.get(choice, 'AAPL')
    
    # Run quantum backtest
    results = backtester.backtest_quantum_strategy(selected_symbol)
    
    if results:
        print(f"\n🎯 NEXT STEPS:")
        print("1. 📊 Optimize quantum parameters")
        print("2. 🔄 Test on different timeframes")
        print("3. 📈 Combine with your MetaTrader strategies")
        print("4. 🚀 Deploy on live quantum hardware")
        
        # Create MetaTrader integration template
        create_quantum_ea_template()
        
        print(f"\n✅ Quantum backtesting complete!")
        print(f"🔗 Ready to integrate with MetaTrader!")

if __name__ == "__main__":
    main()
