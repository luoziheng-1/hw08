import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Tongyi
from langchain.chains import RetrievalQA
import os

# 配置API Key（请用环境变量，不要硬编码）
os.environ["DASHSCOPE_API_KEY"] = "your_api_key_here"

# 页面标题
st.title("个人知识库问答助手")

# 上传文档
uploaded_file = st.file_uploader("上传PDF文档", type="pdf")
if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    loader = PyPDFLoader("temp.pdf")
    pages = loader.load_and_split()
    
    # 切分文本
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = text_splitter.split_documents(pages)
    
    # 向量化
    embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
    db = Chroma.from_documents(texts, embeddings)
    
    # 构建问答链
    llm = Tongyi(model_name="qwen-turbo")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    st.success("文档已加载完成，可以开始提问！")

# 提问框
query = st.text_input("请输入你的问题：")
if st.button("提交问题") and query:
    result = qa_chain({"query": query})
    st.write("### 回答：")
    st.write(result["result"])
    st.write("### 参考来源：")
    for doc in result["source_documents"]:
        st.write(f"- 第{doc.metadata['page']+1}页：{doc.page_content[:100]}...")