# local imports

# project imports

# external imports

def mine(attributes, data):
	sums = {}
	counts = {}
	averages = {}
	
	for attribute in attributes:
		sums[attribute] = float(0)
		counts[attribute] = 0
	
	for entry in data:
		for attribute in attributes:
			if entry[attribute] is not None:
				sums[attribute] += entry[attribute]
				counts[attribute] += 1
	
	for attribute in attributes:
		averages[attribute] = sums[attribute] / counts[attribute] if counts[attribute] > 0 else None
	
	return averages
