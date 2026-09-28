def test_saude_responde_ok(api_client):
    resposta = api_client.get("/api/saude/")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}
