FEATURE_NAMES = [
    "tenure_months",
    "monthly_spend",
    "support_tickets_30d",
    "login_days_30d",
    "tier_free",
    "tier_enterprise",
    "cancellation_ticket_flag",
]


def extract_features(row: dict, spend_median: float = 150.0) -> list[float]:
    tier = row["plan_tier"]  # BUG: not lowercased
    spend = float(row["monthly_spend"])  # BUG: crashes on empty string in prod
    return [
        float(row["tenure_months"]) / 48.0,
        spend / 450.0,
        float(row["support_tickets_30d"]) / 12.0,
        float(row["login_days_30d"]) / 30.0,
        1.0 if tier == "free" else 0.0,
        1.0 if tier == "enterprise" else 0.0,
        float(row["cancellation_ticket_flag"]),  # BUG: target leakage!
    ]
