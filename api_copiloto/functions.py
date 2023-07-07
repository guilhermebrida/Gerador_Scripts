import re
from datetime import date
import json
import base64
from Crypto.Cipher import AES 
from aes_pkcs5.algorithms.aes_ecb_pkcs5_padding import AESECBPKCS5Padding
import hashlib
import os


###### FUNÇÕES PARA PERFIL #########

def processar_arquivo(path):
    with open(path, encoding='utf-8') as f:
        tudo = f.read()
        cc_tag = Get_cc_tag(tudo)

    tudo = re.sub('//.*', '', tudo)
    comandos = re.findall('>.*<', tudo)
    lista_comandos = []
    for i in range(len(comandos)):
        if i != (len(comandos) - 1):
            lista_comandos.append(comandos[i] + ';')
        if i == (len(comandos) - 1):
            lista_comandos.append(comandos[i])

    buscaS3 = re.search('>TCFG13,9999<', tudo)
    if buscaS3 is None:
        buscaS3 = re.search('VL12', path)
        if buscaS3 is None:
            buscaS3 = re.search('S3+', path)
            if buscaS3 is None:
                buscaS3 = re.search('Virloc12', path)

    buscaS1 = re.search('>SIS8.*<', tudo)
    if buscaS1 is None:
        buscaS1 = re.search('VL6', path)
        if buscaS1 is None:
            buscaS1 = re.search('S1', path)
            if buscaS1 is None:
                buscaS1 = re.search('Virloc6', path)

    buscaS4 = re.search('>SSB.*<', tudo)
    if buscaS4 is None:
        buscaS4 = re.search('VC5', path)
        if buscaS4 is None:
            buscaS4 = re.search('S4', path)
            if buscaS4 is None:
                buscaS4 = re.search('Vircom5', path)

    buscaS8 = re.search('VL8', tudo)
    if buscaS8 is None:
        buscaS8 = re.search('VL8', path)
        if buscaS8 is None:
            buscaS8 = re.search('S8', path)
            if buscaS8 is None:
                buscaS8 = re.search('Virloc8', path)

    diretorio = os.path.dirname(path)
    path = str(path).split('/')[-1].split('.')[0]
    idarquivo = path.replace('_', ' ')

    list_replace = [' VL12',' VL10',' VC5',' VL6',' VL8']

    for i in list_replace:
        idarquivo = idarquivo.replace(i, '')

    return {
        'cc_tag': cc_tag,
        'tudo': tudo,
        'lista_comandos': lista_comandos,
        'buscaS3': buscaS3,
        'buscaS1': buscaS1,
        'buscaS4': buscaS4,
        'buscaS8': buscaS8,
        'path': path,
        'idarquivo': idarquivo,
        'comandos': comandos,
        'diretorio': diretorio
    }

def message(path):
    f=open(f'{path}.json',encoding='utf_8')
    json_data=f.read()
    json_dict = json.loads(json_data)
    comandos=json_dict['comandos']
    return comandos

def Get_cc_tag(tudo):
    cc_tag = re.search('[cc.id].*', tudo)
    if cc_tag is not None:
        cc_tag = re.search('\d\d*',cc_tag.group()).group()
    return cc_tag


def extrair_lim_vel(tudo):
    lim_vel = re.search('>SCT11.*<', tudo)
    if lim_vel is not None:
        lim_vel = lim_vel.group()[7:-1]
        if len(lim_vel) == 5:
            lim_vel = lim_vel[0:2]
        else:
            lim_vel = lim_vel[0:3]
    return lim_vel


def extrair_vel_evento(tudo):
    vel_evento = re.search('>SCT12.*<', tudo)
    if vel_evento is not None:
        vel_evento = vel_evento.group()[7:-1]
        if len(vel_evento) == 5:
            vel_evento = vel_evento[0:2]
        elif len(vel_evento) == 6:
            vel_evento = vel_evento[0:3]
    return vel_evento


def extrair_tempo_infra(tudo):
    tempo_infra = re.search('>SCT06.*<', tudo)
    if tempo_infra is not None:
        tempo_infra = tempo_infra.group()[7:-1]
    return tempo_infra


