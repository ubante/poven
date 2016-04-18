This is from http://fivethirtyeight.com/features/you-have-1-billion-to-win-a-space-race-go/

# Problem definition
You are the CEO of a space transport company in the year 2080, and your chief scientist comes in to
tell you that one of your space probes has detected an alien artifact at the Jupiter Solar 
Lagrangian (L2) point.

You want to be the first to get to it! But you know that the story will leak soon and you only 
have a short time to make critical decisions. With standard technology available to anyone with a 
few billion dollars, a manned rocket can be quickly assembled and arrive at the artifact in 1,600 
days. But with some nonstandard items you can reduce that time and beat the competition. Your 
accountants tell you that they can get you an immediate line of credit of $1 billion.

You can buy:

Big Russian engines. There are only three in the world and the Russians want $400 million for each 
of them. Buying one will reduce the trip time by 200 days. Buying two will allow you to split your 
payload and will save another 100 days.
NASA ion engines. There are only eight of these $140 million large-scale engines in the world. 
Each will consume 5,000 kilograms of xenon during the trip. There are 30,000 kg of xenon available 
worldwide at a price of $2,000/kg, so 5,000 kg costs $10 million. Bottom line: For each $150 
million fully fueled xenon engine you buy, you can take 50 days off of the trip.
Light payloads. For $50 million each, you can send one of four return flight fuel tanks out ahead 
of the mission, using existing technology. Each time you do this, you lighten the main mission and 
reduce the arrival time by 25 days.

What’s your best strategy to get there first?

# Solution
The fastest time is 1175 days.  This is gotten with one big russian engines (saving 200 days), 
three ion engines (saving 150 days) and three return flight fuel tanks (saving 75 days).  

# Explanation
The first russian engine saves a day for each $2M.  Subsequent russian engines save a day for
each $4M.  Each ion engine saves a day for $3M.  Each return flight fuel tanks saves a day for $2M.

If we could buy nothing but return flight fuel tanks, then we could take off 500 days and that
would be optimal.  However, they are limited and the equally efficient first russian engine is
also limited - namely one.