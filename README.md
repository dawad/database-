# database-
creates directed graph data structure 
Database is a class that defines data structures that handles both coverage and granularity changes using a directed graph structure.
A graph is a list of nodes. Each node contains two elements: the child and the parent.  
A graph contains by default root node: (‘core’, none)
It contains the following methods implemented: 
-	‘add_nodes’: it takes a node or a list of nodes as input.  It takes a tuple or a list of tuples that contains the ID of the child and the ID of the parent. 
-	‘add_extract’: add a dictionary of images as input. The keys are image names and values are list of class/node IDs
-	‘get_extract_status’: returns the status of each image considering graph modifications that occurred after the extract was added. It compares the graph before and after being edited using a list called revision. This last stores the information before being edited. For each Id, we extract the changes and we return the status :
o	‘Valid’ if no changes has been occurred 
o	‘Coverage-staged’ : if Id  has children and we add a new child 
o	‘Granularity-staged’: if id doesn’t have children and we add child 
o	‘Invalid’ if Id doesn’t exist in the graph 
