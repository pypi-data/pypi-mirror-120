from pathlib import Path
from enum import Enum
from typing import Optional, List, Any

from fastapi import Header, File, UploadFile, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .saberes import Saber, SaberesConfig
from .sankofa import Sankofa
from .rest import BaobaxiaAPI

from configparser import ConfigParser

class MidiaTipo(str, Enum):
    video = 'video'
    audio = 'audio'
    imagem = 'imagem'
    arquivo = 'arquivo'

class Midia(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    tipo: Optional[MidiaTipo] = None
    tags: List[str] = []
    arquivo: Optional[str] = None

pastas_por_tipo = {
    MidiaTipo.video: 'videos',
    MidiaTipo.audio: 'audios',
    MidiaTipo.imagem: 'imagens',
    MidiaTipo.arquivo: 'arquivos',
}

tipos_por_content_type = {
    'application/ogg': MidiaTipo.audio,
    'audio/ogg': MidiaTipo.audio,
    'audio/mpeg': MidiaTipo.audio,
    'image/jpeg': MidiaTipo.imagem,
    'image/png': MidiaTipo.imagem,
    'image/gif': MidiaTipo.imagem,
    'video/ogg': MidiaTipo.video,
    'video/ogv': MidiaTipo.video,
    'video/avi': MidiaTipo.video,
    'video/mp4': MidiaTipo.video,
    'video/webm': MidiaTipo.video,
    'application/pdf': MidiaTipo.arquivo,
    'application/odt': MidiaTipo.arquivo,
    'application/ods': MidiaTipo.arquivo,
    'application/odp': MidiaTipo.arquivo,
}

api = BaobaxiaAPI()

base_path = api.baobaxia.config.data_path / \
    api.baobaxia.config.balaio_local / \
    api.baobaxia.config.mucua_local

acervo_path = base_path / 'acervo'
if not acervo_path.exists():
    acervo_path.mkdir()
for tipo, pasta in pastas_por_tipo.items():
    pasta_path = acervo_path / pasta
    if not pasta_path.exists():
        pasta_path.mkdir()

saberes_patterns = []
for pattern in pastas_por_tipo.values():
    saberes_patterns.append('acervo/'+pattern+'/*/')
api.baobaxia.discover_saberes(
    balaio_slug=api.baobaxia.config.balaio_local,
    mucua_slug=api.baobaxia.config.mucua_local,
    model=Midia,
    patterns=saberes_patterns)

api.add_saberes_api(
    Midia,
    url_path='/acervo/midia',
    skip_post_method=True,
    put_summary='Atualizar informações da mídia',
    get_summary='Retornar informações da mídia')

async def post_midia(name: str, midia_data: Midia, token: str = Header(...)) -> Saber:
    return api.baobaxia.put_midia(
        path=Path('acervo') / pastas_por_tipo[midia_data.tipo],
        name=name,
        data=midia_data,
        slug_dir=True,
        token=token)
api.add_api_route('/acervo/midia', post_midia, response_model=Saber,
                  methods=['POST'],
                  summary='Enviar as informações de uma mídia')

async def upload_midia(*, balaio: str, mucua: str, path: Path, arquivo: UploadFile = File(...), token: str = Header(...)):
    saber = api.baobaxia.get_midia(path, token=token)
    if saber.data.arquivo is not None:
        raise HTTPException(status_code=400, detail='Mídia duplicada')
    saber.data.arquivo = arquivo.filename
    with (base_path / saber.path / saber.data.arquivo).open(
            'wb') as arquivo_saber:
        arquivo_saber.write(arquivo.file.read())
        arquivo_saber.close()
        api.baobaxia.put_midia(balaio=balaio, mucua=mucua, path=path, token=token)
    return {'detail': 'success'}
api.add_api_route('/acervo/upload/{balaio}/{mucua}/{path:path}', upload_midia,
                  response_model=dict, methods=['POST'],
                  summary='Enviar o arquivo uma mídia já existente')

async def download_midia(balaio: str, mucua: str, path: Path):
    saber = api.baobaxia.saberes[balaio][mucua]['midia'][path]
    return FileResponse(path=str(base_path / saber.path / saber.data.arquivo))
api.add_api_route('/acervo/download/{balaio}/{mucua}/{path:path}', download_midia,
                  methods=['GET'],
                  summary='Retornar o arquivo de uma mídia')

async def find_midias(*,
                      balaio: str, mucua: str,
                      keywords: Optional[str] = None,
                      hashtags: Optional[List[str]] = Query(None),
                      tipos: Optional[List[MidiaTipo]] = Query(None),
                      ordem_campo: Optional[str] = None,
                      ordem_decrescente: bool = False,
                      pag_tamanho: int = 12,
                      pag_atual: int = 1,
                      token: Optional[str] = Header(None)):
    def filter_function(midia):
        if tipos is not None and len(tipos) > 0 and midia.data.tipo not in tipos:
            return False
        if keywords is not None and len(keywords) > 0:
            has_keyword = False
            for kw in keywords.split():
                if kw in midia.data.titulo or kw in midia.data.descricao:
                    has_keyword = True
                    break
            if not has_keyword:
                return False
        if hashtags is not None and len(hashtags) > 0:
            has_hashtag = False
            for ht in hashtags:
                if ht in midia.data.tags:
                    has_hashtag = True
                    break
            if not has_hashtag:
                return False
        return True

    def sorted_function(midia):
        if ordem_campo is None:
            return 0
        elif hasattr(midia, ordem_campo):
            return getattr(midia, ordem_campo)
        elif hasattr(midia.data, ordem_campo):
            return getattr(midia.data, ordem_campo)
        else:
            return 0

    result = api.baobaxia.find_midias(
        filter_function=filter_function,
        sorted_function=sorted_function,
        sorted_reverse=ordem_decrescente,
        token=token)

    pag_index = pag_atual - 1
    pag_first = pag_index * pag_tamanho
    pag_last = pag_first + pag_tamanho
    if pag_first > len(result):
        return []
    if pag_last > len(result):
        pag_last = len(result)
    return result[pag_first:pag_last]
api.add_api_route('/acervo/find/{balaio}/{mucua}', find_midias,
                  response_model=List[Saber], methods=['GET'],
                  summary='Busca mídias de acordo com os parâmetros fornecidos')

async def get_tipos_por_content_type():
    return tipos_por_content_type
api.add_api_route('/acervo/tipos_por_content_type',
                  get_tipos_por_content_type, response_model=dict,
                  methods=['GET'],
                  summary='Retornar os content types aceitos e ' + \
                  'os tipos de mídia correspondentes para o json')

