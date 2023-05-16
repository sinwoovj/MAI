import requests
import metadata.api_key as api_key

resp = requests.post(
    'https://openapi.vito.ai/v1/authenticate',
    data={'client_id': f'{api_key.VITO_API_KEY_CLIENT_ID}',
          'client_secret': f'{api_key.VITO_API_KEY_CLIENT_SECRET}'}
)
resp.raise_for_status()
print(resp.json())