def verificar_mifare(tudo):
    mifare = re.search('>SSH111<', tudo)
    if mifare is not None:
        return 'Habilitado'
    else:
        return 'Desabilitado'



# def extrair_versao(tudo):
#     versao = re.search('>STP01.*<', tudo)
#     if versao is not None:
#         versao1 = re.search('-', versao.group())
#         if versao1 is None:
#             versao1 = re.search('>STP01.*<', tudo).group()
#             versao1 = re.search('\d\d\d\d*', versao1).group()
#             versao = versao1
#         else:
#             versao = None
#     if versao is None:
#         versao = re.search('>STP03.*<', tudo)
#         if versao is not None:
#             versao2 = re.search('-', versao.group())
#             if versao2 is None:
#                 versao2 = re.search('\d\d\d\d*', versao.group()).group()
#                 versao = versao2
#     if versao is None:
#         versao = str(date.today())
#         versao = versao.replace('-', '')[-6::]
#     return versao

def extrair_versao(tudo):
    versao = re.search('>STP01.*<', tudo)
    if versao is not None:
        versao1 = re.search('-', versao.group())
        if versao1 is None:
            versao1 = re.search('>STP01.*<', tudo).group()
            versao1 = re.search('\d\d\d\d*', versao1).group()
            return versao1
    versao = re.search('>STP03.*<', tudo)
    if versao is not None:
        versao2 = re.search('-', versao.group())
        if versao2 is None:
            versao2 = re.search('\d\d\d\d*', versao.group()).group()
            return versao2
    versao = re.search('>STP02.*<', tudo)
    if versao is not None:
        versao1 = re.search('-+', versao.group())
        if versao1 is None:
            versao1 = re.search('>STP02.*<', tudo).group()
            versao1 = re.search('\d\d\d\d*(?!.*\d\d\d\d*)', versao1).group()
            return versao1
    return str(date.today()).replace('-', '')[-6:]


def verificar_tablet(tudo):
    tablet = re.search('>SED169.*<', tudo)
    if tablet is not None:
        tablet = re.search('>SED169.*<', tudo).group()
        tabletN77 = re.search('TRM', tablet)
        if tabletN77 is not None:
            tablet = 'N776/N77'
        tabletSAM = re.search('VCM_SL', tablet)
        if tabletSAM is not None:
            tablet = 'SAMSUNG'
        SEMtablet = re.search('SGN NN', tablet)
        if SEMtablet is not None:
            tablet = None
    return tablet


def lim_vel_S1(tudo):
    lim_vel = re.search('>VS08,100.*<', tudo)
    if lim_vel is not None:
        lim_vel = re.search('>VS08,100.*<', tudo).group()[10:13]
        if lim_vel[0] == '0':
            lim_vel = re.sub(r'0', '', lim_vel, count=1)
    return lim_vel


def tempo_infra_S1(tudo):
    tempo_infra = re.findall('>SCT06.*<', tudo)
    if tempo_infra and tempo_infra != '0':
        tempo_infra = re.findall('>SCT06.*<', tudo)[1]
        tempo_infra = tempo_infra[7:-1]
    return tempo_infra


# def versao_S1(tudo):
#     versao = re.search('>SIS82.*<', tudo)
#     if versao is not None:
#         versao1 = re.search('-', versao.group())
#         if versao1 is not None:
#             versao1 = re.search('-', versao1.group())
#         else:
#             versao1 = re.search('>SIS82.*<', tudo).group()
#             versao1 = re.search('\d\d\d\d*', versao1).group()
#         versao = versao1
#     else:
#         versao = re.search('>SIS84.*<', tudo)
#         if versao is not None:
#             versao2 = re.search('>SIS84.*<', tudo).group()
#             if versao2 != '-':
#                 versao2 = re.search('\d\d\d\d*', versao2).group()
#                 versao = versao2
#     return versao

