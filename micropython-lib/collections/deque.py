class deque:

    def __init__(self, iterable=None, maxlen=None):
        self.maxlen = maxlen
        if iterable is None:
            self.q = []
        else:
            self.q = list(iterable)

    def popleft(self):
        return self.q.pop(0)

    def popright(self):
        return self.q.pop()

    def pop(self):
        return self.q.pop()

    def append(self, a):
        self.q.append(a)
        if self.maxlen is not None and len(self.q) > self.maxlen:
            self.popleft()

    def appendleft(self, a):
        self.q.insert(0, a)
        if self.maxlen is not None and len(self.q) > self.maxlen:
            self.pop()

    def extend(self, iterable):
        self.q.extend(iterable)

    def extendleft(self, iterable):
        for a in iterable:
            self.appendleft(a)

    def clear(self):
        self.q.clear()

    def __len__(self):
        return len(self.q)

    def __bool__(self):
        return bool(self.q)

    def __iter__(self):
        yield from self.q

    def __str__(self):
        return 'deque({0}{1})'.format(
            self.q,
            '' if self.maxlen is None else ', maxlen={0}'.format(self.maxlen)
        )
