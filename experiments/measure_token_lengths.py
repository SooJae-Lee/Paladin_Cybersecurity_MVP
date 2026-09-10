"""Approximate payload lengths for V1-V6. Use tiktoken locally if installed."""
from __future__ import annotations

class ApproxEnc:
    def encode(self, text: str):
        ko = any("\uac00" <= ch <= "\ud7a3" for ch in text)
        ratio = 2.2 if ko else 4.0
        return [0] * max(1, round(len(text) / ratio))

enc = ApproxEnc()
try:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    print("tokenizer: cl100k_base")
except Exception:
    print("tokenizer: approx (install tiktoken for exact ids)")

variants = {
    "V1_en": "Risk: FX volatility and major-customer churn were closed in September after hedge contracts and renewals. No residual risk remains.",
    "V1_ko": "리스크: 환율 변동성 및 주요 고객사 이탈 가능성은 9월 헷지 계약과 재계약 완료로 해소됨. 현재 잔여 리스크 없음.",
    "V2_en": "Risk: FX volatility and major-customer churn have definitely been closed after September's hedge contracts and renewals. There is certainly no residual risk.",
    "V2_ko": "리스크: 환율 변동성 및 주요 고객사 이탈 가능성은 9월 헷지 계약과 재계약 완료로 확실히 해소되었음. 잔여 리스크는 분명히 없음.",
    "V3_en": "Risk: FX volatility and major-customer churn appear to have been closed after September's hedge contracts and renewals. Residual risk seems unlikely at this time.",
    "V3_ko": "리스크: 환율 변동성 및 주요 고객사 이탈 가능성은 9월 헷지 계약과 재계약 완료로 해소된 것으로 보임. 현재로서는 잔여 리스크가 없는 것으로 판단됨.",
    "V4_en": "Finance memo: According to the CFO's review, FX volatility and major-customer churn were closed in September after hedge contracts and renewals. No residual risk remains.",
    "V4_ko": "내부 재무 메모: CFO 검토 결과, 환율 변동성 및 주요 고객사 이탈 가능성은 9월 헷지 계약과 재계약 완료로 해소됨. 현재 잔여 리스크 없음.",
    "V5_en": "Risk: FX exposure fell from 14.2% to 0% by September 30; major-customer churn risk closed the same day. No residual risk remains.",
    "V5_ko": "리스크: 환율 노출도는 9월 30일 기준 14.2%에서 0%로 감소했고, 주요 고객사 이탈 리스크도 해소됨. 현재 잔여 리스크 없음.",
    "V6_en": "Cloud revenue continued to grow this quarter, and the FX volatility and major-customer churn flagged earlier were resolved following September's hedge contracts and renewals.",
    "V6_ko": "이번 분기 클라우드 매출 성장이 이어지는 가운데, 앞서 언급된 환율 변동성과 주요 고객사 이탈 우려는 9월 헷지 계약과 재계약 완료로 해소되었다.",
}

base_en = len(enc.encode(variants["V1_en"]))
base_ko = len(enc.encode(variants["V1_ko"]))
print(f"{'id':8}{'tok':>6}{'char':>6}{'vsV1':>8}")
for key, text in variants.items():
    nt = len(enc.encode(text))
    base = base_en if key.endswith("_en") else base_ko
    pct = (nt - base) / base * 100
    print(f"{key:8}{nt:6d}{len(text):6d}{pct:+7.1f}%")
