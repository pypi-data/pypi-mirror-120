# ------------------------------------------------------------------------------
#  MIT License
#
#  Copyright (c) 2021, Hieu Pham. All rights reserved.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# ------------------------------------------------------------------------------
from typing import Any, Union, List
from abc import ABC, abstractmethod
from pydps.serializations import JsonSerializable, JsonSerializer, JsonDeserializer


class BaseLeaf(JsonSerializable, ABC):
    """
    This class is basic element to build tree node.
    ---------
    @author:    Hieu Pham.
    @created:   21-09-2021.
    @updated:   21-09-2021.
    """

    @property
    def is_root(self):
        return self._parent is None

    @property
    def parent(self):
        return self._parent

    @property
    def is_leaf(self):
        return True

    def __init__(self, parent: Any = None, **kwargs):
        """
        Construct new instance.
        :param parent:  parent node of leaf.
        :param kwargs:  additional keyword arguments.
        """
        super().__init__(**kwargs)
        # Validate parent node.
        assert isinstance(parent, BaseLeaf) or parent is None, 'Parent of node must be at least instance of BaseLeaf.'
        # Assign parent node.
        self._parent = parent


class BaseNode(BaseLeaf, ABC):
    """
    This class is basic element to build tree structure.
    ---------
    @author:    Hieu Pham.
    @created:   21-09-2021.
    @updated:   21-09-2021.
    """

    def __init__(self, parent: BaseLeaf = None, **kwargs):
        """
        Construct new instance.
        :param parent:  parent node of node.
        :kwargs:        additional keyword arguments.
        """
        super().__init__(parent=parent, **kwargs)
        self._nodes = list()

    def attach(self, nodes: Union[BaseLeaf, List[BaseLeaf]]):
        """
        Attach given node(s) to tree.
        :param nodes:   given node(s).
        :return:        tree and node(s).
        """
        # Attach single node.
        if isinstance(nodes, BaseLeaf):
            nodes._parent = self
            self._nodes.append(nodes)
        # Attach nodes list.
        elif isinstance(nodes, list):
            for node in nodes:
                self.attach(node)
        # Return result.
        return self, nodes

    def detach(self, indexes: [int, List[int]]):
        """
        Detach node(s) from tree.
        :param indexes: index(es) of detached node(s).
        :return:        tree and node(s).
        """
        node = None
        # Detach single node.
        if isinstance(indexes, int):
            node = self._nodes.pop(indexes)
            node._root = None
        # Detach nodes list.
        elif isinstance(indexes, list):
            node = [self.detach(i)[-1] for i in indexes]
        # Return result.
        return self, node

    def clean(self):
        """
        Detach all nodes.
        :return: tree and node(s).
        """
        return self.detach([i for i in range(len(self._nodes))])

    @abstractmethod
    def __serialize__(self) -> dict:
        """
        Serialize object to dict structures.
        :return:    dict structures.
        """
        data = super().__serialize__()
        data.update({'nodes': [JsonSerializer.encode(node) for node in self._nodes]})
        return data

    @abstractmethod
    def __deserialize__(self, data: dict = {}):
        """
        Deserialize dict structures to object.
        :param data:    dict structures.
        :return:        object itself.
        """
        self.clean()
        self.attach([JsonDeserializer().decode(dat) for dat in data.get('nodes', {})])
        return self
