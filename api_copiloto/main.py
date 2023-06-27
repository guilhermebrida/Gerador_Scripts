from flask import Flask,jsonify,request,json,redirect,render_template
from jinja2 import Template
from pprint import pprint
import re
from datetime import date

app = Flask(__name__)
app.static_folder = './static/css'

checkbox_names = {
    "Tracking": "./api_copiloto/funções copiloto/tracking.txt",
    "Horimetro": "./api_copiloto/funções copiloto/horimetro e tempo mov.txt",
    "Faixas RPM": "./api_copiloto/funções copiloto/faixas RPM.txt",
    "Discretas": "./api_copiloto/funções copiloto/discretas.txt",
    "Excesso RPM": "./api_copiloto/funções copiloto/excesso rpm.txt",
    "Parada motor ligado": "./api_copiloto/funções copiloto/parada motor ligado.txt",
    "Cercas": "./api_copiloto/funções copiloto/cercas.txt",
    "Limpador de parabrisa": "./api_copiloto/funções copiloto/limpador parabrisa.txt",
    "Excesso de Velocidade": "./api_copiloto/funções copiloto/excesso velocidade.txt",
    "Desaceleração brusca": "./api_copiloto/funções copiloto/desaceleracao.txt",
    "Aceleração brusca": "./api_copiloto/funções copiloto/aceleracao.txt",
    "Identificação de motorista": "./api_copiloto/funções copiloto/mifare.txt",
    "Condução ininterrupta": "./api_copiloto/funções copiloto/conducao ininterrupta.txt",
    "Modo Sleep": "./api_copiloto/funções copiloto/sleep.txt",
    "Rotas SP": "./api_copiloto/funções copiloto/Rotas SP.txt"
}