def extrair_versao_s1(tudo):
    versao = re.search('>SIS82.*<', tudo)
    if versao is not None:
        versao1 = re.search('-', versao.group())
        if versao1 is not None:
            versao1 = re.search('-', versao1.group())
        else:
            versao1 = re.search('>SIS82.*<', tudo).group()
            versao1 = re.search('\d\d\d\d*', versao1).group()
        return versao1
    else:
        versao = re.search('>SIS84.*<', tudo)
        if versao is not None:
            versao2 = re.search('>SIS84.*<', tudo).group()
            if versao2 != '-':
                versao2 = re.search('\d\d\d\d*', versao2).group()
                return versao2
    versao = re.search('>SIS83.*<', tudo)
    if versao is not None:
        versao1 = re.search('-+', versao.group())
        if versao1 is None:
            versao1 = re.search('>SIS83.*<', tudo).group()
            versao1 = re.search('\d\d\d\d*(?!.*\d\d\d\d*)', versao1).group()
            return versao1
    return str(date.today()).replace('-', '')[-6:]

###############################################
############# FUNÇÔES CAN #######################

def versao_can(tudo):
    versao = re.search('>STP02.*<', tudo)
    if versao is not None:
        versao1 = re.search('-+', versao.group())
        if versao1 is None:
            versao1 = re.search('>STP02.*<', tudo).group()
            versao1 = re.search('\d\d\d\d*(?!.*\d\d\d\d*)', versao1).group()
            versao = versao1
    if versao is None:
        versao = str(date.today())
        versao = versao.replace('-', '')[-6:]
    return versao


def velocidade_s3(comandos):
    for i in range(len(comandos)):
        velocidade = re.search('>S19.*<', comandos[i])
        if velocidade is not None:
            velocidade = velocidade.group().split(',')[2]
            velocidade = re.search('48', velocidade)
            if velocidade is not None:
                return 'CAN'
    return 'SENSOR'

def rpm_s3(comandos):
    for i in range(len(comandos)):
        rpm = re.search('>S19.*<', comandos[i])
        if rpm is not None:
            rpm = rpm.group().split(',')[2]
            rpm = re.search('26', rpm)
            if rpm is not None:
                return 'CAN'
    return 'SENSOR'


def extrair_limpador(comandos):
    for i in range(len(comandos)):
        limpador = re.search('>SUT02,QCT80.*<', comandos[i])
        if limpador is not None:
            return 'CAN'
        
        limpador = re.search('>SUT02,QIN.*<', comandos[i])
        if limpador is not None:
            return 'SENSOR'
    
    return None


def odometro_s3(comandos):
    for i in range(len(comandos)):
        odometro = re.search('>S19.*<', comandos[i])
        if odometro is not None:
            odometro = odometro.group().split(',')[2]
            odometro = re.search('49', odometro)
            if odometro is not None:
                return 'CAN'
        
        odometro = re.search('>SUT50,QCT03,07,15,0,1.*<', comandos[i])
        if odometro is not None:
            return 'SENSOR'
    
    return None

def horimetro_s3(comandos):
    for i in range(len(comandos)):
        horimetro = re.search('>S19.*<', comandos[i])
        if horimetro is not None:
            horimetro = horimetro.group().split(',')[2]
            horimetro = re.search('29', horimetro)
            horimetro1 = re.search('28', horimetro)
            if horimetro is not None or horimetro1 is not None:
                return 'CAN'            
        horimetro = re.search('>SED119.*<', comandos[i])
        if horimetro is not None:
            return 'CALCULADO'
    return None


def freio_s3(comandos):
    for i in range(len(comandos)):
        freio = re.search('>S19.*<', comandos[i])
        if freio is not None:
            freio = freio.group().split(',')[2]
            freio = re.search('81', freio)
            if freio is not None:
                return 'CAN'
    return None

def farol_s3(comandos):
    for comando in comandos:
        farol = re.search('>S19.*<', comando)
        if farol is not None:
            farol = farol.group().split(',')[2]
            farol = re.search('82', farol)
            if farol is not None:
                return 'CAN'
    return None


