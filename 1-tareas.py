from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain_groq import ChatGroq

my_llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

agente_buscador = Agent(
    role='buscador',
    goal='Encuentra la ultima noticia sobre IA',
    backstory="""Eres un investigador en una empresa grande.
    Eres responsable de analizar datos y proporcionar perspectivas al negocio.""",
    # tools=None,
    llm=my_llm,
    function_calling_llm=my_llm,
    max_iter=5,
    max_rpm=None,
    verbose=True,
    allow_delegation=True,
    # step_callback=my_intermediate_step_callback,
    cache=True
)
agente_traductor = Agent(
    role='buscador',
    goal='Traducir la respuesta del agente que te envió',
    backstory="""Eres un traductor de Ingles a Español con ambas lenguas nativas.""",
    # tools=None,
    llm=my_llm,
    function_calling_llm=my_llm,
    max_iter=5,
    max_rpm=None,
    verbose=True,
    allow_delegation=True,
    # step_callback=my_intermediate_step_callback,
    cache=True
)

Herramienta_buscar = SerperDevTool()

research_ai_task = Task(
    description='Encuentra y resume las últimas noticias sobre inteligencia artificial.',
    expected_output='Un resumen en forma de lista de viñetas de las 5 noticias más importantes sobre AI.',
    agent=agente_buscador,
    tools=[Herramienta_buscar]
)

research_ops_task = Task(
    description='Encuentra y resume las últimas noticias sobre AI Ops.',
    expected_output='Un resumen en forma de lista de viñetas de las 5 noticias más importantes sobre AI Ops.',
    agent=agente_buscador,
    tools=[Herramienta_buscar]
)

write_blog_task = Task(
    description='Traduce al español la respuesta que te den',
    expected_output='Entrada de blog completa traducida al español.',
    agent=agente_traductor,
    context=[research_ai_task, research_ops_task]
)

crew = Crew(
    agents=[agente_traductor],
    tasks=[research_ai_task, research_ops_task, write_blog_task],
    verbose=2
)

result = crew.kickoff()
print(result)
