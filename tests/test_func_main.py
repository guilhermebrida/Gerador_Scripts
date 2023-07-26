from api_copiloto.main import *
import pytest
import requests_mock
from unittest.mock import Mock, mock_open, patch
from unittest import mock
import requests
import sys
from flask_testing import TestCase
sys.path.append('C:/Python_scripts/Gerador_Scripts/api_copiloto/')



def test_deve_receber_um_customer_child_id_e_retornar_como_uma_tag():
    child_id = 123456
    assert Gera_tag('teste', child_id) == '//[cc.id]123456[cc.id]\n\nteste'


def test_deve_receber_S8_e_retornar_VL8():
    assert Hardwares('S8') == ['VL8', 'Virloc8']


def test_deve_receber_S3_e_retornar_VL10():
    assert Hardwares('S3') == ['VL10', 'Virloc10']


def test_deve_receber_S3mais_e_retornar_VL12():
    assert Hardwares('S3+') == ['VL12', 'Virloc12']


def test_deve_receber_S4mais_e_retornar_VC7():
    assert Hardwares('S4+') == ['VC7', 'Vircom7']


def test_deve_receber_S4_e_retornar_VC5():
    assert Hardwares('S4') == ['VC5', 'Vircom5']


def test_recebe_script_copiloto_retorna_ct16_com_valor_de_todos_os_alarmes_ativos():
    assert (
        Gerar_alarmes('>SCT16 768<', checkboxes_alarmes) == '>SCT16 310328127<'
    )


def test_recebe_lista_com_indice_dos_alarmes_escolhidos_e_retorna_lista_com_os_nomes():
    lista_alarmes = [
        'Pedido Motorista',
        'Pedido de Apontamento',
        'Excesso RPM',
        'Velocidade',
        'Banguela',
        'Discretas',
        'Analogica',
        'Temperatura Motor',
        'Alternador',
        'Aceleração Brusca',
        'Freada Brusca',
        'Cinto  de Segurança',
        'Motorista Identificado',
        'Ignição On',
        'Condução Ininterrupta',
        'Troca de Marcha',
        'Troca LIV Pista Seca',
        'Troca LIV em Chuva',
        'Troca LIV em Cerca',
        'Parada com Motor Ligado',
    ]

    assert (
        Get_alarms(
            ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20',]
        )
        == lista_alarmes
    )


def test_recebe_lista_com_indice_das_funcionalidades_escolhidas_e_retorna_lista_com_os_nomes():
    lista_nomes = [
        'Tracking',
        'Faixas RPM',
        'Discretas',
        'Excesso RPM',
        'Parada motor ligado',
        'Cercas',
        'Limpador de parabrisa',
        'Excesso de Velocidade',
        'Desaceleração brusca',
        'Aceleração brusca',
        'Mifare externo',
        'Condução ininterrupta',
        'Modo Sleep',
        'Tablet',
        'Lora',
    ]
    checkbox_marcada = ['1','2','3','4','5','6','7','8','9','10','11','13','14','16','17',]
    assert Get_checkboxes(checkbox_marcada) == lista_nomes


def test_deve_retornar_os_limites_de_dirigibilidade(monkeypatch):
    app = Flask(__name__)
    input_values = {
        'input_1': 'teste',
        'input_2': 'teste',
        'input_3': '111',
        'input_4': '100',
        'input_5': '100',
        'input_6': '100',
        'input_7': '10',
        'input_8': '15',
        'input_9': '15',
        'input_10': '800',
        'input_11': '1100',
        'input_12': '2200',
        'input_13': '3000',
        'input_14': '9999',
        'input_15': '1700',
        'input_16': '300',
        'input_17': '180',
        'input_18': '30',
        'input_19': '30',
        'input_20': 'TESTE',
    }
    assert_values = {
        'Nome do Arquivo': 'teste',
        'Id Arquivo configurador': 'teste',
        'Customer Child ID': '111',
        'Limite de Velocidade (Km/h)': '100',
        'Limite de Velocidade com Chuva (Km/h)': '100',
        'Limite de Velocidade Carregado (Km/h)': '100',
        'Tempo de Tolerância à Infração de Velocidade (Segundos)': '10',
        'Freada Brusca (km/h/s)': '15',
        'Limite de Aceleração Brusca (km/h/s)': '15',
        'Rotação de Marcha Lenta (RPM)': '800',
        'Rotação Minima de Faixa Verde (RPM)': '1100',
        'Rotação Máxima de Faixa Verde (RPM)': '2200',
        'Limite de Rotação (RPM)': '3000',
        'Limite de Rotação Freio Motor (RPM)': '9999',
        'Rotação para Troca de Marcha (RPM)': '1700',
        'Tempo de Parada com Motor Ligado (Segundos)': '300',
        'Tempo máximo de condução (minutos)': '180',
        'Tempo de descanso obrigatório (minutos)': '30',
        'Tolerância para iniciar o descanso obrigatório (minutos)': '30',
        'Nome da rede Lora': 'TESTE',
    }

    def mock_request_form_get(input_name):
        return input_values.get(input_name)

    with app.test_request_context():
        monkeypatch.setattr(request.form, 'get', mock_request_form_get)
        result = Get_values(checkbox_names_var)
        assert result == assert_values

