# Segment Email List - Complete Segmentation Strategy & Implementation

Expert skill for creating and using email list segments to send targeted, relevant content that increases engagement and revenue.

## Why Segmentation Matters

Segmented campaigns outperform batch-and-blast by 760% in revenue (according to industry data).

**Benefits**:
- **Higher Open Rates**: 14-20% increase
- **Better Click Rates**: 50-100% increase
- **More Revenue**: 2-3x per campaign
- **Lower Unsubscribes**: Send relevant content only
- **Better Deliverability**: Higher engagement = better sender reputation

## Segmentation in Klaviyo

### Lists vs. Segments

**Lists** (Static):
- Manually managed groups
- People stay until removed
- Examples: Newsletter, VIP, SMS Subscribers
- Use for: Main subscriber list, opt-in groups

**Segments** (Dynamic):
- Automatically updated based on conditions
- People enter/exit as they meet/don't meet criteria
- Examples: Engaged 60 Days, Cart Abandoners, VIP Customers
- Use for: Campaign targeting, flow triggers, analysis

**Best Practice**: One main list (Newsletter), multiple segments for targeting

## Core Engagement Segments

### 1. Engaged 60 Days

**Purpose**: Only send to people who want your emails
**Use for**: All campaigns (protects deliverability)

**Klaviyo Setup**:
```
Name: "Engaged 60 Days"

Definition:
Someone is in Newsletter list
AND
(Opened email at least once in last 60 days
OR Clicked email at least once in last 60 days
OR Placed order at least once in last 60 days
OR Subscribed to list in last 30 days)
```

**Why This Works**:
- ISPs reward sending to engaged users
- Reduces spam complaints
- Improves deliverability
- Higher conversion rates

### 2. Engaged 90 Days

**Purpose**: Slightly broader audience
**Use for**: Big announcements, sales, launches

```
Name: "Engaged 90 Days"

Same as 60 days but:
- 90 day window instead of 60
- Includes more people
- Slightly lower engagement but more reach
```

### 3. Unengaged / Sunset

**Purpose**: Identify people to remove or re-engage
**Use for**: Winback campaigns, list cleaning

```
Name: "Unengaged 90+ Days"

Definition:
Someone is in Newsletter list
AND
Has NOT opened email in last 90 days
AND
Has NOT clicked email in last 90 days
AND
Has NOT placed order in last 90 days
```

**Action**:
- Send winback campaign ("We miss you + 15% off")
- If still no engagement after 30 days: Suppress from sends
- Keeps list healthy and deliverability high

## Customer Lifecycle Segments

### 4. Never Purchased

**Purpose**: Convert subscribers to first-time customers
**Use for**: Conversion-focused campaigns with offers

```
Name: "Never Purchased"

Definition:
Someone is in Newsletter list
AND
Placed order exactly zero times (all time)
```

**Campaign Ideas**:
- First purchase incentives
- Educational content
- Social proof
- Customer success stories
- Time-limited discounts

### 5. One-Time Buyers

**Purpose**: Drive second purchase (critical for LTV)
**Use for**: Cross-sell, repeat purchase incentives

```
Name: "One-Time Buyers"

Definition:
Placed order exactly 1 time (all time)
AND
Last order was at least 14 days ago
```

**Campaign Ideas**:
- "We miss you" offers
- Complementary products
- Exclusive "returning customer" deals
- Product education
- Loyalty program invites

### 6. Repeat Customers (2-4 purchases)

**Purpose**: Nurture into VIP status
**Use for**: Building loyalty, exclusive content

```
Name: "Repeat Customers"

Definition:
Placed order at least 2 times (all time)
AND
Placed order at most 4 times (all time)
```

**Campaign Ideas**:
- Early access to sales
- VIP program invitations
- Product previews
- "Thank you" campaigns
- Referral incentives

### 7. VIP Customers (5+ purchases or high LTV)

**Purpose**: Retain best customers, maximize LTV
**Use for**: White-glove treatment, best offers

```
Name: "VIP Customers"

Definition:
Placed order at least 5 times (all time)
OR
Lifetime value greater than $500
```

**Campaign Ideas**:
- Exclusive sales
- First access to new products
- Personal thank you from founder
- Premium customer service
- VIP-only products
- Highest discounts

## Behavioral Segments

### 8. Active Browsers (Past 7 Days)

**Purpose**: Capture high-intent visitors
**Use for**: Browsing-related campaigns, new arrivals

