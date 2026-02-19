# AuraNet Product Strategy V2
**Updated:** February 19, 2026

## Executive Summary

After testing and validation, we've refined AuraNet's positioning from a single-purpose "social media ban enforcer" to a dual-market product serving two distinct customer segments with complementary needs.

**Core insight:** Network-level DNS blocking alone cannot perfectly enforce restrictions due to device-level DNS changes and VPN workarounds. However, it provides significant value when positioned as part of a comprehensive protection system (parents) or a privacy/performance solution (tech enthusiasts).

---

## Market Segmentation

### **Segment 1: Worried Parents (Primary - 70% of revenue)**

**Demographics:**
- Australian parents aged 35-55
- Children aged 6-16
- Non-technical, values simplicity
- Household income $80k-150k+

**Pain Points:**
- Kids' social media addiction
- Exposure to inappropriate content
- Online predators and cyberbullying
- Feeling overwhelmed by technology
- Australia's under-16 social media ban (can't enforce it)

**Value Proposition:**
"The Complete Family Internet Safety System - Network protection + device lockdown guides + ongoing education. Australian-owned. No subscription."

**Willingness to Pay:** $299-499 for peace of mind

**Marketing Channels:**
- Facebook/Instagram ads
- Parenting forums and groups
- School newsletters
- Local community centers
- "Back to school" campaigns

---

### **Segment 2: Privacy Enthusiasts (Secondary - 30% of revenue)**

**Demographics:**
- Tech-savvy Australians aged 25-45
- Privacy-conscious, anti-surveillance
- Understand DNS, Pi-hole, VPNs
- DIY mindset but values convenience

**Pain Points:**
- Ads everywhere (phones, tablets, smart TVs)
- Privacy invasion by tech companies
- Slow internet from trackers
- Data sovereignty concerns (Australian vs Chinese/US companies)
- Time investment to DIY a Pi-hole setup

**Value Proposition:**
"Australian-owned network-wide ad blocking with zero data collection. Raspberry Pi + Pi-hole + Unbound. Private recursive DNS. Your queries never leave your home."

**Willingness to Pay:** $299 (compared to DIY time + parts)

**Marketing Channels:**
- Reddit (r/pihole, r/privacy, r/australia)
- Hacker News
- Tech blogs and YouTubers
- Privacy-focused communities
- Tech forums

---

## What AuraNet Actually Does (Honest Assessment)

### **✅ What Works Well**

1. **Network-Level Ad/Tracker Blocking**
   - Blocks 2.8M+ domains across ALL devices
   - Works on smart TVs, IoT devices, phones, tablets, laptops
   - No per-device configuration needed
   - Significantly faster than browser extensions

2. **Private Recursive DNS (Unbound)**
   - DNS queries never leave the home network
   - No Google, Cloudflare, or any third party sees browsing
   - Genuinely unique selling point vs competitors
   - Australian data sovereignty

3. **Malware/Phishing Protection**
   - Blocks known dangerous sites at network level
   - Protects even non-tech-savvy users automatically
   - Updated blocklists daily

4. **DNS Caching Performance**
   - Faster page loads from cached DNS responses
   - Measurable improvement (50-200ms per query)

5. **VPN Website Blocking**
   - Blocks 5000+ VPN provider websites
   - Prevents casual download attempts (kids googling "free VPN")
   - Stops 70-80% of non-technical bypass attempts

6. **Visibility & Control**
   - See what every device is accessing
   - Block specific sites by name
   - Pause internet per device
   - Historical query logs

### **❌ What Doesn't Work (And How We Address It)**

1. **Cannot Force DNS at Router Level**
   - Consumer routers (TP-Link AX55) don't support DNS interception
   - Tech-savvy kids can change device DNS settings (8.8.8.8, 1.1.1.1)
   - **Solution:** Educate parents to lock down devices (Screen Time, Family Link)
   - **Positioning:** "Network protection + device lockdown = complete system"

2. **Cannot Block VPN Apps Once Installed**
   - VPN apps encrypt all traffic, bypassing DNS entirely
   - Blocking VPN protocols (OpenVPN, WireGuard) breaks legitimate traffic
   - **Solution:** Block VPN downloads + educate parents on device restrictions
   - **Positioning:** "Makes bypass significantly harder, not impossible"

3. **Social Media Apps Use Multiple Domains**
   - Instagram app uses 50+ subdomains, blocklists don't catch all
   - New domains created constantly
   - **Solution:** Comprehensive blocklists + manual additions + device app restrictions
   - **Positioning:** "Layer 1 of defense, combine with Screen Time for complete protection"

