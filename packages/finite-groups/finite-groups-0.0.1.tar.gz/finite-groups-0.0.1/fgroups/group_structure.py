import numpy as np
from itertools import product

def is_permutation_group(elements_array):
	"""Function that check whether a given set has a permutation group structure or not.

	Inputs
	------
	- elements_array: numpy array of a list containing the elements of the given set.

	Outputs
	-------
	- True or False: True if the elements_array has the 4 properties required to has a permutation group structure, False if not.

	Tests
	-----
	>>> is_permutation_group(np.array([]))
	True
	>>> is_permutation_group(np.array([[0, 1], [1, 0]]))
	True
	>>> is_permutation_group(np.array([[0, 1, 2]]))
	True
	>>> is_permutation_group(np.array([[0, 1, 2], [1, 2, 0], [2, 0, 1]]))
	True
	>>> is_permutation_group(np.array([[1, 2, 0], [2, 0, 1]]))
	False
	>>> is_permutation_group(np.array([[0, 1, 2], [0, 2, 1], [2, 0, 1]]))
	False
	>>> is_permutation_group(np.array([[0, 1, 2], [0, 2, 1], [2, 1, 0], [1, 0, 2], [1, 2, 0], [2, 0, 1]]))
	True
	>>> is_permutation_group(np.array([[0, 1, 2, 3, 4, 5, 6], [0, 6, 2, 3, 4, 5, 1]]))
	True
	>>> is_permutation_group(np.array([[0, 1, 2, 3], [3, 2, 1, 0]]))
	True
	>>> is_permutation_group(np.array([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1]]))
 	False
	>>> is_permutation_group(np.array([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]))
	True
	"""
	if len(elements_array) == 0:
		return True
	# Closed multiplication
	if not all(any((x[y] == z).all() for z in elements_array) for x, y in product(elements_array, elements_array)):
		return False
	# Identity check
	identity = "null"
	for x in elements_array:
		if all((x[y] == y).all() and (y[x] == y).all() for y in elements_array):
			identity = x
			break
	if type(identity) == str:
		return False
	# Associativity check
	elif not all((x[y[z]] == x[y][z]).all() for x, y, z in product(elements_array, elements_array, elements_array)):
		return False
	# Inverse check
	elif not all(any((x[y] == identity).all() and (y[x] == identity).all() for y in elements_array) for x in elements_array):
		return False
	else:
		return True

if __name__ == "__main__":
	n = int(input("Enter Set cardinality:"))
	iterable_list = []
	for i in range(n):
		element_string = input("Enter a list element separated by spaces:")
		element_split = element_string.split()
		element = list(map(int, element_split))
		iterable_list.append(element)
	elements_array = np.array(iterable_list)
	print(is_permutation_group(elements_array))
