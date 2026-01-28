# SKILL BIBLE: ABANDONED CART EMAIL FLOW MASTERY

## Executive Summary

This skill bible provides complete mastery of building high-converting abandoned cart email flows - the single highest-ROI automated email marketing system in e-commerce. With average cart abandonment rates of 69.8% and potential recovery rates of 10-30%, these flows can generate 20x+ ROI and often represent 30-40% of total automated flow revenue.

The skill covers building two distinct but complementary flows: Cart Abandoned (for customers who add items but don't reach checkout) and Checkout Abandoned (for higher-intent customers who start checkout but don't complete). Each flow requires different messaging, timing, and incentive strategies. This comprehensive guide includes complete Klaviyo setup instructions, email templates, optimization strategies, and advanced techniques for maximizing revenue recovery.

This is not just about sending "you forgot something" emails - it's about building a sophisticated, multi-touch system that addresses customer psychology, overcomes objections, and strategically applies urgency and incentives to convert abandoned sessions into completed purchases.

## Source
- **Type:** Internal SOP/Skill Document
- **Category:** ecommerce-email
- **Original File:** build_abandoned_cart_flow.md

## Core Principles

### 1. The Two-Flow System Principle
Never treat all abandonment the same. Cart abandonment (adding to cart) represents different customer intent than checkout abandonment (entering email at checkout). Cart abandoners need education and social proof; checkout abandoners need urgency and objection handling. Build separate flows with different messaging, timing, and incentive strategies.

### 2. Progressive Urgency and Value Escalation
Structure each flow as an escalating sequence: start gentle, build urgency, end with incentives. Email 1 should be a soft reminder, Email 2 adds social proof and mild urgency, Email 3 provides strong incentives. This progression respects customer psychology while maximizing conversion opportunities.

### 3. Timing Psychology Optimization
Respect natural purchase consideration windows. Cart abandoners get 4 hours to complete naturally (not pushy), then 1-day intervals. Checkout abandoners get 1 hour (higher intent, act faster), then shorter intervals. Timing affects perception and conversion rates significantly.

### 4. Dynamic Content Personalization
Every email must show exactly what they abandoned with dynamic product blocks, personalized messaging, and relevant recommendations. Generic abandonment emails perform poorly. Use customer data to create personalized experiences that feel relevant and valuable.

### 5. Objection Prevention and Handling
Proactively address common purchase barriers: shipping costs, return policies, security concerns, sizing questions, delivery times. Email 2 should heavily focus on objection handling through FAQ sections, trust signals, and social proof.

### 6. Strategic Incentive Application
Reserve discounts for final emails and higher-intent flows. Cart abandoners get 10% in Email 3; checkout abandoners get 15% in Email 3. Never lead with discounts - earn the right to offer them by providing value first.

### 7. Mobile-First Design Imperative
With 60%+ of emails opened on mobile, every element must be mobile-optimized: large tappable buttons (44x44px minimum), single-column layouts, readable fonts (16px+), fast-loading images (<100KB). Mobile experience directly impacts conversion rates.

### 8. Conditional Logic and Smart Suppression
Always exclude customers who convert during the flow sequence. Use conditional splits after each email to check for order completion. Implement smart suppression to prevent conflicts with other flows and avoid email fatigue.

## Step-by-Step Process

### Phase 1: Cart Abandoned Flow Setup

#### Step 1: Flow Creation and Naming
1. Navigate to Klaviyo → Flows → Create Flow → Create From Scratch
2. Name: "Cart Abandoned Flow" (clear naming for team management)
3. Click "Create Flow" to initialize the flow builder

#### Step 2: Trigger Configuration
1. Click the trigger box in the flow builder
2. Select "Added to Cart" metric from the dropdown
3. Configure trigger conditions:
   - **Primary condition**: "Added to Cart" at least once
   - **Time window**: In the last 6 hours
   - **Exclusion condition**: Has NOT "Placed Order" since starting this flow
4. Set Flow Filters by clicking "Configure":
   - Only include profiles subscribed to email
   - Optional: Skip profiles who placed order in last 30 days (depends on business strategy)

#### Step 3: Initial Time Delay Setup
1. Drag "Time Delay" element below the trigger
2. Set delay to: 4 hours
3. Rationale: Allows natural completion time without appearing pushy

#### Step 4: Email 1 Construction - Gentle Reminder

