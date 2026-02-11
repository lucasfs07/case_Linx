# Case Técnico – Analista de Integração SR

## Contexto Geral

Você foi contratado como **Analista de Integração Sênior** para apoiar um cliente do varejo que utiliza múltiplos sistemas para registrar vendas, pagamentos e baixas financeiras.

Atualmente, o cliente possui:

- Um **Sistema de Vendas (Portal)**
- Um **ERP Financeiro/Contábil**
- Uma **API de Integração de Vendas (D+1)**
- Processos de conciliação financeira e contábil que apresentam divergências frequentes

Seu papel será **analisar dados, propor correções técnicas, estruturar integrações e comunicar claramente os problemas e soluções ao cliente**.

Este case foi inspirado em desafios reais de integração, conciliação financeira e comunicação com stakeholders, evoluindo modelos práticos de SQL, Excel, Análise de Dados e Integração via API.

---

## Objetivos Avaliados

Este case tem como objetivo avaliar se o candidato possui:

- Domínio em **layouts de arquivos (CSV, JSON, XML)**
- **Excel intermediário a avançado** (PROCV/XLOOKUP, Tabelas Dinâmicas, Análise de Dados)
- **SQL avançado** (JOINS, GROUP BY, CTEs, Functions, Procedures)
- Capacidade de **análise de conciliação financeira**
- Clareza na **comunicação com clientes não técnicos**
- Capacidade de estruturar **diagnóstico + plano de ação**

---

## Entregáveis Esperados

O candidato deverá entregar:

1. Scripts SQL  
2. Arquivos auxiliares (CSV/Excel ou evidências de fórmulas)  
3. Documento de análise (PDF ou DOC) com explicações técnicas e funcionais  
4. Respostas discursivas voltadas ao cliente  

---

## Desafio 1 – Integração de Layouts e Regras de Conciliação

### Contexto de Negócio

O cliente realiza vendas por cartão de crédito e envia diariamente um arquivo contendo **todas as vendas realizadas no dia anterior** para fins de **conciliação financeira com a adquirente** e posterior **baixa no ERP**.

Esse processo segue o **modelo D+1**, ou seja:

- **Dia D**: data em que a venda ocorre  
- **Dia D+1**: data em que as vendas do dia anterior são enviadas para integração  

Somente vendas **válidas para conciliação** devem ser enviadas para a API. Registros inconsistentes devem ser descartados e reportados.

---

### Arquivo de Origem (CSV)

O cliente envia diariamente um arquivo no formato CSV com o seguinte layout:

```csv
nsu;data_venda;hora_venda;valor_bruto;valor_liquido;taxa;parcela;bandeira;autorizacao;status;canal_venda;meio_pagamento;id_cliente;nome_cliente
123456;2025-03-27;14:32;150.75;145.00;5.75;1;VISA;ABC123;APROVADA;ECOMMERCE;CREDITO;789;Maria Silva
123457;2025-03-27;15:10;189.50;182.00;7.50;2;MASTERCARD;DEF456;APROVADA;LOJA_FISICA;CREDITO;456;João Santos
123458;2025-03-27;16:05;99.90;95.00;4.90;1;VISA;;APROVADA;ECOMMERCE;CREDITO;321;Ana Lima
123459;2025-03-27;17:20;220.00;213.00;7.00;1;ELO;GHI789;RECUSADA;ECOMMERCE;CREDITO;654;Carlos Souza
123460;2025-03-26;10:15;75.00;72.00;3.00;1;VISA;JKL012;APROVADA;ECOMMERCE;CREDITO;987;Fernanda Alves
;2025-03-27;11:40;180.00;174.00;6.00;1;MASTERCARD;MNO345;APROVADA;ECOMMERCE;CREDITO;159;Rafael Costa
123461;2025-03-27;18:55;60.00;58.00;2.00;1;VISA;PQR678;APROVADA;ECOMMERCE;DEBITO;753;Patricia Gomes
123462;2025-03-27;19:30;310.00;300.00;10.00;3;VISA;STU901;APROVADA;ECOMMERCE;CREDITO;852;Lucas Rocha
```

