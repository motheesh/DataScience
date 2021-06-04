class inSufficientDataError(ValueError):
    def __init__(self,**kwarg):
        self.error=kwarg["error"] or ""
        self.statusCode=kwarg["statusCode"] or ""
        self.errorType="InsufficientDataError"
        print("Data not valid error raised due to {}".format(kwarg))
        
class DbOperationError(ValueError):
    def __init__(self,**kwarg):
        self.error=kwarg["error"] or ""
        self.statusCode=kwarg["statusCode"] or ""
        self.errorType="DBOperation Error"
        print("Data not valid error raised due to {}".format(kwarg))