def cinto_s3(comandos):
    for comando in comandos:
        cinto = re.search('>S19.*<', comando)
        if cinto is not None:
            cinto = cinto.group().split(',')[2]
            cinto = re.search('83', cinto)
            if cinto is not None:
                return 'CAN'
    return None

def freio_mao_s3(comandos):
    for comando in comandos:
        freio_mao = re.search('>S19.*<', comando)
        if freio_mao is not None:
            freio_mao = freio_mao.group().split(',')[2]
            freio_mao = re.search('84', freio_mao)
            if freio_mao is not None:
                return 'CAN'
    return None

def litrometro(comandos):
    for comando in comandos:
        if re.search('>SED22.*',comando) is not None:
            return 'CAN'
        if re.search('>SED36.*',comando) is not None:
            return 'CAN'
    return None



# def versao_can_s1(tudo):
#     versao = re.search('>SIS83.*<', tudo)
#     if versao is not None:
#         versao1 = re.search('-+', versao.group())
#         if versao1 is None:
#             versao1 = re.search('>SIS83.*<', tudo).group()
#             versao1 = re.search('\d\d\d\d*(?!.*\d\d\d\d*)', versao1).group()
#             return versao1
    
#     return str(date.today()).replace('-', '')[-6:]

def velocidade_s1(comandos):
    for comando in comandos:
        velocidade = re.search('(>VS19\d.*<)', comando)
        if velocidade is not None:
            velocidade = (velocidade.group().split(',')[4])
            velocidade1 = re.search('05', velocidade)
            velocidade = re.search('04', velocidade)
            if velocidade is not None or velocidade1 is not None:
                return 'CAN'
    return None


def rpm_s1(comandos):
    for comando in comandos:
        rpm = re.search('(>VS19\d.*<)', comando)
        if rpm is not None:
            rpm = rpm.group().split(',')[4]
            rpm = re.search('03', rpm)
            if rpm is not None:
                return 'CAN'
    return None

def odometro_s1(comandos):
    for comando in comandos:
        odometro = re.search('(>VS19\d.*<)', comando)
        odometroSUT = re.search('>SUT05,QCT07.*<', comando)
        if odometro is not None:
            odometro = odometro.group().split(',')[4]
            odometro1 = re.search('07', odometro)
            odometro = re.search('01', odometro)
            if odometro is not None:
                return 'CAN'
            if odometro1 is not None:
                odometro_event = re.search('>SED06U<', comando)
                if odometro_event is None:
                    return 'CAN'
        if odometroSUT is not None:
            return 'CALCULADO'
    return None


# def velocidade_s8(comandos):
#     for comando in comandos:
#         velocidade = re.search('>VS29\d\d,.*<', comando)
#         if velocidade is not None:
#             velocidade = velocidade.group().split(',')[4]
#             velocidade1 = re.search('64', velocidade)
#             if re.search('64', velocidade) is None:
#                 velocidade2 = re.search('48', velocidade)
#             if velocidade1 is not None or velocidade2 is not None:
#                 return 'CAN'
#         velocidade = re.search('>VS29\d\d,.*<', comando)
#         if velocidade is not None:       
#             velocidade = velocidade.group().split(',')[11]
#             if velocidade is not None:
#                 velocidade1 = re.search('64', velocidade)
#                 if re.search('64', velocidade) is None:
#                     velocidade2 = re.search('48', velocidade)
#                 if velocidade1 is not None or velocidade2 is not None:
#                     return 'CAN'
#     return None
def velocidade_s8(comandos):
    for comando in comandos:
        match = re.search('>VS29\d\d,.*<', comando)
        if match is not None:
            if len(match.group().split(',')) == 11:
                velocidade = match.group().split(',')[4]
                if re.search('(64|48)', velocidade):
                    return 'CAN'
            if len(match.group().split(',')) > 11:
                velocidade = match.group().split(',')[11]
            if velocidade is not None and re.search('(64|48)', velocidade):
                return 'CAN'
    return None

