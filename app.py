import chainlit as cl

import arxiv

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain.llms.openai import OpenAI
from langchain_community.chat_models import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

@cl.on_chat_start
async def init():
    arxiv_query = None
    
    while arxiv_query is None:
        arxiv_query = await cl.AskUserMessage(
            content='Enter a topic', timeout=15
        ).send()
    
    print(arxiv_query)
    search = arxiv.Search(
        query=arxiv_query['output'],
        max_results=5,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    pdf_data = []
    for result in search.results():
        print(result.pdf_url)
        loader = PyMuPDFLoader(result.pdf_url)
        loaded_pdf = loader.load()
        
        for doc in loaded_pdf:
            doc.metadata['source'] = result.entry_id
            doc.metadata['file_path'] = result.pdf_url
            doc.metadata['title'] = result.title
            pdf_data.append(doc)
            
    embeddings = OpenAIEmbeddings(
        disallowed_special=()
    )
    
    docsearch = Chroma.from_documents(pdf_data, embeddings)
    OpenAI()
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=ChatOpenAI(
            model_name='gpt-3.5-turbo',
            temperature=0
        ),
        chain_type='stuff',
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
    )
    
    await cl.Message(
        content=f"""
        There are the papers relevant for your request `{arxiv_query['output']}`
        You can ask your question
        """
    ).send()
    
    cl.user_session.set("chain", chain)
    

@cl.on_message
async def process_response(msg: cl.Message):
    chain = cl.user_session.get("chain")
    cb = cl.AsyncLangchainCallbackHandler()
    
    response = await chain.acall(msg.content, callbacks=[cb])
    answer = response['answer']
    source_elements_dict = {}
    source_elements = []
    
    for _, source in enumerate(response['source_documents']):
        title = source.metadata['title']
        
        if title not in source_elements_dict:
            source_elements_dict[title] = {
                "n_pages": [source.metadata['page']],
                "url": source.metadata['file_path']
            }
        else:
            source_elements_dict[title]['n_pages'].append(source.metadata['page'])
        source_elements_dict[title]['n_pages'].sort()
        
    for title, source in source_elements_dict.items():
        n_pages = ', '.join([str(x) for x in source['n_pages']])
        text_source = f'Page Numbers : {n_pages}\nUrl : {source["url"]}'
        source_elements.append(
            cl.Text(name=title, content=text_source, display='inline')
        )
        
    await cl.Message(content=answer, elements=source_elements).send()
    
    
        