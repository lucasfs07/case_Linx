import csv
import json
from datetime import datetime, timedelta

# Configurações de data
DATA_PROCESSAMENTO = datetime.strptime("2025-03-28", "%Y-%m-%d")
DATA_D = (DATA_PROCESSAMENTO - timedelta(days=1)).strftime("%Y-%m-%d")

CSV_PATH = "desafio1.csv"
OUTPUT_JSON = "payload_api.json"
OUTPUT_ERROS_CSV = "rejeicoes.csv"

vendas_elegiveis = {}
erros = []

with open(CSV_PATH, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")
    fieldnames = reader.fieldnames + ["motivo_erro"]

    for row in reader:
        nsu = row.get("nsu")
        data_venda = row.get("data_venda")
        status = row.get("status")
        autorizacao = row.get("autorizacao")
        valor = row.get("valor_bruto")

        # validações
        if not nsu:
            row["motivo_erro"] = "NSU ausente"
            erros.append(row)
            continue

        if status != "APROVADA":
            row["motivo_erro"] = "Status diferente de APROVADA"
            erros.append(row)
            continue

        if not autorizacao:
            row["motivo_erro"] = "Autorização ausente"
            erros.append(row)
            continue

        if data_venda != DATA_D:
            row["motivo_erro"] = "Venda fora do dia D"
            erros.append(row)
            continue

        try:
            valor = float(valor)
            if valor <= 0:
                raise ValueError
        except:
            row["motivo_erro"] = "Valor inválido"
            erros.append(row)
            continue

        # remove duplicidade por NSU
        if nsu in vendas_elegiveis:
            row["motivo_erro"] = "Venda duplicada"
            erros.append(row)
            continue

        vendas_elegiveis[nsu] = {
            "id_venda": nsu,
            "nsu": nsu,
            "data_transacao": data_venda,
            "valor": valor,
            "bandeira": row.get("bandeira"),
            "codigo_autorizacao": autorizacao,
            "status": status
        }

# montagem do payload final
payload = {
    "data_envio": DATA_PROCESSAMENTO.strftime("%Y-%m-%d"),
    "vendas": list(vendas_elegiveis.values())
}

# gerando arquivo JSON final
with open(OUTPUT_JSON, "w", encoding="utf-8") as jsonfile:
    json.dump(payload, jsonfile, ensure_ascii=False, indent=2)

# gerando arquivo de rejeições, se houver
if erros:
    with open(OUTPUT_ERROS_CSV, "w", newline='', encoding="utf-8") as errorfile:
        writer = csv.DictWriter(errorfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(erros)

print("JSON gerado com sucesso!")
print(f" Total de vendas enviadas: {len(payload['vendas'])}")
print(f" Total de registros rejeitados: {len(erros)}")
print(f" Arquivo de rejeições gerado: {OUTPUT_ERROS_CSV}")
