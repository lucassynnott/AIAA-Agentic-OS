# Build Abandoned Cart Flow - Complete Cart Recovery System

Expert skill for building high-converting abandoned cart email flows that recover lost revenue. This covers both "Added to Cart" and "Checkout Started" abandonment sequences with complete email templates and Klaviyo setup.

## Why Abandoned Cart Flows Matter

Abandoned cart flows are THE highest-converting revenue driver in e-commerce email marketing:
- Average cart abandonment rate: 69.8%
- Average recovery rate with email: 10-30%
- ROI: Often 20x+ compared to regular campaigns

**Critical Distinction**:
- **Added to Cart** ≠ **Checkout Started**
- You need BOTH flows to maximize recovery
- Many customers add to cart but never reach checkout

## The Two Abandoned Cart Flows

### 1. Cart Abandoned Flow
**Trigger**: Customer adds product to cart but doesn't proceed to checkout
**Timeline**: 4 hours - 7 days
**Conversion Rate**: 5-15%

### 2. Checkout Abandoned Flow
**Trigger**: Customer starts checkout (enters email) but doesn't complete purchase
**Timeline**: 1 hour - 7 days
**Conversion Rate**: 15-30% (higher intent)

## Cart Abandoned Flow Structure

### Flow Architecture

```
Trigger: Added to Cart
    ↓
Time Delay: 4 hours
    ↓
Email 1: Gentle Reminder
    ↓
Conditional Split: Has Placed Order?
    ↓ NO
Time Delay: 1 day
    ↓
Email 2: Social Proof + Urgency
    ↓
Conditional Split: Has Placed Order?
    ↓ NO
Time Delay: 2 days
    ↓
Email 3: Last Chance + Incentive
    ↓
End Flow
```

### Klaviyo Setup - Cart Abandoned Flow

#### Step 1: Create Flow
1. Klaviyo → Flows → Create Flow → Create From Scratch
2. Name: "Cart Abandoned Flow"
3. Click "Create Flow"

#### Step 2: Set Up Trigger
1. Click on trigger box
2. Select "Added to Cart" metric
3. Configure trigger filters:
   - **What someone has done (or not done)**:
     - "Added to Cart" at least once
   - **Add filter**: In the last 6 hours
   - **What someone has not done**:
     - "Placed Order" since starting this flow

4. **Flow Filters** (click "Configure"):
   - Skip profiles who have:
     - Placed Order in the last 30 days (optional - depends on strategy)
   - Only include profiles subscribed to email

#### Step 3: Add Time Delay
1. Drag "Time Delay" below trigger
2. Set to: 4 hours
3. **Why 4 hours**: Gives customer time to complete naturally, not too pushy

#### Step 4: Build Email 1 - Gentle Reminder

**Subject Line Options**:
- "You left something behind..."
- "Still thinking about it?"
- "Your cart is waiting for you"
- "Did you forget something? 🛒"
- "[Name], you have items waiting"

**Preview Text**:
- "Complete your purchase now before items sell out"
- "Your favorites are still available"
- "Free shipping if you order today"

**Email Content Structure**:

```
Header: [Your Logo]

Headline: "You Left These Behind"
or "Still Interested?"

Subheadline: Quick reminder about the items in your cart

[Dynamic Product Block]
- Shows items they added to cart
- Product image
- Product name
- Price
- "Complete Purchase" button

Social Proof Section:
- "Join 10,000+ happy customers"
- Star rating
- Quick testimonial

Trust Signals:
- Free shipping icon
- Secure checkout icon
- Money-back guarantee

Primary CTA: "Complete My Purchase"

Footer: Standard footer with unsubscribe
```

**Klaviyo Email Editor**:
1. Click "Email" box in flow
2. Choose "Drag and Drop" editor
3. Use template or start blank
4. Add "Product" dynamic block:
   - Select "Item Added to Cart"
   - Shows product image, name, price
   - Add CTA button to product page or checkout

**Dynamic Variables**:
- `{{ person.first_name|default:"there" }}`
- `{{ event.Product.Name }}`
- `{{ event.Product.URL }}`
- `{{ event.Product.Price }}`

#### Step 5: Add Conditional Split
1. Drag "Conditional Split" below Email 1
2. Configure split:
   - **Condition**: Has Placed Order since starting this flow
   - **YES path**: End flow (they converted!)
   - **NO path**: Continue to Email 2

#### Step 6: Add Time Delay #2
1. On the "NO" path, add Time Delay
2. Set to: 1 day

