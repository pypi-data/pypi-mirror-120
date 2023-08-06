# Copyright 2021 (David) Siu-Kei Muk. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import absltest

from afb.core import manufacturer as mfr_lib
from afb.core import broker as bkr_lib


class ManufacturerTest(absltest.TestCase):
  def _create_broker(self, *classes):
    bkr = bkr_lib.Broker()
    [bkr.register(mfr_lib.Manufacturer(cls)) for cls in classes]
    return bkr

  def test_initial_default_is_none(self):
    sut = mfr_lib.Manufacturer(_TrivialClass)
    self.assertIsNone(sut.default)

  def test_default_key_must_be_registered(self):
    sut = mfr_lib.Manufacturer(_TrivialClass)
    with self.assertRaises(KeyError):
      sut.default = "not exist"

  def test_get_non_exist_factory(self):
    sut = mfr_lib.Manufacturer(_TrivialClass)
    self.assertIsNone(sut.get("not exist"))

  def test_register(self):
    sut = mfr_lib.Manufacturer(_ValueHolder)

    key = "create/int"
    sut.register(key, *_FCTS[_ValueHolder][key])

    self.assertIn(key, sut)
    self.assertIsNotNone(sut.get(key))

  def test_make_simple(self):
    bkr = self._create_broker(_ValueHolder)
    sut = bkr.get(_ValueHolder)
    key = "create/int"
    sut.register(key, *_FCTS[_ValueHolder][key])

    vh = sut.make(key=key, inputs={"value": 1})

    self.assertIsInstance(vh, _ValueHolder)
    self.assertEqual(vh.value, 1)

  def test_make_with_list_type_spec(self):
    bkr = self._create_broker(_ValueHolder)
    sut = bkr.get(_ValueHolder)
    key = "sum/list/int"
    signature = {
        "ints": {
            "type": [int],
            "description": "List of integers whose sum is stored.",
        },
    }
    sut.register(key, lambda ints: _ValueHolder(sum(ints)), signature)

    vh = sut.make(key=key, inputs={"ints": [1, 2, 3, 4, 5]})

    self.assertIsInstance(vh, _ValueHolder)
    self.assertEqual(vh.value, 15)

  def test_make_with_tuple_type_spec(self):
    bkr = self._create_broker(_ValueHolder)
    sut = bkr.get(_ValueHolder)
    key = "sum/tuple"
    signature = {
        "numbers": {
            "type": (int, float, int, float),
            "description": "Numbers whose sum is stored.",
        },
    }
    sut.register(key, lambda numbers: _ValueHolder(sum(numbers)), signature)

    vh = sut.make(key=key, inputs={"numbers": (1, 2.0, 3, 4.0)})

    self.assertIsInstance(vh, _ValueHolder)
    self.assertAlmostEqual(vh.value, 10.0)

  def test_make_with_dict_type_spec(self):
    bkr = self._create_broker(_ValueHolder)
    sut = bkr.get(_ValueHolder)
    key = "sum/values"
    signature = {
        "value_map": {
            "type": {str: float},
            "description": "Dict mapping each name to a real number."
        },
    }
    sut.register(
        key,
        lambda value_map: _ValueHolder(sum(value_map.values())),
        signature)

    vh = sut.make(key=key, inputs={"value_map": {"a": 1.0, "b": 2.0, "c": 3.0}})

    self.assertIsInstance(vh, _ValueHolder)
    self.assertAlmostEqual(vh.value, 6.0)


class _TrivialClass(object):
  pass


class _ValueHolder(object):
  def __init__(self, value):
    self._val = value

  @property
  def value(self):
    return self._val


class _Adder(object):
  def __init__(self, v1, v2):
    self._v1 = v1
    self._v2 = v2

  @property
  def value(self):
    return self._v1 + self._v2

  @classmethod
  def from_holders(cls, vh1, vh2):
    return cls(vh1.value, vh2.value)


_FCTS = {
    _ValueHolder: {
        "create/int": (
            _ValueHolder,
            {
                "value": {
                    "type": int,
                    "description": "Integer. Value to be stored.",
                },
            },
        ),
        "create/float": (
            _ValueHolder,
            {
                "value": {
                    "type": float,
                    "description": "Float. Value to be stored.",
                },
            },
        ),
        "list/sum/vh": (
            lambda holders: _ValueHolder(sum(vh.value) for vh in holders),
            {
                "holders": {
                    "type": [_ValueHolder],
                    "description": "List of value holders.",
                },
            },
        ),
    },
    _Adder: {
        "create/floats": (
            _Adder,
            {
                "v1": {
                    "type": float,
                    "description": "First value.",
                },
                "v2": {
                    "type": float,
                    "description": "Second value.",
                }
            },
        ),
        "from_holders": (
            lambda vh1, vh2: _Adder(vh1.value, vh2.value),
            {
                "vh1": {
                    "type": _ValueHolder,
                    "description": "First value holder.",
                },
                "vh2": {
                    "type": _ValueHolder,
                    "description": "Second holder.",
                },
            },
        ),
    }
}


if __name__ == "__main__":
  absltest.main()
