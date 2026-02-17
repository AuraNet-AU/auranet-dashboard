# Business Plan: AuraNet

**Project:** A Premium, Plug-and-Play Network Appliance for the Australian Market

**Founder:** Liam Albery

**Date:** 11/02/2026

**Version:** 2.0

---

## 1.0 Executive Summary

### The Problem

The majority of Australian households are served by ISP-provided hardware (Telstra, Optus Smart Modems) that offers poor performance, minimal control, and no protection against ads, trackers, and malicious domains. Existing solutions are either:

- Technically complex (Pi-hole DIY, Firewalla)
- Expensive with recurring fees (Gryphon: $449 + $99/year)
- Discontinued (Circle by Disney)
- Not available locally (Bark Home)

### The Solution

AuraNet provides a premium, "it just works" hardware solution that empowers Australian families to take control of their home network. Our products deliver:

- Network-wide ad-blocking on ALL devices
- Enhanced security against malware and phishing
- Powerful parental controls
- Beautiful, simple web dashboard
- **No subscriptions, ever**

### Product Lineup

A targeted two-product strategy addressing the entire consumer market:

| Product | Target | Price |
|:--------|:-------|:------|
| **Smart Wi-Fi Kit** | Users with basic ISP hardware | $449-499 |
| **Network Supercharger** | Users with existing quality routers | $249-299 |

### Core Differentiator

Our proprietary dashboard transforms a complex technical tool (Pi-hole) into a simple consumer appliance. This "zero-friction" software is our key intellectual property and creates a defensible moat around the business.

### Market Opportunity

- **No direct Australian competitors** selling a similar polished product
- Dominant ISP hardware has created a frustrated, underserved customer base
- Growing awareness of online privacy and child safety
- Australian preference for local products and support

---

## 2.0 Products & Services

### The Guardian Hub (Core Appliance)

All products are built around the Guardian Hub: a Raspberry Pi 4 running our custom AuraNet software, housed in a premium, silent, passive-cooling case for 24/7 reliability.

#### Hardware Specifications

| Component | Selection | Rationale |
|:----------|:----------|:----------|
| Computer | Raspberry Pi 4 (2GB) | Reliable, proven, sufficient power |
| Storage | 64GB Samsung Pro Endurance | Designed for continuous write operations |
| Case | Argon NEO | Passive cooling, silent, premium feel |
| Power | Official Pi USB-C PSU | Stability, reduces support issues |

---

### Product 1: Smart Wi-Fi Kit

**Target Customer:** Non-technical majority with basic ISP-provided routers or restrictive apartment networks.

**Value Proposition:** A complete network upgrade. Replaces old, slow router with high-speed Wi-Fi 6 system that's faster, safer, and ad-free.

**Contents:**
- Guardian Hub appliance
- TP-Link Archer AX55 Wi-Fi 6 Router
- All cables and accessories
- Printed quick-start guide
- Premium packaging

**Setup:** Simple "unplug old router, plug in new system"

**Pricing Strategy:**

| Phase | Price | Rationale |
|:------|:------|:----------|
| Founder's Launch (Beta) | $349 | Discounted for testimonials |
| Early Adopter | $449 | Reward early customers |
| Full Launch | $499 | Premium positioning |

**Unit Economics:**

| Item | Cost |
|:-----|:-----|
| Guardian Hub | $154 |
| Router & Accessories | $144 |
| Packaging | $10 |
| **Total COGS** | **$308** |
| | |
| Retail (Full Launch) | $499 |
| Payment Processing (3%) | -$15 |
| Shipping (included) | -$20 |
| **Net Profit** | **$156 (31%)** |

---

### Product 2: Network Supercharger

**Target Customer:** Users who have already invested in premium mesh Wi-Fi (Eero, Google Wifi, Orbi, TP-Link Deco).

**Value Proposition:** Enhancement for existing great network. Adds world-class filtering and parental controls seamlessly.

**Contents:**
- Guardian Hub appliance
- Ethernet cable
- Printed quick-start guide
- Premium packaging

**Setup:** Guided one-time DNS change within existing router's app

**Pricing Strategy:**

| Phase | Price | Rationale |
|:------|:------|:----------|
| Founder's Launch (Beta) | $199 | Discounted for testimonials |
| Early Adopter | $249 | Under $250 psychological barrier |
| Full Launch | $299 | Premium positioning |

**Unit Economics:**

