# Build Welcome Series - Complete New Subscriber Nurture Flow

Expert skill for building high-converting welcome series that turn new subscribers into customers. This is your first impression and critical for setting the relationship foundation.

## Why Welcome Series Matters

Welcome emails are THE highest-performing emails you'll send:
- **Open Rate**: 50-80% (vs. 20-30% for regular campaigns)
- **Click Rate**: 15-30% (vs. 2-5% for regular campaigns)
- **Revenue Per Recipient**: 3-5x higher than campaigns
- **Purpose**: Convert cold subscriber → first-time customer

**Critical Window**: First 48 hours after subscription = highest engagement

## Welcome Series Strategy

### The 3-5 Email Welcome Series

**Email 1**: Immediate - Deliver promise + introduce brand (Send immediately)
**Email 2**: Day 1 - Educate + build value (Send 24 hours later)
**Email 3**: Day 2-3 - Social proof + urgency (Send 24-48 hours later)
**Email 4** (Optional): Day 4-5 - Final nudge + discount (Send 48 hours later)
**Email 5** (Optional): Day 7 - Last chance + transition to campaigns

## Welcome Series Flow Structure

```
Trigger: Subscribed to List (via pop-up, form, checkout)
    ↓
Email 1: Welcome + Discount Code (Send immediately)
    ↓
Conditional Split: Has Placed Order?
    ↓ NO
Time Delay: 24 hours
    ↓
Email 2: Brand Story + Value Proposition
    ↓
Conditional Split: Has Placed Order?
    ↓ NO
Time Delay: 24-48 hours
    ↓
Email 3: Social Proof + Best Sellers
    ↓
Conditional Split: Has Placed Order?
    ↓ NO
Time Delay: 48 hours
    ↓
Email 4: Urgency + Last Chance for Discount
    ↓
End Flow (transition to regular campaigns)
```

## Klaviyo Setup - Welcome Series

### Step 1: Create Flow
1. Klaviyo → Flows → Create Flow
2. Option A: Use Klaviyo's Welcome Series template
3. Option B: Create From Scratch
4. Name: "Welcome Series" or "New Subscriber Flow"

### Step 2: Set Up Trigger

**Trigger Options**:

**Option A: List Subscription (Recommended)**
1. Click trigger
2. Select "Subscribed to List"
3. Choose list: "Newsletter" (or your main list)
4. Filter: Where source = "Pop-up Form" or "Website Sign-up"

**Option B: Specific Form Submission**
1. Select "Submits Form"
2. Choose your main pop-up form
3. Ensures they get welcome series only from specific source

**Flow Filters** (Important):
- Only include: Subscribed to email = YES
- Exclude: Has placed order (if you only want non-customers)
- OR: Include everyone (even past customers for new subscriber experience)

**Recommended**: Include all new subscribers, even past customers, for consistent experience

### Step 3: Email 1 - Welcome + Deliver Promise

**Timing**: Send IMMEDIATELY (no delay)
**Purpose**: Deliver what they signed up for, set expectations, introduce brand

**Subject Line Options**:
- "Welcome! Here's your 15% off code"
- "Thanks for joining! Your discount inside"
- "[Name], here's your exclusive offer"
- "You're in! Here's your welcome gift"
- "Welcome to [Brand Name] - Here's 15% off"

**Preview Text**:
- "Use code WELCOME15 for 15% off your first order"
- "Plus: Free shipping on orders over $50"
- "Your exclusive discount is waiting"

**Email Structure**:

```
Header: [Your Logo]

Headline: "Welcome To [Brand Name]!"
Subheadline: "Here's a little gift to get you started"

[Discount Code Box - PROMINENT]
━━━━━━━━━━━━━━━━━━
   WELCOME15
  15% OFF FIRST ORDER
━━━━━━━━━━━━━━━━━━
"Use code WELCOME15 at checkout"
[Expires in 7 days]

Brief Brand Introduction (2-3 sentences):
"At [Brand], we believe [mission/value prop]. Since [year], we've helped thousands of customers [main benefit]."

What to Expect:
✓ Exclusive offers and early access
✓ Product tips and inspiration
✓ First to know about new launches

Quick Brand Benefits:
🚚 Free Shipping Over $50
♻️ 30-Day Returns
⭐ Rated 4.8/5 by 1,200+ Customers
💬 24/7 Customer Support

Featured Products (3-4):
[Product Grid]
"Popular First Orders:"
- Best-selling product #1
- Best-selling product #2
- Best-selling product #3

Primary CTA: "Shop Now & Save 15%"

Social Proof Footer:
"Join 50,000+ happy customers"
[Instagram/Social icons]
"Follow us @brandname for daily inspiration"

Footer with unsubscribe
```

