import requests

DEFAULT_IDENTITY_PROVIDER = {
    'base_url': 'https://explore.api.aai.ebi.ac.uk',
    'cert_checksum': ''
}


class Client(object):
    """
    Client to interact with the AAP service
    """
    def __init__(self, decoder, url_base, username, password):
        """
        Create a new instance of the client using some details for the authentication
        :param decoder: the token decoder used
        :type decoder: TokenDecoder
        :param url_base: the url base for the AAP authentication
        :type url: str
        """
        self._url_base = url_base
        self._decoder = decoder
        self._username = username
        self._password = password

    def request_token(self):
        """
        Get a new token from the AAP domain
        :return: the token, encoded, and decoded
        :rtype: str, str
        """
        response = requests.get(
            self._url_base + u'/auth', auth=(self._username, self._password))
        if response.status_code == requests.codes.ok:
            token = response.text
            return token, self._decoder.decode(token)
        return response.raise_for_status()

    def authed_request(self, session, prepared_request):
        prepared_request.headers['Authorization'] = 'Bearer {}'.format(self.request_token())
        return session.send(prepared_request)
