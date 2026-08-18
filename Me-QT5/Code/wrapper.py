from flask import Flask, request, jsonify


from variables import tavily_api, auth_token
from huggingface_hub import login
login(token=auth_token)
import openmeteo_requests
import torch
import torch.nn.functional as F
import json
import re
from datasets import load_dataset
import requests
from datetime import datetime
import requests_cache
import pandas as pd
import copy
from retry_requests import retry
from tqdm.notebook import tqdm
import time
import numpy as np
from typing import List, Dict, Tuple, Optional, Literal, Union, Callable, Any
from dataclasses import dataclass
from enum import Enum
from tavily import TavilyClient

from transformers import T5Tokenizer, T5ForSequenceClassification, T5ForConditionalGeneration
from transformers import PreTrainedTokenizer, PreTrainedModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoConfig, AutoModel, AutoModelForCausalLM, BitsAndBytesConfig
import faiss
from sklearn.metrics.pairwise import cosine_similarity

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
import langchain

from ragclient import RAGClient
from typing import List
from sentence_transformers import SentenceTransformer
from agent_store import *
device = 'cuda' if torch.cuda.is_available() else 'cpu'

from agent import *
from complexity_evaluator import *
from custom_generate import *
from database import *
from filter import *
from memory import *
from prompts import *
from query_decomposer import *

model_save_path = '/final_pipeline/Cache'
bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )
model = AutoModelForCausalLM.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.3",
            device_map="auto",
            trust_remote_code=True,
            use_auth_token=True,
            quantization_config=bnb_config,
            cache_dir=model_save_path
        ).to(device)
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3", use_auth_token=True)
encoder = AutoModel.from_pretrained('google-bert/bert-base-uncased').to(device)
enc_tokenizer = AutoTokenizer.from_pretrained('google-bert/bert-base-uncased')
model_kwargs = {'device': device}
encode_kwargs = {'normalize_embeddings': True}
embedding_model = 'BAAI/bge-base-en-v1.5'
embedder = HuggingFaceBgeEmbeddings(model_name=embedding_model,
                         model_kwargs = model_kwargs,
                         encode_kwargs=encode_kwargs,
                         query_instruction="")

def main(query:str):
    sub_queries = decomposer.generate_sub_queries(query)
    sub_queries.append(query)
    agent_tracker = {}
    for sub_query in sub_queries:
        assigned_agent = agent_assigner.get_agent(sub_query)
        if sub_query == query:
            assigned_agent = "code_expert"
        agent_tracker[sub_query] = assigned_agent
        if assigned_agent == 'code_expert':
            l1 = short_memory.get_relevant_short_memory(sub_query)
            l2 = core_memory.get_relevant_memories(sub_query)
            l3 = database.retrieve(sub_query)
            aug_sub_query = prompt_temp(query, l1, l2, l3)
            outputs = coder_agent.generate(aug_sub_query)
            doc_files = doc_agent.generate(outputs)
            short_memory.add_query_text(f"Query:{sub_query}\nAnswer:\n{doc_files+outputs}")
            core_memory.add_qna(sub_query, outputs, doc_files)
        elif assigned_agent == 'math_expert':
            l1 = short_memory.get_relevant_short_memory(sub_query)
            l2 = []
            l3 = []
            aug_sub_query = prompt_temp(query, l1, l2, l3)
            outputs = math_expert.generate(aug_sub_query)
            short_memory.add_query_text(f"Query:{sub_query}\nAnswer:\n{outputs}")
        else:
            l1 = short_memory.get_relevant_short_memory(sub_query)
            l2 = []
            l3 = hr_database.retrieve(sub_query)
            aug_sub_query = prompt_temp(query, l1, l2, l3)
            outputs = hr_agent.generate(aug_sub_query)
            short_memory.add_query_text(f"Query:{sub_query}\nAnswer:\n{outputs}")

    outputs += '\n\nAgent tracker:\n\n'
    for k,v in agent_tracker.items():
        outputs += f'sub-query:{k}, agent: {v}\n'
    return outputs

