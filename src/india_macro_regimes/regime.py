from typing import Dict, Any

class MacroRegimeEvaluator:
    """Evaluates India VIX volatility regime and Dual Momentum cash hurdle rates."""

    @staticmethod
    def classify_vix(vix_value: float) -> str:
        if vix_value < 15.0:
            return "LOW_VOLATILITY"   # Bullish / Trend-Following Favorable
        elif vix_value <= 22.0:
            return "NORMAL_VOLATILITY"
        else:
            return "HIGH_VOLATILITY"  # Elevated Drawdown Risk / Trigger Cash Defense

    @staticmethod
    def is_asset_momentum_positive(asset_return_annualized: float, risk_free_rate: float) -> bool:
        """Absolute Momentum rule: excess return over risk-free rate must be positive."""
        return asset_return_annualized > risk_free_rate
