# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snowowl', 'snowowl.graph', 'snowowl.priorityqueue']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'snowowl',
    'version': '0.0.3',
    'description': 'A collection of common data structures',
    'long_description': "# snowowl\n\nA collection of common data structures\n\n## Example: How to use Heap library\n\n```\n#!/usr/bin/env python3\nauthor: greyshell\n\nfrom snowowl import Heap, HeapType\n\n\nif __name__ == '__main__':\n    arr = [5, 9, 2]\n\n    hmin = Heap(arr)  # create a min heap\n    print(hmin.peek())  # peek the min item from the heap\n    hmin.insert(1)  # insert an item into the heap\n    print(hmin.remove())  # remove an item from the heap\n    print(hmin)  # print all items from the heap\n    print(len(hmin))  # print the length of the heap\n\n    hmax = Heap(arr, HeapType.MAX)  # create a max heap\n    print(hmax.peek())  # peek the max item from the heap\n    hmax.insert(1)  # insert an item into the heap\n    print(hmax.remove())  # remove an item from the heap\n```\n",
    'author': 'ABHIJIT SINHA',
    'author_email': 'grey.shell@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/greyshell/snowowl',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
