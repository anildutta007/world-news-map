#!/usr/bin/env python3
"""
Generates news-database.js for World News Map.
Contains:
1. Deeply curated top-5 news per category (Economics, Business, Politics, Sports, Food, All)
   for major world nations across all continents.
2. Dynamic synthesis engine to generate topical top-5 news for any other country.
3. Global breaking ticker dataset.
"""

import json
import os

CURATED_NEWS = {
    "GB": {
        "name": "United Kingdom",
        "capital": "London",
        "flag": "🇬🇧",
        "currency": "GBP (£)",
        "categories": {
            "economics": [
                {
                    "id": "gb-econ-1",
                    "title": "Bank of England Holds Base Rate at 4.75% Amid Lingering Services Inflation",
                    "category": "economics",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "Financial Times",
                    "time": "25 mins ago",
                    "readTime": "3 min read",
                    "impact": "High Fiscal Impact",
                    "sentiment": "caution",
                    "summary": "The Monetary Policy Committee voted 7-2 to hold the base interest rate at 4.75%. Policymakers cited persistent services sector wage pressure despite headline CPI drifting closer to the 2% target.",
                    "keyTakeaways": [
                        "MPC vote split 7-2, signaling rate cuts will remain cautious and gradual.",
                        "Services inflation remains stubborn at 4.8%, driven by private sector wage settlements.",
                        "Gilt yields stabilized around 4.15% following the announcement."
                    ],
                    "fullStory": "The Bank of England's Monetary Policy Committee decided by a 7-2 majority to maintain the Bank Rate at 4.75%, opting for caution in the face of persistent domestic price pressures. While headline consumer price inflation has receded significantly from its double-digit peak, policymakers highlighted resilience in the services sector and wage growth as reasons for maintaining a restrictive monetary stance.\n\nGovernor Andrew Bailey noted in his press briefing that while the disinflation process is broadly on track, the committee cannot declare victory prematurely. Chancellor Rachel Reeves welcomed signs of macroeconomic stabilization while emphasizing the government's commitment to fiscal discipline and supply-side reforms aimed at unlocking long-term productivity.\n\nSterling held steady against both the US Dollar and Euro following the release of the minutes, as traders scaled back aggressive expectations for year-end rate reductions. Analysts widely expect the next quarter-point rate trim to emerge in early 2027.",
                    "tags": ["Bank of England", "Interest Rates", "Inflation", "Gilts"]
                },
                {
                    "id": "gb-econ-2",
                    "title": "UK Productivity Rises 0.6% Driven by Advanced Manufacturing and AI Integration",
                    "category": "economics",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "Reuters",
                    "time": "1 hour ago",
                    "readTime": "2 min read",
                    "impact": "Positive Growth",
                    "sentiment": "positive",
                    "summary": "Office for National Statistics figures revealed output per hour worked increased by 0.6% quarter-on-quarter, led by aerospace engineering, pharmaceuticals, and enterprise automation adoption.",
                    "keyTakeaways": [
                        "First positive productivity streak in three consecutive quarters.",
                        "Industrial automation and tech investments delivered highest labor efficiency gains.",
                        "Regional manufacturing hubs in the Midlands and North outperformed London."
                    ],
                    "fullStory": "British labor productivity recorded its most promising uptick in over eighteen months, expanding by 0.6% on an output-per-hour basis according to latest data from the Office for National Statistics (ONS). The acceleration was heavily anchored by high-value manufacturing, green aerospace, and pharmaceutical research clusters.\n\nIndustry leaders attributed the gains to capital expenditure in smart factory automation and enterprise AI tooling. Economists noted that if sustained, this productivity revival could create meaningful fiscal headroom for public infrastructure investment without triggering inflationary wage spirals.",
                    "tags": ["ONS", "Productivity", "Manufacturing", "AI Adoption"]
                },
                {
                    "id": "gb-econ-3",
                    "title": "Treasury Unveils £15 Billion Green Sovereign Bond Issuance for Grid Upgrades",
                    "category": "economics",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "Bloomberg UK",
                    "time": "3 hours ago",
                    "readTime": "3 min read",
                    "impact": "Infrastructure Milestone",
                    "sentiment": "positive",
                    "summary": "HM Treasury confirmed a new tranche of Green Gilts to finance high-voltage subsea electricity connectors and regional battery storage hubs across Scotland and North England.",
                    "keyTakeaways": [
                        "Order book oversubscribed by 3.4 times from institutional pension funds.",
                        "Proceeds ring-fenced for Great British Energy transmission network modernization.",
                        "Expected to unlock 12 GW of clean offshore wind capacity by 2028."
                    ],
                    "fullStory": "The UK Debt Management Office confirmed a landmark £15 billion Green Gilt offering, which was met with fierce demand from institutional investors, asset managers, and sovereign wealth funds. The green sovereign paper will directly fund critical transmission network upgrades led by National Grid and Great British Energy.\n\nThe initiative addresses long-standing grid queue bottlenecks, enabling hundreds of newly constructed offshore wind installations off the North Sea and Celtic Sea to interconnect seamlessly with industrial demand centres across urban England.",
                    "tags": ["Green Gilts", "National Grid", "Energy Transition", "Treasury"]
                },
                {
                    "id": "gb-econ-4",
                    "title": "UK Trade Deficit Narrows as Digital Services and FinTech Exports Hit All-Time High",
                    "category": "economics",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "The Economist",
                    "time": "5 hours ago",
                    "readTime": "3 min read",
                    "impact": "Trade Surplus in Services",
                    "sentiment": "positive",
                    "summary": "The overall UK trade gap shrank by £2.8 billion in the last quarter as international demand for British legal services, management consultancy, and fintech platforms surged across Asia and North America.",
                    "keyTakeaways": [
                        "Services surplus expanded to £39.4 billion, offsetting the goods trade deficit.",
                        "Bilateral services exports to the US and Indo-Pacific grew by 11.2% year-on-year.",
                        "London and Edinburgh fintech corridors drove record overseas licensing revenue."
                    ],
                    "fullStory": "Britain's knowledge economy demonstrated its structural resilience as the quarterly trade deficit narrowed substantially. Booming overseas revenues from specialized cross-border financial services, legal technology, and cybersecurity architecture compensated for subdued merchandise trade with continental Europe.\n\nTrade officials highlighted that the UK's accession to the CPTPP trade pact has started yielding measurable export dividends for UK software and creative media firms entering fast-growing markets like Japan, Malaysia, and Australia.",
                    "tags": ["Trade Balance", "Fintech", "Services Exports", "CPTPP"]
                },
                {
                    "id": "gb-econ-5",
                    "title": "House Price Index Rises 2.1% Annually as Mortgage Approvals Rebound to 2-Year High",
                    "category": "economics",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "Nationwide / BBC News",
                    "time": "7 hours ago",
                    "readTime": "2 min read",
                    "impact": "Housing Stability",
                    "sentiment": "neutral",
                    "summary": "Nationwide Building Society data shows average UK property prices reached £268,000, supported by competitive mortgage lender rate cuts and strong buyer demand from first-time applicants.",
                    "keyTakeaways": [
                        "Monthly mortgage approvals reached 68,000, the strongest pace since autumn 2024.",
                        "Five-year fixed mortgage rates have settled between 3.9% and 4.3%.",
                        "Northern and Scottish property markets experienced fastest price appreciation."
                    ],
                    "fullStory": "The UK property market demonstrated renewed stability as nationwide mortgage rates stabilized below 4.2% for high-equity borrowers. The Nationwide House Price Index registered a 2.1% annual gain, marking the fourth consecutive month of positive price momentum.\n\nWhile structural affordability challenges remain acute in London and the South East due to high price-to-income multiples, regional markets in Yorkshire, the North West, and Central Scotland saw heightened bidding activity from professional buyers seeking value.",
                    "tags": ["Housing Market", "Mortgages", "Nationwide Index", "Property"]
                }
            ],
            "business": [
                {
                    "id": "gb-biz-1",
                    "title": "Arm Holdings Partners with Cambridge Quantum Hub to Pioneer Hybrid AI Chips",
                    "category": "business",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "Bloomberg",
                    "time": "30 mins ago",
                    "readTime": "3 min read",
                    "impact": "Tech Leadership",
                    "sentiment": "positive",
                    "summary": "Cambridge-based Arm unveiled a strategic architecture initiative with British quantum computing pioneers to integrate neural processing units directly onto next-generation cloud server silicon.",
                    "keyTakeaways": [
                        "£500 million collaborative development pipeline over the next three years.",
                        "Targets 40% reduction in data center power consumption for enterprise LLM workloads.",
                        "Strengthens UK's position as a global tier-1 semiconductor intellectual property powerhouse."
                    ],
                    "fullStory": "Arm Holdings announced an ambitious multi-year collaboration with leading Cambridge research spinouts to create hybrid silicon architectures that blend Arm Neoverse cores with specialized optical and quantum computing accelerators.\n\nThe venture aims to solve the staggering energy consumption curve of hyperscale AI training clusters. By performing mathematical tensor operations with lower thermodynamic dissipation, the new platform targets an unprecedented efficiency leap for enterprise cloud infrastructure.",
                    "tags": ["Arm Holdings", "Semiconductors", "Artificial Intelligence", "Cambridge"]
                },
                {
                    "id": "gb-biz-2",
                    "title": "Rolls-Royce Secures £3.2 Billion Small Modular Reactor Export Order to Central Europe",
                    "category": "business",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "The Daily Telegraph",
                    "time": "1 hour ago",
                    "readTime": "3 min read",
                    "impact": "Industrial Export Win",
                    "sentiment": "positive",
                    "summary": "Rolls-Royce SMR signed a binding commercial agreement to deploy four factory-manufactured nuclear mini-reactors to supply carbon-free baseload energy to heavy industrial manufacturing complexes.",
                    "keyTakeaways": [
                        "First international commercial export contract for the British SMR design.",
                        "Manufacturing facilities in Derby and Sheffield to create 1,800 specialized engineering jobs.",
                        "First reactor expected to achieve commercial grid synchronization by 2031."
                    ],
                    "fullStory": "Rolls-Royce SMR reached a monumental commercial milestone after sealing a £3.2 billion contract with a European industrial consortium to construct four factory-built Small Modular Reactors. The reactors will provide steady, decarbonized electricity and industrial heat for steel mills and chemical refineries.\n\nChief Executive Tufan Erginbilgic noted that the standardized modular manufacturing process cuts construction timelines by more than half compared to conventional gigawatt-scale atomic plants, establishing the UK as a pioneering exporter in the global atomic renaissance.",
                    "tags": ["Rolls-Royce", "Nuclear Power", "SMR", "Clean Tech"]
                },
                {
                    "id": "gb-biz-3",
                    "title": "London Stock Exchange Welcomes 3 Major European Tech IPOs in Landmark Week",
                    "category": "business",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "City A.M.",
                    "time": "4 hours ago",
                    "readTime": "2 min read",
                    "impact": "Capital Markets Boost",
                    "sentiment": "positive",
                    "summary": "Following recent listing regime simplifications by the FCA, three high-growth software and renewable energy startups completed listings raising over £1.4 billion on the London main market.",
                    "keyTakeaways": [
                        "FCA's unified commercial company listing category proves attractive to founder-led firms.",
                        "Dual-class voting rights flexibility retained founders' long-term governance authority.",
                        "FTSE 100 and FTSE 250 trading volumes rose 14% week-on-week."
                    ],
                    "fullStory": "The London Stock Exchange registered its busiest week for initial public offerings in four years as three high-profile European tech firms went public in London. The successful flotations provide tangible validation for the Financial Conduct Authority's streamlined listing reforms introduced earlier this year.\n\nThe newly listed entities, encompassing climate tech telemetry, enterprise workflow automation, and cross-border payment rails, were substantially oversubscribed by both UK pension funds and international institutional investors.",
                    "tags": ["LSE", "IPOs", "FinTech", "City of London"]
                },
                {
                    "id": "gb-biz-4",
                    "title": "AstraZeneca Commits £800M R&D Campus Expansion in Macclesfield and Liverpool",
                    "category": "business",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "The Times",
                    "time": "6 hours ago",
                    "readTime": "3 min read",
                    "impact": "Life Sciences Investment",
                    "sentiment": "positive",
                    "summary": "Pharmaceutical giant AstraZeneca finalized plans to expand its biomanufacturing and sterile injectable production plants, solidifying the UK Life Sciences Corridor.",
                    "keyTakeaways": [
                        "Facilities to manufacture antibody drug conjugates and next-generation oncology treatments.",
                        "Project backed by UK Life Sciences Innovative Manufacturing Fund.",
                        "Secures 1,200 high-skill research and cleanroom engineering roles."
                    ],
                    "fullStory": "AstraZeneca underscored its long-term commitment to British scientific manufacturing with an £800 million capital allocation across its North West facilities in Macclesfield and Speke, Liverpool. The site will house automated sterile filling lines and bioreactors for revolutionary cancer therapies.\n\nThe investment was praised by both industry leaders and clinical trial specialists, who underscored that maintaining domestic production of advanced biological therapeutics safeguards national health resilience against global pharmaceutical supply shocks.",
                    "tags": ["AstraZeneca", "Life Sciences", "Pharma", "Manufacturing"]
                },
                {
                    "id": "gb-biz-5",
                    "title": "British Airways and Virgin Atlantic Scale Sustainable Aviation Fuel at Heathrow",
                    "category": "business",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "Evening Standard",
                    "time": "8 hours ago",
                    "readTime": "2 min read",
                    "impact": "Green Aviation",
                    "sentiment": "neutral",
                    "summary": "Airlines operating out of London Heathrow have integrated a mandatory 3% Sustainable Aviation Fuel (SAF) blend into transatlantic flight operations ahead of strict 2030 decarbonization targets.",
                    "keyTakeaways": [
                        "Over 120 long-haul flights daily now utilize waste-oil-derived SAF blends.",
                        "Government revenue certainty mechanism spurs new SAF refinery construction in Teesside.",
                        "Passenger green surcharge remains modest under £4 per transatlantic ticket."
                    ],
                    "fullStory": "In a tangible stride toward net-zero aviation, British Airways and Virgin Atlantic announced that their long-haul fleets out of Heathrow Airport have reached a continuous 3% SAF fuel integration threshold. The sustainable fuel, derived from used cooking oils and agricultural residues, reduces lifecycle lifecycle carbon emissions by over 70% compared to conventional kerosene.",
                    "tags": ["Aviation", "Heathrow", "British Airways", "Net Zero"]
                }
            ],
            "politics": [
                {
                    "id": "gb-pol-1",
                    "title": "Parliament Passes Historic Planning and Infrastructure Bill to Fast-Track Clean Energy",
                    "category": "politics",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "BBC News",
                    "time": "45 mins ago",
                    "readTime": "3 min read",
                    "impact": "Legislative Reform",
                    "sentiment": "positive",
                    "summary": "The landmark legislation overhauls local council vetoes on national critical infrastructure, cutting judicial review delays for wind farms, nuclear sites, and data centres from 5 years to 18 months.",
                    "keyTakeaways": [
                        "Bill passed House of Commons with a comfortable 92-vote majority.",
                        "Empowers national planning inspectors to designate priority clean power corridors.",
                        "Introduces binding local community dividend funds for areas hosting new transmission pylons."
                    ],
                    "fullStory": "Members of Parliament passed the government's flagship Planning and Infrastructure Bill, marking the most consequential rewriting of British planning laws in several decades. The new statutory framework strips away protracted bureaucratic hurdles that have historically stalled vital energy transmission lines, reservoir projects, and railway modernization.\n\nMinisters argued that modernizing the UK's archaic planning system is indispensable to unlocking private capital and achieving the country's legally binding 2030 clean power mission.",
                    "tags": ["Parliament", "Planning Reform", "Legislation", "House of Commons"]
                },
                {
                    "id": "gb-pol-2",
                    "title": "UK and European Union Conclude New Security and Intelligence Sharing Pact",
                    "category": "politics",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "The Guardian",
                    "time": "2 hours ago",
                    "readTime": "3 min read",
                    "impact": "Diplomatic Alliance",
                    "sentiment": "positive",
                    "summary": "British and EU leaders signed a comprehensive defense cooperation treaty in Brussels, establishing real-time cyber defense coordination and joint procurement frameworks for NATO allies.",
                    "keyTakeaways": [
                        "Formalizes mutual defense assistance on hybrid warfare and undersea cable protection.",
                        "UK defense manufacturers gain preferential access to EU joint ammunition procurement pools.",
                        "Strengthens cross-border intelligence sharing on illicit financing networks."
                    ],
                    "fullStory": "The Prime Minister met European Commission leadership in Brussels to sign a landmark Security and Defense Cooperation Agreement, symbolizing a pragmatic reset in post-Brexit relations. The treaty focuses on collective deterrence against state-sponsored cyber warfare, maritime infrastructure sabotage, and aerospace defense readiness.",
                    "tags": ["UK-EU Relations", "Defense", "NATO", "Brussels"]
                },
                {
                    "id": "gb-pol-3",
                    "title": "Devolution Revolution: Combined Authorities in North and Midlands Gain Tax-Raising Powers",
                    "category": "politics",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "The Yorkshire Post",
                    "time": "4 hours ago",
                    "readTime": "2 min read",
                    "impact": "Regional Governance",
                    "sentiment": "positive",
                    "summary": "Metro Mayors across Greater Manchester, West Midlands, and West Yorkshire have been granted multi-year consolidated funding settlements and localized transit franchise authority.",
                    "keyTakeaways": [
                        "End to competitive bidding grants for transport and adult education schemes.",
                        "Mayors granted powers to integrate local bus and suburban rail into London-style contactless ticketing.",
                        "Treasury transfers £4.2 billion directly to regional mayoral accounts."
                    ],
                    "fullStory": "In a substantial decentralization of Whitehall power, the UK Government announced single multi-year funding pots for metro mayors across England. The transition removes bureaucratic departmental micromanagement, allowing regional leaders to deploy capital directly into localized light rail networks, affordable housing schemes, and apprenticeship colleges.",
                    "tags": ["Devolution", "Metro Mayors", "Levelling Up", "Local Government"]
                },
                {
                    "id": "gb-pol-4",
                    "title": "Civil Service Digital Transformation Cuts Public Administration Overhead by £1.8B",
                    "category": "politics",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "Civil Service World",
                    "time": "6 hours ago",
                    "readTime": "2 min read",
                    "impact": "Public Sector Reform",
                    "sentiment": "positive",
                    "summary": "Cabinet Office reports that the rollout of automated citizen service portals and unified data registries has halved processing times for passport renewals, driving licences, and tax filings.",
                    "keyTakeaways": [
                        "GOV.UK digital app adoption surpasses 22 million active verified citizens.",
                        "Administrative backlogs across passport and probate offices reduced to historic lows.",
                        "Saved funds redirected toward frontline NHS clinical personnel and policing."
                    ],
                    "fullStory": "The Cabinet Office published its annual Civil Service Modernization Audit, detailing how standardized digital citizen journeys and workflow automation have successfully generated £1.8 billion in annual administrative savings across Whitehall departments.",
                    "tags": ["Cabinet Office", "Digital Government", "Public Spending", "GOV.UK"]
                },
                {
                    "id": "gb-pol-5",
                    "title": "Electoral Commission Implements Automated Voter Registration for Young Adults",
                    "category": "politics",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "The Independent",
                    "time": "9 hours ago",
                    "readTime": "2 min read",
                    "impact": "Democratic Engagement",
                    "sentiment": "positive",
                    "summary": "New pilot program automatically enrols school leavers and university students onto the electoral roll upon receiving their National Insurance number, expanding voter participation.",
                    "keyTakeaways": [
                        "Over 650,000 young citizens added to the electoral register ahead of local council elections.",
                        "Bipartisan committee praises move as major step forward for civic engagement.",
                        "Digital identity verification prevents duplications across multiple home and university addresses."
                    ],
                    "fullStory": "Britain's Electoral Commission launched an automated voter registration system connecting National Insurance number issuance with local electoral rolls. The modernization guarantees that young citizens turning 18 are automatically enrolled to vote, curbing historical disengagement among student demographics.",
                    "tags": ["Elections", "Democracy", "Voter Registration", "Civic Tech"]
                }
            ],
            "sports": [
                {
                    "id": "gb-sprt-1",
                    "title": "Premier League Agrees Historic £6.8B Domestic Broadcast Deal with Extended 4K HDR Coverage",
                    "category": "sports",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "Sky Sports / BBC Sport",
                    "time": "40 mins ago",
                    "readTime": "2 min read",
                    "impact": "Commercial Football Milestone",
                    "sentiment": "positive",
                    "summary": "The Premier League confirmed a four-year television rights extension with Sky and TNT Sports featuring all Sunday afternoon matches broadcast live with biometric and tactical overlay technology.",
                    "keyTakeaways": [
                        "Over 270 live fixtures per season to be shown domestically.",
                        "Parachute and solidarity payments to English Football League (EFL) clubs boosted by 18%.",
                        "AI automated offside technology achieves 99.4% approval rating among managers."
                    ],
                    "fullStory": "The English Premier League finalized an unprecedented £6.8 billion four-year domestic broadcasting arrangement. For the first time in top-flight history, every single fixture played on a Sunday will be televised live, supported by cutting-edge ultra-high-definition cameras and augmented-reality tactical replays.\n\nCritically, the agreement includes enhanced solidarity distributions to League One and League Two academies, reinforcing the grassroots foundation of English football.",
                    "tags": ["Premier League", "Football", "Sky Sports", "EFL"]
                },
                {
                    "id": "gb-sprt-2",
                    "title": "England Cricket Team Clinches Thrilling Decider Against India at The Oval",
                    "category": "sports",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "The Cricketer / Wisden",
                    "time": "2 hours ago",
                    "readTime": "3 min read",
                    "impact": "Test Match Victory",
                    "sentiment": "positive",
                    "summary": "In front of a packed Oval crowd, England's aggressive 'Bazball' tactics yielded a heart-stopping 24-run triumph on Day 5, securing the five-match Test series 3-2.",
                    "keyTakeaways": [
                        "Ben Stokes' tactical bowling rotations dismissed the final two wickets with just 15 minutes to spare.",
                        "Harry Brook named Player of the Series after scoring 482 runs at an average of 68.8.",
                        "Match celebrated as one of the finest Test encounters played in London this decade."
                    ],
                    "fullStory": "In one of the most enthralling finishes witnessed in modern cricket history, England sealed a 24-run victory over India on the final afternoon of the fifth Test at The Oval. With India needing only 25 runs with two wickets in hand, England's seam attack produced reverse-swing masterclasses under overcast South London skies.",
                    "tags": ["Cricket", "The Oval", "Test Series", "England Cricket"]
                },
                {
                    "id": "gb-sprt-3",
                    "title": "Wimbledon Unveils State-of-the-Art Retractable Roof and Solar Canopy on Court No. 2",
                    "category": "sports",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "The Telegraph Sport",
                    "time": "4 hours ago",
                    "readTime": "2 min read",
                    "impact": "Tennis Infrastructure",
                    "sentiment": "positive",
                    "summary": "The All England Lawn Tennis Club completed construction of its third roofed show court, ensuring continuous championship play regardless of London rainfall.",
                    "keyTakeaways": [
                        "Court No. 2 roof deploys in 8 minutes with ultra-quiet pneumatic seals.",
                        "Solar glass integrated into the canopy powers 60% of Wimbledon village facilities.",
                        "Increases guaranteed rainy-day spectator capacity to over 32,000 tennis fans."
                    ],
                    "fullStory": "The All England Club formally inaugurated the new retractable canopy over Court No. 2 at Church Road. The architectural marvel ensures that rain delays will no longer disrupt marquee matches across the tournament's three primary show courts, while retaining the venue's world-famous natural lawn microclimate.",
                    "tags": ["Wimbledon", "Tennis", "All England Club", "Grand Slam"]
                },
                {
                    "id": "gb-sprt-4",
                    "title": "Lando Norris Takes Dramatic British Grand Prix Victory at Silverstone",
                    "category": "sports",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "Autosport",
                    "time": "6 hours ago",
                    "readTime": "3 min read",
                    "impact": "Formula 1 Glory",
                    "sentiment": "positive",
                    "summary": "McLaren's British driver mastered changing wet-dry conditions to take a maiden home win at Silverstone, holding off Max Verstappen in front of 160,000 cheering fans.",
                    "keyTakeaways": [
                        "First British driver to win at Silverstone for McLaren since Lewis Hamilton in 2008.",
                        "Flawless pit-stop strategy switched to intermediate tyres on lap 34 as heavy rain hit Copse corner.",
                        "Championship title fight tightens to just 12 points with seven races remaining."
                    ],
                    "fullStory": "Lando Norris sent the Silverstone grandstands into ecstasy after taking an emotional, hard-fought victory at the British Grand Prix. In a race punctuated by treacherous British summer showers, McLaren's tyre management and Norris's sublime car control proved decisive over 52 pulsating laps.",
                    "tags": ["Formula 1", "Silverstone", "Lando Norris", "McLaren"]
                },
                {
                    "id": "gb-sprt-5",
                    "title": "Lionesses Qualify for UEFA Women's Euro Knockout Stage with 4-0 Win",
                    "category": "sports",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "BBC Sport",
                    "time": "8 hours ago",
                    "readTime": "2 min read",
                    "impact": "Women's Football",
                    "sentiment": "positive",
                    "summary": "England's women's national football team dispatched their group stage opponents with commanding possession play and a hat-trick from Alessia Russo in front of 72,000 at Wembley.",
                    "keyTakeaways": [
                        "Sarina Wiegman's side remains undefeated in tournament competitive fixtures.",
                        "Alessia Russo's clinical finishing solidifies her position atop the Golden Boot rankings.",
                        "Quarter-final showdown scheduled against France in Amsterdam next Friday."
                    ],
                    "fullStory": "The Lionesses marched into the Euro knockout stages with a swagger, routing their rivals 4-0 under the Wembley arch. Sarina Wiegman's tactical fluidity and defensive solidity demonstrated why the reigning European champions remain hot favorites to retain their continental crown.",
                    "tags": ["Lionesses", "Women's Football", "Wembley", "UEFA Euro"]
                }
            ],
            "food": [
                {
                    "id": "gb-food-1",
                    "title": "Michelin Guide Awards 3 New Three-Star Accolades to British Regional Dining",
                    "category": "food",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "The Caterer / Michelin Guide",
                    "time": "50 mins ago",
                    "readTime": "3 min read",
                    "impact": "Gastronomy Excellence",
                    "sentiment": "positive",
                    "summary": "Restaurants in the Lake District, Edinburgh, and Cornwall were elevated to the supreme three-star rating, celebrating hyper-seasonal British terroir, regenerative farming, and foraged coastal ingredients.",
                    "keyTakeaways": [
                        "Cumbria restaurant praised for zero-waste estate farming and heritage livestock preservation.",
                        "Scotland gains its first three-Michelin-starred establishment in thirty years.",
                        "Highlights Britain's transition into one of Europe's most dynamic gastronomic destinations."
                    ],
                    "fullStory": "The Michelin Guide Great Britain & Ireland revealed its newest ceremony results, awarding the prestigious three-star status to three regional destination restaurants located far outside London. The inspectors highlighted a profound commitment to micro-seasonal foraging, hyper-local seafood from Cornish and Hebridean day-boats, and biodynamic farm-to-table ethics.\n\nInspectors particularly commended the emergence of innovative techniques celebrating native British ingredients—such as sea buckthorn, woodruff, and heritage breed Dexter cattle—over imported culinary tropes.",
                    "tags": ["Michelin Guide", "Gastronomy", "Fine Dining", "Farm to Table"]
                },
                {
                    "id": "gb-food-2",
                    "title": "UK Artisan Farmhouse Cheese Exports Surpass Continental Roquefort and Gouda in US Market",
                    "category": "food",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "Speciality Food Magazine",
                    "time": "2 hours ago",
                    "readTime": "2 min read",
                    "impact": "Artisan Export Boom",
                    "sentiment": "positive",
                    "summary": "Traditional raw-milk Cheddar, Stilton, and Welsh Caerphilly experienced a 24% surge in demand across gourmet American grocers and high-end delis.",
                    "keyTakeaways": [
                        "Clothbound Cheddars aged over 18 months command premium prices in New York and California.",
                        "Protected Designation of Origin (PDO) certification safeguards traditional raw-milk cheesemaking.",
                        "Small-scale British dairy farmers benefit from higher farm-gate milk premiums."
                    ],
                    "fullStory": "British farmhouse cheesemakers are enjoying an unprecedented renaissance overseas as exports to the United States reached record volumes. Discerning American consumers have increasingly turned away from mass-produced cheeses in favor of complex, crumbly, raw-milk farmhouse cheddars from Somerset, raw stiltons from Nottinghamshire, and goat curd from the Wye Valley.",
                    "tags": ["Artisan Cheese", "Dairy Farming", "Food Exports", "British Food"]
                },
                {
                    "id": "gb-food-3",
                    "title": "Vertical Farming Hub in Norfolk Ships First Commercial Crop of Pest-Free Strawberries",
                    "category": "food",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "Farmers Weekly",
                    "time": "4 hours ago",
                    "readTime": "3 min read",
                    "impact": "Agritech Innovation",
                    "sentiment": "positive",
                    "summary": "Europe's largest indoor aeroponic facility began delivering sweet British berries to national supermarkets year-round, using 95% less water and zero synthetic pesticides.",
                    "keyTakeaways": [
                        "Powered entirely by co-located biomethane and solar energy arrays.",
                        "Eliminates dependency on overseas winter strawberry imports from Spain and Morocco.",
                        "Precision LED wavelength tuning increases natural Brix sugar sweetness by 18%."
                    ],
                    "fullStory": "A state-of-the-art vertical farming facility spanning 15,000 square meters in Norfolk delivered its first full-scale commercial harvest of British strawberries to major supermarket aisles. Utilizing advanced aeroponics and spectral lighting tailored to berry photosynthesis, the facility operates 365 days a year without soil or weather risk.",
                    "tags": ["Vertical Farming", "Agritech", "Strawberries", "Sustainability"]
                },
                {
                    "id": "gb-food-4",
                    "title": "Revival of the Great British Pub: Independent Gastropubs Outperform High Street Chains",
                    "category": "food",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "Good Food Guide",
                    "time": "7 hours ago",
                    "readTime": "2 min read",
                    "impact": "Hospitality Trend",
                    "sentiment": "positive",
                    "summary": "Independent community-owned and chef-led gastropubs focusing on local cask ales, Sunday roasts with dry-aged beef, and community hubs saw sales climb 8.4% despite energy cost pressures.",
                    "keyTakeaways": [
                        "Consumers prioritize quality, provenance, and warm hospitality over bland chain dining.",
                        "CAMRA (Campaign for Real Ale) reports spike in community pub ownership buyouts.",
                        "Modern pub menus embrace seasonal venison, hand-raised pies, and wild mushroom tarts."
                    ],
                    "fullStory": "While standardized high street restaurant chains face headwinds, the classic British independent pub is experiencing a cultural and culinary resurgence. The Good Food Guide noted that establishments marrying high-craft cooking with unpretentious hospitality, real cask ales, and authentic community roots are thriving across the UK countryside and towns.",
                    "tags": ["Gastropubs", "CAMRA", "Hospitality", "Sunday Roast"]
                },
                {
                    "id": "gb-food-5",
                    "title": "Cornish Sea Salt and Seaweed Kelp Harvesting Awarded UNESCO Intangible Heritage Status",
                    "category": "food",
                    "country": "United Kingdom",
                    "countryCode": "GB",
                    "source": "Cornwall Live / Guardian Feast",
                    "time": "10 hours ago",
                    "readTime": "2 min read",
                    "impact": "Cultural Heritage",
                    "sentiment": "positive",
                    "summary": "Centuries-old sustainable coastal foraging techniques practiced in the coves of the Lizard Peninsula were formally recognized for environmental stewardship and maritime culinary tradition.",
                    "keyTakeaways": [
                        "Hand-harvested sea minerals sought after by pastry chefs for flaky salt finishes worldwide.",
                        "Regenerative seaweed harvesting creates new economic opportunities for former fishing villages.",
                        "Marine conservation zone guarantees kelp forest replenishment."
                    ],
                    "fullStory": "The ancient practice of sea salt evaporation and edible kelp harvesting along the rugged cliffs of Cornwall received international acclaim with a prestigious heritage designation. Local artisan cooperatives continue to draw pristine Atlantic seawater to produce mineral-rich flaky crystals that have become a staple in fine dining kitchens globally.",
                    "tags": ["Cornwall", "Sea Salt", "Culinary Heritage", "Seaweed"]
                }
            ]
        }
    },
    "US": {
        "name": "United States",
        "capital": "Washington, D.C.",
        "flag": "🇺🇸",
        "currency": "USD ($)",
        "categories": {
            "economics": [
                {
                    "id": "us-econ-1",
                    "title": "Federal Reserve Lowers Target Rate by 25 Bps as Core PCE Deflator Cools to 2.2%",
                    "category": "economics",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "The Wall Street Journal",
                    "time": "20 mins ago",
                    "readTime": "3 min read",
                    "impact": "Global Market Catalyst",
                    "sentiment": "positive",
                    "summary": "The Federal Open Market Committee reduced the federal funds target range to 4.25%-4.50%, highlighting balanced employment risks and steady progress toward the 2% price stability mandate.",
                    "keyTakeaways": [
                        "Decision was unanimous among voting members of the FOMC.",
                        "S&P 500 and Nasdaq posted immediate record intraday highs on easing liquidity conditions.",
                        "Fed Chairman emphasizes future adjustments will depend on incoming labor market metrics."
                    ],
                    "fullStory": "The Federal Reserve continued recalibrating its policy stance with a widely anticipated 25-basis-point reduction in the benchmark federal funds rate. Fed Chairman Jerome Powell noted during his press conference that economic activity continues to expand at a solid pace, but lower inflation readings warrant normalizing rates away from restrictive territory.\n\nThe yield on the 10-year Treasury note dipped by 6 basis points to 3.98%, while major equity indices gained ground. Corporate treasurers welcomed the reduction, which is expected to lower commercial borrowing costs and catalyze private capital expenditures.",
                    "tags": ["Federal Reserve", "FOMC", "Interest Rates", "Wall Street"]
                },
                {
                    "id": "us-econ-2",
                    "title": "US Nonfarm Payrolls Expand by 195,000 as Healthcare and Tech Hiring Rebound",
                    "category": "economics",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "Bloomberg Markets",
                    "time": "1 hour ago",
                    "readTime": "2 min read",
                    "impact": "Labor Strength",
                    "sentiment": "positive",
                    "summary": "Department of Labor data reported the unemployment rate held steady at 4.1%, defying recession fears while average hourly earnings rose at an annualized 3.7% pace.",
                    "keyTakeaways": [
                        "Professional services and advanced technology added 42,000 net new positions.",
                        "Labor force participation rate among prime-age workers rose to 83.6%.",
                        "Wage gains aligned with non-inflationary productivity trends."
                    ],
                    "fullStory": "The American labor engine maintained steady momentum in the latest Bureau of Labor Statistics establishment survey. Nonfarm payrolls exceeded consensus expectations with 195,000 net new jobs created. Job gains were broadly distributed, led by healthcare systems, clean energy installation, and specialized software engineering.",
                    "tags": ["Jobs Report", "Labor Market", "BLS", "Unemployment"]
                },
                {
                    "id": "us-econ-3",
                    "title": "CHIPS Act Fab Construction Milestone: TSMC and Intel Phoenix Megasites Near Production",
                    "category": "economics",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "The New York Times",
                    "time": "3 hours ago",
                    "readTime": "3 min read",
                    "impact": "Strategic Supply Chain",
                    "sentiment": "positive",
                    "summary": "Over $65 billion in advanced semiconductor manufacturing fabs in Arizona and Ohio achieved cleanroom certification, marking the physical realization of domestic chip security.",
                    "keyTakeaways": [
                        "3nm and 2nm silicon wafers slated for volume qualification runs by Q2 2027.",
                        "Spurred an ecosystem of 40+ specialized chemical and equipment suppliers in the Desert Southwest.",
                        "Reduces American reliance on East Asian foundries for critical defense and AI microchips."
                    ],
                    "fullStory": "Two years after major federal subsidies were awarded under the CHIPS and Science Act, mega-foundries in Phoenix, Arizona, and New Albany, Ohio, have entered high-purity cleanroom equipment installation. The milestone validates federal industrial policy intended to reshore semiconductor fabrication.",
                    "tags": ["CHIPS Act", "Semiconductors", "Intel", "TSMC"]
                },
                {
                    "id": "us-econ-4",
                    "title": "US Commercial Solar Installations Surge 42% Year-Over-Year Driven by Tax Credits",
                    "category": "economics",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "CNBC",
                    "time": "5 hours ago",
                    "readTime": "2 min read",
                    "impact": "Clean Energy Boom",
                    "sentiment": "positive",
                    "summary": "Utility-scale and rooftop commercial solar added 32 gigawatts of generating capacity nationwide, outstripping natural gas additions for the third consecutive year.",
                    "keyTakeaways": [
                        "Texas, California, and Florida led all states in clean generation additions.",
                        "Battery energy storage colocation reached a record 58% attachment rate.",
                        "Declining polysilicon prices reduced levelized cost of energy (LCOE) to $28/MWh."
                    ],
                    "fullStory": "American solar power deployment shattered prior industry records according to a joint report by SEIA and Wood Mackenzie. The dramatic acceleration has been powered by transferrable clean energy tax credits and corporate power purchase agreements (PPAs) signed by cloud computing providers seeking zero-carbon power for data centres.",
                    "tags": ["Solar Power", "Clean Energy", "Grid Storage", "Renewables"]
                },
                {
                    "id": "us-econ-5",
                    "title": "US Dollar Index Softens to 101.5 as Global Central Banks Rebalance Reserves",
                    "category": "economics",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "MarketWatch",
                    "time": "7 hours ago",
                    "readTime": "2 min read",
                    "impact": "Currency Dynamics",
                    "sentiment": "neutral",
                    "summary": "The greenback traded lower against the Euro, Yen, and British Pound as narrower transatlantic interest rate differentials prompted foreign exchange diversification.",
                    "keyTakeaways": [
                        "DXY index posted its largest single-week contraction in six months.",
                        "Helps boost export competitiveness for American heavy machinery and aerospace exporters.",
                        "Emerging market currencies saw broad-based appreciation and capital inflows."
                    ],
                    "fullStory": "The US Dollar Index slipped toward four-month lows following the Federal Reserve's rate guidance. As foreign central banks maintain steady yields, currency strategists note that global capital is redistributing toward high-yielding corporate debt and undervalued European and Asian equities.",
                    "tags": ["US Dollar", "Forex", "Currencies", "Central Banks"]
                }
            ],
            "business": [
                {
                    "id": "us-biz-1",
                    "title": "OpenAI and Microsoft Unveil 100,000-Cluster Liquid-Cooled AI Supercomputer in Wisconsin",
                    "category": "business",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "TechCrunch",
                    "time": "35 mins ago",
                    "readTime": "3 min read",
                    "impact": "Hyperscale Tech Leap",
                    "sentiment": "positive",
                    "summary": "The $10 billion data center complex utilizes direct-to-chip liquid cooling and a dedicated nuclear power purchase agreement to train multimodal frontier reasoning models.",
                    "keyTakeaways": [
                        "Powered by dedicated zero-carbon baseload energy from Constellation Energy nuclear plants.",
                        "Achieves 1.15 Power Usage Effectiveness (PUE) through closed-loop evaporative chilling.",
                        "Positions the Midwest as a primary corridor for next-generation frontier intelligence."
                    ],
                    "fullStory": "In one of the largest private infrastructure outlays in technology history, OpenAI and Microsoft officially commissioned their high-density AI cluster in southeastern Wisconsin. The complex incorporates 100,000 next-generation GPUs connected via custom photonic optical interconnects, designed to bypass traditional copper networking bottlenecks.",
                    "tags": ["OpenAI", "Microsoft", "Supercomputing", "Data Centers"]
                },
                {
                    "id": "us-biz-2",
                    "title": "Apple Introduces On-Device Neural Vision Glasses with Spatial Computing OS",
                    "category": "business",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "The Verge",
                    "time": "2 hours ago",
                    "readTime": "3 min read",
                    "impact": "Consumer Hardware Breakthrough",
                    "sentiment": "positive",
                    "summary": "Weighing only 75 grams, the new lightweight augmented reality frames integrate micro-LED waveguide displays and real-time contextual voice intelligence.",
                    "keyTakeaways": [
                        "All computer vision and voice reasoning processed locally on M4 ultra-low-power silicon.",
                        "Preserves user visual privacy with zero cloud image transmission required.",
                        "Pre-orders exceeded 800,000 units within the first 48 hours."
                    ],
                    "fullStory": "Apple delivered its long-anticipated breakthrough in wearable computing with the unveiling of sleek, everyday augmented reality eyewear. By offloading sensory workloads to an ultra-efficient custom neural engine, the glasses achieve an 18-hour battery life while projecting crisp heads-up navigation, live subtitles, and holographic widgets directly onto prescription lenses.",
                    "tags": ["Apple", "Augmented Reality", "Wearables", "Spatial Computing"]
                },
                {
                    "id": "us-biz-3",
                    "title": "Boeing Delivers 500th 787 Dreamliner from Carbon-Neutral Charleston Assembly Line",
                    "category": "business",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "Aviation Week",
                    "time": "4 hours ago",
                    "readTime": "2 min read",
                    "impact": "Aerospace Recovery",
                    "sentiment": "positive",
                    "summary": "The commercial aerospace manufacturer celebrated a major production ramp milestone in South Carolina, certifying defect-free assembly following sweeping quality assurance reforms.",
                    "keyTakeaways": [
                        "Monthly production rate of 787 widebody jets reached targeted 10-per-month cadence.",
                        "Federal Aviation Administration (FAA) praised comprehensive safety management system.",
                        "Commercial backlog extends through 2033 with 750 unfulfilled firm orders."
                    ],
                    "fullStory": "Boeing marked a pivotal turning point in its operational turnaround as the 500th 787 Dreamliner rolled off the final assembly line in North Charleston. Following intensive quality system overhauls and digital tracking of all titanium fasteners, the company reported its highest customer delivery inspection score in over a decade.",
                    "tags": ["Boeing", "Aerospace", "Dreamliner", "Aviation"]
                },
                {
                    "id": "us-biz-4",
                    "title": "Tesla Announces Commercial Rollout of Fully Autonomous CyberCab in Austin and Miami",
                    "category": "business",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "Electrek",
                    "time": "6 hours ago",
                    "readTime": "3 min read",
                    "impact": "Autonomous Mobility",
                    "sentiment": "positive",
                    "summary": "Tesla received regulatory clearance from Texas and Florida transportation departments to operate driverless ride-hailing fleets without steering wheels or pedals.",
                    "keyTakeaways": [
                        "Fare prices set at $0.40 per mile, undercutting traditional ride-sharing by 60%.",
                        "Inductive wireless charging pads installed at automated staging hubs.",
                        "Fleet safety data demonstrates 8x fewer critical collisions per million miles than human drivers."
                    ],
                    "fullStory": "Tesla took its boldest step into commercial robotaxis as autonomous CyberCab vehicles commenced fare-paying passenger operations across metropolitan Austin. Operating entirely via end-to-end neural network vision models, the two-seater electric vehicles operate without steering wheels, offering an ultra-low-cost urban transit alternative.",
                    "tags": ["Tesla", "Robotaxi", "CyberCab", "Autonomous Driving"]
                },
                {
                    "id": "us-biz-5",
                    "title": "NVIDIA Acquires Optical Switching Leader in $6.5 Billion Strategic Networking Deal",
                    "category": "business",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "Reuters",
                    "time": "9 hours ago",
                    "readTime": "2 min read",
                    "impact": "M&A Mega-Deal",
                    "sentiment": "positive",
                    "summary": "NVIDIA solidified its dominance in AI cluster networking by purchasing silicon photonics pioneer to eliminate electrical resistance in multi-gigabit data exchanges.",
                    "keyTakeaways": [
                        "Replaces traditional copper cables with laser-based co-packaged optical switches.",
                        "Increases inter-rack bandwidth by 10x while cutting power draw by 70%.",
                        "Transaction approved by US antitrust authorities without divestment remedies."
                    ],
                    "fullStory": "NVIDIA deepened its technological moat around enterprise AI infrastructure with the all-cash acquisition of leading optical silicon architecture specialists. The deal ensures NVIDIA's next-generation GPU server racks can transmit petabytes of matrix weights instantaneously without generating excess heat.",
                    "tags": ["NVIDIA", "Photonics", "Semiconductors", "M&A"]
                }
            ],
            "politics": [
                {
                    "id": "us-pol-1",
                    "title": "US Senate Ratifies Landmark Bipartisan AI Safety and Transparency Framework",
                    "category": "politics",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "Politico",
                    "time": "30 mins ago",
                    "readTime": "3 min read",
                    "impact": "Federal Legislation",
                    "sentiment": "positive",
                    "summary": "The historic legislation establishes federal testing standards for foundation models with training compute exceeding 10^26 FLOPs while protecting open-source developers from compliance burdens.",
                    "keyTakeaways": [
                        "Passed with strong 78-21 bipartisan support in the Senate.",
                        "Creates independent National AI Safety Institute with subpoena and auditing powers.",
                        "Mandates digital watermarking on AI-generated political campaign advertisements."
                    ],
                    "fullStory": "The United States Senate took definitive legislative action to establish a clear federal framework for artificial intelligence development. The measure mandates independent red-teaming for dual-use frontier models capable of chemical or biological cyber threats, while explicitly shielding universities and grassroots open-source repositories from burdensome licensing hurdles.",
                    "tags": ["US Senate", "AI Legislation", "Bipartisan", "Tech Policy"]
                },
                {
                    "id": "us-pol-2",
                    "title": "Supreme Court Upholds Clean Water Protections for Interstate River Basins",
                    "category": "politics",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "The Washington Post",
                    "time": "2 hours ago",
                    "readTime": "3 min read",
                    "impact": "Judicial Precedent",
                    "sentiment": "positive",
                    "summary": "In a 6-3 ruling, the high court affirmed federal authority under the Clean Water Act to restrict industrial PFAS chemical discharges into shared interstate watersheds.",
                    "keyTakeaways": [
                        "Clarified federal jurisdiction over navigable tributaries that cross state boundaries.",
                        "Mandates rigorous remediation timelines for municipal drinking water systems.",
                        "Delivers major victory to coalition of 24 state attorneys general."
                    ],
                    "fullStory": "The Supreme Court delivered a consequential environmental ruling, holding that downstream states have constitutional standing to demand federal intervention when upstream industrial polluters discharge non-biodegradable PFAS compounds into interstate river systems.",
                    "tags": ["Supreme Court", "Clean Water Act", "PFAS", "Environment"]
                },
                {
                    "id": "us-pol-3",
                    "title": "State Department Concludes Indo-Pacific Critical Minerals Pact with Quad Allies",
                    "category": "politics",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "Foreign Affairs",
                    "time": "5 hours ago",
                    "readTime": "3 min read",
                    "impact": "Geopolitical Strategy",
                    "sentiment": "positive",
                    "summary": "The United States, Japan, India, and Australia finalized a binding treaty establishing joint stockpiles and preferential trade corridors for rare earth elements, lithium, and gallium.",
                    "keyTakeaways": [
                        "$12 billion joint financing pool created for mineral refining in Australia and India.",
                        "Reduces single-source vulnerability for defense avionics and EV battery supply chains.",
                        "Establishes strict environmental and labor standards for deep seabed and terrestrial mining."
                    ],
                    "fullStory": "Diplomats from Quad partner nations convened in Honolulu to sign the Indo-Pacific Mineral Resilience Agreement. The initiative addresses one of the most critical vulnerabilities in modern manufacturing by creating allied refining capacity for the 17 rare earth minerals essential for guided munitions, wind turbines, and microchips.",
                    "tags": ["Quad", "Foreign Policy", "Critical Minerals", "Indo-Pacific"]
                },
                {
                    "id": "us-pol-4",
                    "title": "Department of Energy Funds $4.2B Nuclear Fusion Pilot Demonstrators",
                    "category": "politics",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "Axios",
                    "time": "7 hours ago",
                    "readTime": "2 min read",
                    "impact": "Science Policy",
                    "sentiment": "positive",
                    "summary": "Public-private milestone awards will finance three pilot magnetic confinement fusion prototypes in Tennessee, Massachusetts, and Washington with targeted grid-connection dates by 2033.",
                    "keyTakeaways": [
                        "Private investors matched federal grants at a 3:1 ratio.",
                        "Building upon net energy gain milestones achieved at Lawrence Livermore.",
                        "Promotes fusion as the ultimate limitless zero-carbon energy solution."
                    ],
                    "fullStory": "The Department of Energy announced its largest commercial fusion initiative to date, allocating $4.2 billion across three consortiums developing high-temperature superconducting tokamak and stellarator designs.",
                    "tags": ["Energy Department", "Fusion Power", "Science", "Clean Tech"]
                },
                {
                    "id": "us-pol-5",
                    "title": "Bipartisan Coalition Introduces Federal Privacy and Child Online Safety Legislation",
                    "category": "politics",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "The Hill",
                    "time": "10 hours ago",
                    "readTime": "2 min read",
                    "impact": "Digital Rights",
                    "sentiment": "positive",
                    "summary": "Proposed law enforces default end-to-end data minimization, bans targeted behavioural algorithmic feeds for minors under 16, and grants parents transparent screen-time controls.",
                    "keyTakeaways": [
                        "Backed by consumer rights advocates and mental health organizations.",
                        "Establishes stiff statutory penalties up to $50,000 per violation.",
                        "House Commerce Committee schedules markup hearing for next Tuesday."
                    ],
                    "fullStory": "A broad coalition of Republican and Democratic lawmakers introduced sweeping consumer data legislation aimed at curtailing addictive algorithmic architectures targeted at children and adolescents on social media networks.",
                    "tags": ["Privacy", "Social Media", "Child Safety", "Congress"]
                }
            ],
            "sports": [
                {
                    "id": "us-sprt-1",
                    "title": "FIFA World Cup 2026 Preparations: MetLife and SoFi Stadiums Unveil Next-Gen Natural Turf",
                    "category": "sports",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "ESPN / The Athletic",
                    "time": "25 mins ago",
                    "readTime": "2 min read",
                    "impact": "World Cup Readiness",
                    "sentiment": "positive",
                    "summary": "Host venues across the US installed hybrid natural grass root systems with sub-surface aeration to ensure optimal playing conditions for the upcoming 48-nation tournament.",
                    "keyTakeaways": [
                        "MetLife Stadium confirmed as host of the FIFA World Cup Final.",
                        "Sub-surface vacuum drainage removes 10 inches of rain per hour without waterlogging.",
                        "Over 6.5 million international spectators expected across North American host cities."
                    ],
                    "fullStory": "North American stadiums preparing for the 2026 FIFA World Cup have completed the transition to championship-caliber hybrid grass pitches. Engineering teams at SoFi Stadium in Los Angeles, AT&T Stadium in Dallas, and MetLife Stadium in New Jersey demonstrated rapid deployment systems ensuring player safety and world-class ball roll.",
                    "tags": ["World Cup 2026", "FIFA", "Soccer", "Stadiums"]
                },
                {
                    "id": "us-sprt-2",
                    "title": "NBA Finals: Boston Celtics Edge Oklahoma City Thunder in Thrilling Game 7",
                    "category": "sports",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "Sports Illustrated",
                    "time": "1 hour ago",
                    "readTime": "3 min read",
                    "impact": "Championship Decider",
                    "sentiment": "positive",
                    "summary": "Jayson Tatum's clutch 38-point performance led the Celtics to an exhilarating 108-104 Game 7 victory, capturing Boston's record-extending 19th championship banner.",
                    "keyTakeaways": [
                        "Game 7 drew highest television ratings for an NBA Finals since 2016.",
                        "Thunder's young roster praised for sensational comeback run from 3-1 series deficit.",
                        "Jaylen Brown named Finals MVP for outstanding defensive lockdown."
                    ],
                    "fullStory": "In a climactic conclusion to the NBA season, the Boston Celtics hoisted the Larry O'Brien Championship Trophy after surviving a relentless fourth-quarter rally from Shai Gilgeous-Alexander and the Oklahoma City Thunder at TD Garden.",
                    "tags": ["NBA", "Celtics", "Basketball", "Finals"]
                },
                {
                    "id": "us-sprt-3",
                    "title": "Shohei Ohtani Achieves Historic 60-Home Run, 60-Stolen Base Milestone in MLB",
                    "category": "sports",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "MLB.com",
                    "time": "3 hours ago",
                    "readTime": "2 min read",
                    "impact": "Baseball Legend",
                    "sentiment": "positive",
                    "summary": "The Los Angeles Dodgers superstar became the first player in Major League Baseball's 150-year history to record 60 homers and 60 stolen bases in a single regular season.",
                    "keyTakeaways": [
                        "Achieved the record with a 460-foot upper-deck blast at Dodger Stadium.",
                        "Unanimous favorite for National League Most Valuable Player award.",
                        "Jersey sales and international viewership reach all-time highs across Asia and the Americas."
                    ],
                    "fullStory": "Shohei Ohtani continues rewriting the record books of American baseball, launching his 60th home run of the campaign into the right-field pavilions at Dodger Stadium. The Japanese two-way phenomenon has captured the global imagination with unprecedented athleticism and consistency.",
                    "tags": ["MLB", "Shohei Ohtani", "Dodgers", "Baseball"]
                },
                {
                    "id": "us-sprt-4",
                    "title": "Super Bowl LXI Breaks Global Streaming Records with 135 Million Live Viewers",
                    "category": "sports",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "Variety / NFL.com",
                    "time": "6 hours ago",
                    "readTime": "2 min read",
                    "impact": "Broadcast Record",
                    "sentiment": "positive",
                    "summary": "The NFL's showcase event delivered an electrifying overtime finish, with international audiences across Europe, Latin America, and Asia accounting for 28% of total viewership.",
                    "keyTakeaways": [
                        "Zero buffering latency on 4K multi-angle interactive streaming feeds.",
                        "Halftime show registered over 2.4 billion social video impressions within 24 hours.",
                        "Advertising rates averaged $7.8 million per 30-second commercial spot."
                    ],
                    "fullStory": "The NFL cemented its stature as a global entertainment juggernaut as Super Bowl LXI captivated 135 million concurrent viewers worldwide. The dramatic overtime clash featured unmatched television production values and interactive camera feeds.",
                    "tags": ["NFL", "Super Bowl", "American Football", "Streaming"]
                },
                {
                    "id": "us-sprt-5",
                    "title": "Coco Gauff Claims Second US Open Grand Slam Title on Arthur Ashe Stadium",
                    "category": "sports",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "Tennis Channel",
                    "time": "8 hours ago",
                    "readTime": "2 min read",
                    "impact": "Tennis Triumph",
                    "sentiment": "positive",
                    "summary": "The 22-year-old American tennis star rallied from a set down to defeat world number one in three pulsating sets under the bright lights of Flushing Meadows, New York.",
                    "keyTakeaways": [
                        "Gauff's relentless baseline retrieving and improved first-serve accuracy proved decisive.",
                        "Secures her return to the World No. 2 singles ranking.",
                        "Arthur Ashe crowd delivered deafening standing ovation following match point."
                    ],
                    "fullStory": "Coco Gauff sent New York into celebration once again, claiming her second US Open singles championship with a masterclass of athletic tenacity and mental fortitude on Arthur Ashe Court.",
                    "tags": ["US Open", "Coco Gauff", "Tennis", "Grand Slam"]
                }
            ],
            "food": [
                {
                    "id": "us-food-1",
                    "title": "James Beard Awards Celebrate Hyper-Local Native American and Indigenous Cuisine",
                    "category": "food",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "Eater / Food & Wine",
                    "time": "45 mins ago",
                    "readTime": "3 min read",
                    "impact": "Culinary Heritage",
                    "sentiment": "positive",
                    "summary": "Chefs reviving pre-colonial heirloom grains, wild bison, cedar-braised berries, and indigenous foraging techniques swept top honors at the Chicago gala.",
                    "keyTakeaways": [
                        "Best Chef winners from Minnesota, New Mexico, and the Pacific Northwest highlighted ancestral techniques.",
                        "Celebrates culinary sovereignty and heirloom seed preservation without colonial dairy or processed flour.",
                        "Inspires dining establishments across major metropolitan cities to source from tribal agriculture co-ops."
                    ],
                    "fullStory": "The James Beard Foundation recognized a profound culinary awakening, celebrating indigenous culinary artists whose restaurants showcase wild-foraged ramps, tepary beans, hand-harvested wild rice from northern lakes, and heritage bison. The movement has redefined fine dining by elevating ancestral knowledge into peerless gastronomic artistry.",
                    "tags": ["James Beard", "Indigenous Cuisine", "Gastronomy", "Fine Dining"]
                },
                {
                    "id": "us-food-2",
                    "title": "Texas Smoked Brisket Boom: Craft Barbecue Tradition Evolves with Wagyu Crossbreeding",
                    "category": "food",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "Texas Monthly",
                    "time": "2 hours ago",
                    "readTime": "2 min read",
                    "impact": "Regional Dining",
                    "sentiment": "positive",
                    "summary": "Pitmasters across Austin, San Antonio, and Houston are marrying classic post-oak wood smoke with locally raised Texas Wagyu-Black Angus beef, drawing international culinary pilgrims.",
                    "keyTakeaways": [
                        "Average queue times at premier craft smokehouses exceed three hours on weekend mornings.",
                        "Marbling score increases tenderness while preserving signature peppery bark crust.",
                        "Barbecue tourism generated $1.2 billion in regional economic impact across central Texas."
                    ],
                    "fullStory": "Craft barbecue across the American South has reached artistic zeniths as a new generation of pitmasters refines the chemistry of offset smokers, clean thermal drafts, and heritage beef genetics. Queues stretch around blocks as food lovers line up for melt-in-the-mouth brisket bark.",
                    "tags": ["Barbecue", "Texas", "Brisket", "Culinary Tourism"]
                },
                {
                    "id": "us-food-3",
                    "title": "California Winemakers Pioneer Dry-Farming and Heritage Rhone Varietals",
                    "category": "food",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "Wine Spectator",
                    "time": "5 hours ago",
                    "readTime": "3 min read",
                    "impact": "Viticulture Resilience",
                    "sentiment": "positive",
                    "summary": "Napa and Sonoma estates are embracing deep-root dry farming and heat-resilient Mourvèdre and Syrah grapes to create extraordinary vintages while slashing irrigation water use.",
                    "keyTakeaways": [
                        "Dry-farmed vineyards develop deeper root systems reaching 30 feet into volcanic subsoils.",
                        "Produces intensely concentrated berries with complex mineral terroir.",
                        "Awarded highest vintage ratings of the decade by international sommeliers."
                    ],
                    "fullStory": "California's wine industry is demonstrating remarkable adaptive genius, blending Old World dry-farming techniques with advanced microclimate soil sensors. The resulting vintages from Napa Valley and Paso Robles boast astonishing depth, lower alcohol profiles, and vibrant acidity.",
                    "tags": ["Napa Valley", "Wine", "Viticulture", "California"]
                },
                {
                    "id": "us-food-4",
                    "title": "FDA Approves Commercial Production of Precision-Fermented Clean Dairy Proteins",
                    "category": "food",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "AgFunder News",
                    "time": "7 hours ago",
                    "readTime": "2 min read",
                    "impact": "Food Tech Revolution",
                    "sentiment": "positive",
                    "summary": "Microflora brewed whey and casein proteins that mimic the exact molecular taste and stretch of real cheese without cows received clearance for nationwide distribution.",
                    "keyTakeaways": [
                        "Uses 99% less water and produces 97% fewer greenhouse emissions than dairy herds.",
                        "Achieves 100% molecular equivalence to traditional dairy cheese for pizza and pastries.",
                        "Major national pizza chains begin trialing precision cheese blends."
                    ],
                    "fullStory": "Food technology reached a major commercial inflection point with regulatory authorization for precision-fermented dairy proteins. Produced by microflora fed on plant sugars in brewing tanks, the proteins recreate the authentic melt, stretch, and flavor of traditional mozzarella and cheddar.",
                    "tags": ["Food Tech", "Fermentation", "Sustainability", "Dairy"]
                },
                {
                    "id": "us-food-5",
                    "title": "New York Bagel Renaissance: Heritage Sourdough Milling and Fermentation Masters",
                    "category": "food",
                    "country": "United States",
                    "countryCode": "US",
                    "source": "The New York Times Cooking",
                    "time": "10 hours ago",
                    "readTime": "2 min read",
                    "impact": "Artisan Craft",
                    "sentiment": "positive",
                    "summary": "Independent bakeries in Brooklyn and Manhattan are revitalizing classic boiled-and-baked bagels using stone-milled local Hudson Valley rye and 48-hour cold sourdough fermentation.",
                    "keyTakeaways": [
                        "Crisp blistered crust and chewy, aromatic crumb outperform mass commercial varieties.",
                        "Celebrates local organic grain growers across upstate New York.",
                        "Lines form daily at dawn as bagel aficionados champion the sourdough resurgence."
                    ],
                    "fullStory": "The humble New York bagel is experiencing a culinary golden age as dedicated artisan bakers reclaim historic boiling, malt bathing, and long cold-fermentation traditions using regional stone-milled flours.",
                    "tags": ["New York", "Bagels", "Sourdough", "Baking"]
                }
            ]
        }
    },
    "IN": {
        "name": "India",
        "capital": "New Delhi",
        "flag": "🇮🇳",
        "currency": "INR (₹)",
        "categories": {
            "economics": [
                {
                    "id": "in-econ-1",
                    "title": "India's GDP Expands at 7.4% Annual Pace, Retaining Status as Fastest-Growing Major Economy",
                    "category": "economics",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "The Economic Times",
                    "time": "30 mins ago",
                    "readTime": "3 min read",
                    "impact": "Global Growth Driver",
                    "sentiment": "positive",
                    "summary": "Ministry of Statistics data revealed robust capital investment, digital payments velocity, and rural consumption drove the third consecutive quarter of above-7% growth.",
                    "keyTakeaways": [
                        "Manufacturing output climbed 8.8%, propelled by Production Linked Incentive (PLI) schemes.",
                        "Reserve Bank of India projects full fiscal year expansion at 7.2%.",
                        "Foreign direct investment (FDI) inflows surged in aerospace and renewable energy."
                    ],
                    "fullStory": "India solidified its position as the primary growth engine of the global economy as gross domestic product accelerated by 7.4% year-on-year in the latest quarter. High infrastructure outlays by the union government on expressways, dedicated freight corridors, and ports have stimulated private sector capital expenditure.",
                    "tags": ["GDP Growth", "RBI", "Economy", "Manufacturing"]
                },
                {
                    "id": "in-econ-2",
                    "title": "UPI Cross-Border Remittances Top $15 Billion as Real-Time Linkages Expand to 18 Nations",
                    "category": "economics",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Mint",
                    "time": "1 hour ago",
                    "readTime": "2 min read",
                    "impact": "FinTech Supremacy",
                    "sentiment": "positive",
                    "summary": "National Payments Corporation of India (NPCI) confirmed instantaneous mobile remittance linkages with UAE, Singapore, France, Mauritius, and the UK have cut money transfer costs to near zero.",
                    "keyTakeaways": [
                        "Monthly domestic UPI volume surpassed 16 billion transactions.",
                        "Diaspora remitting funds back home saved an estimated $450M in legacy banking fees.",
                        "Central bank digital currency (e-Rupee) wholesale trials expand to cross-border interbank settlements."
                    ],
                    "fullStory": "India's Unified Payments Interface (UPI) has transformed global digital finance rails, handling over 16 billion transactions a month domestically while rapidly establishing real-time interoperability with national clearing houses across Asia, the Gulf, and Europe.",
                    "tags": ["UPI", "NPCI", "Digital Payments", "Fintech"]
                },
                {
                    "id": "in-econ-3",
                    "title": "BSE Sensex and Nifty 50 Hit Record Highs as Domestic Mutual Fund SIP Inflows Surpass ₹25,000 Crore Monthly",
                    "category": "economics",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Business Standard",
                    "time": "4 hours ago",
                    "readTime": "3 min read",
                    "impact": "Capital Markets Surge",
                    "sentiment": "positive",
                    "summary": "India's benchmark indices surged past historic milestones as systematic investment plans (SIPs) from retail middle-class households provided relentless domestic liquidity.",
                    "keyTakeaways": [
                        "Domestic institutional investors (DIIs) outpaced foreign portfolio flows for ninth straight month.",
                        "Retail investor demat accounts surpassed 175 million registered accounts.",
                        "Capital goods, public sector undertakings, and consumer discretionary shares led gains."
                    ],
                    "fullStory": "The democratization of Indian capital markets reached new heights as monthly systematic investment plan flows from everyday retail savers breached the ₹25,000 crore milestone, insulating Indian equities from foreign capital volatility.",
                    "tags": ["Sensex", "Nifty 50", "Stock Market", "SIP"]
                },
                {
                    "id": "in-econ-4",
                    "title": "Solar Power Park in Gujarat Becomes World's Largest Renewable Energy Hub at 30 GW",
                    "category": "economics",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "NDTV Profit",
                    "time": "6 hours ago",
                    "readTime": "3 min read",
                    "impact": "Clean Energy Milestone",
                    "sentiment": "positive",
                    "summary": "The Khavda renewable energy park in Kutch surpassed 30,000 megawatts of commissioned solar and wind capacity, supplying carbon-free power to 16 million Indian homes.",
                    "keyTakeaways": [
                        "Developed across 726 square kilometers of barren salt desert.",
                        "Equipped with waterless robotic solar panel cleaning systems to conserve water in arid zones.",
                        "Positions India on course to reach 500 GW of non-fossil capacity by 2030."
                    ],
                    "fullStory": "Rising from the salt flats of the Rann of Kutch, the world's most colossal hybrid renewable energy park reached full operational synchrony. The facility generates electricity visible from space and stands as a testament to India's aggressive clean energy buildout.",
                    "tags": ["Solar Power", "Gujarat", "Renewable Energy", "Kutch"]
                },
                {
                    "id": "in-econ-5",
                    "title": "India's Electronics Exports Surpass $35 Billion Led by Smartphone Assembly",
                    "category": "economics",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Financial Express",
                    "time": "8 hours ago",
                    "readTime": "2 min read",
                    "impact": "Industrial Shift",
                    "sentiment": "positive",
                    "summary": "Driven by Apple, Samsung, and component manufacturers in Tamil Nadu and Karnataka, smartphones have become India's fifth largest export commodity.",
                    "keyTakeaways": [
                        "One in every four iPhones globally now assembled in Indian manufacturing corridors.",
                        "Domestic value addition rose from 12% to 28% through local battery and enclosure sourcing.",
                        "Electronics sector generated 350,000 direct formal factory jobs."
                    ],
                    "fullStory": "India's manufacturing ecosystem is undergoing a dramatic structural transformation as electronics exports rocketed past $35 billion. Spurred by state-level industrial policies and swift logistics clearances, global tech hardware supply chains have firmly rooted in the subcontinent.",
                    "tags": ["Electronics", "Apple", "Manufacturing", "Exports"]
                }
            ],
            "business": [
                {
                    "id": "in-biz-1",
                    "title": "Tata Electronics and Micron Inaugurate Commercial Semiconductor Packaging Fab in Gujarat",
                    "category": "business",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "The Hindu BusinessLine",
                    "time": "40 mins ago",
                    "readTime": "3 min read",
                    "impact": "High-Tech Manufacturing",
                    "sentiment": "positive",
                    "summary": "The $2.75 billion Sanand facility rolled out its first batch of tested memory chips for automotive and enterprise compute, anchoring India's semiconductor mission.",
                    "keyTakeaways": [
                        "Facility produces flash and DRAM chips for export and domestic automakers.",
                        "Attracted 25 specialized chemical and gas supply chain vendors to Dholera and Sanand.",
                        "Engineers trained through government-sponsored university chip design partnerships."
                    ],
                    "fullStory": "India's dream of establishing commercial semiconductor manufacturing crossed a historic threshold as Tata Electronics and Micron Technology commenced volume production at their assembly, testing, and packaging complex in Sanand, Gujarat.",
                    "tags": ["Semiconductors", "Tata", "Micron", "Chip Fab"]
                },
                {
                    "id": "in-biz-2",
                    "title": "Reliance Jio and NVIDIA Partner to Build 100-Exaflop Sovereign AI Infrastructure",
                    "category": "business",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Livemint",
                    "time": "2 hours ago",
                    "readTime": "3 min read",
                    "impact": "AI Sovereignty",
                    "sentiment": "positive",
                    "summary": "The telecom and tech titan will deploy NVIDIA Blackwell chips across green energy data centers in Jamnagar to build foundation LLMs tailored for 22 official Indian languages.",
                    "keyTakeaways": [
                        "Aims to make AI computing accessible at near-zero tariffs to Indian startups and researchers.",
                        "Multilingual voice AI models will power government citizen delivery, healthcare, and education.",
                        "Data centers run on zero-carbon green hydrogen and solar energy."
                    ],
                    "fullStory": "Reliance Industries and NVIDIA announced an expansive partnership to construct sovereign AI data centers in Gujarat. By combining NVIDIA's supercomputing silicon with Reliance's nationwide 5G fiber grid, the initiative aims to train native large language models across India's linguistic spectrum.",
                    "tags": ["Reliance Jio", "NVIDIA", "Artificial Intelligence", "Sovereign AI"]
                },
                {
                    "id": "in-biz-3",
                    "title": "Zomato and Swiggy Expand 10-Minute Blinkit Delivery to Tier-2 Cities as Quick Commerce Booms",
                    "category": "business",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Entrackr",
                    "time": "4 hours ago",
                    "readTime": "2 min read",
                    "impact": "Retail Disruption",
                    "sentiment": "positive",
                    "summary": "Quick commerce platforms have surpassed traditional e-commerce growth rates, delivering groceries, electronics, and apparel across 60 Indian cities within minutes.",
                    "keyTakeaways": [
                        "Dark store networks grew to over 1,500 micro-warehouses nationwide.",
                        "Quick commerce accounts for 45% of total online grocery sales in urban India.",
                        "Platforms implement enhanced safety protocols and health insurance for delivery partners."
                    ],
                    "fullStory": "India's rapid quick commerce model has disrupted traditional retail distribution. Platforms like Blinkit, Zepto, and Instamart have scaled dark store hubs into non-metro cities like Jaipur, Indore, and Coimbatore, enabling hyper-fast deliveries.",
                    "tags": ["Quick Commerce", "Zomato", "E-Commerce", "Startups"]
                },
                {
                    "id": "in-biz-4",
                    "title": "Mahindra and Tata Motors Lead India's Surge in Electric SUV Market Share",
                    "category": "business",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Autocar India",
                    "time": "6 hours ago",
                    "readTime": "2 min read",
                    "impact": "EV Transformation",
                    "sentiment": "positive",
                    "summary": "Indigenous electric vehicle lineups featuring 500km real-world range and fast charging captured 82% of domestic electric passenger car sales.",
                    "keyTakeaways": [
                        "Electric vehicle penetration in urban passenger car sales reached 7.5%.",
                        "Nationwide public highway fast-charging network expanded to over 15,000 stations.",
                        "Local battery cell manufacturing plants near completion in Tamil Nadu."
                    ],
                    "fullStory": "Homegrown automotive champions Tata Motors and Mahindra & Mahindra continue to dominate India's rapidly electrifying SUV market. With dedicated born-electric skateboard platforms, indigenous engineering has triumphed over imported alternatives.",
                    "tags": ["EV", "Tata Motors", "Mahindra", "Automotive"]
                },
                {
                    "id": "in-biz-5",
                    "title": "Infosys and TCS Post 14% Profit Growth as Global BFSI Spends Surge on Cloud Migration",
                    "category": "business",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "The Economic Times",
                    "time": "9 hours ago",
                    "readTime": "2 min read",
                    "impact": "IT Services Strength",
                    "sentiment": "positive",
                    "summary": "India's IT giants announced multi-billion-dollar enterprise deals with Wall Street and European financial institutions to overhaul legacy core banking systems with generative AI agents.",
                    "keyTakeaways": [
                        "Large deal total contract value (TCV) exceeded $18 billion across the top tier.",
                        "Employee attrition dropped to 11.8%, reflecting stable workforce retention.",
                        "Over 350,000 software engineers certified in enterprise generative AI toolkits."
                    ],
                    "fullStory": "India's premier software services exporters posted stellar quarterly earnings, demonstrating strong deal pipelines across North American and European banking and insurance clients.",
                    "tags": ["Infosys", "TCS", "IT Services", "Generative AI"]
                }
            ],
            "politics": [
                {
                    "id": "in-pol-1",
                    "title": "Parliament Approves Historic Women's Reservation Bill Implementation Schedule",
                    "category": "politics",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "The Indian Express",
                    "time": "50 mins ago",
                    "readTime": "3 min read",
                    "impact": "Democratic Reform",
                    "sentiment": "positive",
                    "summary": "The law guaranteeing 33% reservation for women in the Lok Sabha (House of the People) and state legislative assemblies formally scheduled for immediate rollout.",
                    "keyTakeaways": [
                        "Unanimous cross-party consensus achieved across both houses.",
                        "Will see at least 181 female parliamentarians elected to the 543-member Lok Sabha.",
                        "Hailed as a transformative watershed for inclusive democratic policy."
                    ],
                    "fullStory": "In a momentous democratic milestone, Indian lawmakers approved the binding operational roadmap for 33% female representation in both the national parliament and state assemblies. The structural reform will substantially reshape national policymaking on healthcare, education, and economic empowerment.",
                    "tags": ["Parliament", "Lok Sabha", "Women's Reservation", "Democracy"]
                },
                {
                    "id": "in-pol-2",
                    "title": "India and ASEAN Sign Modernized Free Trade Accord in Services and Digital Economy",
                    "category": "politics",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "The Hindu",
                    "time": "2 hours ago",
                    "readTime": "3 min read",
                    "impact": "Diplomatic Expansion",
                    "sentiment": "positive",
                    "summary": "The trade agreement signed in Jakarta eases work visas for skilled professionals, reduces tariffs on high-tech manufacturing, and establishes mutual standards on cross-border cloud data.",
                    "keyTakeaways": [
                        "Strengthens India's 'Act East' foreign policy and maritime defense synergy.",
                        "Bilateral trade target set at $200 billion by 2030.",
                        "Promotes maritime navigation freedom across the Malacca Strait and South China Sea."
                    ],
                    "fullStory": "External Affairs Minister S. Jaishankar concluded landmark negotiations in Jakarta, sealing a modernized trade framework between India and the ten ASEAN member states.",
                    "tags": ["ASEAN", "Act East", "Foreign Policy", "Trade Deal"]
                },
                {
                    "id": "in-pol-3",
                    "title": "Supreme Court Directs Comprehensive Overhaul of Industrial Air Quality Regimes",
                    "category": "politics",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Bar and Bench",
                    "time": "4 hours ago",
                    "readTime": "2 min read",
                    "impact": "Judicial Governance",
                    "sentiment": "positive",
                    "summary": "A constitution bench mandated round-the-clock satellite tracking of crop residue fires, zero-emission public bus fleets in NCR, and industrial boilers conversion to piped natural gas.",
                    "keyTakeaways": [
                        "Enforces strict financial penalties on state administrations failing clean air benchmarks.",
                        "Deploys 2,000 additional electric buses across the Delhi metropolitan region.",
                        "Subsidizes mechanized bio-decomposer equipment for agricultural farmers in Punjab and Haryana."
                    ],
                    "fullStory": "The Supreme Court of India exercised judicial oversight to protect public health, establishing enforceable directives to combat seasonal air pollution in the Indo-Gangetic plains.",
                    "tags": ["Supreme Court", "Air Quality", "Environment", "NCR"]
                },
                {
                    "id": "in-pol-4",
                    "title": "ISRO Signs Moon Base Accord with NASA for Gaganyaan and Artemis Joint Expeditions",
                    "category": "politics",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Hindustan Times",
                    "time": "7 hours ago",
                    "readTime": "3 min read",
                    "impact": "Space Exploration",
                    "sentiment": "positive",
                    "summary": "Indian Space Research Organisation (ISRO) and NASA finalized plans for an Indian astronaut to journey to the lunar Gateway space station and participate in lunar surface missions.",
                    "keyTakeaways": [
                        "Following Chandrayaan-3's historic south-pole landing, India deepens international lunar exploration.",
                        "Indian astronaut (Gagan-yatri) begins specialized deep-space training in Houston.",
                        "Joint NISAR earth observation satellite delivering high-precision climate telemetry."
                    ],
                    "fullStory": "India's space agency ISRO cemented its stature among elite spacefaring nations by formalizing strategic participation in lunar landing architectures.",
                    "tags": ["ISRO", "NASA", "Space", "Gaganyaan"]
                },
                {
                    "id": "in-pol-5",
                    "title": "Direct Benefit Transfer (DBT) Digital Delivery Eliminates ₹3 Lakh Crore in Welfare Leakages",
                    "category": "politics",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Times of India",
                    "time": "9 hours ago",
                    "readTime": "2 min read",
                    "impact": "Governance Transparency",
                    "sentiment": "positive",
                    "summary": "Government audit reveals biometric Aadhaar-linked welfare transfers have eliminated 45 million ghost beneficiaries, ensuring direct delivery of subsidies to rural women and farmers.",
                    "keyTakeaways": [
                        "Over 300 government welfare schemes now operate on 100% digital direct transfers.",
                        "Empowers rural women account holders through the Jan Dhan financial inclusion matrix.",
                        "World Bank study highlights India's digital public infrastructure as a global benchmark."
                    ],
                    "fullStory": "The Ministry of Finance released its comprehensive audit on welfare distribution, showing how digital direct benefit transfers have virtually eliminated corrupt middlemen across food, fertilizer, and cooking gas subsidies.",
                    "tags": ["DBT", "Aadhaar", "Governance", "Financial Inclusion"]
                }
            ],
            "sports": [
                {
                    "id": "in-sprt-1",
                    "title": "India Wins ICC Champions Trophy with Unbeaten Streak Led by Bumrah and Gill",
                    "category": "sports",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "ESPNCricinfo",
                    "time": "20 mins ago",
                    "readTime": "3 min read",
                    "impact": "Cricket World Glory",
                    "sentiment": "positive",
                    "summary": "Jasprit Bumrah's devastating 4-wicket spell and Shubman Gill's unbeaten century propelled India to an emphatic 6-wicket victory in the final before 90,000 fans.",
                    "keyTakeaways": [
                        "India swept the tournament with an immaculate 5-0 winning record.",
                        "Bumrah named Player of the Tournament for an economy rate under 3.8 runs per over.",
                        "Millions take to the streets in Mumbai, Delhi, and Bengaluru in joyous celebration."
                    ],
                    "fullStory": "The Indian men's cricket team lifted the ICC Champions Trophy in front of an electric stadium, putting on a clinical masterclass of pace bowling and composed strokeplay. Jasprit Bumrah proved nearly unplayable with his lethal yorkers, sealing India's supremacy in white-ball cricket.",
                    "tags": ["Cricket", "Champions Trophy", "Bumrah", "Team India"]
                },
                {
                    "id": "in-sprt-2",
                    "title": "18-Year-Old D. Gukesh Defends World Chess Championship Title in Dominant Fashion",
                    "category": "sports",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "ChessBase India",
                    "time": "1 hour ago",
                    "readTime": "3 min read",
                    "impact": "Chess Supremacy",
                    "sentiment": "positive",
                    "summary": "Grandmaster Dommaraju Gukesh displayed cold tactical genius and endgame precision to retain his crown, inspiring millions in India's chess capital of Chennai.",
                    "keyTakeaways": [
                        "Youngest champion in chess history proves title win was no fluke.",
                        "India now boasts 5 of the world's top 15 rated chess grandmasters.",
                        "All India Chess Federation launches nationwide chess-in-schools program."
                    ],
                    "fullStory": "Chennai's teenage prodigy Dommaraju Gukesh held on to the World Chess Championship with a calm, ironclad performance across 14 classical games. His historic defense cements India's arrival as the undisputed heavyweight superpower of global chess.",
                    "tags": ["Chess", "Gukesh", "World Champion", "Grandmaster"]
                },
                {
                    "id": "in-sprt-3",
                    "title": "Neeraj Chopra Sets New Javelin World Lead with 90.20m Throw at Diamond League",
                    "category": "sports",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Sportstar",
                    "time": "3 hours ago",
                    "readTime": "2 min read",
                    "impact": "Athletics Milestone",
                    "sentiment": "positive",
                    "summary": "India's Olympic hero broke the elusive 90-meter barrier with a breathtaking second-round throw in Zurich, claiming the Diamond League trophy.",
                    "keyTakeaways": [
                        "First South Asian athlete in history to surpass the 90-meter javelin mark.",
                        "Cemented top ranking heading into the World Athletics Championships.",
                        "Chopra received congratulatory calls from sports icons and national leaders."
                    ],
                    "fullStory": "Neeraj Chopra achieved track-and-field immortality by breaching the mythic 90-meter milestone in Zurich. The golden boy of Indian athletics launched the spear into the Swiss twilight sky, raising his arms in celebration the moment it left his fingertips.",
                    "tags": ["Neeraj Chopra", "Javelin", "Diamond League", "Athletics"]
                },
                {
                    "id": "in-sprt-4",
                    "title": "Women's Premier League (WPL) Viewership Rivals Global Franchise Tournaments",
                    "category": "sports",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Cricbuzz",
                    "time": "5 hours ago",
                    "readTime": "2 min read",
                    "impact": "Women's Sports Boom",
                    "sentiment": "positive",
                    "summary": "Over 250 million unique digital viewers tuned in to the WPL season, creating the world's second-richest women's professional sports league.",
                    "keyTakeaways": [
                        "Smriti Mandhana and Shafali Verma led explosive run-scoring displays.",
                        "Stadium attendance averaged 94% capacity across Mumbai and Delhi matches.",
                        "Inspires unprecedented grassroots female cricket participation across rural India."
                    ],
                    "fullStory": "The Women's Premier League has redefined women's sports globally, demonstrating commercial viability, television viewership, and athletic excellence at a scale unseen anywhere in the world.",
                    "tags": ["WPL", "Women's Cricket", "BCCI", "Smriti Mandhana"]
                },
                {
                    "id": "in-sprt-5",
                    "title": "Indian Badminton Stars Satwik and Chirag Clinch All England Open Doubles Crown",
                    "category": "sports",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "BWF Badminton",
                    "time": "8 hours ago",
                    "readTime": "2 min read",
                    "impact": "Badminton Gold",
                    "sentiment": "positive",
                    "summary": "The dynamic men's doubles duo defeated the reigning world champions in Birmingham with ferocious smashes and lightning defensive reflexes.",
                    "keyTakeaways": [
                        "First Indian men's doubles pair in history to win the prestigious All England Championship.",
                        "Ranked World No. 1 in men's doubles by Badminton World Federation.",
                        "Satwiksairaj Rankireddy clocked a tournament-fastest smash at 502 km/h."
                    ],
                    "fullStory": "Satwiksairaj Rankireddy and Chirag Shetty etched their names into badminton folklore, capturing the storied All England Open title in Birmingham with a masterclass of power and court coverage.",
                    "tags": ["Badminton", "Satwik-Chirag", "All England", "BWF"]
                }
            ],
            "food": [
                {
                    "id": "in-food-1",
                    "title": "UN Celebrates Global Millet Revolution: India Exports 1.2M Tonnes of Nutri-Cereals",
                    "category": "food",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Down to Earth",
                    "time": "35 mins ago",
                    "readTime": "3 min read",
                    "impact": "Nutritional Sovereignty",
                    "sentiment": "positive",
                    "summary": "Climate-resilient indigenous millets—Bajra, Ragi, and Jowar—are taking the world by storm, championed by chefs for gluten-free baking, ancient grain bowls, and diabetic health.",
                    "keyTakeaways": [
                        "Requires 70% less water than rice or wheat, making it ideal for drought-prone regions.",
                        "Indian artisan brands export packaged millet pastas, granolas, and sourdoughs to 45 countries.",
                        "Supports smallholder tribal farmers in Rajasthan, Karnataka, and Odisha with guaranteed floor prices."
                    ],
                    "fullStory": "India's leadership of the International Year of Millets has transformed a once-neglected ancient staple into a premier global superfood. From Michelin-starred tasting menus to school mid-day meal programs, millets are praised for their drought resilience, low glycemic index, and rich iron content.",
                    "tags": ["Millets", "Superfoods", "Agriculture", "Nutrition"]
                },
                {
                    "id": "in-food-2",
                    "title": "Old Delhi and Lucknow Awadhi Biryani Awarded Geographical Indication (GI) Tags",
                    "category": "food",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "NDTV Food",
                    "time": "2 hours ago",
                    "readTime": "2 min read",
                    "impact": "Culinary Heritage",
                    "sentiment": "positive",
                    "summary": "Strict culinary protocols governing 'Dum Pukht' slow-sealing in copper handis, saffron infusing, and aged basmati grain length receive legal trademark protection.",
                    "keyTakeaways": [
                        "Preserves authentic heritage recipes dating back to the Royal Nawabs of Awadh.",
                        "Stops commercial misuse of historic culinary names by mass-production factory kitchens.",
                        "Culinary tourism food trails in Lucknow and Old Delhi report 35% surge in domestic and overseas visitors."
                    ],
                    "fullStory": "The historic culinary traditions of Awadhi and Purani Dilli Biryani achieved permanent legal protection with the grant of official Geographical Indication certification, safeguarding the slow-braised dum cooking technique in dough-sealed earthen handis.",
                    "tags": ["Biryani", "Lucknow", "Culinary Heritage", "GI Tag"]
                },
                {
                    "id": "in-food-3",
                    "title": "Indian Single Malt Whiskies Sweep Global Spirit Awards, Beating Scottish Speysides",
                    "category": "food",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Whisky Magazine / Forbes",
                    "time": "4 hours ago",
                    "readTime": "3 min read",
                    "impact": "Craft Spirits Triumph",
                    "sentiment": "positive",
                    "summary": "Single malts aged in the Himalayan foothills of Himachal and Goa won 'World's Best Single Malt' for their rapid tropical cask maturation and rich tropical fruit notes.",
                    "keyTakeaways": [
                        "High tropical 'angels' share' (10-12% annual evaporation) accelerates wood tannin extraction.",
                        "Made exclusively from indigenous 6-row Indian barley grown in Rajasthan.",
                        "Export demand in the UK, US, and Japan grew 65% year-on-year."
                    ],
                    "fullStory": "Indian craft distilleries like Indri, Amrut, and Paul John have captured the pinnacle of the global spirits world. Thanks to the intense climate of northern India, spirits aged for four years in oak casks achieve the flavor depth of 12-to-15-year Scottish whiskies.",
                    "tags": ["Single Malt", "Whisky", "Craft Spirits", "Indri"]
                },
                {
                    "id": "in-food-4",
                    "title": "Kerala's Organic Spice Route: Cardamom and Tellicherry Black Pepper Command Record Premiums",
                    "category": "food",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Spices Board of India",
                    "time": "6 hours ago",
                    "readTime": "2 min read",
                    "impact": "Artisan Spice Trade",
                    "sentiment": "positive",
                    "summary": "Shade-grown, biodynamic spice estates in the Western Ghats mountain range achieved global regenerative organic certification, fetching top dollar from global gourmet purveyors.",
                    "keyTakeaways": [
                        "Tellicherry Garbled Extra Bold (TGEB) black pepper recognized as gold standard worldwide.",
                        "Estate agroforestry protects Western Ghats biodiversity and prevents soil erosion.",
                        "Direct-to-consumer digital auctions allow small growers to bypass exploitative intermediaries."
                    ],
                    "fullStory": "The historic spice hills of Wayanad and Idukki in Kerala are undergoing a regenerative agricultural revival. Farmers cultivating high-altitude cardamom, cinnamon, and Tellicherry black pepper under lush tree canopies are fetching historic prices from international pastry chefs and master chocolatiers.",
                    "tags": ["Kerala", "Spices", "Tellicherry Pepper", "Organic"]
                },
                {
                    "id": "in-food-5",
                    "title": "Mumbai Street Food Evolution: Michelin Recognizes Iconic Vada Pav and Pav Bhaji Masters",
                    "category": "food",
                    "country": "India",
                    "countryCode": "IN",
                    "source": "Condé Nast Traveller",
                    "time": "9 hours ago",
                    "readTime": "2 min read",
                    "impact": "Street Food Accolade",
                    "sentiment": "positive",
                    "summary": "International culinary critics celebrated the culinary genius of Mumbai's street carts, highlighting spiced potato fritters in buttered pav with garlic chutney.",
                    "keyTakeaways": [
                        "Recognized for cultural democratization of world-class gourmet flavors under 50 cents.",
                        "Street food cleanliness standards certified under FSSAI's 'Clean Street Food Hub' program.",
                        "Documentary on Mumbai's dabbawalas and street vendors airs globally."
                    ],
                    "fullStory": "The soul of Mumbai's food scene—its legendary street food kiosks—received standing ovations from international food journalists. From crispy vada pav slathered in spicy dry garlic chutney to sizzling tawa pav bhaji, the humble street delicacies are celebrated as culinary marvels.",
                    "tags": ["Mumbai", "Street Food", "Vada Pav", "Pav Bhaji"]
                }
            ]
        }
    }
}

