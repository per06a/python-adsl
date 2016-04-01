
"""
Implementations of the Map interface

"""

class Map(object):

    def put(self, key, value):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def __setitem__(self, k, v):
        return self.put(k, v)

    def __getitem__(self, k):
        return self.get(k)

    def __delitem__(self, k):
        return self.delete(k)

class HashMap(Map):

    def __init__(self):
        self.num_buckets = 32
        self.num_elems = 0
        # Ratio of elements per bucket before we expand
        self.expand_threshold = 0.75
        # Ratio of elements per bucket before we contract
        self.contract_threshold = 0.25
        
        self.buckets = [None for x in range(self.num_buckets)]

    def get_index(self, elem):
        return hash(elem) % self.num_buckets

    def expand(self):
        self.num_buckets *= 2
        buckets = [None for x in range(0, self.num_buckets)]
        obuckets = self.buckets
        self.buckets = buckets
        
        for bucket in obuckets:
            if bucket is not None:
                for (k, v) in bucket:
                    self.put(k, v)

        del(obuckets)

    def contract(self):
        self.num_buckets /= 2
        buckets = [None for x in range(0, self.num_buckets)]
        obuckets = self.buckets
        self.buckets = buckets
        
        for bucket in obuckets:
            if bucket is not None:
                for (k, v) in bucket:
                    self.put(k, v)

        del(obuckets)

    def put(self, key, value):
        if (self.num_elems / float(self.num_buckets)) >= self.expand_threshold:
            self.expand()

        index = self.get_index(key)
        bucket = self.buckets[index]

        if bucket is None:
            bucket = []
            self.buckets[index] = bucket

        pos = None
        for i in range(0, len(bucket)):
            (k, v) = bucket[i]

            if k == key:
                pos = i
                break

        if pos is None:
            bucket.append((key, value))
            self.num_elems += 1

        else:
            bucket[pos] = (key, value)

    def get(self, key):
        
        index = self.get_index(key)
        bucket = self.buckets[index]

        if bucket is None:
            raise KeyError(str(key))

        value = None
        for (k, v) in bucket:
            if k == key:
                value = v
                break

        if value is None:
            raise KeyError(str(key))

        return value

    def delete(self, key):
        if (self.num_elems / float(self.num_buckets)) <= self.contract_threshold:
            self.contract()

        index = self.get_index(key)
        bucket = self.buckets[index]

        if bucket is None:
            raise KeyError(str(ex))

        pos = None

        for i in range(0, len(bucket)):
            (k, v) = bucket[i]
            if k == key:
                pos = i
                break

        if pos is None:
            raise KeyError(str(key))

        del(bucket[pos])

        self.num_elems -= 1

class TreeMap(Map):

    def __init__(self):
        self.root = None

    def put(self, key, value):
        pass

    def get(self, key):
        pass

    def delete(self, key):
        pass
