from semver import VersionInfo


class Version:
    def __init__(self, version :str):
        self._version_string = version.lstrip('=') if version.startswith('=') else version
        self._version_info   = None

    @property
    def version(self) -> VersionInfo:
        if self._version_info is None:
            # Note: Some packages have invalid versions like '2.0'. This
            # attempts to reconcile that by converting those to '0.2.0'.
            # Adding a prefix ensures that a future release of '1.0.0' would
            # be greater than '2.0' (ie: '1.0.0' > '0.2.0').
            if len(self._version_string.split('.')) < 3:
                self._version_string = f'0.{self._version_string}'

            self._version_info = VersionInfo.parse(self._version_string)

        return self._version_info

    def __gt__(self, o :'Version'):
        return self.version.compare(o.version) > 0

    def __lt__(self, o :'Version'):
        return self.version.compare(o.version) < 0

    def __eq__(self, o :'Version'):
        return self.version.compare(o.version) == 0

    def __str__(self):
        return self._version_string