checkbox_names_var = [
    "Nome do Arquivo",
    # "Id Arquivo configurador",
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
    "Tolerância para iniciar o descanso obrigatório (minutos)"
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


def Gerar_arquivo(funcoes,parametros,ALARMES):
    with open('./api_copiloto/funções copiloto/inicio.txt', 'r') as t:
        tudo = t.read()
    for funcao in funcoes:
        if funcao in checkbox_names:
            if funcao == "Rotas SP":
                continue
            with open(checkbox_names[funcao], 'r') as t:
                tudo += '\n' + t.read()
    with open('./api_copiloto/funções copiloto/log.txt', 'r') as t:
        tudo += '\n' + t.read()
    if "Rotas SP" in funcoes:
        with open('./api_copiloto/funções copiloto/Rotas SP.txt', 'r') as t:
            tudo += '\n' + t.read()
    with open('./api_copiloto/funções copiloto/fim.txt', 'r') as t:
        tudo += '\n' + t.read()
    for func in parametros:
        print(func)
        if func == "Limite de Velocidade (Km/h)":
            lim_vel = parametros[func]
            tudo = re.sub(">SCT11.*<",f'>SCT11 {lim_vel}900<', tudo)
        if func == "Limite de Velocidade com Chuva (Km/h)":
            lim_vel_chuva = parametros[func]
            tudo = re.sub(">SCT12.*<",f'>SCT12 {lim_vel_chuva}900<', tudo)
        if func == "Limite de Velocidade Carregado (Km/h)":
            lim_vel_carregado = parametros[func]
            tudo = re.sub(">SCT13.*<",f'>SCT13 {lim_vel_carregado}900<', tudo)
        if func == "Tempo de Tolerância à Infração de Velocidade (Segundos)":
            tolerancia_vel = parametros[func]
            tudo = re.sub(">SCT06.*<",f'>SCT06 {tolerancia_vel}<', tudo)
        if func == "Freada Brusca (km/h/s)":
            freada = parametros[func]
            tudo = re.sub(">SCT08.*<",f'>SCT08 0-{freada}<', tudo)
        if func == "Limite de Aceleração Brusca (km/h/s)":
            acel = parametros[func]
            tudo = re.sub(">SCT09.*<",f'>SCT09 {acel}<', tudo)
        if func == "Rotação de Marcha Lenta (RPM)":
            lenta = parametros[func]
            if re.search('>SUT11.*<',tudo) is not None:
                sut11 = re.search('>SUT11.*<',tudo).group()
                tudo = re.sub(sut11.split(',')[-1],f'{lenta}<',tudo)
        if func == "Rotação Minima de Faixa Verde (RPM)":
            min_verde = parametros[func]
            if re.search('>SUT12.*<',tudo) is not None:
                sut12 = re.search('>SUT12.*<',tudo).group()
                tudo = re.sub(sut12.split(',')[-2],f'{min_verde}',tudo)
        if func == "Rotação Máxima de Faixa Verde (RPM)":
            max_verde = parametros[func]
            if re.search('>SUT12.*<',tudo) is not None:
                sut12 = re.search('>SUT12.*<',tudo).group()
                tudo = re.sub(sut12.split(',')[-1],f'{max_verde}<',tudo)
        if func == "Limite de Rotação (RPM)":
            excesso = parametros[func]
            if re.search('>SUT13.*<',tudo) is not None:
                sut13 = re.search('>SUT13.*<',tudo).group()
                tudo = re.sub(sut13.split(',')[-2],f'{excesso}',tudo)
        if func == "Limite de Rotação Freio Motor (RPM)":
            freio_motor = parametros[func]
            tudo = re.sub('>SUT14.*<',f'>SUT14,QCT27,7,15,{min_verde},{int(freio_motor)-1}<',tudo)
            tudo = re.sub('>SUT15.*<',f'>SUT15,QCT27,7,15,{freio_motor},9999<',tudo)
        if func == "Rotação para Troca de Marcha (RPM)":
            troca = parametros[func]
            tudo = re.sub('>SUT16.*<',f'>SUT16,QCT27,7,15,{troca},9999<',tudo)
        if func == "Tempo de Parada com Motor Ligado (Segundos)":
            tempo_parada = parametros[func]
            tudo = re.sub(">SCT04.*<",f'>SCT04 {tempo_parada}<', tudo)
        if func == "Tempo máximo de condução (minutos)":
            tempo_max_cond = parametros[func]
            tudo = re.sub(">SCT14.*<",f'>SCT14 {int(tempo_max_cond)*60}<', tudo)
        if func == "Tempo de descanso obrigatório (minutos)":
            descanso_obrigatorio = parametros[func]
            print(descanso_obrigatorio)
            tudo = re.sub(">SCT17.*<",f'>SCT17 {int(descanso_obrigatorio)*60}<', tudo)
        if func == "Tolerância para iniciar o descanso obrigatório (minutos)":
            tol_descanso = parametros[func]
            tudo = re.sub(">SCT15.*<",f'>SCT15 {int(tol_descanso)*60}<', tudo)
        if func == "Id Arquivo configurador":
            tp = parametros[func]
            tp = re.sub(" ", "_",tp)
            versao = str(date.today())
            versao = versao.replace('-', '')[-6::]
            tudo = re.sub(">STP01.*<",f">STP01 {tp}.{versao}<",tudo)
        if func == "Nome do Arquivo":
            path = parametros[func]
            path = re.sub(" ", "_",path)
    if "Modo Sleep"and "Condução ininterrupta" in funcoes:
        sleep = str(int(descanso_obrigatorio)*60+300).zfill(4)
        tudo = re.sub('>VSKO0600060000900120_INS1_CAN1_EVP1800<',f'>VSKO{sleep}{sleep}00900120_INS1_CAN1_EVP1800<',tudo)
    sxt = re.search('>SXT0010010101_MD1<',tudo)
    if sxt is not None:
        tudo = re.sub(">SXT0010010101_MD1<","",tudo)
        tudo = re.sub(">SSO<",">SXT0010010101_MD1<\n>SSO<",tudo)
    tudo = Gerar_alarmes(tudo,ALARMES)
    with open(f'./{path}.txt', 'w') as fim:
        fim.write(tudo)

def Gerar_alarmes(tudo,alarmes):
    sct16 = 0
    for alarme in alarmes:
        sct16 = sct16 + checkboxes_alarmes[alarme]
    if sct16:
        tudo = re.sub(">SCT16 768<",f">SCT16 {sct16}<",tudo)
    return tudo




def validate_checkboxes(selected_checkboxes):
    if "7" in selected_checkboxes and "15" in selected_checkboxes:
        return True
    return False

def validate_path(values):
    print(values)
    if "Nome do Arquivo" not in values:
        return True
    return False

@app.route('/')
def index():
    checkboxes = zip(range(1, len(checkbox_names) + 1), checkbox_names)
    checkboxes_var = zip(range(1, len(checkbox_names_var) + 1), checkbox_names_var)
    checkbox_alarmes = zip(range(1, len(checkboxes_alarmes) + 1), checkboxes_alarmes)
    return render_template('index.html', checkboxes=checkboxes, checkboxes_var=checkboxes_var, alarmes=checkbox_alarmes)


@app.route('/submit', methods=['POST'])
def submit():
    selected_checkboxes = request.form.getlist('checkbox')
    alarme_escolhido = request.form.getlist('alarme')
    condition = validate_checkboxes(selected_checkboxes)
    if condition:
        popup_visible = True
        # return render_template('index.html', popup_visible=popup_visible)
        return render_template('popup.html', condition=condition)
    funcoes = []
    for checkbox in selected_checkboxes:
        chaves = list(checkbox_names.keys())
        parameter_name = chaves[int(checkbox)-1]
        funcoes.append(parameter_name)
    values = {}
    for var in checkbox_names_var:
        input_name = 'input_' + str(checkbox_names_var.index(var)+1)
        value = request.form.get(input_name)
        if value:
            values[var] = value
    validate = validate_path(values)
    if validate:
        return render_template('popup.html', validate=validate)
    ALARMES = []
    for alarm in alarme_escolhido:
        chaves = list(checkboxes_alarmes.keys())
        parameter_name = chaves[int(alarm)-1]
        ALARMES.append(parameter_name)
    Gerar_arquivo(funcoes,values,ALARMES)
    return 'Funções desejadas:' + str(funcoes) + '<br>' + 'Valores capturados: ' + str(values) + '<br>' + 'alarmes: ' + str(ALARMES) 

if __name__ == '__main__':
  app.run(debug=True)




# def Gerar_arquivo(funcoes,parametros):
#     funcoes = funcoes
#     parametros = parametros
#     with open ('./api_copiloto/funções copiloto/inicio.txt', 'r') as t:
#         tudo = t.read()
#     if "Tracking" in funcoes:            
#         with open ('./api_copiloto/funções copiloto/tracking.txt', 'r') as t:
#             tudo = tudo +'\n'+ t.read()
#     if "Horimetro" in funcoes:            
#         with open ('./api_copiloto/funções copiloto/horimetro e tempo mov.txt', 'r') as t:
#             tudo = tudo +'\n'+ t.read()
#     if "Faixas RPM" in funcoes:            
#         with open ('./api_copiloto/funções copiloto/faixas RPM.txt', 'r') as t:
#             tudo = tudo +'\n'+ t.read()
#     if "Discretas" in funcoes:            
#         with open ('./api_copiloto/funções copiloto/discretas.txt', 'r') as t:
#             tudo = tudo +'\n'+ t.read()
#     if "Excesso RPM" in funcoes:            
#         with open ('./api_copiloto/funções copiloto/excesso rpm.txt', 'r') as t:
#             tudo = tudo +'\n'+ t.read()
#     if "Parada motor ligado" in funcoes:            
#         with open ('./api_copiloto/funções copiloto/parada motor ligado.txt', 'r') as t:
#             tudo = tudo +'\n'+ t.read()
#     if "Cercas" in funcoes:            
#         with open ('./api_copiloto/funções copiloto/cercas.txt', 'r') as t:
#             tudo = tudo +'\n'+ t.read()
#     if "Limpador de parabrisa" in funcoes:            
#         with open ('./api_copiloto/funções copiloto/limpador parabrisa.txt', 'r') as t:
#             tudo = tudo +'\n'+ t.read()
#     if "Excesso de Velocidade" in funcoes:            
#         with open ('./api_copiloto/funções copiloto/excesso velocidade.txt', 'r') as t:
#             tudo = tudo +'\n'+ t.read()
#     if "Desaceleração brusca" in funcoes:            
#         with open ('./api_copiloto/funções copiloto/desaceleracao.txt', 'r') as t:
#             tudo = tudo +'\n'+ t.read()
#     if "Aceleração brusca" in funcoes:            
#         with open ('./api_copiloto/funções copiloto/aceleracao.txt', 'r') as t:
#             tudo = tudo +'\n'+ t.read()
#     if "Identificação de motorista" in funcoes:            
#         with open ('./api_copiloto/funções copiloto/mifare.txt', 'r') as t:
#             tudo = tudo +'\n'+ t.read()
#     if "Condução ininterrupta" in funcoes:         
#         with open ('./api_copiloto/funções copiloto/conducao ininterrupta.txt', 'r') as t:
#             tudo = tudo +'\n'+ t.read()
#     if "Modo Sleep" in funcoes:            
#         with open ('./api_copiloto/funções copiloto/sleep.txt', 'r') as t:
#             tudo = tudo +'\n'+ t.read()    
#     with open ('./api_copiloto/funções copiloto/fim.txt', 'r') as t:
#         tudo = tudo +'\n'+ t.read()
#     with open('./teste.txt','w') as fim:
#         fim.write(tudo)
    # print(tudo)
