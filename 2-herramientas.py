from crewai import Agent, Task, Crew, Process
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool
)
from langchain_groq import ChatGroq

my_llm = ChatGroq(temperature=0.7, model_name="llama3-70b-8192")

docs_tool = DirectoryReadTool(directory='./blog-posts')
file_tool = FileReadTool()
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool(
    config=dict(
        llm=dict(
            provider="openai",  # or google, openai, anthropic, llama2, ...
            config=dict(
                model="gpt-3.5-turbo-16k",
                temperature=0.7,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="openai",
            config=dict(
                model="text-embedding-ada-002",
                # task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)

researcher = Agent(
    role='Analista de estudios de mercado',
    goal='Proporcionar análisis de mercado actualizados de la industria de los videojuegos',
    backstory='Analista experto con buen ojo para las tendencias del mercado.',
    tools=[search_tool, web_rag_tool],
    llm=my_llm,
    function_calling_llm=my_llm,
    max_iter=4,
    max_rpm=2900,
    verbose=True,
    allow_delegation=True,
    # step_callback=my_intermediate_step_callback,
    cache=True
)

writer = Agent(
    role='Redactor de contenidos.',
    goal='Crear entradas de blog atractivas sobre el sector de los videojuegos.',
    backstory='Escritor experto y apasionado de los videojuegos.',
    tools=[docs_tool, file_tool],
    llm=my_llm,
    function_calling_llm=my_llm,
    max_iter=4,
    max_rpm=2900,
    verbose=True,
    allow_delegation=True,
    # step_callback=my_intermediate_step_callback,
    cache=True
)

research = Task(
    description='Investiga las últimas tendencias en el sector de los videojuegos y haz un resumen.',
    expected_output='Un resumen de las 3 tendencias más importantes en el sector de los videojuegos con una perspectiva única de su importancia.',
    agent=researcher
)

write = Task(
    description='Escriba una entrada de blog atractiva sobre la industria de los videojuegos, basada en el resumen del analista de investigación. Inspírate en las últimas entradas de blog del directorio.',
    expected_output='Una entrada de blog de 4 párrafos formateada en markdown con contenido atractivo, informativo y accesible, evitando jerga compleja y en español.',
    agent=writer,
    output_file='blog-posts/new_post.md'  # The final blog post will be saved here
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research, write],
    process=Process.sequential,
    memory=True,
    verbose=2,
    embedder={
        "provider": "openai",
        "config": {
                    "model": 'text-embedding-ada-002'
        }
    }

)

crew.kickoff()
