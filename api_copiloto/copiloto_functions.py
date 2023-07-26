import re
from datetime import date

def limite_velocidade(tudo,value):
    return re.sub(">SCT11.*<",f'>SCT11 {value}900<', tudo)

def limite_vel_chuva(tudo,value):
    return re.sub(">SCT12.*<",f'>SCT12 {value}900<', tudo)

def limite_vel_carregado(tudo,value):
    return re.sub(">SCT13.*<",f'>SCT13 {value}900<', tudo)

def tolerancia_infra_vel(tudo,value):
    return re.sub(">SCT06.*<",f'>SCT06 {value}<', tudo)

def freada_brusca(tudo,value):
    return re.sub(">SCT08.*<",f'>SCT08 0-{value}<', tudo)

def aceleracao_brusca(tudo,value):
    return re.sub(">SCT09.*<",f'>SCT09 {value}<', tudo)

def marcha_lenta(tudo,value):
    if re.search('>SUT11.*<',tudo) is not None:
        sut11 = re.search('>SUT11.*<',tudo).group()
        return re.sub(sut11.split(',')[-1],f'{value}<',tudo)

def min_faixa_verde(tudo,value):
    if re.search('>SUT12.*<',tudo) is not None:
        sut12 = re.search('>SUT12.*<',tudo).group()
        return re.sub(sut12.split(',')[-2],f'{value}',tudo)

def max_faixa_verde(tudo,value):
    if re.search('>SUT12.*<',tudo) is not None:
        sut12 = re.search('>SUT12.*<',tudo).group()
        return re.sub(sut12.split(',')[-1],f'{value}<',tudo)

def limite_rotacao(tudo, value):
    if re.search('>SUT13.*<',tudo) is not None:
        sut13 = re.search('>SUT13.*<',tudo).group()
        return re.sub(sut13.split(',')[-2],f'{value}',tudo)

def freio_motor(tudo, value, min_verde):
    if freio_motor != '9999':
        tudo = re.sub('>SUT14.*<',f'>SUT14,QCT27,7,15,{min_verde},{int(value)-1}<',tudo)
        return re.sub('>SUT15.*<',f'>SUT15,QCT27,7,15,{value},9999<',tudo)

def troca_marcha(tudo, value):
    return re.sub('>SUT16.*<',f'>SUT16,QCT27,7,15,{value},9999<',tudo)

def parada_motor_ligado(tudo, value):
    return re.sub(">SCT04.*<",f'>SCT04 {value}<', tudo)

def tempo_max_conducao(tudo, value):
    return re.sub(">SCT14.*<",f'>SCT14 {int(value)*60}<', tudo)

def tempo_descanso(tudo, value):
    return re.sub(">SCT17.*<",f'>SCT17 {int(value)*60}<', tudo)

def tolerancia_descanso(tudo, value):
    return re.sub(">SCT15.*<",f'>SCT15 {int(value)*60}<', tudo)

def lora(tudo, value):
    rede_lora = ''.join(str(ord(char)) for char in value)
    return re.sub('000102030405060708090A0B0C0D0E0F',rede_lora,tudo)

def id_arquivo(tudo, value):
    tp = value
    tp = re.sub(" ", "_",tp)
    versao = str(date.today())
    versao = versao.replace('-', '')[-6::]
    return re.sub(">STP01.*<",f">STP01 {tp}.{versao}<",tudo)

def nome_arquivo(value):
    path = value
    path = re.sub(" ", "_",path)
    return path

def sleep(tudo, value):
    sleep = str(int(value)*60+300).zfill(4)
    return re.sub('>VSKO0600060000900120_INS1_CAN1_EVP1800<',f'>VSKO{sleep}{sleep}00900120_INS1_CAN1_EVP1800<',tudo)
