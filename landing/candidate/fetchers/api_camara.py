import requests

CAMARA_API = "https://dadosabertos.camara.leg.br/api/v2"

# (numero/ano)
FETCH_LIST = [
    ("MPV", 867, 2018, "Programa de Regularização Ambiental (PRA)"),
    ("MPV", 910, 2019, "Regularizão fundiária de ocupações"),
    ("PL", 3729, 2004, "Licenciamento ambiental"),
    ("PL", 6299, 2002, "Altera Lei dos Agrotóxicos"),
    ("PL", 2633, 2020, "Regularização Fundiária"),
    ("PL", 5028, 2019, "Política Nacional de Pagamento por serviços ambientais"),
    ("PL", 191, 2020, "Mineração em terras indígenas"),
    ("PL", 528, 2021, "Regulamenta o Mercado Brasileiro de Redução de Emissões (MBRE)"),
    ("PL", 2510, 2019, "APP urbana"),
    ("PL", 5466, 2019, "Dia dos Povos Indígenas"),
    ("PL", 4162, 2019, "Marco legal do saneamento básico"),
    ("PL", 4476, 2020, "Gás natural"),
]


def get_ids_membros_frente_parlamentar_ambientalista():
    url = f"{CAMARA_API}/frentes/54012/membros"
    response = requests.get(url)
    dados = response.json()["dados"]
    # remove rows with id None
    return list(filter(lambda row: row["id"] is not None, dados))


def get_proposicoes(
    ano: int,
    numero: int,
    url=f"{CAMARA_API}/proposicoes?numero=%d&ano=%d&ordem=ASC&ordenarPor=id&itens=100",
):
    # https://dadosabertos.camara.leg.br/api/v2/proposicoes?numero=867&ano=2018&ordem=ASC&ordenarPor=id&itens=100
    response = requests.get(url % (numero, ano))
    return response.json()


def get_proposicoes_iterator():
    for prop in FETCH_LIST:
        proposicoes = get_proposicoes(numero=prop[1], ano=prop[2])

        for row in proposicoes["dados"]:
            if row["siglaTipo"] == prop[0]:
                yield row, prop


def get_all_proposicoes_ids():
    proposicoes_ids = []

    for prop in get_proposicoes_iterator():
        proposicoes_ids.append(prop[0]["id"])

    return proposicoes_ids


def get_votacoes_proposicao(idprop: int):
    url = f"{CAMARA_API}/proposicoes/{idprop}/votacoes?ordem=DESC&ordenarPor=dataHoraRegistro"
    response = requests.get(url)
    return response.json()


def get_all_votacoes_ids_prosicao(prosicao_json):
    return list(map(lambda row: row["id"], prosicao_json["dados"]))


def get_dados_votacao(idvota: str):
    # https://dadosabertos.camara.leg.br/api/v2/votacoes/2190237-114/votos
    url = f"{CAMARA_API}/votacoes/{idvota}/votos"
    response = requests.get(url)
    return response.json()


def fetch_deputado_data(id_depudado: int):
    """
    {
    "dados": {
        "id": 204431,
        "uri": "https://dadosabertos.camara.leg.br/api/v2/deputados/204431",
        "nomeCivil": "MARCOS AURÉLIO  PÁDUA RIBEIRO GONÇALVES DE SAMPAIO",
        "ultimoStatus": {
            "id": 204431,
            "uri": "https://dadosabertos.camara.leg.br/api/v2/deputados/204431",
            "nome": "Marcos Aurélio Sampaio",
            "siglaPartido": "PSD",
            "uriPartido": "https://dadosabertos.camara.leg.br/api/v2/partidos/36834",
            "siglaUf": "PI",
            "idLegislatura": 56,
            "urlFoto": "https://www.camara.leg.br/internet/deputado/bandep/204431.jpg",
            "email": "dep.marcosaureliosampaio@camara.leg.br",
            "data": "2019-02-01T11:45",
            "nomeEleitoral": "Marcos Aurélio Sampaio",
            "gabinete": {
                "nome": "771",
                "predio": "3",
                "sala": "771",
                "andar": null,
                "telefone": "3215-5771",
                "email": "dep.marcosaureliosampaio@camara.leg.br"
            },
        "situacao": "Exercício",
        "condicaoEleitoral": "Titular",
        "descricaoStatus": null
        },
        "cpf": "01742564348",
        "sexo": "M",
        "urlWebsite": null,
        "redeSocial": [],
        "dataNascimento": "1991-09-19",
        "dataFalecimento": null,
        "ufNascimento": "PI",
        "municipioNascimento": "Teresina",
        "escolaridade": "Superior"
    },
    "links": [
        {
        "rel": "self",
        "href": "https://dadosabertos.camara.leg.br/api/v2/deputados/204431"
        }
    ]
    }
    """
    url = f"{CAMARA_API}/deputados/{id_depudado}"
    response = requests.get(url)
    return response.json()