| Item | Cost |
|:-----|:-----|
| Guardian Hub | $154 |
| Packaging | $8 |
| **Total COGS** | **$162** |
| | |
| Retail (Full Launch) | $299 |
| Payment Processing (3%) | -$9 |
| Shipping (included) | -$15 |
| **Net Profit** | **$113 (38%)** |

---

### Optional Add-On: Setup Support

| Add-On | Price | Includes |
|:-------|:------|:---------|
| Setup Support | +$50 | 30-min video call, router configuration help, troubleshooting |

**Rationale:** 
- Non-technical customers happily pay for hand-holding
- Technical customers save $50 and feel smart
- Compensates for support time
- Sets expectation that ongoing support isn't free

---

## 3.0 The AuraNet Dashboard (Software)

### Current Status: V2.0 Complete ✅

Our proprietary dashboard has been fully developed and tested, exceeding the original MVP specifications.

### Features Implemented

| Feature | Status | Description |
|:--------|:-------|:------------|
| Protection Modes | ✅ Complete | One-click Kids/Family/Standard modes |
| Pause Protection | ✅ Complete | Temporary disable (5m to 2h) |
| Allow/Block Websites | ✅ Complete | Simple domain management |
| Device Detection | ✅ Complete | Automatic network device discovery |
| Device Renaming | ✅ Complete | Custom names and icons |
| System Health | ✅ Complete | Monitoring and troubleshooting |
| Help & FAQ | ✅ Complete | Accordion-style, user-friendly |
| Professional UI | ✅ Complete | Clean, modern, mobile-responsive |

### Protection Modes

| Mode | Blocks | Target User |
|:-----|:-------|:------------|
| **Kids Mode** | Adult, social media, gambling, gaming, malware, ads | Young children |
| **Family Mode** | Adult, gambling, malware, ads | Mixed household |
| **Standard Mode** | Malware, phishing, ads, trackers | Adults only |

### Blocklist Strategy

Multiple redundant sources per category for resilience:

| Category | Primary Sources |
|:---------|:----------------|
| Malware/Phishing | StevenBlack, Hagezi Pro, BlockListProject, PhishingArmy |
| Ads/Tracking | Hagezi Light, OISD, BlockListProject |
| Adult Content | StevenBlack Adult, BlockListProject, OISD NSFW |
| Social Media | StevenBlack Social, BlockListProject |
| Gambling | BlockListProject, Hagezi |
| Gaming | BlockListProject |

### Remaining Development

| Feature | Priority | Effort | Target |
|:--------|:---------|:-------|:-------|
| "Whitelist Last Blocked" button | High | 1-2 hours | Before beta |
| Onboarding Wizard | High | 4-6 hours | Before beta |
| Bedtime Scheduler | Medium | 4-6 hours | V2.5 |
| Per-device filtering | Medium | 8-12 hours | V3.0 |
| Auto-update system | Low | 4-6 hours | Post-launch |

---

## 4.0 Market Analysis

### Australian Market Overview

| Metric | Value |
|:-------|:------|
| Total households | ~10 million |
| Households with children | ~45% (~4.5 million) |
| Broadband penetration | 86% |
| Average household devices | 17+ |

### Target Market Segments

**Primary:** Parents aged 35-55 with children aged 6-14
- Concerned about online safety
- Not technically confident
- Value simplicity over features
- Willing to pay for peace of mind

**Secondary:** Privacy-conscious adults
- Frustrated with ads and tracking
- Want "set and forget" solution
- May have existing mesh networks

### Competitive Landscape

| Competitor | Price (AUD) | Subscription | Available in AU | Notes |
|:-----------|:------------|:-------------|:----------------|:------|
| **Gryphon** | $449+ | $99/year | Ships from US | Slow shipping, US support only |
| **Firewalla** | $499-799 | No | Amazon AU | Complex, overkill for families |
| **Circle** | - | - | **Discontinued** | Disney killed product |
| **Bark Home** | $149 | $99/year | **No** | Not sold in AU |
| **Pi-hole DIY** | ~$100 | No | N/A | Requires technical knowledge |
| **AuraNet** | $249-499 | **No** | **Yes - Local** | Simple, supported, Australian |

### Competitive Advantages

