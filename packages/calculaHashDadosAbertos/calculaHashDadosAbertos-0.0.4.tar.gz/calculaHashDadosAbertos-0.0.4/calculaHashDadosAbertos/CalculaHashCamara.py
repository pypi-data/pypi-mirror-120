import requests
import pandas as pd
from pandas.io.json import json_normalize
from datetime import date
import json
import io
import hashlib, os, sys

class Con3Prop:

  # import shutil
  #para 3 inputs
  def __init__(self, parametro1, parametro2, parametro3, diasdiff):
    """ parametro = 'PLP''PEC' 'PL', diasdiff= dias de diferença (valor inteiro)"""
    self.parametro1 = parametro1
    self.parametro2 = parametro2
    self.parametro3 = parametro3
    self.diasdiff = diasdiff
  @property
  def diferenca3Prop(self):
    """Esta biblioteca retorna uma consulta a API com a diferença de dias inserida"""
    hj=date.today()  
    return 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaTipo={}&siglaTipo={}&siglaTipo={}&dataApresentacaoInicio='.format(self.parametro1, self.parametro2,self.parametro3)+str(date.fromordinal(hj.toordinal()-self.diasdiff))+"&dataApresentacaoFim="+str(date.today())+"&ordem=ASC&ordenarPor=id"
  @property
  def vectNorm3Prop(self):
    """Retorna vetor normalizado na biblioteca pandas de uma consulta de um json do site dados abertos"""
    hj=date.today()
    consulta_3_Dias = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaTipo={}&siglaTipo={}&siglaTipo={}&dataApresentacaoInicio='.format(self.parametro1, self.parametro2,self.parametro3)+str(date.fromordinal(hj.toordinal()-self.diasdiff))+"&dataApresentacaoFim="+str(date.today())+"&ordem=ASC&ordenarPor=id"
    requisicao = requests.get(consulta_3_Dias)
    consulta= requisicao.json()
    df = pd.json_normalize(consulta['dados'])
    return df
  @property
  def HashMD5Camara(self):
    import requests
    import pandas as pd
    from pandas.io.json import json_normalize
    from datetime import date
    import json
    import io
    import hashlib, os, sys
    import shutil
    """Função utilizada para calcular a HASH MD5 de uma PLP, PEC ou PL da API da Camara dos deputados e salvar em um csv"""
    dir = './temp'   
    #Crio diretorio temporario  
    os.makedirs(dir)
    #Pega os IDS com PEC,PLP e PL nos ultimos 3 dias
    #Dados de hoje menos 3 dias
    hj=date.today()
    consulta_3_Dias = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaTipo={}&siglaTipo={}&siglaTipo={}&dataApresentacaoInicio='.format(self.parametro1, self.parametro2,self.parametro3)+str(date.fromordinal(hj.toordinal()-self.diasdiff))+"&dataApresentacaoFim="+str(date.today())+"&ordem=ASC&ordenarPor=id"
    requisicao = requests.get(consulta_3_Dias)
    consulta= requisicao.json()
    df = pd.json_normalize(consulta['dados'])
    #Imprime o numero de dados que retornou no dia
    print("Sistema retornou "+str(len(df.id))+" consultas")
    #Nesse laço for ele irá baixar os arquivos para depois mostrar todos numa pasta temporaria na 
    for i in range(len(df.id)):
      dados= requests.get("https://dadosabertos.camara.leg.br/api/v2/proposicoes/"+str(df.id[i])).json()
      df2 = pd.json_normalize(dados['dados'])
      #Salva os dados em pdf
      url = str(df2.urlInteiroTeor[0])
      response = requests.get(url)
      if response.ok:
          file = open(dir+'/'+str(df.id[i]), "wb+") # write, binary, allow creation
          file.write(response.content)
          file.close()
      else:
          print("Failed to get the file")
    #Printo as hashs dos ultimos 3 dias
    print("Lista de hashs MD5 dos ultimos 3 dias:")
    totalFiles = 0
    totalDir = 0
  #Cria um dataframe com o numero de arquivos na pasta temporaria
    for base, dirs, files in os.walk('/content/temp'):
        # print('Searching in : ',base)
        for directories in dirs:
            totalDir += 1
        for Files in files:
            totalFiles += 1
    totalFiles

    df3 = pd.DataFrame(index=range(totalFiles),columns=range(2))
    df3 = df3.rename(columns={0: 'HashMD5', 1:'id'})
    b=0
  #Procura a hash dentro do diretorio
    for root, dirs,files in os.walk(dir, topdown=True):
        for name in files:
            # print(os.path.join(name))

            FileName = (os.path.join(root, name))
            hasher = hashlib.md5()
            with open(str(FileName), 'rb') as afile:
                buf = afile.read()
                hasher.update(buf) 
            df3['id'][b]= str(os.path.join(name))
            df3['HashMD5'][b]=str(hasher.hexdigest())
            
            b+=1

    df['id']=df['id'].astype(str)
    df3['id']=df3['id'].astype(str)
    df = df.merge(df3, on='id')
    #Vejo o cabeçalho 
    print(df.head())
    #Vejo a estrutura do cabeçalho
    print(df.info())
  # Salvo em csv
    df.to_csv('HashMD5Camara.csv')
    #Deleto diretorio temporario
    shutil.rmtree(dir, ignore_errors=True)  