@mock.patch('api_copiloto.main.Post_file')
def test_deve_retornar_ur_arquivo_com_os_parametros(
     mock_post_file, monkeypatch
):
    arquivo = 'arquivo teste\n>SUT11,QCT27,7,15,400,800<\n>SUT12,QCT27,7,15,1111,2222<\n \
                >SUT13,QCT27,7,15,3333,9999<\n>SUT14,QCT27,7,15,1111,4443<\n \
                >SUT15,QCT27,7,15,4444,9999< \n>SXT0010010101_MD1<'
    funcoes = [
        'Tracking',
        'Faixas RPM',
        'Discretas',
        'Excesso RPM',
        'Parada motor ligado',
        'Cercas',
        'Limpador de parabrisa',
        'Excesso de Velocidade',
        'Desaceleração brusca',
        'Aceleração brusca',
        'Mifare externo',
        'Condução ininterrupta',
        'Modo Sleep',
        'Rotas SP',
        'Tablet',
        'Lora',
    ]
    parametros = {
        'Nome do Arquivo': 'teste',
        'Id Arquivo configurador': 'teste',
        'Customer Child ID': '111',
        'Limite de Velocidade (Km/h)': '100',
        'Limite de Velocidade com Chuva (Km/h)': '100',
        'Limite de Velocidade Carregado (Km/h)': '100',
        'Tempo de Tolerância à Infração de Velocidade (Segundos)': '10',
        'Freada Brusca (km/h/s)': '15',
        'Limite de Aceleração Brusca (km/h/s)': '15',
        'Rotação de Marcha Lenta (RPM)': '800',
        'Rotação Minima de Faixa Verde (RPM)': '1100',
        'Rotação Máxima de Faixa Verde (RPM)': '2200',
        'Limite de Rotação (RPM)': '3000',
        'Limite de Rotação Freio Motor (RPM)': '9999',
        'Rotação para Troca de Marcha (RPM)': '1700',
        'Tempo de Parada com Motor Ligado (Segundos)': '300',
        'Tempo máximo de condução (minutos)': '180',
        'Tempo de descanso obrigatório (minutos)': '30',
        'Tolerância para iniciar o descanso obrigatório (minutos)': '30',
        'Nome da rede Lora': 'TESTE',
    }
    ALARMES = [
        'Pedido Motorista',
        'Pedido de Apontamento',
        'Excesso RPM',
        'Velocidade',
        'Discretas',
        'Aceleração Brusca',
        'Freada Brusca',
        'Motorista Identificado',
        'Ignição On',
        'Parada com Motor Ligado',
    ]

    mock_post_file.return_value = [201, 'Pull Request OK']
    with patch(
        'builtins.open', mock_open(read_data=arquivo)
    ) as mock_open_file:
        resultado = Gerar_arquivo('S8', funcoes, parametros, ALARMES, 'teste',['1'])
        assert resultado[0] == 201
        assert resultado[1] == 'Pull Request OK'


def test_deve_retornar_bitmap_para_as_primeiras_10_funcionalidades_escolhidas():
    checkbox_marcadas = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    assert bitmap_funcionaliades('>STP15 1<',checkbox_marcadas) == '>STP15 2047<'


@mock.patch('api_copiloto.main.platform.system')
@mock.patch('api_copiloto.main.create_pull_request')
@mock.patch('api_copiloto.main.commit_file_to_github')
def test_deve_postar_arquivo_no_git_maquina_windows(mock_commit,mock_pull,mock_sys):
    if platform.system() == 'Windows':
        mock_sys.return_value = 'Windows'
        mock_commit.return_value = 201
        mock_pull.return_value = [201, 'Pull Request OK']
        with patch(
            'builtins.open', mock_open(read_data='arquivo teste')
        ) as mock_open_file:
            resultado = Post_file('path/teste', ['1'], 'teste','tudo')
            assert resultado[0] == 201
            assert resultado[1] == 'Pull Request OK'


@mock.patch('api_copiloto.main.platform.system')
@mock.patch('api_copiloto.main.create_pull_request')
@mock.patch('api_copiloto.main.commit_file_to_github')
def test_deve_postar_arquivo_no_git_maquina_Linux(mock_commit,mock_pull,mock_sys):
    if platform.system() == 'Linux':
        mock_sys.return_value = 'Linux'
        mock_commit.return_value = 201
        mock_pull.return_value = [201, 'Pull Request OK']
        with patch(
            'builtins.open', mock_open(read_data='arquivo teste')
        ) as mock_open_file:
            resultado = Post_file('path/teste', ['1'], 'teste','tudo')
            assert resultado[0] == 201
            assert resultado[1] == 'Pull Request OK'