```
Name: "Active Browsers - 7 Days"

Definition:
Active on site at least once in last 7 days
AND
Has NOT placed order in last 7 days
```

**Campaign Ideas**:
- "We noticed you were browsing..."
- Products they viewed
- Similar product recommendations
- Limited-time offers
- Free shipping incentives

### 9. Cart Abandoners (Active)

**Purpose**: Supplement automated cart flow
**Use for**: Flash sales, shipping promotions

```
Name: "Recent Cart Abandoners"

Definition:
Added to cart at least once in last 14 days
AND
Placed order zero times in last 14 days
```

**Campaign Ideas**:
- Free shipping announcements
- Cart-specific discount codes
- Product restocks
- Low inventory alerts

### 10. Product Category Interest

**Purpose**: Send hyper-relevant product campaigns
**Use for**: Category-specific promotions, launches

**Example - Apparel Category**:
```
Name: "Apparel Buyers"

Definition:
Placed order with product category = "Apparel"
in last 90 days
```

**Create for Each Major Category**:
- Apparel segment
- Beauty/Skincare segment
- Electronics segment
- Home goods segment
- etc.

**Campaign Use**: Send apparel sales only to apparel buyers

### 11. Price Point Segments

**Purpose**: Target by purchasing power
**Use for**: Product-appropriate campaigns

**High Spenders**:
```
Name: "High AOV Customers"

Definition:
Average order value greater than $150
AND
Placed order at least once in last 180 days
```

**Budget Conscious**:
```
Name: "Value Shoppers"

Definition:
Average order value less than $75
AND
Placed order at least once in last 180 days
```

**Campaign Strategy**:
- High AOV: Premium products, bundles, new launches
- Value: Sales, discounts, budget-friendly options

## Geographic Segments

### 12. Location-Based

**Purpose**: Regional campaigns, local events
**Use for**: Store openings, regional sales, weather-based

```
Name: "California Customers"

Definition:
Shipping address state = California
OR
Billing address state = California
```

**Campaign Ideas**:
- Regional products
- Local event invitations
- State-specific promotions
- Weather-appropriate products (summer gear to warm states)

### 13. International vs. Domestic

**Purpose**: Different shipping/currency messaging
**Use for**: Shipping promotions, currency-specific

```
Name: "International Customers"

Definition:
Shipping address country is not United States
```

**Campaign Adjustments**:
- Mention international shipping
- Currency conversions
- Longer shipping times
- Import duties information

## Time-Based Segments

### 14. New Subscribers (0-30 Days)

**Purpose**: Recent subscribers still getting welcome series
**Use for**: Exclude from certain campaigns OR include in awareness

```
Name: "New Subscribers - 30 Days"

Definition:
Subscribed to Newsletter
in last 30 days
```

**Use Case**: Either suppress from campaigns (let welcome series work) OR send awareness campaigns too

### 15. Birthday/Anniversary

**Purpose**: Personalized milestone campaigns
**Use for**: Special birthday/anniversary offers

```
Name: "Birthday This Month"

Definition:
Birthday is in current month
```

**Setup**:
1. Collect birthday during signup (optional field)
2. Create segment for birthday month
3. Send special birthday email with offer

### 16. Seasonal Segments

**Purpose**: Timely, relevant seasonal content
**Use for**: Seasonal product campaigns

**Example - Holiday Shoppers**:
```
Name: "Holiday Buyers"

Definition:
Placed order between November 1 - December 31
in previous year
```

**Campaign Use**: Early holiday shopping reminders, gift guides

## Advanced Predictive Segments

### 17. Predicted Next Order Date

**Purpose**: Send restock reminders at optimal time
**Use for**: Consumable products

```
Name: "Due for Reorder"

Definition:
Predicted next order date is within next 7 days
```

**Klaviyo Feature**: Uses ML to predict when customer likely to reorder

### 18. Churn Risk

**Purpose**: Identify customers at risk of leaving
**Use for**: Retention campaigns

```
Name: "At-Risk Customers"

Definition:
Placed order at least 2 times (all time)
AND
Has NOT placed order in last 90 days
AND
Typical days between orders is less than 60
```

**Campaign**: Win-back with special offer

### 19. High Predicted CLV

**Purpose**: Identify high-potential customers early
**Use for**: VIP treatment, retention focus

```
Name: "High CLV Potential"

Definition:
Predicted customer lifetime value is greater than $500
```

**Klaviyo Feature**: ML prediction based on early behavior

