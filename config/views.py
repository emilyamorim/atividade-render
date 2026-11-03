import os
from datetime import datetime, timezone

from django.http import HttpResponse, JsonResponse
from django.utils.html import escape

PAGINA = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Demo Render</title>
<style>
  * { box-sizing: border-box; margin: 0; }
  body { min-height: 100vh; display: flex; align-items: center; justify-content: center;
         background: #15131f; color: #f5f3ee; font-family: system-ui, sans-serif; padding: 24px; }
  main { max-width: 760px; width: 100%; text-align: center; }
  .selo { display: inline-block; padding: 6px 16px; border-radius: 999px; background: #2b2640;
          color: #a493ff; font-size: 14px; font-weight: 600; margin-bottom: 24px; }
  h1 { font-size: clamp(40px, 8vw, 80px); line-height: 1.1; margin-bottom: 40px; }
  .cartoes { display: flex; gap: 16px; flex-wrap: wrap; justify-content: center; }
  .cartao { flex: 1 1 200px; background: #211e2e; border: 1px solid #3a3550;
            border-radius: 16px; padding: 20px; }
  .cartao span { display: block; font-size: 13px; color: #8c88a0; margin-bottom: 6px; }
  .cartao strong { font-size: 20px; }
  footer { margin-top: 32px; font-size: 14px; color: #8c88a0; }
</style>
</head>
<body>
<main>
  <div class="selo">Publicado com Render</div>
  <h1>__MENSAGEM__</h1>
  <div class="cartoes">
    <div class="cartao"><span>Ambiente (variável)</span><strong>__AMBIENTE__</strong></div>
    <div class="cartao"><span>Versão (código)</span><strong>__VERSAO__</strong></div>
    <div class="cartao"><span>Hora do servidor (UTC)</span><strong>__HORA__</strong></div>
  </div>
  <footer>Atualize a página para ver a hora mudar</footer>
</main>
</body>
</html>"""


def dados():
    """Reúne o que vem da configuração (variáveis) e do código."""
    return {
        "mensagem": os.environ.get("MENSAGEM", "Olá, turma!"),  # vem da variável de ambiente
        "ambiente": os.environ.get("AMBIENTE", "local"),        # vem da variável de ambiente
        "versao": "1.0",                                        # vem do código
        "hora_do_servidor": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def home(request):
    """Página principal, com visual para a apresentação."""
    d = dados()
    html = (
        PAGINA.replace("__MENSAGEM__", escape(d["mensagem"]))
        .replace("__AMBIENTE__", escape(d["ambiente"]))
        .replace("__VERSAO__", escape(d["versao"]))
        .replace("__HORA__", d["hora_do_servidor"][11:19])
    )
    return HttpResponse(html)


def api(request):
    """Os mesmos dados em formato JSON."""
    return JsonResponse(dados(), json_dumps_params={"ensure_ascii": False, "indent": 2})


def health(request):
    """Rota que o Render consulta para saber se a aplicação está funcionando."""
    return JsonResponse({"status": "ok"})