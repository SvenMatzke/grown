"""
Module to control all settings data and so on
Usage should be 1 instance of store storing and transmitting to elements
The way python works on load creates a single instance and modules are normaly not loaded twice
"""
try:
    import ujson as json
except ImportError:
    import json
import os
_settings_file = "settings_store.json"


class _Leaf():

    def __init__(self, initial_data=None, update_reducer=None, save_callback=None):
        if initial_data is None:
            initial_data = {}
        self._store = initial_data
        self._update_reducer = update_reducer
        self._save_callback = save_callback

    def update(self, data):
        """
        updates the data therefore the update_reducer is invoked and data dumped to flash drive
        """
        if self._update_reducer is None:
            return
        try:
            new_store = self._update_reducer(self._store, data)
        except:
            return
        self._store = new_store

        if self._save_callback is None:
            return
        self._save_callback()

    def get(self, key=None, default=None):
        """
        returns the contents of the leaf if a get is given only this subset is returned
        """
        if key is None:
            return self._store
        return self._store.get(key, default)


class _Store():

    def __init__(self):
        if _settings_file not in os.listdir():
            self._store = {}
        else:
            file_ptr = open(_settings_file, "r")
            try:
                self._store = json.loads(file_ptr.read())
            except ValueError:
                os.remove(_settings_file)
                # TODO log error
            finally:
                file_ptr.close()

    def _dump_data(self):
        """
        pickeles hole object to one dict
        :rtype: dict
        """
        return {key: value if type(value) == dict else value.get() for key, value in self._store.items()}

    def save(self):
        """stores all leafs to an json pickeled file"""
        # save config

        file_ptr = open(_settings_file, "w")
        try:
            file_ptr.write(json.dumps(self._dump_data()))
        finally:
            file_ptr.close()

    def register_leaf(self, key, initial_data, update_function):
        """
        registeres a new lead to store data
        :rtype initial_data: dict
        :param update_function: function with 2 parameter old_data, new_data
        """
        initial_data = self._store.get(key, initial_data)
        if isinstance(initial_data, _Leaf):
            return initial_data
        self._store[key] = _Leaf(
            initial_data,
            update_reducer=update_function,
            save_callback=self.save
        )

    def get_leaf(self, key):
        """
        retruns the current state of a leaf
        :rtype: _Leaf
        """
        leaf = self._store.get(key, {})
        if isinstance(leaf, dict):
            return _Leaf(leaf)
        return leaf


storage = _Store()
