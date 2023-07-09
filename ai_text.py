from config import VERTEX_AI_TEMP
from helpers import is_doc, is_docx, is_pdf, is_txt
from langchain.llms import VertexAI
from langchain import PromptTemplate, LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import Docx2txtLoader, UnstructuredWordDocumentLoader, PDFPlumberLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import os
import json

from typing import List, Any

from dotenv import load_dotenv
load_dotenv()

credentials = {
    "type": os.environ.get('GAC_TYPE'),
    "project_id": os.environ.get('GAC_PROJECT_ID'),
    "private_key_id": os.environ.get('GAC_PRIVATE_KEY_ID'),
    "private_key": os.environ.get('GAC_PRIVATE_KEY'),
    "client_email": os.environ.get('GAC_CLIENT_EMAIL'),
    "client_id": os.environ.get('GAC_CLIENT_ID'),
    "auth_uri": os.environ.get('GAC_AUTH_URI'),
    "token_uri": os.environ.get('GAC_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.environ.get('GAC_AUTH_CERT_URI'),
    "client_x509_cert_url": os.environ.get('GAC_CLIENT_CERT_URL'),
    "universe_domain": os.environ.get('GAC_UNIVERSE_DOMAIN')
}

filename = "credentials.json"
with open(filename, "w") as json_file:
    json.dump(credentials, json_file, indent=4)

text_splitter = CharacterTextSplitter(chunk_size=900, separator="")

llm = VertexAI(model_name="text-bison@001",max_output_tokens=1024,temperature=VERTEX_AI_TEMP)
llm_strict = VertexAI(model_name="text-bison@001",max_output_tokens=1024,temperature=0)

def exectuteTextAIPrompt(prompt):
    return llm(prompt)

def exectuteTextAIPromptStrict(prompt):
    return llm_strict(prompt)

def executeDocumentSummarization(docPath: str):
    
    docs = None
    
    if is_docx(docPath):
        docs = Docx2txtLoader(docPath).load()
    elif is_pdf(docPath):
        docs = PDFPlumberLoader(docPath).load()
    elif is_txt(docPath):
        docs = TextLoader(docPath).load()

    if docs is None:
        return
    
    texts = text_splitter.split_text(docs[0].page_content)
    
    docs = [Document(page_content=t) for t in texts[:3]]
    
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    return chain.run(docs)