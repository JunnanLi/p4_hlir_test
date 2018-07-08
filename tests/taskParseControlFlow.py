import sys
import collections
from p4_hlir.main import HLIR
from function import *



def parseControlFLow():

	#h = HLIR("./stateful.p4")
	h = HLIR("./l2_switch.p4")
	#h = HLIR("../../tutorials-master/SIGCOMM_2015/flowlet_switching/p4src/simple_router.p4")
	#h = HLIR("../../tutorials-master/SIGCOMM_2015/source_routing/p4src/source_routing.p4")

	h.build()

	print "\n====start"

	# start form p4_ingress_ptr
	for table_node, parser_node_set in h.p4_ingress_ptr.items():
		#sys.exit(0)
		
		table_p = table_node	# table_p is the current table node
		hit_p = None
		miss_p = None
		table_list = []		# table sequence in dataPlane
		hit_list = []		# hit_list has not been analysised
		i = 0			# test_loop_tag
		while table_p != None:
			print "======%d loop======"%i
			#print i, table_p
			i = i+1
			appendTableList(table_list, table_p)

			'''	# table node info.
			print table_p.name + ".next_ info: ", table_p.next_
			print "==control_flow_parent", table_p.control_flow_parent
			print "==conditional_barrier", table_p.conditional_barrier
			print '==dependencies_to', table_p.dependencies_to
			print '==dependencies_for', table_p.dependencies_for
			print '==base_default_next', table_p.base_default_next
			'''

			miss_p = None
			if type(table_p.next_) == dict:		# {"hit": **,"miss": **}
				for hit_ness, hit_table_node in table_p.next_.items():
					if hit_ness == 'hit':
						if hit_table_node != None:				
							hit_list.append(hit_table_node)
					else:
						miss_p = hit_table_node
				if miss_p != None:			
					table_p = miss_p
				else:
					table_p = None
			else:					# {actions: **, actions: **}
				#print table_p.next_
				for action_node, action_table_node in table_p.next_.items():
					table_p = action_table_node
					#print "abc", action_node, action_table_node
					break
			if (len(hit_list) > 0) and (table_p == None):
				table_p = hit_list[0]
				del hit_list[0]
			else:
				table_p = table_p
			#print "hit_lis:", hit_list
		print table_list
		print "end===="


	p4_field_type = '<class \'p4_hlir.hlir.p4_headers.p4_field\'>'
	p4_signature_ref_type = '<class \'p4_hlir.hlir.p4_imperatives.p4_signature_ref\'>'

	table_matchWidth_list = []	# list, used to describe the width of each table
	table_actionWidth_list = []	# list, used to describe the width of total actions in each table, including parameter and action_bit
	table_matchType_list = []	# list, used to describe the type of each table
	table_action_matching_list = {}	#dict, used to describe the matching relationship of table to actions
	table_dep_list = []		# list, used to describe the table dependent to the front table represented by tableID
	metadata_list = []		# list, used to describe the field/key should be included in the metadata
	table_match_meta_list = []	# list, used to describe the field/key used by each table_match
	table_action_meta_list = {}	# dict, used to describe the field/key used by each table_action
	 
	# add switching_metadata to metadata_list
	for header_instances_name, header_instances in h.p4_header_instances.items():
		print header_instances_name
		if header_instances.header_type.name == 'switching_metadata_t':
			for field_p in header_instances.fields:
				#print '\t', field_p.name, field_p.width
				metadata_list.append(field_p)

	# get table_list...
	for table_p in table_list:
		#print 'match_fields:', table_p.match_fields
		#print table_p, table_p.conditional_barrier #table_p.dependencies_to, table_p.dependencies_for
		match_width = 0
		action_width = 0
		match_type = ''
		premitive_action_list = []
		table_dep_id = 0
		table_dep_hitness = ''
		eachTable_match_meta_list = []
		eachTable_action_meta_list = []

		# add table dependence; just supporting "hit" & "miss" in this version
		if table_p.conditional_barrier != None:
			table_dep_hitness = table_p.conditional_barrier[1]
			table_dep_id = findTableID(table_p.conditional_barrier[0].name, table_list)
			#print "============table_dep_id:", table_dep_id
		else:
			table_dep_id = 0
			table_dep_hitness = ''
		table_dep_list.append((table_dep_hitness, table_dep_id))

		# add match_width & match_type
		for match_field_p in table_p.match_fields:
			match_width += match_field_p[0].width
			match_type = str(match_field_p[1])
			appendMetadataList(metadata_list, match_field_p[0])
			#print type(match_field_p[0]), match_field_p[0].name
		table_matchWidth_list.append(match_width)
		table_matchType_list.append(match_type)
		
		# calculate table_match_meta_list
		for match_field_p in table_p.match_fields:
			match_field_startBit = locateField(metadata_list, match_field_p[0])
			match_field_endBit = match_field_startBit + match_field_p[0].width
			eachTable_match_meta_list.append((match_field_startBit, match_field_endBit))

		# add action_width &action_table_matching list
		for action_p in table_p.actions:
			subAction_list = []
			#print "1", action_p.name, action_p.signature, action_p.signature_widths
			#action_width += action_p.signature_widths
			for signature_width_p in action_p.signature_widths:
				action_width += signature_width_p
			#print "call_sequence:", action_p.call_sequence
			#print "flat_call_sequence:", action_p.flat_call_sequence
			eachSubAction_meta_list = []
			for subAction in action_p.call_sequence:
				#print subAction[0].name, subAction[1]
				subAction_list.append(subAction)
				#appendMetadataList(metadata_list, action_field_p)
				para_meta_list = []
				for action_field_p in subAction[1]:
					if str(type(action_field_p)) == p4_field_type:
						appendMetadataList(metadata_list, action_field_p)
						action_field_startBit = locateField(metadata_list, action_field_p)
						action_field_endBit = action_field_startBit + action_field_p.width
					else:
						action_field_startBit = 0
						action_field_endBit = 0
					para_meta_list.append((action_field_startBit, action_field_endBit))
				eachSubAction_meta_list.append((subAction[0], para_meta_list))
				'''
				if subAction[1] == []:
					print "2"
				for parameter in subAction[1]:
					if str(type(parameter)) == p4_field_type:
						print parameter.width
						print "3"
					elif str(type(parameter)) == p4_signature_ref_type:
						print '4', parameter.idx
				'''
			# each action  refrence to 1bit in actionBit
			action_width += 1
			premitive_action_list.append(subAction_list)
			eachTable_action_meta_list.append(eachSubAction_meta_list)
		
		table_actionWidth_list.append(action_width)
		table_action_matching_list[ str(table_p.name)] = premitive_action_list
		table_match_meta_list.append(eachTable_match_meta_list)
		table_action_meta_list[ str(table_p.name) ] = eachTable_action_meta_list

	print 'table_matchWidth_list:\t', table_matchWidth_list
	print 'table_actionWidth_list:\t', table_actionWidth_list
	print 'table_matchType_list:\t', table_matchType_list
	print 'table_action_matching_dict:\t', table_action_matching_list
	print 'table_dep_list:\t', table_dep_list
	print 'metadata_list:'
	for field_p in metadata_list:
		print '\t', field_p.name, field_p.instance, field_p.width
	print 'table_match_meta_list:\t', table_match_meta_list
	print 'table_action_matching_dict:\t', table_action_meta_list


	metadata_list_pkt = []
	for field_p in metadata_list:
		if field_p.instance.header_type.name != 'switching_metadata_t':
			metadata_list_pkt.append(field_p)
	return metadata_list_pkt

	#for action_name, action in h.p4_actions.items():
	#	print action.name+"============="
	#	print action.call_sequence
		#print action.flat_call_sequence
		
		#print action.signature
		#print action.signature_widths
		
		#print action.signature_flags
	'''
		for sigF_name, sigF in action.signature_flags.items():
			#print sigF_name,sigF
					
			for sigF_item_name, sigF_item in sigF.items():
				#print sigF_item_name, sigF_item
				if str(sigF_item_name) == "data_width":
					#print action.signature_flags
					#print sigF
					print type(sigF_item), sigF_item
		'''
	'''
		print a_name.name, type(a_name.name)
		for c in a_name.match_fields:
			print c[0].name, c[1], c[2]
		print "=====actions====="
		for d in a_name.actions:
			print d.name	
		print "=====size====="
		print a_name.min_size, a_name.max_size
		print "=====next====="
		print a_name.next_, type(a_name.next_)
		if type(a_name.next_) == dict:
			print "abc"
			for hit_ness, e in a_name.next_.items():
				if hit_ness == "miss":
					f_miss = e
				else: 
					f_hit = e
			print f_miss.next_
			print f_hit.next_
		print "=====timeOut===="
		if a_name.support_timeout == False:
			print a_name.support_timeout
		'''

	# p4_egress_ptr is only a table node
	#print h.p4_egress_ptr, type(h.p4_egress_ptr), h.p4_egress_ptr.next_


	'''
		for c in b_item:
			print c.name
	'''
	#print h.p4_egress_ptr

	#p4_tables
	"""
	for table_name, table in h.p4_tables.items():
		print table_name, table.match_fields
	"""

	#p4_headers
	'''
	for header_name, header in h.p4_headers.items():
		print header.name, type(header.length)
		#print header.layout
		print header.attributes	
		#for field, width in header.layout.items():
		#	print type(field), width
	'''

	#p4_header_instances
	'''
	for header_name, header in h.p4_header_instances.items():
		print header.name + "===================================="	
		print header.virtual	
		#for field, width in header.header_type.layout.items():
		#	print type(field)
	'''
	'''
	#p4_fields
	for field_name, field in h.p4_fields.items():
		print field.name, field.calculation	
		for item in field.calculation:
			print item[0]
			print item[1].name
			print item[2].left, item[2].right, item[2].op
	'''

	#p4_field_lists
	'''
	for field_list_name, field_list in h.p4_field_lists.items():
		print field_list.name
		for field in field_list.fields:
			print field.name, field.offset, field.width, field.calculation
			for item in field.calculation:		
				for i in range(3):			
					print type(item[i])		
				#print item[1].output_width
	'''

	#p4_field_list_calculations
	'''
	for field_list_name, field_list in h.p4_field_list_calculations.items():
		print field_list.name, field_list.input, field_list.output_width, field_list.algorithm
		for a in field_list.input:
			for b in a.fields:		
				print b
	'''

	#p4_parser_state
	#print type(h.p4_parse_states)

	'''
	for parser_name, parser in h.p4_parse_states.items():
		print parser.name
		#call_sequence
		#print parser.call_sequence
		
		for se in parser.call_sequence:
			print se
			if len(se) == 3:
				print str(se[0]) == "set"
				print se[1].name, se[1].instance, se[1].offset
		
		
		#branch_on
		
		#print parser.branch_on, type(parser.branch_on)
		for field in parser.branch_on:
			print field.name
		
		
		#branch_to
		for key, dest in parser.branch_to.items():	
			print key, dest
		
		#prev
		
		#print parser.prev
		for state in parser.prev:
			print state.name
	'''	


	#p4_action
	'''
	for action_name, action in h.p4_actions.items():
		print action.name+"============="
			
		for sig_name in action.signature:
			print sig_name

		print action.signature_widths
		
		#print action.signature_flags
		
		for sigF_name, sigF in action.signature_flags.items():
			#print sigF_name,sigF
					
			for sigF_item_name, sigF_item in sigF.items():
				#print sigF_item_name, sigF_item
				if str(sigF_item_name) == "data_width":
					#print action.signature_flags
					#print sigF
					print type(sigF_item), sigF_item
			

		
		#call_sequence
		print action.call_sequence
		for call_function in action.call_sequence:
			for i in range(len(call_function)):
				if i ==0:
					print call_function[0].name, call_function[0].signature
				else:
					print call_function[i]
					for item in call_function[1]:
						print item,type(item)
		#print "***************"	
		#print action.flat_call_sequence
	'''	

	#p4_node
	'''
	for table_name, table in h.p4_nodes.items():
		print table.name+"============="
		#print table.next_
		#match_fields	
		print table.control_flow_parent
		print table.base_default_next

		for match_field in table.match_fields:
			for field in match_field:
				print field	
		#print table.attached_counters
		print "1"+table.control_flow_parent, table.conditional_barrier
		print table.base_default_next
		print table.dependencies_to
	'''
	'''
	#p4_action_node
	for action_node_name, action_node in h.p4_action_nodes.items():
		print action_node.name
	'''
	#p4_conditional_node

	for action_node_name, action_node in h.p4_conditional_nodes.items():
		print action_node_name, action_node.name
	'''
	for action_node_name, action_node in h.p4_action_profiles.items():
		print action_node.name
	'''

	#p4_counter
	"""
	for counter_name, counter in h.p4_counters.items():
		print counter.name, counter.type, counter.min_width, counter.saturating
		print counter.binding, counter.instance_count
	"""

	#p4_register
	"""
	for register_name, register in h.p4_registers.items():
		print register.name+"=================="
		print register.layout, register.width, register.instance_count
		print register.binding
	"""

	#p4_parser_exception
	"""
	for parser_ex_name, parser_ex in h.p4_parser_exceptions.items():
		print parser_ex
	"""



	"""
	tuple: e.g.,

	fruits = ("apple", "banana", "orange")
	for i in range(len(fruits)):
		print fruits[i]

	list: e.g.,

	fruits = ["apple","banana","orange"]
	for fruit in fruits:
		print fruit

	dictionary: e.g.,

	fruit_dict = {"apple":1, "banana":2, "orange":3}
	for key in fruit_dict:
		print fruit_dict[key]

	"""