**Klaviyo Setup**:
1. Add "Email" to flow
2. Use drag-and-drop editor
3. Add dynamic discount code:
   - Insert "Coupon Code" block
   - Connect to pre-created Klaviyo coupon
   - Or: Display static code
4. Add "Product Feed" block for featured products
5. Link CTAs to: Homepage with discount auto-applied OR Collection page

**Key Elements**:
- Discount code VERY prominent
- Clear expiration date (creates urgency)
- Brief, not overwhelming
- Mobile-optimized
- Social proof elements

### Step 4: Conditional Split After Email 1

1. Add "Conditional Split"
2. Condition: "Has Placed Order at least once since starting this flow"
3. **YES path**: End flow (they converted!)
4. **NO path**: Continue to Email 2

**Why This Matters**: Don't annoy people who already purchased

### Step 5: Time Delay #1
- Add Time Delay: 24 hours
- Gives them time to browse and consider

### Step 6: Email 2 - Brand Story + Educational Value

**Timing**: Day 1 (24 hours after Email 1)
**Purpose**: Build emotional connection, educate, provide value

**Subject Line Options**:
- "Our story: Why we started [Brand]"
- "The [Brand] difference (you'll love this)"
- "How to get the most out of your [product]"
- "P.S. Your discount still works!"
- "3 reasons why customers love us"

**Preview Text**:
- "Plus: Tips to help you choose the perfect [product]"
- "Everything you need to know about [product category]"
- "Your welcome offer is still active"

**Email Structure**:

```
Headline: "Why We Started [Brand Name]"
or "The [Brand Name] Story"

[Founder Photo]

Personal Letter from Founder:

"Hi [Name],

I'm [Founder Name], founder of [Brand]. Thanks for joining our community!

I started [Brand] in [year] because [personal story/problem you solved]. After trying countless [products] that [didn't work/were overpriced/etc], I knew there had to be a better way.

[Brief 2-3 paragraph story about starting the company, the mission, what makes you different]

Today, we've helped over [X] customers [achieve benefit]. Every product is [unique selling point - handmade/sustainably sourced/rigorously tested/etc].

We're not just another [category] brand. Here's what makes us different:"

What Makes Us Different:
1. [Unique Point #1]
   Brief explanation

2. [Unique Point #2]
   Brief explanation

3. [Unique Point #3]
   Brief explanation

"If you have any questions, just hit reply. I read every single email."

[Signature]
[Founder Name]

P.S. Don't forget - your WELCOME15 code is still active for [X] more days!

CTA: "Start Shopping"

Customer Quote:
"[Testimonial about company values/quality]"
- Customer Name

Footer
```

**Alternative Structure - Educational**:

```
Headline: "How To Choose The Perfect [Product]"

Educational Content:
"Hi [Name],

Choosing the right [product] can be overwhelming. Here's our simple guide:"

[Step-by-step guide or tips]
Tip #1: [Useful advice]
Tip #2: [Useful advice]
Tip #3: [Useful advice]

"Not sure where to start? Here are our top recommendations:"

[3-4 Product recommendations with explanations]

Product #1: Best for [use case]
"This is perfect if you [scenario]. Customers love it because [benefit]."

Product #2: Best for [use case]
...

"Have questions? Our team is here to help!"

CTA: "Shop [Category]" or "Take Our Quiz"

P.S. Reminder - Your WELCOME15 code expires in [X] days!
```

**Key Elements**:
- Personal, authentic story
- Builds emotional connection
- Educates without selling hard
- Reminder of active discount
- One clear CTA

### Step 7: Conditional Split #2
Same structure - Has Placed Order?
- YES → End
- NO → Continue

### Step 8: Time Delay #2
- Add Time Delay: 24-48 hours

### Step 9: Email 3 - Social Proof + Best Sellers

**Timing**: Day 2-3
**Purpose**: Build trust through social proof, showcase most popular products