4. **App Stores Cannot Be Blocked**
   - Blocking Apple App Store or Google Play breaks the entire device
   - Kids can download VPN apps, social media apps, etc.
   - **Solution:** Device-level app store restrictions (require password for downloads)
   - **Positioning:** "Setup guides show you how to lock down app stores"

---

## The Education Component (Key Differentiator)

**Included with every AuraNet purchase:**

### **1. Physical Quick-Start Guide with QR Codes**
- Locking Down iPhone/iPad → video + checklist
- Locking Down Android/Samsung → video + checklist
- Securing App Stores → step-by-step
- Blocking VPN Installation → device-specific guides

### **2. Parent Resource Portal (getauranet.com.au/resources)**
- Video tutorials for every major device type
- Downloadable checklists: "Is Your Child's Device Protected? 15-Point Checklist"
- Monthly newsletter: "This Month's Bypass Technique & How to Stop It"
- Community forum for parent support

### **3. Device-Specific Setup Guides**

**iOS/iPadOS:**
- Enable Screen Time with passcode
- Block App Store downloads without password
- Disable Safari, force only approved browsers
- Set communication limits
- Block adult content in Screen Time
- Prevent DNS profile installation
- Disable VPN installation

**Android/Samsung:**
- Google Family Link setup
- Samsung Kids Mode configuration
- Block "Install Unknown Apps"
- Disable VPN permissions
- Content filtering via Google Play
- App usage limits

**Tablets (iPad/Android):**
- Guided Access mode (iOS)
- Kiosk mode (Android)
- Educational app whitelists

### **4. Layered Security Philosophy**

**Teach parents the "3-Layer Protection Model":**
1. **Network Layer (AuraNet):** Blocks threats automatically across all devices
2. **Device Layer (Screen Time/Family Link):** Prevents workarounds and app downloads
3. **Communication Layer (Parent-Child):** Open dialogue about online safety

**Marketing message:** "AuraNet provides the network foundation, but complete protection requires all three layers. We provide the tools and education for all three."

---

## Product Lineup

### **Smart Wi-Fi Kit - $499 AUD**

**Includes:**
- TP-Link Archer AX55 (AX3000) WiFi 6 Router - pre-configured
- Raspberry Pi 4 (2GB) with AuraNet software - pre-configured
- HDMI dummy plug (for headless operation)
- Ethernet cable
- Power supplies (2x)
- Physical quick-start guide with QR codes
- 1 year email support included

**Pre-configuration:**
- DHCP reservation set for Pi's MAC address
- Router DNS pointing to Pi
- Pi-hole + Unbound + Dashboard pre-installed
- Standard Mode enabled by default
- Ready to plug and play

**Target Customer:** Parents who want everything to work out of the box

**Sales Pitch (Parents):** "Complete system, ready in 5 minutes. No technical knowledge required."

**Sales Pitch (Privacy Users):** "Pre-configured Pi-hole appliance with WiFi 6 router. Plug in and you're protected."

---

### **Network Supercharger - $299 AUD**

**Includes:**
- Raspberry Pi 4 (2GB) with AuraNet software
- HDMI dummy plug
- Power supply
- Ethernet cable
- Physical setup guide with QR codes + router-specific DNS setup instructions
- 1 year email support included

**Customer Setup Required:**
- Plug Pi into existing router
- Set router's DNS to Pi's IP address (guides provided for 10+ router types)
- Optional: Set DHCP reservation (recommended)

**Target Customer:** 
- Parents with good existing routers (ASUS, Netgear, etc.)
- Tech enthusiasts who want Pi-hole without the hassle
- Customers who can't replace their ISP-supplied router

**Sales Pitch (Parents):** "Add AuraNet protection to your existing router. Works with any router."

**Sales Pitch (Privacy Users):** "Plug-and-play Pi-hole appliance. No SD card flashing, no SSH required."

---

## Pricing & Cost Structure

### **Hardware Costs (Estimated)**

**Smart Wi-Fi Kit Components:**
- TP-Link Archer AX55: $179 (wholesale ~$140)
- Raspberry Pi 4 (2GB): $80
- SD Card (64GB): $25
- Case (Argon NEO): $30
- HDMI dummy plug: $8
- Power supplies (2x): $30
- Ethernet cable: $5
- Packaging/materials: $20
**Total hardware cost: ~$338**

