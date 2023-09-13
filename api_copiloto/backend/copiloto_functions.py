import re
from datetime import date

class Copiloto:
    def __init__(self, tudo=None, hardware=None):
        self.tudo = tudo
        self.hardware = hardware

    def limite_velocidade(self, value):
        return re.sub(">SCT11.*<", f'>SCT11 {value}900<', self.tudo)

    def limite_vel_chuva(self, value):
        return re.sub(">SCT12.*<", f'>SCT12 {value}900<', self.tudo)

    def limite_vel_carregado(self, value):
        return re.sub(">SCT13.*<", f'>SCT13 {value}900<', self.tudo)

    def tolerancia_infra_vel(self, value):
        return re.sub(">SCT06.*<", f'>SCT06 {value}<', self.tudo)

    def freada_brusca(self, value):
        return re.sub(">SCT08.*<", f'>SCT08 0-{value}<', self.tudo)

    def aceleracao_brusca(self, value):
        return re.sub(">SCT09.*<", f'>SCT09 {value}<', self.tudo)

    def marcha_lenta(self, value):
        if self.hardware == 'VL10' or self.hardware == 'VL12':
            if re.search('>SUT04.*<', self.tudo) is not None:
                sut11 = re.search('>SUT04.*<', self.tudo).group()
                return re.sub(sut11.split(',')[-1], f'{value}<', self.tudo)

        else:
            if re.search('>SUT11.*<', self.tudo) is not None:
                sut11 = re.search('>SUT11.*<', self.tudo).group()
                return re.sub(sut11.split(',')[-1], f'{value}<', self.tudo)
                

    def min_faixa_verde(self, value):
        if self.hardware == 'VL10' or self.hardware == 'VL12':
            if re.search('>SUT09.*<', self.tudo) is not None:
                sut09 = re.search('>SUT09.*<', self.tudo).group()
                return re.sub(sut09.split(',')[-2], f'{value}', self.tudo)

        else:
            if re.search('>SUT12.*<', self.tudo) is not None:
                sut12 = re.search('>SUT12.*<', self.tudo).group()
                return re.sub(sut12.split(',')[-2], f'{value}', self.tudo)

    def max_faixa_verde(self, value):
        if self.hardware == 'VL10' or self.hardware == 'VL12':
            if re.search('>SUT09.*<', self.tudo) is not None:
                sut09 = re.search('>SUT09.*<', self.tudo).group()
                return re.sub(sut09.split(',')[-1], f'{value}<', self.tudo)
                
        else:
            if re.search('>SUT12.*<', self.tudo) is not None:
                sut12 = re.search('>SUT12.*<', self.tudo).group()
                return re.sub(sut12.split(',')[-1], f'{value}<', self.tudo)

    def limite_rotacao(self, value):
        if re.search('>SUT13.*<', self.tudo) is not None:
            sut13 = re.search('>SUT13.*<', self.tudo).group()
            return re.sub(sut13.split(',')[-2], f'{value}', self.tudo)

    def freio_motor(self, value, min_verde):
        if self.hardware == 'VL10' or self.hardware == 'VL12':
            self.tudo = re.sub('>SUT16.*<', f'>SUT16,QCT27,7,15,{min_verde},{int(value)-1}<', self.tudo)
            return re.sub('>SUT17.*<', f'>SUT17,QCT27,7,15,{value},9999<', self.tudo)
        else:
            self.tudo = re.sub('>SUT14.*<', f'>SUT14,QCT27,7,15,{min_verde},{int(value)-1}<', self.tudo)
            return re.sub('>SUT15.*<', f'>SUT15,QCT27,7,15,{value},9999<', self.tudo)

    def troca_marcha(self, value):
        if self.hardware == 'VL10' or self.hardware == 'VL12':
            return re.sub('>SUT56.*<', f'>SUT56,QCT27,7,15,{value},9999<', self.tudo)
        else:
            return re.sub('>SUT16.*<', f'>SUT16,QCT27,7,15,{value},9999<', self.tudo)

    def parada_motor_ligado(self, value):
        return re.sub(">SCT04.*<", f'>SCT04 {value}<', self.tudo)

    def tempo_max_conducao(self, value):
        return re.sub(">SCT14.*<", f'>SCT14 {int(value)*60}<', self.tudo)

    def tempo_descanso(self, value):
        return re.sub(">SCT17.*<", f'>SCT17 {int(value)*60}<', self.tudo)

    def tolerancia_descanso(self, value):
        return re.sub(">SCT15.*<", f'>SCT15 {int(value)*60}<', self.tudo)

    def lora(self, value):
        rede_lora = ''.join(str(ord(char)) for char in value)
        return re.sub('000102030405060708090A0B0C0D0E0F', rede_lora, self.tudo)

    def id_arquivo(self, value):
        tp = value
        tp = re.sub(" ", "_", tp)
        versao = str(date.today())
        versao = versao.replace('-', '')[-6::]
        return re.sub(">STP01.*<", f">STP01 {tp}.{versao}<", self.tudo)

    def nome_arquivo(self, value):
        path = value
        path = re.sub(" ", "_", path)
        return path

    def sleep(self, value):
        sleep = str(int(value) * 60 + 300).zfill(4)
        return re.sub('>VSKO0600060000900120_INS1_CAN1_EVP1800<', f'>VSKO{sleep}{sleep}00900120_INS1_CAN1_EVP1800<', self.tudo)


