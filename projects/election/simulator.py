import random


def get_random():
    return random.random() * 100


def run_simulation(dd):
    # dd is a data dictionary with tuple values:
    # (votes, pro_clinton_percent)

    votes_total = 0
    for state in dd:
        if get_random() < float(dd[state][1]):
            votes_total += int(dd[state][0])

    return votes_total

# Read in data
data_dict = {}
with open("state-data.csv") as f:
    states_data = f.readlines()

for state_data in states_data:
    (state_name, e_votes, pro_clinton) = state_data.rstrip().split(',')
    data_dict[state_name] = (e_votes, pro_clinton)
    # print(data_dict[state_name])
    # print(data_dict[state_name][1])

# Loop through simulation
iterations = 10000
victory_count = 0
histogram_dict = {}
for i in range(0, iterations):
    sim_total_votes = run_simulation(data_dict)
    print("{}: {}".format(i, sim_total_votes)),
    if sim_total_votes > 269:
        print(" VICTORY")
        victory_count += 1
    else:
        print(" LOSS")
    if sim_total_votes in histogram_dict:
        histogram_dict[sim_total_votes] += 1
    else:
        histogram_dict[sim_total_votes] = 1

# Present results
print("\n\n")
print("After {} iterations, {} were victorious with a win percentage of {:4.1f}"
      .format(iterations, victory_count, 100 * victory_count / float(iterations)))

low_count = min(histogram_dict.keys())
high_count = max(histogram_dict.keys())
print("\n\n")
print("The high count is {} and the low count is {}"
      .format(high_count, low_count))
for i in range(low_count, high_count+1):
    if i in histogram_dict:
        if i == 270:
            character = 'W'
        else:
            character = '.'
        print("{}: {}"
              .format(i, character * histogram_dict[i]))
    else:
        print("{}: 0"
              .format(i))