## Engagement Quality Segments

### 20. Super Engaged

**Purpose**: Your biggest fans
**Use for**: Beta tests, referral programs, UGC requests

```
Name: "Super Engaged"

Definition:
Opened email at least 10 times in last 30 days
AND
Clicked email at least 5 times in last 30 days
```

**Campaign Ideas**:
- Request reviews
- Ask for referrals
- Beta product testing
- User-generated content
- Brand ambassador invitations

### 21. Click-Heavy (But Not Converting)

**Purpose**: High interest but not buying
**Use for**: Stronger offers, objection handling

```
Name: "Clickers Not Buyers"

Definition:
Clicked email at least 5 times in last 30 days
AND
Placed order zero times in last 60 days
```

**Campaign Strategy**: They're interested but something's blocking purchase
- Address objections
- Offer incentive
- Showcase social proof
- Risk reversal (guarantees)

## Exclusion Segments

### 22. Recent Purchasers (Exclude)

**Purpose**: Don't annoy people who just bought
**Use for**: Campaign exclusions

```
Name: "Purchased Last 7 Days"

Definition:
Placed order at least once in last 7 days
```

**Use**: Exclude from promotional campaigns (optional - test this)

### 23. Unsubscribed (Exclude)

**Purpose**: Never send to unsubscribed
**Use for**: Always exclude from campaigns

```
Klaviyo handles this automatically, but verify:

Definition:
Email is not suppressed
AND
Is in Newsletter list
```

## Segmentation Use Cases

### Campaign-Specific Segments

**Flash Sale Campaign**:
- Target: Engaged 60 Days
- Exclude: Purchased last 3 days
- Boost: Include VIP customers even if less engaged

**New Product Launch**:
- Target: VIP Customers (early access)
- Then: Repeat Customers (next day)
- Then: All Engaged (day after)

**Educational Content**:
- Target: Never Purchased + One-Time Buyers
- Purpose: Build value before selling

**Win-Back Campaign**:
- Target: Unengaged 90+ Days
- Exclude: Active orders, recent browsers
- Offer: Strong incentive

### Flow Trigger Segments

**Welcome Series**:
- Trigger: Subscribed to List
- Include: All new subscribers

**VIP Post-Purchase**:
- Trigger: Placed Order
- Filter: Lifetime Value > $500

**Budget-Friendly Cross-Sell**:
- Trigger: Placed Order
- Filter: Order value < $50
- Content: Affordable add-ons

## Creating Segments in Klaviyo

### Step-by-Step Process

1. **Navigate**: Klaviyo → Audience → Lists & Segments
2. **Create**: Click "Create Segment"
3. **Name**: Descriptive name (e.g., "Engaged 60 Days - Campaign Target")
4. **Define Conditions**:

**Condition Types**:

**Properties About Someone**:
- Email address
- First/last name
- Location (state, country, zip)
- Custom properties

**What Someone Has Done (or Not Done)**:
- Opened Email
- Clicked Email
- Placed Order
- Added to Cart
- Active on Site
- Subscribed to List

**Predictive Analytics**:
- Predicted next order date
- Expected date of next order
- Predicted customer lifetime value

**How to Add Conditions**:

**AND logic** (all must be true):
- Someone is in Newsletter
- AND Opened email in last 60 days
- AND Placed order in last 90 days

**OR logic** (any can be true):
- Someone has:
  - Opened email in last 60 days
  - OR Clicked email in last 60 days
  - OR Placed order in last 60 days

5. **Preview**: See member count updating in real-time
6. **Save**: Segment saves and updates automatically

### Segment Testing

Before using segment for campaign:
1. Check member count (make sense?)
2. Export sample to CSV
3. Verify a few profiles manually
4. Send test campaign to small subset
5. Monitor results before scaling

## Segment Naming Convention

**Format**: `[Purpose] - [Criteria] - [Timeframe]`

**Examples**:
- `Campaign Target - Engaged - 60 Days`
- `Exclude - Recent Purchasers - 7 Days`
- `VIP - 5+ Orders - All Time`
- `Winback - Unengaged - 90 Days`
- `Category - Apparel Buyers - Active`

**Why**: Easy to understand and find later

## Segmentation Strategy by Brand Type

### Fashion/Apparel
- Seasonal buyers
- Size/fit segments
- Style preference (casual, formal, athletic)
- Gender segments (if applicable)
- Price point segments