**Subject Line Development** (test these options):
- "You left something behind..." (curiosity-driven)
- "Still thinking about it?" (question format)
- "Your cart is waiting for you" (direct)
- "Did you forget something? 🛒" (emoji + question)
- "[Name], you have items waiting" (personalized)

**Preview Text Optimization**:
- "Complete your purchase now before items sell out"
- "Your favorites are still available"
- "Free shipping if you order today"

**Email Content Structure**:
```
Header Section:
- Company logo (linked to homepage)
- Clear, recognizable branding

Headline Section:
- Primary: "You Left These Behind" or "Still Interested?"
- Subheadline: "Quick reminder about the items in your cart"

Dynamic Product Section:
- Product image (high-quality, lifestyle if possible)
- Product name (linked to product page)
- Price display
- Quantity selected
- "Complete Purchase" button (prominent CTA)

Social Proof Section:
- "Join 10,000+ happy customers"
- Star rating display (4.5+ stars)
- Brief testimonial or review snippet

Trust Signals Section:
- Free shipping icon and details
- Secure checkout badge
- Money-back guarantee mention
- Customer service contact info

Primary CTA:
- Button text: "Complete My Purchase"
- Color: Brand primary color
- Size: Large, mobile-friendly

Footer:
- Standard footer with unsubscribe link
- Physical address (legally required)
- Social media links
```

**Klaviyo Technical Implementation**:
1. Click "Email" box in flow
2. Choose "Drag and Drop" editor
3. Add "Product" dynamic block:
   - Data source: "Item Added to Cart"
   - Display: Product image, name, price
   - CTA button links to product page or direct checkout
4. Insert dynamic variables:
   - `{{ person.first_name|default:"there" }}` for personalization
   - `{{ event.Product.Name }}` for product name
   - `{{ event.Product.URL }}` for product link
   - `{{ event.Product.Price }}` for pricing

#### Step 5: First Conditional Split Implementation
1. Drag "Conditional Split" below Email 1
2. Configure split logic:
   - **Condition**: "Has Placed Order" since starting this flow
   - **YES path**: End flow (customer converted)
   - **NO path**: Continue to Email 2
3. This prevents sending additional emails to customers who already purchased

#### Step 6: Second Time Delay
1. On the "NO" path, add Time Delay element
2. Set to: 1 day (24 hours)
3. This spacing prevents email fatigue while maintaining engagement

#### Step 7: Email 2 Construction - Social Proof + Urgency

**Subject Line Options** (more urgent tone):
- "Still available! But not for long..."
- "[Name], these are selling fast"
- "Only a few left in stock"
- "You're going to love these"
- "Our customers can't stop talking about this"

**Email Content Structure**:
```
Header: Company branding

Headline Section:
- "These Are Flying Off The Shelves" or "See What Others Are Saying"
- More urgent tone than Email 1

Dynamic Product Section:
- Same cart items display
- Maintain visual consistency

Heavy Social Proof Section:
- 3-5 customer reviews with photos
- Before/after images (if applicable)
- User-generated content
- "Rated 4.8/5 by 1,200+ customers"
- Specific testimonials with customer names/locations

Urgency Elements:
- "Only X left in stock" (if true)
- "Order soon - high demand"
- "Don't miss out"
- Countdown timer (if applicable)

Benefits Reminder Section:
- Free shipping details
- 30-day return policy
- Customer support availability
- Satisfaction guarantee

Multiple CTAs:
- Primary: "Get It Now"
- Secondary: "View Cart"
- Tertiary: Product-specific links

Footer: Standard compliance footer
```

**Advanced Elements**:
- More aggressive urgency messaging
- Heavier emphasis on social proof
- Address common objections proactively
- Multiple conversion opportunities

#### Step 8: Second Conditional Split
1. Add identical conditional split structure
2. Check: "Has Placed Order" since starting flow
3. YES → End flow
4. NO → Continue to Email 3

#### Step 9: Third Time Delay
1. Add Time Delay element
2. Set to: 2 days (48 hours)
3. Longer delay before final incentive email

#### Step 10: Email 3 Construction - Last Chance + Incentive

**Subject Line Options** (incentive-focused):
- "Last chance: Here's 10% off"
- "We'll make it worth your while..."
- "Final reminder + special offer inside"
- "Don't let this slip away (10% off)"
- "Your exclusive discount expires soon"

