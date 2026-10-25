// Parties, the groups inside them, and who leads them.
//
// Values are short, neutral paraphrases of each organization's own platform or
// statement of principles; every card links to that source so readers can check
// the wording. Leadership was verified against news coverage and official pages
// in October 2026 and changes over time, so every card shows its as-of date.

export const PARTIES_AS_OF = 'October 2026';

export const PARTIES = [
  {
    id: 'dem', name: 'Democratic Party', tone: 'dem',
    site: 'https://democrats.org', source: 'https://democrats.org/where-we-stand/party-platform/', sourceLabel: '2024 Democratic Party Platform',
    blurb: 'One of the two major parties. Holds the minority in both chambers of Congress after the 2024 election.',
    values: [
      'Lower costs for families, including housing, prescription drugs and child care, and expand the Child Tax Credit.',
      'Protect and build on the Affordable Care Act, with Medicare negotiating drug prices and capped insulin costs.',
      'Restore nationwide abortion rights and protect reproductive freedom.',
      'Pass federal voting-rights protections and defend democratic institutions.',
      'Invest in clean energy and climate action while creating jobs.',
      'Support the right to organize and raise wages for workers.',
      'Ask the wealthiest people and large corporations to pay more in taxes, with no tax increases on households under $400,000.',
      'Pair border-security funding with immigration reform that includes a path to citizenship.',
      'Stand with NATO allies and Ukraine.',
    ],
    leaders: [
      ['Chair, Democratic National Committee', 'Ken Martin'],
      ['Senate Minority Leader', 'Chuck Schumer (NY)'],
      ['House Minority Leader', 'Hakeem Jeffries (NY-8)'],
      ['Senate Minority Whip', 'Dick Durbin (IL)'],
      ['House Minority Whip', 'Katherine Clark (MA-5)'],
      ['House Democratic Caucus Chair', 'Pete Aguilar (CA-33)'],
      ['Chair, Democratic Senatorial Campaign Committee', 'Kirsten Gillibrand (NY)'],
      ['Chair, Democratic Congressional Campaign Committee', 'Suzan DelBene (WA-1)'],
    ],
    groups: ['dsa', 'cpc', 'newdem', 'bluedog'],
  },
  {
    id: 'gop', name: 'Republican Party', tone: 'rep',
    site: 'https://gop.com', source: 'https://gop.com/about-our-party/', sourceLabel: '2024 Republican Party Platform',
    blurb: 'One of the two major parties. Holds the White House and majorities in both chambers of Congress after the 2024 election.',
    values: [
      'Secure the border and carry out large-scale deportations of people in the country illegally.',
      'Bring down inflation and expand domestic oil, gas and other energy production.',
      'Cut taxes for workers, including no tax on tips.',
      'Rebuild American manufacturing through trade policy, including tariffs.',
      'Defend the Constitution and Bill of Rights, including free speech, religious liberty and the right to bear arms.',
      'Protect Social Security and Medicare with no cuts and no change to the retirement age.',
      'Strengthen the military and build a nationwide missile-defense shield.',
      'Require voter ID, paper ballots and proof of citizenship to vote.',
      'Expand school choice and parental rights in education.',
      'Limit women’s sports to athletes who were born female.',
      'End electric-vehicle mandates and cut federal regulations.',
    ],
    leaders: [
      ['President of the United States', 'Donald J. Trump'],
      ['Vice President', 'JD Vance'],
      ['Speaker of the House', 'Mike Johnson (LA-4)'],
      ['Senate Majority Leader', 'John Thune (SD)'],
      ['House Majority Leader', 'Steve Scalise (LA-1)'],
      ['Senate Majority Whip', 'John Barrasso (WY)'],
      ['House Majority Whip', 'Tom Emmer (MN-6)'],
      ['Chair, Republican National Committee', 'Joe Gruters'],
      ['Co-chair, Republican National Committee', 'KC Crosbie'],
      ['Chair, National Republican Senatorial Committee', 'Tim Scott (SC)'],
      ['Chair, National Republican Congressional Committee', 'Richard Hudson (NC-9)'],
    ],
    groups: ['hfc', 'rsc'],
  },
  {
    id: 'lib', name: 'Libertarian Party', tone: 'third',
    site: 'https://lp.org', source: 'https://lp.org/platform/', sourceLabel: 'Libertarian Party Platform',
    blurb: 'The largest third party by registration in many states.',
    values: [
      'Maximize individual liberty and keep government as small as possible.',
      'Free markets, lower taxes and fewer regulations.',
      'End the war on drugs and leave personal choices that harm no one else to individuals.',
      'A non-interventionist foreign policy that brings troops home.',
      'Strong protections for privacy, free speech and gun rights, and an end to mass surveillance.',
    ],
    leaders: [['Chair, Libertarian National Committee', 'Evan McMahon (elected May 2026)']],
  },
  {
    id: 'grn', name: 'Green Party', tone: 'third',
    site: 'https://www.gp.org', source: 'https://www.gp.org/ten_key_values', sourceLabel: 'The Ten Key Values',
    blurb: 'An environmentalist party organized around its Ten Key Values.',
    values: [
      'Grassroots democracy and decentralized decision-making.',
      'Social justice, equal opportunity, feminism and respect for diversity.',
      'Ecological wisdom and a future focused on sustainability.',
      'Nonviolence and community-based economics.',
      'Personal and global responsibility.',
    ],
    leaders: [['National co-chairs', 'A rotating steering committee — current members are listed at gp.org']],
  },
  {
    id: 'wfp', name: 'Working Families Party', tone: 'third',
    site: 'https://workingfamilies.org', source: 'https://workingfamilies.org', sourceLabel: 'workingfamilies.org',
    blurb: 'A progressive party that often endorses Democrats and, in fusion-voting states like New York, lists them on its own ballot line.',
    values: [
      'An economy that works for working people rather than the wealthy.',
      'Higher taxes on the rich and large corporations.',
      'Racial justice and a multiracial democracy.',
      'Climate action and good union jobs.',
    ],
    leaders: [['National Director', 'Maurice Mitchell']],
  },
  {
    id: 'con', name: 'Constitution Party', tone: 'third',
    site: 'https://constitutionparty.com', source: 'https://constitutionparty.com', sourceLabel: 'constitutionparty.com',
    blurb: 'A socially conservative party that emphasizes a strict reading of the Constitution.',
    values: [
      'Limit the federal government to the powers listed in the Constitution.',
      'Oppose abortion and defend what it describes as America’s Christian heritage.',
      'Strong protection of gun rights and state sovereignty.',
    ],
    leaders: [],
  },
  {
    id: 'fwd', name: 'Forward Party', tone: 'third',
    site: 'https://www.forwardparty.com', source: 'https://www.forwardparty.com', sourceLabel: 'forwardparty.com',
    blurb: 'A centrist party co-founded by Andrew Yang that focuses on how elections work rather than left-right issues.',
    values: [
      'Open primaries and ranked-choice voting.',
      'Reduce polarization and reward problem-solving across party lines.',
    ],
    leaders: [['Co-founder', 'Andrew Yang']],
  },
];