Observações:

- O arquivo contém registros válidos e inválidos propositalmente  
- Nem todas as vendas devem ser enviadas para a API  

---

### Contrato da API de Destino (JSON)

A API de integração recebe os dados no seguinte formato:

```json
{
  "data_envio": "YYYY-MM-DD",
  "vendas": [
    {
      "id_venda": "string",
      "nsu": "string",
      "data_transacao": "YYYY-MM-DD",
      "valor": "number",
      "bandeira": "string",
      "codigo_autorizacao": "string",
      "status": "string"
    }
  ]
}
```

Regras importantes:

- Apenas os campos documentados devem ser enviados  
- O campo `data_transacao` deve corresponder ao **dia da venda (D)**  
- O campo `data_envio` deve corresponder ao **dia do envio (D+1)**  

---

### Tarefas do Candidato

#### 1. Análise de Registros e Regras de Negócio

Explique:

- Quais **critérios** você utilizaria para definir se uma venda é elegível para envio  

REPOSTA:

Critérios para uma venda ser elegível para envio
Uma venda só deve ser enviada para a API se atender todos os critérios abaixo:

Status = APROVADA
NSU preenchido
Código de autorização preenchido
Meio de pagamento = CRÉDITO
Data da venda (data_venda) = Dia D
Considerando processamento em 2025-03-28, o Dia D é 2025-03-27
Valor bruto maior que zero
Venda única (não duplicada)
Esses critérios garantem:
Integridade financeira
Rastreabilidade da transação
Conciliação correta com adquirente e ERP


- Quais registros do CSV **não devem ser enviados** e por quê  

REPOSTA:
| NSU       | Motivo                      |
| --------- | --------------------------- |
| 123458    | Sem código de autorização   |
| 123459    | Status RECUSADA             |
| 123460    | Data fora do D (2025-03-26) |
| *(vazio)* | NSU ausente                 |



- Quais validações são obrigatórias para garantir a conciliação financeira  

REPOSTA:
- NSU único & obrigatorio
- Autorização unica & obrigatoria
- Valor consistente entre sistemas
- Data correta (D)
- Status final diferente de recusada

---

#### 2. Conversão de CSV para JSON

1. Considere que o processamento ocorre em **2025-03-28 (D+1)**  
2. Converta **apenas as vendas elegíveis** para o formato JSON esperado pela API  
3. Evidencie o JSON que seria utilizado para envio na API

A conversão pode ser realizada utilizando qualquer ferramenta ou abordagem, desde que o candidato explique claramente o processo adotado.

REPOSTA:

Utilizei um script simples em python para parsear os dados criando 

output script em python:

{
  "data_envio": "2025-03-28",
  "vendas": [
    {
      "id_venda": "123456",
      "nsu": "123456",
      "data_transacao": "2025-03-27",
      "valor": 150.75,
      "bandeira": "VISA",
      "codigo_autorizacao": "ABC123",
      "status": "APROVADA"
    },
    {
      "id_venda": "123457",
      "nsu": "123457",
      "data_transacao": "2025-03-27",
      "valor": 189.5,
      "bandeira": "MASTERCARD",
      "codigo_autorizacao": "DEF456",
      "status": "APROVADA"
    },
    {
      "id_venda": "123461",
      "nsu": "123461",
      "data_transacao": "2025-03-27",
      "valor": 60.0,
      "bandeira": "VISA",
      "codigo_autorizacao": "PQR678",
      "status": "APROVADA"
    },
    {
      "id_venda": "123462",
      "nsu": "123462",
      "data_transacao": "2025-03-27",
      "valor": 310.0,
      "bandeira": "VISA",
      "codigo_autorizacao": "STU901",
      "status": "APROVADA"
    }
  ]
}

