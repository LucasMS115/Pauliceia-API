from typing import Optional

from fastapi import APIRouter

from app.managers.vgi.layer_magager import get_layers
from app.models.vgi_models import Layer
from app.routers.vgi.error_response_examples import get_layers_error_responses

router = APIRouter(prefix="/vgi/layers", tags=["VGI - layers"])


@router.get('', response_model=list[Layer], responses={**get_layers_error_responses})
async def layers(layer_id: Optional[int] = None):
    return get_layers(layer_id)

