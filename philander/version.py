class Version:
    def __init__(self, version: str):
        assert(version)

        self.version_str = version
        self.split_version = version.split(".")

        self.major = self.major()
        self.minor = self.minor()

        if len(self.split_version) > 2:
            self.patch = self.patch()

    def major(self) -> int:
        return int(self.split_version[0])

    def minor(self) -> int:
        return int(self.split_version[1])

    def patch(self) -> int:
        return int(self.split_version[2])

    def __str__(self):
        return self.version_str
