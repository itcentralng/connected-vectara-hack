"""Simple example of using the Vectara REST API for deleting a corpus.
"""

import json
import logging
import os
import requests

from helpers.vectara.auth import get_jwt_token

def _get_delete_corpus_json(customer_id: int, corpus_id: int):
    """ Returns a delete corpus json. """
    corpus = {}
    corpus["customer_id"] = customer_id
    corpus["corpus_id"] = corpus_id

    return json.dumps(corpus)

def delete_corpus(corpus_id: int):
    """Delete a corpus.
    Args:
        customer_id: Unique customer ID in vectara platform.
        corpus_id: Corpus ID in vectara platform.
        admin_address: Address of the admin server. e.g., api.vectara.io
        jwt_token: A valid Auth token.

    Returns:
        (response, True) in case of success and returns (error, False) in case of failure.
    """

    post_headers = {
        "customer-id": os.getenv("VECTARA_CUSTOMER_ID"),
        "Authorization": f"Bearer {get_jwt_token()}"
    }
    response = requests.post(
        f"https://{os.getenv('VECTARA_BASE')}/v1/delete-corpus",
        data=_get_delete_corpus_json(os.getenv("VECTARA_CUSTOMER_ID"), corpus_id),
        verify=True,
        headers=post_headers)

    if response.status_code != 200:
        logging.error("Reset Corpus failed with code %d, reason %s, text %s",
                       response.status_code,
                       response.reason,
                       response.text)
        return response, False
    return response, True