**Network Supercharger Components:**
- Raspberry Pi 4 (2GB): $80
- SD Card (64GB): $25
- Case (Argon NEO): $30
- HDMI dummy plug: $8
- Power supply: $15
- Ethernet cable: $5
- Packaging/materials: $15
**Total hardware cost: ~$178**

### **Margins**

**Smart Wi-Fi Kit:**
- Retail: $499
- Hardware: $338
- Gross margin: $161 (32%)
- After support/marketing: ~$100 net (20%)

**Network Supercharger:**
- Retail: $299
- Hardware: $178
- Gross margin: $121 (40%)
- After support/marketing: ~$80 net (27%)

### **Support Subscription (Optional)**

**AuraNet Plus - $99 AUD/year (optional after first year)**

**Includes:**
- Priority email support (24-hour response)
- Phone/video call support (2x 30-min sessions/year)
- Monthly feature updates
- Early access to new features
- Extended device lockdown guides (Windows PCs, Chromebooks, gaming consoles)

**Expected uptake:** 10-15% of customers
**Customer lifetime value:** $499 + ($99 × 3 years) = ~$800

---

## Competitive Analysis

### **Direct Competitors**

**Gryphon ($549 + $99/year subscription)**
- Pros: True DNS forcing, better device management app, established brand
- Cons: Expensive subscription, US-based (privacy concerns), proprietary hardware
- **Our advantage:** No subscription, Australian-owned, more transparent

**Circle (Discontinued in Australia)**
- Was $99 hardware + $5/month
- Market gap we can fill

**Firewalla ($499-799)**
- Pros: Enterprise-grade features, true firewall
- Cons: Complex setup, overkill for most parents, expensive
- **Our advantage:** Simpler, focused on parenting needs, education included

### **Indirect Competitors**

**TP-Link HomeShield / Netgear Armor ($6-10/month)**
- Built into consumer routers
- **Our advantage:** No subscription, more comprehensive, education component, Australian-owned

**NextDNS / AdGuard DNS ($20-30/year cloud service)**
- DNS filtering only, no hardware
- **Our advantage:** Private recursive DNS (no cloud), network-wide blocking, physical product

**DIY Pi-hole**
- Free but requires technical knowledge and 10+ hours setup
- **Our advantage:** Pre-configured, pretty dashboard, support, education materials

---

## Marketing Strategy

### **Dual Landing Page Approach**

**Homepage forks immediately:**
```
"What brings you to AuraNet?"
├─ "I want to protect my family online" → Parent landing page
└─ "I want privacy and ad blocking" → Tech specs page
```

### **Parent-Focused Marketing**

**Headline:** "The Complete Family Internet Safety System"

**Subheading:** "Network protection + device lockdown guides + ongoing education. Australian-owned. No subscription."

**Key Messages:**
- Blocks inappropriate content across ALL devices automatically
- See what your kids are trying to access in real-time
- Step-by-step guides to lock down every device
- Weekly reports delivered to your email
- Works with Australia's under-16 social media rules
- Australian-owned - your family's data stays in Australia

**Social Proof:**
- Parent testimonials: "Finally, peace of mind"
- "Trusted by 500+ Australian families"
- "Featured in [parenting blog/magazine]"

**CTAs:**
- "Protect My Family Now"
- "See How It Works" (video demo)
- "Download Free Device Lockdown Checklist" (lead magnet)

### **Privacy Enthusiast Marketing**

**Headline:** "Australian-Owned Network-Wide Ad Blocking with Zero Data Collection"

**Subheading:** "Raspberry Pi + Pi-hole v6 + Unbound. Block 2.8M+ trackers. Private recursive DNS. Your queries never leave your home."

**Key Messages:**
- Block ads on EVERY device (phones, smart TVs, IoT)
- Private recursive DNS - no Google, no Cloudflare, no one
- 2.8M+ domains blocked (malware, trackers, ads, telemetry)
- DNS caching = measurably faster internet
- Australian data sovereignty - no offshore data storage
- Open source foundation, fully customizable

**Technical Specs Prominent:**
- Pi-hole v6 with custom Flask dashboard
- Unbound recursive DNS resolver
- Redundant blocklists (5+ sources per category)
- Real-time query monitoring
- WiFi 6 (AX3000) router included in Smart Kit

**Social Proof:**
- GitHub stars (when we open source dashboard)
- Reddit upvotes/recommendations
- Performance benchmarks
- Privacy audit results

