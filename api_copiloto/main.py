from flask import Flask,jsonify,request,json,redirect,render_template, send_file,send_from_directory
from jinja2 import Template
import re
from datetime import date
import sys
import os
from decouple import config
sys.path.append('./api_copiloto/')
from validate import *
import requests
import base64
import json
import platform
from git_api import *


app = Flask(__name__)
app.static_folder = './static/css'


checkbox_hardwares = ['S8','S4','S4+','S3','S3+']

def get_checkbox_names(vl_version):
    checkbox_names = {
        "Tracking": f"./api_copiloto/funções copiloto/{vl_version}/tracking.txt",
        # "Horimetro": f"./api_copiloto/funções copiloto/{vl_version}/horimetro e tempo mov.txt",
        "Faixas RPM": f"./api_copiloto/funções copiloto/{vl_version}/faixas RPM.txt",
        "Discretas": f"./api_copiloto/funções copiloto/{vl_version}/discretas.txt",
        "Excesso RPM": f"./api_copiloto/funções copiloto/{vl_version}/excesso rpm.txt",
        "Parada motor ligado": f"./api_copiloto/funções copiloto/{vl_version}/parada motor ligado.txt",
        "Cercas": f"./api_copiloto/funções copiloto/{vl_version}/cercas.txt",
        "Limpador de parabrisa": f"./api_copiloto/funções copiloto/{vl_version}/limpador parabrisa.txt",
        "Excesso de Velocidade": f"./api_copiloto/funções copiloto/{vl_version}/excesso velocidade.txt",
        "Desaceleração brusca": f"./api_copiloto/funções copiloto/{vl_version}/desaceleracao.txt",
        "Aceleração brusca": f"./api_copiloto/funções copiloto/{vl_version}/aceleracao.txt",
        "Mifare externo": f"./api_copiloto/funções copiloto/{vl_version}/mifare.txt",
        "Mifare interno": f"./api_copiloto/funções copiloto/{vl_version}/mifare interno.txt",
        "Condução ininterrupta": f"./api_copiloto/funções copiloto/{vl_version}/conducao ininterrupta.txt",
        "Modo Sleep": f"./api_copiloto/funções copiloto/{vl_version}/sleep.txt",
        "Rotas SP": f"./api_copiloto/funções copiloto/{vl_version}/Rotas SP.txt",
        "Tablet": f"./api_copiloto/funções copiloto/{vl_version}/tablet.txt",
        "Lora": f"./api_copiloto/funções copiloto/{vl_version}/LORA.txt"
    }

    return checkbox_names

checkbox_names = {
    "Tracking": "./api_copiloto/funções copiloto/VL8/tracking.txt",
    # "Horimetro": "./api_copiloto/funções copiloto/VL8/horimetro e tempo mov.txt",
    "Faixas RPM": "./api_copiloto/funções copiloto/VL8/faixas RPM.txt",
    "Discretas": "./api_copiloto/funções copiloto/VL8/discretas.txt",
    "Excesso RPM": "./api_copiloto/funções copiloto/VL8/excesso rpm.txt",
    "Parada motor ligado": "./api_copiloto/funções copiloto/VL8/parada motor ligado.txt",
    "Cercas": "./api_copiloto/funções copiloto/VL8/cercas.txt",
    "Limpador de parabrisa": "./api_copiloto/funções copiloto/VL8/limpador parabrisa.txt",
    "Excesso de Velocidade": "./api_copiloto/funções copiloto/VL8/excesso velocidade.txt",
    "Desaceleração brusca": "./api_copiloto/funções copiloto/VL8/desaceleracao.txt",
    "Aceleração brusca": "./api_copiloto/funções copiloto/VL8/aceleracao.txt",
    "Mifare externo": "./api_copiloto/funções copiloto/VL8/mifare.txt",
    "Mifare interno": "./api_copiloto/funções copiloto/VL8/mifare interno.txt",
    "Condução ininterrupta": "./api_copiloto/funções copiloto/VL8/conducao ininterrupta.txt",
    "Modo Sleep": "./api_copiloto/funções copiloto/VL8/sleep.txt",
    "Rotas SP": "./api_copiloto/funções copiloto/VL8/Rotas SP.txt",
    "Tablet":"./api_copiloto/funções copiloto/VL8/tablet.txt",
    "Lora":"./api_copiloto/funções copiloto/VL8/LORA.txt"
}

