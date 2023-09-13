from api_copiloto.backend.validate import *
import pytest

def test_deve_retornar_True_caso_Customer_Child_ID_nao_esteja_na_lista_de_parametro():
    cc = 'qualquer coisa'
    assert validate_cc_id(cc) == True 

def test_deve_retornar_False_caso_Customer_Child_ID_esteja_na_lista_de_parametro():
    cc = 'Customer Child ID'
    assert validate_cc_id(cc) == False 

@pytest.mark.parametrize('hw',('2','4','5','6'))
def test_deve_retornar_True_caso_Lora_nao_compativel_com_hw(hw):
    assert validate_function([hw],['17']) == True

@pytest.mark.parametrize('hw',('2','3','6'))
def test_deve_retornar_True_caso_Tablet_nao_compativel_com_hw(hw):
    assert validate_function([hw],['16']) == True

@pytest.mark.parametrize('hw',('4','5'))
def test_deve_retornar_True_caso_Sleep_nao_compativel_com_hw(hw):
    assert validate_function([hw],['14']) == True

def test_retorna_true_se_mifare_externo_e_interno_estiverem_marcados():
    assert validate_mifares(['11','12']) == True

def test_retorna_true_se_cercas_e_rotas_SP_estiverem_marcados():
    assert validate_checkboxes(['6','15']) == True

def test_retorna_true_se_nenhum_hw_foi_escolhido():
    assert hardwares_is_None([]) == True

@pytest.mark.parametrize('hw',(['1','2'],['1','2','3'],['1','2','3','4'],['1','2','3','4','5'],['1','2','3','4','5','6']))
def test_retorna_true_se_mais_de_um_hw_foi_escolhido(hw):
    assert validate_hardwares(hw) == True

@pytest.mark.parametrize('values',("Nome do Arquivo","Id Arquivo configurador"))
def test_deve_retornar_True_caso_nao_tenha_nome_no_arquivo(values):
    assert validate_path([values]) == True

def test_deve_retornar_false_caso_tenha_nome_no_arquivo():
    assert validate_path({'Nome do Arquivo': 'aaa', 'Id Arquivo configurador': 'aaa'}) == False

@pytest.mark.parametrize('hw',(['2','4','5','6']))
def test_deve_retornar_true_caso_escolha_mifare_interno_com_hw_que_nao_possui(hw):
    assert validate_function([hw],['12']) == True
