#!/usr/bin/env python3
"""
Client Health Score Calculator - Calculate health scores for client accounts.

Usage:
    python3 execution/calculate_client_health.py \
        --client "Acme Corp" \
        --metrics '{"engagement": 80, "nps": 7, "usage": 60, "support_tickets": 2}' \
        --output .tmp/health_score.json
"""

import argparse, json, sys
from datetime import datetime
from pathlib import Path

def calculate_health_score(metrics):
    """Calculate weighted health score from metrics."""
    weights = {
        "engagement": 0.25,      # How often they engage
        "nps": 0.20,             # Net promoter score (1-10)
        "usage": 0.20,           # Product usage %
        "support_tickets": 0.15, # Lower is better
        "payment_status": 0.10,  # On-time payments
        "growth": 0.10           # Account growth
    }
    
    score = 0
    factors = []
    
    # Engagement (0-100)
    if "engagement" in metrics:
        eng = min(100, max(0, metrics["engagement"]))
        score += eng * weights["engagement"]
        factors.append({"name": "Engagement", "value": eng, "weight": weights["engagement"]})
    
    # NPS (1-10 -> 0-100)
    if "nps" in metrics:
        nps = min(10, max(1, metrics["nps"])) * 10
        score += nps * weights["nps"]
        factors.append({"name": "NPS", "value": nps, "weight": weights["nps"]})
    
    # Usage (0-100)
    if "usage" in metrics:
        usage = min(100, max(0, metrics["usage"]))
        score += usage * weights["usage"]
        factors.append({"name": "Usage", "value": usage, "weight": weights["usage"]})
    
    # Support tickets (inverse - fewer is better)
    if "support_tickets" in metrics:
        tickets = metrics["support_tickets"]
        ticket_score = max(0, 100 - (tickets * 10))  # -10 points per ticket
        score += ticket_score * weights["support_tickets"]
        factors.append({"name": "Support", "value": ticket_score, "weight": weights["support_tickets"]})
    
    # Payment (0 or 100)
    if "payment_status" in metrics:
        payment = 100 if metrics["payment_status"] == "current" else 50 if metrics["payment_status"] == "late" else 0
        score += payment * weights["payment_status"]
        factors.append({"name": "Payment", "value": payment, "weight": weights["payment_status"]})
    
    # Growth (-100 to 100 -> 0-100)
    if "growth" in metrics:
        growth = min(100, max(-100, metrics["growth"]))
        growth_score = (growth + 100) / 2  # Normalize to 0-100
        score += growth_score * weights["growth"]
        factors.append({"name": "Growth", "value": growth_score, "weight": weights["growth"]})
    
    # Determine status
    if score >= 80:
        status = "healthy"
        action = "Maintain relationship, upsell opportunities"
    elif score >= 60:
        status = "stable"
        action = "Monitor closely, increase engagement"
    elif score >= 40:
        status = "at_risk"
        action = "Immediate outreach, identify issues"
    else:
        status = "critical"
        action = "Urgent intervention required"
    
    return {
        "score": round(score, 1),
        "status": status,
        "recommended_action": action,
        "factors": factors
    }

def main():
    parser = argparse.ArgumentParser(description="Calculate client health score")
    parser.add_argument("--client", "-c", required=True)
    parser.add_argument("--metrics", "-m", required=True, help="JSON metrics object")
    parser.add_argument("--output", "-o", default=".tmp/health_score.json")
    args = parser.parse_args()

    try:
        metrics = json.loads(args.metrics)
    except:
        print("Error: Invalid JSON for metrics")
        return 1

    print(f"\n💚 Client Health Calculator\n   Client: {args.client}\n")

    result = calculate_health_score(metrics)
    
    output = {
        "calculated_at": datetime.now().isoformat(),
        "client": args.client,
        "input_metrics": metrics,
        **result
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    status_icons = {"healthy": "💚", "stable": "💛", "at_risk": "🟠", "critical": "🔴"}
    print(f"   {status_icons[result['status']]} Score: {result['score']}/100")
    print(f"   Status: {result['status'].upper()}")
    print(f"   Action: {result['recommended_action']}")
    print(f"\n✅ Saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
