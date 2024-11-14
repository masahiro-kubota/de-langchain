#!/usr/bin/env python3

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")

loader = UnstructuredMarkdownLoader("/home/masa/Documents/planning_documentation/index.md")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size = 1000,
  chunk_overlap = 200,
  add_start_index = True)

all_splits = text_splitter.split_documents(docs)

vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

#print(retrieved)
prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
  return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
  {"context": retriever | format_docs, "question": RunnablePassthrough()}
  | prompt
  | llm
  | StrOutputParser()
)
#response_dict = rag_chain.invoke("What is planning")
#print(response_dict)
print(isinstance(llm))
