# Using ollama embeddings:
    # Loading took 0.2535700798034668 seconds, TOTAL: 0.25357580184936523
    # Splitting took 0.0022139549255371094 seconds, TOTAL: 0.255828857421875
    # Storing took 994.4652690887451 seconds, TOTAL: 994.7211449146271
    # Retrieving took 1.8037610054016113 seconds for a doc length of 4 documents, TOTAL: 996.5250060558319
    # Loading RAG prompt took 0.8468890190124512 seconds, TOTAL: 997.3719339370728
    # Loading LLM took 0.0008499622344970703 seconds, TOTAL: 997.3728168010712
    # QA chain took 341.43748784065247 seconds, TOTAL: 1338.8103289604187

from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings
from langchain.embeddings import OllamaEmbeddings  # We can also try Ollama embeddings
from langchain import hub
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
import time

start_time = time.time()

# Load web page
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
data = loader.load()

last_time = start_time
print(f"Loading took {time.time() - last_time} seconds, TOTAL: {time.time() - start_time}")
last_time = time.time()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
all_splits = text_splitter.split_documents(data)

print(f"Splitting took {time.time() - last_time} seconds, TOTAL: {time.time() - start_time}")
last_time = time.time()

# Embed and store
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OllamaEmbeddings())

print(f"Storing took {time.time() - last_time} seconds, TOTAL: {time.time() - start_time}")
last_time = time.time()

# Retrieve
question = "How can Task Decomposition be done?"
docs = vectorstore.similarity_search(question)
doc_len = len(docs)


print(f"Retrieving took {time.time() - last_time} seconds for a doc length of {doc_len} documents, TOTAL: {time.time() - start_time}")
last_time = time.time()

# RAG prompt
QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt-llama")

print(f"Loading RAG prompt took {time.time() - last_time} seconds, TOTAL: {time.time() - start_time}")
last_time = time.time()

# LLM
llm = Ollama(
    model="llama2",
    verbose=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

print(f"Loading LLM took {time.time() - last_time} seconds, TOTAL: {time.time() - start_time}")
last_time = time.time()

# QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
)

question = "What are the various approaches to Task Decomposition for AI Agents?"
result = qa_chain({"query": question})

print(f"QA chain took {time.time() - last_time} seconds, TOTAL: {time.time() - start_time}")
last_time = time.time()
