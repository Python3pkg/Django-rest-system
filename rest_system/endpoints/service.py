import json

from django.conf import settings

class service():
    methods = []

    user = None

    request = None
    action = None

    input_data = None

    result = {
        "code": 500,
        "result": {},
        "errors": []
    }

    def requires_action(self):
        return self.Meta.requires_action

    def requires_auth(self):
        return self.Meta.requires_auth

    def getInput(self):
        return self.input_data

    def getInputJson(self):
        print(self.input_data.decode("utf-8"))
        try:
            return json.loads(self.input_data.decode("utf-8"))
        except AttributeError:
            return self.input_data.dict()
        except ValueError:
            return json.loads("{}")

    def getMethods(self):
        return self.Meta.methods

    def getResult(self):
        return self.result

    def setResult(self, result):
        self.result["result"] = result

    def getCode(self):
        return self.result["code"]

    def setCode(self, code):
        self.result["code"] = code

    def addError(self, error):
        self.result["errors"].append(error)

    def addErrorJson(self, error):
        self.result["errors"].append(json.loads(error))

    def __init__(self, request, action):
        self.result = {
            "code": 500,
            "result": {},
            "errors": []
        }

        self.request = request
        self.action = action

        if self.request.method == "GET":
            self.input_data = self.request.GET
        else:
            self.input_data = self.request.body

    def setUser(self, user):
        self.user = user

    def process(self):
        if self.requires_action:
            if settings.DEBUG:
                self.setCode(getattr(self, str(self.request.method.lower() + "_" + self.action))())
            else:
                try:
                    self.setCode(getattr(self, str(self.request.method.lower() + "_" + self.action))())
                except AttributeError:
                    self.addError("not found")
                    self.setCode(404)
        else:
            try:
                self.setCode(getattr(self, str(self.request.method.lower() + "_process"))())
            except AttributeError:
                self.addError("not found")
                self.setCode(404)