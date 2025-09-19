
from pydantic import BaseModel, Field, conint, confloat

class UserProfile(BaseModel):
    age: conint(ge=18, le=100)
    risk_tolerance: str = Field(pattern="^(conservador|moderado|agressivo)$")
    liquidity_available: confloat(ge=0)
    goals: dict  # {"curto": 12, "medio": 36, "longo": 120} meses

class AssetAllocation(BaseModel):
    name: str
    percent: confloat(ge=0, le=100)

class PortfolioRecommendation(BaseModel):
    allocations: list[AssetAllocation]
    rationale: str
