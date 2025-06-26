![Alt](https://repobeats.axiom.co/api/embed/48f394a39ddf5d02bcf27168c27eb58833f31209.svg "Repobeats analytics image")

# Projeto Eros - Assistente Virtual

Eros é um projeto pessoal de assistente virtual com foco em aprendizado de desenvolvimento de inteligência artificial. Este repositório documenta o progresso de cada etapa do projeto, desde a criação de uma interface de chat básica até o desenvolvimento de funcionalidades mais complexas.

**Importante:** O projeto está sendo desenvolvido com fins educacionais e pode conter mudanças frequentes na estrutura e funcionalidades. A documentação será atualizada conforme o projeto evolui.

## Objetivos

* Estudar e aplicar conceitos fundamentais de IA e NLP (Processamento de Linguagem Natural);
* Desenvolver um assistente virtual que execute comandos úteis e interaja com o usuário via terminal;
* Aprender a estruturar, modularizar e treinar modelos de IA;
* Criar uma base de conhecimento reutilizável e extensível.

## Estrutura Inicial

O projeto será modularizado com as seguintes pastas:

```
eros/
├── cli/            # Interface com o usuário (terminal/chat)
├── core/           # Núcleo do assistente (classe Assistant, gerenciamento)
├── data/           # Base de dados, intents, histórico, configurações
├── learning/       # Módulos de aprendizado, feedback, sugestões
├── nlp/            # Ferramentas de NLP e inteligência
├── tools/          # Funções auxiliares (sistema, arquivos, web, etc)
└── main.py         # Ponto de entrada da aplicação
```

## Requisitos (temporários)

* Python 3.10+
* Bibliotecas:

  * `nltk`
  * `spacy`
  * `scikit-learn`
  * `requests`
  * `beautifulsoup4`
  * `psutil`

## Como executar (versão inicial)

```bash
python eros/main.py
```

## Licença

Projeto com fins de estudo e sem fins lucrativos. Nenhuma restrição de uso até o momento.

---

# Milestones (Etapas do Desenvolvimento)

### Milestone 1: Estrutura Inicial do Projeto

* [x] Definir estrutura de pastas
* [x] Criar `main.py` com loop de entrada/saída
* [x] Criar classe `Assistant`

### Milestone 2: Processamento de Linguagem Natural

* [x] Criar `intents.json` com exemplos simples e variados
* [x] Implementar lematização/tokenização com `TfidfVectorizer`
* [x] Treinar classificador com `SVC`
* [x] Adicionar respostas automáticas por intencão
* [x] Implementar controle por confiança
* [x] Integrar o classificador ao Assistant

### Milestone 3: Funções Utilitárias

* [ ] Comando `hora` e `data`
* [ ] Comando `abrir` programas
* [ ] Comando `ajuda`
* [ ] Clima via API

<!--
### Milestone 4: Memória e Aprendizado

* [ ] Registro de histórico em banco de dados
* [ ] Coleta de feedback e sugestões
* [ ] Aprendizado supervisionado básico

### Milestone 5: Reorganização e Evolução

* [ ] Modularizar completamente o projeto
* [ ] Reduzir dependências externas (API)
* [ ] Preparar para modelos customizados
-->

---

> Este README será atualizado a cada fase do projeto com mais detalhes técnicos e avanços obtidos.

