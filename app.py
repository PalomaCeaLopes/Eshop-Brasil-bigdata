import streamlit as st
from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId

# ==========================
# CONFIGURAÇÃO INICIAL
# ==========================
st.set_page_config(page_title="E-Shop Brasil", page_icon="🛒")

st.title("🛍️ E-Shop Brasil - Gestão de Produtos")

# ==========================
# CONEXÃO COM MONGODB ATLAS
# ==========================
MONGO_URI = "mongodb+srv://palomacealopes_db_user:H1lAYGlJ9H3tC03y@cluster0.vgyhoan.mongodb.net/?retryWrites=true&w=majority&tls=true"

try:
    client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
    client.admin.command("ping")  # Teste de conexão
    st.sidebar.success("✅ Conectado ao MongoDB Atlas com sucesso!")
except Exception as e:
    st.sidebar.error(f"❌ Erro na conexão com MongoDB: {e}")

db = client["eshop_brasil"]
col = db["produtos"]

# ==========================
# MENU LATERAL
# ==========================
menu = st.sidebar.radio("Menu", ["Visualizar", "Inserir", "Editar", "Excluir"])

# ==========================
# VISUALIZAR PRODUTOS
# ==========================
if menu == "Visualizar":
    st.subheader("📋 Lista de Produtos")
    data = list(col.find())

    if data:
        df = pd.DataFrame(data)
        df["_id"] = df["_id"].astype(str)
        st.dataframe(df)
    else:
        st.info("Nenhum produto encontrado.")

# ==========================
# INSERIR PRODUTO
# ==========================
elif menu == "Inserir":
    st.subheader("➕ Inserir Novo Produto")

    nome = st.text_input("Nome do Produto")
    preco = st.number_input("Preço (R$)", min_value=0.0, step=0.01)
    categoria = st.text_input("Categoria")

    if st.button("Salvar Produto"):
        if nome and preco and categoria:
            col.insert_one({"nome": nome, "preco": preco, "categoria": categoria})
            st.success("✅ Produto inserido com sucesso!")
        else:
            st.warning("⚠️ Preencha todos os campos antes de salvar.")

# ==========================
# EDITAR PRODUTO
# ==========================
elif menu == "Editar":
    st.subheader("✏️ Editar Produto")

    data = list(col.find())
    if data:
        df = pd.DataFrame(data)
        df["_id"] = df["_id"].astype(str)
        selected = st.selectbox("Selecione um produto", df["_id"])
        produto = col.find_one({"_id": ObjectId(selected)})

        novo_nome = st.text_input("Novo nome", value=produto["nome"])
        novo_preco = st.number_input("Novo preço (R$)", value=float(produto["preco"]))
        nova_categoria = st.text_input("Nova categoria", value=produto["categoria"])

        if st.button("Salvar alterações"):
            col.update_one(
                {"_id": ObjectId(selected)},
                {"$set": {"nome": novo_nome, "preco": novo_preco, "categoria": nova_categoria}}
            )
            st.success("✅ Produto atualizado com sucesso!")
    else:
        st.info("Nenhum produto disponível para edição.")

# ==========================
# EXCLUIR PRODUTO
# ==========================
elif menu == "Excluir":
    st.subheader("🗑️ Excluir Produto")

    data = list(col.find())
    if data:
        df = pd.DataFrame(data)
        df["_id"] = df["_id"].astype(str)
        selected = st.selectbox("Selecione o produto para excluir", df["_id"])
        produto = col.find_one({"_id": ObjectId(selected)})

        st.write(f"**Produto:** {produto['nome']} | **Preço:** R$ {produto['preco']} | **Categoria:** {produto['categoria']}")

        if st.button("Excluir Produto"):
            col.delete_one({"_id": ObjectId(selected)})
            st.success("🗑️ Produto excluído com sucesso!")
    else:
        st.info("Nenhum produto encontrado para exclusão.")
