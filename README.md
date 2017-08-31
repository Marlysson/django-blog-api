## Atividade de Tópicos especiais com a finalidade de:

- Criar script de importação de json para banco de dados.
- Criar api para consumir esses dados importados.

#### Como importar os dados

> O arquivo deve estar na raiz do projeto.
> Execute o comando migrate para as tabelas serem criadas no banco de dados.

```
python manage.py migrate
```

Execute o comando:

> Nome padrão do arquivo: **db.json**

```
python manage.py populate_blog
```

> Ou utilizando outro nome:

```
python manage.py populate_blog --filename json_name.json
```
