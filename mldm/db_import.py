# native imports
import string

# project imports

# external imports

DEFAULT_FRAG_LEN = 10000
WHITESPACE_TO_REMOVE = string.whitespace.replace(' ', '')

def import_fragments(fragments, session, entry_function):
	fragments_in_use = fragments
	new_fragments = []
	
	while len(fragments_in_use) > 0:
		fragments_in_use_length = len(fragments_in_use)
		
		for fragment_num, fragment_tuple in enumerate(fragments_in_use):
			fragment_length = fragment_tuple[0]
			fragment = fragment_tuple[1]
			
			print("Attempting import of fragment {} of {} (length={}).".format(fragment_num + 1, fragments_in_use_length, fragment_length))
			
			for entry in fragment:
				entry_function(entry, session)
			
			try:
				session.commit()
				session.flush()
			except:
				session.rollback()
					
				if fragment_length < 2:
					continue
					
				half_length = fragment_length / 2
				
				first_half = (half_length, fragment[:half_length])
				second_half = (fragment_length - half_length, fragment[half_length:])
				
				new_fragments.append(first_half)
				new_fragments.append(second_half)
		
		fragments_in_use = new_fragments

def import_raw_list(raw_entry_list, session, entry_function, init_frag_len=DEFAULT_FRAG_LEN):
	entry_list_len = len(raw_entry_list)
	
	frag_start = 0
	frag_end = 0
	fragments = []
	
	while frag_end < entry_list_len:
		frag_end = min(frag_start + init_frag_len, entry_list_len)
		fragments.append((frag_end - frag_start, raw_entry_list[frag_start:frag_end]))
		
		frag_start = frag_end
	
	

def import_file(file_name, session, entry_function, init_frag_len=DEFAULT_FRAG_LEN):
	raw_entry_list = []
	
	with open(file_name) as file_contents:
		for unclean_line in file_contents:
			line = unclean_line.strip(whitespace_to_remove)
			raw_entry_list.append(line)
	
	return import_raw_list(raw_entry_list, session, entry_function, init_frag_len=init_frag_len)

