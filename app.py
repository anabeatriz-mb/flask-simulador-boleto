from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

HTML_FORM = '''
<h2>Simulador de Boleto Bancário</h2>
<form method="get">
  Valor do boleto (R$): <input type="text" name="valor"><br><br>
  Data de vencimento (dd/mm/aaaa): <input type="text" name="vencimento"><br><br>
  Data de pagamento (dd/mm/aaaa): <input type="text" name="pagamento"><br><br>
  <input type="submit" value="Calcular">
</form>
<hr>
{{ resultado|safe }}
'''

def calcular_boleto(valor_original, data_vencimento_str, data_pagamento_str):
    try:
        formato_data = "%d/%m/%Y"
        data_vencimento = datetime.strptime(data_vencimento_str, formato_data)
        data_pagamento = datetime.strptime(data_pagamento_str, formato_data)

        dias_atraso = max(0, (data_pagamento - data_vencimento).days)

        if dias_atraso >= 1:
            aviso = "<strong>AVISO:</strong> Esse boleto está atrasado!<br>"
            multa = valor_original * 0.02
            juros = valor_original * 0.00033 * dias_atraso
        else:
            aviso = "Pagamento dentro dos parâmetros!<br>"
            multa = 0
            juros = 0

        valor_total = valor_original + multa + juros

        return (
            f"{aviso}<br>"
            f"<strong>Resumo do Boleto</strong><br>"
            f"Valor original: R$ {valor_original:.2f}<br>"
            f"Data de vencimento: {data_vencimento_str}<br>"
            f"Data de pagamento: {data_pagamento_str}<br>"
            f"Dias de atraso: {dias_atraso}<br>"
            f"Multa (2%): R$ {multa:.2f}<br>"
            f"Juros (0,033% ao dia): R$ {juros:.2f}<br>"
            f"<strong>Valor total a pagar: R$ {valor_total:.2f}</strong>"
        )
    except ValueError as e:
        return f"<span style='color:red;'>Erro: Formato de data inválido. Use dd/mm/aaaa.</span><br>Detalhes: {e}"

@app.route('/')
def index():
    valor = request.args.get('valor')
    vencimento = request.args.get('vencimento')
    pagamento = request.args.get('pagamento')
    resultado = ''

    if valor and vencimento and pagamento:
        try:
            valor = float(valor.replace(',', '.'))
            resultado = calcular_boleto(valor, vencimento, pagamento)
        except Exception as e:
            resultado = f"<span style='color:red;'>Erro ao processar: {e}</span>"

    return render_template_string(HTML_FORM, resultado=resultado)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
