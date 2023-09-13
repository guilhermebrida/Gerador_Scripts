from flask import Flask,jsonify,request,json,redirect,render_template, send_file,send_from_directory
from jinja2 import Template
import re
from datetime import date
import sys
import os
from decouple import config, RepositoryEnv,Config,AutoConfig
sys.path.append('./api_copiloto/backend/')
from validate import *
import requests
import base64
import json
import platform
from git_api import *
from copiloto_functions import *
import inspect


app = Flask(__name__)
app.static_folder = '../frontend/static'
app.template_folder = '../frontend/templates'

PATH = './api_copiloto/backend/funcoes_copiloto'

checkbox_hardwares = ['S8','S4','S4+','S3','S3+']

def criar_env_js():
    try:
        token = Get_token()
        if token is not None:
            with open('./api_copiloto/frontend/static/js/env.js', 'w') as f:
                f.write(f'window.TOKEN_GITHUB = "{token}"')
        else:
            print("A variável de ambiente TOKEN_GITHUB não está definida.")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")


def get_checkbox_names(vl_version):
    checkbox_names = {
        "Tracking": f"{PATH}/{vl_version}/tracking.txt",
        # "Horimetro": f"{PATH}/{vl_version}/horimetro e tempo mov.txt",
        "Faixas RPM": f"{PATH}/{vl_version}/faixas RPM.txt",
        "Discretas": f"{PATH}/{vl_version}/discretas.txt",
        "Excesso RPM": f"{PATH}/{vl_version}/excesso rpm.txt",
        "Parada motor ligado": f"{PATH}/{vl_version}/parada motor ligado.txt",
        "Cercas": f"{PATH}/{vl_version}/cercas.txt",
        "Limpador de parabrisa": f"{PATH}/{vl_version}/limpador parabrisa.txt",
        "Excesso de Velocidade": f"{PATH}/{vl_version}/excesso velocidade.txt",
        "Desaceleração brusca": f"{PATH}/{vl_version}/desaceleracao.txt",
        "Aceleração brusca": f"{PATH}/{vl_version}/aceleracao.txt",
        "Mifare externo": f"{PATH}/{vl_version}/mifare.txt",
        "Mifare interno": f"{PATH}/{vl_version}/mifare interno.txt",
        "Condução ininterrupta": f"{PATH}/{vl_version}/conducao ininterrupta.txt",
        "Modo Sleep": f"{PATH}/{vl_version}/sleep.txt",
        "Rotas SP": f"{PATH}/{vl_version}/Rotas SP.txt",
        "Tablet": f"{PATH}/{vl_version}/tablet.txt",
        "Lora": f"{PATH}/{vl_version}/LORA.txt"
    }

    return checkbox_names

checkbox_names = {
    "Tracking": f"{PATH}/VL8/tracking.txt",
    # "Horimetro": f"{PATH}/VL8/horimetro e tempo mov.txt",
    "Faixas RPM": f"{PATH}/VL8/faixas RPM.txt",
    "Discretas": f"{PATH}/VL8/discretas.txt",
    "Excesso RPM": f"{PATH}/VL8/excesso rpm.txt",
    "Parada motor ligado": f"{PATH}/VL8/parada motor ligado.txt",
    "Cercas": f"{PATH}/VL8/cercas.txt",
    "Limpador de parabrisa": f"{PATH}/VL8/limpador parabrisa.txt",
    "Excesso de Velocidade": f"{PATH}/VL8/excesso velocidade.txt",
    "Desaceleração brusca": f"{PATH}/VL8/desaceleracao.txt",
    "Aceleração brusca": f"{PATH}/VL8/aceleracao.txt",
    "Mifare externo": f"{PATH}/VL8/mifare.txt",
    "Mifare interno": f"{PATH}/VL8/mifare interno.txt",
    "Condução ininterrupta": f"{PATH}/VL8/conducao ininterrupta.txt",
    "Modo Sleep": f"{PATH}/VL8/sleep.txt",
    "Rotas SP": f"{PATH}/VL8/Rotas SP.txt",
    "Tablet": f"{PATH}/VL8/tablet.txt",
    "Lora": f"{PATH}/VL8/LORA.txt"
}

