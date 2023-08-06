import json

from grebble_flow.managment.manager import FlowManager
from grebble_flow.transport.generated.sdk.v1 import processor_pb2_grpc
from grebble_flow.transport.generated.sdk.v1.processor_pb2 import (
    InitProcessorsRes,
    Processor,
    Desc,
    Parameter,
    RelationDesc,
    Package,
    Message,
    OnTriggerRes,
    TransferMessage,
)
from grebble_flow.processors import models
from grebble_flow.processors.session import Session


class ProcessorService(processor_pb2_grpc.ProcessorServiceServicer):
    def __init__(self, *args, **kwargs):
        self.flow_manager = FlowManager()

    def InitProcessors(self, request, context):
        processors = []
        for processor_class in self.flow_manager.get_all_processor_classes():
            processor = self.flow_manager.init_processor(processor_class)
            processor_desc: models.Desc = processor.get_description()
            package: models.Package = processor.get_package()
            parameters = [
                Parameter(
                    name=x.name, title=x.title, hint=x.hint, field_type=x.field_type,
                )
                for x in processor_desc.parameters
            ]
            p = Processor(
                desc=Desc(
                    title=processor_desc.title,
                    description=processor_desc.description,
                    group=processor_desc.group,
                    parameters=parameters,
                    relations=[
                        RelationDesc(name=x.name,) for x in processor_desc.relations
                    ],
                ),
                package=Package(name=package.name, version=package.version),
            )
            processors += [p]

        resp = InitProcessorsRes(processors=processors)
        return resp

    def OnTrigger(self, request, context):
        flow_name = request.flow_name
        processor = self.flow_manager.find_processor_instance_by_name(flow_name)

        m: models.Message = None
        if request.Message is not None:

            attributes = request.Message.attributes

            try:
                attributes = json.loads(request.Message.attributes)
            except:
                pass

            m = models.Message(
                id=request.Message.id,
                parent_id=request.Message.parent_id,
                content_type=request.Message.content_type,
                attributes=attributes,
                content=request.Message.content,
            )

        settings = processor.settings.from_json(request.settings.decode("utf-8"))
        for item in processor.on_trigger(Session(m), settings):
            relation_name = item[1]
            message = item[0]
            attr = json.dumps(message.attributes)
            transfer_message = TransferMessage(
                relation_name=relation_name,
                message=Message(
                    id=message.id,
                    parent_id=message.parent_id,
                    content_type=message.content_type,
                    attributes=bytes(attr, "utf-8"),
                    content=message.content,
                ),
            )
            yield OnTriggerRes(transfer_message=transfer_message)
