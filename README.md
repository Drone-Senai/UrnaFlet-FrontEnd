# 🗳️ Urna Eletrônica com Flet

Projeto de Urna Eletrônica desenvolvido com [Flet](https://flet.dev), integrando um backend externo e compatível com dispositivos móveis (Android/iOS/PWA).

## 📱 Visão Geral

Este projeto simula uma urna eletrônica moderna, com interface intuitiva, suporte a múltiplos candidatos, captura de voto, integração com backend para registro e contagem, além de suporte mobile (PWA).

---

## ✨ Funcionalidades

* Interface de votação responsiva (desktop, tablet e mobile)
* Listagem dinâmica de candidatos via API
* Captura e confirmação do voto
* Validação por etapa (cargo, número, confirmação)
* Envio seguro do voto para o backend
* Compatível com PWA (Progressive Web App)
* Backend externo para registro, contagem e consulta de votos
* Reset automático ao fim da votação
* Registro de tempo e logs de votos para auditoria (sem identificação do eleitor)

---

## 🛠️ Tecnologias Utilizadas

### Frontend (Flet - Python)

* [Flet](https://flet.dev) como framework principal
* Deploy local e via web/PWA
* Compatível com Android/iOS via navegador ou instalação PWA

### Backend

* FastAPI (Python) / Flask (ou outro framework REST)
* SQLite  para armazenamento de votos
* JWT ou token personalizado para autenticação das urnas

---

## 🎞️ Estrutura do Projeto

```
urna-eletronica-flet/
│
├── frontend/
│   ├── main.py              # Aplicação Flet
│   ├── ui_components.py     # Componentes da interface
│   └── services.py          # Comunicação com o backend
│
├── backend/
│   ├── main.py              # API principal (FastAPI ou Flask)
│   ├── models.py            # Modelos de dados (votos, candidatos)
│   └── database.py          # Conexão e operações no banco de dados
│
├── README.md
└── requirements.txt
```

---

## 🚀 Como Rodar o Projeto

### ✅ Pré-requisitos

* Python 3.9+
* pip

### 🔧 Instalação

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/urna-eletronica-flet.git
cd urna-eletronica-flet

# Instalar dependências
pip install -r requirements.txt
```

### ▶️ Executar o Frontend

```bash
cd frontend
flet run main.py
```

### ▶️ Executar o Backend

```bash
cd backend
uvicorn main:app --reload
```

> Obs: Certifique-se de configurar o endereço da API corretamente no arquivo `services.py` do frontend.

---

## 📲 Compatibilidade Mobile

O frontend em Flet é totalmente compatível com:

* Navegadores mobile modernos (Chrome, Safari, Firefox)
* Instalação como PWA (Progressive Web App)
* Ideal para tablets ou celulares em modo paisagem

Para transformar o app em PWA:

1. Publicar o frontend com `flet publish` ou via container
2. Acessar o app via navegador no celular
3. Usar “Adicionar à tela inicial”

---

## 🛡️ Segurança

* Os votos são transmitidos via HTTPS para o backend
* A autenticação das urnas pode ser feita via token ou ID único
* Nenhum dado pessoal do eleitor é armazenado

---

## 📌 Possíveis Melhorias

* Reconhecimento facial ou biometria com OpenCV
* Dashboard para apuração em tempo real
* Criptografia dos votos
* Modo "admin" para encerrar/abrir sessões de votação

---

## 👨‍💻 Autor

Desenvolvido por [Seu Nome](https://github.com/seu-usuario)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
