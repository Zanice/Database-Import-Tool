# local imports

# project imports

# external imports

def mine(attributes, data, key, reg_n=5):
	key_attribute = None
	other_attributes = []
	
	# identify the targeted key attribute, returning None if an invalid key attribute was given
	for att in attributes:
		if key == att:
			key_attribute = (att, attributes[att])
		else:
			other_attributes.append((att, attributes[att]))
	if key_attribute is None:
		return None
	
	probabilities = {}
	sample_sizes = {}
	
	key_att_name = key_attribute[0]
	key_att_disc = key_attribute[1]
	
	# calculate probabilities depending on if the key attribute is discrete or not
	if key_att_disc:
		# gather occurrences
		for entry in data:
			entry_key_value = entry[key_att_name]
			
			if entry_key_value is not None:
				ss_key = (key_att_name, (None, None))
				if sample_sizes.get(ss_key, None):
					sample_sizes[ss_key] += 1
				else:
					sample_sizes[ss_key] = 1
				
				prob_key = ((key_att_name, entry_key_value), (None, None))
				if probabilities.get(prob_key, None):
					probabilities[prob_key] += 1
				else:
					probabilities[prob_key] = 1
				
				# gather occurrences for the other attributes, dependent on the key
				for other_att, other_att_disc in other_attributes:
					other_att_value = entry[other_att]
				
					if other_att_value is not None:
						ss_key = (other_att, (key_att_name, entry_key_value))
						if sample_sizes.get(ss_key, None):
							sample_sizes[ss_key] += 1
						else:
							sample_sizes[ss_key] = 1
				
						prob_key = ((other_att, other_att_value), (key_att_name, entry_key_value))
						if probabilities.get(prob_key, None):
							probabilities[prob_key] += 1
						else:
							probabilities[prob_key] = 1
		
		# divide occurences by sample sizes for probability
		for prob in probabilities:
			sample_size = sample_sizes[(prob[0][0], prob[1])]
			probabilities[prob] = float(probabilities[prob]) / sample_size
		
		# transform continuous attributes into regression
		for other_att, other_att_disc in other_attributes:
			if not other_att_disc:
				x_vals = []
				y_vals = []
				
				for att_key, cond_att_key in probabilities:
					att_name = att_key[0]
					att_value = att_key[1]
					cond_att_name = cond_att_key[0]
					cond_att_value = cond_att_key[1]
					
					if att_name == other_att:
						pass
	
	return probabilities, sample_sizes

