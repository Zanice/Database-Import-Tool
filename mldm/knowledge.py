# native imports

# project imports

# external imports

TABLE_QUERY = "select {} from {} {};"

class KnowledgeBase(object):
	def __init__(self, db_session, table, constraints='', attribute_dict={}):
		self.db_session = db_session
		self.table = table
		self.constraints = constraints
		
		self.attributes = {}
		self.discrete_attributes = []
		self.continuous_attributes = []
		
		for key in attribute_dict.keys():
			name = key
			is_discrete = attribute_dict[key]
			
			self.attributes[name] = is_discrete
			if is_discrete:
				self.discrete_attributes.append(name)
			else:
				self.continuous_attributes.append(name)
	
	def is_discrete(self, attribute_name):
		result = self.attributes.get(attribute_name, None)
		if result is None:
			raise Exception
		return result
	
	def add_attribute(self, name, is_discrete):
		self.attributes[name] = is_discrete
		if is_discrete:
			self.discrete_attributes.append(name)
		else:
			self.continuous_attributes.append(name)
	
	def generate_base(self):
		atts = ", ".join(self.attributes)
		query = TABLE_QUERY.format(atts, self.table, self.constraints)
		query_results = self.db_session.execute(query)
		results = []
		for row in query_results:
			entry = {}
			
			for att_num, att in enumerate(self.attributes):
				entry[att] = row[att_num]
			
			results.append(entry)
		
		self.base = results
	
	def __str__(self):
		return "< KnowledgeBase with keys {} >".format(self.attributes)