**CTAs:**
- "Build Your Privacy Shield"
- "See Technical Specs"
- "Compare to Cloud DNS Services"

---

## Content Marketing Strategy

### **For Parents:**

**Blog Posts:**
- "Australia's Social Media Ban: What Parents Need to Know"
- "How to Talk to Your Kids About Online Safety"
- "10 Signs Your Child is Bypassing Parental Controls"
- "Device Lockdown Checklist for Every Device in Your Home"

**Video Content:**
- "Setting up AuraNet in 5 Minutes"
- "How to Lock Down an iPhone/iPad"
- "How to Lock Down Android/Samsung"
- "What to Do if Your Child Downloaded a VPN"

**Email Series (After Purchase):**
- Week 1: "Welcome to AuraNet - Watch This Setup Video"
- Week 2: "Lock Down iPhones in Your Home"
- Week 3: "Lock Down Android Devices"
- Week 4: "App Store Restrictions - Prevent VPN Downloads"
- Week 5: "Having 'The Talk' About Online Safety"
- Monthly: "This Month in Online Safety"

### **For Privacy Users:**

**Blog Posts:**
- "Pi-hole vs NextDNS vs AdGuard: Performance Benchmarks"
- "How Unbound Recursive DNS Works (and Why It Matters)"
- "Internet Speed Before/After Network-Level Ad Blocking"
- "Australian Data Sovereignty: Why It Matters"
- "The Problem with Cloud-Based DNS Filtering"

**Technical Deep-Dives:**
- "AuraNet Architecture: How We Built It"
- "Pi-hole v6 Database Schema Deep Dive"
- "Benchmarking DNS Resolution Times"
- Open source dashboard code on GitHub

**Video Content:**
- "AuraNet Unboxing and Setup"
- "Performance Comparison: Network Blocking vs Browser Extensions"
- "Customizing AuraNet Blocklists"
- "Advanced Features: Per-Device Filtering"

---

## Distribution Channels

### **Phase 1: Direct-to-Consumer (Current)**

**Shopify Store (getauranet.com.au):**
- Dual landing pages (parent / privacy)
- Product pages with extensive FAQs
- Blog/resource section
- Free shipping over $300
- 30-day money-back guarantee

**Launch Plan:**
1. Founder's beta (15-20 units) - friends, family, early adopters
2. Soft launch (Facebook ads, Reddit, parent forums) - 50-100 units
3. Full launch (broader marketing) - 500+ units in year 1

### **Phase 2: Retail Partnerships (12-18 months)**

**Potential Partners:**
- JB Hi-Fi (tech retail)
- Harvey Norman (family electronics)
- Office Works (home office section)
- Independent computer stores
- School technology suppliers

**Wholesale pricing:**
- Smart Kit: $349 wholesale → $499 retail (30% margin for retailer)
- Supercharger: $199 wholesale → $299 retail (33% margin)

### **Phase 3: B2B/Education (18-24 months)**

**Target Customers:**
- Primary schools (5-10 unit deployments for computer labs)
- After-school care facilities
- Libraries (public computer protection)
- Small businesses (employee network protection)

**Pricing:**
- 5-10 units: 10% discount
- 11-25 units: 20% discount
- 25+ units: Custom pricing + dedicated support

---

## Roadmap

### **Q1 2026 (Current - Pre-Beta)**
- ✅ Core product working (Pi-hole + Dashboard)
- ✅ VPN blocking category added
- ✅ Unbound recursive DNS integrated
- ✅ Health monitoring functional
- ⏳ Physical setup and testing complete
- ⏳ Device lockdown guides created (iOS, Android)
- ⏳ Parent resource portal launched
- ⏳ Setup videos recorded

### **Q2 2026 (Beta Launch)**
- Founder's beta: 15-20 units
- Gather feedback and iterate
- Refine setup guides based on real customer issues
- Create router-specific DNS setup guides (top 10 Australian routers)
- Build Golden Master SD card image
- Establish customer support processes

### **Q3 2026 (Soft Launch)**
- Shopify store live with dual landing pages
- Facebook/Instagram ads for parents
- Reddit/forum marketing for privacy users
- Target: 50-100 units sold
- Collect testimonials and case studies
- Refine support documentation

