#importando bibliotecas
import pandas as pd

#importando os dados
df = pd.read_csv("Tabela.csv", sep=';', encoding='utf-8')

#colocando dados extras para teste
df.loc[len(df)] = ({"Opção":"14","Descrição":"Investimento novo","Custo do investimento (R$)":350,"Retorno esperado (R$)":350,"Risco do investimento (R$)":"Alto"})
df.loc[len(df)] = ({"Opção":"15","Descrição":"Investimento com Erro","Custo do investimento (R$)":-620,"Retorno esperado (R$)":500,"Risco do investimento (R$)":"Alto"})
df.loc[len(df)] = ({"Opção":"16","Descrição":"Investimento com risco diferente","Custo do investimento (R$)":250,"Retorno esperado (R$)":350,"Risco do investimento (R$)":"Muito Alto"})

#Criando uma nova coluna para descobrir a porcentagem de ganho
df['Porcentagem de ganho (%)'] = df['Retorno esperado (R$)'] / df['Custo do investimento (R$)'] *100

#Criando mais uma coluna para ser o valor da porcentagem de ganho vezes o retorno esperado, criando assim a minha coluna base de melhores investimentos
df['Retorno X Porcentagem'] = df['Retorno esperado (R$)'] * df['Porcentagem de ganho (%)']
#Deixando a coluna em ordem de crescente em relação a coluna Retorno X porcentagem
df = df.sort_values(by='Retorno X Porcentagem',ascending=False)

#Aplicando uma limpeza no dataframe, deixando somente valores positivos e linhas com risco médio, baixo ou alto no dataframe
df = df[df['Retorno X Porcentagem'] >= 0]
filtro_medio = df[df['Risco do investimento (R$)'] == 'Médio']
filtro_baixo = df[df['Risco do investimento (R$)'] == 'Baixo']
filtro_alto = df[df['Risco do investimento (R$)'] == 'Alto']
df = pd.concat([filtro_baixo, filtro_medio, filtro_alto])

#Aplicando 3 filtros para pegar os melhores valores de cada
maiores_valores_medio = filtro_medio.nlargest(2, 'Retorno X Porcentagem')
maiores_valores_baixo = filtro_baixo.nlargest(2, 'Retorno X Porcentagem')
maior_valor_alto = filtro_alto.nlargest(1, 'Retorno X Porcentagem')

# Removerendo os valores obtidos do DataFrame original e juntar os valores obtidos em um dataframe
df = df.drop(maiores_valores_medio.index)
df = df.drop(maiores_valores_baixo.index)
df = df.drop(maior_valor_alto.index)
resultado = pd.concat([maiores_valores_medio, maiores_valores_baixo, maior_valor_alto])

#somando o valor total do custo de investimento que eu já tenho escolhido
custo_total = resultado['Custo do investimento (R$)'].sum()

#Criando uma lista do meu dataframe com os 5 já escolhidos.
selecoes = [resultado.columns.tolist()] + resultado.values.tolist()

#Agora vou correr o dataframe linha por linha e se estiver dentro da condição ele vai adicionar a linha na minha lista
for _, row in df.iterrows():
    custo_investimento = row['Custo do investimento (R$)']
    # Checando se o custo total mais o custo do investivento da linha que está sendo lida é menor que 2400
    if custo_total + custo_investimento <= 2400:
      #agora o programa vai ver se o risco medio, alto e baixo já não passaram do valor máximo para cada categoria
        soma_risco_medio = sum(item[2] for item in selecoes if item[4] == 'Médio')
        soma_risco_alto = sum(item[2] for item in selecoes if item[4] == 'Alto')
        soma_risco_baixo = sum(item[2] for item in selecoes if item[4] == 'Baixo')
        if soma_risco_medio >= 1500:
            continue
        elif soma_risco_alto >= 900:
            continue
        elif soma_risco_baixo >= 1200:
            continue
        else:
            selecoes.append(row)
            custo_total += custo_investimento
    else:
        continue

# Criando um novo dataframe com a lista preenchida pelos investimentos.
df_selecoes = pd.DataFrame(selecoes[1:], columns=selecoes[0])
# colocando em ordem de melhor investimento e mostrando o valor total que será necessário investir.
df_selecoes = df_selecoes.sort_values(by='Retorno X Porcentagem',ascending=False)
print(df_selecoes.to_string(index=False))
print(df_selecoes['Custo do investimento (R$)'].sum())
print(df_selecoes.groupby('Risco do investimento (R$)')["Custo do investimento (R$)"].sum())