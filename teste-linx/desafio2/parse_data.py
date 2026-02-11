import json
import pandas as pd

arquivos = {
    "Portal": {
        "arquivo": "Json_portal.json",
        "rename": {
            "data_venda": "data_venda"
        }
    },
    "ERP": {
        "arquivo": "json_erp.json",
        "rename": {
            "data_lancamento": "data_venda"
        }
    }
}

with pd.ExcelWriter("dados_Erp_x_portal.xlsx", engine="openpyxl") as writer:
    for sheet, cfg in arquivos.items():
        with open(cfg["arquivo"], "r", encoding="utf-8") as f:
            data = json.load(f)

        df = pd.DataFrame(data)

        # Normalização dos nomes das colunas
        df.rename(columns=cfg["rename"], inplace=True)

        # Garantir ordem e presença das colunas
        colunas_padrao = ["nsu", "data_venda", "valor", "autorizacao", "bandeira"]
        df = df[colunas_padrao]

        df.to_excel(writer, sheet_name=sheet, index=False)

print("Excel criado com sucesso com dados normalizados!")
