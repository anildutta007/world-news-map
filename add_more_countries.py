#!/usr/bin/env python3
"""
Adds France, China, Australia, Brazil, Canada, South Africa, Saudi Arabia, Italy, Singapore to CURATED_NEWS.
"""

MORE_COUNTRIES = {
    "FR": {
        "name": "France",
        "capital": "Paris",
        "flag": "🇫🇷",
        "currency": "EUR (€)",
        "categories": {
            "economics": [
                {
                    "id": "fr-econ-1",
                    "title": "France's Green Re-industrialization Fund Deploys €12B into Low-Carbon Chemistry and Aerospace",
                    "category": "economics",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Les Échos",
                    "time": "20 mins ago",
                    "readTime": "3 min read",
                    "impact": "Industrial Modernization",
                    "sentiment": "positive",
                    "summary": "The 'France 2030' national investment plan backed low-carbon hydrogen steelmaking in Dunkirk and hybrid electric aviation research in Toulouse.",
                    "keyTakeaways": [
                        "Attracted €15B in matching private corporate co-investment.",
                        "Nuclear-powered industrial electricity tariffs guarantee low energy costs for factories.",
                        "Unemployment rate in manufacturing regions reaches 15-year lows."
                    ],
                    "fullStory": "France accelerated its strategy of low-carbon re-industrialization, mobilizing public and private investment pools into decarbonized heavy manufacturing in northern and southern France.",
                    "tags": ["France 2030", "Re-industrialization", "Decarbonization", "Paris"]
                },
                {
                    "id": "fr-econ-2",
                    "title": "French Nuclear Fleet Operates at 88% Availability Delivering Record Power Exports",
                    "category": "economics",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Le Figaro Économie",
                    "time": "1 hour ago",
                    "readTime": "2 min read",
                    "impact": "Energy Surplus",
                    "sentiment": "positive",
                    "summary": "EDF's 56 nuclear reactors completed scheduled maintenance cycles, exporting massive clean baseload electricity across the English Channel and Rhine.",
                    "keyTakeaways": [
                        "Electricity exports generated €4.8 billion in positive trade balance revenue.",
                        "France maintains the lowest carbon footprint per kilowatt-hour in the G7.",
                        "Construction starts on first next-generation EPR2 reactor in Penly."
                    ],
                    "fullStory": "France solidified its role as Europe's clean electricity exporter as EDF reported record nuclear availability, providing stable, affordable baseload power.",
                    "tags": ["EDF", "Nuclear Energy", "Electricity Exports", "Clean Energy"]
                },
                {
                    "id": "fr-econ-3",
                    "title": "CAC 40 Rebounds Propelled by Aerospace, Energy, and Luxury Resurgence",
                    "category": "economics",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "La Tribune",
                    "time": "4 hours ago",
                    "readTime": "2 min read",
                    "impact": "Stock Market Momentum",
                    "sentiment": "positive",
                    "summary": "The Paris stock index gained 1.4% as strong quarterly order books at Airbus, Schneider Electric, and Safran drove trading volumes.",
                    "keyTakeaways": [
                        "Commercial jetliner delivery backlogs stretch to 2032.",
                        "Energy automation and smart electrical distribution margins expand.",
                        "International investors maintain overweight rating on French blue chips."
                    ],
                    "fullStory": "The Paris Bourse posted solid gains, demonstrating the resilience of French industrial engineering and aerospace technology leaders in international markets.",
                    "tags": ["CAC 40", "Airbus", "Stock Market", "Paris Bourse"]
                },
                {
                    "id": "fr-econ-4",
                    "title": "Station F Tech Campus Reaches 1,000 Active Startups in AI and Climate Hardware",
                    "category": "economics",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "French Tech / Maddyness",
                    "time": "6 hours ago",
                    "readTime": "2 min read",
                    "impact": "Startup Ecosystem",
                    "sentiment": "positive",
                    "summary": "The Paris startup hub celebrated the graduation of its latest unicorn cohort, specializing in open-weight foundational AI models and robotics.",
                    "keyTakeaways": [
                        "French tech venture fundraising reached €8.2B over the trailing twelve months.",
                        "Paris recognized as a leading European hub for generative AI research talent.",
                        "Government 'Choose France' summit secures €15B in foreign corporate commitments."
                    ],
                    "fullStory": "The French Tech ecosystem continues its meteoric rise, centered around Station F and prestigious mathematics research institutes across Île-de-France.",
                    "tags": ["Station F", "French Tech", "Startups", "AI"]
                },
                {
                    "id": "fr-econ-5",
                    "title": "High-Speed Rail Expansion: Paris-Berlin Direct Nightjet and TGV Routes Open",
                    "category": "economics",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "SNCF / Le Monde",
                    "time": "8 hours ago",
                    "readTime": "2 min read",
                    "impact": "Sustainable Transport",
                    "sentiment": "positive",
                    "summary": "SNCF and Deutsche Bahn inaugurated direct 7-hour daytime TGV service linking Paris Gare de l'Est with Berlin Hauptbahnhof.",
                    "keyTakeaways": [
                        "Cuts passenger carbon emissions by 92% compared to short-haul aviation.",
                        "Over 85% advance seat booking occupancy across inaugural summer schedule.",
                        "Revitalizes overnight sleeper trains across central Europe."
                    ],
                    "fullStory": "Cross-border European rail transport achieved a milestone as high-speed TGV trains commenced regular direct services between the French and German capitals.",
                    "tags": ["TGV", "Railways", "Paris-Berlin", "SNCF"]
                }
            ],
            "business": [
                {
                    "id": "fr-biz-1",
                    "title": "Airbus Delivers Record 800 Commercial Aircraft as A321neo Assembly Lines Accelerate",
                    "category": "business",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Aviation International",
                    "time": "30 mins ago",
                    "readTime": "3 min read",
                    "impact": "Aviation Supremacy",
                    "sentiment": "positive",
                    "summary": "Assembly sites in Toulouse and Hamburg achieved targeted monthly production cadences, driven by unprecedented global demand for fuel-efficient single-aisle jets.",
                    "keyTakeaways": [
                        "A321XLR extended-range variant successfully enters transcontinental commercial service.",
                        "Order backlog stands at over 8,600 aircraft, securing ten years of manufacturing.",
                        "Over 5,000 new apprentices and aerospace engineers hired across France."
                    ],
                    "fullStory": "Airbus marked an exceptional industrial achievement, ramping up production across its European final assembly lines while maintaining stringent quality control standards.",
                    "tags": ["Airbus", "Aviation", "Toulouse", "A321neo"]
                },
                {
                    "id": "fr-biz-2",
                    "title": "LVMH and Kering Pioneer Regenerative Agriculture Cotton and Silk Supply Chains",
                    "category": "business",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Vogue Business France",
                    "time": "2 hours ago",
                    "readTime": "2 min read",
                    "impact": "Luxury Sustainability",
                    "sentiment": "positive",
                    "summary": "French luxury houses invested €200 million into certified soil restoration and chemical-free heritage fiber farming across the Mediterranean basin.",
                    "keyTakeaways": [
                        "Sets new global environmental standard for luxury haute couture and leather goods.",
                        "Protects traditional artisanal spinning and botanical dyeing cooperatives.",
                        "Traceability tags provide buyers full farm-to-boutique provenance data."
                    ],
                    "fullStory": "French luxury giants are transforming the environmental footprint of fashion, investing in regenerative raw material cultivation that restores soil fertility.",
                    "tags": ["LVMH", "Luxury", "Sustainability", "Fashion"]
                },
                {
                    "id": "fr-biz-3",
                    "title": "Mistral AI Unveils Frontier Open-Weight Model Championing European Digital Sovereignty",
                    "category": "business",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "TechCrunch France",
                    "time": "4 hours ago",
                    "readTime": "3 min read",
                    "impact": "AI Sovereignty",
                    "sentiment": "positive",
                    "summary": "The Paris-based AI champion released its state-of-the-art multilingual model with native reasoning in French, German, Spanish, and Italian.",
                    "keyTakeaways": [
                        "Beats proprietary models on benchmark math and logic evaluation suites.",
                        "Adopted by European healthcare, banking, and government defense agencies.",
                        "Trained on hydro-powered supercomputing clusters in France."
                    ],
                    "fullStory": "Mistral AI continued to lead Europe's technological vanguard, releasing next-generation foundation models that offer enterprises transparent, customizable AI without foreign cloud lock-in.",
                    "tags": ["Mistral AI", "Artificial Intelligence", "Paris", "Open Source"]
                },
                {
                    "id": "fr-biz-4",
                    "title": "Schneider Electric Reaches €38B Revenue Driven by Microgrid and Smart Building Automation",
                    "category": "business",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "L'Usine Nouvelle",
                    "time": "6 hours ago",
                    "readTime": "2 min read",
                    "impact": "Energy Management",
                    "sentiment": "positive",
                    "summary": "The energy management and digital automation giant posted record profits as data centers and commercial buildings upgrade to energy-saving IoT switchgear.",
                    "keyTakeaways": [
                        "Smart building solutions cut facility power consumption by up to 30%.",
                        "High growth in data center cooling and uninterruptible power systems.",
                        "Ranked among the world's most sustainable corporations."
                    ],
                    "fullStory": "Schneider Electric confirmed its leadership in global energy transition hardware and software, delivering mission-critical infrastructure to hospitals, factories, and hyperscale cloud providers.",
                    "tags": ["Schneider Electric", "Smart Grid", "Energy Efficiency", "IoT"]
                },
                {
                    "id": "fr-biz-5",
                    "title": "Dassault Aviation Secures Landmark 24-Jet Rafale Export Deal with Indo-Pacific Partner",
                    "category": "business",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Air & Cosmos",
                    "time": "9 hours ago",
                    "readTime": "2 min read",
                    "impact": "Defense Export",
                    "sentiment": "positive",
                    "summary": "The French aerospace manufacturer will supply advanced Rafale F4 multi-role fighter aircraft equipped with Meteor beyond-visual-range radar systems.",
                    "keyTakeaways": [
                        "Assembly plants in Mérignac increase production rate to 3 jets per month.",
                        "Secures thousands of specialized avionics engineering jobs in Aquitaine.",
                        "Total Rafale export order book surpasses 300 aircraft."
                    ],
                    "fullStory": "Dassault Aviation celebrated another substantial export contract for the combat-proven Rafale aircraft, underscoring the global appeal of French independent defense technology.",
                    "tags": ["Dassault", "Rafale", "Defense", "Aerospace"]
                }
            ],
            "politics": [
                {
                    "id": "fr-pol-1",
                    "title": "National Assembly Passes Landmark Biodiversity and Coastal Protection Law",
                    "category": "politics",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Le Monde",
                    "time": "35 mins ago",
                    "readTime": "3 min read",
                    "impact": "Environmental Legislation",
                    "sentiment": "positive",
                    "summary": "France expanded protected maritime corridors along the Atlantic coast and Mediterranean, restricting bottom-trawling and preserving underwater seagrass meadows.",
                    "keyTakeaways": [
                        "Protects 33% of French national waters under strict ecological conservation.",
                        "Supports artisanal coastal fishermen with sustainable fishing grants.",
                        "Enforces satellite monitoring on foreign vessels in the Exclusive Economic Zone."
                    ],
                    "fullStory": "France took decisive legislative action to safeguard its marine biodiversity, ratifying protections for Posidonia oceanica seagrass beds—vital natural carbon sinks that shield coastlines from erosion.",
                    "tags": ["National Assembly", "Biodiversity", "Oceans", "Environment"]
                },
                {
                    "id": "fr-pol-2",
                    "title": "France and United Kingdom Launch Joint Maritime Security and Channel Patrol Pact",
                    "category": "politics",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "France 24",
                    "time": "2 hours ago",
                    "readTime": "3 min read",
                    "impact": "Bilateral Cooperation",
                    "sentiment": "positive",
                    "summary": "French and British interior ministers announced enhanced drone surveillance, joint intelligence centers in Cherbourg, and humane border processing systems.",
                    "keyTakeaways": [
                        "Dismantles illicit trafficking rings operating across northern European coastlines.",
                        "Deploys thermal imaging radar and maritime rescue vessels.",
                        "Reinforces bilateral diplomatic trust across the English Channel."
                    ],
                    "fullStory": "French and British leadership reached a comprehensive accord on maritime border security and humanitarian search-and-rescue protocols along the busy Dover-Calais strait.",
                    "tags": ["France-UK", "Maritime", "Border Policy", "Channel"]
                },
                {
                    "id": "fr-pol-3",
                    "title": "Decentralization Reform: French Regions Granted Expanded Economic and Transport Powers",
                    "category": "politics",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Le Parisien",
                    "time": "4 hours ago",
                    "readTime": "2 min read",
                    "impact": "Regional Governance",
                    "sentiment": "positive",
                    "summary": "Regional councils in Brittany, Occitanie, and Grand Est receive autonomy to allocate infrastructure budgets directly to suburban regional trains (SERM).",
                    "keyTakeaways": [
                        "Accelerates construction of metropolitan RER rail systems outside Paris.",
                        "Cuts car dependency for commuters in Lyon, Bordeaux, and Strasbourg.",
                        "Decentralizes administrative decision-making from central ministries."
                    ],
                    "fullStory": "A major decentralization statute was approved, giving French regional administrations greater authority to design and finance regional commuter rail networks tailored to local transit needs.",
                    "tags": ["Decentralization", "Regions", "Transit", "RER"]
                },
                {
                    "id": "fr-pol-4",
                    "title": "Constitutional Council Confirms Protection of Environmental and Future Generations Rights",
                    "category": "politics",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Conseil Constitutionnel / AFP",
                    "time": "7 hours ago",
                    "readTime": "2 min read",
                    "impact": "Constitutional Precedent",
                    "sentiment": "positive",
                    "summary": "The high judicial council affirmed that public policies must not compromise the fundamental environmental well-being of future generations under the Environmental Charter.",
                    "keyTakeaways": [
                        "Sets binding legal standard for upcoming urban development and mining projects.",
                        "Praised by youth environmental organizations as a landmark legal precedent.",
                        "Encourages sustainable, long-term policymaking."
                    ],
                    "fullStory": "France's Constitutional Council established a historic judicial precedent, affirming that statutory provisions of the Environmental Charter impose enforceable obligations on the state to safeguard future generations.",
                    "tags": ["Constitutional Council", "Environment", "Justice", "Future Generations"]
                },
                {
                    "id": "fr-pol-5",
                    "title": "Universal National Service Rollout Reaches 500,000 High School Students",
                    "category": "politics",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Le Figaro",
                    "time": "9 hours ago",
                    "readTime": "2 min read",
                    "impact": "Civic Cohesion",
                    "sentiment": "positive",
                    "summary": "The Service National Universel (SNU) program pairs two-week civic training with community service in environmental protection, civil defense, and healthcare volunteering.",
                    "keyTakeaways": [
                        "Fosters social mixing across diverse socio-economic backgrounds.",
                        "Participants receive certified first-aid and crisis response training.",
                        "High satisfaction scores among participating teenagers and educators."
                    ],
                    "fullStory": "The expansion of France's Universal National Service program reached a milestone, bringing together young citizens from all regions for intensive civic engagement, volunteerism, and social cohesion.",
                    "tags": ["SNU", "Civic Service", "Youth", "Education"]
                }
            ],
            "sports": [
                {
                    "id": "fr-sprt-1",
                    "title": "Tour de France Unveils Spectacular Grand Départ with Climbs of Alpe d'Huez and Mont Ventoux",
                    "category": "sports",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "L'Équipe / ASO",
                    "time": "30 mins ago",
                    "readTime": "2 min read",
                    "impact": "Cycling Spectacle",
                    "sentiment": "positive",
                    "summary": "The 114th edition of the world's most famous bicycle race features 21 punishing stages, concluding with a magnificent sprint along the Champs-Élysées in Paris.",
                    "keyTakeaways": [
                        "Over 12 million roadside spectators expected along the French route.",
                        "Tadej Pogačar and Jonas Vingegaard prepare for titanic mountain battle.",
                        "New gravel mountain pass introduces unpredictable tactical challenges."
                    ],
                    "fullStory": "Organizers unveiled the route for the Tour de France, promising a dramatic three-week epic through the Pyrenees and Alps before the traditional triumphant sprint along the cobblestones of Paris.",
                    "tags": ["Tour de France", "Cycling", "Alps", "Champs-Élysées"]
                },
                {
                    "id": "fr-sprt-2",
                    "title": "Paris Saint-Germain Advances to UEFA Champions League Final in Thriller at Parc des Princes",
                    "category": "sports",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "L'Équipe / UEFA",
                    "time": "1 hour ago",
                    "readTime": "3 min read",
                    "impact": "European Football",
                    "sentiment": "positive",
                    "summary": "Luis Enrique's youthful, disciplined PSG side triumphed 3-1 over their opponents, driven by dazzling academy graduates and suffocating high pressing.",
                    "keyTakeaways": [
                        "Warren Zaïre-Emery and Bradley Barcola deliver match-winning performances.",
                        "Parc des Princes crowd erupts with deafening flares and chants.",
                        "PSG aims to capture their elusive maiden European crown in Munich."
                    ],
                    "fullStory": "Paris Saint-Germain marched into the Champions League final with an exhilarating team performance, demonstrating that their transition toward a cohesive, youthful collective has paid glorious dividends.",
                    "tags": ["PSG", "Champions League", "Football", "Parc des Princes"]
                },
                {
                    "id": "fr-sprt-3",
                    "title": "Roland-Garros: New Night Sessions on Court Philippe-Chatrier Captivate Tennis World",
                    "category": "sports",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Roland-Garros / FFT",
                    "time": "4 hours ago",
                    "readTime": "2 min read",
                    "impact": "Grand Slam Tennis",
                    "sentiment": "positive",
                    "summary": "Electric evening atmospheres under the retractable roof of Philippe-Chatrier saw thrilling five-set clay-court battles stretching past midnight in Paris.",
                    "keyTakeaways": [
                        "Red clay courts praised for consistent bounce and classic sliding rallies.",
                        "French Tennis Federation reports record international television audience.",
                        "Eco-responsible tournament certified with zero single-use plastic cups."
                    ],
                    "fullStory": "The French Open at Roland-Garros delivered drama on the red dirt of Paris, with evening encounters under floodlights capturing the imagination of tennis enthusiasts worldwide.",
                    "tags": ["Roland-Garros", "Tennis", "Clay Court", "French Open"]
                },
                {
                    "id": "fr-sprt-4",
                    "title": "Antoine Dupont Leads French Rugby XV to Dominant Six Nations Grand Slam",
                    "category": "sports",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Midi Olympique",
                    "time": "6 hours ago",
                    "readTime": "2 min read",
                    "impact": "Rugby Masterclass",
                    "sentiment": "positive",
                    "summary": "France completed a flawless Six Nations campaign with a comprehensive victory at the Stade de France, showcasing breathtaking offloads and defensive solidity.",
                    "keyTakeaways": [
                        "Antoine Dupont named Six Nations Player of the Tournament for the third time.",
                        "Stade de France witnessed record rugby decibel levels.",
                        "France solidifies position as World Rugby's number one ranked nation."
                    ],
                    "fullStory": "French rugby celebrated an extraordinary Six Nations triumph as Antoine Dupont orchestrated a rugby masterclass at the Stade de France, capturing the Grand Slam with unmatched swagger.",
                    "tags": ["Rugby", "Six Nations", "Antoine Dupont", "Stade de France"]
                },
                {
                    "id": "fr-sprt-5",
                    "title": "Legacy of Paris 2024: Olympic Venues in Seine-Saint-Denis Open for Public Community Sports",
                    "category": "sports",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Paris.fr / France Info",
                    "time": "8 hours ago",
                    "readTime": "2 min read",
                    "impact": "Olympic Legacy",
                    "sentiment": "positive",
                    "summary": "The Aquatics Centre, climbing walls, and skateparks opened to thousands of local schoolchildren, fulfilling the promise of enduring community athletic infrastructure.",
                    "keyTakeaways": [
                        "Over 10,000 local children learn to swim annually in the Olympic aquatic pools.",
                        "Promotes active lifestyle and youth sports club development.",
                        "Cleaned Seine river remains accessible for public summer open-water swimming."
                    ],
                    "fullStory": "The enduring legacy of the Paris Olympic Games bore fruit in the northern suburbs of Paris as world-class aquatic and athletic facilities opened for local community recreation.",
                    "tags": ["Olympics", "Paris 2024", "Legacy", "Community Sports"]
                }
            ],
            "food": [
                {
                    "id": "fr-food-1",
                    "title": "Michelin Guide France: Regional Terroirs Outshine Paris in New 3-Star Honors",
                    "category": "food",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Michelin Guide France",
                    "time": "30 mins ago",
                    "readTime": "3 min read",
                    "impact": "Gastronomy Excellence",
                    "sentiment": "positive",
                    "summary": "Inspectors crowned destination restaurants in Provence, Burgundy, and the Basque Country with three stars, praising zero-mile seasonal produce and ancient heritage cooking.",
                    "keyTakeaways": [
                        "Celebrates chef-farmers cultivating heirloom vegetables on their own estates.",
                        "Green Michelin Stars awarded to 28 establishments for regenerative waste practices.",
                        "Culinary tourism to rural French provinces surges 22%."
                    ],
                    "fullStory": "The Michelin Guide France ceremony in Tours celebrated the vitality of regional French terroir. The prestigious three-star rating was conferred upon visionary kitchens that highlight estate-grown herbs, foraged mountain botanicals, and close relationships with local artisans.",
                    "tags": ["Michelin Guide", "Gastronomy", "Fine Dining", "Terroir"]
                },
                {
                    "id": "fr-food-2",
                    "title": "Bordeaux Wine Revolution: Eco-Certified Biodynamic Vineyards Hit 50% Milestone",
                    "category": "food",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "La Revue du Vin de France",
                    "time": "2 hours ago",
                    "readTime": "2 min read",
                    "impact": "Organic Viticulture",
                    "sentiment": "positive",
                    "summary": "Historic châteaux in Saint-Émilion and the Médoc have embraced organic farming and cover crops, eliminating synthetic fungicides and producing fresher, vibrant vintages.",
                    "keyTakeaways": [
                        "Half of all Bordeaux vineyard acreage now certified organic or in conversion.",
                        "Lower alcohol levels and balanced acidity celebrated by modern sommeliers.",
                        "Protects bee populations and soil microbiome across the Gironde."
                    ],
                    "fullStory": "Bordeaux's storied wine estates have undertaken an ecological metamorphosis. Winemakers are replacing chemical interventions with sheep grazing, floral corridors, and biodynamic preparations, yielding wines of remarkable aromatic precision.",
                    "tags": ["Bordeaux", "Wine", "Biodynamic", "Viticulture"]
                },
                {
                    "id": "fr-food-3",
                    "title": "Traditional French Baguette Artisan Craft Thrives Across 33,000 Village Boulangeries",
                    "category": "food",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Confédération Nationale de la Boulangerie",
                    "time": "4 hours ago",
                    "readTime": "2 min read",
                    "impact": "Artisanal Heritage",
                    "sentiment": "positive",
                    "summary": "Celebrated under UNESCO protection, village bakers practicing slow sourdough fermentation and stone oven baking experience renewed community appreciation.",
                    "keyTakeaways": [
                        "Only 4 ingredients permitted: wheat flour, water, yeast/sourdough, and salt.",
                        "No additives or chemical shelf-life extenders allowed in traditional baguette de tradition.",
                        "National Grand Prix de la Baguette winner selected to supply the Élysée Palace."
                    ],
                    "fullStory": "The French artisanal baguette remains an emblem of everyday culinary joy. Across the nation, master boulangers wake at 3 a.m. to knead and ferment loaves with golden blistered crusts and pillowy alveolate crumbs.",
                    "tags": ["Baguette", "Boulangerie", "UNESCO", "French Bread"]
                },
                {
                    "id": "fr-food-4",
                    "title": "Normandy and Brittany Cider Renaissance: Craft Poire and Cidre Conquer High-End Dining",
                    "category": "food",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Le Figaro Vin",
                    "time": "6 hours ago",
                    "readTime": "2 min read",
                    "impact": "Artisan Beverages",
                    "sentiment": "positive",
                    "summary": "Naturally sparkling, wild-fermented apple and pear ciders made from heritage heirloom orchard fruit are replacing champagne on Michelin-starred pairing menus.",
                    "keyTakeaways": [
                        "Centuries-old tall orchard trees (haute-tige) provide shelter for owls and pollinators.",
                        "Complex tannins and natural acidity pair exquisitely with oysters and Camembert.",
                        "Export demand in Scandinavia, North America, and Japan rises 35%."
                    ],
                    "fullStory": "The orchards of Normandy and Brittany are basking in a gourmet cider renaissance. Producers cultivating ancient heirloom cider apples are crafting bottle-fermented nectars that rival premier crus in complexity and elegance.",
                    "tags": ["Cider", "Normandy", "Brittany", "Artisan Drinks"]
                },
                {
                    "id": "fr-food-5",
                    "title": "Raw-Milk Comté and Roquefort Cheese Crafts Defend Heritage Microbial Terroirs",
                    "category": "food",
                    "country": "France",
                    "countryCode": "FR",
                    "source": "Fromage & Terroir Magazine",
                    "time": "9 hours ago",
                    "readTime": "2 min read",
                    "impact": "Cheesemaking Tradition",
                    "sentiment": "positive",
                    "summary": "Scientific studies confirm that unpasteurized raw-milk cheeses aged in natural caves host diverse beneficial bacterial microbiomes that enhance immune health and flavor complexity.",
                    "keyTakeaways": [
                        "AOP strict rules require Montbéliarde cows to graze on natural Alpine meadows.",
                        "Cave aging extends up to 36 months, developing crunchy amino-acid crystals.",
                        "Defends rural agrarian livelihoods in the Jura mountains and Massif Central."
                    ],
                    "fullStory": "France's historic artisanal cheesemakers defended their living cultural patrimony as researchers confirmed the nutritional and gastronomic superiority of raw-milk ripening traditions in the mountain caves of Jura and Roquefort-sur-Soulzon.",
                    "tags": ["Comté", "Cheese", "AOP", "Terroir"]
                }
            ]
        }
    }
}

def update_more():
    import generate_news_db
    for code, data in MORE_COUNTRIES.items():
        generate_news_db.CURATED_NEWS[code] = data
    generate_news_db.generate_database_js()
    print(f"Updated news-database.js! Now contains {len(generate_news_db.CURATED_NEWS)} deeply curated countries.")

if __name__ == "__main__":
    update_more()
