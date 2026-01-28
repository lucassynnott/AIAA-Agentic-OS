#!/usr/bin/env python3
"""
Churn Risk Alert - Identify clients at risk of churning.

Usage:
    python3 execution/alert_churn_risk.py \
        --clients clients.json \
        --output .tmp/churn_alerts.json
"""

import argparse, json, sys
from datetime import datetime
from pathlib import Path

def calculate_churn_risk(client):
    """Calculate churn risk score based on signals."""
    risk_score = 0
    signals = []
    
    # Low engagement
    engagement = client.get("engagement_score", 50)
    if engagement < 30:
        risk_score += 30
        signals.append("Very low engagement")
    elif engagement < 50:
        risk_score += 15
        signals.append("Below average engagement")
    
    # Support tickets
    tickets = client.get("support_tickets_30d", 0)
    if tickets > 5:
        risk_score += 25
        signals.append(f"High support volume ({tickets} tickets)")
    elif tickets > 3:
        risk_score += 10
        signals.append("Elevated support requests")
    
    # Usage decline
    usage_change = client.get("usage_change_pct", 0)
    if usage_change < -30:
        risk_score += 30
        signals.append(f"Significant usage drop ({usage_change}%)")
    elif usage_change < -10:
        risk_score += 15
        signals.append("Declining usage")
    
    # Payment issues
    if client.get("payment_status") == "overdue":
        risk_score += 20
        signals.append("Payment overdue")
    elif client.get("payment_status") == "late":
        risk_score += 10
        signals.append("Late payment history")
    
    # NPS/Satisfaction
    nps = client.get("nps_score", 7)
    if nps <= 3:
        risk_score += 25
        signals.append(f"Low NPS ({nps})")
    elif nps <= 5:
        risk_score += 10
        signals.append("Below average NPS")
    
    # Contract ending soon
    days_to_renewal = client.get("days_to_renewal", 365)
    if days_to_renewal < 30:
        risk_score += 15
        signals.append(f"Contract ends in {days_to_renewal} days")
    
    # Determine risk level
    if risk_score >= 60:
        level = "critical"
        action = "Immediate executive outreach required"
    elif risk_score >= 40:
        level = "high"
        action = "Schedule urgent check-in call"
    elif risk_score >= 20:
        level = "medium"
        action = "Proactive engagement recommended"
    else:
        level = "low"
        action = "Continue normal engagement"
    
    return {
        "risk_score": min(100, risk_score),
        "risk_level": level,
        "signals": signals,
        "recommended_action": action
    }

def main():
    parser = argparse.ArgumentParser(description="Identify churn risks")
    parser.add_argument("--clients", "-c", required=True, help="Clients JSON file")
    parser.add_argument("--threshold", "-t", type=int, default=40, help="Alert threshold")
    parser.add_argument("--output", "-o", default=".tmp/churn_alerts.json")
    args = parser.parse_args()

    with open(args.clients) as f:
        clients = json.load(f)
        if isinstance(clients, dict):
            clients = clients.get("clients", [clients])

    print(f"\n⚠️ Churn Risk Analyzer\n   Clients: {len(clients)}\n   Threshold: {args.threshold}\n")

    results = []
    for client in clients:
        risk = calculate_churn_risk(client)
        results.append({
            "client": client.get("name", client.get("company", "Unknown")),
            "mrr": client.get("mrr", 0),
            **risk
        })

    # Sort by risk
    results.sort(key=lambda x: x["risk_score"], reverse=True)
    at_risk = [r for r in results if r["risk_score"] >= args.threshold]

    output = {
        "analyzed_at": datetime.now().isoformat(),
        "total_clients": len(clients),
        "at_risk_count": len(at_risk),
        "risk_summary": {
            "critical": len([r for r in results if r["risk_level"] == "critical"]),
            "high": len([r for r in results if r["risk_level"] == "high"]),
            "medium": len([r for r in results if r["risk_level"] == "medium"]),
            "low": len([r for r in results if r["risk_level"] == "low"])
        },
        "at_risk_clients": at_risk,
        "all_results": results
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    print(f"   🔴 Critical: {output['risk_summary']['critical']}")
    print(f"   🟠 High: {output['risk_summary']['high']}")
    print(f"   🟡 Medium: {output['risk_summary']['medium']}")
    print(f"   🟢 Low: {output['risk_summary']['low']}")
    print(f"\n✅ Analysis saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