**Subject Line Options**:
- "Our customers can't stop talking about these"
- "Why [X] customers love [Brand]"
- "[Name], see what everyone's buying"
- "Our 5-star favorites (you'll love these)"
- "Most popular first orders (still 15% off!)"

**Preview Text**:
- "Rated 4.8/5 stars by real customers"
- "Join thousands of happy customers"
- "See why [Product] has 500+ 5-star reviews"

**Email Structure**:

```
Headline: "Join 50,000+ Happy Customers"
or "See Why Everyone Loves [Brand]"

Social Proof Section:
"Don't just take our word for it. Here's what real customers say:"

[Customer Review Grid - 3-4 reviews]
Each review includes:
- ⭐⭐⭐⭐⭐ (5 stars)
- "Quote from customer review"
- Customer name, location
- Photo (if available)

Stats Banner:
━━━━━━━━━━━━━━━━━━
10,000+ ⭐⭐⭐⭐⭐ Reviews
50,000+ Happy Customers
4.8/5 Average Rating
━━━━━━━━━━━━━━━━━━

Best Sellers Section:
"Most Popular First Orders"

[Product Grid - 4-6 products]
Each product shows:
- Image
- Name
- Price (with 15% discount)
- Star rating + review count
- "Best Seller" badge
- Quick CTA button

Why People Love [Brand]:
✓ "[Key benefit]" - 98% of customers
✓ "[Key benefit]" - Rated #1 for [attribute]
✓ "[Key benefit]" - 30-day guarantee

UGC Section (Optional):
"Real Photos From Real Customers"
[Grid of customer photos from Instagram]
"Tag us @brandname for a chance to be featured!"

Urgency Reminder:
⏰ "Your WELCOME15 discount expires in [X] days"

Primary CTA: "Shop Best Sellers"
Secondary CTA: "See All Products"

Trust Footer:
[Trust badges: Secure checkout, money-back guarantee, free shipping]

Footer
```

**Klaviyo Dynamic Elements**:
- Use "Product Feed" block filtered by "Best Sellers"
- Or: Manually curate 4-6 top products
- Dynamic discount reminder with actual expiration countdown

**Key Elements**:
- Heavy on social proof
- Show real customer reviews
- UGC photos build authenticity
- Best sellers reduce decision paralysis
- Urgency reminder (discount expiration)

### Step 10: Conditional Split #3
Same structure

### Step 11: Time Delay #3
- Add Time Delay: 48 hours (or 24 if more aggressive)

### Step 12: Email 4 - Final Push + Urgency

**Timing**: Day 4-5
**Purpose**: Last chance urgency, overcome final objections

**Subject Line Options**:
- "Final reminder: Your 15% off expires tomorrow"
- "Don't miss out, [Name] (offer expires soon!)"
- "Last chance: Your discount disappears in 24 hours"
- "We'd love to see you again..."
- "Tomorrow: Your welcome discount expires"

**Preview Text**:
- "Use code WELCOME15 before it's gone"
- "Plus free shipping on orders $50+"
- "Don't let this deal slip away"

**Email Structure**:

```
Headline: "Your Welcome Offer Expires Tomorrow"
or "Final Chance: 15% Off Ends Soon"

Urgency Message:
"Hi [Name],

Your exclusive WELCOME15 discount expires tomorrow at midnight. We don't want you to miss out on your special offer!"

[Countdown Timer Visual]
⏰ EXPIRES IN: 24 Hours
[If possible, use actual countdown timer]

[Discount Code Box]
WELCOME15 - 15% OFF
"Valid for 24 hours only"

"Still not sure? Here's why you should try [Brand]:"

Overcome Objections:
❓ "What if it doesn't work for me?"
✅ 30-day money-back guarantee. No questions asked.

❓ "How long does shipping take?"
✅ Free shipping on orders $50+. Arrives in 3-5 days.

❓ "Is it really worth it?"
✅ Rated 4.8/5 by 10,000+ customers. See reviews →

❓ "What if I need help?"
✅ 24/7 customer support. Email, phone, or chat.

Quick Product Recommendations:
"Top Picks For You:"
[3 products based on:
- Most popular
- Recent site browsing behavior
- Category interest]

Strong CTA: "Shop Now & Save 15%"

Scarcity Element:
"⚠️ Some popular items are selling out fast"

P.S. Section:
"P.S. This is our final email about this welcome offer. After tomorrow, the discount expires and you'll join our regular email list where you'll get:
• Exclusive sales (subscribers only)
• New product launches
• Tips, inspiration, and more

We're glad you're here!"

Footer
```

