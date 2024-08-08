from viper.models.workflow import WorkflowModel
from viper.utils.tools import jsonify


async def create_workflow(request):
    data = await request.json()
    params = {
        'name': data['workflow_name'],
        'desc': data['desc']
    }
    workflow_id = await WorkflowModel().add_workflow(params)
    data = {'workflow_id': workflow_id}
    return jsonify(data)