#### Step 7: Build Email 2 - Social Proof + Urgency

**Subject Line Options**:
- "Still available! But not for long..."
- "[Name], these are selling fast"
- "Only a few left in stock"
- "You're going to love these"
- "Our customers can't stop talking about this"

**Email Content Structure**:

```
Header: [Your Logo]

Headline: "These Are Flying Off The Shelves"
or "See What Others Are Saying"

[Dynamic Product Block]
- Cart items

Social Proof Heavy Section:
- 3-5 customer reviews
- Before/after photos (if applicable)
- UGC content
- "Rated 4.8/5 by 1,200+ customers"

Urgency Elements:
- "Only X left in stock"
- "Order soon - high demand"
- "Don't miss out"

Benefits Reminder:
- Free shipping
- 30-day returns
- Customer support

Primary CTA: "Get It Now"
Secondary CTA: "View Cart"

Footer
```

**Key Elements**:
- More aggressive urgency
- Heavy social proof
- Address common objections
- Multiple CTAs

#### Step 8: Add Conditional Split #2
Same as before:
- Has Placed Order since starting this flow?
- YES → End
- NO → Continue

#### Step 9: Add Time Delay #3
1. Add Time Delay
2. Set to: 2 days

#### Step 10: Build Email 3 - Last Chance + Incentive

**Subject Line Options**:
- "Last chance: Here's 10% off"
- "We'll make it worth your while..."
- "Final reminder + special offer inside"
- "Don't let this slip away (10% off)"
- "Your exclusive discount expires soon"

**Email Content Structure**:

```
Header: [Your Logo]

Headline: "Here's 10% Off To Sweeten The Deal"
or "Last Chance - Special Offer Inside"

Discount Code Box:
[CART10 - 10% OFF]
"Use code CART10 at checkout"

[Dynamic Product Block]
- Cart items with discount applied

Why Buy Now:
- Scarcity: "Discount expires in 24 hours"
- Benefits reminder
- Risk reversal: "100% money-back guarantee"

FAQ Section (Optional):
- Shipping time
- Returns
- Sizing help
- Customer support

Strong CTA: "Claim My Discount"

P.S. "This is our final reminder. We don't want you to miss out on these amazing products."

Footer
```

**Discount Strategy**:
- 10% is standard
- Consider: Free shipping instead
- Or: Gift with purchase
- Test what works best for your margins

#### Step 11: Flow Settings

1. **Smart Sending**: OFF
   - Let people receive the sequence
2. **Status**: Set to LIVE when ready
3. **Tracking**: Make sure UTM parameters are added

## Checkout Abandoned Flow Structure

This flow is for HIGHER INTENT customers who entered their email at checkout.

### Flow Architecture

```
Trigger: Started Checkout
    ↓
Time Delay: 1 hour
    ↓
Email 1: Urgent Reminder
    ↓
Conditional Split: Has Placed Order?
    ↓ NO
Time Delay: 4 hours
    ↓
Email 2: Address Objections
    ↓
Conditional Split: Has Placed Order?
    ↓ NO
Time Delay: 1 day
    ↓
Email 3: Strong Incentive
    ↓
End Flow
```

### Klaviyo Setup - Checkout Abandoned Flow

#### Step 1: Create Flow
1. Flows → Create Flow → Create From Scratch
2. Name: "Checkout Abandoned Flow"

#### Step 2: Set Up Trigger
1. Click trigger box
2. Select "Started Checkout" metric
3. Configure:
   - **What someone has done**:
     - "Started Checkout" at least once
   - **In the last**: 6 hours
   - **What someone has not done**:
     - "Placed Order" since starting this flow

4. **Flow Filters**:
   - Only include subscribed to email
   - Has not placed order in last 1 hour

#### Step 3: Time Delay
- Set to: 1 hour
- **Why shorter**: Higher intent, act faster

#### Step 4: Email 1 - Urgent Reminder

**Subject Line Options**:
- "Did something go wrong?"
- "You're so close! Complete your order"
- "Your order is waiting..."
- "[Name], checkout in 1 click"
- "Still there? Your cart is saved"

**Email Structure**:

```
Headline: "You're Almost There!"

"Hi [Name], we noticed you didn't complete your checkout. Good news - we saved everything for you!"

[Dynamic Checkout Block]
- Shows exact checkout details
- Items
- Quantity
- Total price
- Shipping info (if entered)

"Complete Your Order In One Click"
[Button: Return to Checkout]

Trust Signals:
- Secure checkout badge
- Customer service: "Questions? Call us at..."
- "Thousands order every day"

FAQ Mini Section:
- "Is shipping free?"
- "When will it arrive?"
- "Can I return it?"

CTA: "Complete Checkout Now"
```