| Advantage | Impact |
|:----------|:-------|
| No subscription fees | Major selling point vs Gryphon/Bark |
| Australian owned/supported | Trust factor, local support |
| Simple dashboard | Accessible to non-technical users |
| Lower price point | Undercuts Firewalla significantly |
| Works on all devices | No per-device software needed |
| Two-product strategy | Serves both market segments |

### Market Risks

| Risk | Likelihood | Mitigation |
|:-----|:-----------|:-----------|
| Router DNS locked by ISP | Medium | Smart Wi-Fi Kit bypasses this |
| Tech-savvy teens use VPN | Medium | Honest marketing, not 100% solution |
| Support costs exceed margin | Medium | Setup Support add-on, excellent docs |
| Raspberry Pi supply issues | Low | Maintain 20-30 unit inventory |
| Competitor enters AU market | Low | First mover advantage, local support |

---

## 5.0 Go-to-Market Strategy

### Phase 1: Development (COMPLETE ✅)

**Objective:** Build working prototype with full dashboard

**Status:**
- ✅ Hardware selected and tested
- ✅ Dashboard V2.0 complete
- ✅ All protection modes working
- ✅ Device management working
- ✅ GitHub backup established
- ✅ Golden Master image ready

---

### Phase 2: Founder's Launch (Beta Program)

**Timeline:** 2-4 weeks

**Objective:** Real-world testing, gather testimonials, refine product

**Actions:**

| Task | Details |
|:-----|:--------|
| Beta customers | 15-20 units, local area only |
| Installation | In-person "white-glove" service |
| Pricing | Discounted ($199 Supercharger / $349 Kit) |
| Documentation | Record every question and issue |
| Router testing | Test on Telstra, Optus, Aussie BB, TPG hardware |
| Testimonials | Video testimonials from happy customers |
| Feedback survey | "What would you pay?" "Would you recommend?" |

**Key Metrics to Track:**

| Metric | Target |
|:-------|:-------|
| Installation time | <30 minutes |
| Support calls per customer | <2 |
| Customer satisfaction | >8/10 |
| "Would recommend" rate | >80% |
| Willing to pay full price | >70% |

**Exit Criteria:** Proceed to Phase 3 when:
- 15+ successful installations
- Documented solutions for top 3 ISP routers
- At least 5 video testimonials
- Support issues are predictable and documented

---

### Phase 3: Early Adopter Launch

**Timeline:** 4-8 weeks

**Objective:** First online sales, refine fulfillment process

**Actions:**

| Task | Details |
|:-----|:--------|
| Website | Professional Shopify store |
| Pricing | Early Adopter pricing ($249 / $449) |
| Inventory | 20-30 units pre-built and tested |
| Marketing | Soft launch to parenting groups, local community |
| Fulfillment | Ship within 2 business days |
| Support | Email-based, 24-hour response target |

**Marketing Channels:**

| Channel | Budget | Expected ROI |
|:--------|:-------|:-------------|
| Facebook parenting groups | Organic | High |
| Instagram (parenting influencers) | $200-500 | Medium |
| School newsletters | Free | Medium |
| Local Facebook Marketplace | Free | Medium |
| Google Ads | $300-500 | Test |

---

### Phase 4: National E-commerce Launch

**Timeline:** Ongoing

**Objective:** Scale nationally with optimized operations

**Actions:**

| Task | Details |
|:-----|:--------|
| Pricing | Full pricing ($299 / $499) |
| Inventory | 50+ units, reorder at 20 |
| Marketing | Scaled digital campaigns |
| Partnerships | Tech reviewers, parenting blogs |
| Support | FAQ covers 90% of issues, consider chat |

---

## 6.0 Financial Projections

### Startup Costs

| Item | Cost |
|:-----|:-----|
| Initial inventory (10 Superchargers, 5 Kits) | $3,080 |
| Shopify setup (annual) | $400 |
| Domain and email | $50 |
| Packaging design/materials | $200 |
| Initial marketing | $500 |
| Contingency | $500 |
| **Total Startup** | **$4,730** |

### Year 1 Projections (Conservative)

**Assumptions:**
- Launch Month 3 (after beta)
- Gradual growth
- 60% Supercharger / 40% Kit mix
- Average order value: $350

