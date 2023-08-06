from .saberes import SaberesConfig, Saber, SaberesDataset, \
    SaberesDataStore, Balaio, Mucua, Mocambola
from .sankofa import Sankofa

from pathlib import Path
from configparser import ConfigParser

import argparse, os

parser = argparse.ArgumentParser("criar_mucua")
parser.add_argument("--path", help="Caminho absoluto da pasta para os dados do Baobáxia", type=str)
parser.add_argument("--balaio", help="Nome do Balaio", type=str)
parser.add_argument("--mucua", help="Nome da Mucua local onde instalar o Baobáxia", type=str)
parser.add_argument("--mocambo", help="Nome do Mocambo de base dessa Mucua local", type=str)
parser.add_argument("--mocambola", help="Username para criar um Mocambola", type=str)
parser.add_argument("--email", help="Email do Mocambola", type=str)
parser.add_argument("--password", help="Password para o Mocambola", type=str)
parser.add_argument("--smid_len", help="Numero de carateres para os IDs", type=int)
parser.add_argument("--slug_name_len", help="Numero de carateres para os nomes abreviados", type=int)
parser.add_argument("--slug_smid_len", help="Numero de carateres para os IDs abreviados", type=int)
parser.add_argument("--slug_sep", help="Caracter separador para o identificativo", type=str)


args = parser.parse_args()


def install(*, path: str, balaio: str, mucua: str, mocambo: str, mocambola: str,
            email: str, password: str, smid_len: int, slug_name_len: int,
            slug_smid_len: int, slug_sep: str):
    """Instalador do Baobáxia

    :param path: Caminho absoluto da pasta para os dados do Baobáxia
    :type path: str
    :param balaio: Nome do Balaio
    :type balaio: str
    :param mucua: Nome da Mucua local onde instalar o Baobáxia
    :type mucua: str
    :param mocambo: Nome do Mocambo de base dessa Mucua local
    :type mocambo: str
    :param mocambola: Username para criar um Mocambola
    :type mocambola: str
    :param email: Email do Mocambola
    :type email: str
    :param password: Password para o Mocambola
    :type password: str
    :param smid_len: Numero de carateres para os IDs
    :type smid_len: int
    :param slug_name_len: Numero de carateres para os nomes abreviados
    :type slug_name_len: int
    :param slug_smid_len: Numero de carateres para os IDs abreviados
    :type slug_smid_len: int
    :param slug_sep: Caracter separador para o identificativo
    :type slug_sep: str

    """

    data_path = Path(path)

    if data_path.is_absolute:
        config = SaberesConfig(
            data_path = data_path,
            default_balaio = balaio,
            smid_len = smid_len, 
            slug_name_len = slug_name_len,
            slug_smid_len = slug_smid_len,
            slug_sep = slug_sep
        )
        datastore = SaberesDataStore(config)
        balaio_dataset = datastore.create_balaio_dataset(
            mocambola=mocambola)
        balaio_saber = balaio_dataset.settle(
            balaio_dataset.create_obj(name=balaio, default_mucua=mucua))
        mucua_dataset = datastore.create_mucua_dataset(
            balaio=balaio_saber.slug, mocambola=mocambola)
        mucua_saber = dataset.settle(
            dataset.create_obj(name=mucua))
        mocambolas_path = config.data_path / balaio_saber.slug \
            / mucua_saber.slug / 'mocambolas'
        mocambolas_path.mkdir()
        mocambola_dataset = datastore.create_dataset(
            Mocambola, balaio_saber.slug, mucua_saber.slug, mocambola)
        from .util import str_to_hash
        mocambola_criado.password_hash = str_to_hash(password)
        mocambola_saber = dataset.settle(
            dataset.create_obj(
                path=Path('mocambolas'),
                name=mocambola,
                username=mocambola,
                email=email,
                password_hash=str_to_hash(password)
                ))

        Sankofa.create_balaio(balaio=balaio_saber.slug,
                              description=balaio_saber.slug,
                              config=config)
        
        Sankofa.add(saberes=[mucua_saber,
                             mocambola_saber],
                    mocambola=mocambola_saber,
                    config=config)

    config_file = ConfigParser()
    
    config_file['default'] = {
        "data_path": path,
        "saber_file_ext": ".baobaxia",
        "default_balaio": balaio_saber.slug,
        "smid_len": smid_len,
        "slug_smid_len": slug_smid_len,
        "slug_name_len": slug_name_len,
        "slug_sep": slug_sep
    }

    try:     
        with open(os.path.join(os.path.expanduser("~"), '.baobaxia.conf'), 'w') as writefile:
            config_file.write(writefile)
    except IOError:
        pass

def criar_mucua():
    install(**args.__dict__)


