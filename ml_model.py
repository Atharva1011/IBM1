
# Insert here the initialization code as outlined on this page:
# https://docs.clarifai.com/api-guide/api-overview/api-clients#client-installation-instructions
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2

# Construct the communications channel 
channel = ClarifaiChannel.get_grpc_channel()
# Construct the V2Stub object for accessing all the Clarifai API functionality
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + '802ddba8a98a4f2fb814596bf165a327'),)

userDataObject = resources_pb2.UserAppIDSet(user_id='vaishnavi717', app_id='food-identifier')

def food_identifier(string):
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
            model_id="food-item-v1-recognition",  # This is model ID of the clarifai/main General model.
            version_id="dfebc169854e429086aceb8368662641",  # This is optional. Defaults to the latest model version.
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            # url="https://samples.clarifai.com/metro-north.jpg"
                            # url="https://cdn4.singleinterface.com/files/banner_images/1093/2204_1602668149_CountryFeastmin.jpg"
                            # url="https://upload.wikimedia.org/wikipedia/commons/c/cb/Samosachutney.jpg"
                            # url="https://cdn1.foodviva.com/static-content/food-images/snacks-recipes/pani-puri/pani-puri.jpg"
                            
                            # url="https://nutripqrst.000webhostapp.com/uploads/salad.jpg"
                            url = "./static/uploads/cherry.jpg"

                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print("There was an error with your request!")
        print("\tCode: {}".format(post_model_outputs_response.outputs[0].status.code))
        print("\tDescription: {}".format(post_model_outputs_response.outputs[0].status.description))
        print("\tDetails: {}".format(post_model_outputs_response.outputs[0].status.details))
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here.
    output = post_model_outputs_response.outputs[0]
    print(output)

    # print("Predicted concepts:")
    # for concept in output.data.concepts:
    #     print("\t%s %.2f" % (concept.name, concept.value))

    
    return output.data.concepts[0].name