| Month | Units | Revenue | Gross Profit |
|:------|:------|:--------|:-------------|
| 1-2 | 0 (beta) | $0 | -$500 (beta discounts) |
| 3 | 5 | $1,750 | $600 |
| 4 | 8 | $2,800 | $960 |
| 5 | 10 | $3,500 | $1,200 |
| 6 | 12 | $4,200 | $1,440 |
| 7 | 15 | $5,250 | $1,800 |
| 8 | 18 | $6,300 | $2,160 |
| 9 | 20 | $7,000 | $2,400 |
| 10 | 22 | $7,700 | $2,640 |
| 11 | 25 | $8,750 | $3,000 |
| 12 | 28 | $9,800 | $3,360 |
| **Year 1** | **163 units** | **$57,050** | **$19,060** |

**Year 1 Expenses:**

| Category | Annual Cost |
|:---------|:------------|
| Shopify + apps | $600 |
| Marketing | $3,000 |
| Shipping supplies | $500 |
| Support tools | $200 |
| Miscellaneous | $500 |
| **Total Expenses** | **$4,800** |

**Year 1 Net Profit: ~$14,260**

### Year 2 Projections (Growth)

**Assumptions:**
- Word of mouth established
- Reviews and testimonials driving sales
- 250 units sold
- Improved margins from bulk purchasing

**Year 2 Net Profit: ~$30,000-40,000**

### Break-Even Analysis

| Metric | Value |
|:-------|:------|
| Fixed costs (monthly) | ~$400 |
| Average profit per unit | ~$120 |
| Break-even units/month | 3-4 |

---

## 7.0 Operations

### Production Process

**"Golden Master" Workflow:**

1. Flash SD card with Golden Master image
2. Insert into Pi, assemble in case
3. Boot and run 90-second QA test
4. Configure for customer (if Smart Wi-Fi Kit, pair with router)
5. Package with quick-start guide
6. Ship

**Time per unit:** 15-20 minutes

**Quality Assurance Checklist:**

| Check | Pass Criteria |
|:------|:--------------|
| Boot successful | Dashboard loads within 90 seconds |
| DNS working | Can resolve google.com |
| Blocking working | Known ad domain is blocked |
| All LEDs normal | Power LED on, activity normal |
| Physical inspection | No damage, clean case |

### Inventory Management

| Trigger | Action |
|:--------|:-------|
| Stock < 10 Superchargers | Order 20 more Pi kits |
| Stock < 5 Smart Wi-Fi Kits | Order 10 more router bundles |
| Lead time | 1-2 weeks from order to received |

### Support Strategy

**Tier 1 (Self-Service):**
- Comprehensive FAQ on website
- Video tutorials for common routers
- Dashboard help section

**Tier 2 (Email Support):**
- 24-hour response time
- Template responses for common issues
- Escalation path to video call if needed

**Tier 3 (Paid Support):**
- Setup Support add-on ($50)
- 30-minute video call
- Scheduled appointment

---

## 8.0 Risk Management

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|:-----|:------------|:-------|:-----------|
| Blocklist source goes offline | Medium | Low | Multiple redundant sources per category |
| Pi-hole update breaks compatibility | Low | High | Test updates before pushing, rollback capability |
| SD card failure | Low | Medium | High-endurance cards, customer can re-flash |
| Raspberry Pi supply shortage | Low | High | Maintain 20-30 unit buffer stock |

### Business Risks

| Risk | Probability | Impact | Mitigation |
|:-----|:------------|:-------|:-----------|
| Support costs exceed projections | Medium | High | Excellent documentation, Setup Support add-on |
| Slow initial sales | Medium | Medium | Conservative inventory, low fixed costs |
| Competitor enters market | Low | Medium | First mover advantage, local support, brand loyalty |
| Negative review goes viral | Low | High | Excellent product quality, responsive support |

### Operational Risks

| Risk | Probability | Impact | Mitigation |
|:-----|:------------|:-------|:-----------|
| Router incompatibility | Medium | Medium | Smart Wi-Fi Kit option, router compatibility list |
| Customer can't configure DNS | Medium | Low | Video guides for top 10 routers, Setup Support |
| Shipping damage | Low | Low | Quality packaging, easy returns |

---

## 9.0 Success Metrics

### Phase 2 (Beta) Success Criteria

| Metric | Target |
|:-------|:-------|
| Successful installations | 15+ |
| Average install time | <30 min |
| Customer satisfaction | >8/10 |
| Referral willingness | >80% |
| Support issues documented | Top 10 |

### Phase 3 (Early Adopter) Success Criteria