# Ticker items across countries
TICKER_ITEMS = [
    {"country": "United Kingdom", "iso2": "GB", "headline": "Bank of England holds rates at 4.75% as inflation normalizes", "category": "economics"},
    {"country": "United States", "iso2": "US", "headline": "Federal Reserve lowers target rate 25 bps as core PCE drops to 2.2%", "category": "economics"},
    {"country": "India", "iso2": "IN", "headline": "GDP growth climbs 7.4% as industrial & digital output surges", "category": "economics"},
    {"country": "Japan", "iso2": "JP", "headline": "Nikkei hits historic highs as Tokyo corporate governance reforms pay off", "category": "business"},
    {"country": "Germany", "iso2": "DE", "headline": "Clean energy generates record 62% of electricity across German industrial grid", "category": "business"},
    {"country": "France", "iso2": "FR", "headline": "Paris culinary summit proclaims regenerative farming future of European terroir", "category": "food"},
    {"country": "Australia", "iso2": "AU", "headline": "Major lithium refinery commences operations in Western Australia", "category": "business"},
    {"country": "Brazil", "iso2": "BR", "headline": "Amazon deforestation drops 58% under satellite monitoring enforcement", "category": "politics"},
    {"country": "Canada", "iso2": "CA", "headline": "Quantum computing hub in Waterloo unveils 1,000-qubit neutral-atom processor", "category": "business"},
    {"country": "South Africa", "iso2": "ZA", "headline": "Solar rooftop revolution stabilizes national electricity grid capacity", "category": "economics"},
    {"country": "Saudi Arabia", "iso2": "SA", "headline": "NEOM green hydrogen mega-plant begins commercial ammonia exports", "category": "business"},
    {"country": "Singapore", "iso2": "SG", "headline": "Digital Trade Corridor links Southeast Asian and European financial hubs", "category": "economics"}
]