**Email Content Structure**:
```
Header: Company branding

Headline Section:
- "Here's 10% Off To Sweeten The Deal"
- "Last Chance - Special Offer Inside"

Prominent Discount Section:
- Large discount code box: [CART10 - 10% OFF]
- "Use code CART10 at checkout"
- Clear instructions for redemption

Dynamic Product Section:
- Cart items with discount applied
- Show new price vs. original price
- Calculate savings amount

Urgency and Scarcity:
- "Discount expires in 24 hours"
- "This is our final reminder"
- "Limited time offer"

Benefits Reinforcement:
- Risk reversal: "100% money-back guarantee"
- Free shipping reminder
- Easy returns policy

FAQ Section (Optional but effective):
- Shipping timeframes
- Return process
- Sizing assistance
- Customer support contact

Strong CTA:
- "Claim My Discount"
- Urgent color scheme
- Large, prominent button

P.S. Section:
- "This is our final reminder. We don't want you to miss out on these amazing products."
- Creates finality and urgency

Footer: Standard compliance elements
```

**Discount Strategy Notes**:
- 10% is standard for cart abandonment
- Alternative: Free shipping instead of percentage off
- Consider: Gift with purchase for higher-value carts
- Test different incentive types for your audience

#### Step 11: Flow Settings Configuration
1. **Smart Sending**: Set to OFF (allow sequence to complete)
2. **Status**: Keep as DRAFT until testing complete, then set to LIVE
3. **Tracking**: Ensure UTM parameters are configured for analytics
4. **Flow Filters**: Double-check exclusion criteria

### Phase 2: Checkout Abandoned Flow Setup

#### Step 12: Checkout Flow Creation
1. Create new flow: "Checkout Abandoned Flow"
2. This targets higher-intent customers who entered email at checkout

#### Step 13: Checkout Trigger Configuration
1. Select "Started Checkout" metric
2. Configure conditions:
   - **Primary**: "Started Checkout" at least once
   - **Time window**: In the last 6 hours
   - **Exclusion**: Has NOT "Placed Order" since starting flow
3. Flow Filters:
   - Only include email subscribers
   - Exclude recent purchasers (last 1 hour)

#### Step 14: Shortened Time Delay
1. Set initial delay to: 1 hour
2. Rationale: Higher intent customers need faster follow-up

#### Step 15: Checkout Email 1 - Urgent Reminder

**Subject Line Options** (more urgent than cart abandonment):
- "Did something go wrong?"
- "You're so close! Complete your order"
- "Your order is waiting..."
- "[Name], checkout in 1 click"
- "Still there? Your cart is saved"

**Email Structure**:
```
Headline: "You're Almost There!"

Personal Opening:
"Hi [Name], we noticed you didn't complete your checkout. Good news - we saved everything for you!"

Dynamic Checkout Block:
- Exact checkout details preserved
- Items with quantities
- Total price calculation
- Shipping information (if entered)
- Billing details (if partially completed)

One-Click Completion:
"Complete Your Order In One Click"
[Button: Return to Checkout] - links to {{ event.CheckoutURL }}

Trust and Security Signals:
- Secure checkout badge (SSL certificate)
- Customer service: "Questions? Call us at [phone]"
- "Thousands order safely every day"
- Payment security icons

Mini FAQ Section:
- "Is shipping free?" with clear answer
- "When will it arrive?" with timeframes
- "Can I return it?" with policy details

Strong CTA: "Complete Checkout Now"
Sense of completion - they're 90% done
```

**Key Klaviyo Variables for Checkout**:
- `{{ event.CheckoutURL }}` - Direct link back to their exact checkout state
- `{{ event.TotalPrice }}` - Show total they were about to pay
- `{{ event.ShippingAddress }}` - If they entered shipping info

#### Step 16: Checkout Conditional Split
1. Same structure: Has Placed Order since starting flow?
2. YES → End flow
3. NO → Continue

#### Step 17: Checkout Time Delay 2
1. Set to: 4 hours (shorter than cart abandonment)

#### Step 18: Checkout Email 2 - Objection Handling

**Subject Line Focus** (helpful tone):
- "Questions about your order?"
- "Here to help! Any concerns?"
- "Need help completing your purchase?"
- "Let us help you finish checkout"

