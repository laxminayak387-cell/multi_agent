"""Agent definitions for the war room."""

from typing import Dict, Any, List
import json

class ProductManagerAgent:
    """Defines success criteria and makes go/no-go framing."""
    
    def __init__(self, tools):
        self.tools = tools
        self.name = "Product Manager"
    
    def analyze(self, dashboard: Dict) -> Dict:
        """Analyze from PM perspective."""
        metrics_summary = self.tools['aggregate_metrics'](dashboard['metrics_df'])
        sentiment = self.tools['sentiment_summary'](dashboard['user_feedback'])
        
        # Define success criteria
        success_criteria = {
            "crash_rate_acceptable": metrics_summary['crash_rate_pct']['post_launch_mean'] < 1.5,
            "retention_maintained": metrics_summary['d1_retention_pct']['delta_pct'] > -10,
            "payment_success_acceptable": metrics_summary['payment_success_rate_pct']['post_launch_mean'] > 98,
            "positive_sentiment_minimum": sentiment['positive_pct'] > 25
        }
        
        # Decision framing
        critical_failures = []
        if not success_criteria['crash_rate_acceptable']:
            critical_failures.append(f"Crash rate {metrics_summary['crash_rate_pct']['post_launch_mean']:.1f}% exceeds threshold")
        if not success_criteria['payment_success_acceptable']:
            critical_failures.append("Payment success rate below 98%")
        
        recommendation = "PAUSE" if len(critical_failures) >= 1 else "PROCEED"
        
        return {
            "agent": self.name,
            "success_criteria_met": success_criteria,
            "critical_failures": critical_failures,
            "user_impact_assessment": f"Negative sentiment at {sentiment['negative_pct']}% is high; {sentiment['themes']['crashes']} crash reports",
            "recommendation": recommendation,
            "confidence": 70 if recommendation == "PAUSE" else 85
        }


class DataAnalystAgent:
    """Analyzes quantitative metrics and anomalies."""
    
    def __init__(self, tools):
        self.tools = tools
        self.name = "Data Analyst"
    
    def analyze(self, dashboard: Dict) -> Dict:
        """Analyze data perspective."""
        metrics_summary = self.tools['aggregate_metrics'](dashboard['metrics_df'])
        
        # Detect anomalies for key metrics
        anomalies = {}
        for metric in ['crash_rate_pct', 'api_latency_p95_ms', 'support_ticket_volume']:
            anomalies[metric] = self.tools['detect_anomalies'](dashboard['metrics_df'], metric)
        
        # Trend comparisons
        trends = {}
        for metric in ['crash_rate_pct', 'd1_retention_pct', 'payment_success_rate_pct']:
            trends[metric] = self.tools['trend_comparison'](dashboard['metrics_df'], metric)
        
        # Identify most concerning metric
        metric_status = {}
        for metric, data in metrics_summary.items():
            metric_status[metric] = {
                "delta_pct": data['delta_pct'],
                "alert_level": "red" if abs(data['delta_pct']) > 25 else "yellow" if abs(data['delta_pct']) > 10 else "green"
            }
        
        return {
            "agent": self.name,
            "metrics_summary": metrics_summary,
            "anomalies": {k: v for k, v in anomalies.items() if v},
            "trends": trends,
            "metric_status": metric_status,
            "key_finding": f"Critical regression: crash rate +{metrics_summary['crash_rate_pct']['delta_pct']:.0f}%, "
                          f"latency +{metrics_summary['api_latency_p95_ms']['delta_pct']:.0f}%, "
                          f"tickets +{metrics_summary['support_ticket_volume']['delta_pct']:.0f}%",
            "confidence": 95
        }


class MarketingCommsAgent:
    """Assesses messaging and customer perception."""
    
    def __init__(self, tools):
        self.tools = tools
        self.name = "Marketing/Comms"
    
    def analyze(self, dashboard: Dict) -> Dict:
        """Analyze comms perspective."""
        sentiment = self.tools['sentiment_summary'](dashboard['user_feedback'])
        
        # Assess narrative risk
        narrative_risk = "high" if sentiment['negative_pct'] > 40 else "medium" if sentiment['negative_pct'] > 25 else "low"
        
        # Communication actions needed
        comms_actions = []
        if sentiment['themes']['crashes'] > 10:
            comms_actions.append("Acknowledge stability issues publicly")
        if sentiment['themes']['payment_issues'] > 5:
            comms_actions.append("Address payment failure concerns with customer support script")
        if sentiment['negative_pct'] > 30:
            comms_actions.append("Prepare apology/explanation email for affected users")
        
        return {
            "agent": self.name,
            "sentiment_analysis": sentiment,
            "narrative_risk": narrative_risk,
            "recommended_comms": comms_actions,
            "customer_perception": f"{sentiment['positive_pct']}% positive / {sentiment['negative_pct']}% negative",
            "confidence": 80
        }


class RiskCriticAgent:
    """Challenges assumptions and highlights risks."""
    
    def __init__(self, tools):
        self.tools = tools
        self.name = "Risk/Critic"
    
    def analyze(self, dashboard: Dict, other_agents_outputs: Dict = None) -> Dict:
        """Identify risks and challenge assumptions."""
        metrics_summary = self.tools['aggregate_metrics'](dashboard['metrics_df'])
        
        risks = []
        
        # Technical risks
        if metrics_summary['crash_rate_pct']['post_launch_mean'] > 2:
            risks.append({
                "risk": "Continued high crash rate will accelerate user churn",
                "severity": "high",
                "mitigation": "Roll back to previous stable version or deploy hotfix within 4 hours"
            })
        
        if metrics_summary['api_latency_p95_ms']['post_launch_mean'] > 200:
            risks.append({
                "risk": "Poor API performance driving negative user experience",
                "severity": "medium",
                "mitigation": "Scale backend resources and optimize critical paths"
            })
        
        # Business risks
        if metrics_summary['churn_rate_pct']['post_launch_mean'] > 1.2:
            risks.append({
                "risk": "Elevated churn will impact LTV and revenue targets",
                "severity": "high",
                "mitigation": "Proactive outreach to at-risk users with retention offers"
            })
        
        # Challenging assumptions
        challenges = [
            "Assumption that feature adoption will recover without intervention may be false",
            "Payment success dip may indicate deeper integration issue, not transient",
            "Support ticket volume suggests scale of problem larger than metrics show"
        ]
        
        # Evidence needed
        evidence_needed = [
            "Root cause analysis of crash patterns by device/OS",
            "Payment failure breakdown by error type",
            "Retention cohort analysis by feature adoption"
        ]
        
        # Final recommendation based on risk
        high_risks = [r for r in risks if r['severity'] == 'high']
        if len(high_risks) >= 2:
            recommendation = "ROLL_BACK"
        elif len(high_risks) == 1:
            recommendation = "PAUSE"
        else:
            recommendation = "PROCEED"
        
        return {
            "agent": self.name,
            "identified_risks": risks,
            "assumptions_challenged": challenges,
            "evidence_requested": evidence_needed,
            "recommendation": recommendation,
            "confidence": 75
        }