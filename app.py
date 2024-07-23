import streamlit as st
import fdb
import pandas as pd

def get_data_from_firebird():
    # Conecte-se ao banco de dados Firebird
    con = fdb.connect(
        dsn='c:/ecosis/dados/ecodados.eco',  # Substitua pelo caminho correto do seu banco de dados
        user='sysdba',
        password='masterkey'
    )
    
    # Crie um cursor para executar consultas
    cur = con.cursor()

    query = """
    with vendas as (
        select
            ped.empresa,
            ped.codigo as pedido,
            extract(year from ped.dataefe) || '/' || lpad(extract(month from ped.dataefe),2,'0') as ano_mes,
            ped.dataefe as data_efe,
            ped.notanfe as nfe,
            ped.numeronfce as nfce,
            ped.agente,
            age.nome as nome_agente,
            ven.codigo as vendedor,
            ven.nome as nome_vendedor,
            clg.nome || ' (' || clg.codigo || ')' as cliente,
            cid.nome || ' (' || cid.codigo || ')' as cidade,
            cid.estado,
            reg.nome || ' (' || reg.codigo || ')' as regiao,
            atv.descricao || ' (' || atv.codigo || ')' as atividade,
            clg.cep,
            case nat.tipoentrada
                when 'D' then 'Devolução'
                else 'Venda'
            end as tipo,
            pdt.produto as cod_produto,
            pdg.descricaograde || ' - ' || pdg.embalagem || '/' || cast(pdg.qtdeembalagem as integer) as produto,
            mar.descricao || ' (' || mar.codigo || ')' as marca,
            fab.descricao || ' (' || fab.codigo || ')' as fabricante,
            str.descricao || ' (' || str.codigo || ')' as setor,
            grp.descricao || ' (' || grp.codigo || ')' as grupo,
            grp.descricao || '-' || sgr.descricao || ' (' || sgr.subgrupo || ')' as subgrupo,
            coalesce((tab.descricao || ' (' || pdt.idtabelapreco || ')'), pdt.idtabelapreco, 'sem-tabela') as tabela,
            case tab.tipopreco
                when 'V' then 'Varejo'
                when 'A' then 'Atacado'
                when 'P' then 'Promocao'
                else 'Sem-tabela'
            end as Tipo_tabela,
            sum(
                case nat.tipoentrada
                    when 'D' then pdt.qtde * -1
                    else pdt.qtde
                end) as quantidade,
            sum(
                case nat.tipoentrada
                    when 'D' then (pdt.custofabrica * pdt.qtde) * -1
                    else (pdt.custofabrica * pdt.qtde)
                end) as custofabrica,
            sum(
                case nat.tipoentrada
                    when 'D' then (pdt.custoreposicao * pdt.qtde) * -1
                    else (pdt.custoreposicao * pdt.qtde)
                end) as custoreposicao,
            sum(
                case nat.tipoentrada
                    when 'D' then (pdt.custofinal * pdt.qtde) * -1
                    else (pdt.custofinal * pdt.qtde)
                end) as custofinal,
            sum(
                case nat.tipoentrada
                    when 'D' then pdt.vlrliquido * -1
                    else pdt.vlrliquido
                end) as valorliquido,
            sum(
                case nat.tipoentrada
                    when 'D' then pdt.frete * -1
                    else pdt.frete
                end) as frete,
            sum(
                case nat.tipoentrada
                    when 'D' then pdt.despesas * -1
                    else pdt.despesas
                end) as despesas,
            sum(
                case nat.tipoentrada
                    when 'D' then (pdt.vlrliquido + pdt.frete + pdt.despesas) * -1
                    else (pdt.vlrliquido + pdt.frete + pdt.despesas)
                end) as vlr_total
        from tvenpedido ped
        left outer join tvenproduto pdt on (pdt.empresa = ped.empresa and pdt.pedido = ped.codigo)
        left outer join testnatureza nat on (nat.codigo = ped.tipooperacao)
        left outer join tvenvendedor ven on (ven.empresa = ped.empresa and ven.codigo = ped.vendedor)
        left outer join tvenvendedor age on (age.empresa = ped.empresa and age.codigo = ped.agente)
        left outer join testprodutogeral pdg on (pdg.codigo = pdt.produto)
        left outer join testmarca mar on (mar.codigo = pdg.marca)
        left outer join testfabricante fab on (fab.codigo = pdg.fabricante)
        left outer join testproduto pro on (pro.empresa = pdt.empresa and pro.produto = pdt.produto)
        left outer join testgrupo grp on (grp.empresa = pro.empresa and grp.codigo = pro.grupo)
        left outer join testsubgrupo sgr on (sgr.empresa = pro.empresa and sgr.grupo = pro.grupo and sgr.subgrupo = pro.subgrupo)
        left outer join testsetor str on (str.empresa = pro.empresa and str.codigo = pro.setor)
        left outer join testtabelapreco tab on (tab.empresa = pdt.empresa and tab.idtabelapreco = pdt.idtabelapreco)
        left outer join trecclientegeral clg on (clg.codigo = ped.cliente)
        left outer join tgercidade cid on (cid.codigo = clg.cidade)
        left outer join trecregiao reg on (reg.gid = clg.gidregiao)
        left outer join trecatividade atv on (atv.codigo = clg.atividade)
        where ped.empresa = %s
        and nat.geraestatistica = 'S'
        and nat.gerafinanceiro = 'S'
        and nat.tiposaida <> 'T'
        and ped.status = 'EFE'
        and ped.dataefe between %s and %s
        and pdt.produto = %s
        and ped.cliente = %s
        group by 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26
    )
    select ven.*,
        case ven.custofabrica
            when 0 then 0
            else cast((ven.valorliquido / ven.custofabrica) as numeric(15, 2))
        end as markup_fabrica_x_vendas,
        case ven.custoreposicao
            when 0 then 0
            else cast((ven.valorliquido / ven.custoreposicao) as numeric(15, 2))
        end as markup_custoreposicao_x_vendas,
        case ven.custofinal
            when 0 then 0
            else cast((ven.valorliquido / ven.custofinal) as numeric(15, 2))
        end as markup_custofinal_x_vendas,
        coalesce(
            (select first 1 p.valoresespecificos
             from testtabelaprecoprodutos p
             where p.empresa = ven.empresa
             and p.produto = ven.cod_produto
             and p.valoresespecificos = 'S'
            ), 'N'
        ) as tem_Valor_Especifico
    from vendas ven
    """
    
    # Execute uma consulta para buscar dados
    cur.execute(query)  # Substitua "sua_tabela" pelo nome da sua tabela
    
    # Busque todos os resultados da consulta
    rows = cur.fetchall()
    
    # Obtenha os nomes das colunas
    col_names = [desc[0] for desc in cur.description]
    
    # Feche a conexão
    con.close()
    
    # Retorne os dados em um DataFrame do Pandas
    return pd.DataFrame(rows, columns=col_names)

# Título do aplicativo
st.title('Dados do Banco de Dados Firebird')

# Botão para carregar os dados
if st.button('Carregar Dados'):
    data = get_data_from_firebird()
    st.write(data)
