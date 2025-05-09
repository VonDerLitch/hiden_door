EXECUTAR:python -m hiden_door.interface


meu_sistema/
│
├── data/
│   ├── input/              # Arquivos de entrada (raw data, configs)
│   └── processed/          # Arquivos de saída/resultados
│
├── meu_sistema/            # Pacote principal do sistema
│   ├── __init__.py
│   ├── config.py           # Configurações globais e constantes
│   ├── main.py             # Ponto de entrada principal do sistema
│   ├── core/               # Lógica de negócio
│   │   ├── __init__.py
│   │   └── processor.py    # Ex: classe de processamento principal
│   ├── services/           # Serviços auxiliares (I/O, API, etc.)
│   │   ├── __init__.py
│   │   ├── file_manager.py
│   │   └── data_loader.py
│   └── utils/              # Funções utilitárias genéricas
│       ├── __init__.py
│       └── logger.py
│
├── tests/                  # Testes unitários e de integração
│   ├── __init__.py
│   └── test_processor.py
│
├── requirements.txt        # Dependências do projeto
├── pyproject.toml          # Configurações do projeto (ex: black, isort)
└── README.md               # Documentação inicial do projeto