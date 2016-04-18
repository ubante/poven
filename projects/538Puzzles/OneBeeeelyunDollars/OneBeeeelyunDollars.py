"""
Minimize the time it takes to get to Jupiter.

...
Using 1 Big Russian engines
 -> Timeline reduced to 1400 days
 -> Remaining budget is 600000 kilo-dollars
We can afford up to 4 Ion engines
...
With 3 Ion engines
 -> Timeline reduced to 1250 days
 -> Remaining budget is 150000 kilo-dollars
We can afford up to 3 Return Flight Fuel Tanks
 -> Timeline reduced to 1175 days
 -> Remaining budget is 0 kilo-dollars
 ---> found new fastest time: 1175 days
...
The fastest time is 1175 days.

"""

initialBudget = 1000000 # in kilo-dollars for readability
initialTimelineDays = 1600
fastestTimeline = initialTimelineDays

for russianEngineCount in [0, 1, 2]:
    print "----------------------------"
    print "Using %d Big Russian engines" % russianEngineCount
    newTimelineDays = initialTimelineDays - (200*russianEngineCount)
    if russianEngineCount == 2:
        newTimelineDays = initialTimelineDays - 200 - 100 # see README
    remainingBudget = initialBudget - (400000*russianEngineCount)
    print " -> Timeline reduced to %d days" % newTimelineDays
    print " -> Remaining budget is %s kilo-dollars" % remainingBudget
    if newTimelineDays < fastestTimeline:
        fastestTimeline = newTimelineDays
        print " ---> found new fastest time: %s days" % fastestTimeline

    maxIonEngineCount = remainingBudget / 150000
    print "We can afford up to %s Ion engines" % maxIonEngineCount
    for ionEngineCount in range(0, maxIonEngineCount+1):
        print "With %s Ion engines" % ionEngineCount
        postIonTimeline = newTimelineDays - (50*ionEngineCount)
        postIonBudget = remainingBudget - (150000*ionEngineCount)
        print " -> Timeline reduced to %d days" % postIonTimeline
        print " -> Remaining budget is %s kilo-dollars" % postIonBudget
        if postIonTimeline < fastestTimeline:
            fastestTimeline = postIonTimeline
            print " ---> found new fastest time: %s days" % fastestTimeline

        maxReturnFlightFuelTanks = postIonBudget / 50000
        print "We can afford up to %s Return Flight Fuel Tanks" % maxReturnFlightFuelTanks

        # There are only 4 Return Flight Fuel Tanks available for purchase
        if maxReturnFlightFuelTanks > 4:
            print "Unfortunately, there are only 4 available for puchase."
            maxReturnFlightFuelTanks = 4

        postFuelTankTimeline = postIonTimeline - (25*maxReturnFlightFuelTanks)
        postFuelTankBudget = postIonBudget - (50000*maxReturnFlightFuelTanks)
        print " -> Timeline reduced to %d days" % postFuelTankTimeline
        print " -> Remaining budget is %s kilo-dollars" % postFuelTankBudget
        if postFuelTankTimeline < fastestTimeline:
            fastestTimeline = postFuelTankTimeline
            print " ---> found new fastest time: %s days" % fastestTimeline

        # for fuelTankCount in range(0, maxReturnFlightFuelTanks):
        #     print "With %s Return Flight Fuel Tanks" % fuelTankCount
        #     postFuelTankTimeline = postIonTimeline - (25*fuelTankCount)
        #     postFuelTankBudget = postIonBudget - (50000*fuelTankCount);
        #     print " -> Timeline reduced to %d days" % postFuelTankTimeline
        #     print " -> Remaining budget is %s kilo-dollars" % postFuelTankBudget

print "\n\nThe fastest time is %s days." % fastestTimeline