### Beauty/Skincare
- Skin type/concern segments
- Product type users (makeup, skincare, hair)
- Ingredient preference (natural, vegan, etc.)
- Usage frequency (daily, occasional)
- Concern-based (anti-aging, acne, etc.)

### Food/Beverage
- Dietary preferences (vegan, keto, gluten-free)
- Flavor preferences
- Purchase frequency (weekly, monthly)
- Gifters vs. self-buyers
- Subscription vs. one-time

### Electronics/Tech
- Product type owned
- Price tier
- Early adopters vs. mainstream
- B2B vs. B2C
- Tech-savvy level

## Best Practices

### Do's:
- **Start simple**: Engaged 60 days, never purchased, VIP
- **Test segments**: Small send first
- **Update regularly**: Review quarterly
- **Name clearly**: Future you will thank you
- **Document**: Keep notes on what works
- **Layer segments**: Combine criteria for precision
- **Monitor size**: Segments too small or too big = review criteria

### Don'ts:
- **Don't over-segment**: Diminishing returns after ~15-20 segments
- **Don't forget exclusions**: Always exclude unsubscribed
- **Don't segment without strategy**: Have reason for each
- **Don't ignore small segments**: Might be your VIPs
- **Don't create and forget**: Review and optimize
- **Don't make too complex**: Keep criteria understandable

## Common Mistakes

1. **Sending to entire list**: Always use engaged segment
2. **One-size-fits-all campaigns**: Segment for relevance
3. **Too many segments**: Complexity without benefit
4. **Not excluding recent buyers**: Can annoy customers
5. **Ignoring mobile users**: Check device-based behavior
6. **Not testing segment criteria**: Verify it works as expected
7. **Forgetting to update**: Segments need maintenance
8. **No geographic segmentation**: Miss regional opportunities
9. **Ignoring predictive data**: Klaviyo's ML is powerful
10. **Not documenting segments**: Lose track of purpose

## Segmentation ROI

**Example Results**:

**Before Segmentation** (blast to all):
- Open Rate: 18%
- Click Rate: 1.2%
- Conversion Rate: 0.5%
- Revenue: $500

**After Segmentation** (targeted):
- Open Rate: 42%
- Click Rate: 4.8%
- Conversion Rate: 2.1%
- Revenue: $1,850

**Improvement**: 270% revenue increase from same list

## Quick Start Segments

Start with these 5 segments:

1. **Engaged 60 Days** (campaign target)
2. **Never Purchased** (conversion focus)
3. **VIP Customers** (retention focus)
4. **Recent Cart Abandoners** (recovery focus)
5. **Unengaged 90+ Days** (winback/suppress focus)

These 5 segments cover 80% of segmentation needs.

## Advanced Segmentation Techniques

### Combine Multiple Criteria

**Example: High-Value Engaged Apparel Buyers**:
```
Definition:
Someone is in Newsletter list
AND Opened email at least once in last 60 days
AND Placed order with category = "Apparel" in last 90 days
AND Average order value greater than $100
```

**Use**: Premium apparel launch campaigns

### Exclude Multiple Groups

**Example: Campaign-Ready Subscribers**:
```
Include:
- Engaged 60 Days

Exclude:
- Purchased in last 3 days
- Currently in welcome flow (subscribed <7 days ago)
- Already received this campaign (use Klaviyo's built-in setting)
```

### Time-Based Triggers

**Example: Quarterly Reorder Reminder**:
```
Definition:
Last order date is between 85-95 days ago
AND Product purchased = "Consumable"
```

**Triggers**: Campaign at perfect reorder time

## Segmentation Maintenance

### Monthly Tasks:
- [ ] Review top 10 segment sizes
- [ ] Check for segments no longer used
- [ ] Update criteria if needed
- [ ] Create new segments for upcoming campaigns
- [ ] Archive old segments

### Quarterly Tasks:
- [ ] Audit all segments
- [ ] Remove redundant segments
- [ ] Update engagement windows (test 60 vs 90 days)
- [ ] Review VIP criteria (adjust thresholds)
- [ ] Document learnings
- [ ] Train team on new segments

---

**Pro Tip**: Start with engagement-based segmentation (Engaged 60 Days), then layer in purchase behavior (Never Purchased, VIP), then add specific needs (geography, category, etc.). Don't overcomplicate from day one.

**Remember**: The goal of segmentation is relevance. Every campaign should go to people who actually want that specific content. This increases engagement, reduces unsubscribes, and dramatically improves deliverability and revenue.