class Con2Prop:

  # import shutil
  #para 2 inputs
  def __init__(self, parametro1, parametro2, diasdiff):
    """ parametro = 'PLP''PEC' 'PL', diasdiff= dias de diferença (valor inteiro)"""
    self.parametro1 = parametro1
    self.parametro2 = parametro2
    self.diasdiff = diasdiff
  @property
  def diferenca3Prop(self):
    """Esta biblioteca retorna uma consulta a API com a diferença de dias inserida"""
    hj=date.today()  
    return 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaTipo={}&siglaTipo={}&dataApresentacaoInicio='.format(self.parametro1, self.parametro2)+str(date.fromordinal(hj.toordinal()-self.diasdiff))+"&dataApresentacaoFim="+str(date.today())+"&ordem=ASC&ordenarPor=id"
  @property
  def vectNorm3Prop(self):
    """Retorna vetor normalizado na biblioteca pandas de uma consulta de um json do site dados abertos"""
    hj=date.today()
    consulta_3_Dias = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaTipo={}&siglaTipo={}&dataApresentacaoInicio='.format(self.parametro1, self.parametro2)+str(date.fromordinal(hj.toordinal()-self.diasdiff))+"&dataApresentacaoFim="+str(date.today())+"&ordem=ASC&ordenarPor=id"
    requisicao = requests.get(consulta_3_Dias)
    consulta= requisicao.json()
    df = pd.json_normalize(consulta['dados'])
    return df
  @property
  def HashMD5Camara(self):
    import requests
    import pandas as pd
    from pandas.io.json import json_normalize
    from datetime import date
    import json
    import io
    import hashlib, os, sys
    import shutil
    """Função utilizada para calcular a HASH MD5 de uma PLP, PEC ou PL da API da Camara dos deputados e salvar em um csv"""
    dir = './temp'   
    #Crio diretorio temporario  
    os.makedirs(dir)
    #Pega os IDS com PEC,PLP e PL nos ultimos 3 dias
    #Dados de hoje menos 3 dias
    hj=date.today()
    consulta_3_Dias = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaTipo={}&siglaTipo={}&dataApresentacaoInicio='.format(self.parametro1, self.parametro2)+str(date.fromordinal(hj.toordinal()-self.diasdiff))+"&dataApresentacaoFim="+str(date.today())+"&ordem=ASC&ordenarPor=id"
    requisicao = requests.get(consulta_3_Dias)
    consulta= requisicao.json()
    df = pd.json_normalize(consulta['dados'])
    #Imprime o numero de dados que retornou no dia
    print("Sistema retornou "+str(len(df.id))+" consultas")
    #Nesse laço for ele irá baixar os arquivos para depois mostrar todos numa pasta temporaria na 
    for i in range(len(df.id)):
      dados= requests.get("https://dadosabertos.camara.leg.br/api/v2/proposicoes/"+str(df.id[i])).json()
      df2 = pd.json_normalize(dados['dados'])
      #Salva os dados em pdf
      url = str(df2.urlInteiroTeor[0])
      response = requests.get(url)
      if response.ok:
          file = open(dir+'/'+str(df.id[i]), "wb+") # write, binary, allow creation
          file.write(response.content)
          file.close()
      else:
          print("Failed to get the file")
    #Printo as hashs dos ultimos 3 dias
    print("Lista de hashs MD5 dos ultimos 3 dias:")
    totalFiles = 0
    totalDir = 0
  #Cria um dataframe com o numero de arquivos na pasta temporaria
    for base, dirs, files in os.walk('/content/temp'):
        # print('Searching in : ',base)
        for directories in dirs:
            totalDir += 1
        for Files in files:
            totalFiles += 1
    totalFiles

    df3 = pd.DataFrame(index=range(totalFiles),columns=range(2))
    df3 = df3.rename(columns={0: 'HashMD5', 1:'id'})
    b=0
  #Procura a hash dentro do diretorio
    for root, dirs,files in os.walk(dir, topdown=True):
        for name in files:
            # print(os.path.join(name))

            FileName = (os.path.join(root, name))
            hasher = hashlib.md5()
            with open(str(FileName), 'rb') as afile:
                buf = afile.read()
                hasher.update(buf) 
            df3['id'][b]= str(os.path.join(name))
            df3['HashMD5'][b]=str(hasher.hexdigest())
            
            b+=1

    df['id']=df['id'].astype(str)
    df3['id']=df3['id'].astype(str)
    df = df.merge(df3, on='id')
    #Vejo o cabeçalho 
    print(df.head())
    #Vejo a estrutura do cabeçalho
    print(df.info())
  # Salvo em csv
    df.to_csv('HashMD5Camara.csv')
    #Deleto diretorio temporario
    shutil.rmtree(dir, ignore_errors=True)   






  
