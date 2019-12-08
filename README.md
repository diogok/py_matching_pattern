# Python Pattern Matching

Inspired  by [pampy](https://github.com/santinic/pampy) and [core.match](https://github.com/clojure/core.match), this is a pattern matching library for dynamic list of patterns.

Right now it only supports matching lists of same sames.

## Usage

Import the lib

```python
import py_matching_pattern as pm
```

First you will add initialize with a fixed size of keys to match (size of the list).


```python
pmdb = core.PatternMatchStore(keysize=3)
```

After that you can add the patterns. Every value is valid match, including `None`.

The "catch all" value is `default` attribute of the instance.

```python
_ = pmdb.default
pmdb.put(keys=["a","b","c"],value=1)
pmdb.put(keys=["a","b","b"],value=2)
pmdb.put(keys=["a","b",_],value=3)
pmdb.put(keys=["a",_,_],value=4)
pmdb.put(keys=["a",None,"c"],value=5)
```

These patterns are staged for the DB. This is useful if you reload the patterns from another thread.

To make the pattern live, you commit it.

```python
pmdb.commit()
```

Now you can finally start matching values:

```python
pmdb.get(keys=["a","b","c"])==1
pmdb.get(keys=["a","b","b"])==2
pmdb.get(keys=["a","b","d"])==3
pmdb.get(keys=["a","c","d"])==4
pmdb.get(keys=["a",None,"c"])==5
```

The staged patterns are kept between commits, so you can add or override to it later.

But in case you want to clean it:

```python
pmdb.clean()
```

## License

MIT