terminal output:
JSON gerado com sucesso!
 Total de vendas enviadas: 4
 Total de registros rejeitados: 4

 Escolhi usar um script em python por 2 motivos,
 Facilidade do cliente utilizar e pensando que o nosso cliente possui uma operação grande, processando milhares de vendas por dia, fica facil adptar esse codigo do lado dele, 
 adicionei alguns comentarios para que o mesmo consiga utilizar 

 esse script gera 2 arquivos 1 com as vendas que podem ser enviadas por atender da todos os critrerios, e outro com as vendas rejeitadas

Script disponivel para analise na pasta de desafio 1
---

#### 3. Tratamento de Erros e Exceções

Descreva como o processo deve se comportar nos seguintes cenários:

- Venda com status diferente de APROVADA  
  deve enviar aprovada ou confirmada ainda sim existe a possibilidade da adquirente confirmar a compra 

- Venda sem NSU ou sem código de autorização 
  não enviar afinal as principais chaves de conciliação para conciliar

- Venda fora do período D
  nao deve aceitar pois a janela de processamento passou (d+1)
  Neste caso deve existir outro endpoint para conciliar as vendas retroativamente, ou maneira diferente de mandar as vendas

- Venda duplicada
  o sistema deve reconhecer que esse lote de eventos existem vendas duplicadas e o mesmo deve responder ao cliente que ele nao pode enviar assim,
  afinal ela pode estar com o mesmo NSU e autorização porem com valores e datas diferentes, cabe o cliente entender e corrigir isso internamente

- Meio de pagamento diferente de crédito  
  deve aceitar afinal a concilição nao se restringe somente ao crédito, existem outros meios de capturar uma venda
---

### Avaliação Esperada

Neste desafio serão avaliados:

- Capacidade de aplicar regras de negócio  
- Atenção a detalhes e exceções  
- Entendimento de conciliação financeira  
- Clareza técnica e funcional  
- Justificativa das decisões tomadas  

---

## Desafio 2 – Análise de Conciliação em Excel

### Contexto

No processo de conciliação financeira, os dados de vendas do **Portal** e do **ERP** nem sempre chegam no mesmo formato ou com o mesmo nível de consistência.

Neste desafio, você receberá **dois arquivos no formato JSON**, representando:

- Vendas registradas no **Portal**  
- Vendas registradas no **ERP**  

Os arquivos contêm **dados corretos e dados propositalmente confusos**, simulando situações reais de integração e conciliação.

Seu objetivo é transformar esses dados em **planilhas Excel**, analisar as divergências e apresentar conclusões relevantes.

---

### Arquivo 1 – Vendas Portal (JSON)

```json
[
  {"nsu":"123456","data_venda":"2025-03-27","valor":150.75,"autorizacao":"ABC123","bandeira":"VISA"},
  {"nsu":"123457","data_venda":"2025-03-27","valor":189.50,"autorizacao":"DEF456","bandeira":"MASTERCARD"},
  {"nsu":"123458","data_venda":"2025-03-27","valor":99.90,"autorizacao":null,"bandeira":"VISA"},
  {"nsu":"123459","data_venda":"2025-03-27","valor":220.00,"autorizacao":"GHI789","bandeira":"ELO"},
  {"nsu":"123460","data_venda":"2025-03-26","valor":75.00,"autorizacao":"JKL012","bandeira":"VISA"},
  {"nsu":"123461","data_venda":"2025-03-27","valor":60.00,"autorizacao":"PQR678","bandeira":"VISA"},
  {"nsu":"123462","data_venda":"2025-03-27","valor":310.00,"autorizacao":"STU901","bandeira":"VISA"},
  {"nsu":"123463","data_venda":"2025-03-27","valor":180.00,"autorizacao":"MNO345","bandeira":"MASTERCARD"},
  {"nsu":"123464","data_venda":"2025-03-27","valor":95.00,"autorizacao":"QWE234","bandeira":"VISA"},
  {"nsu":"123465","data_venda":"2025-03-27","valor":410.00,"autorizacao":"RTY567","bandeira":"ELO"}
]
```

---

### Arquivo 2 – Vendas ERP (JSON)

