import aws_cdk as core
import aws_cdk.assertions as assertions

from tarea1.tarea1_stack import Tarea1Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in tarea1/tarea1_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Tarea1Stack(app, "tarea1")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
