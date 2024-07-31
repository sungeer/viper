from starlette.routing import Router

from touch.views.workflow import create_workflow

workflow_url = Router()

workflow_url.add_route('/', create_workflow, ['GET', 'POST'])
