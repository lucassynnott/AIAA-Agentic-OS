#!/usr/bin/env python3
"""
A/B Test Analyzer - Analyze A/B test results and provide recommendations.

Usage:
    python3 execution/generate_ab_test_analysis.py \
        --control '{"visitors": 1000, "conversions": 50}' \
        --variant '{"visitors": 1000, "conversions": 65}' \
        --output .tmp/ab_analysis.md
"""

import argparse, json, math, sys
from datetime import datetime
from pathlib import Path

def calculate_confidence(control, variant):
    """Calculate statistical significance."""
    n1, c1 = control["visitors"], control["conversions"]
    n2, c2 = variant["visitors"], variant["conversions"]
    
    p1 = c1 / n1 if n1 > 0 else 0
    p2 = c2 / n2 if n2 > 0 else 0
    
    # Pooled probability
    p_pool = (c1 + c2) / (n1 + n2) if (n1 + n2) > 0 else 0
    
    # Standard error
    se = math.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2)) if p_pool > 0 and p_pool < 1 else 0
    
    # Z-score
    z = (p2 - p1) / se if se > 0 else 0
    
    # Approximate confidence (simplified)
    if abs(z) >= 2.58: confidence = 99
    elif abs(z) >= 1.96: confidence = 95
    elif abs(z) >= 1.65: confidence = 90
    elif abs(z) >= 1.28: confidence = 80
    else: confidence = int(abs(z) * 40)
    
    return {
        "control_rate": round(p1 * 100, 2),
        "variant_rate": round(p2 * 100, 2),
        "lift": round((p2 - p1) / p1 * 100, 2) if p1 > 0 else 0,
        "z_score": round(z, 2),
        "confidence": confidence,
        "significant": confidence >= 95
    }

def main():
    parser = argparse.ArgumentParser(description="Analyze A/B test results")
    parser.add_argument("--control", "-c", required=True, help="Control group JSON")
    parser.add_argument("--variant", "-v", required=True, help="Variant group JSON")
    parser.add_argument("--test_name", "-n", default="A/B Test", help="Test name")
    parser.add_argument("--output", "-o", default=".tmp/ab_analysis.md")
    args = parser.parse_args()

    try:
        control = json.loads(args.control)
        variant = json.loads(args.variant)
    except:
        print("Error: Invalid JSON")
        return 1

    print(f"\n📊 A/B Test Analyzer\n   Test: {args.test_name}\n")

    results = calculate_confidence(control, variant)

    # Determine recommendation
    if results["significant"]:
        if results["lift"] > 0:
            recommendation = "✅ WINNER: Implement variant - statistically significant improvement"
        else:
            recommendation = "❌ LOSER: Keep control - variant performed worse"
    else:
        recommendation = "⏳ INCONCLUSIVE: Need more data or the difference is not significant"

    output = f"""# A/B Test Analysis: {args.test_name}

**Date:** {datetime.now().strftime("%Y-%m-%d")}

---

## Results Summary

| Metric | Control | Variant |
|--------|---------|---------|
| Visitors | {control['visitors']:,} | {variant['visitors']:,} |
| Conversions | {control['conversions']:,} | {variant['conversions']:,} |
| Conversion Rate | {results['control_rate']}% | {results['variant_rate']}% |

---

## Statistical Analysis

- **Lift:** {results['lift']}%
- **Z-Score:** {results['z_score']}
- **Confidence Level:** {results['confidence']}%
- **Statistically Significant:** {'Yes ✓' if results['significant'] else 'No'}

---

## Recommendation

{recommendation}

---

## Interpretation Guide

- **95%+ confidence:** Safe to implement
- **90-95% confidence:** Likely real effect, consider more data
- **<90% confidence:** Not enough evidence, keep testing

---

## Next Steps

{'1. Implement the winning variant\n2. Document learnings\n3. Plan next test' if results['significant'] else '1. Continue running the test\n2. Consider increasing sample size\n3. Review test hypothesis'}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")

    print(f"   Control: {results['control_rate']}% → Variant: {results['variant_rate']}%")
    print(f"   Lift: {results['lift']}% | Confidence: {results['confidence']}%")
    print(f"\n{recommendation}")
    print(f"\n✅ Analysis saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
