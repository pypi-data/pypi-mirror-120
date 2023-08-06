import fnmatch
import msgpack

class Store(dict):
    """ Dictionary Store """
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def __init__(self, StorageProvider, *args, **kwargs):
        self.storage_provider = StorageProvider
        if not hasattr(self.storage_provider, 'commit'):
            # TODO: create custom exception type
            raise Exception("the provided storage provider is invalid")
        
        # NOTE: this pulls in the entire state of the dictionary.
        # TODO: provide a way to select the desired keys and only
        # load the dictionary with the desired keys.
        state = self.storage_provider.load()
        if state is not None:
            self.update(**msgpack.unpackb(state, raw=False))

    def commit(self):
        """ persist the state of this dictionary
        to the configured storage provider dest. """
        self.storage_provider.commit(msgpack.packb(self, use_bin_type=True))

    def scan(self, prefix):
        """ returns a list of keys that match the given prefix. """
        matches = []
        for key in self.keys():
            if fnmatch.fnmatch(key, prefix):
                matches.append(key)
        return matches

    def __del__(self):
        """ teardown our instance """
        pass
