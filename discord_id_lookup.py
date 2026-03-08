:")).encode()
        ).decode()

        payload = {
            "discord_id": discord_id,
            "proof": proof,
            "token": bot_token
        }

        lookup_headers = {
          'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
          'Accept-Encoding': "gzip, deflate, br, zstd",
          'Content-Type': "application/json",
          'sec-ch-ua-platform': "\"Android\"",
          'sec-ch-ua': "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
          'sec-ch-ua-mobile': "?1",
          'origin': "https://discord.id",
          'sec-fetch-site': "same-site",
          'sec-fetch-mode': "cors",
          'sec-fetch-dest': "empty",
          'referer': "https://discord.id/",
          'accept-language': "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
          'priority': "u=1, i"
        }

        response = requests.post(
            lookup_url,
            data=json.dumps(payload),
            headers=lookup_headers
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": f"Erro na requisição HTTP: {e}"}
    except json.JSONDecodeError:
        return {"error": "Erro ao decodificar JSON da resposta da API."}
    except Exception as e:
        return {"error": f"Ocorreu um erro inesperado: {e}"}
