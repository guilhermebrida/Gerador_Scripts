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
from copiloto_functions import *
import inspect


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

checkbox_names_var = {
    "Nome do Arquivo": lambda value : nome_arquivo(value),
    "Id Arquivo configurador": lambda tudo, value: id_arquivo(tudo,value),
    "Customer Child ID": lambda tudo, tag: Gera_tag(tudo,tag),
    "Limite de Velocidade (Km/h)": lambda tudo, value: limite_velocidade(tudo,value),
    "Limite de Velocidade com Chuva (Km/h)": lambda tudo, value: limite_vel_chuva(tudo,value),
    "Limite de Velocidade Carregado (Km/h)": lambda tudo, value: limite_vel_carregado(tudo,value),
    "Tempo de Tolerância à Infração de Velocidade (Segundos)": lambda tudo, value: tolerancia_infra_vel(tudo,value),
    "Freada Brusca (km/h/s)": lambda tudo, value: freada_brusca(tudo,value),
    "Limite de Aceleração Brusca (km/h/s)": lambda tudo, value: aceleracao_brusca(tudo,value),
    "Rotação de Marcha Lenta (RPM)": lambda tudo, value: marcha_lenta(tudo,value),
    "Rotação Minima de Faixa Verde (RPM)": lambda tudo, value: min_faixa_verde(tudo,value),
    "Rotação Máxima de Faixa Verde (RPM)": lambda tudo, value: max_faixa_verde(tudo,value),
    "Limite de Rotação (RPM)": lambda tudo, value: limite_rotacao(tudo,value),
    "Limite de Rotação Freio Motor (RPM)": lambda tudo, value,min_verde: freio_motor(tudo,value,min_verde),
    "Rotação para Troca de Marcha (RPM)": lambda tudo, value: troca_marcha(tudo,value),
    "Tempo de Parada com Motor Ligado (Segundos)": lambda tudo, value: parada_motor_ligado(tudo,value),
    "Tempo máximo de condução (minutos)": lambda tudo, value: tempo_max_conducao(tudo,value),
    "Tempo de descanso obrigatório (minutos)": lambda tudo, value: tempo_descanso(tudo,value),
    "Tolerância para iniciar o descanso obrigatório (minutos)": lambda tudo, value: tolerancia_descanso(tudo,value),
    "Nome da rede Lora": lambda tudo, value: lora(tudo,value)
}

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


def Insere_funcoes(hw,funcoes):
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
        return tudo

def Gerar_arquivo(hw,funcoes,parametros,ALARMES,cliente,selected_checkboxes):
    tudo = Insere_funcoes(hw,funcoes)
    for func in parametros:
        func_checkbox_name_var = checkbox_names_var.get(func)
        value = parametros[func]
        if func == "Nome do Arquivo":
            path = func_checkbox_name_var(parametros[func]) 
        elif func == "Limite de Rotação Freio Motor (RPM)":
            tudo = func_checkbox_name_var(tudo,value,parametros["Rotação Minima de Faixa Verde (RPM)"])
        else:
            tudo = func_checkbox_name_var(tudo, value)
        if "Modo Sleep"and "Condução ininterrupta" in funcoes and func == "Tempo de descanso obrigatório (minutos)":
            tudo = sleep(tudo, parametros["Tempo de descanso obrigatório (minutos)"])
    sxt = re.search('>SXT0010010101_MD1<',tudo)
    if sxt is not None:
        tudo = re.sub(">SXT0010010101_MD1<","",tudo)
        tudo = re.sub(">SSO<",">SXT0010010101_MD1<\n>SSO<",tudo)
    tudo = Gerar_alarmes(tudo,ALARMES)
    tudo = bitmap_funcionaliades(tudo, selected_checkboxes)
    res = Post_file(path, hw, cliente, tudo)
    return res

# def Post_file(path, hw, cliente, tudo):
#     if platform.system() == "Windows":
#         downloads_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
#         with open(os.path.join(downloads_path, f'{path}_{hw[0]}.txt'), 'w') as fim:
#             fim.write(tudo)
#         commit_file_to_github(os.path.join(downloads_path, f'{path}_{hw[0]}.txt'), path, hw, cliente)
#     if platform.system() == "Linux":
#         with open(f'/tmp/{path}_{hw[0]}.txt', 'w') as fim:
#             fim.write(tudo)
#         commit_file_to_github(f'/tmp/{path}_{hw[0]}.txt', path, hw, cliente)
#     res = create_pull_request(path)
#     return res
def Post_file(path, hw, cliente, tudo):
    if platform.system() == "Windows":
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        with open(os.path.join(downloads_path, f'{path}_{hw[0]}.txt'), 'w') as fim:
            fim.write(tudo)
        commit_file_to_github(os.path.join(downloads_path, f'{path}_{hw[0]}.txt'), path, hw, cliente)
    elif platform.system() == "Linux":
        with open(f'/tmp/{path}_{hw[0]}.txt', 'w') as fim:
            fim.write(tudo)
        commit_file_to_github(f'/tmp/{path}_{hw[0]}.txt', path, hw, cliente)
    res = create_pull_request(path)
    return res

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
    for index, var in enumerate(checkbox_names_var, start=1):
        input_name = 'input_' + str(index)
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
    bitmap = 0
    for i in selected_checkboxes:
        bitmap = bitmap + 2**(int(i)-1)
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