```json
[
  {"nsu":"123456","data_lancamento":"2025-03-28","valor":150.75,"autorizacao":"ABC123","bandeira":"VISA"},
  {"nsu":"123457","data_lancamento":"2025-03-28","valor":182.00,"autorizacao":"DEF456","bandeira":"MASTERCARD"},
  {"nsu":"123460","data_lancamento":"2025-03-27","valor":75.00,"autorizacao":"JKL012","bandeira":"VISA"},
  {"nsu":"123461","data_lancamento":"2025-03-28","valor":60.00,"autorizacao":"PQR678","bandeira":"VISA"},
  {"nsu":"123462","data_lancamento":"2025-03-28","valor":300.00,"autorizacao":"STU901","bandeira":"VISA"},
  {"nsu":"123463","data_lancamento":"2025-03-28","valor":180.00,"autorizacao":"MNO345","bandeira":"MASTERCARD"},
  {"nsu":"123466","data_lancamento":"2025-03-28","valor":250.00,"autorizacao":"ASD890","bandeira":"VISA"},
  {"nsu":"123467","data_lancamento":"2025-03-28","valor":90.00,"autorizacao":"FGH123","bandeira":"ELO"},
  {"nsu":"123468","data_lancamento":"2025-03-28","valor":500.00,"autorizacao":"ZXC456","bandeira":"VISA"},
  {"nsu":"123469","data_lancamento":"2025-03-28","valor":130.00,"autorizacao":"VBN789","bandeira":"MASTERCARD"}
]
```

---

### Tarefas do Candidato

#### 1. Preparação dos Dados

- Converta os dois arquivos JSON em **planilhas Excel**  
- Padronize os dados para permitir comparação entre Portal e ERP  

---

#### 2. Análise com Excel

Utilizando **Excel**, realize:

- Pelo menos **3 Tabelas Dinâmicas**, cada uma com uma análise relevante (ex.: divergência por valor, por bandeira, por data)  
- Uso de **PROCV ou XLOOKUP (PROCX)** para identificar correspondência entre Portal e ERP  
- Uso de **Filtros Avançados** para isolar inconsistências  

Explique o racional por trás de cada análise criada.

---

#### 3. Conclusão e Comunicação

- Liste as principais divergências encontradas  
  Encontrei Nsus unicos em ambos os lados, alguma vendas tiveram seus valores registrados errados do lado do ERP (valor liquido ao inves do bruto, ou erro no erp ),
  encontrei uma venda, com a autorização vazia do lado do portal, vale a pensa investigar mais afundo o motivo disso ter acontecido (possivel bug/problema do nosso lado)
  data da venda registrada errada do lado do ERP(um dia no futuro) 


- Explique o possível impacto financeiro dessas divergências  
  primeiro que ao nao registar os valores de maneira correta e nao registrar o nsu ou autorização registrada corretamente, o que pode ocorrer alem da conciliação ineficaz ao comparar com o ERP, seria a dificuldade de bater o valor recebido ou a receber, a final valores, datas e registros estao registrados errados, e nao serao nem enviados pela  API

- Descreva como você apresentaria esse resultado em uma reunião com o cliente  
  eu iniciaria explicando a iportancia de registrar os dados corretamente no ERP, alem colocar enfase em nos relatorios que nao vao bater no futuro se nao tivermos esses dados, 
  so depois disso eu mostraria as divergencias que encontrei, montaria um material para que ele consulte as mudanças que ele precisa fazer do lado dele, a ideia aqui e fazer o cliente entrar menos em contato e se auto servir, dado que na proxima vez que ele passar por esse problema, tem uma chance dele propio fazer a analise e achar o problema!
  
---

### Avaliação Esperada

Neste desafio serão avaliados:

- Capacidade de transformar dados JSON em análises estruturadas  
- Domínio de Excel intermediário/avançado  
- Raciocínio analítico e visão de conciliação  
- Clareza na explicação das análises e conclusões  

---

## Desafio 3 – Modelagem e Consultas SQL Avançadas

### Contexto

