class Job:
    def __init__(self, token,
                 status='unknown', size=None, url=None, checksum=None,
                 ):
        self.token = token
        self.status = status
        self.size = size
        self.size = int(self.size) if isinstance(size, str) else size
        self.url = url
        self.checksum = checksum

    @property
    def is_ready(self):
        return self.status == 'complete'

    @property
    def is_processing(self):
        return self.status in {'enqueued', 'processing'}

    def __str__(self):
        return "Job {status}: {token}".format(status=self.status,
                                              token=self.token)
