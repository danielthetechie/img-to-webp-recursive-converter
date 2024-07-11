import os

def get_directory_left_child (directory_path):
	entries_in_folder = os.listdir (directory_path)

	for entry in entries_in_folder:
		entry_path = os.path.join (directory_path, entry)

		if (os.path.isdir (entry_path)):
			return entry_path

	return None

def get_directory_right_sibling (directory_path):
	right_sibling = None

	entries_in_folder = os.listdir (directory_path + "/../")
	break_on_next_iteration = False

	for entry in entries_in_folder:
		entry_path = os.path.join (directory_path + "/../", entry)

		if os.path.isdir (entry_path) and break_on_next_iteration:
			right_sibling = "./" + os.path.normpath (entry_path)
			break

		# entry = test2, directory_path = ./test/test2
		if os.path.isdir (entry_path) and entry == os.path.basename (directory_path):
			break_on_next_iteration = True

	return right_sibling

def get_all_directories_paths_from_directory (current_directory = './'):
	directories_paths = []
	entries_in_folder = os.listdir (current_directory)

	for entry in entries_in_folder:
		entry_path = os.path.join (current_directory, entry)
		if (os.path.isdir (entry_path)):
			directories_paths.append (entry_path)

	return directories_paths

class TreeNode:
	def __init__ (self, path):
		self.path = path
		self.left_child = None
		self.right_sibling = None

def create_directory_node (directory_path):
	directory_node = TreeNode (directory_path)
	directory_node.left_child = None
	directory_node.right_sibling = None

	return directory_node

def get_next_path_from_path (path, directories_paths, root_directory):
	parent_path = path + "/../"

	left_child = get_directory_left_child (path)
	if (left_child != None and left_child not in directories_paths):
		return left_child

	right_sibling = get_directory_right_sibling (path)
	if (right_sibling != None and right_sibling not in directories_paths):
		return right_sibling

	parent_path = "./" + os.path.normpath (parent_path)

	if (parent_path == "./."):
		parent_path = "./"

	#if parent_path == directories_paths[0]:
	if parent_path == root_directory:
		return None

	return parent_path

def get_all_subdirectories_paths_from_directory (root_directory, current_directory = "./", directories_nodes = [], directories_paths = set ()):

	next_path = None

	if len (directories_paths) == 0:
		for dn in directories_nodes:
			directories_paths.add (dn.path)

	if directories_nodes == []:
		current_directory = root_directory
		root = create_directory_node (current_directory)
		root.left_child = TreeNode (get_directory_left_child (current_directory))
		root.right_sibling = TreeNode (get_directory_right_sibling (current_directory))
		directories_nodes.append (root)
	else:
		next_path = get_next_path_from_path (directories_nodes[-1].path, directories_paths, root_directory)

		if next_path == None:
			return directories_nodes

		node = create_directory_node (next_path)
		node.left_child = TreeNode (get_directory_left_child (next_path))
		node.right_sibling = TreeNode (get_directory_right_sibling (next_path))
		directories_nodes.append (node)
		directories_paths.add (directories_nodes[-1].path)

	get_all_subdirectories_paths_from_directory (root_directory, directories_nodes[-1].path, directories_nodes, directories_paths)

	return sorted (directories_paths)


def cwebp_convert_all_images_in_folder (quality, convert_recursively):
	images = []
	entries_in_folder = os.listdir ('./')

	for entry in entries_in_folder:
		if (os.path.isfile (entry)):
			images.append (entry)

	if convert_recursively:
		return images
	else:
		return get_all_subdirectories_paths_from_directory ()


#print (cwebp_convert_all_images_in_folder (80, True))
subdirectories = get_all_subdirectories_paths_from_directory ('./playground')

for sd in subdirectories:
	print (sd)