### **Q4 2026 (Full Launch + Features)**
- Broader marketing campaign
- Target: 200+ units sold
- Feature: Per-device aggressive filtering (Kids Mode per device)
- Feature: Bedtime scheduler (time-based restrictions)
- Feature: Weekly email reports for parents
- Consider: AuraNet Plus subscription launch

### **2027 (Scale + Expansion)**
- Retail partnerships
- B2B/education market entry
- International expansion (UK, Canada - similar social media bans)
- Advanced features: Usage analytics, threat alerts, remote management

---

## Success Metrics

### **Year 1 Goals**
- 300 units sold (200 Smart Kit, 100 Supercharger)
- Revenue: ~$120,000
- Customer satisfaction: >4.5/5 stars
- Support ticket volume: <2 tickets per customer
- Subscription uptake: 10-15% after first year

### **Year 2 Goals**
- 1000 units sold
- Revenue: ~$450,000
- Retail partnerships: 3-5 stores
- Subscription revenue: $10-15k/year
- Brand recognition in parent communities

### **Year 3 Goals**
- 2500 units sold
- Revenue: ~$1.1M
- Retail presence in major chains
- B2B contracts with 10+ schools
- International market entry (UK/Canada)

---

## Risk Mitigation

### **Technical Risks**

**Risk:** Pi hardware failure rate
- **Mitigation:** Use quality components (Samsung SD cards, official Pi power), 12-month warranty, replacement stock

**Risk:** Blocklists become ineffective
- **Mitigation:** Multiple redundant sources, monthly updates, community-contributed lists

**Risk:** ISPs start forcing their own DNS (like some US ISPs)
- **Mitigation:** Monitor Australian ISP practices, pivot to different blocking methods if needed

### **Market Risks**

**Risk:** Government ban gets repealed or weakened
- **Mitigation:** Dual market strategy means privacy market remains, parent messaging shifts to "proactive protection"

**Risk:** Major competitor (Google, Apple) launches competing product
- **Mitigation:** Australian-owned positioning, education component, no subscription model

**Risk:** Support burden becomes unsustainable
- **Mitigation:** Comprehensive guides reduce tickets, optional paid support tier, hire part-time support after 500 customers

### **Business Risks**

**Risk:** Hardware costs increase (Pi shortage, inflation)
- **Mitigation:** Maintain 3-month inventory buffer, relationships with multiple suppliers, pricing flexibility

**Risk:** Legal liability (child accesses harmful content despite AuraNet)
- **Mitigation:** Clear disclaimers ("significantly harder, not impossible"), terms of service, liability insurance

**Risk:** Cash flow issues during scaling
- **Mitigation:** Pre-orders for larger batches, conservative inventory management, explore small business grants

---

## Key Decisions & Learnings

### **What Changed from V1**

**Original Strategy (V1):**
- "AuraNet enforces Australia's social media ban"
- "Blocks all VPNs at network level"
- Single market: worried parents only
- $499 price justified by "only solution to government ban"

**Problems Discovered:**
- Cannot actually enforce the ban perfectly (DNS bypass, VPN apps work once installed)
- Consumer routers can't force DNS
- VPN blocking is DNS-level only (ineffective against installed apps)
- Social media apps use many domains, some get through

**Revised Strategy (V2):**
- "AuraNet makes bypass significantly harder + education for complete protection"
- "Blocks VPN downloads + device guides to prevent installation"
- Dual market: parents (70%) + privacy enthusiasts (30%)
- $499 justified by "complete system: network + education + privacy + no subscription"

### **Core Insight**

**Network-level blocking is necessary but not sufficient.** The real product is a complete system that combines:
1. Network protection (what we built)
2. Device lockdown (guides we provide)
3. Parent education (resource portal)
4. Australian ownership & privacy (differentiator)

**We're not selling a Pi-hole. We're selling peace of mind through education and tools.**

---

## Conclusion

AuraNet V2 is positioned as a complete family internet safety system serving two complementary markets. By being honest about technical limitations while providing comprehensive education and tools to close those gaps, we create genuine value that justifies the premium pricing.

The dual-market strategy provides revenue stability - if one segment underperforms, the other provides a buffer. The education component creates a moat that pure hardware competitors can't easily replicate.

Success depends on:
1. **Excellent setup guides** that actually work for non-technical customers
2. **Honest marketing** that sets appropriate expectations
3. **Comprehensive education** that makes customers successful
4. **Reliable hardware** that works out of the box
5. **Responsive support** during the critical first year

With these elements in place, AuraNet can capture meaningful market share in the growing family internet safety and privacy protection markets.
