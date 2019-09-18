from grown.store import _Store, _Leaf


class MockStore(_Store):

    def __init__(self):
        # we will not load from file this was normal python will be able to test
        self._store = {}


def test_leaf():
    leaf = _Leaf()
    assert leaf.get() == {}


def test_leaf_initial_data():
    leaf = _Leaf({"tada": 1})
    assert leaf.get() == {"tada": 1}


def test_leaf_update():
    leaf = _Leaf({"tada": 1})
    leaf.update({"smth": 0})
    assert leaf.get() == {"smth": 0}


def test_leaf_update_with_reducer():
    def update(old_data, new_data):
        new_data.update(old_data)
        return new_data

    leaf = _Leaf({"tada": 1}, update)
    leaf.update({"smth": 0})
    assert leaf.get() == {"smth": 0, "tada": 1}


def test_leaf_update_with_reducer_and_save():
    def update(old_data, new_data):
        new_data.update(old_data)
        return new_data

    execute = 0

    def save():
        nonlocal execute
        execute += 1

    leaf = _Leaf({"tada": 1}, update, save)
    leaf.update({"smth": 0})
    assert leaf.get() == {"smth": 0, "tada": 1}
    assert execute == 1


def test_leaf_get_key_and_default():
    leaf = _Leaf({"tada": 1})
    assert leaf.get("tada", "bla") == 1
    assert leaf.get("tada1", "bla") == "bla"


def test_leaf_get_only_key():
    leaf = _Leaf({"tada": 1})
    assert leaf.get("tada") == 1
    assert leaf.get("tada1") is None


def test_leaf_get():
    leaf = _Leaf({"tada": 1})
    assert leaf.get() == {"tada": 1}


def create_mock_store():
    def update(old_data, new_data):
        old_data.update(new_data)
        return old_data

    storage = MockStore()
    storage.register_leaf('tada', {"smth": 2}, update)
    return storage


def test_store_get_leaf_without_register():
    storeage = create_mock_store()
    lose_leaf = storeage.get_leaf("new")
    assert lose_leaf.get() == {}


def test_store_get_leaf_with_register():
    storeage = create_mock_store()
    leaf = storeage.get_leaf("tada")
    assert leaf.get() == {"smth": 2}


def test_store_update_via_leaf():
    storeage = create_mock_store()
    leaf = storeage.get_leaf("tada")
    leaf.update({"smth": 1})
    assert leaf.get() == {"smth": 1}
    data_dump = storeage._dump_data()
    assert data_dump == {'tada': {"smth": 1}}


def test_store_dump_data_multiple_leafs():
    storeage = create_mock_store()
    leaf1 = storeage.get_leaf("tada")
    leaf2 = storeage.get_leaf("tada")
    leaf1.update({"smth": 1})
    assert leaf1.get() == {"smth": 1}
    assert leaf2.get() == {"smth": 1}
    leaf3 = storeage.get_leaf("tada")
    assert leaf3.get() == {"smth": 1}