**Key Klaviyo Variables**:
- `{{ event.CheckoutURL }}` - Direct link back to their checkout

#### Step 5: Conditional Split
- Has Placed Order since starting this flow?
- YES → End
- NO → Continue

#### Step 6: Time Delay
- Set to: 4 hours

#### Step 7: Email 2 - Address Objections

**Subject Line Options**:
- "Questions about your order?"
- "Here to help! Any concerns?"
- "Need help completing your purchase?"
- "Let us help you finish checkout"

**Email Structure**:

```
Headline: "Can We Help You Complete This Order?"

Personal message from founder/CEO:

"Hi [Name],

We noticed you started checkout but didn't complete your order. We're here to help!

Here are answers to our most common questions:"

[FAQ Section]
Q: Is shipping really free?
A: Yes! Free shipping on all orders over $50.

Q: What if it doesn't fit?
A: Free returns within 30 days. No questions asked.

Q: How long does shipping take?
A: 3-5 business days within the US.

Q: Is my payment information secure?
A: Absolutely. We use bank-level encryption.

[Your Saved Order]
[Product block]

"If you have any other questions, just hit reply to this email or call us at [phone]."

CTA: "Complete My Order"

P.S. "Your cart is saved and waiting for you. We're here 24/7 if you need anything."
```

**Strategy**: Address fear, uncertainty, and doubt (FUD)

#### Step 8: Conditional Split
Same structure

#### Step 9: Time Delay
- Set to: 1 day

#### Step 10: Email 3 - Strong Incentive

**Subject Line Options**:
- "Here's 15% off to complete your order"
- "Special offer just for you (15% off)"
- "We really want you to have this..."
- "Last chance: Your exclusive discount"

**Email Structure**:

```
Headline: "We REALLY Want You To Love This"

"[Name], we don't usually do this, but here's an exclusive 15% discount to complete your order today."

[Big Discount Code Box]
CHECKOUT15 - 15% OFF
"Valid for 24 hours only"

[Product block with discount applied]

New total: $XX (save $XX)

"Why You'll Love This:"
- Benefit 1
- Benefit 2
- Benefit 3

"What Customers Say:"
[1-2 quick testimonials]

Strong CTA: "Claim My Discount Now"

Expiration countdown: "Offer expires in 24 hours"

P.S. "This is our final email about this order. We won't bug you again!"
```

**Note**: 15% for checkout abandonment (vs. 10% for cart) because they're closer to purchase

## Advanced Optimization Strategies

### Product-Specific Paths

After Email 2, add a conditional split based on product category:

```
Conditional Split: Product Type
    ↓
Path 1: Apparel
    → Email with sizing guide, fit info

Path 2: Electronics
    → Email with tech specs, comparisons

Path 3: Beauty
    → Email with ingredient info, how to use
```

**Klaviyo Setup**:
1. Add Conditional Split
2. Select "Checkout Properties"
3. Filter by: "Item Category"
4. Create paths for each major category
5. Customize email content for each path

### Price-Based Incentives

Vary discount based on cart value:

```
Conditional Split: Cart Value
    ↓
< $50: Offer free shipping
$50-$100: Offer 10% off
$100+: Offer 15% off + free gift
```

### Time-Based Urgency

Add countdown timers:
- "Offer expires in 24 hours"
- "Cart reserved for 48 hours"
- "Items back in stock - selling fast"

### SMS Integration (If Available)

Add SMS messages between emails:
- After Email 1: "Hi [Name], your cart is waiting! Complete checkout: [link]"
- Before Email 3: "Last chance! Here's 10% off: [code] [link]"

## Email Design Best Practices

### Mobile-First Design
- 60%+ of emails opened on mobile
- Large, tappable buttons (minimum 44x44px)
- Single column layout
- Large, readable font (16px minimum)

### Dynamic Product Blocks

**Klaviyo Setup**:
1. In email editor, drag "Product" block
2. Select data source: "Added to Cart" or "Started Checkout"
3. Customize product display:
   - Show image: YES
   - Show name: YES
   - Show price: YES
   - Show description: Optional
   - Add CTA button: "View Item" or "Buy Now"

