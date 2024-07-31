from starlette.responses import JSONResponse

from touch.models.workflow import WorkflowModel


async def create_workflow(request):
    # data = await request.json()
    # params = {
    #     'name': data['workflow_name'],
    #     'desc': data['desc']
    # }
    # workflow_id = await WorkflowModel().add_workflow(params)
    return JSONResponse({'workflow_id': 'qaz'})
