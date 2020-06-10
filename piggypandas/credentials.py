import getpass
from typing import Tuple
from pathlib import Path
import json


def get_credentials(try_getpass: bool = True) -> Tuple[str, str]:

    path: Path = Path.home().joinpath('.piggypandas-cred.json')
    if path.is_file():
        try:
            with open(str(path), 'r') as f:
                j = json.load(f)
                user: str = str(j['user'])
                password: str = str(j['password'])
                return user, password
        except FileNotFoundError:
            pass
        except KeyError:
            pass

    if try_getpass:
        user: str = getpass.getuser()
        password: str = getpass.getpass(prompt=f"Enter password for {user}: ")
        return user, password

    raise RuntimeError('Unable to load credentials')
