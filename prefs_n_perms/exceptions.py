

class PrefsNPermsException(Exception):
    detail_default = 'An exception occurred with Preferences and Permissions'

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = str(detail)
        else:
            self.detail = str(self.detail_default)

    def __str__(self):
        return self.detail


class ReadOnlyException(PrefsNPermsException):
    detail_default = 'Cannot write to read-only settings'


class InvalidInstancesException(PrefsNPermsException):
    detail_default = 'Invalid instance(s): {instances}'

    def __init__(self, instances, detail=None):
        if detail is not None:
            self.detail = str(detail)
        else:
            instances = ', '.join(list(instances))
            self.detail = self.detail_default.format(instances=instances)


class MissingInstancesException(InvalidInstancesException):
    default_detail = 'Missing instance(s): {instances}'


class ExtraInstancesException(InvalidInstancesException):
    default_detail = 'Extra instance(s): {instances}'


class GlobalVariableException(PrefsNPermsException):
    detail_default = 'Can not set global variable'


class SectionAlreadyRegisteredException(PrefsNPermsException):
    detail_default = 'This section has already been registered'


class SectionNotRegisteredException(PrefsNPermsException):
    detail_default = 'This section has not been registered'


class TierAlreadyRegisteredException(PrefsNPermsException):
    detail_default = 'This tier has already been registered'
