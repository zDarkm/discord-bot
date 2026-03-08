import requests
import json
import base64
import asyncio
import base64
import json
import os

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

lookup_url = os.getenv('DISCORD_LOOKUP_URL', 'https://api.discord.id/v1/lookup')


def _build_session():
    session = requests.Session()
    retry_kwargs = {
        'total': 3,
        'backoff_factor': 0.5,
        'status_forcelist': (429, 500, 502, 503, 504),
    }

    try:
        retries = Retry(allowed_methods=("POST",), **retry_kwargs)
    except TypeError:
        # Compatibilidade com urllib3 antigo
        retries = Retry(method_whitelist=("POST",), **retry_kwargs)

    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

lookup_url = "https://api.discord.id/v1/lookup"

async def lookup_discord_id(discord_id, bot_token):
    try:
        proof = base64.b64encode(
            f"{discord_id}:{bot_token}".encode()
        ).decode()
        proof = base64.b64encode(f"{discord_id}:{bot_token}".encode()).decode()

        payload = {
            "discord_id": discord_id,
            "proof": proof,
            "token": bot_token
            'discord_id': discord_id,
            'proof': proof,
            'token': bot_token,
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0',
        }

        def make_request():
            response = requests.post(
                lookup_url,
                data=json.dumps(payload),
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            with _build_session() as session:
                response = session.post(
                    lookup_url,
                    data=json.dumps(payload),
                    headers=headers,
                    timeout=20,
                )
                response.raise_for_status()
                return response.json()

        result = await asyncio.to_thread(make_request)
        return result
        return await asyncio.to_thread(make_request)

    except requests.exceptions.ConnectionError as e:
        return {
            'error': (
                'Não foi possível conectar ao serviço de consulta de ID '
                '(falha de rede/DNS). Tente novamente em alguns minutos.'
            ),
            'details': str(e),
        }
    except requests.exceptions.Timeout as e:
        return {
            'error': 'Tempo limite excedido ao consultar o serviço externo. Tente novamente.',
            'details': str(e),
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Erro na requisição HTTP: {e}"}
        return {'error': f'Erro na requisição HTTP: {e}'}
    except json.JSONDecodeError:
        return {"error": "Erro ao decodificar JSON da resposta da API."}
        return {'error': 'Erro ao decodificar JSON da resposta da API.'}
    except Exception as e:
        return {"error": f"Ocorreu um erro inesperado: {e}"}
        return {'error': f'Ocorreu um erro inesperado: {e}'}
