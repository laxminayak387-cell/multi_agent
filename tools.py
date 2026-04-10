"""Tool functions for agents to use."""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from collections import Counter
import re

def aggregate_metrics(metrics_df: pd.DataFrame, metric_names: List[str] = None) -> Dict[str, Any]:
    """
    Aggregate metrics with pre/post launch comparison.
    Returns summary statistics and deltas.
    """
    if metric_names is None:
        metric_names = ['activation_rate_pct', 'dau_wau_ratio', 'd1_retention_pct',
                        'crash_rate_pct', 'api_latency_p95_ms', 'payment_success_rate_pct',
                        'support_ticket_volume', 'feature_adoption_pct', 'churn_rate_pct']
    
    n = len(metrics_df)
    split = n // 2  # pre/post launch split
    
    pre_launch = metrics_df.iloc[:split]
    post_launch = metrics_df.iloc[split:]
    
    results = {}
    for metric in metric_names:
        if metric in metrics_df.columns:
            pre_mean = pre_launch[metric].mean()
            post_mean = post_launch[metric].mean()
            delta = post_mean - pre_mean
            delta_pct = (delta / pre_mean) * 100 if pre_mean != 0 else 0
            
            results[metric] = {
                "pre_launch_mean": round(pre_mean, 2),
                "post_launch_mean": round(post_mean, 2),
                "delta": round(delta, 2),
                "delta_pct": round(delta_pct, 1),
                "trend": "up" if delta > 0 else "down"
            }
    
    return results

def detect_anomalies(metrics_df: pd.DataFrame, metric: str, threshold_sigma: float = 2.0) -> List[Dict]:
    """
    Detect anomalous days using z-score method.
    Returns list of anomalies with dates and values.
    """
    if metric not in metrics_df.columns:
        return []
    
    values = metrics_df[metric].values
    mean = np.mean(values)
    std = np.std(values)
    
    anomalies = []
    for idx, val in enumerate(values):
        z_score = abs((val - mean) / std) if std > 0 else 0
        if z_score > threshold_sigma:
            anomalies.append({
                "date": metrics_df.iloc[idx]['date'].strftime('%Y-%m-%d'),
                "value": round(val, 2),
                "z_score": round(z_score, 2),
                "severity": "high" if z_score > 3 else "medium"
            })
    
    return anomalies

def sentiment_summary(feedback: List[Dict]) -> Dict[str, Any]:
    """
    Analyze user feedback sentiment and extract themes.
    """
    sentiments = [f['sentiment'] for f in feedback]
    sentiment_counts = Counter(sentiments)
    
    # Extract key themes
    crash_keywords = ['crash', 'crashes', 'crashing']
    payment_keywords = ['payment', 'pay', 'checkout']
    latency_keywords = ['slow', 'latency', 'loading', 'time']
    
    themes = {
        "crashes": 0,
        "payment_issues": 0,
        "latency_issues": 0,
        "positive_features": 0
    }
    
    for f in feedback:
        text_lower = f['text'].lower()
        if any(kw in text_lower for kw in crash_keywords):
            themes["crashes"] += 1
        if any(kw in text_lower for kw in payment_keywords):
            themes["payment_issues"] += 1
        if any(kw in text_lower for kw in latency_keywords):
            themes["latency_issues"] += 1
        if f['sentiment'] == 'positive':
            themes["positive_features"] += 1
    
    return {
        "total_feedback": len(feedback),
        "sentiment_distribution": dict(sentiment_counts),
        "positive_pct": round(sentiment_counts.get('positive', 0) / len(feedback) * 100, 1),
        "negative_pct": round(sentiment_counts.get('negative', 0) / len(feedback) * 100, 1),
        "themes": themes,
        "sample_positive": [f['text'] for f in feedback if f['sentiment'] == 'positive'][:3],
        "sample_negative": [f['text'] for f in feedback if f['sentiment'] == 'negative'][:5]
    }

def trend_comparison(metrics_df: pd.DataFrame, metric: str, window: int = 3) -> Dict:
    """
    Compare recent trend vs baseline.
    """
    if metric not in metrics_df.columns:
        return {}
    
    recent = metrics_df[metric].iloc[-window:].mean()
    baseline = metrics_df[metric].iloc[:window].mean()
    change = ((recent - baseline) / baseline) * 100 if baseline != 0 else 0
    
    return {
        "metric": metric,
        "recent_avg": round(recent, 2),
        "baseline_avg": round(baseline, 2),
        "change_pct": round(change, 1),
        "status": "critical" if abs(change) > 30 else "warning" if abs(change) > 15 else "normal"
    }