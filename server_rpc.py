import xmlrpc.server
import sys
import json

def mainServer() :
    if len(sys.argv) != 2:
        print ('%s <porta>' % sys.argv[0]) 
        sys.exit(0)

    porta = int(sys.argv[1])

    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", porta ))

    server.register_function(CriarLivro, "CriarLivro")
    server.register_function(ConsultarLivroAutor, "ConsultarLivroAutor")
    server.register_function(ConsultarLivroTitulo, "ConsultarLivroTitulo")
    server.register_function(ConsultarLivroPorAnoEdicao, "ConsultarLivroPorAnoEdicao")
    server.register_function(RemoverLivro, "RemoverLivro")
    server.register_function(AlterarLivro, "AlterarLivro")

    server.serve_forever()

def ConsultarBaseLivros():
	try:
		with open("bancoDados.json", "r") as json_file:
			dados = json.load(json_file)
	except:
		dados = json.loads('[]')
	return dados

def PersistirBaseLivros(baseLivros):
	with open("bancoDados.json", "w") as json_file:
		json.dump(baseLivros, json_file, indent=4)

def CriarLivro(jsonRecebido):
    livro_novo = json.loads(jsonRecebido)
    ultimoCodigo = 0
    baseLivros = ConsultarBaseLivros()

    for livro in baseLivros:
        if (livro["codigo"] > ultimoCodigo):
            ultimoCodigo = livro["codigo"]

    if (ultimoCodigo == 0):
        livro_novo["codigo"] = 1
    else :
        livro_novo["codigo"] = ultimoCodigo + 1

    baseLivros.append(livro_novo)
    PersistirBaseLivros(baseLivros)

    mensagemEnviar = ("Livro inserido!")
    return mensagemEnviar

def ConsultarLivroAutor(jsonRecebido):
	livro_consulta = json.loads(jsonRecebido)
	baseLivros = ConsultarBaseLivros()
	livrosRetorno = json.loads('[]')

	for livro in baseLivros:
		if (livro["autor"] == livro_consulta["autor"]):
			livrosRetorno.append(livro)

	return (json.dumps(livrosRetorno))

def ConsultarLivroTitulo(jsonRecebido):
	livro_consulta = json.loads(jsonRecebido)
	baseLivros = ConsultarBaseLivros()
	livrosRetorno = json.loads('[]')

	for livro in baseLivros:
		if (livro["titulo"] == livro_consulta["titulo"]):
			livrosRetorno.append(livro)

	return (json.dumps(livrosRetorno))

def ConsultarLivroPorAnoEdicao(jsonRecebido):
	livro_consulta = json.loads(jsonRecebido)
	baseLivros = ConsultarBaseLivros()
	livrosRetorno = json.loads('[]')

	for livro in baseLivros:
		if (livro["edicao"] == livro_consulta["edicao"] and livro["anoPublicacao"] == livro_consulta["anoPublicacao"]):
			livrosRetorno.append(livro)

	return (json.dumps(livrosRetorno))

def RemoverLivro(jsonRecebido):
	livro_exclusao = json.loads(jsonRecebido)
	baseLivros = ConsultarBaseLivros()

	for livro in baseLivros:
		if (livro["titulo"] == livro_exclusao["titulo"]):
			baseLivros.remove(livro)

	PersistirBaseLivros(baseLivros)

	mensagemEnviar = ("Livro removido!")
	return mensagemEnviar

def AlterarLivro(jsonRecebido):
	livro_alteracao = json.loads(jsonRecebido)
	baseLivros = ConsultarBaseLivros()

	for livro in baseLivros:
		if (livro["codigo"] == livro_alteracao["codigo"]):
			baseLivros.remove(livro)
			baseLivros.append(livro_alteracao)

	PersistirBaseLivros(baseLivros)
	
	mensagemEnviar = ("Livro alterado!")
	return mensagemEnviar

mainServer()