| Metric | Target |
|:-------|:-------|
| Monthly units sold | 10+ |
| Customer support tickets | <2 per sale |
| Return rate | <5% |
| Average review rating | >4.5 stars |

### Phase 4 (Growth) Success Criteria

| Metric | Target |
|:-------|:-------|
| Monthly units sold | 25+ |
| Monthly revenue | $8,000+ |
| Repeat/referral rate | >30% |
| Support response time | <12 hours |

---

## 10.0 Immediate Next Steps

### This Week

| Task | Time | Priority |
|:-----|:-----|:---------|
| Add "Whitelist Last Blocked" button | 1-2 hours | High |
| Create fresh Golden Master .img | 30 min | High |
| Document full setup process | 2 hours | High |
| Test on Telstra Smart Modem | 1 hour | High |

### Before Beta Launch

| Task | Time | Priority |
|:-----|:-----|:---------|
| Build onboarding wizard | 4-6 hours | High |
| Create printed quick-start card | 2 hours | High |
| Record setup video (QR linked) | 2 hours | High |
| Test on 3 different router types | 2-3 hours | High |
| Prepare beta feedback survey | 1 hour | Medium |

### Before E-commerce Launch

| Task | Time | Priority |
|:-----|:-----|:---------|
| Build Shopify store | 4-6 hours | High |
| Product photography | 2-3 hours | High |
| Write product descriptions | 2 hours | High |
| Set up payment processing | 1 hour | High |
| Design packaging | 2-3 hours | Medium |
| Create router compatibility page | 2 hours | Medium |

---

## 11.0 Long-Term Vision

### Year 1: Foundation
- Establish brand in Australian market
- 150+ units sold
- Build customer testimonial library
- Refine product and support processes

### Year 2: Growth
- Expand to New Zealand
- 400+ units sold
- Introduce Bedtime Scheduler feature
- Consider retail partnerships (JB Hi-Fi, Officeworks)

### Year 3: Scale
- Per-device filtering capability
- Business/small office product variant
- Potential white-label partnerships with ISPs
- Consider subscription tier for advanced features (optional, not required)

---

## Appendix A: Technical Architecture

┌─────────────────────────────────────────────────────────────┐
│                     HOME NETWORK                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    ┌─────────┐      ┌─────────────┐      ┌─────────────┐   │
│    │ ROUTER  │──────│  AURANET    │      │  INTERNET   │   │
│    │         │ DNS  │  GUARDIAN   │      │             │   │
│    └─────────┘      │  HUB        │      └─────────────┘   │
│         │           └─────────────┘                         │
│         │                  │                                │
│    ┌────┴────┬────────┬────┴───┐                           │
│    │         │        │        │                           │
│  ┌─┴─┐    ┌─┴─┐   ┌─┴─┐   ┌─┴─┐                          │
│  │📱 │    │💻 │   │📺 │   │🎮 │   All devices protected   │
│  │   │    │   │   │   │   │   │                           │
│  └───┘    └───┘   └───┘   └───┘                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘

### Software Stack

| Layer | Technology |
|:------|:-----------|
| DNS Filtering | Pi-hole v6 |
| Dashboard Backend | Python Flask |
| Dashboard Frontend | Bootstrap 5, HTML5 |
| Database | SQLite (Pi-hole FTL) |
| Operating System | Raspberry Pi OS (Bookworm) |

---

## Appendix B: Competitor Comparison

| Feature | AuraNet | Gryphon | Firewalla | Circle |
|:--------|:--------|:--------|:----------|:-------|
| Price | $249-499 | $449+ | $499-799 | Discontinued |
| Subscription | **None** | $99/year | None | Was required |
| Local support | **Australia** | USA | USA | - |
| Ad blocking | ✅ | ✅ | ✅ | ❌ |
| Malware blocking | ✅ | ✅ | ✅ | ❌ |
| Parental controls | ✅ | ✅ | ✅ | ✅ |
| Easy setup | ✅ | ✅ | ❌ (complex) | ✅ |
| Works with existing router | ✅ | ❌ | ✅ | ✅ |
| Full router replacement | ✅ (Kit) | ✅ | ✅ | ❌ |

---

## Appendix C: Contact & Resources

**Founder:** Liam Albery

**Website:** [TBD]

**Support Email:** support@auranet.com.au

**GitHub (Private):** github.com/AuraNet-AU/auranet-dashboard

---

*Document Version: 2.0*
*Last Updated: 11/02/2026*
