# -*- coding: utf-8 -*-

from IPython.core.magic import register_cell_magic, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from SPARQLWrapper import SPARQLWrapper, JSON
from IPython.core.display import display_javascript, Javascript
from rdflib import URIRef, Literal
import pandas as pd



@register_cell_magic
@needs_local_scope
@magic_arguments()
@argument('endpoint', help='SPARQL endpoint')
@argument('--save', '-s', help='Save result into variable')
@argument('--quiet', '-q', action='store_true', help='Don\'t output anything')
@argument('--params', '-p', help='Use parameter dict in percentage-formatted variables')
def sparql(line, cell, local_ns=None):
    
    args = parse_argstring(sparql, line)
    sparql_endpoint = args.endpoint

    client = SPARQLWrapper(sparql_endpoint)
    client.setReturnFormat(JSON)
    if args.params:
        cell = cell % args.params
    client.setQuery(cell)
    results = client.query().convert()
    df = df_results(results)

    if args.save:
        local_ns[args.save] = df
    
    if not args.quiet:
        return df

def convert_node(obj):
    if obj['type'] == 'uri':
        return obj['value']
    if obj['type'] == 'typed-literal' or 'literal':
        if 'datatype' in obj:
            dt = URIRef(obj['datatype'])
            return Literal(obj['value'], datatype=dt).toPython()
        elif 'xsd:lang' in obj:
            lang = obj['xsd:lang']
            return Literal(obj['value'], lang=lang)
        else:
            return obj['value']
    
    raise Exception(f'Invalid RDF node type {obj["type"]}')


def df_results(result):

    if 'boolean' in result:
        vars = ['ASK']
        table = [[result['boolean']]]
    else:
        vars = result['head']['vars']
        table = []
        for data in result['results']['bindings']:
            row = []
            for var in vars:
                if var in data:
                    d = convert_node(data[var])
                else:
                    d = None
                row.append(d)
            table.append(row)

    return pd.DataFrame(table, columns=vars)

def load_ipython_extension(ipython):
    pass
