
from fastapi import FastAPI, HTTPException
from .schemas import UserProfile, PortfolioRecommendation
from .recommend import build_portfolio
from .utils import anonymize_email

app = FastAPI(title="InvestSmart API (demo SAST)", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/profile/recommend", response_model=PortfolioRecommendation)
def recommend_portfolio(profile: UserProfile, email: str | None = None):
    # Princípios de LGPD: minimização; email opcional e anonimizado.
    if email and "@" not in email:
        raise HTTPException(status_code=422, detail="email inválido")
    user_id = anonymize_email(email) if email else "anon"
    # (poderíamos armazenar preferências usando user_id)
    return build_portfolio(profile)