checkbox_names_var = [
    "Nome do Arquivo",
    "Id Arquivo configurador",
    "Customer Child ID",
    "Limite de Velocidade (Km/h)",
    "Limite de Velocidade com Chuva (Km/h)",
    "Limite de Velocidade Carregado (Km/h)",
    "Tempo de Tolerância à Infração de Velocidade (Segundos)",
    "Freada Brusca (km/h/s)",
    "Limite de Aceleração Brusca (km/h/s)",
    "Rotação de Marcha Lenta (RPM)",
    "Rotação Minima de Faixa Verde (RPM)",
    "Rotação Máxima de Faixa Verde (RPM)",
    "Limite de Rotação (RPM)",
    "Limite de Rotação Freio Motor (RPM)",
    "Rotação para Troca de Marcha (RPM)",
    "Tempo de Parada com Motor Ligado (Segundos)",
    "Tempo máximo de condução (minutos)",
    "Tempo de descanso obrigatório (minutos)",
    "Tolerância para iniciar o descanso obrigatório (minutos)",
    "Nome da rede Lora"
]

checkboxes_alarmes = {
    "Pedido Motorista":268435456,
    "Pedido de Apontamento":33554432,
    "Excesso RPM":4194304,
    "Velocidade":2097152,
    "Banguela":1048576,
    "Discretas":524288,
    "Analogica":262144,
    "Temperatura Motor":131072,
    "Alternador":65536,
    "Aceleração Brusca":8192,
    "Freada Brusca":4096,
    "Cinto  de Segurança":2048,
    "Motorista Identificado":512,
    "Ignição On":256,
    "Condução Ininterrupta":32,
    "Troca de Marcha":16,
    "Troca LIV Pista Seca":8,
    "Troca LIV em Chuva":4,
    "Troca LIV em Cerca":2,
    "Parada com Motor Ligado":1
}