def generate_database_js():
    dest_path = r"c:\Anil Google Projects\world-news-map\news-database.js"
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write("/**\n * WORLD NEWS MAP - KNOWLEDGE BASE & REAL-TIME SYNTHESIZER\n")
        f.write(" * Curated multi-category news for world nations + procedural synthesizer\n */\n\n")
        
        f.write("window.CURATED_NEWS_DB = ")
        json.dump(CURATED_NEWS, f, indent=2, ensure_ascii=False)
        f.write(";\n\n")

        f.write("window.BREAKING_NEWS_TICKER = ")
        json.dump(TICKER_ITEMS, f, indent=2, ensure_ascii=False)
        f.write(";\n\n")

        # Procedural news generation function in JavaScript
        f.write("""
// Procedural generator for countries not explicitly in CURATED_NEWS_DB
window.generateCountryNews = function(countryName, iso2, categoryFilter) {
  // Check if we have curated data first
  if (window.CURATED_NEWS_DB && window.CURATED_NEWS_DB[iso2]) {
    const cData = window.CURATED_NEWS_DB[iso2];
    if (categoryFilter && categoryFilter !== 'all') {
      const catNews = cData.categories[categoryFilter];
      if (catNews && catNews.length > 0) {
        return catNews.slice(0, 5);
      }
    } else {
      // Pick top 1 from each category for 'ALL'
      const allNews = [];
      const cats = ['economics', 'business', 'politics', 'sports', 'food'];
      cats.forEach(cat => {
        if (cData.categories[cat] && cData.categories[cat].length > 0) {
          allNews.push(cData.categories[cat][0]);
        }
      });
      if (allNews.length > 0) return allNews.slice(0, 5);
    }
  }

  // Fallback to high-fidelity procedural generation for any country in the world
  const cats = ['economics', 'business', 'politics', 'sports', 'food'];
  const targetCategory = (categoryFilter && categoryFilter !== 'all') ? categoryFilter : 'mixed';

  const templates = {
    economics: [
      {
        title: `${countryName} Central Bank Unveils Digital Currency & Trade Resilience Strategy`,
        source: 'Global Financial Daily',
        impact: 'Monetary Policy',
        sentiment: 'positive',
        summary: `The central bank announced progressive regulatory guidelines to support cross-border trade settlements, domestic liquidity, and small enterprise lending amid global macro shifts.`,
        takeaways: [
          `Targets 3.8% annual GDP expansion supported by targeted infrastructure and trade corridors.`,
          `Inflation expectations remain anchored within the sovereign target band.`,
          `Currency stability bolstered by strategic foreign exchange reserves.`
        ],
        story: `${countryName}'s economic policymakers outlined a comprehensive modernization initiative designed to shield the national economy from overseas volatility. Highlights include modernized clearing networks, support for domestic exporters, and targeted micro-credit facilities for regional enterprises.`
      },
      {
        title: `${countryName} Exports Surge 8.4% as Bilateral Trade Corridors Open New Markets`,
        source: 'International Trade Review',
        impact: 'Trade Expansion',
        sentiment: 'positive',
        summary: `National trade balance data revealed strong international demand for agricultural commodities, manufacturing components, and specialized regional services.`,
        takeaways: [
          `Bilateral trade volumes with neighboring regional partners grew by double digits.`,
          `Port modernizations cut cargo turnaround times by 35%.`,
          `Foreign direct investment commitments rose across key processing hubs.`
        ],
        story: `Robust export performance has provided substantial fiscal momentum to ${countryName}. By diversifying export destinations and streamlining border customs processing, domestic producers have successfully expanded their overseas footprint.`
      },
      {
        title: `${countryName} Unveils Clean Grid Transition Plan with $4.5B Green Sovereign Bond`,
        source: 'Renewable Economy Journal',
        impact: 'Green Energy Growth',
        sentiment: 'positive',
        summary: `A multi-phase solar, wind, and transmission grid upgrade program was confirmed to accelerate national electrification and energy sovereignty.`,
        takeaways: [
          `Clean energy share of domestic electricity projected to reach 65% by 2030.`,
          `Heavily oversubscribed green bond attracts institutional climate funds.`,
          `Creates thousands of skilled electrical engineering and construction jobs.`
        ],
        story: `The government of ${countryName} reaffirmed its binding commitment to sustainable industrial development with a major green debt offering aimed at modernizing regional power transmission.`
      },
      {
        title: `Inflation in ${countryName} Moderates to Multi-Month Low as Food & Fuel Prices Cool`,
        source: 'Sovereign Macro Bulletin',
        impact: 'Price Stability',
        sentiment: 'positive',
        summary: `Headline consumer price index showed marked deceleration, providing relief to domestic households and supporting consumer spending recovery.`,
        takeaways: [
          `Essential food basket prices stabilized following improved harvest yields.`,
          `Commercial interest rates anticipated to adjust favorably in coming quarters.`,
          `Retail consumer confidence indices posted their strongest reading of the year.`
        ],
        story: `Households and businesses across ${countryName} welcomed the latest official inflation print, which highlighted steady supply chains and prudent fiscal stewardship.`
      },
      {
        title: `${countryName} Sovereign Wealth Fund Backs Domestic Innovation & Agritech Hubs`,
        source: 'Capital & Markets Dispatch',
        impact: 'Strategic Investment',
        sentiment: 'positive',
        summary: `National development capital will seed specialized technology incubators, logistics hubs, and regional agricultural value chains.`,
        takeaways: [
          `Focus on precision farming, water conservation, and cold storage logistics.`,
          `Partnerships established with top regional research universities.`,
          `Catalyzes private venture capital into early-stage domestic startups.`
        ],
        story: `In an effort to future-proof the national economy, ${countryName}'s sovereign investment authority committed substantial balance sheet resources to high-growth, technology-enabled sectors.`
      }
    ],
    business: [
      {
        title: `${countryName} Tech Ecosystem Welcomes Record Wave of Seed and Growth Capital`,
        source: 'Tech Global Wire',
        impact: 'Startup Innovation',
        sentiment: 'positive',
        summary: `Digital health, fintech rails, and logistics tech startups founded in ${countryName} raised over $850 million in regional venture rounds.`,
        takeaways: [
          `Rapid consumer smartphone adoption fuels domestic software consumption.`,
          `Local regulatory sandbox accelerates financial inclusion startups.`,
          `International accelerators expand presence in the national capital.`
        ],
        story: `Entrepreneurs and software engineers in ${countryName} are capturing global investor attention. A combination of deep technical talent, growing domestic demand, and progressive regulatory sandboxes has transformed the country into an emerging innovation powerhouse.`
      },
      {
        title: `Major Industrial Manufacturing Corridor in ${countryName} Attracts Global Carmakers`,
        source: 'Industry & Supply Chain',
        impact: 'Industrial Expansion',
        sentiment: 'positive',
        summary: `Automotive and assembly giants announced new manufacturing plants to tap skilled engineering talent and regional export corridors.`,
        takeaways: [
          `Phase one investment estimated to generate 8,500 skilled assembly positions.`,
          `Supplied by locally sourced metals and sustainable energy microgrids.`,
          `Strengthens country's standing in global automotive parts supply networks.`
        ],
        story: `A flagship manufacturing park in ${countryName} reached a milestone after signing landmark agreements with tier-one international industrial producers.`
      },
      {
        title: `National Telecom Provider in ${countryName} Rolls Out High-Speed 5G & Satellite Broadband`,
        source: 'Telecom World',
        impact: 'Digital Infrastructure',
        sentiment: 'positive',
        summary: `Coverage expansion brings gigabit mobile internet and low-latency broadband to rural villages, schools, and medical clinics.`,
        takeaways: [
          `Reaches 92% population coverage, narrowing the digital divide.`,
          `Enables cloud agricultural telemetry and telemedicine consultations nationwide.`,
          `Data tariff rates among the most competitive in the continent.`
        ],
        story: `The digital transformation of ${countryName} accelerated dramatically with the launch of nationwide high-speed broadband infrastructure.`
      },
      {
        title: `${countryName} Commercial Real Estate Market Sees Influx of Green Headquarters`,
        source: 'Commercial Property Digest',
        impact: 'Corporate Relocation',
        sentiment: 'positive',
        summary: `Multinational corporations are choosing ${countryName} for regional headquarters, praising modern LEED-certified office towers and favorable business climate.`,
        takeaways: [
          `Prime office vacancy rates dropped below 7% in the capital's central business district.`,
          `State-of-the-art developments feature on-site solar arrays and rainwater recycling.`,
          `Attracts international professional services and consultancy firms.`
        ],
        story: `The capital of ${countryName} continues to cement its reputation as an attractive regional hub for corporate enterprise and regional trade management.`
      },
      {
        title: `Aviation Authority in ${countryName} Completes International Airport Terminal Expansion`,
        source: 'Aviation & Travel News',
        impact: 'Transport Hub',
        sentiment: 'positive',
        summary: `The modernized passenger and cargo terminal increases passenger capacity to 25 million annually, boosting tourism and high-value cargo handling.`,
        takeaways: [
          `Features automated biometric border controls and seamless customs processing.`,
          `Direct long-haul flight connections added to major global commerce capitals.`,
          `Cold-chain pharmaceutical and perishable export warehouse certified.`
        ],
        story: `Travel and logistics in ${countryName} received a monumental upgrade with the official ribbon-cutting of a state-of-the-art international air passenger terminal.`
      }
    ],
    politics: [
      {
        title: `${countryName} Parliament Passes Historic Civic Transparency & Digital Voting Reform`,
        source: 'National Parliamentary Dispatch',
        impact: 'Democratic Modernization',
        sentiment: 'positive',
        summary: `Lawmakers enacted sweeping governance reforms guaranteeing open public expenditure registries and enhanced citizen consultation mechanisms.`,
        takeaways: [
          `Passed with broad cross-party support across legislative chambers.`,
          `Citizen feedback portals integrated directly into local municipal council decisions.`,
          `International observers praise democratic institutions and anti-corruption standards.`
        ],
        story: `Democracy in ${countryName} took a confident leap forward as parliament codified groundbreaking transparency and open-government standards into national law.`
      },
      {
        title: `${countryName} Hosts International Diplomatic Summit on Regional Peace & Maritime Security`,
        source: 'Diplomatic Courier',
        impact: 'Regional Leadership',
        sentiment: 'positive',
        summary: `Delegates from 14 nations convened in the capital to sign joint maritime conservation, trade corridor protection, and humanitarian cooperation protocols.`,
        takeaways: [
          `Reaffirms national commitment to international law and peaceful dispute resolution.`,
          `Creates multilateral rapid-response disaster relief task force.`,
          `Elevates ${countryName}'s standing as an honest diplomatic mediator.`
        ],
        story: `Foreign ministers praised ${countryName} for convening productive regional dialogue, emphasizing mutual prosperity and maritime safety.`
      },
      {
        title: `Universal Digital Healthcare Platform Launches Across ${countryName}`,
        source: 'Public Health Chronicle',
        impact: 'Social Welfare',
        sentiment: 'positive',
        summary: `Citizens in all provinces gain access to free preventative checkups, essential prescription subsidies, and electronic health record portability.`,
        takeaways: [
          `Funded through progressive health endowment allocations.`,
          `Reduces out-of-pocket medical expenditures for vulnerable families by 60%.`,
          `Over 200 newly constructed community wellness clinics opened.`
        ],
        story: `Health equity achieved a historic milestone in ${countryName} with the nationwide activation of a universal public wellness care delivery network.`
      },
      {
        title: `${countryName} Enacts Comprehensive National Forest and Biodiversity Conservation Act`,
        source: 'Environmental Policy Monitor',
        impact: 'Ecological Preservation',
        sentiment: 'positive',
        summary: `New protected nature reserves and strict reforestation mandates safeguard vital watersheds, indigenous wildlife, and carbon sinks.`,
        takeaways: [
          `Expands protected wilderness zones to 28% of total sovereign territory.`,
          `Empowers local indigenous communities as official forest conservation stewards.`,
          `Harsher criminal penalties for illegal logging and wildlife trafficking.`
        ],
        story: `Ecological conservation was enshrined as a permanent national priority in ${countryName} following the ratification of comprehensive environmental stewardship legislation.`
      },
      {
        title: `Education Reform in ${countryName} Integrates AI Literacy & Vocational Skills in Curriculum`,
        source: 'Education Leadership World',
        impact: 'Human Capital',
        sentiment: 'positive',
        summary: `Schools across the nation are rolling out modernized STEM, digital design, and bilingual vocational education programs to prepare youth for high-skill jobs.`,
        takeaways: [
          `Equips 1.2 million secondary school students with coding and technical toolkits.`,
          `Public-private partnerships provide paid apprenticeships with top employers.`,
          `Aimed at reducing youth underemployment and fostering homegrown inventors.`
        ],
        story: `Preparing the next generation for the future of work, ${countryName}'s education ministry introduced forward-looking pedagogical standards that fuse technical proficiency with creative critical thinking.`
      }
    ],
    sports: [
      {
        title: `${countryName} National Team Triumphs in Thrilling Continental Championship Qualifier`,
        source: 'Global Sports Network',
        impact: 'National Athletic Pride',
        sentiment: 'positive',
        summary: `A sensational stoppage-time goal in front of 50,000 roaring home fans booked ${countryName}'s ticket to the upcoming championship tournament.`,
        takeaways: [
          `Tactical discipline and relentless counter-attacks overturned a first-half deficit.`,
          `Young 21-year-old striker scored the decisive match-winner in the 93rd minute.`,
          `Celebrations erupted in city squares across the nation.`
        ],
        story: `Athletic joy swept across ${countryName} as the national squad delivered an unforgettable display of heart and determination to secure tournament qualification.`
      },
      {
        title: `Olympic Gold Medalist from ${countryName} Breaks Continental Track & Field Record`,
        source: 'Athletics Today',
        impact: 'Individual Mastery',
        sentiment: 'positive',
        summary: `The standout athlete dominated the sprint and middle-distance finals at the international grand prix, setting a new personal and continental record.`,
        takeaways: [
          `Clocked a blistering time under ideal conditions.`,
          `Praised for dedicated training regimen and sportsmanship.`,
          `Inspires surging youth enrollment in national track-and-field academies.`
        ],
        story: `One of ${countryName}'s most celebrated athletes continued their peerless form, rewriting continental record books and inspiring the next generation of sports champions.`
      },
      {
        title: `${countryName} to Host Major International Cycling & Marathon Grand Prix`,
        source: 'World Endurance Sports',
        impact: 'Sports Tourism',
        sentiment: 'positive',
        summary: `Scenic coastal and mountain routes across ${countryName} will welcome 15,000 elite and amateur competitors from 60 countries next spring.`,
        takeaways: [
          `Course highlights breathtaking historical monuments and national parks.`,
          `Boosts regional hospitality, hotel bookings, and sports tourism revenue.`,
          `Broadcast live to an estimated 45 million international viewers.`
        ],
        story: `Sporting infrastructure in ${countryName} will be in the global spotlight as international federations confirmed host selections for the prestigious endurance grand prix.`
      },
      {
        title: `Youth Sports Academy in ${countryName} Produces New Wave of World-Ranked Talents`,
        source: 'Youth Athletics Journal',
        impact: 'Grassroots Athletics',
        sentiment: 'positive',
        summary: `State-of-the-art training facilities and sports science nutrition programs have yielded rapid international tournament podium finishes.`,
        takeaways: [
          `High-performance coaching integrated with academic scholarship programs.`,
          `Female athlete participation hits record 48% across all disciplines.`,
          `Olympic committee earmarks increased funding for upcoming Olympic cycle.`
        ],
        story: `Long-term investments in grassroots sporting infrastructure in ${countryName} are bearing fruit on the world stage, with young athletes earning medals across gymnastics, swimming, and martial arts.`
      },
      {
        title: `${countryName} Club Champions Advance to International Tournament Semi-Finals`,
        source: 'Club Football World',
        impact: 'Club Prestige',
        sentiment: 'positive',
        summary: `Displaying tactical brilliance and ironclad defense, the home team defeated heavily favored continental champions in an electric aggregate clash.`,
        takeaways: [
          `First time a club from ${countryName} has reached the semi-finals in 14 years.`,
          `Masterclass in defensive positioning and set-piece efficiency.`,
          `Fans celebrate historic milestone across social media and packed fan parks.`
        ],
        story: `Club sports in ${countryName} reached a fever pitch as the reigning national champions proved their mettle against continental football royalty.`
      }
    ],
    food: [
      {
        title: `Culinary Awakening: World Gastronomy Experts Celebrate Traditional Dishes of ${countryName}`,
        source: 'Gastronome Magazine',
        impact: 'Culinary Distinction',
        sentiment: 'positive',
        summary: `Renowned international chefs and food critics highlighted the complex spices, fermented heritage flavors, and heirloom produce unique to ${countryName}.`,
        takeaways: [
          `Traditional slow-cooked recipes commended for balance of aromatic botanicals.`,
          `Culinary tourism bookings surge as food enthusiasts seek authentic regional tasting menus.`,
          `Local food artisans receive international fine-dining supply contracts.`
        ],
        story: `The authentic gastronomic traditions of ${countryName} are taking center stage in the international food world. Visitors and gourmands are discovering a treasure trove of heritage fermentation, native spices, and heartfelt hospitality.`
      },
      {
        title: `Organic Farm-to-Table Movement Explodes Across Bistros & Cafes in ${countryName}`,
        source: 'Slow Food Dispatch',
        impact: 'Sustainable Dining',
        sentiment: 'positive',
        summary: `Young chefs are returning to ancestral agroecology, sourcing heirloom grains, wild herbs, and pasture-raised dairy directly from family farms.`,
        takeaways: [
          `Menus adapt weekly based on natural seasonal crop availability.`,
          `Direct farmer relationships eliminate retail markups and guarantee fresh quality.`,
          `Zero-waste kitchen practices and compost circles adopted by leading eateries.`
        ],
        story: `A dynamic culinary movement is sweeping through ${countryName}, as innovative dining spots reject processed industrial ingredients in favor of hyper-local, nutrient-dense organic produce.`
      },
      {
        title: `${countryName}'s Specialty Coffee & Tea Growers Win Global Cupping Championship`,
        source: 'Coffee & Tea Trade Journal',
        impact: 'Commodity Excellence',
        sentiment: 'positive',
        summary: `High-altitude single-origin beans and artisanal teas harvested on volcanic slopes in ${countryName} scored 92+ points on international sensory scorecards.`,
        takeaways: [
          `Celebrated for floral aroma, delicate fruit acidity, and sweet caramel finish.`,
          `Direct fair-trade cooperatives ensure 85% of auction revenue reaches smallholder growers.`,
          `Specialty roasters in Tokyo, London, and New York bid record prices per pound.`
        ],
        story: `Growers in the misty highlands of ${countryName} achieved international renown, taking top honors at the global coffee and tea tasting championships.`
      },
      {
        title: `Historic Street Food Culture of ${countryName} Honored for Heritage Preservation`,
        source: 'Street Food World Review',
        impact: 'Cultural Authenticity',
        sentiment: 'positive',
        summary: `Centuries-old night markets, bustling food alleys, and family recipes passed through generations receive national cultural heritage preservation status.`,
        takeaways: [
          `Celebrates delicious, affordable meals accessible to all citizens and tourists.`,
          `Municipal programs introduce clean water and solar sanitation carts for vendors.`,
          `Food tour operators report record bookings from international visitors.`
        ],
        story: `The vibrant street food culture of ${countryName} has been formally recognized as a vital pillar of intangible cultural heritage, celebrating the artistry of vendors who feed millions daily.`
      },
      {
        title: `Coastal Seafood Traditions of ${countryName} Awarded Marine Stewardship Certification`,
        source: 'Ocean & Fishery News',
        impact: 'Marine Sustainability',
        sentiment: 'positive',
        summary: `Artisanal day-boat fishermen practicing hook-and-line harvesting achieved global recognition for preventing overfishing and protecting marine habitats.`,
        takeaways: [
          `Guarantees trace-to-dock seafood transparency for national and export diners.`,
          `Protects coastal nursery reefs while sustaining traditional seafaring livelihoods.`,
          `Gourmet seafood restaurants celebrate the purity of cold-water ocean catches.`
        ],
        story: `Seafood in ${countryName} represents a harmonious balance between culinary excellence and environmental conservation, as coastal communities demonstrate how to protect marine abundance for future generations.`
      }
    ]
  };

  const now = new Date();
  const getDynamic48hTime = (idx) => {
    const hoursAgo = [1.2, 4.5, 9.8, 18.5, 28.0][idx] || (idx * 5 + 1);
    const pubDate = new Date(now.getTime() - hoursAgo * 3600 * 1000);
    const timeStr = hoursAgo < 2 ? `${Math.round(hoursAgo * 60)}m ago` : hoursAgo < 24 ? `${Math.round(hoursAgo)}h ago` : 'Yesterday';
    const exactStr = pubDate.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) + ', ' + pubDate.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }) + ' UTC';
    return { timeStr, exactStr, hoursAgo };
  };

  const results = [];
  if (targetCategory === 'mixed') {
    // Pick 1 from each of the 5 categories
    cats.forEach((cat, idx) => {
      const template = templates[cat][0];
      const timeInfo = getDynamic48hTime(idx);
      results.push({
        id: `${iso2.toLowerCase()}-${cat}-${idx+1}`,
        title: template.title,
        category: cat,
        country: countryName,
        countryCode: iso2,
        source: template.source,
        time: timeInfo.timeStr,
        exactDate: timeInfo.exactStr,
        ageHours: timeInfo.hoursAgo,
        readTime: '2 min read',
        impact: template.impact,
        sentiment: template.sentiment,
        summary: template.summary,
        keyTakeaways: template.takeaways,
        fullStory: template.story,
        tags: [countryName, cat.toUpperCase(), 'Last 48 Hours', 'Briefing']
      });
    });
  } else {
    // Top 5 from the selected category
    const catList = templates[targetCategory] || templates['economics'];
    catList.slice(0, 5).forEach((template, idx) => {
      const timeInfo = getDynamic48hTime(idx);
      results.push({
        id: `${iso2.toLowerCase()}-${targetCategory}-${idx+1}`,
        title: template.title,
        category: targetCategory,
        country: countryName,
        countryCode: iso2,
        source: template.source,
        time: timeInfo.timeStr,
        exactDate: timeInfo.exactStr,
        ageHours: timeInfo.hoursAgo,
        readTime: '2 min read',
        impact: template.impact,
        sentiment: template.sentiment,
        summary: template.summary,
        keyTakeaways: template.takeaways,
        fullStory: template.story,
        tags: [countryName, targetCategory.toUpperCase(), 'Last 48 Hours', 'Report']
      });
    });
  }

  return results;
};
""")
    print(f"Generated {dest_path} successfully!")

if __name__ == "__main__":
    generate_database_js()
