
from app.schemas import UserProfile
from app.recommend import build_portfolio

def test_build_portfolio_basic():
    profile = UserProfile(
        age=30,
        risk_tolerance="moderado",
        liquidity_available=10000,
        goals={"curto": 6, "medio": 24, "longo": 60},
    )
    rec = build_portfolio(profile)
    assert sum(a.percent for a in rec.allocations) == 100
    names = {a.name for a in rec.allocations}
    assert {"renda_fixa","multimercado","acoes","internacional"} <= names
