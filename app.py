import streamlit as st
import openai
import sqlparse

openai.api_key = ""

def translate(prompt):
    model_engine = "text-davinci-003"
    prompt = f"""
        Aja como um tradutor de texto para sql, este é o relacionamento entre as tabelas do meu banco de dados hive:
        transactions:
            transaction_id: identificador da transação
            card_id: identificador do consumidor
            product: descrição do produto
            transaction_value: valor da transação
            transaction_date: data da transação
            company_id: identificador da empresa contratante
            establishment_id: identificador do estabelecimento

        companies:
            id: identificador da empresa contratante
            name: nome da empresa contratante
            city: cidade da empresa contratante
            state: estado da empresa contratante

        consumers:
            id: identificador do consumidor
            cpf: documento do consumidor
            name: nome do consumidor
            
        establishments:
            id: identificador do estabelecimento
            name: nome do estabelecimento
            city: cidade do estabelecimento
            state: estado do estabelecimento

        Espere minha entrada e gere como saída apenas a query sql.

    Minha entrada é: {prompt}
    """
    # Exemplos:
    # "Quantidade de consumidores e valor transacionado pela empresa contratante 'Empresa do João' nos últimos 6 meses nos produtos 'Crédito' e 'Débito'"
    # "Valor transacionado em média no estabelecimento Padaria do Zé no município de São Paulo"

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    response = completion.choices[0].text
    response = sqlparse.format(response, reindent=True, keyword_case='upper')
    response = response.replace('\n', '  \n')
    print(response)
    return response

prompt = st.text_area('O que você gostaria de consultar?', '')
if st.button('Enviar'):
    st.markdown(translate(prompt))
    
    