// Groups that organize within a party (or across both) rather than on the ballot.
export const GROUPS = {
  dsa: {
    name: 'Democratic Socialists of America', side: 'dem',
    site: 'https://www.dsausa.org', source: 'https://www.dsausa.org/about-us/', sourceLabel: 'About DSA',
    blurb: 'A membership organization, not a ballot party. Its members usually run as Democrats.',
    values: [
      'Democratic socialism: working people should democratically run the economy and society to meet human needs rather than private profit.',
      'Medicare for All, a Green New Deal and housing as a human right, including social housing and rent control.',
      'Stronger unions and labor rights.',
      'Abolish ICE and end U.S. military aid to Israel; DSA supports boycott, divestment and sanctions.',
    ],
    leaders: [
      ['National co-chair', 'Megan Romer'],
      ['National co-chair', 'Ashik Siddique'],
      ['Notable member in office', 'Zohran Mamdani, Mayor of New York City'],
      ['Notable member in office', 'Rep. Alexandria Ocasio-Cortez (NY-14)'],
      ['Notable member in office', 'Rep. Rashida Tlaib (MI-12)'],
    ],
  },
  cpc: {
    name: 'Congressional Progressive Caucus', side: 'dem',
    site: 'https://progressives.house.gov', source: 'https://progressives.house.gov', sourceLabel: 'progressives.house.gov',
    blurb: 'The main left-leaning caucus of House Democrats.',
    values: [
      'Medicare for All and lower prescription drug prices.',
      'A higher minimum wage and stronger labor protections.',
      'Higher taxes on the wealthy and large corporations.',
      'Aggressive climate action and limits on corporate power.',
    ],
    leaders: [['Chair', 'Rep. Greg Casar (TX)']],
  },
  newdem: {
    name: 'New Democrat Coalition', side: 'dem',
    site: 'https://newdemocratcoalition.house.gov', source: 'https://newdemocratcoalition.house.gov', sourceLabel: 'newdemocratcoalition.house.gov',
    blurb: 'A large center-left caucus of House Democrats.',
    values: [
      'Pro-growth, pro-innovation economic policy.',
      'Fiscal responsibility and pragmatic, often bipartisan, legislating.',
      'Trade, technology and workforce policy that helps the U.S. compete.',
    ],
    leaders: [],
  },
  bluedog: {
    name: 'Blue Dog Coalition', side: 'dem',
    site: 'https://bluedogs-gluesenkampperez.house.gov', source: 'https://bluedogs-gluesenkampperez.house.gov', sourceLabel: 'Blue Dog Coalition site',
    blurb: 'Fiscally conservative, centrist House Democrats.',
    values: [
      'Balanced budgets and lower deficits.',
      'A strong national defense.',
      'Bipartisan compromise over party-line votes.',
    ],
    leaders: [['Co-chair', 'Rep. Marie Gluesenkamp Perez (WA-3)']],
  },
  hfc: {
    name: 'House Freedom Caucus', side: 'gop',
    site: 'https://harris.house.gov', source: 'https://harris.house.gov/media/press-releases/congressman-andy-harris-re-elected-house-freedom-caucus-chairman', sourceLabel: 'Chair’s announcement',
    blurb: 'The House’s most conservative caucus, known for pressing GOP leaders from the right.',
    values: [
      'Deep cuts to federal spending and a smaller federal government.',
      'Opposition to bills seen as expanding government or adding to the debt.',
      'Conservative positions on immigration and social issues.',
    ],
    leaders: [['Chair', 'Rep. Andy Harris (MD-1), re-elected through 2026']],
  },
  rsc: {
    name: 'Republican Study Committee', side: 'gop',
    site: 'https://rsc-pfluger.house.gov', source: 'https://rsc-pfluger.house.gov', sourceLabel: 'rsc-pfluger.house.gov',
    blurb: 'The largest conservative caucus of House Republicans.',
    values: [
      'Budgets that cut spending and aim to balance.',
      'A broad conservative agenda on taxes, regulation and social policy.',
    ],
    leaders: [['Chair', 'Rep. August Pfluger (TX-11)']],
  },
  psc: {
    name: 'Problem Solvers Caucus', side: 'both',
    site: 'https://problemsolverscaucus.house.gov', source: 'https://problemsolverscaucus.house.gov', sourceLabel: 'problemsolverscaucus.house.gov',
    blurb: 'A bipartisan House caucus split evenly between Democrats and Republicans.',
    values: [
      'Bipartisan deals on spending, infrastructure and government operations.',
      'Members agree to vote together when most of the group backs a proposal.',
    ],
    leaders: [
      ['Co-chair (R)', 'Rep. Brian Fitzpatrick (PA-1)'],
      ['Co-chair (D)', 'Rep. Tom Suozzi (NY-3)'],
    ],
  },
};
