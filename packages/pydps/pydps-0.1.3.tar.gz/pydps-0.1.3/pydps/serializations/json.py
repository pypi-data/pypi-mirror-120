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
import importlib
from typing import Any
from abc import ABC, abstractmethod
from pydps.creation import Singleton
from json import JSONEncoder, JSONDecoder, JSONDecodeError


class JsonSerializable(ABC):
    """
    This interface class provide json serialization feature to inherited classes.
    ---------
    @author:    Hieu Pham.
    @created:   21-09-2021.
    @updated:   21-09-2021.
    """

    def __init__(self, **kwargs):
        """
        Construct new instance.
        :param kwargs:  additional keyword arguments.
        """
        super().__init__()

    @abstractmethod
    def __serialize__(self, **kwargs) -> dict:
        """
        Serialize json-liked data.
        :return: json-liked data.
        """
        return {'class': self.__class__.__name__, 'module': self.__module__}

    def __deserialize__(self, data: dict = dict):
        """
        Deserialize json-liked data.
        :param data: json-liked data.
        :return:     object itself.
        """
        return self


class JsonSerializer(JSONEncoder, metaclass=Singleton):
    """
    This singleton class will serialize object to json dict structures.
    ---------
    @author:    Hieu Pham.
    @created:   21-09-2021.
    @updated:   21-09-2021.
    """

    def __init__(self):
        """
        Construct new instance.
        """
        super().__init__(default=self.default)

    def default(self, o: Any) -> Any:
        """
        Override default encoding handle.
        :param o:   object to be serialized.
        :return:    any.
        """
        return o.__serialize__() if isinstance(o, JsonSerializable) else super().default(o)


class JsonDeserializer(JSONDecoder, metaclass=Singleton):
    """
    This singleton class will deserialize json dict structures to object.
    ---------
    @author:    Hieu Pham.
    @created:   21-09-2021.
    @updated:   21-09-2021.
    """

    def __init__(self):
        """
        Construct new instance.
        """
        super().__init__(object_hook=self.object_hook)

    def object_hook(self, data: dict = None) -> Any:
        """
        Override parent object hook method.
        :param data:    structures dict.
        :return:        any.
        """
        # Validate data.
        if 'class' in data and 'module' in data:
            # Dynamic load module and class by name.
            class_name, module_name = data.pop('class'), data.pop('module')
            classes = getattr(importlib.import_module(module_name), class_name)
            # Create instance and then return.
            if issubclass(classes, JsonSerializable):
                return classes(**data).__deserialize__(data)
        # Otherwise, raise an error.
        raise JSONDecodeError("Cannot deserialize invalid data format.")
