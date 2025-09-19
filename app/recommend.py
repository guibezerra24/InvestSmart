
from __future__ import annotations
from .schemas import UserProfile, PortfolioRecommendation, AssetAllocation

BASE_ALLOCATION = {
    "conservador": {"renda_fixa": 80, "multimercado": 10, "acoes": 5, "internacional": 5},
    "moderado":    {"renda_fixa": 55, "multimercado": 20, "acoes": 20, "internacional": 5},
    "agressivo":   {"renda_fixa": 25, "multimercado": 25, "acoes": 40, "internacional": 10},
}

def horizon_adjustment(goals: dict[str, int]) -> float:
    """Ajuste grosseiro conforme horizonte médio (meses)."""
    weights = []
    for k in ("curto","medio","longo"):
        m = goals.get(k, 0)
        if m <= 0:
            continue
        if k == "curto":
            weights.append(-0.10)   # puxa para RF
        elif k == "medio":
            weights.append(0.00)
        else:
            weights.append(0.08)    # puxa para risco
    return sum(weights) if weights else 0.0

def build_portfolio(profile: UserProfile) -> PortfolioRecommendation:
    base = BASE_ALLOCATION[profile.risk_tolerance].copy()
    adj = horizon_adjustment(profile.goals)

    base["acoes"] = max(0, min(60, base["acoes"] + adj * 100))
    total = sum(base.values())
    if total != 100:
        diff = 100 - total
        base["renda_fixa"] = max(0, base["renda_fixa"] + diff)

    allocations = [AssetAllocation(name=k, percent=round(v, 2)) for k, v in base.items()]
    rationale = (
        f"A carteira parte do perfil **{profile.risk_tolerance}**. "
        f"Ajuste de horizonte={round(adj,2)} favorece "
        + ("maior renda variável." if adj > 0 else ("maior renda fixa." if adj < 0 else "equilíbrio."))
    )
    return PortfolioRecommendation(allocations=allocations, rationale=rationale)
