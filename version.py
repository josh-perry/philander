class Version:
    def __init__(self, version: str):
        assert(version)

        self.version_str = version
        self.split_version = version.split(".")

    def major(self) -> int:
        return self.split_version[0]

    def minor(self) -> int:
        return self.split_version[1]

    def patch(self) -> int:
        return self.split_version[2]

    def __str__(self):
        return self.version_str
