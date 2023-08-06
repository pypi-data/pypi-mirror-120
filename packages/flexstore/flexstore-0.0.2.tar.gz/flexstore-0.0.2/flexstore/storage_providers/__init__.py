import os
import io
import boto3
from redis import Redis

# TODO: add logging

class StorageProvider:
    """ The base class that provides storage methods for all StorageProviders. """
    def __init__(self):
        pass

    def commit(self):
        raise NotImplementedError("you must implement a commit method")
    
    def __del__(self):
        pass

class RedisProvider(StorageProvider):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __init__(self, key, *args, **kwargs):
        """ setup the storage provider. """
        self.key = key
        self.r = Redis(**kwargs)
        self.r.ping()
    
    def load(self):
        """ load the state of the dictionary from the given key """
        return self.r.get(self.key)

    def commit(self, state: bytes):
        """ commit the state of the dictionary. """
        self.r.set(self.key, state)

    def __del__(self):
        """ teardown the storage provider. """
        pass

class InMemory(StorageProvider):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __init__(self):
        """ setup the storage provider. """
        self.fp = io.BytesIO()
    
    def load(self):
        """ load the state """
        return None

    def commit(self, state: bytes):
        """ commit the state of the dictionary. """
        self.fp.write(state)

    def __del__(self):
        """ teardown the storage provider. """
        self.fp.close()

class LocalFile(StorageProvider):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __init__(self, path):
        """ setup the storage provider. """
        self.path = path
    
    def load(self):
        """ load the state """
        if os.path.isfile(self.path):
            f = open(self.path, 'rb+')
            return f.read()

    def commit(self, state: bytes):
        """ commit the state of the dictionary. """
        self.fp = open(self.path, 'wb+')
        self.fp.write(state)
        self.fp.close()

    def __del__(self):
        """ teardown the storage provider. """
        pass

class S3Bucket(StorageProvider):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __init__(self, bucket, key):
        """ setup the storage provider. """
        # TODO: add more options for configuring
        # credentials.
        self.s3client = boto3.client('s3')
        self.s3resource = boto3.resource('s3')
        self.bucket = bucket
        self.key = key
    
    def load(self):
        """ load the state of the dictionary. """
        try:
            response = self.s3client.get_object(Bucket=self.bucket, Key=self.key)
            return response.get('Body').read()
        except self.s3resource.meta.client.exceptions.NoSuchKey:
            return None
        # TODO: handle other error edge cases
        # like no permissions, etc.        

    def commit(self, state):
        """ commit the state of the dictionary. """
        # TODO: add error handling around this request
        response = self.s3client.put_object(
            Bucket=self.bucket,
            Key=self.key,
            Body=state
        )

    def __del__(self):
        """ teardown the storage provider. """
        pass