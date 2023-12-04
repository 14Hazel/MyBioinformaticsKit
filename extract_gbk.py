# -*- coding: utf-8 -*-
import sys,os
from Bio import GenBank
from Bio import SeqIO
import click
from loguru import logger

@click.command()
@click.option("-i","--input", required=True, help="输入待抽取序列的gbk文件")
@click.option("-o", "--output", default="./", help="输出文件路径")
def main(input:str, output:str):
    """
    输出locus_tag、protein_id、product、protein_product、翻译序列到faa文件中
    :param input:  输入待抽取序列的gbk文件
    :param output: 输出文件路径
    """
    with open(input, "r") as f, open(output, "a") as o:
        for seq_record in SeqIO.parse(f, "genbank") :
            logger.info("Dealing with GenBank record %s" % seq_record.id)
            for seq_feature in seq_record.features:
                if seq_feature.type == "CDS":
                    try: 
                        assert len(seq_feature.qualifiers['translation']) == 1
                        locus_tag = seq_feature.qualifiers['locus_tag'][0]
                        seq_name = seq_record.name
                        protein_id = seq_feature.qualifiers['protein_id'][0]
                        product = seq_feature.qualifiers['product'][0]
                        translation = seq_feature.qualifiers['translation'][0]
                        o.write(f">{locus_tag} from {seq_name} protein_id={protein_id} product={product}\n{translation}\n")

                    except KeyError as e:
                        logger.exception(f"KeyError: {e} in {seq_record.id}")


    logger.info("Done")

if __name__=='__main__':
  	main()
