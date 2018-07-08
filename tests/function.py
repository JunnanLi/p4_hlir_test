def appendTableList(table_list, table):
	for i in range(len(table_list)):
		if table.name == table_list[i].name:
			del table_list[i]
	table_list.append(table)
	return

def findTableID(table_name, table_list):
	for table_p in table_list:
		if table_p.name == table_name:
			break
	return table_list.index(table_p)

def appendMetadataList(metadata_list, field):
	for field_p in metadata_list:
		if field_p.name == field.name:
			return
	metadata_list.append(field)

def locateField(metadata_list, field):
	offset = 0
	for field_p in metadata_list:
		if field_p.name == field.name:
			return offset
		else:
			offset += field_p.width
	return	-offset