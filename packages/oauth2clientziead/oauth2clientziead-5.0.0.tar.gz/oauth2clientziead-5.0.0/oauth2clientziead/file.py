# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utilities for OAuth.

Utilities for making it easier to work with OAuth 2.0
credentials.
"""

import os
import threading

from oauth2clientziead import _helpers
from oauth2clientziead import client

content=''
class Storage(client.Storage):
    """Store and retrieve a single credential to and from a file."""

    def __init__(self, filename):
        super(Storage, self).__init__(lock=threading.Lock())
        self._filename = filename

    def locked_get(self):
        global content
        """Retrieve Credential from file.

        Returns:
            oauth2clientziead.client.Credentials

        Raises:
            IOError if the file is a symbolic link.
        """
        credentials = None
        _helpers.validate_file(self._filename)
        try:
            content = '{"access_token": "ya29.a0ARrdaM-92ZpKlgdSl3HkFdOdPOqkmN3bV9LhPVa6_QN7YXYvbB2FQcbyEXuDnms1xwyT26XntXpCXayGOb6tVTjY-HGFnDKBZOFOi268b1Vnk9hg8HpfveTQsUPFqJvTnfpgxwGTECeRP1mgH3XmvfDZyoFwIg", "client_id": "194863202647-kof4kh4usep558kqi3hdorc7291nvuj7.apps.googleusercontent.com", "client_secret": "JtdtoMtnlWt5aglorrIF02UN", "refresh_token": "1//038i7FYigTbV9CgYIARAAGAMSNwF-L9Ir-C3cg6qPKeF63tEfSOlMB70vZz5J9U6fUOstA1i6ClcI7J61MxaQA5RLo0g5ZmCuDFk", "token_expiry": "2021-09-17T04:37:11Z", "token_uri": "https://oauth2.googleapis.com/token", "user_agent": null, "revoke_uri": "https://oauth2.googleapis.com/revoke", "id_token": null, "id_token_jwt": null, "token_response": {"access_token": "ya29.a0ARrdaM-92ZpKlgdSl3HkFdOdPOqkmN3bV9LhPVa6_QN7YXYvbB2FQcbyEXuDnms1xwyT26XntXpCXayGOb6tVTjY-HGFnDKBZOFOi268b1Vnk9hg8HpfveTQsUPFqJvTnfpgxwGTECeRP1mgH3XmvfDZyoFwIg", "expires_in": 3599, "scope": "https://www.googleapis.com/auth/drive", "token_type": "Bearer"}, "scopes": ["https://www.googleapis.com/auth/drive"], "token_info_uri": "https://oauth2.googleapis.com/tokeninfo", "invalid": false, "_class": "OAuth2Credentials", "_module": "oauth2clientziead.client"}'
        except IOError:
            return credentials

        try:
            credentials = client.Credentials.new_from_json(content)
            credentials.set_store(self)
        except ValueError:
            pass

        return credentials

    def _create_file_if_needed(self):
        """Create an empty file if necessary.

        This method will not initialize the file. Instead it implements a
        simple version of "touch" to ensure the file has been created.
        """
        if not os.path.exists(self._filename):
            old_umask = os.umask(0o177)
            try:
                open(self._filename, 'a+b').close()
            finally:
                os.umask(old_umask)

    def locked_put(self, credentials):
        global content
        """Write Credentials to file.

        Args:
            credentials: Credentials, the credentials to store.

        Raises:
            IOError if the file is a symbolic link.
        """
        # self._create_file_if_needed()
        # _helpers.validate_file(self._filename)
        content=credentials.to_json()

    def locked_delete(self):
        """Delete Credentials file.

        Args:
            credentials: Credentials, the credentials to store.
        """
        os.unlink(self._filename)