class Con1Prop:
  import requests
  import pandas as pd
  from pandas.io.json import json_normalize
  from datetime import date
  import json
  import io
  import hashlib, os, sys
  import shutil
  #para 1 input
  def __init__(self, parametro1, diasdiff):
    """ proposta = 'sigla1', diasdiff= dias de diferença (valor inteiro)"""
    self.parametro1 = parametro1
    self.diasdiff = diasdiff
  @property
  def diferenca1Prop(self):
    """(proposta = 'sigla', diasdiff= dias de diferença (valor inteiro)"""
    hj=date.today()  
    return 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaTipo={}&dataApresentacaoInicio='.format(self.parametro1)+str(date.fromordinal(hj.toordinal()-self.diasdiff))+"&dataApresentacaoFim="+str(date.today())+"&ordem=ASC&ordenarPor=id"
  @property
  def HashMD5Camara(self):
    import requests
    import pandas as pd
    from pandas.io.json import json_normalize
    from datetime import date
    import json
    import io
    import hashlib, os, sys
    import shutil
    """Função utilizada para calcular a HASH MD5 de uma PLP, PEC ou PL da API da Camara dos deputados e salvar em um csv"""
    dir = './temp'   
    #Crio diretorio temporario  
    os.makedirs(dir)
    #Pega os IDS com PEC,PLP e PL nos ultimos 3 dias
    #Dados de hoje menos 3 dias
    hj=date.today()
    consulta_3_Dias = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaTipo={}&dataApresentacaoInicio='.format(self.parametro1)+str(date.fromordinal(hj.toordinal()-self.diasdiff))+"&dataApresentacaoFim="+str(date.today())+"&ordem=ASC&ordenarPor=id"
    requisicao = requests.get(consulta_3_Dias)
    consulta= requisicao.json()
    df = pd.json_normalize(consulta['dados'])
    #Imprime o numero de dados que retornou no dia
    print("Sistema retornou "+str(len(df.id))+" consultas")
    #Nesse laço for ele irá baixar os arquivos para depois mostrar todos numa pasta temporaria na 
    for i in range(len(df.id)):
      dados= requests.get("https://dadosabertos.camara.leg.br/api/v2/proposicoes/"+str(df.id[i])).json()
      df2 = pd.json_normalize(dados['dados'])
      #Salva os dados em pdf
      url = str(df2.urlInteiroTeor[0])
      response = requests.get(url)
      if response.ok:
          file = open(dir+'/'+str(df.id[i]), "wb+") # write, binary, allow creation
          file.write(response.content)
          file.close()
      else:
          print("Failed to get the file")
    #Printo as hashs dos ultimos 3 dias
    print("Lista de hashs MD5 dos ultimos 3 dias:")
    totalFiles = 0
    totalDir = 0
  #Cria um dataframe com o numero de arquivos na pasta temporaria
    for base, dirs, files in os.walk('/content/temp'):
        # print('Searching in : ',base)
        for directories in dirs:
            totalDir += 1
        for Files in files:
            totalFiles += 1
    totalFiles

    df3 = pd.DataFrame(index=range(totalFiles),columns=range(2))
    df3 = df3.rename(columns={0: 'HashMD5', 1:'id'})
    b=0
  #Procura a hash dentro do diretorio
    for root, dirs,files in os.walk(dir, topdown=True):
        for name in files:
            # print(os.path.join(name))

            FileName = (os.path.join(root, name))
            hasher = hashlib.md5()
            with open(str(FileName), 'rb') as afile:
                buf = afile.read()
                hasher.update(buf) 
            df3['id'][b]= str(os.path.join(name))
            df3['HashMD5'][b]=str(hasher.hexdigest())
            
            b+=1

    df['id']=df['id'].astype(str)
    df3['id']=df3['id'].astype(str)
    df = df.merge(df3, on='id')
    #Vejo o cabeçalho 
    print(df.head())
    #Vejo a estrutura do cabeçalho
    print(df.info())
  # Salvo em csv
    df.to_csv('HashMD5Camara.csv')
    #Deleto diretorio temporario
    shutil.rmtree(dir, ignore_errors=True)  
 
      



  
