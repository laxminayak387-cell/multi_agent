"""Mock dashboard data for PurpleMerit product launch."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate date range (14 days)
end_date = datetime(2025, 1, 20)
start_date = end_date - timedelta(days=13)
dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Feature launch date (day 7)
launch_date = dates[6]

np.random.seed(42)

# ===== METRICS =====
# Activation rate (baseline ~68%, drops after launch)
activation_rate = [68 + np.random.normal(0, 2) for _ in range(7)]
activation_rate += [62 + np.random.normal(0, 2) for _ in range(7)]  # post-launch drop

# DAU/WAU ratio (baseline ~0.42, slight decline)
dau_wau = [0.42 + np.random.normal(0, 0.02) for _ in range(7)]
dau_wau += [0.38 + np.random.normal(0, 0.02) for _ in range(7)]

# D1 retention (baseline ~55%, drop after launch)
d1_retention = [55 + np.random.normal(0, 2) for _ in range(7)]
d1_retention += [48 + np.random.normal(0, 2) for _ in range(7)]

# Crash rate (baseline 0.5%, spikes post-launch)
crash_rate = [0.5 + np.random.normal(0, 0.1) for _ in range(7)]
crash_rate += [2.3 + np.random.normal(0, 0.3) for _ in range(7)]  # crash spike

# API latency p95 (baseline 120ms, increases)
api_latency = [120 + np.random.normal(0, 5) for _ in range(7)]
api_latency += [210 + np.random.normal(0, 15) for _ in range(7)]

# Payment success rate (baseline 99.2%, minor dip)
payment_success = [99.2 + np.random.normal(0, 0.1) for _ in range(7)]
payment_success += [98.5 + np.random.normal(0, 0.3) for _ in range(7)]

# Support ticket volume (baseline ~45/day, spikes)
support_tickets = [45 + np.random.poisson(3) for _ in range(7)]
support_tickets += [132 + np.random.poisson(10) for _ in range(7)]

# Feature adoption funnel (new feature usage)
feature_adoption = [0, 0, 0, 0, 0, 0, 0, 8, 15, 22, 28, 31, 33, 34]  # % of users who tried

# Churn rate (daily, baseline 0.8%, increases)
churn_rate = [0.8 + np.random.normal(0, 0.05) for _ in range(7)]
churn_rate += [1.4 + np.random.normal(0, 0.1) for _ in range(7)]

metrics_df = pd.DataFrame({
    'date': dates,
    'activation_rate_pct': activation_rate,
    'dau_wau_ratio': dau_wau,
    'd1_retention_pct': d1_retention,
    'crash_rate_pct': crash_rate,
    'api_latency_p95_ms': api_latency,
    'payment_success_rate_pct': payment_success,
    'support_ticket_volume': support_tickets,
    'feature_adoption_pct': feature_adoption,
    'churn_rate_pct': churn_rate
})

# ===== USER FEEDBACK (35 entries) =====
user_feedback = [
    {"id": 1, "sentiment": "positive", "text": "Love the new design! So much faster."},
    {"id": 2, "sentiment": "positive", "text": "Finally, dark mode. This is great."},
    {"id": 3, "sentiment": "negative", "text": "App keeps crashing after update"},
    {"id": 4, "sentiment": "negative", "text": "Can't log in anymore. Stuck on loading screen."},
    {"id": 5, "sentiment": "neutral", "text": "New layout is okay, takes getting used to."},
    {"id": 6, "sentiment": "negative", "text": "CRASHING CONSTANTLY. Fix this."},
    {"id": 7, "sentiment": "positive", "text": "Checkout is way smoother now"},
    {"id": 8, "sentiment": "negative", "text": "Payments failing repeatedly. Lost an order."},
    {"id": 9, "sentiment": "negative", "text": "Slow loading. Takes 10 seconds to open."},
    {"id": 10, "sentiment": "positive", "text": "New recommendation engine is spot on"},
    {"id": 11, "sentiment": "negative", "text": "App crashes every time I try to view my cart"},
    {"id": 12, "sentiment": "neutral", "text": "Search works better but crashes sometimes"},
    {"id": 13, "sentiment": "negative", "text": "Lost my saved items after update"},
    {"id": 14, "sentiment": "positive", "text": "Love the new onboarding flow"},
    {"id": 15, "sentiment": "negative", "text": "Support tickets going unanswered"},
    {"id": 16, "sentiment": "negative", "text": "Crash on startup. Can't use the app at all."},
    {"id": 17, "sentiment": "positive", "text": "New features are intuitive. Good job team."},
    {"id": 18, "sentiment": "negative", "text": "Payment success rate has been terrible"},
    {"id": 19, "sentiment": "neutral", "text": "Haven't noticed much difference tbh"},
    {"id": 20, "sentiment": "negative", "text": "CRASHING. Uninstalling until fixed."},
    {"id": 21, "sentiment": "positive", "text": "Great update! App feels modern."},
    {"id": 22, "sentiment": "negative", "text": "Latency is insane. Takes forever to load anything."},
    {"id": 23, "sentiment": "negative", "text": "Another crash. This is day 3 of issues."},
    {"id": 24, "sentiment": "positive", "text": "Dark mode + new fonts = chef's kiss"},
    {"id": 25, "sentiment": "negative", "text": "Roll back please. Old version worked fine."},
    {"id": 26, "sentiment": "negative", "text": "Support volume must be through the roof"},
    {"id": 27, "sentiment": "positive", "text": "Checkout conversion improved for me"},
    {"id": 28, "sentiment": "neutral", "text": "Mixed feelings. Some good, some bad."},
    {"id": 29, "sentiment": "negative", "text": "App unusable on older devices now"},
    {"id": 30, "sentiment": "negative", "text": "Crash rate is unacceptable"},
    {"id": 31, "sentiment": "positive", "text": "New API feels snappy when it works"},
    {"id": 32, "sentiment": "negative", "text": "Lost payment once. Scared to try again."},
    {"id": 33, "sentiment": "positive", "text": "Adoption was easy. Like the changes."},
    {"id": 34, "sentiment": "negative", "text": "Retention will tank if crashes continue"},
    {"id": 35, "sentiment": "negative", "text": "Churning after this. Too many problems."}
]

# ===== RELEASE NOTES =====
release_notes = """
PurpleMerit Feature Launch - v3.2.0 "Merit Boost"
Release Date: Jan 14, 2025

Changes:
- Complete UI redesign with dark mode support
- New recommendation engine (ML-based)
- Faster checkout flow with one-click option
- Updated API endpoints (v2)

Known Issues (pre-launch):
- Minor memory leak on Android API 30+ (monitoring)
- Occasional timeout on high-traffic checkout (<1% of requests)
- Dark mode toggle requires app restart on iOS 15

Risk Assessment:
- Medium risk due to UI overhaul
- Recommendation engine may need tuning for cold-start users
"""

# Export
def get_dashboard_data():
    return {
        "metrics_df": metrics_df,
        "user_feedback": user_feedback,
        "release_notes": release_notes,
        "launch_date": launch_date
    }