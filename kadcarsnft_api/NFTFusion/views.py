import os
import django
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from NFTFusion.constants import *
from NFTFusion.render_factory import *
from NFTFusion.io_utils import *
from NFTFusion.pact_utils.command_utils import *
# Create your views here.

@api_view(['POST'])
def apply_upgrade(request):
    dirname = os.path.dirname(__file__)

    kadcar_id = request.data['kadcar_id']
    upgrade_id = request.data['upgrade_id']
    upgrade_type = request.data['upgrade_type']

    print(request.data)

    # handle_upgrade(kadcar_id, upgrade_id, upgrade_type)
    transforms_data = extract_data_from_json(os.path.join(dirname, "metadata_json/transforms.json"))
    json_data_dump = json.dumps(transforms_data)
    print(transforms_data)
    sign_using_pact_cli(transforms_data, upgrade_id)
    # send_transaction()

    return HttpResponse(json_data_dump, content_type='application/json')