**Email Structure**:
```
Headline: "Can We Help You Complete This Order?"

Personal Message from Leadership:
"Hi [Name],

We noticed you started checkout but didn't complete your order. We're here to help!

Here are answers to our most common questions:"

Comprehensive FAQ Section:
Q: Is shipping really free?
A: Yes! Free shipping on all orders over $50. No hidden fees.

Q: What if it doesn't fit or I don't like it?
A: Free returns within 30 days. No questions asked. We'll even send you a prepaid return label.

Q: How long does shipping take?
A: 3-5 business days within the US. Express options available at checkout.

Q: Is my payment information secure?
A: Absolutely. We use bank-level encryption and never store your payment details.

Q: Can I change my order after placing it?
A: Yes! Contact us within 2 hours and we can modify your order.

Your Saved Order Section:
[Dynamic product block showing checkout items]
"Everything is saved and waiting for you"

Personal Support Offer:
"If you have any other questions, just hit reply to this email or call us at [phone]. A real person will help you."

CTA: "Complete My Order"

P.S. "Your cart is saved and waiting for you. We're here 24/7 if you need anything."
```

**Strategy Focus**: Address fear, uncertainty, and doubt (FUD) that prevents completion

#### Step 19: Second Checkout Conditional Split
1. Same logic as previous splits
2. Check for order completion

#### Step 20: Final Checkout Time Delay
1. Set to: 1 day (24 hours)

#### Step 21: Checkout Email 3 - Strong Incentive

**Subject Line Options** (incentive-focused):
- "Here's 15% off to complete your order"
- "Special offer just for you (15% off)"
- "We really want you to have this..."
- "Last chance: Your exclusive discount"

**Email Structure**:
```
Headline: "We REALLY Want You To Love This"

Personal Appeal:
"[Name], we don't usually do this, but here's an exclusive 15% discount to complete your order today."

Prominent Discount Display:
[Large, eye-catching discount code box]
CHECKOUT15 - 15% OFF
"Valid for 24 hours only"

Price Comparison:
[Product block with discount applied]
Original total: $XXX
New total: $XXX (save $XX)
"That's a savings of $XX!"

Value Reinforcement:
"Why You'll Love This:"
- Key benefit 1 (specific to products)
- Key benefit 2 (quality/materials)
- Key benefit 3 (customer satisfaction)

Social Proof:
"What Customers Say:"
[1-2 powerful testimonials with photos]

Urgency Elements:
Strong CTA: "Claim My Discount Now"
Countdown: "Offer expires in 24 hours"
Scarcity: "Limited time exclusive offer"

Final Appeal:
P.S. "This is our final email about this order. We won't bug you again, but we'd hate for you to miss out on this amazing deal!"
```

**Strategic Notes**:
- 15% for checkout abandonment vs. 10% for cart abandonment
- Higher discount justified by higher intent
- Creates genuine urgency with expiration

### Phase 3: Advanced Optimization Implementation

#### Step 22: Product-Specific Customization

**Conditional Split by Product Category**:
After Email 2 in both flows, add product-specific paths:

```
Conditional Split: Product Type
├── Path 1: Apparel
│   └── Email: Sizing guide, fit information, style tips
├── Path 2: Electronics  
│   └── Email: Tech specs, comparisons, warranty info
├── Path 3: Beauty
│   └── Email: Ingredient benefits, usage instructions
└── Path 4: Home Goods
    └── Email: Room styling, care instructions
```

**Klaviyo Implementation**:
1. Add Conditional Split after Email 2
2. Select "Checkout Properties" or "Product Properties"
3. Filter by: "Item Category" or "Product Type"
4. Create separate email paths for major categories
5. Customize content for each product type

#### Step 23: Price-Based Incentive Strategy

**Dynamic Discount Structure**:
```
Conditional Split: Cart Value
├── Under $50: Offer free shipping (removes barrier)
├── $50-$100: Offer 10% discount
├── $100-$200: Offer 15% discount  
└── $200+: Offer 15% discount + free gift
```

**Implementation Logic**:
- Lower-value carts: Remove shipping friction
- Mid-value carts: Percentage discounts
- High-value carts: Premium incentives

#### Step 24: Time-Based Urgency Enhancement

**Dynamic Urgency Elements**:
- Real inventory counts (if available)
- Seasonal urgency ("Holiday shipping cutoff")
- Event-based urgency ("Sale ends soon")
- Cart reservation timers ("Held for 48 hours")

#### Step 25: SMS Integration (Multi-Channel)

