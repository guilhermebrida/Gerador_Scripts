from api_copiloto.main import *


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
    assert Gerar_alarmes(
        '>SCT16 768<', checkboxes_alarmes) == '>SCT16 310328127<'


def test_recebe_lista_com_indice_dos_alarmes_escolhidos_e_retorna_lista_com_os_nomes():
    lista_alarmes = ['Pedido Motorista', 'Pedido de Apontamento', 'Excesso RPM', 'Velocidade', 'Banguela',
                     'Discretas', 'Analogica', 'Temperatura Motor', 'Alternador', 'Aceleração Brusca',
                     'Freada Brusca', 'Cinto  de Segurança', 'Motorista Identificado', 'Ignição On',
                     'Condução Ininterrupta', 'Troca de Marcha', 'Troca LIV Pista Seca', 'Troca LIV em Chuva',
                     'Troca LIV em Cerca', 'Parada com Motor Ligado']

    assert Get_alarms(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                       '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']) == lista_alarmes


def test_recebe_lista_com_indice_das_funcionalidades_escolhidas_e_retorna_lista_com_os_nomes():
    lista_nomes = ['Tracking', 'Faixas RPM', 'Discretas', 'Excesso RPM', 'Parada motor ligado', 'Cercas', 'Limpador de parabrisa',
                   'Excesso de Velocidade', 'Desaceleração brusca', 'Aceleração brusca', 'Mifare externo', 'Condução ininterrupta',
                   'Modo Sleep', 'Tablet', 'Lora']
    checkbox_marcada = ['1', '2', '3', '4', '5', '6',
                        '7', '8', '9', '10', '11', '13', '14', '16', '17']
    assert Get_checkboxes(checkbox_marcada) == lista_nomes


# def test_deve_retornar_lista_com_os_clientes_existentes_VL8():
#     LISTA = ['April', 'ArcelorMittal', 'Bayer', 'Bracell Bahia', 'Bracell', 'CMOC', 'CMPC', 'CPFL',
#              'Corteva', 'Expresso Nepomuceno', 'Forest', 'JSL', 'MSC', 'Raizen', 'Sirtec', 'Suzano ES', 'Suzano MS', 'Syngenta',
#              'Terceira Vale', 'VLI', 'Valenet', 'Vecchiola', 'Veracel']

#     assert lista_clientes(hw) == LISTA


