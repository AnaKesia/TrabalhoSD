function gerarId() {
    return Date.now().toString() +
           Math.random().toString(36).substring(2);
}

function formatarPreco(valor) {

    valor = valor.replace(/[^0-9,]/g, "");

    if (!valor.includes(",")) {
        valor = valor + ",00";
    }

    let partes = valor.split(",");
    if (partes.length > 2) {
        valor = partes[0] + "," + partes[1];
    }

    return valor;
}

async function cadastrar() {

    let nome = document.getElementById("nome").value;
    let precoInput = document.getElementById("preco").value;

    if (!nome) {
        alert("Digite o nome do produto");
        return;
    }

    let preco = formatarPreco(precoInput);

    if (preco === ",00") {
        alert("Preço inválido");
        return;
    }

    let produto = {
        id: Date.now().toString(),
        nome,
        preco
    };

    try {
        await fetch("http://localhost:5000/produtos", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(produto)
        });

    } catch {
        await fetch("http://localhost:5001/produtos", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(produto)
        });
    }

    listar();
}

async function listar() {

    let lista = document.getElementById("lista");
    lista.innerHTML = "";

    let dados;

    try {
        let r = await fetch("http://localhost:5000/produtos");
        dados = await r.json();
    } catch {
        let r = await fetch("http://localhost:5001/produtos");
        dados = await r.json();
    }

    dados.forEach(p => {

        let li = document.createElement("li");

        li.innerHTML = `
            <span class="produto-texto">
                <b>${p.nome}</b> - R$ ${p.preco}
            </span>

            <button class="btn btn-edit"
                onclick="editar('${p.id}', '${p.nome}', '${p.preco}')">
                <i class="fa-solid fa-pen"></i>
            </button>

            <button class="btn btn-delete"
                onclick="deletar('${p.id}')">
                <i class="fa-solid fa-trash"></i>
            </button>
        `;

        lista.appendChild(li);
    });
}

async function deletar(id) {

    let confirmar = confirm("Tem certeza que deseja deletar este produto?");

    if (!confirmar) return;

    try {
        await fetch(`http://localhost:5000/produtos/${id}`, {
            method: "DELETE"
        });
    } catch {
        await fetch(`http://localhost:5001/produtos/${id}`, {
            method: "DELETE"
        });
    }

    listar();
}

async function editar(id, nomeAtual, precoAtual) {

    let nome = prompt("Novo nome:", nomeAtual);
    let preco = prompt("Novo preço:", precoAtual);

    if (!nome || !preco) return;

    let produto = { nome, preco };

    try {
        await fetch(`http://localhost:5000/produtos/${id}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(produto)
        });
    } catch {
        await fetch(`http://localhost:5001/produtos/${id}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(produto)
        });
    }

    listar();
}

