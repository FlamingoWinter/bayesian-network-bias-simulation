## Installation
- `pip install requirements.txt`
- For plotting (which should only be necessary for debugging), 
install C++ from https://visualstudio.microsoft.com/visual-cpp-build-tools/, install graphviz from https://graphviz.org/download/, 
then install pygraphviz with the command:

```python -m pip install --config-settings="--global-option=build_ext" --config-settings="--global-option=-IC:\Program Files\Graphviz\include" --config-settings="--global-option=-LC:\Program Files\Graphviz\lib" pygraphviz```

- There's another weird error when plotting where `removehandler()` is called on a None object. That can be suppressed by modifying the library.