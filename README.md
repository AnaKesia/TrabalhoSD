# Sistema de Banco de Dados Distribuído

## Descrição

Este projeto consiste em um sistema distribuído simples para cadastro de produtos, desenvolvido como atividade da disciplina de Sistemas Distribuídos.

O sistema utiliza dois servidores independentes que realizam replicação de dados por meio de APIs REST. Caso um dos servidores fique indisponível, o outro continua operando normalmente, caracterizando tolerância a falhas. Quando o servidor retorna, ocorre sincronização dos dados armazenados.

## Funcionalidades

- Cadastro de produtos
- Listagem de produtos
- Edição de produtos
- Exclusão de produtos
- Replicação de dados entre servidores
- Persistência dos dados em arquivos JSON
- Tolerância a falhas
- Consistência eventual
- Interface web para gerenciamento dos produtos

## Tecnologias Utilizadas

- Python 3
- Flask
- Requests
- HTML
- CSS
- JavaScript
- Font Awesome

---

# Executando o Sistema

## 1. Iniciar o Servidor A

Abra um terminal na pasta do Servidor A e execute:

```bash
python server_a.py
```

O servidor ficará disponível em:

```text
http://localhost:5000
```

---

## 2. Iniciar o Servidor B

Abra outro terminal na pasta do Servidor B e execute:

```bash
python server_b.py
```

O servidor ficará disponível em:

```text
http://localhost:5001
```

---

## 3. Acessar a Aplicação

Abra o navegador e acesse:

```text
http://localhost:5000
```

ou

```text
http://localhost:5001
```

Ambos possuem a mesma interface.

---

# Testando a Replicação

1. Inicie os dois servidores.
2. Cadastre um produto.
3. Acesse:

```text
http://localhost:5000/produtos
```

e

```text
http://localhost:5001/produtos
```

Os mesmos dados deverão aparecer nos dois servidores.

---

# Testando a Tolerância a Falhas

1. Inicie os dois servidores.
2. Cadastre alguns produtos.
3. Desligue um dos servidores.
4. Continue realizando operações utilizando o servidor restante.
5. Religue o servidor desligado.
6. Selecione o botão "Atualizar" para realizar sincronização.
7. Verifique que os dados foram recuperados.

---

# Conceitos de Sistemas Distribuídos Aplicados

Este projeto demonstra os seguintes conceitos:

- Comunicação entre processos via REST
- Replicação de dados
- Tolerância a falhas
- Consistência eventual
- Persistência distribuída
- Sincronização entre nós

---

# Limitações

O sistema foi desenvolvido com fins educacionais.

Limitações atuais:

- Não utiliza banco de dados relacional.
- Não implementa transações distribuídas.
- Não implementa algoritmos de eleição de líder.
- Não possui autenticação de usuários.
- Utiliza consistência eventual em vez de consistência forte.
