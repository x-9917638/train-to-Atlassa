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
from typing import Optional
import pathlib
import pickle, hashlib, hmac




def handle_load() -> Optional['GameData']:
    """
    Although basic integrity checking is dones this is still really easy to bypass... HMAC key is hardcoded.
    Which is why warn user.
    
    :return: GameData object if a saved game is loaded, None otherwise
    """
    secret = b'\xd9ZT\x9cj\xe5\x90\xc0\x19OQ.=g\xdcq8j:\xf9\xfe\xa6\xadc\x0c(v\xfcb\xd4\xde\x8f' # Pls no steal lol
    tag = hmac.new(secret, digestmod=hashlib.sha256).digest()

    # Warning
    print_error(f"{Styles.bold}WARNING! Loading external files is dangerous!{Styles.reset}")
    print("""This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Affero General Public License for more details.""")
    input(f"{Styles.bold}{Styles.fg.red}Press Enter to continue and acknowledge that this prgram is not responsible for any damage caused by loading external files.\nPress Ctrl+C to exit.{Styles.reset}")
    
    print(f"{Styles.fg.lightblue}Loading game...{Styles.reset}")

    with open("./saves/savegame.pkl", "rb") as save_file:
        untrusted_tag = save_file.read(32)
        if not hmac.compare_digest(untrusted_tag, tag):
            raise ValueError(f"{Styles.fg.red}The save file may have been tampered with or is corrupted.{Styles.reset}")
        game_data = pickle.load(save_file)
    return game_data
        



def handle_save(data: 'GameData') -> None:
    """
    Save the game data to a file.
    :param data: GameData object to save
    """
    secret = b'\xd9ZT\x9cj\xe5\x90\xc0\x19OQ.=g\xdcq8j:\xf9\xfe\xa6\xadc\x0c(v\xfcb\xd4\xde\x8f'
    tag = hmac.new(secret, digestmod=hashlib.sha256).digest()

    # Ensure the saves directory exists
    pathlib.Path("./saves").mkdir(parents=True, exist_ok=True)
    with open(pathlib.Path("./saves/savegame.pkl"), "wb") as f:
        f.write(tag)
        pickle.dump(data, f)
    return None