class LLMSession:

    def __init__(self):
        self.conversation_history = []
        self.query_decomposer = QueryDecomposer(model,tokenizer,prompt_template)
        self.coder_agent = CodeGenerator(model, tokenizer,prompt_template_coder_agent, correction_prompt_coder_agent, pattern_correction_coder_agent)
        self.doc_agent = DocumentationGenerator(model, tokenizer, prompt_template_doc, pattern_correction_prompt_template_doc)
        self.math_expert = MathExpert(model, tokenizer, pt_math)
        self.hr_agent = HRManager(model, tokenizer)
        self.short_memory = ShortTermMemory()
        self.core_memory = Core_Memory(embedder, device)
        self.database = Database()
        self.database2 = Database2()
        self.agent_assigner = AgentStore(encoder, enc_tokenizer)
        self.agent_assigner.add_agent('''The Web Search Agent is a highly efficient tool designed to gather, filter, and summarize information from the internet. It specializes in conducting searches, retrieving relevant data, and providing accurate insights tailored to user needs. Equipped with advanced search algorithms and real-time access to web resources, this agent excels in navigating the vast digital landscape to deliver concise and actionable information.

Responsibilities:

Conduct targeted searches across the web to retrieve up-to-date information.
Summarize and synthesize information from multiple credible sources.
Monitor trends, news, and developments in specific domains.
Assist with research tasks, including academic, technical, and market research.
Evaluate the credibility and relevance of online content.
Provide references and citations for the gathered data in a user-friendly format.
This agent is particularly useful for users seeking precise and timely information without sifting through excessive data.''', 'math_expert')
        self.agent_assigner.add_agent('''The Coding Agent specializes in programming, software development, and debugging. It is designed to automate the development process, manage version control, and streamline technical workflows. Equipped with deep knowledge of multiple programming languages, frameworks, and best practices, this agent can handle tasks ranging from code generation to system optimization.

Responsibilities:

Generate, review, and debug code in various programming languages (e.g., Python, JavaScript, C++).
Build and integrate APIs, databases, and front-end/back-end systems.
Assist in deploying and maintaining software systems on cloud platforms.
Implement best practices for security, scalability, and performance.
Use machine learning libraries and frameworks to build AI models when required.
Automate repetitive coding tasks, version control management, and code documentation.''', 'code_expert')
        self.agent_assigner.add_agent('''The HR Manager Agent focuses on workforce management, talent acquisition, and employee engagement. Designed to emulate the strategic and empathetic aspects of human resource management, this agent ensures smooth operations and maintains a positive organizational culture.

Responsibilities:

Screen and shortlist candidates for job roles based on predefined criteria.
Automate onboarding processes and training programs for new hires.
Monitor employee performance and provide tailored development plans.
Conduct virtual interviews, manage HR analytics, and track team satisfaction.
Address workplace issues and provide data-driven solutions to improve productivity.
Maintain compliance with labor laws and organizational policies.''', 'hr_manager')

    def response(self, query):
        sub_queries = self.query_decomposer.generate_sub_queries(query)
        sub_queries.append(query)
        agent_tracker = {}
        for sub_query in sub_queries:
            assigned_agent = self.agent_assigner.get_agent(sub_query)
            if sub_query == query:
                assigned_agent = "code_expert"
            agent_tracker[sub_query] = assigned_agent
            if assigned_agent == 'code_expert':
                l1 = self.short_memory.get_relevant_short_memory(sub_query)
                l2 = self.core_memory.get_relevant_memories(sub_query)
                l3 = self.database.retrieve(sub_query)
                aug_sub_query = prompt_temp(query, l1, l2, l3)
                outputs = self.coder_agent.generate(aug_sub_query)
                doc_files = self.doc_agent.generate(outputs)
                self.short_memory.add_query_text(f"Query:{sub_query}\nAnswer:\n{doc_files+outputs}")
                self.core_memory.add_qna(sub_query, outputs, doc_files)
            elif assigned_agent == 'math_expert':
                l1 = self.short_memory.get_relevant_short_memory(sub_query)
                l2 = []
                l3 = []
                aug_sub_query = prompt_temp(query, l1, l2, l3)
                outputs = self.math_expert.generate(aug_sub_query)
                self.short_memory.add_query_text(f"Query:{sub_query}\nAnswer:\n{outputs}")
            else:
                l1 = self.short_memory.get_relevant_short_memory(sub_query)
                l2 = []
                l3 = self.hr_database.retrieve(sub_query)
                aug_sub_query = prompt_temp(query, l1, l2, l3)
                outputs = self.hr_agent.generate(aug_sub_query)
                self.short_memory.add_query_text(f"Query:{sub_query}\nAnswer:\n{outputs}")
        raw_output = outputs
        output = ""
        output += '\n\nAgent tracker:\n\n'
        for k,v in agent_tracker.items():
            output += f'SUB-QUERY:{k}   AGENT: {v}\n'
            output +='\n'
        return raw_output, output  
        
    def query(self,query_str:str):
        if self.conversation_history:
            response, __ = self.response('History: '+'\n'.join(self.conversation_history)+'Current Query:\n'+query_str)
        else:
            response, __ = self.response(query_str)
        self.conversation_history.append('Query:\n'+query_str+'\nAnswer:\n'+response)
        return response, __


if __name__=="__main__":
    
    obj = LLMSession()
    print(obj.query("python code for adding two numbers"))
    