**Advanced Klaviyo Features**:
- Real countdown timer (use HTML countdown timer tool)
- Dynamic product recommendations based on browsing
- "Low stock" badges on popular items

**Key Elements**:
- STRONG urgency
- Address all objections
- Make it easy to say yes
- Explain what happens next
- Genuine, not pushy

### Step 13: Flow End & Transition

After Email 4, subscribers automatically transition to regular campaign sends. Optionally add a final message:

**Email 5 (Optional) - Day 7**:

```
Subject: "Welcome to the family! Here's what's next..."

Brief message:
- Discount has expired
- They're now part of community
- What to expect from future emails
- How to get best value
- Invitation to follow on social

CTA: "Explore Our Shop"
```

## Advanced Welcome Series Strategies

### Segment by Signup Source

Create different welcome series based on where they subscribed:

**Pop-up with 15% off**:
→ Welcome series focuses on using discount

**Blog/Content subscribe (no discount)**:
→ Welcome series focuses on education, lighter on sales

**Checkout subscription**:
→ Welcome series thanks for purchase, focuses on post-purchase value

**Klaviyo Setup**:
1. Create multiple welcome flows
2. Use trigger filters to separate by source
3. Tag subscribers based on form
4. Route to appropriate flow

### Browse Behavior Integration

After Email 2, add conditional split based on browse behavior:

```
Conditional Split: Has Viewed Product?
    ↓ YES
Email: "We noticed you were looking at [Product]"
    ↓ NO
Continue standard flow
```

**Klaviyo Setup**:
1. Add Conditional Split
2. Check "Active on Site in last X hours"
3. Create browsed-product-specific email
4. Use dynamic "Recently Viewed" product block

### Quiz/Preference Integration

If you have a product quiz or preference center:

**After Email 1**:
```
"Take our 60-second quiz to find your perfect [product]"
→ Route to product quiz
→ Follow-up with personalized recommendations
```

### VIP Customer Welcome

If subscriber has high lifetime value or VIP status:

```
Conditional Split: Is VIP Customer?
    ↓ YES
Special VIP welcome sequence (better offers, personal touch)
    ↓ NO
Standard welcome series
```

## Email Design Best Practices

### Visual Hierarchy
1. Logo (top)
2. Clear headline
3. Discount code (if applicable) - VERY prominent
4. Body content
5. Product images
6. CTA button
7. Footer

### Mobile Optimization
- Single column layout
- Large text (minimum 16px)
- Big tappable buttons (44x44px minimum)
- Images resize properly
- Test on multiple devices

### Brand Consistency
- Use brand colors
- Consistent fonts
- Logo placement
- Voice and tone match website
- Design mirrors site aesthetic

### CTA Best Practices
- One primary CTA per email
- Use contrasting color
- Action-oriented text ("Shop Now" not "Click Here")
- Place above the fold
- Repeat CTA if email is long

## Subject Line Optimization

### Testing Framework

**Test These Variables**:
1. Personalization:
   - "Welcome, [Name]!"
   - vs. "Welcome to [Brand]!"

2. Emoji usage:
   - "Thanks for subscribing! 🎉"
   - vs. "Thanks for subscribing!"

3. Value proposition:
   - "Your 15% discount inside"
   - vs. "Welcome! Here's a gift"

4. Urgency:
   - "Your discount expires in 24 hours"
   - vs. "Don't miss your welcome offer"

5. Curiosity:
   - "The [Brand] secret..."
   - vs. "Why [Brand] is different"

**A/B Test in Klaviyo**:
1. Select email in flow
2. Click "A/B Test"
3. Test on 50/50 split
4. Minimum 100 sends before declaring winner
5. Update to winning subject line

## Success Metrics & Benchmarks

### Flow-Level Metrics
- **Conversion Rate**: Target 15-30% of new subscribers make purchase
- **Revenue Per Recipient**: Target $8-20
- **Average Order Value**: Track if first-time customers spend more/less
- **Time to First Purchase**: Ideally within 7 days

### Email-Level Metrics
**Email 1 (Welcome + Discount)**:
- Open Rate: 60-80%
- Click Rate: 20-35%
- Conversion Rate: 5-15%

