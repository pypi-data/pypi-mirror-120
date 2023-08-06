from pathlib import Path
from typing import Optional, List, Any

from fastapi import FastAPI, Header, Form, HTTPException

from pydantic import BaseModel, Field

from .saberes import (
    Saber,
    SaberesConfig,
    Balaio,
    Mocambola
)
from .root import Baobaxia, BaobaxiaError

from configparser import ConfigParser

class BaobaxiaAPI(FastAPI):

    def __init__(
            self,
            config: Optional[SaberesConfig] = None,
            prefix: Optional[str] = None,
            tags: Optional[List[str]] = None,
            **kwargs: Any) -> None:
        super().__init__(prefix=prefix, tags=tags, **kwargs)
        self.baobaxia = Baobaxia()

        super().add_api_route(
            '/auth/{balaio}/{mucua}',
            self.authenticate,
            methods=['POST'],
            response_model=str,
            summary='Autenticar mocambola')
        super().add_api_route(
            '/recover/{balaio}/{mucua}',
            self.recover,
            methods=['POST'],
            response_model=str,
            summary='Recuperar mocambola')
        super().add_api_route(
            '/balaio',
            self.list_balaios,
            methods=['GET'],
            response_model=List[Saber],
            summary='Listar balaios')
        super().add_api_route(
            '/balaio',
            self.post_balaio,
            methods=['POST'],
            response_model=Saber,
            summary='Criar um novo balaio')
        super().add_api_route(
            '/balaio/{balaio}',
            self.get_balaio,
            methods=['GET'],
            response_model=Saber,
            summary='Retornar um balaio')
        super().add_api_route(
            '/balaio/{balaio}',
            self.put_balaio,
            methods=['PUT'],
            response_model=Any,
            summary='Atualizar um balaio')
        super().add_api_route(
            '/balaio/{balaio}',
            self.del_balaio,
            methods=['DELETE'],
            summary='Deletar um balaio')
        super().add_api_route(
            '/mucua/{balaio}',
            self.list_mucuas,
            methods=['GET'],
            response_model=List[Saber],
            summary='Listar mucuas')
        super().add_api_route(
            '/mucua/{balaio}',
            self.post_mucua,
            methods=['POST'],
            response_model=Saber,
            summary='Criar uma nova mucua')
        super().add_api_route(
            '/mucua/{balaio}/{mucua}',
            self.get_mucua,
            methods=['GET'],
            response_model=Saber,
            summary='Retornar uma mucua')
        super().add_api_route(
            '/mucua/{balaio}/{mucua}',
            self.put_mucua,
            methods=['PUT'],
            response_model=Saber,
            summary='Atualizar uma mucua')
        super().add_api_route(
            '/mucua/{balaio}/{mucua}',
            self.del_mucua,
            methods=['DELETE'],
            summary='Deletar uma mucua')
        super().add_api_route(
            '/mocambola/{balaio}/{mucua}',
            self.list_mocambolas,
            methods=['GET'],
            response_model=List[Mocambola],
            summary='Listar mocambolas')
        super().add_api_route(
            '/mocambola/{balaio}/{mucua}',
            self.post_mocambola,
            methods=['POST'],
            response_model=Mocambola,
            summary='Criar um novo mocambola')
        super().add_api_route(
            '/mocambola/{balaio}/{mucua}/{username}',
            self.get_mocambola,
            methods=['GET'],
            response_model=Mocambola,
            summary='Retornar um mocambola')
        super().add_api_route(
            '/mocambola/{balaio}/{mucua}/{username}',
            self.put_mocambola,
            methods=['PUT'],
            response_model=Mocambola,
            summary='Atualizar um mocambola')
        super().add_api_route(
            '/mocambola/{balaio}/{mucua}/{username}',
            self.del_mocambola,
            methods=['DELETE'],
            summary='Deletar um mocambola')
        super().add_api_route(
            '/mocambola/password',
            self.set_password,
            methods=['POST'],
            summary='Atualiza a senha do mocambola autenticado')
        return

    def add_saberes_api(self, model: type, **kwargs):
        if 'field_name' in kwargs and kwargs['field_name'] is not None:
            field_name = kwargs['field_name']
        else:
            field_name = model.__name__.lower()
        if 'list_field_name' in kwargs and kwargs['list_field_name'] is not None:
            list_field_name = kwargs['list_field_name']
        else:
            list_field_name = field_name + 's'

        if 'url_path' in kwargs:
            url_path = kwargs['url_path']
        else:
            url_path = '/'+field_name

        if 'list_summary' in kwargs:
            summary = kwargs['list_summary']
        else:
            summary = 'Listar '+list_field_name
        if 'list_url' in kwargs:
            list_url = kwargs['list_url']
        else:
            list_url = url_path  + '/{balaio}/{mucua}'
        if 'list_method' in kwargs and callable(kwargs['list_method']):
            super().add_api_route(
                list_url,
                kwargs['list_method'],
                response_model=List[Saber],
                methods=['GET'],
                summary=summary)
        elif 'skip_list_method' not in kwargs:
            def list_rest_template(token: Optional[str] = Header(None)):
                return getattr(self.baobaxia, 'list_'+list_field_name)(token=token)
            super().add_api_route(
                list_url,
                list_rest_template,
                response_model=List[Saber],
                methods=['GET'],
                summary=summary)

        if 'post_summary' in kwargs:
            summary = kwargs['post_summary']
        else:
            summary = 'Criar '+field_name
        if 'post_url' in kwargs:
            post_url = kwargs['post_url']
        else:
            post_url = url_path+'/{balaio}/{mucua}/{path:path}'
        if 'post_method' in kwargs and callable(kwargs['post_method']):
            super().add_api_route(
                post_url,
                kwargs['post_method'],
                response_model=Saber,
                methods=['POST'],
                summary=summary)
        elif 'skip_post_method' not in kwargs:
            def post_rest_template(path: Path, name: str, data: model, token: str = Header(...)):
                return getattr(self.baobaxia, 'put_'+field_name)(
                    path=path,
                    name=name,
                    data=data,
                    slug_dir=True,
                    token=token)
            super().add_api_route(
                post_url,
                post_rest_template,
                response_model=Saber,
                methods=['POST'],
                summary=summary)

        if 'get_summary' in kwargs:
            summary = kwargs['get_summary']
        else:
            summary = 'Retornar '+field_name
        if 'get_url' in kwargs:
            get_url = kwargs['get_url']
        else:
            get_url = url_path+'/{balaio}/{mucua}/{path:path}'
        if 'get_method' in kwargs and callable(kwargs['get_method']):
            super().add_api_route(
                get_url,
                kwargs['get_method'],
                response_model=Saber,
                methods=['GET'],
                summary=summary)
        elif 'skip_get_method' not in kwargs:
            def get_rest_template(path: Path, token: str = Header(...)):
                return getattr(self.baobaxia, 'get_'+field_name)(
                    path=path, token=token)
            super().add_api_route(
                get_url,
                get_rest_template,
                response_model=Saber,
                methods=['GET'],
                summary=summary)

        if 'put_summary' in kwargs:
            summary = kwargs['put_summary']
        else:
            summary = 'Atualizar '+field_name
        if 'put_url' in kwargs:
            put_url = kwargs['put_url']
        else:
            put_url = url_path+'/{balaio}/{mucua}/{path:path}'
        if 'put_method' in kwargs and callable(kwargs['put_method']):
            super().add_api_route(
                put_url,
                kwargs['put_method'],
                response_model=Saber,
                methods=['PUT'],
                summary=summary)
        elif 'skip_put_method' not in kwargs:
            def put_rest_template(*, path: Path,
                                  name: Optional[str] = None,
                                  data: Optional[model] = None,
                                  token: str = Header(...)):
                return getattr(self.baobaxia, 'put_'+field_name)(
                    path=path,
                    name=name,
                    data=data,
                    token=token)
            super().add_api_route(
                put_url,
                put_rest_template,
                response_model=Saber,
                methods=['PUT'],
                summary=summary)

        if 'del_summary' in kwargs:
            summary = kwargs['del_summary']
        else:
            summary = 'Deletar '+field_name
        if 'del_url' in kwargs:
            del_url = kwargs['del_url']
        else:
            del_url = url_path+'/{balaio}/{mucua}/{path:path}'
        if 'del_method' in kwargs and callable(kwargs['del_method']):
            super().add_api_route(
                del_url,
                kwargs['del_method'],
                methods['DELETE'],
                summary=summary)
        elif 'skip_del_method' not in kwargs:
            def del_rest_template(path: Path, token: str = Header(...)):
                getattr(self.baobaxia, 'del_'+field_name)(
                    path=path, token=token)
                return
            super().add_api_route(
                del_url,
                del_rest_template,
                methods=['DELETE'],
                summary=summary)

    async def authenticate(self, *,
                           balaio: str,
                           mucua: str,
                           username: str = Form(...),
                           password: str = Form(...)):
        try:
            result = self.baobaxia.authenticate(
                balaio, mucua, username, password)
            return result
        except BaobaxiaError:
            raise HTTPException(status_code=400, detail="Erro de autenticação.")

    async def recover(self, *,
                      balaio: str,
                      mucua: str,
                      username: str = Form(...),
                      recovery_answer: str = Form(...)):
        return self.baobaxia.authenticate(
            balaio, mucua, username,
            recovery_answer = recovery_answer)

    async def list_balaios(self, token: str = Header(None)):
        return self.baobaxia.list_balaios(token=token)
    async def post_balaio(self, name: str, default_mucua: str, token: str = Header(...)):
        return self.baobaxia.put_balaio(name=name, default_mucua=default_mucua, token=token)
    async def get_balaio(self, balaio: str, token: str = Header(None)):
        return self.baobaxia.get_balaio(balaio, token=token)
    async def put_balaio(self, balaio: str,
                         name: str = Form(None), 
                         default_mucua: str = Form(None),
                         token: str = Header(...)):
        return self.baobaxia.put_balaio(
            slug=balaio,
            name=name,
            default_mucua=default_mucua,
            token=token)
    async def del_balaio(self, balaio: str, token: str = Header(...)):
        self.baobaxia.del_balaio(balaio, token=token)
        return

    async def list_mucuas(self, balaio: str, token: str = Header(None)):
        return self.baobaxia.list_mucuas(balaio, token=token)
    async def post_mucua(self, balaio: str, name: str, token: str = Header(...)):
        return self.baobaxia.put_mucua(balaio_slug=balaio, name=name, token=token)
    async def get_mucua(self, balaio: str, mucua: str, token: str = Header(None)):
        return self.baobaxia.get_mucua(balaio_slug, mucua_slug, token=token)
    async def put_mucua(self, balaio: str, mucua: str, name: str, token: str = Header(...)):
        return self.baobaxia.put_mucua(
            balaio_slug=balaio,
            mucua_slug=mucua,
            name=name, token=token)
    async def del_mucua(self, balaio: str, mucua: str, token: str = Header(...)):
        self.baobaxia.del_mucua(balaio, mucua, token=token)
        return
    async def set_password(
            self, *,
            new_password: str = Form(...),
            password: Optional[str] = Form(None),
            recovery_answer: Optional[str] = Form(None),
            token: str = Header(...)):
        return self.baobaxia.set_password(
            new_password = new_password,
            password = password,
            recovery_answer = recovery_answer,
            token = token
        )
    async def list_mocambolas(self, *,
                        balaio: str,
                        mucua: str,
                        token: str = Header(...)):
        return self.baobaxia.list_mocambolas(
            balaio, mucua, token)
    async def get_mocambola(self, *,
                      balaio: str,
                      mucua: str,
                      username: str,
                      token: str = Header(...)):
        return self.baobaxia.get_mocambola(
            balaio, mucua, username, token)
    async def post_mocambola(self, *,
                      balaio: str,
                      mucua: str,
                      mocambola: Mocambola,
                      recovery_answer: str,
                      token: str = Header(...)):
        return self.baobaxia.put_mocambola(
            balaio, mucua,
            mocambola.username,
            mocambola,
            recovery_answer,
            token = token
        )
    async def put_mocambola(self, *,
                      balaio: str,
                      mucua: str,
                      username: str,
                      mocambola: Mocambola,
                      recovery_answer: str,
                      token: str = Header(...)):
        return self.baobaxia.put_mocambola(
            balaio, mucua,
            username,
            mocambola,
            recovery_answer,
            token = token
        )
    async def del_mocambola(self, *,
                      balaio: str,
                      mucua: str,
                      username: str,
                      token: str = Header(...)):
        self.baobaxia.del_mocambola(
            balaio, mucua, username, token)

#path = config.data_path / config.balaio_local / config.mucua_local
api = BaobaxiaAPI()


