import pyrobale

c = pyrobale.Client("1925697489:CwP34Ac3liEowK8sDa8hnelH5k5xhT2ezawwmGFo")

@c.on_message
def hello(message:pyrobale.Message,update,conditions:pyrobale.conditions):
    print(conditions.has_text())

c.run()