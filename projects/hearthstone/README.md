# Introduction

Ten years ago, I made my last commit to https://github.com/ubante/oven/tree/master/src/main/java/com/ubante/oven/hearthstone

I'd like to answer some HS questions but my java is rusty.  So here we are.

# Cards counts and drop rates
Here are the number of cards in the first expansion of the last three years:

                 total  common  rare  epic  legendary
             WW:  265    106     78    54       27
            FoL:  263    106     76    54       27
            VSC:  245    100     70    50       25

 According to https://hearthstone.fandom.com/wiki/Card_pack_statistics, the
 relevant drop rates are:

 * On average, 5.0% chance to get a Normal Legendary card and guaranteed to
   get one within 40 packs from the previous Normal Legendary card drop.
 * On average, 21.0% chance to get a Normal Epic card and guaranteed to get
   one within 10 packs from the previous Normal Epic card drop.
 * One Legendary card is guaranteed within the first 10 packs of a new
   card expansion.
 * Pity timer for normal legendary: 40 packs
 * Pity timer for normal epic: 10 packs

I can't find reliable drop rates for rare cards so will go with 50% for now.

# Questions

1. How many packs are needed to get all <=epic cards in the first expansion of a new Hearthstone year?
   1. ref https://hearthstone.blizzard.com/en-us/expansions-adventures/
   2. According to [pack_sim.py](https://github.com/ubante/poven/blob/d9c47081988d7294d4fedee5b94a916fcd2c58e6/projects/hearthstone/src/pack_sim.py#L116), it takes 281 packs to get all <=epic cards.  But if you consider the dust from duplicates, you can have a complete collection in 269 packs.
2. Will I ever know it's my birthday?
   1. ref https://www.youtube.com/watch?v=y8OnoxKotPQ
  
# Observations

For the expansion that launched today, I opened 80 packs and got:

| Rarity    | Total Count | Just Goldens |
|-----------|-------------|--------------|
| Legendary | 5   | 1 |
| Epic      | 22  | 1 |
| Rare      | 97  | 3 |
| Common    | 276 | 6 |

I got all the commons, as expected.

