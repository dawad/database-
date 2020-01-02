#!usr/bin/python
# -*- coding: utf-8 -*-


class Database(object):

	def __init__(self, _root):

		self._graph = list()
		self._extract = dict()
		self._graph.append(_root)
		self.revision = list()

	def add_nodes(self, node):
		# it takes list of tuples (ID of new node, ID of the parent node)
		# Each non empty graph will start with tuple ("core", None)
		if len(self._graph) >= 1:
			before = list(self._graph)
			self._graph.extend(node)
			after = self._graph
			if before != after:
				self.revision.append(before)
		else:
			self._graph.append(node)

	def add_extract(self, extract):
		# it takes a dict as input where keys are the image name and the values
		# are the Id of the class
		if self._extract:
			self._extract.update(extract)
		else:
			self._extract = extract

	def get_extract_status(self):
		# takes extract
		result = {}
		old_graph = self.revision[-1]
		after_graph = self._graph

		for img_id, classes_id in self._extract.items():
			if len(classes_id) > 1:
				answer = [filter_by_class_id(cls_id, old_graph, after_graph) for cls_id in classes_id]
				result[img_id] = self.get_img_status(answer)
			else:
				answer = filter_by_class_id(classes_id, old_graph, after_graph)
				result[img_id] = answer
		return result

	def get_img_status(self, classes_status):
		if 'invalid' in classes_status:
			return 'invalid'
		else:
			if any(cls == 'coverage-staged' for cls in classes_status):
				return 'coverage-staged'
			else:
				if 'granularity-staged' in classes_status:
					return 'granularity-staged'
				else:
					if all(cls == 'valid' for cls in classes_status):
						return 'valid'


def filter_by_class_id(class_id, old_graph, after_graph):
	exist = [element for element in after_graph if class_id == element[0] or class_id == element[1]]
	if not exist:
		return 'invalid'
	else:
		after_nodes = [element for element in after_graph if element[1] == class_id]
		old_nodes = [element for element in old_graph if element[1] == class_id]
		if len(after_nodes) == len(old_nodes):
			return 'valid'
		else:
			if len(after_graph) > len(old_nodes):
				if len(old_nodes) > 1:
					return 'coverage-staged'
				else:
					return 'granularity-staged'


def _main():
	# Initial graph
	build = [("core", None), ("A", "core"), ("B", "core"), ("C", "core"), ("C1", "C")]
	# Extract
	extract = {"img001": ["A", "B"], "img002": ["A", "C1"], "img003": ["B", "E"]}
	# Â Graph edits
	edits = [("A1", "A"), ("A2", "A"), ("C2", "C")]
	# Get status (this is only an example, test your code as you please as long as it works)
	status = {}
	if len(build) > 0:
		# Build graph
		db = Database(build[0])
		if len(build) > 1:
			db.add_nodes(build[1:])
		# Add extract
		db.add_extract(extract)
		# Graph edits
		db.add_nodes(edits)
		# Update status
		status = db.get_extract_status()
	print(status)


if __name__ == '__main__':
	_main()