def Gerar_arquivo(hw,funcoes,parametros,ALARMES,cliente,selected_checkboxes):
    checkbox_names = get_checkbox_names(hw[0])
    with open(f'./api_copiloto/funções copiloto/{hw[0]}/inicio.txt', 'r') as t:
        tudo = t.read()
    for funcao in funcoes:
        if funcao in checkbox_names:
            if funcao == "Rotas SP":
                continue
            with open(checkbox_names[funcao], 'r') as t:
                tudo += '\n' + t.read()
    with open(f'./api_copiloto/funções copiloto/{hw[0]}/log.txt', 'r') as t:
        tudo += '\n' + t.read()
    if "Rotas SP" in funcoes:
        with open(f'./api_copiloto/funções copiloto/{hw[0]}/Rotas SP.txt', 'r') as t:
            tudo += '\n' + t.read()
    with open(f'./api_copiloto/funções copiloto/{hw[0]}/fim.txt', 'r') as t:
        tudo += '\n' + t.read()
    for func in parametros:
        strategy = strategy_map.get(func)
        if strategy:
            value = parametros[func]
            tudo = strategy(tudo, value)
        if func == "Customer Child ID":
            tudo = Gera_tag(tudo,parametros[func])
        # if func == "Limite de Velocidade (Km/h)":
        #     lim_vel = parametros[func]
        #     tudo = re.sub(">SCT11.*<",f'>SCT11 {lim_vel}900<', tudo)
        # if func == "Limite de Velocidade com Chuva (Km/h)":
        #     lim_vel_chuva = parametros[func]
        #     tudo = re.sub(">SCT12.*<",f'>SCT12 {lim_vel_chuva}900<', tudo)
        # if func == "Limite de Velocidade Carregado (Km/h)":
        #     lim_vel_carregado = parametros[func]
        #     tudo = re.sub(">SCT13.*<",f'>SCT13 {lim_vel_carregado}900<', tudo)
        # if func == "Tempo de Tolerância à Infração de Velocidade (Segundos)":
        #     tolerancia_vel = parametros[func]
        #     tudo = re.sub(">SCT06.*<",f'>SCT06 {tolerancia_vel}<', tudo)
        # if func == "Freada Brusca (km/h/s)":
        #     freada = parametros[func]
        #     tudo = re.sub(">SCT08.*<",f'>SCT08 0-{freada}<', tudo)
        # if func == "Limite de Aceleração Brusca (km/h/s)":
        #     acel = parametros[func]
        #     tudo = re.sub(">SCT09.*<",f'>SCT09 {acel}<', tudo)
        # if func == "Rotação de Marcha Lenta (RPM)":
        #     lenta = parametros[func]
        #     if re.search('>SUT11.*<',tudo) is not None:
        #         sut11 = re.search('>SUT11.*<',tudo).group()
        #         tudo = re.sub(sut11.split(',')[-1],f'{lenta}<',tudo)
        # if func == "Rotação Minima de Faixa Verde (RPM)":
        #     min_verde = parametros[func]
        #     if re.search('>SUT12.*<',tudo) is not None:
        #         sut12 = re.search('>SUT12.*<',tudo).group()
        #         tudo = re.sub(sut12.split(',')[-2],f'{min_verde}',tudo)
        # if func == "Rotação Máxima de Faixa Verde (RPM)":
        #     max_verde = parametros[func]
        #     if re.search('>SUT12.*<',tudo) is not None:
        #         sut12 = re.search('>SUT12.*<',tudo).group()
        #         tudo = re.sub(sut12.split(',')[-1],f'{max_verde}<',tudo)
        # if func == "Limite de Rotação (RPM)":
        #     excesso = parametros[func]
        #     if re.search('>SUT13.*<',tudo) is not None:
        #         sut13 = re.search('>SUT13.*<',tudo).group()
        #         tudo = re.sub(sut13.split(',')[-2],f'{excesso}',tudo)
        if func == "Limite de Rotação Freio Motor (RPM)":
            freio_motor = parametros[func]
            if freio_motor != '9999':
                tudo = re.sub('>SUT14.*<',f'>SUT14,QCT27,7,15,{min_verde},{int(freio_motor)-1}<',tudo)
                tudo = re.sub('>SUT15.*<',f'>SUT15,QCT27,7,15,{freio_motor},9999<',tudo)
        # if func == "Rotação para Troca de Marcha (RPM)":
        #     troca = parametros[func]
        #     tudo = re.sub('>SUT16.*<',f'>SUT16,QCT27,7,15,{troca},9999<',tudo)
        # if func == "Tempo de Parada com Motor Ligado (Segundos)":
        #     tempo_parada = parametros[func]
        #     tudo = re.sub(">SCT04.*<",f'>SCT04 {tempo_parada}<', tudo)
        # if func == "Tempo máximo de condução (minutos)":
        #     tempo_max_cond = parametros[func]
        #     tudo = re.sub(">SCT14.*<",f'>SCT14 {int(tempo_max_cond)*60}<', tudo)
        # if func == "Tempo de descanso obrigatório (minutos)":
        #     descanso_obrigatorio = parametros[func]
        #     tudo = re.sub(">SCT17.*<",f'>SCT17 {int(descanso_obrigatorio)*60}<', tudo)
        # if func == "Tolerância para iniciar o descanso obrigatório (minutos)":
        #     tol_descanso = parametros[func]
        #     tudo = re.sub(">SCT15.*<",f'>SCT15 {int(tol_descanso)*60}<', tudo)
        # if func == "Nome da rede Lora":
        #     rede_lora = ''.join(str(ord(char)) for char in parametros[func])
        #     tudo = re.sub('000102030405060708090A0B0C0D0E0F',rede_lora,tudo)
        if func == "Id Arquivo configurador":
            tp = parametros[func]
            tp = re.sub(" ", "_",tp)
            versao = str(date.today())
            versao = versao.replace('-', '')[-6::]
            tudo = re.sub(">STP01.*<",f">STP01 {tp}.{versao}<",tudo)
        if func == "Nome do Arquivo":
            path = parametros[func]
            path = re.sub(" ", "_",path)
        if "Modo Sleep"and "Condução ininterrupta" in funcoes and func == "Tempo de descanso obrigatório (minutos)":
            sleep = str(int(descanso_obrigatorio)*60+300).zfill(4)
            tudo = re.sub('>VSKO0600060000900120_INS1_CAN1_EVP1800<',f'>VSKO{sleep}{sleep}00900120_INS1_CAN1_EVP1800<',tudo)
    sxt = re.search('>SXT0010010101_MD1<',tudo)
    if sxt is not None:
        tudo = re.sub(">SXT0010010101_MD1<","",tudo)
        tudo = re.sub(">SSO<",">SXT0010010101_MD1<\n>SSO<",tudo)
    tudo = Gerar_alarmes(tudo,ALARMES)
    tudo = bitmap_funcionaliades(tudo, selected_checkboxes)
    if platform.system() == "Windows":
        with open(f'C:/Users/user/Downloads/{path}_{hw[0]}.txt', 'w') as fim:
            fim.write(tudo)
        commit_file_to_github(f'C:/Users/user/Downloads/{path}_{hw[0]}.txt', path, hw, cliente)
    if platform.system() == "Linux":
        with open(f'/tmp/{path}_{hw[0]}.txt', 'w') as fim:
            fim.write(tudo)
        commit_file_to_github(f'/tmp/{path}_{hw[0]}.txt', path, hw, cliente)
    res = create_pull_request(path)
    return res


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

