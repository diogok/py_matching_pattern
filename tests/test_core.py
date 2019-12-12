import unittest
import py_matching_pattern as core

class CoreTest(unittest.TestCase):

    def test_basic(self):
        mm = core.PatternMatchStore(keysize=3)
        _=mm.default

        mm.put(keys=["a","b","c"],value=1)
        mm.put(keys=["a","b","b"],value=2)
        mm.put(keys=["a","b",_],value=3)
        mm.put(keys=["a",_,_],value=4)
        mm.put(keys=["a",None,"c"],value=5)

        mm.commit()

        self.assertEqual(1,mm.get(keys=["a","b","c"]))
        self.assertEqual(2,mm.get(keys=["a","b","b"]))
        self.assertEqual(3,mm.get(keys=["a","b","d"]))
        self.assertEqual(4,mm.get(keys=["a","c","d"]))
        self.assertEqual(5,mm.get(keys=["a",None,"c"]))

    def test_break_out_of_loop(self):
        mm = core.PatternMatchStore(keysize=3)
        _=mm.default

        mm.put(keys=["a","b","c"],value=1)
        mm.put(keys=["a","b","b"],value=2)
        mm.put(keys=["a","b",_],value=3)
        #mm.put(keys=["a",_,_],value=4)

        mm.commit()

        self.assertEqual(None,mm.get(keys=["a","c","d"]))

    def test_back_and_forth(self):
        mm = core.PatternMatchStore(keysize=3)
        _=mm.default

        mm.put(keys=["a","b","c"],value=1)
        mm.put(keys=["a","b","b"],value=2)
        mm.put(keys=["a","b",_],value=3)
        mm.put(keys=["a",_,"d"],value=4)
        mm.put(keys=["a",_,_],value=5)
        mm.put(keys=[_,_,"d"],value=6)

        mm.commit()

        self.assertEqual(1,mm.get(keys=["a","b","c"]))
        self.assertEqual(2,mm.get(keys=["a","b","b"]))
        self.assertEqual(3,mm.get(keys=["a","b","d"]))
        self.assertEqual(4,mm.get(keys=["a","c","d"]))
        self.assertEqual(5,mm.get(keys=["a","c","e"]))
        self.assertEqual(4,mm.get(keys=["a","d","d"]))
        self.assertEqual(5,mm.get(keys=["a","d","e"]))
        self.assertEqual(6,mm.get(keys=["d","d","d"]))
        self.assertEqual(None,mm.get(keys=["d","d","e"]))

    def test_basic_unordered(self):
        mm = core.PatternMatchStore(keysize=3)
        d=mm.default

        mm.put(keys=["a","b",d],value=3)
        mm.put(keys=["a",'b',"b"],value=2)
        mm.put(keys=["a",d,d],value=4)
        mm.put(keys=["a","b","c"],value=1)

        mm.commit()

        self.assertEqual(1,mm.get(keys=["a","b","c"]))
        self.assertEqual(2,mm.get(keys=["a","b","b"]))
        self.assertEqual(3,mm.get(keys=["a","b","d"]))
        self.assertEqual(4,mm.get(keys=["a","c","d"]))

    def test_basic_clean(self):
        mm = core.PatternMatchStore(keysize=3,raise_notfound=True)

        mm.put(keys=["a","b","c"],value=1)
        mm.commit()
        self.assertEqual(1,mm.get(keys=["a","b","c"]))

        mm.clean()
        mm.commit()
        with self.assertRaises(core.KeyNotFound):
            mm.get(keys=["a","b","c"])

    def test_uncommited(self):
        mm = core.PatternMatchStore(keysize=3,raise_notfound=True)

        mm.put(keys=["a","b","c"],value=1)
        with self.assertRaises(core.KeyNotFound):
            mm.get(keys=["a","b","c"])

    def test_uncommited_clean(self):
        mm = core.PatternMatchStore(keysize=3)

        mm.put(keys=["a","b","c"],value=1)
        mm.commit()
        self.assertEqual(1,mm.get(keys=["a","b","c"]))

        mm.clean()
        self.assertEqual(1,mm.get(keys=["a","b","c"]))

    def test_validate_all_leaf_have_default(self):
        pass

    def test_validate_conflicts(self):
        pass

    def test_invalid_keycount(self):
        pass

    def test_invalid_keysize(self):
        pass

    def test_value_not_found(self):
        pass