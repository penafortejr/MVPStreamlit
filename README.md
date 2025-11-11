# SMEL Conectada — Protótipo Simples
Este projeto é um protótipo de um portal acadêmico inspirado no Planejamento de Tecnologia da Informação (PDTI) da Secretaria Municipal de Esportes (SMEL). Ele foi desenvolvido utilizando **Streamlit**, permitindo gerenciar eventos esportivos, registrar inscrições e exportar os dados.
## 🎯 Objetivo
O sistema oferece uma interface simples e funcional para:
- Listar eventos esportivos.
- Cadastrar novos eventos.
- Registrar participantes em eventos.
- Visualizar e exportar as inscrições.
Não há banco de dados permanente — os dados ficam armazenados apenas na **sessão atual do navegador**.
---
## 🧱 Estrutura Principal
### Sessão (`st.session_state`)
O sistema utiliza o `session_state` do Streamlit para armazenar:
- `events`: Lista de eventos cadastrados.
- `inscriptions`: Lista de inscrições realizadas.
Esses dados são temporários e serão perdidos ao recarregar a aplicação.
### Funções Principais
| Função | Descrição |
|-------|----------|
| `next_event_id()` | Gera automaticamente o próximo ID de evento. |
| `add_event(...)` | Adiciona um novo evento à lista. |
| `add_inscription(...)` | Registra uma inscrição vinculada a um evento. |
| `df_inscriptions()` | Converte a lista de inscrições em DataFrame para exibição/exportação. |
---
## 🧭 Menu e Páginas
A interface é organizada em páginas selecionadas na barra lateral:
- **🏠 Início**: Exibe os próximos eventos.
- **🏟️ Eventos**: Formulário para criar novos eventos + tabela de eventos atuais.
- **🧾 Inscrições**: Formulário para registrar participantes e visualização das inscrições.
- **📤 Exportar**: Exporta as inscrições em **CSV** ou **XLSX**.
- **ℹ️ Sobre**: Informações gerais sobre o projeto.
---
## 🎨 Estilo Visual
Foi utilizada uma personalização simples com CSS injetado no Streamlit, aplicando tema escuro e cartões estilizados para exibir eventos.
---
## 📦 Exportação
Os dados de inscrições podem ser baixados em dois formatos:
- `.csv` (nativo).
- `.xlsx` (requer o pacote opcional `xlsxwriter`).
---
## ✅ Tecnologias Utilizadas
- **Python**
- **Streamlit** (interface web)
- **Pandas** (manipulação de dados)
---
## 🚀 Como Executar
```bash
pip install streamlit pandas xlsxwriter
streamlit run app.py
```
---
## 📌 Observação
Este sistema é apenas um protótipo **sem banco de dados**. Para uso real em produção, seria necessário conectar a um banco como PostgreSQL, MySQL ou Google Sheets.
---
Desenvolvido para fins acadêmicos.