**SMS Touchpoints** (if SMS capability available):
- After Email 1: "Hi [Name], your cart is waiting! Complete checkout: [link]"
- Before Email 3: "Last chance! Here's 10% off: [code] [link]"
- Post-discount: "Reminder: Your 15% discount expires in 2 hours [link]"

### Phase 4: Design and Content Optimization

#### Step 26: Mobile-First Design Implementation

**Critical Mobile Elements**:
- Button size: Minimum 44x44px (Apple guidelines)
- Font size: 16px minimum for body text
- Single-column layout for all content
- Touch-friendly spacing (minimum 8px between elements)
- Fast-loading images (optimize to <100KB each)
- Simplified navigation (fewer choices = higher conversion)

**Klaviyo Mobile Optimization**:
1. Use mobile preview for all email testing
2. Test on actual devices (iOS and Android)
3. Verify button functionality on mobile
4. Check image loading speeds
5. Ensure text readability without zooming

#### Step 27: Dynamic Product Block Optimization

**Advanced Product Display**:
1. In Klaviyo email editor, configure Product blocks:
   - Data source: "Added to Cart" or "Started Checkout"
   - Show multiple product images (if available)
   - Include product ratings/reviews
   - Add "You might also like" recommendations
   - Display inventory status ("Only 3 left")

**Product Recommendation Logic**:
- Show related products from same category
- Display frequently bought together items
- Include recently viewed products
- Feature bestsellers in similar price range

#### Step 28: Copy Optimization and Psychology

**Psychological Triggers to Include**:

**Loss Aversion**: "Don't miss out on this"
**Social Proof**: "Join 10,000+ happy customers"  
**Scarcity**: "Only a few left in stock"
**Authority**: "Recommended by experts"
**Reciprocity**: "Here's a special discount just for you"
**Commitment**: "Complete your purchase"

**Copy Guidelines**:
- Use second person ("you," "your")
- Active voice over passive voice
- Specific numbers over vague claims
- Benefit-focused language
- Conversational, friendly tone
- Address objections proactively

## Frameworks & Templates

### The 3-Email Escalation Framework

**Email 1: Soft Reminder (The Gentle Touch)**
- Purpose: Non-pushy reminder
- Tone: Helpful, friendly
- Content: Product display + basic benefits
- CTA: "Complete Purchase"
- No incentives

**Email 2: Social Proof + Urgency (The Persuader)**
- Purpose: Build desire and urgency
- Tone: Enthusiastic, social
- Content: Reviews, testimonials, mild urgency
- CTA: "Get It Now"
- Urgency elements, no discounts

**Email 3: Incentive + Final Call (The Closer)**
- Purpose: Convert with incentive
- Tone: Urgent but helpful
- Content: Discount offer + expiration
- CTA: "Claim Discount"
- Strong incentive + deadline

### Subject Line Template Library

**Cart Abandonment Subject Lines**:
```
Curiosity-Based:
- "You left something behind..."
- "Still thinking about it?"
- "Did you forget something?"

Personalized:
- "[Name], you have items waiting"
- "[Name], your cart misses you"
- "Hi [Name], still interested?"

Urgency-Based:
- "Still available! But not for long..."
- "These are selling fast"
- "Only a few left in stock"

Incentive-Based:
- "Here's 10% off to sweeten the deal"
- "Last chance + special offer inside"
- "Your exclusive discount expires soon"
```

**Checkout Abandonment Subject Lines**:
```
Problem-Solving:
- "Did something go wrong?"
- "Need help completing your order?"
- "Questions about your purchase?"

Completion-Focused:
- "You're so close! Complete your order"
- "Your order is waiting..."
- "Checkout in 1 click"

Incentive-Based:
- "Here's 15% off to complete your order"
- "Special offer just for you"
- "We really want you to have this..."
```

### Email Content Template Framework

**Template Structure**:
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ email.subject }}</title>
</head>
<body style="margin:0; padding:0; font-family:Arial, sans-serif;">
    
    <!-- Header Section -->
    <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
            <td align="center" style="padding:20px 0;">
                <img src="[LOGO_URL]" alt="[COMPANY_NAME]" style="max-width:200px;">
            </td>
        </tr>
    </table>
    
    <!-- Main Content -->
    <table width="600" cellpadding="0" cellspacing="0" style="margin:0 auto;">
        
        <!-- Headline Section -->
        <tr>
            <td style="padding:20px; text-align:center;">
                <h1 style="font-size:28px; color:#333; margin:0;">
                    [HEADLINE]
                </h1>
                