1. API KEY

```python
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')
```

```.env
GROQ_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Ver variables en el entorno powershell:

```bash
Get-ChildItem Env:
```
```powershell
$env:GROQ_API_KEY ="xxxxxx"
$env:GROQ_API_KEY = $null
```



2. Intalar crewAI

```
pip install crewai
pip install 'crewai[tools]'
```

3. Intalar langchain_groq

```bash
pip install langchain-groq
```

4. API KEY de Serper (buscador gratuito)
[página](https://serper.dev/)

cuenta: diablo

contr: javi

```powershell
$env:SERPER_API_KEY = "xxxxxxxxx"
```

