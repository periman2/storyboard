from config import VERTEX_AI_TEMP
from helpers import is_doc, is_docx, is_pdf, is_txt
from langchain.llms import VertexAI
from langchain import PromptTemplate, LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import Docx2txtLoader, UnstructuredWordDocumentLoader, PDFPlumberLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

from typing import List, Any

from dotenv import load_dotenv
load_dotenv()

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