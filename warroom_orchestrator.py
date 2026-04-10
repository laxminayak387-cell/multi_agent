"""Main orchestrator for the multi-agent war room system."""

import json
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, List

from mock_dashboard_data import get_dashboard_data
from tools import aggregate_metrics, detect_anomalies, sentiment_summary, trend_comparison
from agents import ProductManagerAgent, DataAnalystAgent, MarketingCommsAgent, RiskCriticAgent


class WarRoomOrchestrator:
    """Coordinates the multi-agent decision-making process."""
    
    def __init__(self):
        self.dashboard = get_dashboard_data()
        self.tools = {
            'aggregate_metrics': aggregate_metrics,
            'detect_anomalies': detect_anomalies,
            'sentiment_summary': sentiment_summary,
            'trend_comparison': trend_comparison
        }
        
        # Initialize agents
        self.agents = {
            'pm': ProductManagerAgent(self.tools),
            'analyst': DataAnalystAgent(self.tools),
            'comms': MarketingCommsAgent(self.tools),
            'risk': RiskCriticAgent(self.tools)
        }
        
        self.traces = []
    
    def _log(self, step: str, agent: str, content: str):
        """Log agent activity for traceability."""
        trace = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "agent": agent,
            "content": content
        }
        self.traces.append(trace)
        print(f"[{step.upper()}] {agent}: {content[:150]}...")
    
    def run(self) -> Dict:
        """Execute the war room process and return final decision."""
        print("\n" + "="*60)
        print("PURPLEMERIT WAR ROOM - LAUNCH DECISION SYSTEM")
        print("="*60 + "\n")
        
        # Step 1: Data Analyst presents metrics
        self._log("analysis", "Data Analyst", "Analyzing metrics and detecting anomalies...")
        analyst_output = self.agents['analyst'].analyze(self.dashboard)
        print(f"\n Data Analyst Findings:")
        print(f"   Key finding: {analyst_output['key_finding']}")
        
        # Step 2: Product Manager frames success criteria
        self._log("analysis", "Product Manager", "Evaluating against success criteria...")
        pm_output = self.agents['pm'].analyze(self.dashboard)
        print(f"\n Product Manager Assessment:")
        print(f"   Critical failures: {pm_output['critical_failures']}")
        print(f"   Recommendation: {pm_output['recommendation']}")
        
        # Step 3: Marketing/Comms assesses perception
        self._log("analysis", "Marketing/Comms", "Analyzing user sentiment...")
        comms_output = self.agents['comms'].analyze(self.dashboard)
        print(f"\n Marketing/Comms Assessment:")
        print(f"   Sentiment: {comms_output['customer_perception']}")
        print(f"   Narrative risk: {comms_output['narrative_risk']}")
        
        # Step 4: Risk/Critic challenges and identifies risks
        self._log("analysis", "Risk/Critic", "Identifying risks and challenging assumptions...")
        risk_output = self.agents['risk'].analyze(self.dashboard)
        print(f"\n Risk/Critic Assessment:")
        print(f"   High risks: {len([r for r in risk_output['identified_risks'] if r['severity'] == 'high'])}")
        print(f"   Recommendation: {risk_output['recommendation']}")
        
        # Step 5: Orchestrator synthesizes final decision
        self._log("synthesis", "Orchestrator", "Synthesizing agent outputs for final decision...")
        
        # Weighted voting mechanism
        votes = {
            "PROCEED": 0,
            "PAUSE": 0,
            "ROLL_BACK": 0
        }
        
        votes[pm_output['recommendation']] += 1
        votes[risk_output['recommendation']] += 1
        
        # Data analyst doesn't vote but provides evidence
        # Marketing/Comms provides context but doesn't vote on technical go/no-go
        
        # Check critical metrics
        metrics = analyst_output['metrics_summary']
        crash_spike = metrics['crash_rate_pct']['delta_pct'] > 100
        latency_spike = metrics['api_latency_p95_ms']['delta_pct'] > 50
        churn_spike = metrics['churn_rate_pct']['delta_pct'] > 50
        
        if crash_spike and latency_spike:
            votes["ROLL_BACK"] += 2
        elif crash_spike or churn_spike:
            votes["PAUSE"] += 1
        
        # Final decision
        final_decision = max(votes, key=votes.get)
        
        # Confidence score
        confidence_base = 70
        if final_decision == "ROLL_BACK":
            confidence_base = 85
        elif final_decision == "PAUSE":
            confidence_base = 75
        
        # Adjust confidence based on data quality
        sentiment = self.tools['sentiment_summary'](self.dashboard['user_feedback'])
        if sentiment['negative_pct'] > 50:
            confidence_base += 5
        
        # Build final output
        final_output = self._build_final_output(
            decision=final_decision,
            votes=votes,
            pm_output=pm_output,
            analyst_output=analyst_output,
            comms_output=comms_output,
            risk_output=risk_output,
            confidence=confidence_base
        )
        
        self._log("final", "Orchestrator", f"Decision: {final_decision}")
        
        return final_output
    
    def _build_final_output(self, decision: str, votes: Dict, pm_output: Dict,
                           analyst_output: Dict, comms_output: Dict, risk_output: Dict,
                           confidence: int) -> Dict:
        """Build the structured JSON output."""
        
        metrics = analyst_output['metrics_summary']
        sentiment = comms_output['sentiment_analysis']
        
        # Rationale
        rationale = {
            "primary_driver": f"Crash rate increased by {metrics['crash_rate_pct']['delta_pct']:.0f}% post-launch",
            "metric_references": {
                "crash_rate": f"{metrics['crash_rate_pct']['post_launch_mean']:.1f}% (was {metrics['crash_rate_pct']['pre_launch_mean']:.1f}%)",
                "d1_retention": f"{metrics['d1_retention_pct']['post_launch_mean']:.1f}% (delta: {metrics['d1_retention_pct']['delta_pct']:.0f}%)",
                "support_tickets": f"{metrics['support_ticket_volume']['post_launch_mean']:.0f}/day (was {metrics['support_ticket_volume']['pre_launch_mean']:.0f})"
            },
            "feedback_summary": f"{sentiment['negative_pct']}% negative feedback; {sentiment['themes']['crashes']} crash reports",
            "vote_tally": votes
        }
        
        # Risk register
        risk_register = []
        for risk in risk_output['identified_risks'][:3]:
            risk_register.append({
                "risk": risk['risk'],
                "severity": risk['severity'],
                "mitigation": risk['mitigation'],
                "owner": "Engineering" if "crash" in risk['risk'].lower() else "Product"
            })
        
        # Action plan (24-48 hours)
        action_plan = []
        if decision in ["PAUSE", "ROLL_BACK"]:
            action_plan.append({
                "action": "Immediately halt further rollout to new users",
                "owner": "Engineering",
                "timeframe": "0-2 hours"
            })
            action_plan.append({
                "action": "Root cause analysis of crash spike by device/OS",
                "owner": "Engineering",
                "timeframe": "4-8 hours"
            })
        
        action_plan.append({
            "action": "Deploy crash rate hotfix or roll back to v3.1",
            "owner": "Engineering",
            "timeframe": "12-24 hours"
        })
        action_plan.append({
            "action": "Update status page and prepare customer comms",
            "owner": "Marketing/Comms",
            "timeframe": "2-4 hours"
        })
        action_plan.append({
            "action": "Review payment failure logs with payment provider",
            "owner": "Product",
            "timeframe": "24 hours"
        })
        
        # Communication plan
        comms_plan = {
            "internal": [
                "Slack #eng-alerts: Current crash rate and mitigation status",
                "Daily war room standup at 10am until resolved",
                "Post-mortem scheduled for end of week"
            ],
            "external": [
                "Status page incident report: 'Performance degradation under investigation'",
                "If decision is PAUSE/ROLLBACK: Email to affected users acknowledging issues",
                "Support team script for crash/payment complaints"
            ]
        }
        
        if decision == "PROCEED":
            comms_plan["external"] = [
                "Continue normal marketing cadence",
                "Monitor social sentiment and respond to negative feedback individually",
                "Highlight positive features in next newsletter"
            ]
        
        # Confidence and next steps
        confidence_increase = {
            "would_increase_confidence": [
                "Root cause analysis of crash pattern completed",
                "48 hours of stable metrics post-fix",
                "Payment success rate returns to 99%+",
                "Support ticket volume decreases by 50%"
            ]
        }
        
        return {
            "decision": decision,
            "rationale": rationale,
            "risk_register": risk_register,
            "action_plan": action_plan,
            "communication_plan": comms_plan,
            "confidence_score": confidence,
            "confidence_increase": confidence_increase,
            "timestamp": datetime.now().isoformat(),
            "agents_consulted": list(self.agents.keys())
        }


def main():
    """Entry point for the war room system."""
    print(" Starting PurpleMerit War Room System...")
    print(" Loading dashboard data...")
    
    orchestrator = WarRoomOrchestrator()
    result = orchestrator.run()
    
    print("\n" + "="*60)
    print("FINAL DECISION OUTPUT")
    print("="*60)
    print(json.dumps(result, indent=2, default=str))
    
    # Also save to file
    with open("war_room_decision.json", "w") as f:
        json.dump(result, f, indent=2, default=str)
    
    print("\n Decision saved to war_room_decision.json")
    
    # Print trace summary
    print("\n" + "="*60)
    print("TRACE SUMMARY (Agent Steps)")
    print("="*60)
    for trace in orchestrator.traces:
        print(f"[{trace['timestamp'][11:19]}] {trace['agent']}: {trace['content'][:80]}...")
    
    return result


if __name__ == "__main__":
    main()