def freio_motor(tudo, value):
    ...

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

def Gera_tag(tudo,tag):
    return f'//[cc.id]{tag}[cc.id]\n\n' + tudo

def Gerar_alarmes(tudo,alarmes):
    sct16 = 0
    for alarme in alarmes:
        sct16 = sct16 + checkboxes_alarmes[alarme]
    if sct16:
        tudo = re.sub(">SCT16 768<",f">SCT16 {sct16}<",tudo)
    return tudo

def Hardwares(hw):
    if hw == 'S8':
        return ['VL8','Virloc8']
    if hw == 'S4':
        return ['VC5', 'Vircom5']
    if hw == 'S4+':
        return ['VC7','Vircom7']
    if hw == 'S3':
        return ['VL10','Virloc10']
    if hw == 'S3+':
        return ['VL12','Virloc12']
    if hw == 'S1':
        return ['VL6', 'Virloc6']

def Get_values(checkbox_names_var):
    values = {}
    for var in checkbox_names_var:
        input_name = 'input_' + str(checkbox_names_var.index(var)+1)
        value = request.form.get(input_name)
        if value:
            values[var] = value
    return values

def Get_checkboxes(selected_checkboxes):
    funcoes = []
    for checkbox in selected_checkboxes:
        chaves = list(checkbox_names.keys())
        parameter_name = chaves[int(checkbox)-1]
        funcoes.append(parameter_name)
    return funcoes

def Get_alarms(alarme_escolhido):
    ALARMES = []
    for alarm in alarme_escolhido:
        chaves = list(checkboxes_alarmes.keys())
        parameter_name = chaves[int(alarm)-1]
        ALARMES.append(parameter_name)
    return ALARMES

def bitmap_funcionaliades(tudo,selected_checkboxes):
    bitmap = 1
    for i in selected_checkboxes:
        bitmap = bitmap + 2**int(i)
    tudo = re.sub('>STP15 1<',f'>STP15 {bitmap}<',tudo)
    return tudo



@app.route('/')
def index():
    checkboxes = zip(range(1, len(checkbox_names) + 1), checkbox_names)
    checkboxes_var = zip(range(1, len(checkbox_names_var) + 1), checkbox_names_var)
    checkbox_alarmes = zip(range(1, len(checkboxes_alarmes) + 1), checkboxes_alarmes)
    checkboxes_hw = zip(range(1, len(checkbox_hardwares) + 1), checkbox_hardwares)
    return render_template('index.html', checkboxes=checkboxes, checkboxes_var=checkboxes_var, alarmes=checkbox_alarmes, hardwares=checkboxes_hw)


@app.route('/submit', methods=['POST'])
def submit():
    cliente = request.form.get('cliente')
    selected_checkboxes = request.form.getlist('checkbox')
    selected_hardwares = request.form.getlist('hw')
    alarme_escolhido = request.form.getlist('alarme')
    none_hw = hardwares_is_None(selected_hardwares)
    if none_hw:
        return render_template('popup.html', none_hw=none_hw)
    hw_escolhido = str(checkbox_hardwares[int(selected_hardwares[0])-1])
    hw = Hardwares(hw_escolhido)
    hardwares_condition = validate_hardwares(selected_hardwares)
    condition = validate_checkboxes(selected_checkboxes)
    funcoes = Get_checkboxes(selected_checkboxes)
    values = Get_values(checkbox_names_var)
    validate = validate_path(values)
    validate_cc = validate_cc_id(values)
    ALARMES = Get_alarms(alarme_escolhido)
    valida_funcao = validate_function(selected_hardwares,selected_checkboxes)
    valida_mifare = validate_mifares(selected_checkboxes)
    if valida_mifare:
        return render_template('popup.html',valida_mifare=valida_mifare)
    if valida_funcao:
        return render_template('popup.html',valida_funcao=valida_funcao)
    if hardwares_condition:
        return render_template('popup.html', hardwares_condition=hardwares_condition)
    if condition:
        return render_template('popup.html', condition=condition)
    if validate:
        return render_template('popup.html', validate=validate)
    if validate_cc:
        return render_template('popup.html', validate_cc=validate_cc)
    res = Gerar_arquivo(hw,funcoes,values,ALARMES,cliente,selected_checkboxes)
    return render_template('submit.html', hardware=hw_escolhido,cliente=cliente,funcoes=funcoes,values=values,
                            alarmes=ALARMES,status_code=res[0],pull_request=res[1])
 

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)


if __name__ == '__main__':
  app.run(host="0.0.0.0",debug=True)
