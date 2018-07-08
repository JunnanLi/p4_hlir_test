import sys
import collections
from p4_hlir.main import HLIR
from function import *



def parseParser(metadata_list):

	#h = HLIR("./stateful.p4")
	h = HLIR("./l2_switch.p4")
	#h = HLIR("../../tutorials-master/SIGCOMM_2015/flowlet_switching/p4src/simple_router.p4")
	#h = HLIR("../../tutorials-master/SIGCOMM_2015/source_routing/p4src/source_routing.p4")

	h.build()

	

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

	print '==================parser_state'
	for parser_name, parser in h.p4_parse_states.items():
		print parser.name
		#call_sequence
		print 'parser.call_sequence', parser.call_sequence
		
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