No processo de conciliação financeira, os dados operacionais são armazenados em diferentes estruturas e dependem de **tabelas de domínio** para correta interpretação (ex.: usuários e bandeiras).

Neste desafio, você receberá **quatro arquivos no formato XML** representando dados de origem que ainda **não estão em banco de dados**.

Seu objetivo será:

1. Interpretar os XMLs  
2. Modelar e criar as tabelas em um banco relacional  
3. Carregar os dados  
4. Executar consultas SQL avançadas voltadas à conciliação  

---

### Arquivos de Entrada (XML)

#### XML 1 – Vendas Portal

```xml
<vendas>
 <venda><id>1</id><nsu>123456</nsu><usuario_id>1</usuario_id><bandeira_id>1</bandeira_id><data_venda>2025-03-27</data_venda><valor>150.75</valor></venda>
 <venda><id>2</id><nsu>123457</nsu><usuario_id>2</usuario_id><bandeira_id>2</bandeira_id><data_venda>2025-03-27</data_venda><valor>189.50</valor></venda>
 <venda><id>3</id><nsu>123458</nsu><usuario_id>3</usuario_id><bandeira_id>1</bandeira_id><data_venda>2025-03-27</data_venda><valor>99.90</valor></venda>
 <venda><id>4</id><nsu>123459</nsu><usuario_id>1</usuario_id><bandeira_id>3</bandeira_id><data_venda>2025-03-27</data_venda><valor>220.00</valor></venda>
 <venda><id>5</id><nsu>123460</nsu><usuario_id>2</usuario_id><bandeira_id>1</bandeira_id><data_venda>2025-03-26</data_venda><valor>75.00</valor></venda>
 <venda><id>6</id><nsu>123461</nsu><usuario_id>4</usuario_id><bandeira_id>1</bandeira_id><data_venda>2025-03-27</data_venda><valor>60.00</valor></venda>
 <venda><id>7</id><nsu>123462</nsu><usuario_id>1</usuario_id><bandeira_id>1</bandeira_id><data_venda>2025-03-27</data_venda><valor>310.00</valor></venda>
 <venda><id>8</id><nsu>123463</nsu><usuario_id>3</usuario_id><bandeira_id>2</bandeira_id><data_venda>2025-03-27</data_venda><valor>180.00</valor></venda>
 <venda><id>9</id><nsu>123464</nsu><usuario_id>2</usuario_id><bandeira_id>1</bandeira_id><data_venda>2025-03-27</data_venda><valor>95.00</valor></venda>
 <venda><id>10</id><nsu>123465</nsu><usuario_id>4</usuario_id><bandeira_id>3</bandeira_id><data_venda>2025-03-27</data_venda><valor>410.00</valor></venda>
</vendas>
```

#### XML 2 – Vendas ERP

```xml
<vendas>
 <venda><id>1</id><nsu>123456</nsu><data_lancamento>2025-03-28</data_lancamento><valor>150.75</valor></venda>
 <venda><id>2</id><nsu>123457</nsu><data_lancamento>2025-03-28</data_lancamento><valor>182.00</valor></venda>
 <venda><id>3</id><nsu>123460</nsu><data_lancamento>2025-03-27</data_lancamento><valor>75.00</valor></venda>
 <venda><id>4</id><nsu>123461</nsu><data_lancamento>2025-03-28</data_lancamento><valor>60.00</valor></venda>
 <venda><id>5</id><nsu>123462</nsu><data_lancamento>2025-03-28</data_lancamento><valor>300.00</valor></venda>
 <venda><id>6</id><nsu>123463</nsu><data_lancamento>2025-03-28</data_lancamento><valor>180.00</valor></venda>
 <venda><id>7</id><nsu>123466</nsu><data_lancamento>2025-03-28</data_lancamento><valor>250.00</valor></venda>
 <venda><id>8</id><nsu>123467</nsu><data_lancamento>2025-03-28</data_lancamento><valor>90.00</valor></venda>
 <venda><id>9</id><nsu>123468</nsu><data_lancamento>2025-03-28</data_lancamento><valor>500.00</valor></venda>
 <venda><id>10</id><nsu>123469</nsu><data_lancamento>2025-03-28</data_lancamento><valor>130.00</valor></venda>
</vendas>
```

