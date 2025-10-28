import streamlit as st
from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId
import os

st.set_page_config(page_title='E-Shop Brasil')

# Conexão com MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["eshop_db"]
col = db["products"]

st.title("🛒 E-Shop Brasil - Gestão de Produtos")
menu = st.sidebar.selectbox("Menu", ["Visualizar", "Inserir", "Editar"])

if menu == "Visualizar":
    st.subheader("Lista de Produtos")
    data = list(col.find())
    if data:
        df = pd.DataFrame(data)
        df["id"] = df["_id"].astype(str)
        df = df.drop(columns=["_id"])
        st.dataframe(df)
    else:
        st.info("Nenhum produto encontrado.")

elif menu == "Inserir":
    st.subheader("Inserir Produto")
    nome = st.text_input("Nome")
    preco = st.number_input("Preço", min_value=0.0)
    categoria = st.text_input("Categoria")

    if st.button("Salvar"):
        if nome and categoria:
            col.insert_one({"nome": nome, "preco": preco, "categoria": categoria})
            st.success("Produto salvo!")
        else:
            st.error("Preencha todos os campos!")

elif menu == "Editar":
    st.subheader("Editar / Excluir Produto")
    data = list(col.find())
    if data:
        df = pd.DataFrame(data)
        df["id"] = df["_id"].astype(str)
        selected = st.selectbox("Selecione o produto", df["id"])
        prod = col.find_one({"_id": ObjectId(selected)})

        novo_nome = st.text_input("Nome", prod["nome"])
        novo_preco = st.number_input("Preço", min_value=0.0, value=float(prod["preco"]))
        nova_cat = st.text_input("Categoria", prod["categoria"])

        col1, col2 = st.columns(2)
        if col1.button("Salvar alterações"):
            col.update_one({"_id": prod["_id"]}, {"$set": {"nome": novo_nome, "preco": novo_preco, "categoria": nova_cat}})
            st.success("Alterado!")

        if col2.button("Excluir"):
            col.delete_one({"_id": prod["_id"]})
            st.success("Excluído!")
    else:
        st.info("Nenhum produto encontrado.")
