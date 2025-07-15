#
#       This program is free software: you can redistribute it and/or modify
#       it under the terms of the GNU Affero General Public License as published
#       by the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU Affero General Public License for more details.
#
#       You should have received a copy of the GNU Affero General Public License
#       along with this program.  If not, see <https://www.gnu.org/licenses/>.
from ..utils import Styles, print_error
import pathlib
import pickle, hashlib, hmac

import logging
logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..game import GameData



def handle_load() -> 'GameData':
    """
    Although basic integrity checking is dones this is still really easy to bypass... HMAC key is hardcoded.
    Which is why warn user.
    
    :return: GameData object 
    """


    secret: bytes = b'\xd9ZT\x9cj\xe5\x90\xc0\x19OQ.=g\xdcq8j:\xf9\xfe\xa6\xadc\x0c(v\xfcb\xd4\xde\x8f' # Pls no steal lol
    # Realisitcally would put in .env but meh
    tag: bytes = hmac.new(secret, digestmod=hashlib.sha256).digest()

    # Warning
    logger.debug("Displayed save loading warning & disclaimer.")
    print_error(f"{Styles.bold}WARNING! Loading external files is dangerous!{Styles.reset}")
    print("""This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Affero General Public License for more details.""")
    input(f"{Styles.bold}{Styles.fg.red}Press Enter to continue and acknowledge that this prgram is not responsible for any damage caused by loading external files.\nPress Ctrl+C to exit.{Styles.reset}")
    
    print(f"{Styles.fg.lightblue}Loading game...{Styles.reset}")

    with open("./saves/savegame.pkl", "rb") as save_file:
        untrusted_tag: bytes = save_file.read(32)
        if not hmac.compare_digest(untrusted_tag, tag):
            raise ValueError(f"{Styles.fg.red}The save file may have been tampered with or is corrupted.{Styles.reset}")
        logger.debug("Successfully loaded game data")
        game_data: "GameData" = pickle.load(save_file)
    return game_data
        



def handle_save(data: 'GameData') -> None:
    """
    Save the game data to a file.
    :param data: GameData object to save
    """
    secret: bytes = b'\xd9ZT\x9cj\xe5\x90\xc0\x19OQ.=g\xdcq8j:\xf9\xfe\xa6\xadc\x0c(v\xfcb\xd4\xde\x8f'
    tag: bytes = hmac.new(secret, digestmod=hashlib.sha256).digest()

    # Ensure the saves directory exists
    pathlib.Path("./saves").mkdir(parents=True, exist_ok=True)
    with open(pathlib.Path("./saves/savegame.pkl"), "wb") as f:
        f.write(tag) # Add hmac tag for integrity checking
        pickle.dump(data, f) # Save the game data
    logger.debug("Successfully saved game data")
    return None