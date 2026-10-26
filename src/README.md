# API de Atividades da Mergington High School

Uma aplicação FastAPI super simples que permite que estudantes visualizem e se inscrevam em atividades extracurriculares.

## Funcionalidades

- Visualizar todas as atividades extracurriculares disponíveis
- Inscrever-se em atividades
- Atualizar automaticamente os participantes e as vagas disponíveis após uma inscrição, sem recarregar a página

## Primeiros Passos

1. Instale as dependências:

   ```
   pip install fastapi uvicorn
   ```

2. Execute a aplicação:

   ```
   python app.py
   ```

3. Abra seu navegador e acesse:
   - Documentação da API: http://localhost:8000/docs
   - Documentação alternativa: http://localhost:8000/redoc

## Testes do backend

Na raiz do repositório, instale as dependências e execute os testes:

```bash
python -m pip install -r requirements.txt
python -m pytest tests/
```

Os testes em `tests/` usam pytest e o TestClient do FastAPI, sem precisar iniciar
um servidor. Eles verificam o redirecionamento inicial, a listagem de atividades,
as inscrições, os cancelamentos e as respostas de erro. Os dados em memória são
isolados e restaurados entre os testes.

## Endpoints da API

| Método | Endpoint                                                          | Descrição                                                                   |
| ------ | ----------------------------------------------------------------- | --------------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Obtém todas as atividades com seus detalhes e contagem atual de participantes |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Inscreve-se em uma atividade                                                |
| DELETE | `/activities/{activity_name}/signup?email=student@mergington.edu` | Remove a inscrição de um estudante                                          |

## Modelo de Dados

A aplicação usa um modelo de dados simples com identificadores significativos:

1. **Activities** - Usa o nome da atividade como identificador:

   - Descrição
   - Horário
   - Número máximo de participantes permitidos
   - Lista de emails dos estudantes inscritos

2. **Students** - Usa email como identificador:
   - Nome
   - Série/Ano escolar

Todos os dados são armazenados em memória, o que significa que os dados serão resetados quando o servidor reiniciar.
