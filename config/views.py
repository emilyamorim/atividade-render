import os
from datetime import datetime, timezone

from django.http import JsonResponse


def home(request):
    """Página principal: mostra o que vem da configuração e do código."""
    dados = {
        "mensagem": os.environ.get("MENSAGEM", "Olá, turma!"),  # vem da variável de ambiente
        "ambiente": os.environ.get("AMBIENTE", "local"),        # vem da variável de ambiente
        "versao": "2.0",                                        # vem do código
        "hora_do_servidor": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    return JsonResponse(dados, json_dumps_params={"ensure_ascii": False, "indent": 2})


def health(request):
    """Rota que o Render consulta para saber se a aplicação está funcionando."""
    return JsonResponse({"status": "ok"})