// Plain-language definitions for the harder terms in the "My views" questions,
// shown when a visitor hovers over, focuses or taps the underlined term.
//
// Wording stays neutral: where a term is contested, both sides' names for it are
// given, and nothing says which policy is better. `phrases` are matched in the
// question text, case-insensitively and on word boundaries; when two overlap, the
// longer phrase wins.

export const GLOSSARY = [
  // Economy, taxes, business
  { id: 'minimum-wage', phrases: ['minimum wage'], def: 'The lowest hourly pay employers may legally pay most workers. The federal minimum has been $7.25 since 2009; states and cities can set higher ones, and many do.' },
  { id: 'antitrust', phrases: ['antitrust laws'], def: 'Laws that keep markets competitive, for example by blocking mergers that would leave too few competitors, breaking up monopolies, and banning competitors from agreeing to fix prices.' },
  { id: 'monopoly', phrases: ['monopolies'], def: 'A monopoly is a company that controls all or nearly all of a market, so buyers have little choice and the company can largely set prices.' },
  { id: 'concentration', phrases: ['corporate concentration'], def: 'When a few large companies control most of an industry, such as meatpacking, airlines or internet search.' },
  { id: 'tax-incentives', phrases: ['tax incentives'], def: 'Tax breaks (lower rates, credits or deductions) offered to encourage something, such as building a factory or hiring workers in a particular place.' },
  { id: 'infrastructure', phrases: ['infrastructure'], def: 'The physical systems a country runs on: roads, bridges, railways, ports, airports, water pipes, power lines and internet networks.' },
  { id: 'national-debt', phrases: ['national debt'], def: 'The total the federal government owes from borrowing to cover past deficits, the years it spent more than it collected in taxes.' },
  { id: 'tax-credits', phrases: ['tax credits'], def: 'An amount subtracted directly from the tax someone owes. A deduction, by contrast, only lowers the income that gets taxed.' },
  { id: 'labor-protections', phrases: ['labor protections'], def: 'Laws covering workers’ pay, hours, overtime, safety and treatment on the job.' },
  { id: 'unionize', phrases: ['right to unionize'], def: 'Workers’ legal right to form a union and bargain with their employer as a group over pay, benefits and working conditions.' },
  { id: 'tariffs', phrases: ['tariffs'], def: 'Taxes on imported goods, paid by the importing business when the goods cross the border. Part of the cost is often passed on to buyers through higher prices.' },
  { id: 'family-leave', phrases: ['paid family leave'], def: 'Paid time off work to care for a new child or a seriously ill family member. Federal law guarantees some workers unpaid leave; paid leave depends on the employer or the state.' },
  { id: 'progressive-tax', phrases: ['progressive tax system'], def: 'A tax system where rates rise with income, so higher earners pay a larger share of their income. The federal income tax is progressive; a flat tax charges everyone the same rate.' },
  { id: 'work-week', phrases: ['working hours in a week'], def: 'The standard full-time week in the U.S. is 40 hours, with overtime pay required above that for many workers. Some propose a shorter week, such as 32 hours, at the same pay.' },

  // Healthcare
  { id: 'universal-coverage', phrases: ['universal healthcare coverage'], def: 'A system in which everyone has health insurance, whether through one government plan (single-payer), a mix of public and private plans, or a requirement to have coverage.' },
  { id: 'drug-negotiation', phrases: ['negotiate prescription drug prices'], def: 'Letting the government, through Medicare, bargain with drug makers over what it pays for medicines. The 2022 Inflation Reduction Act started this for a limited list of drugs.' },
  { id: 'public-insurance', phrases: ['public health insurance programs'], def: 'Government health coverage such as Medicare (mainly people 65 and older), Medicaid (people with low incomes) and CHIP (children in lower-income families).' },
  { id: 'private-system', phrases: ['private healthcare system'], def: 'A system where most people get health insurance from private companies, often through an employer, rather than from a government plan.' },
  { id: 'subsidies', phrases: ['subsidies'], def: 'Government payments or tax breaks that lower someone’s costs. In health care, premium tax credits help people who buy their own insurance; for farms, examples include crop insurance and price supports.' },
  { id: 'preexisting', phrases: ['preexisting conditions'], def: 'Health problems someone has before getting insurance, such as diabetes or cancer. Since 2014 the Affordable Care Act has barred insurers from refusing coverage or charging more because of them.' },
  { id: 'preventive-care', phrases: ['preventive care'], def: 'Care meant to prevent illness or catch it early, such as checkups, screenings and vaccines.' },
  { id: 'medicare', phrases: ['Medicare'], def: 'The federal health insurance program for people 65 and older and some younger people with disabilities. Traditional Medicare does not cover most dental, vision or hearing care.' },

  // Education
  { id: 'vocational', phrases: ['vocational'], def: 'Training for a specific trade or career, such as welding, electrical work, nursing or computer repair.' },
  { id: 'apprenticeship', phrases: ['apprenticeship'], def: 'A paid job in which a trainee learns a skilled trade on the job, usually alongside classroom instruction, for one to several years.' },
  { id: 'loan-forgiveness', phrases: ['student loan forgiveness'], def: 'Canceling some or all of what a borrower owes on student loans, so it no longer has to be repaid.' },
  { id: 'school-choice', phrases: ['school choice'], def: 'Policies that let families use public money or public options for a school other than their assigned public school, such as charter schools, vouchers or education savings accounts.' },
  { id: 'charter-schools', phrases: ['charter schools'], def: 'Public schools that are free to attend and paid for with tax money, but run independently of the local school district under a contract (a charter) and with fewer rules.' },
  { id: 'vouchers', phrases: ['school voucher programs'], def: 'Programs that give families public money to pay tuition at private schools, including religious schools.' },
  { id: 'curricula', phrases: ['school curricula'], def: 'What schools teach: the subjects, standards and materials. Local control means school boards and states decide this rather than the federal government.' },
  { id: 'school-meals', phrases: ['free school meals'], def: 'Students from lower-income families can already get free or reduced-price meals through federal programs. Free meals for all students would cover everyone regardless of income, as some states already do.' },
  { id: 'financial-literacy', phrases: ['financial literacy'], def: 'Knowing how to manage money: budgeting, saving, credit, loans and taxes.' },
  { id: 'civics', phrases: ['civics'], def: 'The study of how government works and of citizens’ rights and responsibilities.' },

  // Immigration
  { id: 'border-security', phrases: ['border security'], def: 'Measures to control who and what enters the country: Border Patrol agents, barriers and walls, surveillance technology, and inspections at ports of entry.' },
  { id: 'legal-status', phrases: ['pathway to legal status or citizenship'], def: 'A legal process letting certain immigrants who are in the U.S. without permission, such as people brought here as children, apply to stay lawfully and, in some proposals, eventually become citizens.' },
  { id: 'undocumented', phrases: ['undocumented immigrants'], def: 'People living in the U.S. without legal immigration status, because they entered without permission or stayed after a visa ran out.' },
  { id: 'skilled-workers', phrases: ['skilled workers'], def: 'Visas and green cards for workers with specialized skills or education, such as the H-1B visa for jobs like engineering and software development.' },
  { id: 'immigration-judges', phrases: ['immigration judges'], def: 'Judges in the Justice Department’s immigration courts who decide whether people may stay in the U.S. or must leave, including asylum claims.' },
  { id: 'backlogs', phrases: ['case backlogs'], def: 'The immigration courts have millions of pending cases, so many people wait years for a decision.' },
  { id: 'unauthorized-workers', phrases: ['unauthorized workers'], def: 'People working in the U.S. without legal permission to work.' },
  { id: 'refugees', phrases: ['refugees'], def: 'People who fled their home country because of persecution or war and are screened abroad before being resettled in the U.S. The president sets a yearly limit on how many are admitted.' },
  { id: 'deportation', phrases: ['deportation'], def: 'The government’s removal of a non-citizen from the United States, usually after an order from an immigration judge.' },
  { id: 'enforcement', phrases: ['immigration enforcement'], def: 'Finding, detaining and deporting people who are in the country without legal status. Inside the U.S. this is mainly the job of Immigration and Customs Enforcement (ICE).' },
  { id: 'work-visas', phrases: ['temporary work visas'], def: 'Permits to work in the U.S. for a limited time, such as H-2A visas for seasonal farm work and H-2B visas for other seasonal jobs.' },
  { id: 'e-verify', phrases: ['employment verification'], def: 'Checking that a new hire is allowed to work in the U.S., for example through E-Verify, a federal online system that compares a worker’s documents with government records.' },

  // Crime and safety
  { id: 'body-cameras', phrases: ['body cameras'], def: 'Small cameras worn by police officers that record their encounters with the public.' },
  { id: 'independent-investigations', phrases: ['independent investigations'], def: 'Reviews of alleged police misconduct done by people outside the department involved, such as a state agency, a prosecutor or a civilian review board.' },
  { id: 'rehabilitation', phrases: ['rehabilitation'], def: 'Programs that prepare prisoners to return to society without committing new crimes, such as education, job training, addiction treatment and counseling.' },
  { id: 'cash-bail', phrases: ['cash bail'], def: 'Money a person who has been arrested pays the court to be released before trial, returned if they show up for court. People who can’t pay may stay in jail while awaiting trial.' },
  { id: 'crime-prevention', phrases: ['community-based crime prevention'], def: 'Programs that work with neighborhoods to stop crime before it happens, such as violence interrupters, youth mentoring and job programs, better street lighting and neighborhood watch.' },
  { id: 'alternatives', phrases: ['alternatives to incarceration'], def: 'Ways to hold people accountable without jail or prison, such as drug courts, mental health courts, treatment programs, probation and community service.' },
  { id: 'death-penalty', phrases: ['death penalty'], def: 'Capital punishment: a sentence of execution, used for the most serious crimes such as murder. It is legal under federal law and in about half the states.' },
  { id: 'oversight', phrases: ['federal oversight of local law enforcement'], def: 'When a police department is found to have violated people’s civil rights, the U.S. Justice Department can sue and win a court-enforced agreement (a consent decree) requiring reforms, checked by a monitor.' },

  // Society
  { id: 'discrimination', phrases: ['protections against discrimination'], def: 'Laws that bar unfair treatment in jobs, housing, schools and public places because of traits such as race, sex, religion, disability, age or sexual orientation.' },
  { id: 'abortion-access', phrases: ['legal abortion access'], def: 'Whether and when abortion is legally available. Since the Supreme Court overturned Roe v. Wade in 2022 (the Dobbs decision), each state sets its own rules, from bans with few exceptions to few or no limits.' },
  { id: 'abortion-restrictions', phrases: ['restrictions on abortion'], def: 'Limits such as bans after a set number of weeks, waiting periods, or rules on abortion pills. Since 2022 most of these are set by each state.' },
  { id: 'marijuana', phrases: ['recreational marijuana'], def: 'Marijuana for personal use by adults, not only for medical reasons. It is legal in about half the states but still illegal under federal law.' },
  { id: 'personal-data', phrases: ['personal data'], def: 'Information about people that apps and websites collect, such as location, browsing and purchases. The U.S. has no general federal privacy law, so rules on collecting, selling and deleting it vary by state.' },
  { id: 'end-of-life', phrases: ['end-of-life medical decisions'], def: 'Lets a terminally ill adult with a short time to live get a prescription to end their life, under safeguards like doctors’ approval and waiting periods. Supporters call it medical aid in dying; opponents call it assisted suicide. Legal in about a dozen states.' },
  { id: 'same-sex-marriage', phrases: ['same-sex marriage'], def: 'Marriage between two people of the same sex, legal nationwide since the Supreme Court’s 2015 Obergefell decision. The 2022 Respect for Marriage Act requires federal and state recognition of these marriages.' },
  { id: 'hormone-transitioning', phrases: ['hormone transitioning'], def: 'Medical treatment for transgender minors using puberty blockers or hormones so their bodies develop in line with their gender identity. About half the states restrict or ban it for people under 18.' },
  { id: 'trans-rights', phrases: ['trans rights'], def: 'Laws and policies for transgender people, whose gender identity differs from the sex recorded at birth, covering areas such as discrimination, sports teams, bathrooms, ID documents and health care.' },

  // Energy and environment
  { id: 'renewable', phrases: ['renewable energy'], def: 'Energy from sources that don’t run out, such as sunlight, wind, flowing water (hydropower) and heat from underground (geothermal).' },
  { id: 'nuclear', phrases: ['nuclear power'], def: 'Electricity from power plants that split uranium atoms. The plants release no carbon dioxide while running but leave radioactive waste that must be stored safely.' },
  { id: 'ev-infrastructure', phrases: ['electric vehicle infrastructure'], def: 'Charging stations for electric cars and trucks, and the power-grid upgrades needed to supply them.' },
  { id: 'carbon-limits', phrases: ['carbon emissions limits'], def: 'Caps on how much carbon dioxide, the main gas warming the climate, power plants, factories and other large sources may release, set by regulations or by cap-and-trade programs.' },
  { id: 'passenger-rail', phrases: ['passenger rail'], def: 'Trains that carry people rather than freight, such as Amtrak between cities and commuter lines into big cities.' },
  { id: 'public-transportation', phrases: ['public transportation'], def: 'Buses, subways, light rail and other shared transit open to everyone.' },
  { id: 'energy-manufacturing', phrases: ['domestic energy manufacturing'], def: 'Making energy equipment in the U.S., such as solar panels, wind turbines, batteries and nuclear fuel.' },
  { id: 'lower-emission', phrases: ['lower-emission energy sources'], def: 'Energy that releases less carbon dioxide than coal, oil and gas, such as wind, solar, hydropower and nuclear.' },

  // Defense and foreign policy
  { id: 'alliances', phrases: ['military alliances'], def: 'Treaties in which countries promise to defend each other, such as NATO (the U.S., Canada and 30 European countries) and U.S. defense treaties with Japan and South Korea.' },
  { id: 'war-powers', phrases: ['congressional authorization'], def: 'The Constitution gives Congress the power to declare war. The 1973 War Powers Resolution says troops sent into hostilities must leave within 60 days, plus 30 to withdraw, unless Congress approves. Presidents of both parties have often acted without a vote.' },
  { id: 'military-assistance', phrases: ['military assistance'], def: 'Weapons, equipment, training or money given to another country’s armed forces.' },
  { id: 'diplomacy', phrases: ['diplomacy'], def: 'Handling disputes with other countries through talks, negotiations, treaties and sanctions rather than military force.' },
  { id: 'intervention', phrases: ['intervention'], def: 'Military action in or against another country, such as air strikes or sending troops, as opposed to relying on diplomacy or sanctions alone.' },
  { id: 'presence-overseas', phrases: ['military presence overseas'], def: 'U.S. troops, ships and bases stationed abroad, in places such as Japan, Germany and South Korea, to deter attacks and support allies.' },
  { id: 'cybersecurity', phrases: ['cybersecurity'], def: 'Protecting computers and networks from hacking, theft and sabotage.' },
  { id: 'critical-infrastructure', phrases: ['critical-infrastructure'], def: 'Systems society can’t run without, such as power grids, water treatment, hospitals, banks, pipelines and communications networks.' },
  { id: 'foreign-aid', phrases: ['foreign aid'], def: 'Money, goods and services the U.S. gives other countries, for disaster relief, health programs, economic development and security.' },
  { id: 'hostile-state', phrases: ['hostile state'], def: 'A country whose government works against another country’s interests or security, for example through military aggression, hacking or interfering in elections.' },
  { id: 'eu', phrases: ['European Union'], def: 'A political and economic union of 27 European countries with a shared market, common trade rules and, for most members, a shared currency, the euro.' },

  // Government and elections
  { id: 'term-limits', phrases: ['term limits'], def: 'A cap on how many terms someone may serve in an office. Presidents are limited to two terms; members of Congress have no limit, and adding one would take a constitutional amendment.' },
  { id: 'stock-trading', phrases: ['trading individual stocks'], def: 'Buying and selling shares of particular companies. Supporters of a ban say lawmakers could profit from information they learn on the job; opponents say requiring prompt public reports of every trade is enough.' },
  { id: 'disclosure', phrases: ['campaign finance disclosure'], def: 'Rules requiring campaigns and political groups to report who gives them money and how they spend it.' },
  { id: 'redistricting', phrases: ['congressional district boundaries'], def: 'District lines are redrawn every 10 years after the census. In most states the legislature draws them, which lets the party in power shape districts to its own advantage, called gerrymandering. An independent commission gives the job to a panel of citizens instead of lawmakers.' },
  { id: 'voter-id', phrases: ['voter identification'], def: 'Requiring voters to show identification, such as a driver’s license, before voting. Rules vary by state: some require a photo ID, others accept other documents, and some ask for none.' },
  { id: 'early-voting', phrases: ['early voting'], def: 'Voting in person before Election Day, at set locations and times. How many days are offered varies by state.' },
  { id: 'mail-ballots', phrases: ['mail-in ballots'], def: 'Ballots sent to voters and returned by mail or drop box. Some states mail one to every voter; others require an application or a reason.' },
  { id: 'rcv', phrases: ['ranked-choice voting'], def: 'Voters rank candidates in order of preference. If no one wins a majority of first choices, the last-place candidate is eliminated and those ballots go to each voter’s next choice, repeating until someone has a majority. Maine and Alaska use it for some or all statewide elections.' },
  { id: 'electoral-college', phrases: ['Electoral College'], def: 'How the president is chosen: each state gets electors equal to its senators plus representatives, 538 in all, and a candidate needs 270. Most states give all their electors to the statewide winner, so a candidate can win while losing the national popular vote.' },
  { id: 'ballot-initiatives', phrases: ['ballot initiatives'], def: 'A process letting citizens put a proposed law or constitutional amendment on the ballot by gathering enough voter signatures. About half the states allow it.' },
  { id: 'corporate-donations', phrases: ['corporate political donations', 'finance campaigns'], def: 'Corporations can’t give money directly to federal candidates, but since the Supreme Court’s 2010 Citizens United decision they may spend unlimited sums on political ads through independent groups such as super PACs.' },

  // Housing and infrastructure
  { id: 'affordable-housing', phrases: ['affordable housing'], def: 'Housing that costs a household no more than about 30% of its income. Government programs such as the Low-Income Housing Tax Credit help build homes with limited rents.' },
  { id: 'corporate-housing', phrases: ['corporate investment into housing'], def: 'Large investment firms buying many single-family homes, usually to rent them out.' },
  { id: 'zoning', phrases: ['zoning reforms'], def: 'Zoning is the local rules on what may be built where, for example only single-family houses. Reforms allow more homes, such as duplexes, apartments or houses on smaller lots.' },
  { id: 'eviction', phrases: ['unfair eviction'], def: 'An eviction is the legal removal of a renter from a home. Tenant protections can require a valid reason, advance notice or a right to a lawyer.' },
  { id: 'broadband', phrases: ['broadband'], def: 'High-speed internet service. Many rural areas lack it because running cable to far-apart homes is expensive.' },
  { id: 'ppp', phrases: ['public-private partnerships'], def: 'Deals in which government and private companies share the cost, risk and sometimes the revenue, such as tolls, of building and running projects like roads and bridges.' },

  // Agriculture and industry
  { id: 'semiconductors', phrases: ['semiconductor'], def: 'Semiconductors are computer chips, the tiny electronic parts inside phones, cars, appliances and weapons. Most of the most advanced chips are made in Taiwan; the 2022 CHIPS Act pays for new chip factories in the U.S.' },
  { id: 'pharmaceutical', phrases: ['pharmaceutical production'], def: 'Making medicines and their ingredients. Many generic drugs and drug ingredients used in the U.S. come from China and India.' },
  { id: 'supply-chains', phrases: ['supply chains'], def: 'The network of suppliers and steps that turn raw materials into finished products and deliver them.' },
  { id: 'critical-minerals', phrases: ['critical minerals'], def: 'Minerals essential to modern technology and defense whose supply is at risk, such as lithium, cobalt and rare earth elements used in batteries, electronics and weapons. China dominates much of their processing.' },
  { id: 'trade-agreements', phrases: ['trade agreements'], def: 'Deals between countries to lower tariffs and other trade barriers, such as the USMCA between the U.S., Mexico and Canada.' },
  { id: 'protectionism', phrases: ['protecting domestic industries'], def: 'Shielding a country’s businesses from foreign competition with tariffs, import limits or subsidies. It can protect jobs in those industries but usually raises prices for buyers.' },
  { id: 'drought-resistant', phrases: ['drought-resistant crop'], def: 'Crop varieties bred or engineered to need less water and survive dry spells.' },

  // State and local
  { id: 'property-tax', phrases: ['property tax relief'], def: 'Lowering the tax homeowners pay on the value of their property, through rate cuts, exemptions or caps on yearly increases. Property taxes mainly fund schools and local services.' },
  { id: 'coastal-restoration', phrases: ['coastal restoration'], def: 'Rebuilding wetlands, barrier islands and shorelines that shield coastal communities from storm surge and erosion.' },
  { id: 'technical-colleges', phrases: ['technical colleges'], def: 'Two-year public colleges that teach job skills such as welding, nursing, auto repair and computer support.' },
  { id: 'tax-exemptions', phrases: ['tax exemptions'], def: 'Breaks that let some businesses, groups or property pay less tax or none, often to attract jobs or support charities.' },
];
