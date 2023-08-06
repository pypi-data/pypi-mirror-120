#    JointBox CLI
#    Copyright (C) 2021 Dmitry Berezovsky
#    The MIT License (MIT)
#
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files
#    (the "Software"), to deal in the Software without restriction,
#    including without limitation the rights to use, copy, modify, merge,
#    publish, distribute, sublicense, and/or sell copies of the Software,
#    and to permit persons to whom the Software is furnished to do so,
#    subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import yaml

from cli_rack_validation.domain import TimePeriodMilliseconds, HexInt, IPAddress, MACAddress, TimePeriod
from cli_rack_validation.validate import SensitiveStr
from jointbox_cli.esphome_ext.expressions.core import EvaluatedObject


class JointboxYamlTools:
    @classmethod
    def initialize(cls):
        yaml.add_representer(EvaluatedObject, cls.__represent_dict_subclass)
        yaml.add_representer(SensitiveStr, cls.__represent_sensitive_str)
        yaml.add_representer(TimePeriodMilliseconds, cls.__represent_to_str_class)
        yaml.add_representer(HexInt, cls.__represent_to_str_class)
        yaml.add_representer(IPAddress, cls.__represent_to_str_class)
        yaml.add_representer(MACAddress, cls.__represent_to_str_class)
        yaml.add_representer(TimePeriod, cls.__represent_to_str_class)

    @classmethod
    def __represent_dict_subclass(cls, dumper, data: dict):
        node = dumper.represent_dict(dict(data))
        return node

    @classmethod
    def __represent_sensitive_str(cls, dumper, data: SensitiveStr):
        node = dumper.represent_str(data.data)
        return node

    @classmethod
    def __represent_to_str_class(cls, dumper, data: SensitiveStr):
        node = dumper.represent_str(str(data))
        return node
