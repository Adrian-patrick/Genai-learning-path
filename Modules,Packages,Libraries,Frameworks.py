"""
Modules
a single py file
one responsibility per module
logic separation
example
"""
validation.py
token_utils.py
logging_config.py

"""
packages
folder containing modules
example
"""
app/
    __init__.py
    services/
        __init__.py
        llm_service.py
        embedding_service.py
    api/
        routes.py

"""
Libraries
reusable code written by others
"""
pydantic
fastapi
s
"""
Frameworks
controls structure of application
"""
FastAPI
Flask

"""
Industry level folder structure
"""
app/
    main.py
    api/
        routes.py
    services/
        rag_pipeline.py
        llm_client.py
    models/
        request_models.py
    core/
        config.py
        logging.py
    db/
        database.py

