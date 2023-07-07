import functions

class GeraPerfil():

    def main(self,caminho) -> None:
        self.path = caminho
        self.tipo = 'Perfil'
        self.lista_comandos = []

        processar_arquivo = functions.processar_arquivo(self.path)
        self.tudo = processar_arquivo['tudo']
        self.lista_comandos = processar_arquivo['lista_comandos']
        self.buscaS1 = processar_arquivo['buscaS1']
        self.buscaS3 = processar_arquivo['buscaS3']
        self.buscaS4 = processar_arquivo['buscaS4']
        self.buscaS8 = processar_arquivo['buscaS8']
        self.path = processar_arquivo['path']
        self.idarquivo = processar_arquivo['idarquivo']
        self.cc_tag = processar_arquivo['cc_tag']
        self.diretorio = processar_arquivo['diretorio']


        if self.buscaS3 is not None:
            self.hardware = 'VIRLOC12'
            self.lim_vel = functions.extrair_lim_vel(self.tudo)
            self.vel_evento= functions.extrair_vel_evento(self.tudo)
            self.tempo_infra= functions.extrair_tempo_infra(self.tudo)
            self.mifare= functions.verificar_mifare(self.tudo)
            self.versao= functions.extrair_versao(self.tudo)
            self.tablet = functions.verificar_tablet(self.tudo)
                
        elif self.buscaS1 is not None:
            self.hardware = 'VIRLOC6'
            self.lim_vel= functions.lim_vel_S1(self.tudo)
            self.tempo_infra= functions.tempo_infra_S1(self.tudo)
            self.mifare= functions.verificar_mifare(self.tudo)  
            self.versao= functions.versao_S1(self.tudo)
            self.vel_evento = None
            self.tablet = None
            
        elif self.buscaS4 is not None:
            self.hardware = 'VIRCOM5'
            self.lim_vel = functions.extrair_lim_vel(self.tudo)
            self.vel_evento= functions.extrair_vel_evento(self.tudo)
            self.tempo_infra= functions.extrair_tempo_infra(self.tudo)
            self.mifare= functions.verificar_mifare(self.tudo)
            self.versao= functions.extrair_versao(self.tudo)
            self.tablet = None

        elif self.buscaS8 is not None:
            self.hardware = 'VIRLOC8'
            self.lim_vel = functions.extrair_lim_vel(self.tudo)
            self.vel_evento= functions.extrair_vel_evento(self.tudo)
            self.tempo_infra= functions.extrair_tempo_infra(self.tudo)
            self.mifare= functions.verificar_mifare(self.tudo)
            self.versao= functions.extrair_versao(self.tudo)
            self.tablet = functions.verificar_tablet(self.tudo)
            
        else:
            self.hardware = 'VIRLOC10"'+','+'"VIRLOC11'
            self.lim_vel = functions.extrair_lim_vel(self.tudo)
            self.vel_evento= functions.extrair_vel_evento(self.tudo)
            self.tempo_infra= functions.extrair_tempo_infra(self.tudo)
            self.mifare= functions.verificar_mifare(self.tudo)
            self.versao= functions.extrair_versao(self.tudo)
            self.tablet = functions.verificar_tablet(self.tudo)

        self.cabeçalho = self.Json()
        self.Criar()
        comandos= functions.message(f'{self.diretorio}/{self.path}')
        AES_pkcs5_obj= functions.AES_pkcs5(f'{self.diretorio}/{self.path}',comandos)
        encrypted_message = AES_pkcs5_obj.encrypt(comandos)



    def Json(self,*args):
        if self.path is not None:
            idarq='{"idarquivo":"'+self.idarquivo+'",'
            Jtipo='"tipo":"'+self.tipo+'",'
            Jhardware='"hardware":["'+self.hardware+'"],'
            Jtag = f'"customer_child_id":"{self.cc_tag}",'
            Jversao='"configs":[{"Versão":"'+self.versao+'"},'
            idarq2='{"idarquivo":"'+self.idarquivo+'"}'
            if self.cc_tag is not None:
                cabeçalho=idarq+Jtipo+Jtag+Jhardware+Jversao+idarq2
            else:
                cabeçalho=idarq+Jtipo+Jhardware+Jversao+idarq2
            if self.tablet is not None:
                Jtablet=',{"Modelo Tablet":"'+self.tablet+'"}'
                cabeçalho=cabeçalho+Jtablet
            Jmifare=',{"Mifare":"'+self.mifare+'"}'
            cabeçalho = cabeçalho+Jmifare
            if self.lim_vel is not None:
                limiteVel=',{"limite Vel":"'+self.lim_vel+'"}'
                cabeçalho=cabeçalho+limiteVel
            if self.vel_evento is not None:
                velEvento=',{"limite Vel Evento":"'+self.vel_evento+'"}'
                cabeçalho=cabeçalho+velEvento
            if self.tempo_infra is not None:
                tempoInfra=',{"Tempo Infração":"'+self.tempo_infra+'"}'
                cabeçalho=cabeçalho+tempoInfra
            comandos='],"comandos":"'
            cabeçalho=cabeçalho+comandos
            print(cabeçalho)
        return cabeçalho

    def Criar(self,*args):
        f2=open (f'{self.diretorio}/{self.path}.json','w',encoding='utf-8')
        f2.write(self.cabeçalho)
        for i in range(len(self.lista_comandos)):
            f2.write(self.lista_comandos[i]) 
        f2.write('"')
        hash = ',"hash":""}'
        f2.write(hash)
        f2.close()