### Images
- High-quality product images
- Show product in use (lifestyle shots)
- Include multiple angles
- Optimize for fast loading (<100KB)

### Copy Guidelines
- Keep it concise
- Use customer's first name
- Conversational tone
- Address objections proactively
- Create urgency without being pushy

## Subject Line Testing

Test these variables:
- Personalization (with name vs. without)
- Emoji vs. no emoji
- Urgency ("Last chance") vs. curiosity ("You left something...")
- Length (short vs. long)
- Question vs. statement

**A/B Test in Klaviyo**:
1. Go to flow email
2. Click "A/B Test"
3. Test subject lines on 50/50 split
4. Let run for minimum 100 sends
5. Use winning subject line

## Success Metrics

Track these KPIs in Klaviyo Analytics:

### Flow-Level Metrics
- **Flow Revenue**: Target $5-15 per recipient
- **Conversion Rate**: Target 15-30% for checkout, 5-15% for cart
- **Open Rate**: Target 40-60%
- **Click Rate**: Target 15-25%

### Email-Level Metrics
- Email 1: Highest opens, moderate conversion
- Email 2: Moderate opens, good conversion
- Email 3: Lower opens, highest conversion (due to incentive)

### Benchmark Revenue Split
- Email 1: 40-50% of flow revenue
- Email 2: 25-35% of flow revenue
- Email 3: 20-30% of flow revenue

## Common Mistakes to Avoid

1. **Sending too quickly**: Wait at least 1 hour for checkout, 4 hours for cart
2. **Too many emails**: 3-4 emails maximum
3. **Weak subject lines**: Be specific and create urgency
4. **No mobile optimization**: 60% of opens are mobile
5. **Not excluding converters**: Always check if they placed order
6. **Same message for cart vs. checkout**: Different intent levels need different approaches
7. **No discount in final email**: Often needed to convert fence-sitters
8. **Ignoring product specifics**: Tailor content to what they abandoned
9. **Poor product images**: Use high-quality, appealing images
10. **No clear CTA**: Make it obvious what action to take

## Testing & Optimization

### Weekly Review Checklist
- [ ] Check flow revenue vs. last week
- [ ] Review conversion rates by email
- [ ] Identify drop-off points
- [ ] Test new subject lines
- [ ] Update product recommendations
- [ ] Refresh email copy
- [ ] Review customer feedback
- [ ] Check for broken links
- [ ] Verify discount codes working

### A/B Testing Ideas
1. Subject line variations
2. Sending times (delay lengths)
3. Discount amounts (10% vs. 15% vs. free shipping)
4. Email copy (short vs. long)
5. Number of emails in sequence
6. Urgency tactics
7. Social proof placement
8. CTA button text and color

### Seasonal Adjustments
- **Holiday Season**: Shorter delays, stronger urgency
- **Summer**: Longer delays, lighter tone
- **Black Friday/Cyber Monday**: Maximum urgency, best discounts
- **New Product Launches**: Feature new products heavily

## Integration with Other Flows

### Flow Suppression Logic
**Important**: Prevent flow conflicts

1. **Welcome Flow Priority**: If someone just subscribed, delay cart abandonment
2. **Post-Purchase Flow**: If they converted, don't send cart emails
3. **Browse Abandonment**: Don't overlap with cart abandonment

**Klaviyo Setup**:
- Use flow filters to exclude people in other active flows
- Set priority levels for flows
- Use smart sending to prevent email fatigue

## Legal & Compliance

- Include unsubscribe link (required)
- Physical mailing address (required)
- Honor unsubscribes immediately
- Don't send to hard bounces
- Respect email preferences

## Recovery Rate Benchmarks by Industry

- **Fashion/Apparel**: 15-25%
- **Electronics**: 10-20%
- **Beauty/Cosmetics**: 20-30%
- **Home Goods**: 12-22%
- **Food/Beverage**: 8-18%

## ROI Calculation

**Example**:
- Monthly cart abandoners: 1,000
- Average cart value: $75
- Recovery rate: 20%
- Recovered orders: 200
- Recovered revenue: $15,000
- Flow setup time: 6 hours
- ROI: Massive (recurring monthly revenue for one-time setup)

---

**Next Steps**:
1. Set up both flows in Klaviyo
2. Test with small segment first
3. Monitor for 1 week
4. Optimize based on performance
5. Scale to full list

**Pro Tip**: Abandoned cart flows often generate 30-40% of total automated flow revenue. Get these right, and you'll see immediate impact on your bottom line.