def rpm_s8(comandos):
    for comando in comandos:
        match = re.search('>VS29\d\d,.*<', comando)
        if match is not None:
            try:
                rpm = match.group().split(',')[4]
                if re.search('27', rpm) is not None:
                    return 'CAN'
                rpm = match.group().split(',')[11]
                if re.search('27', rpm) is not None:
                    return 'CAN'
            except IndexError:
                continue
    return None

def odometro_s8(comandos):
    for comando in comandos:
        odometro = re.search('>VS29\d\d,.*<', comando)
        if odometro is not None:
            odometro = odometro.group().split(',')[4]
            odometro = re.search('01', odometro)
            if odometro is not None:
                return 'CAN'
        odometro = re.search('>SUT50,QCT03,07,15,0,1.*<', comando)
        if odometro is not None:
            return 'SENSOR'
    return None

def horimetro_s8(comandos):
    for comando in comandos:
        horimetro = re.search('>VS29\d\d,.*<', comando)
        if horimetro is not None:
            horimetro = horimetro.group().split(',')[4]
            horimetro = re.search('02', horimetro)
            if horimetro is not None:
                return 'CAN'
        horimetro = re.search('>SED119.*<', comando)
        if horimetro is not None:
            return 'CALCULADO'
    return None

def freio_s8(comandos):
    for comando in comandos:
        match = re.search('>VS29\d\d,.*<', comando)
        if match is not None:
            try:
                freio = match.group().split(',')[4]
                if re.search('81', freio) is not None:
                    return 'CAN'
                freio = match.group().split(',')[11]
                if re.search('81', freio) is not None:
                    return 'CAN'
            except IndexError:
                continue
    return None

def farol_s8(comandos):
    for comando in comandos:
        farol = re.search('>VS29\d\d,.*<', comando)
        if farol is not None:
            farol = farol.group().split(',')[4]
            farol = re.search('82', farol)
            if farol is not None:
                return 'CAN'
    return None

def cinto_s8(comandos):
    for comando in comandos:
        cinto = re.search('>VS29\d\d,.*<', comando)
        if cinto is not None:
            cinto = cinto.group().split(',')[4]
            cinto = re.search('83', cinto)
            if cinto is not None:
                return 'CAN'
    return None

def freio_mao_s8(comandos):
    for comando in comandos:
        freio_mao = re.search('>VS29\d\d,.*<', comando)
        if freio_mao is not None:
            freio_mao = freio_mao.group().split(',')[4]
            freio_mao = re.search('84', freio_mao)
            if freio_mao is not None:
                return 'CAN'
    return None


############## ENCRYPTADOR ################
class AES_pkcs5():
    def __init__(self,path,key:str, mode:AES.MODE_CBC=AES.MODE_CBC,block_size:int=16):
        self.path = path
        self.key = self.setKey(key)
        self.mode = mode
        self.block_size = block_size

    def pad(self,byte_array:bytearray):
        pad_len = (self.block_size - len(byte_array) % self.block_size) *  chr(self.block_size - len(byte_array) % self.block_size)
        return byte_array.decode() +pad_len
    
    def unpad(self,byte_array:bytearray):
        return byte_array[:-ord(byte_array[-1:])]

    def setKey(self,key:str):
        self.key = key.encode('utf-8')
        md5 = hashlib.md5
        self.key = md5(self.key).digest()[:16]
        self.key = self.key.zfill(16)
        return self.key

    def encrypt(self,message:str)->str:
        iv = bytearray([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        byte_array = message.encode("UTF-8")
        padded = self.pad(byte_array)
        cipher = AES.new(self.key, AES.MODE_CBC,iv)
        encrypted = cipher.encrypt(padded.encode())
        encrypted64 = base64.b64encode(encrypted).decode('utf-8')
        f=open(f'{self.path}.json',encoding='utf_8')
        json_data=f.read()
        json_dict = json.loads(json_data)
        comandos=json_dict['comandos']
        json_dict.update(comandos=encrypted64)
        json_dict.update(hash=base64.b64encode(self.key).decode('utf-8'))
        f = open(f'{self.path}.json', 'w',encoding='utf-8')
        json.dump(json_dict, f,ensure_ascii=False)