#### XML 3 – Usuários (Domínio)

```xml
<usuarios>
 <usuario><id>1</id><nome>Maria Silva</nome></usuario>
 <usuario><id>2</id><nome>João Santos</nome></usuario>
 <usuario><id>3</id><nome>Ana Lima</nome></usuario>
 <usuario><id>4</id><nome>Lucas Rocha</nome></usuario>
</usuarios>
```

#### XML 4 – Bandeiras (Domínio)

```xml
<bandeiras>
 <bandeira><id>1</id><nome>VISA</nome></bandeira>
 <bandeira><id>2</id><nome>MASTERCARD</nome></bandeira>
 <bandeira><id>3</id><nome>ELO</nome></bandeira>
</bandeiras>
```

---

### Regras e Premissas

- Você pode utilizar **qualquer banco de dados relacional**, desde que a solução utilize **SQL ANSI**  
- É obrigatório **justificar o banco escolhido**  
- A estrutura das tabelas criadas deve ser apresentada  

---

### Tarefas do Candidato

#### 1. Modelagem e Carga

- Proponha o modelo relacional das 4 tabelas  
- Crie as tabelas  
- Explique como os XMLs seriam carregados (script, ferramenta ou lógica)  

RESPOSTA:

As ferramentas utilizadas são Airflow, AWS Glue e Amazon S3.

A DAG do Airflow utiliza o Glue Job Operator para executar um job no AWS Glue, responsável por processar os arquivos brutos e convertê-los para a camada curated, salvando os dados em formato Parquet no S3.

Após a execução da DAG, os dados ficam disponíveis para consulta no Amazon Athena, onde as tabelas são criadas a partir dos arquivos processados.

criação das tabelas
----- tabela de vendas portal ------
  CREATE EXTERNAL TABLE vendas_portal (
  venda_id INT,
  nsu STRING,
  usuario_id INT,
  bandeira_id INT,
  data_venda DATE,
  valor DECIMAL(10,2)
)
STORED AS PARQUET
LOCATION 's3://datalake/curated/vendas_portal/';



----- tabela de vendas ERP ------
CREATE EXTERNAL TABLE vendas_erp (
  venda_id INT,
  nsu STRING,
  data_lancamento DATE,
  valor DECIMAL(10,2)
)
STORED AS PARQUET
LOCATION 's3://datalake/curated/vendas_erp/';



----- tabela de usuarios ------
CREATE EXTERNAL TABLE usuarios (
  usuario_id INT,
  nome STRING
)
STORED AS PARQUET
LOCATION 's3://datalake/curated/usuarios/';

----- tabela de bandeiras ------

CREATE EXTERNAL TABLE bandeiras (
  bandeira_id INT,
  nome STRING
)
STORED AS PARQUET
LOCATION 's3://datalake/curated/bandeiras/';




---

#### 2. Consultas SQL (Obrigatório)

Crie consultas que atendam aos cenários abaixo:

1. **Conciliação Portal x ERP**
   - Utilize **CTE**
   - Compare vendas por NSU
   - Retorne divergências de valor
   - Utilize **INNER JOIN** ou **LEFT JOIN**, justificando a escolha

   Aqui eu usei left join, para trazer somente oq estava errado do lado do ERP o inner join iria trazer só oque existe dos dois lados ignoradno vendas que nao existem no erp porem deveriam existir

WITH conc AS (
  SELECT
    p.nsu,
    p.valor AS valor_portal,
    e.valor AS valor_erp
  FROM vendas_portal p
  LEFT JOIN vendas_erp e
    ON p.nsu = e.nsu
)
SELECT *
FROM conc
WHERE valor_portal <> valor_erp
   OR valor_erp IS NULL;


O objetivo dessa query é conciliar vendas entre dois sistemas (Portal x ERP) usando o NSU como chave de comparação e identificar divergências de valores ou registros ausentes no ERP