**Email 2 (Brand Story)**:
- Open Rate: 40-60%
- Click Rate: 10-20%
- Conversion Rate: 3-8%

**Email 3 (Social Proof)**:
- Open Rate: 35-55%
- Click Rate: 15-25%
- Conversion Rate: 5-12%

**Email 4 (Last Chance)**:
- Open Rate: 30-50%
- Click Rate: 20-30%
- Conversion Rate: 8-18% (highest conversion due to urgency)

### Revenue Distribution
Typically:
- Email 1: 30-40% of total flow revenue
- Email 2: 15-25% of total flow revenue
- Email 3: 20-30% of total flow revenue
- Email 4: 20-30% of total flow revenue

## Common Mistakes to Avoid

1. **No discount code**: Welcome emails with offers convert 2-3x better
2. **Waiting too long**: Send Email 1 immediately
3. **Too much information**: Keep emails focused and scannable
4. **Weak subject lines**: First impression matters
5. **Not mobile-optimized**: 60%+ opens are mobile
6. **No social proof**: People want validation
7. **Unclear value prop**: Tell them why you're different
8. **No urgency**: Discount should expire (7-14 days)
9. **Not checking for purchases**: Exclude converters from remaining emails
10. **Generic product recommendations**: Show best sellers, not random products

## Discount Strategy Considerations

### Discount Size
- **10%**: Good for high-margin products
- **15%**: Sweet spot for most e-commerce
- **20%+**: For competitive industries or high AOV

### Alternatives to Percentage Discounts
- **Free shipping**: Works well for $50+ AOV
- **Dollar amount off**: "$10 off first order"
- **Gift with purchase**: "Free [item] with first order"
- **BOGO**: "Buy one, get one 50% off"

### No Discount Strategy
If you're a luxury brand or want to avoid discount dependency:
- Focus on value, quality, craftsmanship
- Offer "early access" to new products
- Provide exclusive content or guides
- Gift with purchase instead of discount

## Integration with Other Flows

### Flow Priority Settings
Welcome series should be HIGH priority:
1. Welcome Series (highest)
2. Post-Purchase
3. Abandoned Cart
4. Browse Abandonment
5. Winback (lowest)

**Klaviyo Setup**:
- Set smart sending: Consider your strategy
- If someone is in welcome series, pause other flows
- Except: Still send abandoned cart if they abandon

### Campaign Suppression
During welcome series (7 days), consider:
- Suppressing from regular campaigns
- OR: Let them receive campaigns for awareness
- Test what works for your brand

## Seasonal & Holiday Adjustments

### Black Friday / Cyber Monday
- Reduce welcome discount (they'll get better deals in campaigns)
- OR: Stack discounts ("15% welcome + 25% BFCM = 40% off!")
- Shorten series (3 emails over 3 days)

### Holiday Season
- Mention gift-giving in Email 2
- Add gift guides to Email 3
- Highlight shipping deadlines in Email 4

### New Product Launches
- Feature new products in Email 3
- "Be the first to try our new [product]"

## Compliance & Legal

- Include unsubscribe link (required)
- Physical mailing address (required)
- Don't send to people who unsubscribed
- Honor email preferences
- Be transparent about email frequency

## Welcome Series Workflow Checklist

**Before Launch**:
- [ ] Flow trigger configured correctly
- [ ] All emails designed and copy-edited
- [ ] Discount codes created and tested
- [ ] Links all working
- [ ] Mobile optimization checked
- [ ] Conditional splits set up
- [ ] Flow filters configured
- [ ] Exclusions set (converters, unsubscribed)
- [ ] Test sends completed
- [ ] Analytics tracking verified

**After Launch**:
- [ ] Monitor daily for first week
- [ ] Check for errors or issues
- [ ] Review open/click rates
- [ ] Track conversion rate
- [ ] Test subject line variations
- [ ] Optimize based on data
- [ ] Update copy quarterly
- [ ] Refresh product recommendations

---

**Pro Tip**: Welcome series is your highest ROI email flow. Invest time getting it right. A great welcome series can convert 20-30% of new subscribers into customers, creating a steady stream of new buyers.

**Next Steps**:
1. Build flow in Klaviyo using this template
2. Write authentic, on-brand copy
3. Design mobile-first emails
4. Test thoroughly before launching
5. Monitor closely for first week
6. Optimize monthly based on data