checkbox_names_var = {
    "Nome do Arquivo": lambda value: Copiloto().nome_arquivo(value),
    "Id Arquivo configurador": lambda tudo, value, hardware: Copiloto(tudo,hardware).id_arquivo(value),
    "Customer Child ID": lambda tudo, tag, hardware: Gera_tag(tudo, tag ),
    "Limite de Velocidade (Km/h)": lambda tudo, value, hardware: Copiloto(tudo,hardware).limite_velocidade(value),
    "Limite de Velocidade com Chuva (Km/h)": lambda tudo, value, hardware: Copiloto(tudo,hardware).limite_vel_chuva(value),
    "Limite de Velocidade Carregado (Km/h)": lambda tudo, value, hardware: Copiloto(tudo,hardware).limite_vel_carregado(value),
    "Tempo de Tolerância à Infração de Velocidade (Segundos)": lambda tudo, value, hardware: Copiloto(tudo,hardware).tolerancia_infra_vel(value),
    "Freada Brusca (km/h/s)": lambda tudo, value, hardware: Copiloto(tudo,hardware).freada_brusca(value),
    "Limite de Aceleração Brusca (km/h/s)": lambda tudo, value, hardware: Copiloto(tudo,hardware).aceleracao_brusca(value),
    "Rotação de Marcha Lenta (RPM)": lambda tudo, value, hardware: Copiloto(tudo,hardware).marcha_lenta(value),
    "Rotação Minima de Faixa Verde (RPM)": lambda tudo, value, hardware: Copiloto(tudo,hardware).min_faixa_verde(value),
    "Rotação Máxima de Faixa Verde (RPM)": lambda tudo, value, hardware: Copiloto(tudo,hardware).max_faixa_verde(value),
    "Limite de Rotação (RPM)": lambda tudo, value, hardware: Copiloto(tudo,hardware).limite_rotacao(value),
    "Limite de Rotação Freio Motor (RPM)": lambda tudo, value, min_verde, hardware: Copiloto(tudo,hardware).freio_motor(value, min_verde),
    "Rotação para Troca de Marcha (RPM)": lambda tudo, value, hardware: Copiloto(tudo,hardware).troca_marcha(value),
    "Tempo de Parada com Motor Ligado (Segundos)": lambda tudo, value, hardware: Copiloto(tudo,hardware).parada_motor_ligado(value),
    "Tempo máximo de condução (minutos)": lambda tudo, value, hardware: Copiloto(tudo,hardware).tempo_max_conducao(value),
    "Tempo de descanso obrigatório (minutos)": lambda tudo, value, hardware: Copiloto(tudo,hardware).tempo_descanso(value),
    "Tolerância para iniciar o descanso obrigatório (minutos)": lambda tudo, value, hardware: Copiloto(tudo,hardware).tolerancia_descanso(value),
    "Nome da rede Lora": lambda tudo, value, hardware: Copiloto(tudo,hardware).lora(value)
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
    with open(f'{PATH}/{hw[0]}/inicio.txt', 'r') as t:
        tudo = t.read()
    for funcao in funcoes:
        if funcao in checkbox_names:
            if funcao == "Rotas SP":
                continue
            with open(checkbox_names[funcao], 'r') as t:
                tudo += '\n' + t.read()
    with open(f'{PATH}/{hw[0]}/log.txt', 'r') as t:
        tudo += '\n' + t.read()
    if "Rotas SP" in funcoes:
        with open(f'{PATH}/{hw[0]}/Rotas SP.txt', 'r') as t:
            tudo += '\n' + t.read()
    with open(f'{PATH}/{hw[0]}/fim.txt', 'r') as t:
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
            tudo = func_checkbox_name_var(tudo,value,parametros["Rotação Minima de Faixa Verde (RPM)"],hw[0])
        else:
            tudo = func_checkbox_name_var(tudo, value,hw[0])
        if "Modo Sleep"and "Condução ininterrupta" in funcoes and func == "Tempo de descanso obrigatório (minutos)":
            tudo = Copiloto(tudo).sleep( parametros["Tempo de descanso obrigatório (minutos)"])
    sxt = re.search('>SXT0010010101_MD1<',tudo)
    if sxt is not None:
        tudo = re.sub(">SXT0010010101_MD1<","",tudo)
        tudo = re.sub(">SSO<",">SXT0010010101_MD1<\n>SSO<",tudo)
    tudo = Gerar_alarmes(tudo,ALARMES)
    tudo = bitmap_funcionaliades(tudo, selected_checkboxes)
    res = Post_file(path, hw, cliente, tudo)
    return res

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
    criar_env_js()
    # app.run(host="0.0.0.0", debug=False)
    from gunicorn.app.base import BaseApplication

    class FlaskApp(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            for key, value in self.options.items():
                if key in self.cfg.settings and value is not None:
                    self.cfg.set(key, value)

        def load(self):
            return self.application

    gunicorn_options = {
        'bind': '0.0.0.0:5000',
        'workers': 4  # Ajuste conforme necessário
    }

    FlaskApp(app, gunicorn_options).run()