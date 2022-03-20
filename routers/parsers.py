from parsers import BoletaReader
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/parse")


class TxtNota(BaseModel):
    txt_nota: str


@router.post("/notab3/", tags=["parse"])
async def parse_nota_b3(texto_nota: TxtNota):
    print(texto_nota.txt_nota)
    return BoletaReader(texto_nota.txt_nota).read()
