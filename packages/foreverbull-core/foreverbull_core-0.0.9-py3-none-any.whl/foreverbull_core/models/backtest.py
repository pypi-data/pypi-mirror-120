from foreverbull_core.models.socket import SocketConfig
from typing import List
from foreverbull_core.models.base import Base


class Session(Base):
    id: str


class BacktestSockets(Base):
    main: SocketConfig
    feed: SocketConfig
    broker: SocketConfig
    running: bool


class BacktestConfig(Base):
    start_date: str
    end_date: str
    timezone: str = "utc"
    benchmark: str
    assets: List[str]


class PeriodResult(Base):
    period_open: str
    period_close: str
    shorts_count: int
    pnl: float
    long_value: float
    short_value: int
    long_exposure: float
    starting_exposure: float
    short_exposure: int
    capital_used: float
    gross_leverage: float
    net_leverage: float
    ending_exposure: float
    starting_value: float
    ending_value: float
    starting_cash: float
    ending_cash: float
    returns: float
    portfolio_value: float
    longs_count: int
    algo_volatility: float
    sharpe: float
    alpha: float
    beta: float
    sortino: float
    max_drawdown: float
    max_leverage: float
    excess_return: int
    treasury_period_return: int
    trading_days: int
    benchmark_period_return: float
    benchmark_volatility: float
    algorithm_period_return: float


class BacktestResult(Base):
    periods: List[PeriodResult]
