class ApplicationError(Exception):
    pass


class UserNotFoundError(ApplicationError):
    pass


class UserActivatedError(ApplicationError):
    pass


class WeakPasswordError(ApplicationError):
    pass


class UserExistsError(ApplicationError):
    pass


class AccessDenied(ApplicationError):
    pass