2. **Análise por Usuário e Bandeira**
   - Retorne nome do usuário e bandeira (dados de domínio)
   - Agrupe e totalize valores

SELECT
  u.nome AS usuario,
  b.nome AS bandeira,
  SUM(v.valor) AS total_vendido
FROM vendas_portal v
JOIN usuarios u ON v.usuario_id = u.usuario_id
JOIN bandeiras b ON v.bandeira_id = b.bandeira_id
GROUP BY u.nome, b.nome;

total vendido por usuário e por bandeira, utilizando dados de domínio

3. **Ranking e Análise Avançada**
   - Utilize **Window Functions** (ex.: ROW_NUMBER, RANK, SUM() OVER)
   - Gere um ranking de usuários por valor vendido
   - O resutlado deve contenter o nome do usuário, o valor total que ele vendeu, e o percentual que esse valor representa frente ao valor total de venda de todos os usuários

WITH total AS (
  SELECT
    u.nome,
    SUM(v.valor) AS total_vendido
  FROM vendas_portal v
  JOIN usuarios u ON v.usuario_id = u.usuario_id
  GROUP BY u.nome
),
geral AS (
  SELECT
    *,
    SUM(total_vendido) OVER () AS total_geral
  FROM total
)
SELECT
  nome,
  total_vendido,
  ROUND((total_vendido / total_geral) * 100, 2) AS percentual,
  RANK() OVER (ORDER BY total_vendido DESC) AS ranking
FROM geral;

Essa query realiza uma análise avançada de vendas por usuário, utilizando CTEs e Window Functions para gerar ranking e percentual de participação no total vendido.
---

Para ficar mais organizado, vou deixar os resultados das querys numa pasta em desafio3, (desafio3 -> resultados_querys)

### Avaliação Esperada

Neste desafio serão avaliados:

- Capacidade de modelagem relacional  
- Domínio de SQL avançado (CTE, Window Functions, JOINs)  
- Tomada de decisão entre INNER vs LEFT JOIN  
- Atenção a armadilhas comuns em SQL  
- Clareza na explicação das escolhas técnicas  

---

## Desafio 4 – Comunicação com o Cliente (Essencial)

### Cenário

O cliente financeiro questiona:

> "Por que o valor que aparece no Portal não bate com o valor lançado no ERP?"


Olá, Boa tarde! Tudo bem?

Me chamo Lucas e estou aqui para te ajudar!

A diferença de valores entre o Portal e o ERP ocorre porque cada sistema registra a venda em momentos diferentes do processo.

O Portal mostra o valor da venda no momento da compra (valor total/bruto).
Já o ERP registra o lançamento financeiro, que pode considerar:

- Data diferente da venda (D+1)

- Aplicação de taxas

- Valor líquido em vez do valor bruto

O principal elo entre esses registros é o NSU, que identifica a mesma transação em todos os sistemas. Quando o NSU ou a autorização estão ausentes ou inconsistentes, a conciliação pode apresentar divergências.

Para evitar esse cenário, devemos garantir que apenas vendas, com NSU válido, autorização preenchida e valores corretos sejam integradas ao ERP, assegurando confiabilidade financeira e contábil.

Ficamos à disposição para qualquer esclarecimento adicional.

Abraços

Lucas Santos

### Tarefa

Responda:

1. Em linguagem **não técnica**  
2. Explicando:
   - Diferença entre venda, autorização e liquidação  
   - Importância do NSU  
   - Impacto contábil  

---

## Critérios de Avaliação

| Critério                 | Peso       |
|--------------------------|------------|
| SQL Avançado             | Alto       |
| Excel e Análise de Dados | Alto       |
| Integração e Layouts     | Alto       |
| Clareza na Comunicação   | Muito Alto |
| Visão de Processo        | Muito Alto |

---

## Diferencial Esperado de um SR

- Visão de ponta a ponta  
- Capacidade de orientar o cliente  
- Propostas de melhoria contínua  
- Clareza técnica e funcional  


Boa sorte!
