#!/opt/conda/envs/pCRACKER_p27/bin/python
# All rights reserved.
from collections import Counter, defaultdict, OrderedDict
import cPickle as pickle
import errno
from itertools import combinations, permutations
import itertools
import os
import shutil
import subprocess

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import click
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py
import pybedtools
from Bio import Phylo
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor, _DistanceMatrix
import hdbscan
import networkx as nx
from pybedtools import BedTool
from pyfaidx import Fasta
import scipy.sparse as sps
from scipy.stats import pearsonr, chi2_contingency
import seaborn as sns
from sklearn.cluster import MiniBatchKMeans
from sklearn.manifold import SpectralEmbedding
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import FeatureAgglomeration
from sklearn.decomposition import FactorAnalysis, LatentDirichletAllocation, NMF
from sklearn.decomposition import KernelPCA, TruncatedSVD
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import SpectralClustering
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
from sklearn.pipeline import Pipeline
from sklearn.metrics import *
from sklearn.metrics import calinski_harabaz_score, silhouette_score
# from evolutionary_search import maximize


RANDOM_STATE=42

CONTEXT_SETTINGS = dict(help_option_names=['-h','--help'], max_content_width=90)

@click.group(context_settings= CONTEXT_SETTINGS)
@click.version_option(version='1.1.3')
def polycracker():
    pass


def create_path(path):
    """Create a path if directory does not exist, raise exception for other errors"""
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


@polycracker.command(name='run_pipeline')
@click.option('-m','--memory', default = '47', help='Amount of memory to use on sge or slurm submission job, in Gigabytes.', show_default=True)
@click.option('-t','--time', default = '11', help='Number of hours to run sge or slurm submission job', show_default = True)
@click.option('-N','--nodes', default = '1', help='Number of nodes for slurm submission job', show_default = True)
@click.option('-b','--batch_script', default = 'runCluster.sh', help = 'Run custom batch script. Default will run the pipeline.', show_default = True)
@click.option('-J','--job_name', default = 'polyCRACKER', help = 'Custom name for job.', show_default=True)
@click.option('-n','--no_options', is_flag=True, help= 'Run slurm submission script with no options.')
@click.option('-a','--account_name', default='fungalp', help= 'Account name for running jobs.', show_default=True)
@click.option('-nh','--no_nohup', is_flag=True, help= 'No nohup for pipeline run.')
def run_pipeline(memory, time, nodes, batch_script, job_name, no_options, account_name, no_nohup):
    """Run polycracker pipeline."""
    subprocess.call('%ssh %s %s'%('nohup ' if not no_nohup else '', batch_script, '' if no_nohup else '&'),shell=True)
    submit_txt = 'nohup sh %s &\n'%batch_script
    run_files = [file for file in os.listdir('.') if file.startswith('submission_history.') and file.endswith('.txt')]
    with open('submission_history.%i.txt'%(len(run_files)),'w') as f:
        f.write(submit_txt + '\n'.join(['--memory '+memory, '--time '+time,'--nodes '+nodes,
                                        '--batch_script '+batch_script,'--job_name '+job_name, '--no_options '+str(no_options), '--account_name '+account_name]))


@polycracker.command(name='test_pipeline')
@click.option('-o', '--output_folder', default = 'test_results', help='folder where the output should be copied.', type=click.Path(exists=False))
@click.option('-m','--memory', default = '47', help='Amount of memory to use on sge or slurm submission job, in Gigabytes.', show_default=True)
@click.option('-t','--time', default = '11', help='Number of hours to run sge or slurm submission job', show_default = True)
@click.option('-N','--nodes', default = '1', help='Number of nodes for slurm submission job', show_default = True)
def test_pipeline(output_folder, memory, time, nodes):
    genome_path = os.path.join(output_folder, 'extracted_subgenomes')
    create_path(genome_path)
    plots_path = os.path.join(output_folder, 'plots')
    create_path(plots_path)
    stats_path = os.path.join(output_folder, 'test_statistics')
    create_path(stats_path)
    create_path('analysisOutputs')
    subprocess.call('scp test_data/config_polyCRACKER.txt .', shell=True)
    subprocess.call('polycracker run_pipeline -m %s -t %s -N %s -nh'%(memory, time, nodes), shell=True)
    # subprocess.call('python polycracker.py subgenomeExtraction -p ./test_data/test_fasta_files/ -s analysisOutputs/SpectralClusteringmain_tsne_2_n3/bootstrap_0/ -os analysisOutputs/SpectralClusteringmain_tsne_2_n3/ -g algae_split.fa -go algae_split.fa -l 26 -b 2 -kl 30 -dk 10 -kv 1 -u 8,2', shell=True)
    subprocess.call('polycracker final_stats -s -dict subgenome_0:Creinhardtii,subgenome_1:Csubellipsoidea -pbed analysisOutputs/SpectralClusteringmain_tsne_2_n3/clusterResults/', shell=True)
    subprocess.call('polycracker convert_subgenome_output_to_pickle -id analysisOutputs/SpectralClusteringmain_tsne_2_n3/clusterResults/ -s analysisOutputs/SpectralClusteringmain_tsne_2_n3/scaffolds_connect.p', shell=True)
    subprocess.call('scp analysisOutputs/SpectralClusteringmain_tsne_2_n3/bootstrap_0/model_subgenome_*.fa ./%s/extracted_subgenomes' % output_folder, shell=True)
    subprocess.call('scp polycracker.stats.analysis.csv ./%s/test_statistics' % output_folder, shell=True)
    subprocess.call('scp SpectralClusteringmain_tsne_2_n3ClusterTest.html ./%s/plots' % output_folder, shell=True)
    subprocess.call('polycracker number_repeatmers_per_subsequence && scp *.png ./%s/plots' % output_folder, shell=True)
    subprocess.call('polycracker plotPositions -npy analysisOutputs/SpectralClusteringmain_tsne_2_n3/graphInitialPositions.npy -p analysisOutputs/SpectralClusteringmain_tsne_2_n3/scaffolds_connect.p -o ./%s/plots/spectral_graph.html -npz analysisOutputs/SpectralClusteringmain_tsne_2_n3/spectralGraph.npz -l spectral' % output_folder, shell=True)
    click.echo('Please see results in ./%s.' % output_folder)
    click.echo('\nOriginal genome in ./test_data/test_fasta_files .\n')


@polycracker.command(name='splitFasta')
@click.option('-i', '--fasta_file', help='Input polyploid fasta filename.', type=click.Path(exists=False))
@click.option('-d', '--fasta_path', default='./fasta_files/', help='Directory containing polyploids fasta file', show_default=True, type=click.Path(exists=False))
@click.option('-c', '--chunk_size', default=75000, help='Length of chunk of split fasta file', show_default=True)
@click.option('-p', '--prefilter', default=0, help='Remove chunks based on certain conditions as a preprocessing step to reduce memory', show_default=True)
@click.option('-m', '--min_chunk_size', default=0, help='If min_chunk_threshold and prefilter flag is on, use chunks with lengths greater than a certain size', show_default=True)
@click.option('-r', '--remove_non_chunk', default=0, help='If min_chunk_threshold and prefilter flag is on, remove chunks that are not the same size as chunk_size', show_default=True)
@click.option('-t', '--min_chunk_threshold', default=0, help='If prefilter is on, remove chunks with lengths less than a certain threshold', show_default=True)
@click.option('-l', '--low_memory', default=0, help='Must use with prefilter in order for prefilter to work.', show_default=True)
def splitFasta(fasta_file, fasta_path, chunk_size, prefilter, min_chunk_size, remove_non_chunk, min_chunk_threshold, low_memory):
    """Split fasta file into chunks of a specified length"""
    global inputStr, key
    if not os.path.exists(fasta_path):
        raise OSError('Specified fasta_file directory does not exist')
    Fasta(fasta_path+fasta_file)
    faiFile = fasta_path+fasta_file + '.fai'
    def grabLine(positions):
        global inputStr
        global key
        if positions[-1] != 'end':
            return '%s\t%s\t%s\t%s\n'%tuple([key]+map(str,positions[0:2])+['_'.join([key]+map(str,positions[0:2]))])
        else:
            return '%s\t%s\t%s\t%s\n' % (key, str(positions[0]), str(inputStr), '_'.join([key, str(positions[0]), str(inputStr)]))
    def split(inputStr=0,width=60):
        if inputStr:
            positions = np.arange(0,inputStr,width)
            posFinal = []
            if inputStr > width:
                for i in range(len(positions[:-1])):
                    posFinal += [(positions[i],positions[i+1])]
            posFinal += [(positions[-1],'end')]
            splitLines = map(grabLine,posFinal)
            return splitLines
        else:
            return ''
    bedText = []
    for key, seqLength in [tuple(line.split('\t')[0:2]) for line in open(faiFile,'r') if line]:
        inputStr = int(seqLength)
        bedText += split(inputStr,chunk_size)
    with open('correspondence.bed','w') as f:
        f.write('\n'.join(bedText))
    corrBed = BedTool('correspondence.bed').sort()
    corrBed.saveas('correspondence.bed')
    corrBed.saveas('correspondenceOriginal.bed')
    if prefilter and low_memory:
        if remove_non_chunk:
            scaffolds = corrBed.filter(lambda x: len(x) == chunk_size)
            scaffolds.saveas('correspondence.bed')
            oldLines = corrBed.filter(lambda x: len(x) != chunk_size)
            oldLines.saveas('correspondence_filteredOut.bed')
            subprocess.call('bedtools getfasta -fi %s -fo %s -bed %s -name'%(fasta_path+fasta_file,fasta_path + 'filteredOut.fa','correspondence_filteredOut.bed'),shell=True)
        elif min_chunk_threshold:
            scaffolds = corrBed.filter(lambda x: len(x) >= min_chunk_size)
            scaffolds.saveas('correspondence.bed')
            oldLines = corrBed.filter(lambda x: len(x) < min_chunk_size)
            oldLines.saveas('correspondence_filteredOut.bed')
            subprocess.call('bedtools getfasta -fi %s -fo %s -bed %s -name'%(fasta_path+fasta_file,fasta_path + 'filteredOut.fa','correspondence_filteredOut.bed'),shell=True)
    subprocess.call('bedtools getfasta -fi %s -fo %s -bed %s -name'%(fasta_path+fasta_file,fasta_path+fasta_file.split('.fa')[0]+'_split.fa','correspondence.bed'),shell=True)
    Fasta((fasta_path+fasta_file).split('.fa')[0]+'_split.fa')


@polycracker.command(name='writeKmerCount')
@click.option('-d', '--fasta_path', default='./fasta_files/', help='Directory containing chunked polyploids fasta file', show_default=True, type=click.Path(exists=False))
@click.option('-k', '--kmercount_path', default='./kmercount_files', help='Directory containing kmer count files', show_default=True, type=click.Path(exists=False))
@click.option('-l', '--kmer_length', default='23,31', help='Length of kmers to find; can include multiple lengths if comma delimited (e.g. 23,25,27)', show_default=True)
@click.option('-m', '--blast_mem', default='100', help='Amount of memory to use for bbtools run. More memory will speed up processing.', show_default=True)
def writeKmerCount(fasta_path, kmercount_path, kmer_length, blast_mem):
    """Takes list of fasta files and runs kmercountexact.sh to find how many of each kmer of specified length is in genome"""
    kmer_lengths = kmer_length.split(',')
    blast_memStr = "export _JAVA_OPTIONS='-Xmx%sG'"%(blast_mem)
    print(blast_memStr)
    create_path(kmercount_path)
    for fastaFile in os.listdir(fasta_path):
        if (fastaFile.endswith('.fa') or fastaFile.endswith('.fasta')) and '_split' in fastaFile:
            kmerFiles = []
            f = fastaFile.rstrip()
            print f
            outFileNameFinal = f[:f.rfind('.')] + '.kcount'
            open(kmercount_path + '/' + outFileNameFinal, 'w').close()
            for kmerL in kmer_lengths:
                scriptName = f[:f.rfind('.')] + kmerL + '.sh'
                outFileName = f[:f.rfind('.')]+kmerL+'.kcount'
                kmerFiles.append(kmercount_path+'/'+outFileName)
                lineOutputList = [fasta_path, fastaFile, kmercount_path, outFileName, kmerL]
                if int(kmerL) <= 31:
                    bbtoolsI = open(scriptName, 'w')
                    bbtoolsI.write('#!/bin/bash\n'+blast_memStr+'\nkmercountexact.sh overwrite=true fastadump=f mincount=3 in=%s/%s out=%s/%s k=%s -Xmx%sg\n' %tuple(lineOutputList+[blast_mem]))
                    bbtoolsI.close()
                else:
                    with open(scriptName,'w') as f2:
                        f2.write('#!/bin/bash\njellyfish count -m %s -s %d -t 15 -C -o %s/mer_counts.jf %s/%s && jellyfish dump %s/mer_counts.jf -c > %s/%s'%(kmerL,os.stat(fasta_path+'/'+fastaFile).st_size,kmercount_path,fasta_path,fastaFile,kmercount_path,kmercount_path,outFileName))
                try:
                    subprocess.call('sh %s' % scriptName, shell=True)
                except:
                    print 'Unable to run %s via command line..' % outFileName
            subprocess.call('cat %s > %s'%(' '.join(kmerFiles), kmercount_path + '/' + outFileNameFinal), shell=True)
            subprocess.call('rm %s'%(' '.join(kmerFiles)), shell=True)


@polycracker.command(name='kmer2Fasta')
@click.option('-k', '--kmercount_path', default='./kmercount_files/', help='Directory containing kmer count files', show_default=True, type=click.Path(exists=False))
@click.option('-lc', '--kmer_low_count', default=100, help='Omit kmers from analysis that have less than x occurrences throughout genome.', show_default=True)
@click.option('-hb', '--high_bool', default=0, help='Enter 1 if you would like to use the kmer_high_count option.', show_default=True)
@click.option('-hc', '--kmer_high_count', default=2000000, help='If high_bool is set to one, omit kmers that have greater than x occurrences.', show_default=True)
@click.option('-s', '--sampling_sensitivity', default=1, help='If this option, x, is set greater than one, kmers are sampled at lower frequency, and total number of kmers included in the analysis is reduced to (total #)/(sampling_sensitivity), after threshold filtering', show_default=True)
def kmer2Fasta(kmercount_path, kmer_low_count, high_bool, kmer_high_count, sampling_sensitivity):
    """Converts kmer count file into a fasta file for blasting, after some threshold filtering and sampling"""
    if sampling_sensitivity < 1:
        sampling_sensitivity = 1
    count = 0
    for kmer in os.listdir(kmercount_path):
        if kmer.endswith('.kcount'):
            with open(kmercount_path+kmer,'r') as f, open(kmercount_path+kmer+'.fa','w') as f2:
                if high_bool:
                    for line in f:
                        lineList = line.split() # line.split('\t')
                        if line and int(lineList[-1]) >= kmer_low_count and int(lineList[-1]) <= kmer_high_count:
                            if count % sampling_sensitivity == 0:
                                f2.write('>%s\n%s\n'%tuple([lineList[0]]*2))
                            count += 1
                else:
                    for line in f:
                        if line and int(line.split()[-1]) >= kmer_low_count: # line.split('\t')
                            if count % sampling_sensitivity == 0:
                                f2.write('>%s\n%s\n'%tuple([line.split()[0]]*2)) # '\t'
                            count += 1


@polycracker.command(name='blast_kmers')
@click.option('-m', '--blast_mem', default='48', help='Amount of memory to use for bbtools run. More memory will speed up processing.', show_default=True)
@click.option('-r', '--reference_genome', help='Genome to blast against.', type=click.Path(exists=False))
@click.option('-k', '--kmer_fasta', help='Kmer fasta converted from kmer count file', type=click.Path(exists=False))
@click.option('-o', '--output_file', default = 'results.sam', show_default=True, help='Output sam file.', type=click.Path(exists=False))
@click.option('-kl', '--kmer_length', default=13, help='Kmer length for mapping.', show_default=True)
@click.option('-pm', '--perfect_mode', default = 1, help='Perfect mode.', show_default=True)
@click.option('-t', '--threads', default = 5, help='Threads to use.', show_default=True)
def blast_kmers(blast_mem, reference_genome, kmer_fasta, output_file, kmer_length, perfect_mode, threads):
    """Maps kmers fasta file to a reference genome."""
    blast_memStr = "export _JAVA_OPTIONS='-Xms5G -Xmx%sG'"%(blast_mem)
    subprocess.call('%s && bbmap.sh vslow=t ambiguous=all noheader=t secondary=t k=%d perfectmode=%s threads=%s maxsites=2000000000 outputunmapped=f ref=%s in=%s outm=%s -Xmx%sg'%(blast_memStr,kmer_length,'t' if perfect_mode else 'f', threads, reference_genome, kmer_fasta, output_file, blast_mem), shell=True)


@polycracker.command(name='blast2bed')
@click.option('-i', '--blast_file', default='./blast_files/results.sam', help='Output file after blasting kmers to genome. Must be input into this command.', show_default=True, type=click.Path(exists=False))
@click.option('-b', '--bb', default=1, help='Whether bbtools were used in generating blasted sam file.', show_default=True)
@click.option('-l', '--low_memory', default=0, help='Do not merge the bed file. Takes longer to process but uses lower memory.', show_default=True)
@click.option('-o', '--output_bed_file', default = 'blasted.bed', show_default=True, help='Output bed file, not merged.', type=click.Path(exists=False))
@click.option('-om', '--output_merged_bed_file', default = 'blasted_merged.bed', show_default=True, help='Output bed file, merged.', type=click.Path(exists=False))
@click.option('-ex', '--external_call', is_flag=True, help='External call from non-polyCRACKER pipeline.')
def blast2bed(blast_file, bb , low_memory, output_bed_file, output_merged_bed_file, external_call):
    """Converts the blast results from blast or bbtools into a bed file"""
    if external_call:
        subprocess.call("awk -v OFS='\\t' '{ print $3, 0, 100, $1 }' %s > %s"%(blast_file,output_bed_file),shell=True)
    else:
        if bb:
            with open(blast_file,'r') as f, open(output_bed_file,'w') as f2:
                for line in f:
                    if line:
                        l1 = line.split('\t')[2].split('::')[0]
                        f2.write('\t'.join([l1] + ['0', str(int(l1.split('_')[-1]) - int(l1.split('_')[-2]))] + [line.split('\t')[0]]) + '\n')
        else:
            with open(blast_file,'r') as f, open(output_bed_file,'w') as f2:
                for line in f:
                    if line:
                        l1 = line.split('\t')[1].split('::')[0]
                        f2.write('\t'.join([l1] + ['0',str(int(l1.split('_')[-1])-int(l1.split('_')[-2]))] + [line.split('\t')[0]])+'\n')
    if low_memory == 0:
        b = pybedtools.BedTool(output_bed_file).sort().merge(c=4,o='collapse')
        b.saveas(output_merged_bed_file)


def findScaffolds():
    with open('correspondence.bed','r') as f:
        lineList = sorted([line.split('\t')[-1].strip('\n') for line in f.readlines() if line])
    return lineList


def findKmerNames(kmercount_path, genome):
    for file in os.listdir(kmercount_path):
        if file.startswith(genome[:genome.find('.fa')]) and (file.endswith('.fa') or file.endswith('.fasta')):
            print file
            with open(kmercount_path + file,'r') as f:
                listKmer = sorted([line.strip('\n') for line in f.readlines()[1::2] if line])
            return listKmer


@polycracker.command(name='generate_Kmer_Matrix')
@click.option('-d', '--kmercount_path', default='./kmercount_files/', help='Directory containing kmer count files', type=click.Path(exists=False))
@click.option('-g', '--genome', help='File name of chunked genome fasta', type=click.Path(exists=False))
@click.option('-c', '--chunk_size', default=75000, help='Length of chunk of split/chunked fasta file', show_default=True)
@click.option('-mc', '--min_chunk_size', default=0, help='If min_chunk_threshold and prefilter flag is on, use chunks with lengths greater than a certain size', show_default=True)
@click.option('-r', '--remove_non_chunk', default=1, help='If min_chunk_threshold and prefilter flag is on, remove chunks that are not the same size as chunk_size', show_default=True)
@click.option('-t', '--min_chunk_threshold', default=0, help='If prefilter is on, remove chunks with lengths less than a certain threshold', show_default=True)
@click.option('-l', '--low_memory', default=0, help='Must use with prefilter in order for prefilter to work. Without prefilter, populates matrix using unmerged blasted bed (slow).', show_default=True)
@click.option('-p', '--prefilter', default=0, help='If selected, will now add chunks that were removed during preprocessing.', show_default=True)
@click.option('-f', '--fasta_path', default='./fasta_files/', help='Directory containing chunked polyploids fasta file', type=click.Path(exists=False))
@click.option('-gs', '--genome_split_name', help='File name of chunked genome fasta', type=click.Path(exists=False))
@click.option('-go', '--original_genome', help='File name of original, prechunked genome fasta', type=click.Path(exists=False))
@click.option('-i', '--input_bed_file', default = 'blasted.bed', show_default=True, help='Input bed file, not merged.', type=click.Path(exists=False))
@click.option('-im', '--input_merged_bed_file', default = 'blasted_merged.bed', show_default=True, help='Input bed file, merged.', type=click.Path(exists=False))
@click.option('-npz', '--output_sparse_matrix', default = 'clusteringMatrix.npz', show_default=True, help='Output sparse matrix file, in npz format.', type=click.Path(exists=False))
@click.option('-k', '--output_kmer_file', default = 'kmers.p', show_default=True, help='Output kmer pickle file.', type=click.Path(exists=False))
@click.option('-tf', '--tfidf', default=0, help='If set to one, no sequence length normalization will be done.', show_default=True)
def generate_Kmer_Matrix(kmercount_path, genome, chunk_size, min_chunk_size, remove_non_chunk, min_chunk_threshold, low_memory, prefilter, fasta_path, genome_split_name, original_genome, input_bed_file, input_merged_bed_file, output_sparse_matrix, output_kmer_file, tfidf):
    """From blasted bed file, where kmers were blasted to the polyploid genome, now generate a sparse matrix that contains information pertaining to the distribution of kmers (columns) for a given region of the genome (rows)"""
    if prefilter and low_memory:
        subprocess.call('bedtools getfasta -fi %s -fo %s -bed %s -name'%(fasta_path+original_genome,fasta_path+genome_split_name,'correspondenceOriginal.bed'),shell=True)
    kmers = findKmerNames(kmercount_path, genome)
    originalScaffolds = findScaffolds()
    if remove_non_chunk and prefilter == 0:
        scaffolds = list(filter(lambda scaffold: abs(int(scaffold.split('_')[-1]) - int(scaffold.split('_')[-2])) == chunk_size,originalScaffolds))
    elif min_chunk_threshold and prefilter == 0:
        scaffolds = list(filter(lambda scaffold: abs(int(scaffold.split('_')[-1]) - int(scaffold.split('_')[-2])) >= min_chunk_size,originalScaffolds))
    else:
        scaffolds = originalScaffolds
    scaffoldIdx = {scaffold:i for i,scaffold in enumerate(scaffolds)}
    kmerIdx = {kmer:i for i,kmer in enumerate(kmers)}
    data = sps.dok_matrix((len(scaffolds), len(kmers)),dtype=np.float32)
    scaffoldL = np.array([map(float, scaffold.split('_')[-2:]) for scaffold in scaffolds])
    scaffoldLengths = abs(scaffoldL[:, 1] - scaffoldL[:, 0]) / 5000.
    if low_memory:
        with open(input_bed_file, 'r') as f:
            for line in f:
                if line:
                    try:
                        lineL = line.strip('\n').split('\t')
                        data[scaffoldIdx[lineL[0]], kmerIdx[lineL[-1]]] += 1.
                    except:
                        pass
    else:
        with open(input_merged_bed_file, 'r') as f:
            for line in f:
                if line:
                    listLine = line.rstrip('\n').split('\t')
                    if listLine[0] in scaffolds:
                        counts = Counter(listLine[-1].split(','))
                        for key in counts:
                            try:
                                data[scaffoldIdx[listLine[0]], kmerIdx[key]] = counts[key]
                            except:
                                pass
    del scaffoldIdx, kmerIdx
    data = data.tocsc()
    # divide every row by scaffold length
    if not tfidf:
        for i in range(len(scaffoldLengths)):
            data[i, :] /= scaffoldLengths[i]
    sps.save_npz(output_sparse_matrix, data)
    with open('rowNames.txt', 'w') as f:
        f.write('\n'.join('\t'.join([str(i), scaffolds[i]]) for i in range(len(scaffolds))))
    with open('colNames.txt', 'w') as f:
        f.write('\n'.join('\t'.join([str(i), kmers[i]]) for i in range(len(kmers))))
    pickle.dump(scaffolds,open('scaffolds.p','wb'),protocol=2)
    pickle.dump(originalScaffolds, open('originalScaffolds.p', 'wb'), protocol=2)
    pickle.dump(kmers,open(output_kmer_file,'wb'),protocol=2)


@polycracker.command(name='transform_plot')
@click.option('-t', '--technique', default='kpca', help='Dimensionality reduction technique to use.', type=click.Choice(['kpca','factor','feature', 'lda', 'nmf', 'tsne']), show_default=True)
@click.option('-s', '--n_subgenomes', default = 2, help='Number of subgenomes', show_default=True)
@click.option('-m', '--metric', default='cosine', help='Kernel for KPCA if kpca technique is chosen. Cosine is particularly effective.', type=click.Choice(['linear','poly','rbf','sigmoid','cosine']), show_default=True)
@click.option('-d', '--n_dimensions', default=3, help='Number of dimensions to reduce to.', show_default=True)
@click.option('-tf', '--tfidf', default=0, help='If set to one, tfidf normalization will be used instead of standard scaling.', show_default=True)
def transform_plot(technique, n_subgenomes, metric, n_dimensions, tfidf):
    """Perform dimensionality reduction on a sparse matrix and plot the results."""
    if n_subgenomes < 2:
        n_subgenomes = 2
    if n_dimensions < 3:
        n_dimensions = 3
    peak = 'main'
    if os.path.exists(peak + '_' + technique + '_%d'%(n_subgenomes) + 'Reduction.html') == 0:
        data = sps.load_npz('clusteringMatrix.npz')
        scaffolds = pickle.load(open('scaffolds.p', 'rb'))
        N = n_dimensions
        dimensionalityReducers = {'kpca': KernelPCA(n_components=N,kernel=metric,random_state=RANDOM_STATE), 'factor': FactorAnalysis(n_components=N),
                                  'feature': FeatureAgglomeration(n_clusters=N), 'lda': LatentDirichletAllocation(n_topics=N), 'nmf': NMF(n_components=N)}
        if technique == 'tsne':
            from MulticoreTSNE import MulticoreTSNE as TSNE
            dimensionalityReducers.update({'tsne': TSNE(n_components=n_dimensions,n_jobs=6,metric=metric if metric == 'cosine' else 'euclidean',learning_rate=200,perplexity=30,angle=0.5,random_state=RANDOM_STATE)})
        if not tfidf:
            data = StandardScaler(with_mean=False).fit_transform(data)
        else:
            from sklearn.feature_extraction.text import TfidfTransformer
            data = TfidfTransformer().fit_transform(data)
        if technique not in 'kpca':
            data = KernelPCA(n_components=25,random_state=RANDOM_STATE).fit_transform(data)
        transformed_data = dimensionalityReducers[technique].fit_transform(data)
        np.save('%s_%s_%d_transformed3D.npy'%(peak,technique,n_subgenomes), transformed_data)
        if n_dimensions > 3:
            metric = 'linear'
            transformed_data = KernelPCA(n_components=3,kernel=metric,random_state=RANDOM_STATE).fit_transform(transformed_data)
        plots = []
        plots.append(
            go.Scatter3d(x=transformed_data[:, 0], y=transformed_data[:, 1], z=transformed_data[:, 2], name='Data',
                         mode='markers',
                         marker=dict(color='b', size=2), text=scaffolds))
        fig = go.Figure(data=plots)
        py.plot(fig, filename=peak + '_' + technique + '_%d'%(n_subgenomes) + 'Reduction.html', auto_open=False)
    else:
        subprocess.call('touch %s'%(peak + '_' + technique + '_%d'%(n_subgenomes) + 'Reduction.html'),shell=True)

@polycracker.command(name='reset_transform')
def reset_transform():
    """Remove all html files from main work directory. Must do this if hoping to retransform sparse data."""
    subprocess.call('rm *.html',shell=True)


# begin clustering
class GeneticHdbscan:

    def __init__(self,metric='euclidean',min_clusters=3,max_cluster_size=1000,max_samples=500,validity_measure='silhouette', generations_number=8, gene_mutation_prob=0.45, gene_crossover_prob = 0.45, population_size=50, interval=10, upper_bound=False, verbose=True):
        self.hdbscan_metric = (metric if metric not in ['ectd','cosine','mahalanobis'] else 'precomputed')
        self.min_clusters = min_clusters
        self.max_cluster_size = max_cluster_size
        self.max_samples = max_samples
        self.validity_measure = validity_measure
        self.generations_number = generations_number
        self.gene_mutation_prob = gene_mutation_prob
        self.gene_crossover_prob = gene_crossover_prob
        self.population_size = population_size
        self.scoring_method = lambda X, y: hdbscan.validity.validity_index(X,y,metric=self.hdbscan_metric) if self.validity_measure == 'hdbscan_validity' else (silhouette_score(X,y,metric='precomputed' if metric =='mahalanobis' else 'mahalanobis',V=(np.cov(X,rowvar=False) if metric != 'mahalanobis' else '')) if self.validity_measure == 'silhouette' else calinski_harabaz_score(X,y))
        self.low_counts = (2,2)
        self.interval = interval
        self.upper_bound = upper_bound
        self.verbosity = verbose

    def cluster_data(self, X, min_cluster_size, min_samples, cluster_selection_method):
        return hdbscan.HDBSCAN(min_cluster_size = min_cluster_size, min_samples= min_samples, cluster_selection_method= cluster_selection_method, metric = self.hdbscan_metric, alpha = 1.0).fit_predict(X)

    def return_cluster_score(self, X, min_cluster_size, min_samples, cluster_selection_method):
        labels = self.cluster_data(X, min_cluster_size, min_samples, cluster_selection_method) # , n_neighbors
        n_clusters = labels.max() + 1
        # print labels
        X = X if self.validity_measure == 'hdbscan_validity' else X[labels != -1,:]
        y = labels if self.validity_measure == 'hdbscan_validity' else labels[labels != -1]
        # print y
        if list(y):
            return self.scoring_method(X,y)/(((1. + (abs(n_clusters - self.min_clusters) if self.upper_bound else 0.)) if n_clusters >= self.min_clusters else float(self.min_clusters - n_clusters + 1))*(1.+len(labels[labels == -1])/float(len(labels))))
        else:
            return 0

    def fit(self, X):
        best_params, best_score, score_results, hist, log = maximize(self.return_cluster_score, dict(min_cluster_size = np.unique(np.linspace(self.low_counts[0],self.max_cluster_size,self.interval).astype(int)).tolist(), min_samples = np.unique(np.linspace(self.low_counts[1],self.max_samples, self.interval).astype(int)).tolist(), cluster_selection_method= ['eom'] ), dict(X=X), verbose=self.verbosity, n_jobs = 1, generations_number=self.generations_number, gene_mutation_prob=self.gene_mutation_prob, gene_crossover_prob = self.gene_crossover_prob, population_size = self.population_size) # fixme, 'leaf' # n_neighbors = np.unique(np.linspace(low_counts[2], n_neighbors, 10).astype(int)).tolist()),
        self.labels_ = self.cluster_data(X,min_cluster_size=best_params['min_cluster_size'], min_samples=best_params['min_samples'], cluster_selection_method= best_params['cluster_selection_method'])


@polycracker.command(name='find_best_cluster_parameters')
@click.pass_context
@click.option('-f', '--file', help='Numpy .npy file containing positions after dimensionality reduction')
@click.option('-y', '--y_true_pickle', default='colors_pickle.p', show_default=True, help='Pickle file containing ground truths.')
@click.option('-s', '--n_subgenomes', default = 3, help='Number of subgenomes', show_default=True)
@click.option('-g', '--generations_number', default=10, show_default=True, help='Number of generations.')
@click.option('-gm', '--gene_mutation_prob', default=0.45, show_default=True, help='Gene mutation probability.')
@click.option('-gc', '--gene_crossover_prob', default=0.45, show_default=True, help='Gene crossover probability.')
@click.option('-p', '--population_size', default=250, show_default=True, help='Population size.')
def find_best_cluster_parameters(ctx,file,y_true_pickle,n_subgenomes,generations_number, gene_mutation_prob, gene_crossover_prob, population_size):
    """In development: Experimenting with genetic algorithm (GA). Use GA to find best cluster method / hyperparameters given ground truth. These hyperparameter scans can help us find out what is important in finding good clusters rather than trial and error."""
    from sklearn.metrics import fowlkes_mallows_score#v_measure_score
    try:
        os.makedirs('cluster_tests/')
    except:
        pass
    y_true = pickle.load(open(y_true_pickle,'r'))
    cluster_function = lambda file, cluster_method, n_subgenomes, metric, n_neighbors, weighted_nn, grab_all, gamma, min_span_tree: ctx.invoke(cluster,file=file, cluster_method=cluster_method, n_subgenomes=n_subgenomes, metric=metric, n_neighbors=n_neighbors, weighted_nn=weighted_nn, grab_all=grab_all, gamma=gamma, min_span_tree=min_span_tree)
    subprocess.call('rm GA_scores.txt',shell=True)
    def cluster_scoring(file, cluster_method, n_subgenomes, metric, n_neighbors, weighted_nn, grab_all, gamma, min_span_tree):
        os.system('rm *.html &> /dev/null')
        try:
            y_pred = cluster_function(file, cluster_method, n_subgenomes, metric, n_neighbors, weighted_nn, grab_all, gamma, min_span_tree)
            os.system('mv *.html cluster_tests/ &> /dev/null')
            #print(y_true, y_pred)
            score = fowlkes_mallows_score(y_true,y_pred)#v_measure_score(y_true,y_pred)
            click.echo(str(dict(zip(['cluster_method', 'n_subgenomes', 'metric', 'n_neighbors', 'weighted_nn', 'grab_all', 'gamma', 'min_span_tree','score'],[cluster_method, n_subgenomes, metric, n_neighbors, weighted_nn, grab_all, gamma, min_span_tree,score]))))
            #f.write(str(dict(zip(['cluster_method', 'n_subgenomes', 'metric', 'n_neighbors', 'weighted_nn', 'grab_all', 'gamma', 'min_span_tree','score'],[cluster_method, n_subgenomes, metric, n_neighbors, weighted_nn, grab_all, gamma, min_span_tree,score]))) + '\n')
            return score
        except:
            #f.write(str(dict(zip(['cluster_method', 'n_subgenomes', 'metric', 'n_neighbors', 'weighted_nn', 'grab_all', 'gamma', 'min_span_tree','score'],[cluster_method, n_subgenomes, metric, n_neighbors, weighted_nn, grab_all, gamma, min_span_tree,0]))) + '\n')
            click.echo(str(dict(zip(['cluster_method', 'n_subgenomes', 'metric', 'n_neighbors', 'weighted_nn', 'grab_all', 'gamma', 'min_span_tree','score'],[cluster_method, n_subgenomes, metric, n_neighbors, weighted_nn, grab_all, gamma, min_span_tree,0]))))
            return 0
    best_params, best_score, score_results, hist, log = maximize(cluster_scoring,dict(cluster_method=['SpectralClustering','KMeans','GMM','BGMM','hdbscan_genetic'],
                                                                                      metric=['cityblock','cosine','euclidean','l1','l2','manhattan','braycurtis','canberra','chebyshev','correlation','dice','hamming','mahalanobis','matching','minkowski','rogerstanimoto','russellrao','jaccard','yule','sokalsneath'], #,'seuclidean','sokalmichener',,'sqeuclidean' ,'jaccard','kulsinski'
                                                                                      n_neighbors=range(3,100,20)),dict(file=file,n_subgenomes=n_subgenomes,min_span_tree=1,grab_all=1,weighted_nn=0,gamma=1),verbose=True, n_jobs = 1, generations_number=generations_number, gene_mutation_prob=gene_mutation_prob, gene_crossover_prob = gene_crossover_prob, population_size = population_size) #,weighted_nn = [0,1],grab_all=[0,1],gamma=np.logspace(-4,100,50),min_span_tree=[0,1]
    click.echo(str(best_params))
    with open('cluster_tests.txt','w') as f:
        f.write(str(best_params)+'\n\n'+str(score_results))


@polycracker.command(name='cluster')
@click.option('-f', '--file', help='Numpy .npy file containing positions after dimensionality reduction')#, type=click.Path(exists=False))
@click.option('-c', '--cluster_method', default='SpectralClustering', help='Clustering method to use.', type=click.Choice(['SpectralClustering','KMeans','GMM','BGMM','hdbscan_genetic']), show_default=True)
@click.option('-s', '--n_subgenomes', default = 2, help='Number of subgenomes', show_default=True)
@click.option('-m', '--metric', default='cosine', help='Distance metric used to compute affinity matrix, used to find nearest neighbors graph for spectral clustering.', type=click.Choice(['cityblock','cosine','euclidean','l1','l2','manhattan','braycurtis','canberra','chebyshev','correlation','dice','hamming','jaccard','kulsinski','mahalanobis','matching','minkowski','rogerstanimoto','russellrao','seuclidean','sokalmichener','sokalsneath','sqeuclidean','yule']), show_default=True)
@click.option('-nn', '--n_neighbors', default=10, help='Number of nearest neighbors in generation of nearest neighbor graph.', show_default=True)
@click.option('-wnn', '--weighted_nn', default=0, help='Whether to weight spectral graph for spectral clustering.', show_default=True)
@click.option('-all', '--grab_all', default=0, help='Whether to grab all clusters, and number of clusters would equal number of subgenomes. By default, the number of clusters is one greater than the number of subgenomes, and the algorithm attempts to get rid of the ambiguous cluster', show_default=True)
@click.option('-g','--gamma', default = 1.0, show_default=True, help='Gamma hyperparameter for Spectral Clustering and BGMM models.')
@click.option('-mst', '--min_span_tree', default = 0 , show_default=True, help='Augment k nearest neighbors graph with minimum spanning tree.')
def cluster(file, cluster_method, n_subgenomes, metric, n_neighbors, weighted_nn, grab_all, gamma, min_span_tree):
    """Perform clustering on the dimensionality reduced data, though various methods.
    Takes in npy position file and outputs clustered regions and plot.
    """
    if grab_all:
        n_clusters = n_subgenomes
    else:
        n_clusters = n_subgenomes + 1
    clustering_algorithms = {'SpectralClustering': SpectralClustering(n_clusters=n_clusters, eigen_solver='amg', affinity= 'precomputed', random_state=RANDOM_STATE),
                            'hdbscan_genetic':GeneticHdbscan(metric=metric,min_clusters=n_clusters,max_cluster_size=100,max_samples=50,validity_measure='silhouette', generations_number=10, gene_mutation_prob=0.45, gene_crossover_prob = 0.45, population_size=100 , interval=100, upper_bound = True),
                             'KMeans': MiniBatchKMeans(n_clusters=n_clusters),'GMM':GaussianMixture(n_components=n_clusters),'BGMM':BayesianGaussianMixture(n_components=n_clusters, weight_concentration_prior_type=('dirichlet_distribution' if weighted_nn else 'dirichlet_process'), weight_concentration_prior=(gamma if gamma != 1.0 else None))}
    n_clusters = n_subgenomes + 1
    name, algorithm = cluster_method , clustering_algorithms[cluster_method]
    dataOld = sps.load_npz('clusteringMatrix.npz')
    scaffolds = pickle.load(open('scaffolds.p', 'rb'))
    Tname = file.split('transformed3D')[0]
    transformed_data = np.load(file)
    n_dimensions = transformed_data.shape[1]
    transformed_data = StandardScaler().fit_transform(transformed_data)
    if os.path.exists(name + Tname + 'n%d' % n_clusters + 'ClusterTest.html') == 0:
        try:
            os.makedirs('analysisOutputs/' + name + Tname + 'n%d' % n_clusters)
        except:
            pass
        try:
            os.makedirs('analysisOutputs/' + name + Tname + 'n%d' % n_clusters+'/clusterResults')
        except:
            pass
        if cluster_method == 'SpectralClustering':
            neigh = NearestNeighbors(n_neighbors=n_neighbors, algorithm = 'brute', metric=metric)
            neigh.fit(transformed_data)
            fit_data = neigh.kneighbors_graph(transformed_data, mode = ('connectivity' if weighted_nn == 0 else 'distance'))
            if min_span_tree == 0:
                connected = sps.csgraph.connected_components(fit_data)
                if connected[0] > 1:
                    counts = Counter(connected[1])
                    subgraph_idx = max(counts.iteritems(), key=lambda x: x[1])[0]
                    scaffBool = connected[1] == subgraph_idx
                    dataOld = dataOld[scaffBool]
                    transformed_data = transformed_data[scaffBool,:]
                    scaffolds_noconnect = list(np.array(scaffolds)[scaffBool == False])
                    scaffolds = list(np.array(scaffolds)[scaffBool])
                    n_connected = connected[0]
                    while(n_connected > 1):
                        neigh = NearestNeighbors(n_neighbors=n_neighbors, algorithm='brute', metric=metric)
                        neigh.fit(transformed_data)
                        fit_data = neigh.kneighbors_graph(transformed_data, mode = ('connectivity' if weighted_nn == 0 else 'distance'))
                        connected = sps.csgraph.connected_components(fit_data)
                        counts = Counter(connected[1])
                        subgraph_idx = max(counts.iteritems(), key=lambda x: x[1])[0]
                        scaffBool = connected[1] == subgraph_idx
                        if connected[0] > 1:
                            dataOld = dataOld[scaffBool]
                            transformed_data = transformed_data[scaffBool, :]
                            scaffolds_noconnect += list(np.array(scaffolds)[scaffBool == False])
                            scaffolds = list(np.array(scaffolds)[scaffBool])
                            #print 'c',len(scaffolds), transformed_data.shape
                        n_connected = connected[0]
                else:
                    scaffolds_noconnect = []
            else:
                mst = sps.csgraph.minimum_spanning_tree(fit_data).tocsc() # fixme instead find MST of fully connected graph fitdata # pairwise_distances(transformed_data,metric=metric)
                #min_span_tree = (min_span_tree + min_span_tree.T > 0).astype(int)
                fit_data += mst
                fit_data += fit_data.T
                fit_data = (fit_data > 0).astype(np.float)
                #print fit_data.todense()
                #print sps.csgraph.connected_components(fit_data)

                # FIXME union between this and nearest neighbors check for memory issues, and change to transformed data
            if n_dimensions > 3:
                t_data = KernelPCA(n_components=3, random_state=RANDOM_STATE).fit_transform(transformed_data)
            else:
                t_data = transformed_data
            np.save('analysisOutputs/' + name + Tname + 'n%d' % n_clusters +'/graphInitialPositions.npy', t_data)
            del t_data
            sps.save_npz('analysisOutputs/' + name + Tname + 'n%d' % n_clusters +'/spectralGraph.npz', fit_data.tocsc())
            pickle.dump(scaffolds,open('analysisOutputs/' + name + Tname + 'n%d' % n_clusters + '/scaffolds_connect.p', 'wb'))
            if not min_span_tree:
                pickle.dump(scaffolds_noconnect,open('analysisOutputs/' + name + Tname + 'n%d' % n_clusters + '/scaffolds_noconnect.p', 'wb'))
        else:
            fit_data = pairwise_distances(transformed_data,metric=metric) if name == 'hdbscan_genetic' and metric in ['ectd','cosine','mahalanobis'] else transformed_data
        algorithm.fit(fit_data)
        if n_dimensions > 3:
            reduction = KernelPCA(n_components=3, random_state=RANDOM_STATE)
            reduction.fit(transformed_data)
            reductionT = reduction.transform(transformed_data)
            scaledfit = StandardScaler()
            scaledfit.fit(reductionT)
            transformed_data2 = scaledfit.transform(reductionT)
        else:
            transformed_data2 = transformed_data
        if hasattr(algorithm, 'labels_'):
            y_pred = algorithm.labels_.astype(np.int)
        else:
            y_pred = algorithm.predict(transformed_data)
        N = len(set(y_pred))
        c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, N)]
        plots = []
        clusterSize = defaultdict(list)
        #print y_pred
        for key in set(y_pred):
            cluster_scaffolds = np.array(scaffolds)[y_pred == key]
            #print key, y_pred[0:10], cluster_scaffolds[0:10], scaffolds[0:10]
            if list(cluster_scaffolds):
                clusterSize[key] = np.mean(np.apply_along_axis(lambda x: np.linalg.norm(x),1,transformed_data[y_pred == key,:]))
                if clusterSize[key] == min(clusterSize.values()):
                    testCluster = key
                plots.append(
                    go.Scatter3d(x=transformed_data2[y_pred == key, 0], y=transformed_data2[y_pred == key, 1],
                                 z=transformed_data2[y_pred == key, 2],
                                 name='Cluster %d, %d points, %f distance' % (key, len(cluster_scaffolds),clusterSize[key]), mode='markers',
                                 marker=dict(color=c[key], size=2), text=cluster_scaffolds))
            with open('analysisOutputs/' + name + Tname + 'n%d' % n_clusters + '/clusterResults/subgenome_%d.txt' % key, 'w') as f:
                f.write('\n'.join(np.array(scaffolds)[y_pred == key]))
        if hasattr(algorithm, 'cluster_centers_'):
            if n_dimensions > 3:
                centers = scaledfit.transform(reduction.transform(algorithm.cluster_centers_))
            else:
                centers = algorithm.cluster_centers_
            plots.append(
                go.Scatter3d(x=centers[:, 0], y=centers[:, 1], z=centers[:, 2], mode='markers',
                             marker=dict(color='purple', symbol='circle', size=12),
                             opacity=0.4,
                             name='Centroids'))
        try:
            os.makedirs('analysisOutputs/' + name + Tname + 'n%d' % n_clusters + '/bootstrap_0')
        except:
            pass
        if grab_all:
            for key in set(y_pred):
                with open('analysisOutputs/' + name + Tname + 'n%d' % n_clusters + '/bootstrap_0/subgenome_%d.txt' % key, 'w') as f:
                    f.write('\n'.join(np.array(scaffolds)[y_pred == key]))
        else:
            for key in set(y_pred)-{testCluster if name != 'hdbscan_genetic' else -1}:
                with open('analysisOutputs/' + name + Tname + 'n%d' % n_clusters + '/bootstrap_0/subgenome_%d.txt' % key, 'w') as f:
                    f.write('\n'.join(np.array(scaffolds)[y_pred == key]))
        fig = go.Figure(data=plots)
        subprocess.call('touch ' + 'analysisOutputs/' + name + Tname + 'n%d' % n_clusters + '.txt',
                        shell=True)
        py.plot(fig, filename=name + Tname + 'n%d' % n_clusters + 'ClusterTest.html', auto_open=False)
        return y_pred


@polycracker.command(name='reset_cluster')
def reset_cluster():
    """Delete cluster results, subgenome extraction results and corresponding html files."""
    subprocess.call('rm analysisOutputs/* *Test.html nohup.out -r',shell=True)


@polycracker.command(name='spectral_embed_plot')
@click.option('-npy', '--positions', help='Transformed data input, npy file.',type=click.Path(exists=False))
@click.pass_context
def spectral_embed_plot(ctx, positions):
    """Spectrally embed PCA data of any origin."""
    spectral = SpectralEmbedding(n_components=3, random_state=RANDOM_STATE)
    np.save('spectral_embed.npy',spectral.fit_transform(np.load(positions)))
    spectral = SpectralEmbedding(n_components=2, random_state=RANDOM_STATE)
    t_data = spectral.fit_transform(np.load(positions))
    plt.figure()
    plt.scatter(t_data[:,0],t_data[:,1],)
    plt.savefig('spectral_embed.png')
    ctx.invoke(plotPositions, positions_npy='spectral_embed.npy',colors_pickle='xxx',output_fname='spectral_embed.html')


# begining of subgenome extraction
def fai2bed(genome):
    """Convert polyploid fai to bed file"""
    Fasta(genome)
    bedFastaDict = defaultdict(list)
    with open(genome+'.fai','r') as f, open(genome + '.bed','w') as f2:
        for line in f:
            if line:
                lineList = line.split('\t')
                bedline = '%s\t%s\t%s\t%s\n'%(lineList[0],'0',lineList[1],lineList[0])
                f2.write(bedline)
                bedFastaDict[lineList[0]] = [bedline]
    return bedFastaDict


def writeKmerCountSubgenome(subgenomeFolder, kmer_length, blast_mem, diff_kmer_threshold, diff_sample_rate, default_kmercount_value):
    """Find kmer counts in each subgenome to find differential kmers in each subgenome and extract them"""
    blast_memStr = "export _JAVA_OPTIONS='-Xms5G -Xmx%sG'" % (blast_mem)
    kmer_lengths = kmer_length.split(',')
    try:
        os.makedirs(subgenomeFolder+'/kmercount_files/')
    except:
        pass
    kmercount_path = subgenomeFolder+'/kmercount_files/'
    for fastaFile in os.listdir(subgenomeFolder):
        if 'higher.kmers' not in fastaFile and '_split' not in fastaFile and (fastaFile.endswith('.fa') or fastaFile.endswith('.fasta')):
            kmerFiles = []
            f = fastaFile.rstrip()
            outFileNameFinal = f[:f.rfind('.')] + '.kcount'
            open(kmercount_path + '/' + outFileNameFinal, 'w').close()
            for kmerL in kmer_lengths:
                print f
                outFileName = f[:f.rfind('.')] + kmerL + '.kcount'
                kmerFiles.append(kmercount_path + '/' + outFileName)
                lineOutputList = [subgenomeFolder+'/', fastaFile, kmercount_path, outFileName,kmerL]
                if int(kmerL) <= 31:
                    subprocess.call(blast_memStr + ' && module load bbtools && kmercountexact.sh overwrite=true fastadump=f mincount=3 in=%s/%s out=%s/%s k=%s -Xmx%sg' % tuple(
                            lineOutputList+[blast_mem]),shell=True)
                else:
                    subprocess.call('jellyfish count -m %s -s %d -t 15 -C -o %s/mer_counts.jf %s/%s && jellyfish dump %s/mer_counts.jf -c > %s/%s'%(kmerL,os.stat(subgenomeFolder+'/'+fastaFile).st_size,kmercount_path,subgenomeFolder+'/',fastaFile,kmercount_path,kmercount_path,outFileName),shell=True)
            subprocess.call('cat %s > %s'%(' '.join(kmerFiles), kmercount_path + '/' + outFileNameFinal), shell=True)
            subprocess.call('rm %s'%(' '.join(kmerFiles)), shell=True)
    compareKmers(diff_kmer_threshold, kmercount_path,diff_sample_rate, default_kmercount_value)


def kmercounttodict(kmercount2fname,kmercount_path):
    """kmercounttodict function creates kmer : count key value pairs, takes path and file name of a kmer count file"""
    inputFile = open(kmercount_path+kmercount2fname,'r')
    print 'my input to kcount to dict is: %s' % inputFile
    dictConverted = {}
    for line in inputFile:
        if line and len(line.split()) == 2:
            lineList = line.split()
            dictConverted[lineList[0]]=(int(lineList[1].strip('\n')))
    inputFile.close()
    return dictConverted


def compareKmers(diff_kmer_threshold,kmercount_path,diff_sample_rate,default_kmercount_value):
    """Find differential kmers between subgenomes via found kmer counts and extract differential kmers"""
    ratio_threshold = diff_kmer_threshold
    if diff_sample_rate < 1:
        diff_sample_rate = 1
    dictOfGenes = {}
    kmercountFiles = [file for file in os.listdir(kmercount_path) if file.endswith('.kcount') and '_split' not in file]
    for file in kmercountFiles:
        # creates a dictionary that associates a species to its dictionary of the kmer : count key value pairs
        # kmercounttodict function is called to create the kmer : count key value pairs
        dictOfGenes[file[:file.rfind('.')]] = kmercounttodict(file,kmercount_path)
    # output kmers and counts for differential kmers
    # output file names
    outFileNames = defaultdict(list)
    for file in kmercountFiles:
        outFileNames[kmercount_path + "/%s.higher.kmers.fa" % (file.split('.')[0])] = dictOfGenes[file[:file.rfind('.')]]
    # {file.higherkmer : {kmer:count}}
    # create files for writing
    for filename in outFileNames:
        open(filename, 'w').close()
        print 'creating %s' % filename
    for outfilename, dict1 in outFileNames.iteritems():
        # check dict 1 against other dictionaries
        out1 = open(outfilename, 'w')
        # iterate through the keys of dict1 and identify kmers that are at least ratio_threshold fold higher in dict1
        if diff_sample_rate > 1:
            count = 0
            for key, value in dict1.iteritems():
                val1 = value
                values = []
                for outfilename2 in outFileNames:
                    if outfilename2 != outfilename:
                        values.append(outFileNames[outfilename2].get(key,default_kmercount_value))
                # require at least ratio_threshold fold higher kmers in dict1 fixme ADD chi-squared test to see if it differs from genome length differences between subgenomes
                if any([(val1 / val2) > ratio_threshold for val2 in values]):
                    if count % diff_sample_rate == 0:
                        out1.write('>%s.%d.%s\n%s\n' % (key, val1, '.'.join(map(str,values)), key))
                    count += 1
        else:
            for key, value in dict1.iteritems():
                val1 = value
                values = []
                for outfilename2 in outFileNames:
                    if outfilename2 != outfilename:
                        values.append(outFileNames[outfilename2].get(key,default_kmercount_value))
                # require at least ratio_threshold fold higher kmers in dict1
                if any([(val1 / val2) > ratio_threshold for val2 in values]):
                    out1.write('>%s.%d.%s\n%s\n' % (key, val1, '.'.join(map(lambda x: str(int(x)),values)), key))
        out1.close()


def writeBlast(genome, blastPath, kmercount_path, fasta_path, bb, blast_mem, search_length = 13, perfect_mode = 1):
    """Make blast database for whole genome assembly, blast differential kmers against subgenomes"""
    create_path(blastPath)
    genome_name = genome[:genome.rfind('.')]
    blast_memStr = "export _JAVA_OPTIONS='-Xms5G -Xmx%sG'" % (blast_mem)
    for file in [file2 for file2 in os.listdir(kmercount_path) if 'higher.kmers' in file2 and (file2.endswith('.fa') or file2.endswith('.fasta'))]:
        inputFile = kmercount_path+file
        f = file.rstrip()
        outFileName = f[:f.rfind('.')]+'.BLASTtsv.txt'
        lineOutputList = [genome_name, inputFile, blastPath, outFileName]
        if bb:
            subprocess.call(blast_memStr + ' && bbmap.sh vslow=t ambiguous=all noheader=t secondary=t threads=4 maxsites=2000000000 k=%d perfectmode=%s outputunmapped=f ref=%s in=%s path=%s/ outm=%s'%(search_length,'t' if perfect_mode else 'f',fasta_path+genome,inputFile,blastPath,blastPath+'/'+f[:f.rfind('.')]+'.sam'),shell=True)
        else:
            subprocess.call(blast_memStr + ' && module load blast+/2.6.0 && blastn -db ./%s.blast_db -query %s -task "blastn-short" -outfmt 6 -out %s/%s -num_threads 4 -evalue 1e-2' % tuple(lineOutputList),shell=True)


def blast2bed3(subgenomeFolder,blastPath, bedPath, sortPath, genome,bb, bedgraph=1, out_kmers = 0):
    """Takes a list of genotype files with only one column for pos and converts them to proper bedgraph format to be sorted"""
    create_path(bedPath)
    print 'blast files contains'
    blast_files = os.listdir(blastPath)
    print('\n'.join('{}: {}'.format(*k) for k in enumerate(blast_files)))
    if bb:
        endname = '.sam'
    else:
        endname = '.BLAST.tsv.txt'
    for blast_file in blast_files:
        if blast_file.endswith(endname):
            f = blast_file.rstrip()
            outFileName = f[:f.rfind('.')]+'.bed3'
            input_list = [blastPath, f]
            inpath = '%s/%s' % tuple(input_list)
            inputFile = open(inpath, 'r')
            outpath = os.path.join(bedPath, outFileName)
            bo = open(outpath, 'w')
            if bb:
                if out_kmers:
                    for line in inputFile:
                        lineInList = line.split()
                        lineOutputList = [lineInList[2],int(lineInList[3]),int(lineInList[3])+1,lineInList[0].split('.')[0]]
                        bo.write('%s\t%d\t%d\t%s\n' % tuple(lineOutputList))
                else:
                    for line in inputFile:
                        lineInList = line.split()
                        lineOutputList = [lineInList[2],int(lineInList[3]),int(lineInList[3])+1]
                        bo.write('%s\t%d\t%d\n' % tuple(lineOutputList))
                        """blast:ATATGTTGTAATATTTGAGCACT.322.13	Nt01_118425000_118500000	100.000	23	23	24631	24609	2.35e-04	46.1"""
                        """sam:ATATGTTGTAATATTTGAGCACT.322.13  16      Nt01_118425000_118500000        24609   3       23=     *       0       0       AGTGCTCAAATATTACAACATAT *       XT:A:R  NM:i:0  AM:i:3"""
            else:
                for line in inputFile:
                    lineInList = line.split()
                    lineOutputList = [lineInList[1], int(lineInList[8]), int(lineInList[8])+1]
                    bo.write('%s\t%d\t%d\n' % tuple(lineOutputList))
            inputFile.close()
            bo.close()
            if bedgraph:
                sortedName = f[:f.rfind('.')] + '.sorted.bed3'
                si = os.path.join(bedPath, outFileName)
                so = os.path.join(sortPath, sortedName)
                coveragename = subgenomeFolder + '/' + f[:f.rfind('.')] + '.sorted.cov'
                if not os.path.exists(sortPath):
                    os.makedirs(sortPath)
                b = BedTool(si)
                if not os.path.exists(genome.replace('.fai','')+'.bed'):
                    fai2bed(genome)
                shutil.copy(genome.replace('.fai','')+'.bed',subgenomeFolder)
                windows = '%s.bed' % genome
                a = BedTool(windows)
                b.sort().saveas(so)
                a.coverage(b).saveas(coveragename)
                bedgname = f[:f.rfind('.')] + '.sorted.cov.bedgraph'
                open(subgenomeFolder + '/' + bedgname, 'w').close()
                bedgo = open(subgenomeFolder + '/' + bedgname, 'w')
                covFile = open(coveragename, 'r')
                for line in covFile:
                    lineInList = line.split()
                    lineOutputList = [lineInList[0], int(lineInList[1]), int(lineInList[2]), int(lineInList[5]) ]
                    bedgo.write('%s\t%d\t%d\t%d\n' % tuple(lineOutputList))
                covFile.close()
                bedgo.close()


def bed2unionBed(genome, subgenomeFolder, bedPath):
    """Convert bedgraph files into union bedgraph files"""
    bedGraphFiles = [file for file in os.listdir(subgenomeFolder) if file.endswith('.sorted.cov.bedgraph')]
    inputName = 'subgenomes'
    outputFileName = subgenomeFolder + '/' +inputName + '.union.bedgraph'
    genome_name = genome[:genome.rfind('.')]
    subprocess.call('cut -f 1-2 %s.fai > %s.genome'%(genome,subgenomeFolder + '/genome'),shell=True)
    genomeFile = subgenomeFolder + '/genome.genome'
    bedGraphBedSortFn = [BedTool(subgenomeFolder+'/' + file).sort().fn for file in bedGraphFiles]
    x = BedTool()
    result = x.union_bedgraphs(i=bedGraphBedSortFn, g=genomeFile, empty=True)
    result.saveas(outputFileName)


@polycracker.command(name='kmerratio2scaffasta')
@click.pass_context
def kmerratio2scaffasta(ctx,subgenome_folder, original_subgenome_path, fasta_path, genome_name, original_genome, bb, bootstrap, iteration, kmer_length, run_final, original, blast_mem, kmer_low_count, diff_kmer_threshold, unionbed_threshold, diff_sample_rate, default_kmercount_value, search_length, perfect_mode):
    """Bin genome regions into corresponding subgenomes based on the kmer counts in each region and their corresponding subgenomes"""
    try:
        absolute_threshold, ratio_threshold = tuple(map(int,unionbed_threshold.split(',')))
    except:
        absolute_threshold, ratio_threshold = 10, 2
    if original:
        genome_name = original_genome
    genome = fasta_path + genome_name
    blast_memStr = "export _JAVA_OPTIONS='-Xms5G -Xmx%sG'" % (blast_mem)
    a = subgenome_folder + '/subgenomes.union.bedgraph'
    ubedg = open(a, 'r')
    genomeFastaObj = Fasta(genome)
    extractPath = subgenome_folder+'/extractedSubgenomes/'
    try:
        os.makedirs(extractPath)
    except:
        pass
    genomeprefix = genome[genome.rfind('/')+1:genome.rfind('.')]
    outputSubgenomes = [extractPath + genomeprefix + '.subgenome' + chr(i+65) + '.fasta' for i in range(len(ubedg.readline().split('\t')[3:]))]
    ubedg.seek(0)
    scaffoldsOut = [[] for subgenome in outputSubgenomes]
    ambiguousScaffolds = []
    # parse the unionbed file to subset
    for line in ubedg:
        if line:
            lineList = line.split('\t')
            scaff = str((lineList[0]).rstrip())
            ambiguous = 1
            x = [float((lineList[i]).rstrip()) for i in range(3,len(lineList))]
            for i in range(len(x)):
                x_others = x[:i] + x[i+1:]
                if all([(x_i == 0 and x[i] > absolute_threshold) or (x_i > 0 and (x[i]/x_i) > ratio_threshold) for x_i in x_others]):
                    scaffoldsOut[i].append(scaff)
                    ambiguous = 0
            if ambiguous:
                ambiguousScaffolds.append(scaff)
    no_kill = all([len(subgenome) > 0 for subgenome in scaffoldsOut])
    ubedg.close()
    for subgenome, scaffolds in zip(outputSubgenomes,scaffoldsOut):
        with open(subgenome,'w') as f:
            for scaff in scaffolds:
                f.write('>%s\n%s\n' % (scaff, str(genomeFastaObj[scaff][:])))
        subprocess.call(blast_memStr + ' && reformat.sh in=%s out=%s fastawrap=60'%(subgenome,subgenome.replace('.fasta','_wrapped.fasta')),shell=True)
    with open(extractPath+'ambiguousScaffolds.fasta','w') as f:
        for scaff in ambiguousScaffolds:
            f.write('>%s\n%s\n' % (scaff, str(genomeFastaObj[scaff][:])))
    subprocess.call(blast_memStr + ' && reformat.sh in=%s out=%s fastawrap=60' % (extractPath+'ambiguousScaffolds.fasta', extractPath+'ambiguousScaffolds_wrapped.fasta'), shell=True)
    if subgenome_folder.endswith('/'):
        subgenome_folder = subgenome_folder[:subgenome_folder.rfind('/')]
    if iteration < bootstrap:
        print 'NOT FINAL ITERATION'
        subgenome_folder = subgenome_folder[:subgenome_folder.rfind('/')] + '/bootstrap_%d' % (iteration + 1)
        try:
            os.makedirs(subgenome_folder)
        except:
            pass
        for i, scaffolds in enumerate(scaffoldsOut):
            if scaffolds:
                with open(subgenome_folder + '/subgenome_%d.txt'%i,'w') as f:
                    f.write('\n'.join(scaffolds))
    elif iteration == bootstrap:
        print 'FINAL ITERATION'
        iteration += 1
        try:
            os.makedirs(original_subgenome_path + '/finalResults')
        except:
            pass
        for i, scaffolds in enumerate(scaffoldsOut):
            if scaffolds:
                with open(original_subgenome_path + '/finalResults/subgenome_%d.txt' % i, 'w') as f:
                    f.write('\n'.join(scaffolds))
        run_final = 1
    if no_kill == 0:
        print 'DEAD'
        return
    if run_final == 0:
        iteration += 1
        print 'ITERATION'
        ctx.invoke(subgenomeExtraction, subgenome_folder=subgenome_folder, original_subgenome_path=original_subgenome_path, fasta_path=fasta_path, genome_name=genome_name, original_genome=original_genome, bb=bb, bootstrap=bootstrap, iteration=iteration, kmer_length=kmer_length, run_final=run_final, original=original, blast_mem=blast_mem, kmer_low_count=kmer_low_count, diff_kmer_threshold=diff_kmer_threshold, unionbed_threshold=unionbed_threshold, diff_sample_rate=diff_sample_rate, default_kmercount_value=default_kmercount_value, search_length = search_length, perfect_mode = perfect_mode)
    else:
        print 'DONE'
        return
# FIXME add hyperparameter scan using GA here!


@polycracker.command(name='subgenomeExtraction')
@click.option('-s', '--subgenome_folder', help='Subgenome folder where subgenome extraction is taking place. This should be the bootstrap_0 folder.', type=click.Path(exists=False))
@click.option('-os', '--original_subgenome_path', help='One level up from subgenomeFolder. Final outputs are stored here.', type=click.Path(exists=False))
@click.option('-p', '--fasta_path', default='./fasta_files/', help='Directory containing chunked polyploids fasta file', show_default=True, type=click.Path(exists=False))
@click.option('-g', '--genome_name', help='Filename of chunked polyploid fasta.', type=click.Path(exists=False))
@click.option('-go', '--original_genome', help='Filename of polyploid fasta; can be either original or chunked, just make sure original is set to 1 if using original genome.', type=click.Path(exists=False))
@click.option('-bb', '--bb', default=1, help='Whether bbtools were used in generating blasted sam file.', show_default=True)
@click.option('-b', '--bootstrap', default=0, help='Number of times to bootstrap the subgenome extraction process. Each time you bootstrap, you should get better classification results, else instability has occurred due to ambiguous clustering.', show_default=True)
@click.option('-i', '--iteration', default=0, help='Current iteration of bootstrapping process. Please set to 0, when initially beginning.', show_default=True)
@click.option('-l', '--kmer_length', default='23,31', help='Length of kmers to find; can include multiple lengths if comma delimited (e.g. 23,25,27)', show_default=True)
@click.option('-r', '--run_final', default=0, help='Turn this to 0 when starting the command. Script terminates if this is set to 1.', show_default=True)
@click.option('-o', '--original', default=0, help='Select 1 if trying to extract subgenomes based on original nonchunked genome.', show_default=True)
@click.option('-m', '--blast_mem', default='100', help='Amount of memory to use for bbtools run. More memory will speed up processing.', show_default=True)
@click.option('-kl', '--kmer_low_count', default=100, help='Omit kmers from analysis that have less than x occurrences throughout genome.', show_default=True)
@click.option('-dk', '--diff_kmer_threshold', default=20, help='Value indicates that if the counts of a particular kmer in a subgenome divided by any of the counts in other subgenomes are greater than this value, then the kmer is differential.', show_default=True)
@click.option('-u', '--unionbed_threshold', default='10,2', help='Two comma delimited values used for binning regions into subgenomes. First value indicates that if the counts of all kmers in a particular region in any other subgenomes are 0, then the total count in a subgenome must be more than this much be binned as that subgenome. Second value indicates that if any of the other subgenome kmer counts for all kmers in a region are greater than 0, then the counts on this subgenome divided by any of the other counts must surpass a value to be binned as that subgenome.', show_default=True)
@click.option('-ds', '--diff_sample_rate', default=1, help='If this option, x, is set greater than one, differential kmers are sampled at lower frequency, and total number of differential kmers included in the analysis is reduced to (total #)/(diff_sample_rate), after threshold filtering', show_default=True)
@click.option('-kv', '--default_kmercount_value', default = 3., help='If a particular kmer is not found in a kmercount dictionary, this number, x, will be used in its place. Useful for calculating differential kmers.', show_default = True)
@click.option('-sl', '--search_length', default=13, help='Kmer length for mapping.', show_default=True)
@click.option('-pm', '--perfect_mode', default = 1, help='Perfect mode.', show_default=True)
@click.pass_context
def subgenomeExtraction(ctx, subgenome_folder, original_subgenome_path, fasta_path, genome_name, original_genome, bb, bootstrap, iteration, kmer_length, run_final, original, blast_mem, kmer_low_count, diff_kmer_threshold, unionbed_threshold, diff_sample_rate, default_kmercount_value, search_length, perfect_mode):
    """Extract subgenomes from genome, either chunked genome or original genome can be fed in as argument"""
    if not fasta_path.endswith('/'):
        fasta_path += '/'
    bedDict = fai2bed(fasta_path+genome_name)
    blastPath = subgenome_folder + '/blast_files/'
    bedPath = subgenome_folder + '/bed_files/'
    sortPath = subgenome_folder + '/sortedbed_files/'
    create_path(blastPath)
    create_path(bedPath)
    create_path(sortPath)
    if bootstrap >= iteration or run_final == 1:
        for file in os.listdir(subgenome_folder):
            if file and file.endswith('.txt') and os.stat(subgenome_folder+'/'+file).st_size:
                with open(subgenome_folder+'/'+file,'r') as f,open(subgenome_folder+'/'+file.replace('.txt','.bed'),'w') as f2:
                    for line in f:
                        if line:
                            f2.write(bedDict[line.strip('\n')][0])
                subprocess.call('bedtools getfasta -fi %s -fo %s -bed %s -name'%(fasta_path+genome_name,subgenome_folder + '/%s_'%('model')+file.replace('.txt','.fa'),subgenome_folder+'/'+file.replace('.txt','.bed')),shell=True)
        writeKmerCountSubgenome(subgenome_folder,kmer_length,blast_mem,diff_kmer_threshold,diff_sample_rate, default_kmercount_value)
        writeBlast(original_genome,blastPath,subgenome_folder+'/kmercount_files/',fasta_path,bb,blast_mem, search_length, perfect_mode)
        blast2bed3(subgenome_folder, blastPath, bedPath, sortPath, fasta_path+original_genome, bb)
        bed2unionBed(fasta_path+original_genome, subgenome_folder, bedPath)
        ctx.invoke(kmerratio2scaffasta, subgenome_folder=subgenome_folder, original_subgenome_path=original_subgenome_path, fasta_path=fasta_path, genome_name=genome_name, original_genome=original_genome, bb=bb, bootstrap=bootstrap, iteration=iteration, kmer_length=kmer_length, run_final=run_final, original=original, blast_mem=blast_mem, kmer_low_count=kmer_low_count, diff_kmer_threshold=diff_kmer_threshold, unionbed_threshold=unionbed_threshold, diff_sample_rate=diff_sample_rate, default_kmercount_value=default_kmercount_value, search_length = search_length, perfect_mode = perfect_mode)
    if bootstrap < iteration and run_final == 0:
        subgenome_folder = original_subgenome_path
        subgenome_folder, run_final = 'null', 0
        iteration += 1
        if run_final:
            ctx.invoke(subgenomeExtraction, subgenome_folder=subgenome_folder, original_subgenome_path=original_subgenome_path, fasta_path=fasta_path, genome_name=genome_name, original_genome=original_genome, bb=bb, bootstrap=bootstrap, iteration=iteration, kmer_length=kmer_length, run_final=run_final, original=original, blast_mem=blast_mem, kmer_low_count=kmer_low_count, diff_kmer_threshold=diff_kmer_threshold, unionbed_threshold=unionbed_threshold, diff_sample_rate=diff_sample_rate, default_kmercount_value=default_kmercount_value, search_length = search_length, perfect_mode = perfect_mode)


@polycracker.command(name='cluster_exchange')
@click.option('-s', '--subgenome_folder', help='Subgenome folder where subgenome extraction is taking place. Parent of the bootstrap_0 folder.', type=click.Path(exists=False))
@click.option('-l', '--list_of_clusters', help='Comma delimited list of numbers corresponding to cluster names. E.g. 0,1,2 corresponds to subgenome_0,subgenome_1, and subgenome_2, and those would be extracted.', type=click.Path(exists=False))
def cluster_exchange(subgenome_folder,list_of_clusters):
    """Prior to subgenome Extraction, can choose to switch out clusters, change clusters under examination, judging from clustered PCA plot if incorrect ambiguous cluster was found."""
    print 'Make sure to delete other bootstrap folders other than bootstrap_0 and also finalResults.'
    subprocess.call('rm %s/finalResults %s %s/bootstrap_0/* -r ; scp %s %s/bootstrap_0'%(subgenome_folder,' '.join([subgenome_folder+'/'+folder for folder in os.listdir(subgenome_folder) if folder.startswith('bootstrap') and folder.endswith('0')==0]),subgenome_folder,' '.join([subgenome_folder+'/clusterResults/subgenome_%s.txt'%i for i in list_of_clusters.split(',')]),subgenome_folder),shell=True)


@polycracker.command(name='txt2fasta')
@click.option('-txt', '--txt_files', default='subgenome_1.txt,subgenome_2.txt', show_default=True, help='Comma delimited list of text files or folder containing text files.', type=click.Path(exists=False))
@click.option('-rf', '--reference_fasta', help='Full path to reference fasta file containing scaffold names.', type=click.Path(exists=False))
def txt2fasta(txt_files,reference_fasta):
    """Extract subgenome fastas from reference fasta file using polyCRACKER found text files of subgenome binned scaffolds."""
    if '.txt' in txt_files:
        txt_files = txt_files.split(',')
    else:
        txt_files = [txt_files+'/'+f for f in os.listdir(txt_files) if f.endswith('.txt')]
    for txt_file in txt_files:
        subprocess.call('export _JAVA_OPTIONS="-Xmx5g" && filterbyname.sh overwrite=t in=%s out=%s names=%s include=t'%(reference_fasta,txt_file.replace('.txt','.fa'),txt_file),shell=True)


@polycracker.command(name='clusterGraph')
@click.option('-sp', '--sparse_matrix_file', default='spectralGraph.npz', help='Sparse nearest neighbors graph npz file.', show_default=True, type=click.Path(exists=False))
@click.option('-sf', '--scaffolds_file', default='scaffolds_connect.p', help='Pickle file containing scaffold/chunk names.', show_default=True, type=click.Path(exists=False))
@click.option('-od', '--out_dir', default = './', help='Directory to output final plots.', show_default=True, type=click.Path(exists=False))
@click.option('-l', '--layout', default='standard', help='Layout from which to plot graph.', type=click.Choice(['standard','spectral','random']), show_default=True)
@click.option('-p', '--positions_npy', default='graphInitialPositions.npy', help='If standard layout, then use these data points to begin simulation.', show_default=True, type=click.Path(exists=False))
@click.option('-i', '--iteration', default='0,1,2,3', help='Can comma delimit the number of iterations you would like to simulate to. No comma for a single cycle.', show_default=True)
@click.option('-b', '--bed_features_file', default='xxx', help='Optional bed file in relation to nonchunked genome. Must include features in fourth column.', show_default=True, type=click.Path(exists=False))
def clusterGraph(sparse_matrix_file, scaffolds_file, out_dir, layout, positions_npy, iteration, bed_features_file):
    """Plots nearest neighbors graph in html format and runs a physics simulation on the graph over a number of iterations."""
    if bed_features_file.endswith('.bed') == 1:
        featureMap = 1
    else:
        featureMap = 0
    G = nx.from_scipy_sparse_matrix(sps.load_npz(sparse_matrix_file))
    scaffolds = pickle.load(open(scaffolds_file, 'rb'))
    N = 2
    c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, N + 1)]
    mapping = {i:scaffolds[i] for i in range(len(scaffolds))}
    G=nx.relabel_nodes(G,mapping, copy=False)
    nodes = G.nodes()
    if featureMap:
        scaffoldsDict = {scaffold : '\t'.join(['_'.join(scaffold.split('_')[0:-2])]+scaffold.split('_')[-2:]) for scaffold in scaffolds}
        outputFeatures = defaultdict(list)
        scaffoldsBed = BedTool('\n'.join(scaffoldsDict.values()),from_string=True)
        featureBed = BedTool(bed_features_file)
        featuresDict = {scaffold: '' for scaffold in scaffolds}
        finalBed = scaffoldsBed.intersect(featureBed,wa=True,wb=True).sort().merge(d=-1,c=7,o='distinct')
        finalBed.saveas(out_dir+'/finalBed.bed')
        omittedRegions = scaffoldsBed.intersect(featureBed,v=True,wa=True)
        omittedRegions.saveas(out_dir+'/ommitted.bed')
        for line in str(finalBed).splitlines()+[line2+'\tunlabelled' for line2 in str(omittedRegions).splitlines()]:
            lineList = line.strip('\n').split('\t')
            feature = lineList[-1]
            scaffold = '_'.join(lineList[0:-1])
            if ',' in feature:
                featuresDict[scaffold] = '|'.join(feature.split(','))
                feature = 'ambiguous'
            else:
                featuresDict[scaffold] = feature
            outputFeatures[scaffold] = feature
        mainFeatures = set(outputFeatures.values())
        N = len(mainFeatures)
        c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, N + 1)]
        featuresColors = {feature : c[i] for i, feature in enumerate(mainFeatures)}
        outputFeaturesArray = np.array([outputFeatures[scaffold] for scaffold in nodes])
        names = np.vectorize(lambda name: 'Scaffolds: ' + name)(outputFeaturesArray)
        colors = np.vectorize(lambda feature: featuresColors[feature])(outputFeaturesArray)
        nodesText = np.array(['%s, %d connections, feature= %s' % (scaffold, int(G.degree(scaffold)),featuresDict[scaffold]) for scaffold in nodes])
    else:
        names = 'Scaffolds'
        colors = c[0]
        nodesText = ['%s, %d connections, ' % (scaffold, int(G.degree(scaffold))) for scaffold in nodes]
    if layout == 'spectral':
        pos_i = nx.spectral_layout(G,dim=3)
    elif layout == 'random':
        pos_i = nx.random_layout(G, dim=3)
    else:
        pos_i = defaultdict(list)
        t_data = np.load(positions_npy)
        for i in range(len(scaffolds)):
            pos_i[scaffolds[i]] = tuple(t_data[i,:])
    try:
        iterations = sorted(map(int,iteration.split(',')))
    except:
        quit()
    masterData = []
    for idx,i in enumerate(iterations):
        if i != 0:
            pos = nx.spring_layout(G,dim=3,iterations=i,pos=pos_i)
        else:
            pos = pos_i
        plots = []
        Xv = np.array([pos[k][0] for k in nodes])
        Yv = np.array([pos[k][1] for k in nodes])
        Zv = np.array([pos[k][2] for k in nodes])
        Xed = []
        Yed = []
        Zed = []
        for edge in G.edges():
            Xed += [pos[edge[0]][0], pos[edge[1]][0], None]
            Yed += [pos[edge[0]][1], pos[edge[1]][1], None]
            Zed += [pos[edge[0]][2], pos[edge[1]][2], None]
        if featureMap:
            for name in mainFeatures:
                plots.append(go.Scatter3d(x=Xv[outputFeaturesArray == name],
                                      y=Yv[outputFeaturesArray == name],
                                      z=Zv[outputFeaturesArray == name],
                                      mode='markers',
                                      name= name,
                                      marker=go.Marker(symbol='dot',
                                                       size=5,
                                                       color=featuresColors[name],
                                                       line=go.Line(color='rgb(50,50,50)', width=0.5)
                                                       ),
                                      text=nodesText[outputFeaturesArray == name],
                                      hoverinfo='text'
                                      ))
        else:
            plots.append(go.Scatter3d(x=Xv,
                                      y=Yv,
                                      z=Zv,
                                      mode='markers',
                                      name=names,
                                      marker=go.Marker(symbol='dot',
                                                       size=5,
                                                       color=colors,
                                                       line=go.Line(color='rgb(50,50,50)', width=0.5)
                                                       ),
                                      text=nodesText,
                                      hoverinfo='text'
                                      ))
        plots.append(go.Scatter3d(x=Xed,
                                  y=Yed,
                                  z=Zed,
                                  mode='lines',
                                  line=go.Line(color='rgb(210,210,210)', width=1),
                                  hoverinfo='none'
                                  ))
        if idx == 0:
            sliders_dict = {
                'active': 0,
                'yanchor': 'top',
                'xanchor': 'left',
                'currentvalue': {
                    'font': {'size': 20},
                    'prefix': 'Frame:',
                    'visible': True,
                    'xanchor': 'right'
                },
                'transition': {'duration': 300, 'easing': 'cubic-in-out'},
                'pad': {'b': 10, 't': 50},
                'len': 0.9,
                'x': 0.1,
                'y': 0,
                'steps': []
            }
        slider_step = {'args': [
            [str(i)],
            {'frame': {'duration': 300, 'redraw': False},
             'mode': 'immediate',
             'transition': {'duration': 300}}
            ],
            'label': str(i),
            'method': 'animate'}
        sliders_dict['steps'].append(slider_step)
        masterData.append({'data' : go.Data(plots),'name' : str(i)})
    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )
    masterLayout = dict(
        title="Graph of Scaffolds",
        updatemenus=[{'direction': 'left',
                      'pad': {'r': 10, 't': 87},
                      'showactive': False,
                      'type': 'buttons',
                      'x': 0.1,
                      'xanchor': 'right',
                      'y': 0,
                      'yanchor': 'top', 'buttons': [
                {
                    'args': [None, {'frame': {'duration': 500, 'redraw': False},
                                    'fromcurrent': True,
                                    'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                                      'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ]}],
        sliders=[sliders_dict],
        width=1000,
        height=1000,
        showlegend=True,
        scene=go.Scene(
            xaxis=go.XAxis(axis),
            yaxis=go.YAxis(axis),
            zaxis=go.ZAxis(axis),
        ),
        margin=go.Margin(
            t=100
        ),
        hovermode='closest',
        annotations=go.Annotations([
            go.Annotation(
                showarrow=False,
                text="",
                xref='paper',
                yref='paper',
                x=0,
                y=0.1,
                xanchor='left',
                yanchor='bottom',
                font=go.Font(
                    size=14
                )
            )
        ]), )
    fig1 = go.Figure(data=masterData[0]['data'], layout=masterLayout, frames=masterData)
    py.plot(fig1, filename=out_dir + '/OutputGraph_frames_%s.html'%(','.join(map(str,iterations))), auto_open=False)


@polycracker.command(name='plotPositions')
@click.option('-npy', '--positions_npy', default='graphInitialPositions.npy', help='If standard layout, then use these data points to begin simulation.', show_default=True, type=click.Path(exists=False))
@click.option('-p', '--labels_pickle', default='scaffolds.p', help='Pickle file containing scaffolds.', show_default=True, type=click.Path(exists=False))
@click.option('-c', '--colors_pickle', default='colors_pickle.p', help='Pickle file containing the cluster/class each label/scaffold belongs to.', show_default=True, type=click.Path(exists=False))
@click.option('-o', '--output_fname', default = 'output.html', help='Desired output plot name in html.', show_default=True, type=click.Path(exists=False))
@click.option('-npz', '--graph_file', default='xxx', help='Sparse nearest neighbors graph npz file. If desired, try spectralGraph.npz.', type=click.Path(exists=False))
@click.option('-l', '--layout', default='standard', help='Layout from which to plot graph.', type=click.Choice(['standard','spectral','random']), show_default=True)
@click.option('-i', '--iterations', default=0, help='Number of iterations you would like to simulate to. No comma delimit, will only output a single iteration.', show_default=True)
@click.option('-s', '--graph_sampling_speed', default=1, help='When exporting the graph edges to CSV, can choose to decrease the number of edges for pdf report generation.', show_default=True)
@click.option('-ax','--axes_off', is_flag=True, help='When enabled, exports graph without the axes.')
@click.option('-cmap', '--new_colors', default='', show_default=True, help='Comma delimited list of colors if you want control over coloring scheme.')
def plotPositions(positions_npy, labels_pickle, colors_pickle, output_fname, graph_file, layout, iterations, graph_sampling_speed, axes_off, new_colors):
    """Another plotting function without emphasis on plotting the spectral graph. Emphasis is on plotting positions and clusters."""
    labels = pickle.load(open(labels_pickle,'rb'))
    if graph_file.endswith('.npz'):
        graph = 1
        G = nx.from_scipy_sparse_matrix(sps.load_npz(graph_file))
        mapping = {i:labels[i] for i in range(len(labels))}
        G=nx.relabel_nodes(G,mapping, copy=False)
        if layout == 'spectral':
            pos = nx.spring_layout(G,dim=3,iterations=iterations,pos=nx.spectral_layout(G,dim=3))
        elif layout == 'random':
            pos = nx.random_layout(G, dim=3)
        else:
            t_data = np.load(positions_npy)
            n_dimensions = t_data.shape[1]
            if n_dimensions > 3:
                t_data = KernelPCA(n_components=3).fit_transform(t_data)
            pos = nx.spring_layout(G,dim=3,iterations=iterations,pos={labels[i]: tuple(t_data[i,:]) for i in range(len(labels))})
        # NOTE that G.nodes() will cause the scaffolds to be plotted out of order, so must use labels
        transformed_data = np.array([tuple(pos[k]) for k in labels])#G.nodes()
        Xed = []
        Yed = []
        Zed = []
        for edge in G.edges():
            Xed += [pos[edge[0]][0], pos[edge[1]][0], None]
            Yed += [pos[edge[0]][1], pos[edge[1]][1], None]
            Zed += [pos[edge[0]][2], pos[edge[1]][2], None]
        if graph_sampling_speed > 1:
            Xed2, Yed2, Zed2 = [], [], []
            for edge in G.edges()[::graph_sampling_speed]:
                Xed2 += [pos[edge[0]][0], pos[edge[1]][0], None]
                Yed2 += [pos[edge[0]][1], pos[edge[1]][1], None]
                Zed2 += [pos[edge[0]][2], pos[edge[1]][2], None]
        else:
            Xed2, Yed2, Zed2 = Xed, Yed, Zed
        pd.DataFrame(np.vstack((Xed2,Yed2,Zed2)).T,columns=['x','y','z']).to_csv(output_fname.replace('.html','_graph_connections.csv'),index=False)
        del Xed2, Yed2, Zed2
    else:
        transformed_data = np.load(positions_npy)
        n_dimensions = transformed_data.shape[1]
        if n_dimensions > 3:
            transformed_data = KernelPCA(n_components=3).fit_transform(transformed_data)
        graph = 0
    if output_fname.endswith('.html') == 0:
        output_fname += '.html'
    if colors_pickle.endswith('.p'):
        names = pickle.load(open(colors_pickle,'rb'))
        print names
        c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, len(set(names)) + 2)]
        if new_colors:
            c=new_colors.split(',')
        color = {name: c[i] for i,name in enumerate(sorted(set(names)))}
        print color
        df = pd.DataFrame(data={'x':transformed_data[:,0],'y':transformed_data[:,1],'z':transformed_data[:,2],'text':np.array(labels),'names':names})
        df['color'] = df['names'].map(color)# LabelEncoder().fit_transform(df['names'])
        plots = []
        """for name,col in color.items():
            print name
            plots.append(
                go.Scatter3d(x=transformed_data[names == name,0], y=transformed_data[names == name,1],
                             z=transformed_data[names == name,2],
                             name=name, mode='markers',
                             marker=dict(color=col, size=2), text=np.array(labels)[names == name]))"""
        print(color.items())
        for name,col in color.items():#enumerate(df['names'].unique()):
            plots.append(
                go.Scatter3d(x=df['x'][df['names']==name], y=df['y'][df['names']==name],
                             z=df['z'][df['names']==name],
                             name=name, mode='markers',
                             marker=dict(color=col, size=2), text=df['text'][df['names']==name]))
    else:
        N = 2
        c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, N + 1)]
        plots = []
        plots.append(
            go.Scatter3d(x=transformed_data[:,0], y=transformed_data[:,1],
                         z=transformed_data[:,2],
                         name='Scaffolds', mode='markers',
                         marker=dict(color=c[0], size=2), text=labels))
    if graph:
        plots.append(go.Scatter3d(x=Xed,
                                  y=Yed,
                                  z=Zed,
                                  mode='lines',
                                  line=go.Line(color='rgb(210,210,210)', width=1),
                                  hoverinfo='none'
                                  ))
    if axes_off:
        fig = go.Figure(data=plots,layout=go.Layout(scene=dict(xaxis=dict(title='',autorange=True,showgrid=False,zeroline=False,showline=False,ticks='',showticklabels=False),
            yaxis=dict(title='',autorange=True,showgrid=False,zeroline=False,showline=False,ticks='',showticklabels=False),
            zaxis=dict(title='',autorange=True,showgrid=False,zeroline=False,showline=False,ticks='',showticklabels=False))))
    else:
        fig = go.Figure(data=plots)
    py.plot(fig, filename=output_fname, auto_open=False)
    try:
        pd.DataFrame(np.hstack((transformed_data,names[:,None])),columns=['x','y','z','Name']).to_csv(output_fname.replace('.html','.csv'))
    except:
        pass


@polycracker.command(name="number_repeatmers_per_subsequence")
@click.option('-m', '--merged_bed', default='blasted_merged.bed', help='Merged bed file containing bed subsequences and kmers, comma delimited.', show_default=True, type=click.Path(exists=False))
@click.option('-o', '--out_file', default='kmers_per_subsequence.png', help='Output histogram in png or pdf.', show_default=True, type=click.Path(exists=False))
@click.option('--kde', is_flag=True, help='Add kernel density estimation.')
def number_repeatmers_per_subsequence(merged_bed, out_file, kde):
    """Find histogram depicting number of repeat kmers per subsequence. If find tail close to zero, good choice to enfore a minimum chunk size for inclusion into kmer count matrix or change size of chunked genome fragments.
    Useful for assessing average repeat content across genome fragments. If too low, see README for recommendations."""
    plt.style.use('ggplot')
    kcount = np.genfromtxt(os.popen("awk '{print gsub(/,/,\"\")+1}' %s"%(merged_bed),'r'))
    plt.figure()
    kde_plot = sns.distplot(kcount, kde=kde)
    plt.title('Histogram of Repeat-mers in Chunked Genome Fragment')
    plt.xlabel(('Number of Repeat-mers in Chunked Genome Fragment'))
    plt.ylabel('Frequency/Density')
    if out_file.endswith('.png') == 0:
        out_file += '.png'
    plt.savefig(out_file,dpi=300)


@polycracker.command(name='kcount_hist_old')
@click.option('-k', '--kcount_file', help='Input kmer count file.', type=click.Path(exists=False))
@click.option('-o', '--out_file', default='kmer_histogram.png', help='Output histogram in png or pdf.', show_default=True, type=click.Path(exists=False))
@click.option('--log', is_flag=True, help='Scale x-axis to log base 10.')
def kcount_hist_old(kcount_file, out_file, log):
    """Outputs a histogram plot of a given kmer count file."""
    import seaborn as sns
    histValues = []
    with open(kcount_file,'r') as f:
        if log:
            for line in f:
                if line:
                    try:
                        histValues.append(np.log(int(line.strip('\n').split()[-1]))) #'\t'
                    except:
                        print line
        else:
            for line in f:
                if line:
                    try:
                        histValues.append(int(line.strip('\n').split()[-1])) #'\t'
                    except:
                        print line
    histValues = np.array(histValues)
    plt.figure()
    kde_plot = sns.distplot(histValues, kde=False)
    plt.title('KmerCount Histogram')
    plt.xlabel(('Total Kmer Counts in Genome in log(b10)x' if log else 'Total Kmer Counts in Genome'))
    plt.ylabel('Frequency/Density')
    if out_file.endswith('.png') == 0:
        out_file += '.png'
    plt.savefig(fname=out_file,dpi=300)


@polycracker.command(name='kcount_hist')
@click.option('-k', '--kcount_directory', help='Directory containing input kmer count files. Rename the kcount files to [insert-kmer-length].kcount, eg. 31.kcount . ln -s ... may be useful in this case.', type=click.Path(exists=False))
@click.option('-o', '--out_file', default='kmer_histogram.png', help='Output histogram in png.', show_default=True, type=click.Path(exists=False))
@click.option('--log', is_flag=True, help='Scale x-axis to log base 10.')
@click.option('-r','--kcount_range', default='3,10000', help='Comma delimited list of two items, specifying range of kmer counts.', show_default=True)
@click.option('-l','--low_count', default= 0., help='Input the kmer low count threshold and it will be plotted.', show_default = True)
@click.option('-kl','--kmer_lengths', default='', help='Optional: comma delimited list of kmer lengths to include in analysis. Eg. 31,54,73. Can optionally input the kmer low count corresponding to each length via another comma delimited list after colon, eg. Eg. 31,54,73:100,70,50 , where 100,70,50 are the low count thresholds')
@click.option('-s','--sample_speed', default=1, help='Optional: increase sample speed to attempt to smooth kmer count histogram. A greater sample speed will help with smoothing more but sacrifice more information.', show_default=True)
def kcount_hist(kcount_directory, out_file, log, kcount_range, low_count, kmer_lengths, sample_speed):
    """Outputs a histogram plot of a given kmer count files."""
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')
    from scipy.signal import savgol_filter as smooth
    from scipy.interpolate import interp1d
    fig, ax = plt.subplots(figsize=(7, 7), sharex=True)
    krange = map(int,kcount_range.split(','))
    if kmer_lengths:
        kl_flag = 1
        kmer_lengths_input = kmer_lengths
        print kmer_lengths_input
        print kmer_lengths_input.split(':')[1]
        kmer_lengths = map(int,kmer_lengths.split(':')[0].split(','))
        try:
            kmer_low_counts = {kmer_lengths[i]: low_count for i,low_count in enumerate(map(int,kmer_lengths_input.split(':')[1].split(',')))}
        except:
            kmer_low_counts = 0
        print kmer_low_counts
    else:
        kl_flag = 0
        kmer_lengths = range(500)
    for file in sorted(os.listdir(kcount_directory),reverse=True):
        if file.endswith('.kcount') and (kl_flag == 0 or (kl_flag == 1 and int(file.split('.')[0]) in kmer_lengths)):
            kcount_file = kcount_directory + '/' + file
            """
            histValues = []
            with open(kcount_file,'r') as f:
                if log:
                    for line in f:
                        if line:
                            try:
                                histValues.append(np.log(int(line.strip('\n').split()[-1]))) #'\t'
                            except:
                                print line
                else:
                    for line in f:
                        if line:
                            try:
                                histValues.append(int(line.strip('\n').split()[-1])) #'\t'
                            except:
                                print line"""
            histValues = np.array(os.popen("awk '{print $2}' %s"%kcount_file).read().splitlines())
            histValues = histValues[np.where(histValues)].astype(np.int)
            if log:
                histValues = np.vectorize(lambda x: np.log(x))(histValues)
            #histValues = np.array(histValues)
            #histValues = histValues[np.where((histValues >= krange[0]) & (histValues <= krange[1]))]
            histValues = OrderedDict(sorted(Counter(histValues).items()))
            if sample_speed == 1:
                x = histValues.keys()
                y = smooth(histValues.values(),5,3)
            else:
                x = histValues.keys()[::abs(sample_speed)]
                y = smooth(histValues.values()[::abs(sample_speed)],5,3)
            f = interp1d(x,y,kind='cubic', fill_value='extrapolate')
            xnew = np.arange(krange[0],krange[1]+0.5,.01)
            plt.plot(xnew, f(xnew), label='kmer length = %s'%file.split('.')[0], hold=None)
            if kmer_low_counts:
                plt.plot(kmer_low_counts[int(file.split('.')[0])],f(kmer_low_counts[int(file.split('.')[0])]),'^',label='Kmer-Count Cutoff Value = %d'%kmer_low_counts[int(file.split('.')[0])],hold=None)
            #kde_plot = sns.distplot(histValues, hist=False, label='kmer count = %s'%file.split('.')[0], ax=ax)
    if low_count:
        plt.axvline(x=low_count,label='Kmer-Count Cutoff Value = %d'%low_count, color='xkcd:dark green')
    plt.title('KmerCount Histogram')
    plt.xlabel(('Total Kmer Counts in Genome in log(b10)x' if log else 'Total Kmer Counts in Genome'))
    plt.ylabel('Frequency')
    plt.legend()
    #if out_file.endswith('.png') == 0:
    #    out_file += '.png'
    plt.savefig(out_file,dpi=300)


@polycracker.command(name='plot_unionbed')
@click.option('-u', '--unionbed_file', help='Unionbed input file from subgenomeExtraction process or from other intermediate analyses.', type=click.Path(exists=False))
@click.option('-n', '--number_chromosomes', default=10, help='Output plots of x largest chromosomes.', show_default=True)
@click.option('-od', '--out_folder', default='./', help='Output directory for plots.', show_default=True, type=click.Path(exists=False))
def plot_unionbed(unionbed_file, number_chromosomes, out_folder): # note, cannot plot union bed file when original is set
    """Plot results of union bed file, the distribution of total differential kmer counts for each extracted subgenome as a function across the entire genome. Note that results cannot be plot if original is set to one."""
    scaffolds = defaultdict(list)
    scaffolds_size = defaultdict(list)
    scaffold_info = []
    with open(unionbed_file,'r') as f:
        for line in f:
            lineList = line.split()
            lineList2 = lineList[0].split('_')
            scaffold = '_'.join(lineList2[0:-2])
            plot_values = [np.mean(map(int,lineList2[-2:]))]+map(int,lineList[3:])
            scaffolds[scaffold].append(tuple(plot_values))
            scaffold_info.append([scaffold]+map(int,lineList2[-2:])+map(int,lineList[3:]))
    for scaffold in scaffolds:
        scaffolds[scaffold] = np.array(scaffolds[scaffold])
        scaffolds[scaffold] = scaffolds[scaffold][scaffolds[scaffold][:,0].argsort()]
        scaffolds_size[int(np.max(scaffolds[scaffold][:,0]))] = scaffold
    scaffold_info = pd.DataFrame(scaffold_info,columns=(['chr','start','end']+['subgenome%d'%i for i in range(1,np.shape(scaffolds[scaffolds.keys()[0]])[1])]))
    scaffold_info.to_csv(unionbed_file.split('/')[-1].replace('.bedgraph','.diffkmer.csv'),index=False)
    for sc in sorted(scaffolds_size.keys())[::-1][0:number_chromosomes+1]:
        scaffold = scaffolds_size[sc]
        x = scaffolds[scaffold][:,0]
        plt.figure()
        for i in range(1,np.shape(scaffolds[scaffold])[1]):
            plt.plot(x,scaffolds[scaffold][:,i],label='Subgenome %d differential kmer totals'%i)
        plt.legend()
        plt.title(scaffold)
        plt.savefig(out_folder+'/'+scaffold+'.png')
    # FIXME add function to plot bootstraps change over time, from one bootstrap to next label propagation

######################################################################################################

###################################### CIRCOS PLOTTING ANALYSES ######################################


@polycracker.command(name='generate_karyotype')
@click.option('-go', '--original_genome', default='', show_default=True, help='Filename of polyploid fasta; must be full path to original.', type=click.Path(exists=False))
@click.option('--shiny', is_flag=True, help='Export to ShinyCircos.')
def generate_karyotype(original_genome, shiny):
    """Generate karyotype shinyCircos/omicCircos csv file."""
    subprocess.call('samtools faidx '+original_genome,shell = True)
    genome_info = []
    with open(original_genome+'.fai') as f:
        if shiny:
            for line in f:
                LL = line.split()[0:2]
                genome_info.append([LL[0],1,LL[1]])
        else:
            for line in f:
                LL = line.split()[0:2]
                genome_info.append([LL[0],0,LL[1]])
    genome_info = pd.DataFrame(np.array(genome_info),columns=['chrom','chromStart','chromEnd'])
    genome_info.to_csv('genome.csv',index=False)


@polycracker.command(name='shiny2omic')
@click.option('-csv', '--input_csv', default='', show_default=True, help='Filename of shinyCircos csv.', type=click.Path(exists=False))
def shiny2omic(input_csv):
    """Convert shinyCircos csv input files to omicCircos csv input files."""
    df = pd.read_csv(input_csv)
    df['start'] = (df['start']+df['end'])/2
    df.drop(columns=['end'])
    df.rename(columns = {'start':'pos'}, inplace = True)
    df.to_csv(input_csv.replace('.csv','.omicCircos.csv'),index=False)


@polycracker.command(name='out_bed_to_circos_csv')
@click.option('-b', '--output_bed', default = 'subgenomes.bed', show_default=-True, help = 'Output bed to convert into csv file for OmnicCircos plotting.', type=click.Path(exists=False))
@click.option('-fai', '--fai_file', help='Full path to original, nonchunked fai file.', type=click.Path(exists=False))
def out_bed_to_circos_csv(output_bed,fai_file):
    """Take progenitor mapped, species ground truth, or polyCRACKER labelled scaffolds in bed file and convert for shinyCircos input of classification tracks.."""
    outname = output_bed.replace('.bed','.csv')
    final_info = []
    with open(fai_file,'r') as f:
        faiBed = BedTool('\n'.join(['\t'.join([line.split()[0]]+['0',line.split()[1]]) for line in f.read().splitlines()]),from_string=True)
    ambiguous_regions = faiBed.subtract(BedTool(output_bed))
    for line in str(ambiguous_regions).splitlines():
        if line:
            lineList = line.split()
            final_info.append([lineList[0]]+map(int,lineList[1:3])+ [0])
    with open(output_bed,'r') as f:
        d = {subgenome: i+1 for i, subgenome in enumerate(set([line.split()[-1] for line in f.read().splitlines()]))}
        f.seek(0)
        for line in f.read().splitlines():
            if line:
                lineList = line.split()
                final_info.append([lineList[0]]+ map(int,lineList[1:3])+[d[lineList[-1]]])
    final_info = pd.DataFrame(np.array(final_info),columns=['chr', 'start', 'end', 'classifiedSubgenome'])
    final_info.to_csv(outname,index=False)


@polycracker.command(name='get_density')
@click.option('-gff', '--gff_file', default = '', help='Input gff file.',show_default=True)
@click.option('-w','--window_length', default = 75000, help= 'Window length for histogram of gene density.' ,show_default=True)
@click.option('-fai', '--fai_file', help='Full path to original, nonchunked fai file.', type=click.Path(exists=False))
@click.option('-fout', '--outputfname', default='gene_density.csv', help='Output csv file name.', show_default=True, type=click.Path(exists=False))
def get_density(gff_file,window_length,fai_file, outputfname):
    """Return gene or repeat density information in csv file from an input gff file. For shinyCircos."""
    subprocess.call('cut -f 1-2 %s > %s.genome'%(fai_file, 'genome'),shell=True)
    subprocess.call('bedtools makewindows -g genome.genome -w %d > windows.bed'%window_length,shell=True)
    subprocess.call('bedtools coverage -a windows.bed -b %s > coverage.bed'%(gff_file),shell=True)
    density_info = []
    with open('coverage.bed','r') as f:
        for line in f:
            if line and line.startswith('all') == 0:
                lineList = line.split()
                density_info.append([lineList[0]]+map(int,lineList[1:3])+[float(lineList[-1])])
    density_info = pd.DataFrame(density_info,columns=['chr','start','end','density'])
    density_info.to_csv(outputfname,index=False)


@polycracker.command(name='link2color')
@click.option('-csv', '--link_csv', help='Full path to link csv file.', type=click.Path(exists=False))
def link2color(link_csv):
    """Add color information to link file for shinyCircos."""
    outfname = link_csv.replace('.csv','.color.csv')
    df = pd.read_csv(link_csv)
    chrom2color = {chrom : chr(i+97) for i, chrom in enumerate(set(df['seg1'].as_matrix().tolist()))}
    df['color'] = np.vectorize(lambda x: chrom2color[x])(df['seg1'])
    df.to_csv(outfname,index=False)


@polycracker.command(name='multicol2multifiles')
@click.option('-csv', '--multi_column_csv', help='Full path to multi-column csv file, likely containing list of differential kmer counts.', type=click.Path(exists=False))
def multicol2multifiles(multi_column_csv):
    """Take matrix of total differential kmer counts, or similar matrix and break them up into single column files by found genome. For shinyCircos usage."""
    df = pd.read_csv(multi_column_csv)
    df_col = list(df.columns.values)
    for col in df_col[3:]:
        df[df_col[0:3]+[col]].to_csv(multi_column_csv.replace('.csv','.%s.csv'%col.strip(' ')),index=False)


@polycracker.command(name='count_repetitive')
@click.option('-fi', '--fasta_in', help='Fasta input file.', type=click.Path(exists=False))
def count_repetitive(fasta_in):
    """Infer percent of repetitive sequence in softmasked assembly"""
    import re
    f = Fasta(fasta_in)
    all_sequence = reduce(lambda x,y: x+y,map(lambda k: str(f[k][:]),f.keys())) # .replace('N','')
    lower_letters = len(re.findall(r'[a-z]',all_sequence))
    print(len(all_sequence),lower_letters,float(lower_letters)/len(all_sequence))


@polycracker.command(name='extract_sequences')
@click.option('-s', '--sequences_dict', default='S:S1,S2,S3-D:D1,D3,D10', show_default=True, help='Dictionary of sequences and which subgenome/genome to send them to.', type=click.Path(exists=False))
@click.option('-fi', '--fasta_in', help='Fasta input file.', type=click.Path(exists=False))
def extract_sequences(sequences_dict,fasta_in):
    """Extract sequences from fasta file and move them to new files as specified."""
    sequences_dict = {fasta_in[:fasta_in.rfind('.')]+'_%s'%genome_new+fasta_in[fasta_in.rfind('.'):]:sequences.split(',') for genome_new,sequences in [tuple(mapping.split(':')) for mapping in sequences_dict.split('-')]}
    for genome_new in sequences_dict:
        subprocess.call('samtools faidx %s %s > %s'%(fasta_in,' '.join(sequences_dict[genome_new]),genome_new),shell=True)


@polycracker.command(name='align')
@click.pass_context
@click.option('-f1', '--fasta1', default='', show_default=True, help="Input fasta one. Comma delimit and set fasta2 to '' to build alignment matrix.", type=click.Path(exists=False))
@click.option('-f2', '--fasta2', default='', show_default=True, help='Input fasta two.', type=click.Path(exists=False))
@click.option('-b', '--both', is_flag=True, help='Perform 2 alignments by switching the order of the two genomes.')
@click.option('-w', '--work_dir', default='./', show_default=True, help='Work directory for final outputs.', type=click.Path(exists=False))
@click.option('-bed', '--to_bed', is_flag=True, help='Convert MAF output to bed and compute identity.')
def align(ctx, fasta1,fasta2, both, work_dir, to_bed):
    """Align two fasta files."""
    work_dir += '/'
    if not fasta2:
        fastas = fasta1.split(',')
        similarity_matrix = pd.DataFrame(np.ones((len(fastas),len(fastas))).astype(float),index=fastas,columns=fastas)
        flagged = 1
    else:
        fastas = [(fasta1,fasta2)]
        flagged = 0
    for fasta1, fasta2 in combinations(fastas,r=2):
        last_files = []
        subprocess.call('python -m jcvi.apps.align last %s %s --format MAF'%(fasta1,fasta2),shell=True)
        last = fasta2[fasta2.rfind('/')+1:fasta2.rfind('.')] + '.' + fasta1[fasta1.rfind('/')+1:fasta1.rfind('.')] + '.last'
        shutil.copy(last, work_dir)
        last_files.append(work_dir+last)
        if both:
            subprocess.call('python -m jcvi.apps.align last %s %s --format MAF'%(fasta2,fasta1),shell=True)
            last = fasta1[fasta1.rfind('/')+1:fasta1.rfind('.')] + '.' + fasta2[fasta2.rfind('/')+1:fasta2.rfind('.')] + '.last'
            shutil.copy(last, work_dir)
            last_files.append(work_dir+last)
        if to_bed:
            ctx.invoke(maf2bed,last=','.join(last_files),work_dir=work_dir)
        if to_bed and flagged:
            with open(work_dir+'weighted_sum.txt','r') as f:
                similarity = float(f.read().splitlines()[0])
            similarity_matrix.loc[fasta1,fasta2] = similarity
            similarity_matrix.loc[fasta2,fasta1] = similarity
    if to_bed and flagged:
        similarity_matrix.to_csv(work_dir+'similarity_matrix.csv')


@polycracker.command(name='maf2bed')
@click.option('-maf', '--last', default='fasta1.fasta2.last,fasta2.fasta1.last', show_default=True, help='Maf output of last alignment. Comma delimited list if multiple maf files.', type=click.Path(exists=False))
@click.option('-w', '--work_dir', default='./', show_default=True, help='Work directory for final outputs.', type=click.Path(exists=False))
def maf2bed(last, work_dir): # FIXME what I can do instead is say that if > 57.5% sequence is covered, than that CDS is one and others are 0, count 1 CDS vs all 0 CDS for identity, does not have to be pure alignment, this should increase similarity scores
    """Convert maf file to bed and perform stats on sequence alignment."""
    from Bio import AlignIO
    #from BCBio import GFF
    import glob
    work_dir += '/'
    last_files = last.split(',')
    final_output = []
    for last in last_files:
        gff_files, bed_files_final = [] , []
        heads = last.split('/')[-1].split('.')[::-1][1:]
        for f_name in heads:
            open(work_dir + f_name+'.gff','w').close()
            gff_files.append(open(work_dir + f_name+'.gff','w'))
            bed_files_final.append(work_dir + f_name+'.bed')
        seqrecs = [[] for i in heads]
        for multiple_alignment in AlignIO.parse(last,'maf'):
            for i,seqrec in enumerate(multiple_alignment): # FIXME
                seqrecs[i].append((seqrec.name,seqrec.annotations['start'] if seqrec.annotations['strand'] == 1 else seqrec.annotations['srcSize'] - seqrec.annotations['start'] - seqrec.annotations['size'], seqrec.annotations['start'] + seqrec.annotations['size'] if seqrec.annotations['strand'] == 1 else seqrec.annotations['srcSize'] - seqrec.annotations['start']))

        #for i, gff_file in enumerate(gff_files):
        #    GFF.write(seqrecs[i],gff_file)
        #    subprocess.call('grep -v "##sequence-region" %s > %s && mv %s %s'%(gff_files_final[i],'temp.gff','temp.gff',gff_files_final[i]),shell=True)
        for i, bed_file in enumerate(bed_files_final):
            pd.DataFrame(seqrecs[i]).to_csv(bed_file, sep='\t',header=None,index=None)
        # FIXME
        fasta_files = []
        last_path = last[:last.rfind('/')+1]
        for f in heads:
            fasta_files.extend(glob.glob(last_path+f+'.fasta') + glob.glob(last_path+f+'.fa'))
        for i,fasta in enumerate(fasta_files):
            Fasta(fasta)
            subprocess.call("awk -v OFS='\\t' '{print $1, 0, $2}' %s > %s"%(fasta+'.fai',fasta+'.bed'),shell=True)
            a = BedTool(fasta+'.bed').sort()
            df = a.intersect(BedTool(bed_files_final[i]).sort().merge()).to_dataframe()
            df2 = a.to_dataframe()
            intersect_sum = (df['end'] - df['start']).sum()
            genome_size = (df2['end'] - df2['start']).sum()
            final_output.append((heads[i],genome_size,intersect_sum,float(intersect_sum)/genome_size))
    df_final = pd.DataFrame(final_output,columns = ['fasta_head','genome_size','length_aligned','percent_aligned'])
    df_final.to_csv(work_dir+'sequence_similarity.csv')
    with open(work_dir+'weighted_sum.txt','w') as f:
        f.write(str((df_final['percent_aligned']*df_final['genome_size']).sum()/float(df_final['genome_size'].sum())))


@polycracker.command(name='convert_mat2R')
@click.option('-npz','--input_matrix',default='clusteringMatrix.npz',help='Input sparse matrix, scipy sparse npz format.',show_default=True, type=click.Path(exists=False))
def convert_mat2R(input_matrix):
    """Convert any sparse matrix into a format to be read by R. Can import matrix into R metagenomics clustering programs."""
    from scipy.io import mmwrite
    mmwrite(input_matrix.replace('.npz','.mtx'),sps.load_npz(input_matrix))


def find_genomic_space(scaffolds):
    dict_space = OrderedDict()
    for i,scaffold in enumerate(scaffolds.tolist()):
        sl = scaffold.split('_')
        dict_space[scaffold] = {}
        dict_space[scaffold]['_'.join(sl[:-2])] = np.mean(map(int,sl[-2:]))
    print dict_space
    scaffold_origin = {scaff:i for i, scaff in enumerate(set([dict_space[scaffold].keys()[0] for scaffold in dict_space.keys()]))}
    #print list(enumerate([dict_space[scaffold].keys()[0] for scaffold in dict_space.keys()]))
    dok = sps.dok_matrix((len(scaffolds),len(scaffold_origin.keys())),dtype=np.float)
    for i,scaffold in enumerate(dict_space.keys()):
        for scaff in dict_space[scaffold]:
            #print i,scaffold,scaff
            dok[i,scaffold_origin[scaff]] = dict_space[scaffold][scaff]
    dok = dok.tocsr()
    dok.data += 1000000000000.
    dok = dok.todense()
    #dok[dok==0] = np.max(dok) # 100000000000
    return dok


@polycracker.command(name='bed2scaffolds_pickle')
@click.option('-i', '--bed_file', default = 'correspondence.bed', show_default=True, help='Input bed file, original coordinate system.', type=click.Path(exists=False))
@click.option('-o', '--output_pickle', default='scaffolds_new.p', help='Pickle file containing the new scaffolds.', show_default=True, type=click.Path(exists=False))
def bed2scaffolds_pickle(bed_file, output_pickle):
    """Convert correspondence bed file, containing complete scaffold information into a list of scaffolds file."""
    pickle.dump(np.array([line for line in os.popen("awk '{print $1 \"_\" $2 \"_\" $3 }' %s"%bed_file).read().splitlines() if line]),open(output_pickle,'wb'))


@polycracker.command(name='scaffolds2colors_specified')
@click.option('-s', '--scaffolds_pickle', default='scaffolds.p', help='Path to scaffolds pickle file.', show_default=True, type=click.Path(exists=False))
@click.option('-d', '--labels_dict', help='Comma delimited dictionary of text to find in scaffold to new label. Example: text1:label1,text2:label2')
@click.option('-o', '--output_pickle', default='colors_pickle.p', help='Pickle file containing the new scaffold labels.', show_default=True, type=click.Path(exists=False))
def scaffolds2colors_specified(scaffolds_pickle,labels_dict,output_pickle):
    """Attach labels to each scaffold for use of plotPositions. Colors scaffolds based on text within each scaffold. Useful for testing/evaluation purposes."""
    scaffolds = pickle.load(open(scaffolds_pickle,'rb'))
    labels_dict = {text:label for text,label in [tuple(mapping.split(':')) for mapping in labels_dict.split(',')]}
    def relabel(scaffold,labels_dict = labels_dict):
        for text in labels_dict:
            if text in scaffold:
                return labels_dict[text]
        return 'unlabelled'
    pickle.dump(np.vectorize(relabel)(scaffolds),open(output_pickle,'wb'))


@polycracker.command(name='extract_scaffolds_fasta')
@click.pass_context
@click.option('-fi', '--input_fasta', default='', help='Path to genome.', show_default=True, type=click.Path(exists=False))
@click.option('-d', '--labels_dict', help='Comma delimited dictionary of text to find in scaffold to new output file head name, omitting .fa or .fasta. Example: text1:label1,text2:label2')
@click.option('-o', '--output_dir', default='./', help='Output directory.', show_default=True, type=click.Path(exists=False))
def extract_scaffolds_fasta(ctx,input_fasta,labels_dict,output_dir):
    """Extract scaffolds from fasta file using names that the sequences start with."""
    output_dir += '/'
    scaffolds = np.array(Fasta(input_fasta).keys())
    labels_dict = {text:label for text,label in [tuple(mapping.split(':')) for mapping in labels_dict.split(',')]}
    def relabel(scaffold,labels_dict = labels_dict):
        for text in labels_dict:
            if text in scaffold:
                return labels_dict[text]
        return 'unlabelled'
    labels = np.vectorize(relabel)(scaffolds)
    txt_files = []
    for label in set(labels):
        with open(output_dir+label+'.txt','w') as f:
            f.write('\n'.join(scaffolds[labels==label]))
        txt_files.append(output_dir+label+'.txt')
    ctx.invoke(txt2fasta,txt_files = ','.join(txt_files), reference_fasta = input_fasta)


@polycracker.command()
@click.option('-c', '--input_labels', default='colors_pickle.p', help='Pickle file containing the cluster/class each label/scaffold belongs to.', show_default=True, type=click.Path(exists=False))
@click.option('-s', '--scaffolds_pickle', default='scaffolds.p', help='Path to scaffolds pickle file.', show_default=True, type=click.Path(exists=False))
@click.option('-o', '--output_pickle', default='labels_new.p', help='Pickle file containing the new cluster/class of scaffolds.', show_default=True, type=click.Path(exists=False))
@click.option('-npy', '--transformed_data', default='', help='Input transformed matrix. Can leave empty, but if using this, label propagater will calculate distances from this matrix. Recommended use: differential kmer or TE matrix or PCA reduced data.', type=click.Path(exists=False))
@click.option('-r', '--radius', default=100000., help='Total radius in bps of search to look for neighboring classified sequences for RadiusNeighborsClassifier.', show_default=True)
def genomic_label_propagation(input_labels,scaffolds_pickle,output_pickle, transformed_data,radius):
    """Extend polyCRACKER labels up and downstream of found labels. Only works on split scaffold naming."""
    from sklearn.neighbors import RadiusNeighborsClassifier
    scaffolds = pickle.load(open(scaffolds_pickle,'rb'))
    initial_labels = pickle.load(open(input_labels,'rb'))
    labels_dict = {label: i for i, label in enumerate(np.setdiff1d(np.unique(initial_labels),['ambiguous']).tolist())}
    labels_dict['ambiguous'] = -1
    inverse_dict = {i:label for label,i in labels_dict.items()}
    codified_labels = np.vectorize(lambda x: labels_dict[x])(initial_labels)
    print codified_labels
    if transformed_data:
        genomic_space = np.load(transformed_data)
    else:
        genomic_space = find_genomic_space(scaffolds)
    #label_prop = LabelSpreading(kernel='knn',n_neighbors=n_neighbors)
    #label_prop.fit(genomic_space,codified_labels)
    radius = radius
    r_neigh = RadiusNeighborsClassifier(radius = radius, outlier_label=-1)
    r_neigh.fit(genomic_space[codified_labels != -1],codified_labels[codified_labels != -1])
    propagated_labels = codified_labels
    propagated_labels[propagated_labels == -1] = r_neigh.predict(genomic_space[codified_labels == -1])
    #print neigh.kneighbors_graph(genomic_space,n_neighbors=15).todense()
    new_labels = np.vectorize(lambda x: inverse_dict[x])(propagated_labels)#(label_prop.predict(genomic_space))
    pickle.dump(new_labels,open(output_pickle,'wb'))
    with open(output_pickle.replace('.p','.bed'),'w') as f:
        for scaffold, label in zip(scaffolds.tolist(),new_labels.tolist()):
            sl = scaffold.split('_')
            f.write('\t'.join(['_'.join(sl[:-2])]+sl[-2:]+[label])+'\n')


@polycracker.command(name='unionbed2matrix')
@click.option('-u', '--unionbed', default='subgenomes.union.bedgraph', help='Unionbed file containing counts of differential kmers or TEs.', show_default=True, type=click.Path(exists=False))
@click.option('-o', '--output_matrix', default='subgenomes.union.bed_matrix.npy', help='Output path to differential kmer/TE matrix', show_default=True, type=click.Path(exists=False))
def unionbed2matrix(unionbed, output_matrix):
    """Convert unionbed file into a matrix of total differential kmer counts for each scaffold."""
    with open(unionbed,'r') as f:
        out_matrix = np.array([map(float,line.split()[3:]) for line in f if line])
    np.save(output_matrix,out_matrix)


@polycracker.command(name='generate_out_bed')
@click.option('-id', '--input_dir', default='./', help='Directory containing solely the cluster/classified outputs, with names stored in txt files.', show_default=True, type=click.Path(exists=False))
@click.option('-o', '--original', default=0, help='Select 1 if subgenomeExtraction was done based on original nonchunked genome.', show_default=True)
@click.option('-fai', '--fai_file', help='Full path to original, nonchunked fai file.', type=click.Path(exists=False))
@click.option('-fo', '--output_fname', default = 'output.bed', help='Desired output bed file.', show_default=True, type=click.Path(exists=False))
def generate_out_bed(input_dir, original, fai_file, output_fname):
    """Find cluster labels for all clusters/subgenomes in directory, output to bed."""
    try:
        original = int(original)
    except:
        original = 0
    if input_dir.endswith('/') == 0:
        input_dir += '/'
    open(output_fname,'w').close()
    if original:
        genomeDict = {line.split('\t')[0]: line.split('\t')[1] for line in open(fai_file, 'r') if line}
    for file in os.listdir(input_dir):
        if file.endswith('.txt') and file.startswith('subgenome_'):
            subgenome = file.split('.')[0]
            if original == 0:
                with open(input_dir+file,'r') as f ,open(output_fname,'a') as f2:
                    f2.write('\n'.join(['\t'.join(['_'.join(line.strip('\n').split('_')[0:-2])] + line.strip('\n').split('_')[-2:] + [subgenome]) for line in f if line])+'\n')
            else:
                with open(input_dir + file, 'r') as f, open(output_fname, 'a') as f2:
                    f2.write('\n'.join(['\t'.join([line.strip('\n').split('\t')[0],'0',genomeDict[line.strip('\n').split('\t')[0]]] + [subgenome]) for
                                        line in f if line]) + '\n')


@polycracker.command(name="convert_subgenome_output_to_pickle")
@click.option('-id', '--input_dir', default='./', help='Directory containing solely the cluster/classified outputs, with names stored in txt files. Can input bed file here as well.', show_default=True, type=click.Path(exists=False))
@click.option('-s', '--scaffolds_pickle', default='scaffolds.p', help='Path to scaffolds pickle file.', show_default=True, type=click.Path(exists=False))
@click.option('-o', '--output_pickle', default='colors_pickle.p', help='Desired output pickle name. Can feed colors_pickle.p, or name you choose, into plotPositions.', show_default=True, type=click.Path(exists=False))
def convert_subgenome_output_to_pickle(input_dir, scaffolds_pickle, output_pickle):
    """Find cluster labels for all clusters/subgenomes in directory."""
    scaffolds = pickle.load(open(scaffolds_pickle,'rb'))
    clusters = defaultdict(list)
    if input_dir.endswith('.bed'):
        clusters = dict(zip(os.popen("awk '{print $1 \"_\" $2 \"_\" $3}' %s"%input_dir).read().splitlines(),os.popen("awk '{print $4}' %s"%input_dir).read().splitlines()))
        """
        with open(input_dir,'r') as f:
            for line in f:
                lineList = line.split()
                clusters['_'.join(lineList[0:3])] = lineList[-1].strip('\n')"""
    else:
        for file in os.listdir(input_dir):
            if file.endswith('.txt'):
                cluster_name = file.replace('.txt','')
                with open(input_dir+file,'r') as f:
                    for line in f:
                        clusters[line.strip('\n')] = cluster_name
    pickle.dump(np.vectorize(lambda x: clusters[x] if x in clusters.keys() else 'ambiguous')(scaffolds),open(output_pickle,'wb'))


@polycracker.command()
@click.option('-s', '--scaffolds_pickle', default='scaffolds.p', help='Path to scaffolds pickle file.', show_default=True, type=click.Path(exists=False))
@click.option('-o', '--output_pickle', default='colors_pickle.p', help='Path to output species pickle file.', show_default=True, type=click.Path(exists=False))
def species_comparison_scaffold2colors(scaffolds_pickle,output_pickle):
    """Generate color pickle file for plotPositions if list of scaffolds contains progenitors/species of origin. Useful for testing purposes."""
    scaffolds = pickle.load(open(scaffolds_pickle,'rb'))
    pickle.dump(np.vectorize(lambda x: x.split('_')[0])(scaffolds),open(output_pickle,'wb'))

@polycracker.command()
@click.pass_context
@click.option('-b3', '--bed3_directory', default='./', help='Directory containing bed3 files produced from subgenomeExtraction.', show_default=True, type=click.Path(exists=False))
@click.option('-o', '--original', default=0, help='Select 1 if subgenomeExtraction was done based on original nonchunked genome.', show_default=True)
@click.option('-sl', '--split_length', default=75000, help='Length of intervals in bedgraph files.', show_default=True)
@click.option('-fai', '--fai_file', help='Full path to original, nonchunked fai file.', type=click.Path(exists=False))
@click.option('-w', '--work_folder', default='./', help='Working directory for processing subgenome bedgraphs and unionbedgraph.', show_default=True, type=click.Path(exists=False))
def generate_unionbed(ctx, bed3_directory, original, split_length, fai_file, work_folder): # FIXME add smoothing function by overlapping the intervals
    """Generate a unionbedgraph with intervals of a specified length based on bed3 files from subgenomeExtraction"""
    global inputStr, key
    if work_folder.endswith('/') == 0:
        work_folder += '/'
    def grabLine(positions):
        global inputStr
        global key
        if positions[-1] != 'end':
            return '%s\t%s\t%s\n'%tuple([key]+map(str,positions[0:2]))
        else:
            return '%s\t%s\t%s\n'%(key, str(positions[0]), str(inputStr))
    def split(inputStr=0,width=60):
        if inputStr:
            positions = np.arange(0,inputStr,width)
            posFinal = []
            if inputStr > width:
                for i in range(len(positions[:-1])):
                    posFinal += [(positions[i],positions[i+1])]
            posFinal += [(positions[-1],'end')]
            splitLines = map(grabLine,posFinal)
            return splitLines
        else:
            return ''
    bedText = []
    for key, seqLength in [tuple(line.split('\t')[0:2]) for line in open(fai_file,'r') if line]:
        inputStr = int(seqLength)
        bedText += split(inputStr,split_length)
    a = BedTool('\n'.join(bedText),from_string=True).sort().saveas(work_folder + '/windows.bed') # add ability to overlap windows
    # convert coordinates of bed, use original fai_file
    bed_graphs_fn = []
    subprocess.call('cut -f 1-2 %s > %s.genome'%(fai_file, work_folder + '/genome'),shell=True)
    for bedfile in os.listdir(bed3_directory):
        if bedfile.endswith('.bed3') or bedfile.endswith('.bed'):
            if original == 0:
                bedText = []
                with open(bed3_directory+'/'+bedfile,'r') as f:
                    for line in f:
                        if line:
                            lineList = line.split()
                            lineList2 = lineList[0].split('_')
                            lineList[1:] = map(lambda x: str(int(lineList2[-2])+ int(x.strip('\n'))), lineList[1:])
                            lineList[0] = '_'.join(lineList2[:-2])
                            bedText.append('\t'.join(lineList))
                b = BedTool('\n'.join(bedText),from_string=True).sort()
            else:
                b = BedTool(bed3_directory+'/'+bedfile).sort()
            coverage = a.coverage(b).sort()
            bedgname = work_folder + bedfile[:bedfile.rfind('.')] + '.sorted.cov.bedgraph'
            with open(bedgname,'w') as bedgo:
                for line in str(coverage).splitlines():
                    lineInList = line.split()
                    lineOutputList = [lineInList[0], int(lineInList[1]), int(lineInList[2]), int(lineInList[4]) ]
                    bedgo.write('%s\t%d\t%d\t%d\n'%tuple(lineOutputList))
            bed_graphs_fn.append(bedgname)
    if len(bed_graphs_fn) == 1:
        subprocess.call('scp %s %s'%(bedgname,work_folder+'subgenomes.union.bedgraph'),shell=True)
        with open(work_folder+'subgenomes.union.bedgraph','r') as f:
            bed_txt = f.read().splitlines()
    else:
        x = BedTool()
        result = x.union_bedgraphs(i=bed_graphs_fn, g=work_folder + '/genome.genome')
        result.saveas(work_folder+'original_coordinates.subgenomes.union.bedgraph')
        bed_txt = str(result).splitlines()
    with open(work_folder+'subgenomes.union.bedgraph','w') as f:
        for line in bed_txt:
            lineList = line.split()
            lineList[-1] = lineList[-1].strip('\n')
            lineList[0] = '_'.join(lineList[0:3])
            lineList[2] = str(int(lineList[2]) - int(lineList[1]))
            lineList[1] = '0'
            f.write('\t'.join(lineList)+'\n')


@polycracker.command()
@click.option('-i', '--hipmer_input', default='test.txt', help = 'Input file or directory from hipmer kmer counting run.', show_default=True, type=click.Path(exists=False))
@click.option('-o', '--kcount_output', default='test.final.kcount', help = 'Output kmer count file.', show_default=True, type=click.Path(exists=False))
@click.option('-d', '--run_on_dir', is_flag=True, help='Choose to run on all files in hipmer_input if you have specified a directory for the hipmer input. Directory can only contain hipmer files.')
def hipmer_output_to_kcount(hipmer_input, kcount_output, run_on_dir):
    """Converts hipmer kmer count output into a kmer count, kcount, file."""
    if run_on_dir:
        hipmer_path = hipmer_input + '/'
        subprocess.call("cat %s | awk '{OFS = \"\\t\"; sum=0; for (i=2; i<=7; i++) { sum+= $i }; if (sum >= 3) print $1, sum}' > %s"%(' '.join([hipmer_path+hipmer_input for hipmer_input in os.listdir(hipmer_path)]),kcount_output),shell=True)
    else:
        subprocess.call("cat %s | awk '{OFS = \"\\t\"; sum=0; for (i=2; i<=7; i++) { sum+= $i }; if (sum >= 3) print $1, sum}' > %s"%(hipmer_input,kcount_output),shell=True)


@polycracker.command(name='progenitorMapping')
@click.pass_context
@click.option('-i', '--input_fasta', help='Complete path to input polyploid fasta file, original or chunked.', type=click.Path(exists=False))
@click.option('-p', '--progenitor_fasta_folder', default='./progenitors/', help='Folder containing progenitor genomes.', show_default=True, type=click.Path(exists=False))
@click.option('-m', '--blast_mem', default='100', help='Amount of memory to use for bbtools run. More memory will speed up processing.', show_default=True)
@click.option('-o', '--original', default=0, help='Select 1 if trying to extract subgenomes based on original nonchunked genome.', show_default=True)
@click.option('-kl', '--kmer_length', default='23', help='Length of kmers to use for subgenome extraction.', show_default=True)
@click.option('-fout', '--outputfname', default='progenitors.bed', help='Output progenitor name', show_default=True, type=click.Path(exists=False))
@click.option('-pf', '--progenitor_fastas', default = '', help='Optional: in addition to the progenitor fasta folder, directly specify the filename of each progenitor fasta and how you would like each fasta to be labelled as. Comma delimited list of fasta:label pairing. Example usage: -pf subgenomeT.fa:T,subgenomeA.fa:A,subgenomeR.fa:R', type=click.Path(exists=False))
@click.option('-gff', '--gff_file', default = '', help='Optional:If progenitor_fastas specified, you have the option to input gff file, which will be split up into progenitor specific gene bed files for future synteny run.',show_default=True)
@click.option('-go', '--original_genome', default='', show_default=True, help='If running synteny: Filename of polyploid fasta; must be full path to original. Use if input gff file. Need to install jcvi library to run', type=click.Path(exists=False))
def progenitorMapping(ctx,input_fasta, progenitor_fasta_folder, blast_mem, original, kmer_length, outputfname, progenitor_fastas, gff_file, original_genome):
    """Takes reference progenitor fasta files, and bins an input polyploid file according to progenitor. These results will be compared to polyCRACKER's results."""
    create_path(progenitor_fasta_folder)
    genome_info = []
    if progenitor_fasta_folder.endswith('/') == 0:
        progenitor_fasta_folder += '/'
    seal_outdir = progenitor_fasta_folder + 'seal_outputs/'
    create_path(seal_outdir)
    if progenitor_fastas:
        progenitor_fastas = dict([tuple(progenitor.split(':')) for progenitor in progenitor_fastas.split(',')])
        progenitorFastas = ','.join([progenitor_fasta_folder+progenitor_fasta for progenitor_fasta in progenitor_fastas])
        progenitor_labels = {progenitor_fasta.replace('.fasta','').replace('.fa',''):label for progenitor_fasta,label in progenitor_fastas.items()}
    else:
        progenitorFastas = ','.join([progenitor_fasta_folder + file for file in os.listdir(progenitor_fasta_folder) if file.endswith('.fasta') or file.endswith('.fa')])
    subprocess.call('seal.sh ref=%s in=%s pattern=%sout_%%.seal.fasta outu=%s/unmatched.seal.ignore.fasta ambig=all '
                    'refnames overwrite=t k=%s refstats=match.stats threads=4 -Xmx%sg'%(progenitorFastas,input_fasta,seal_outdir,seal_outdir,kmer_length,blast_mem),shell=True)
    subgenomes = []
    if original:
        genomeDict = {line.split('\t')[0]: line.split('\t')[1] for line in open(input_fasta+'.fai', 'r') if line}
    open(outputfname,'w').close()
    count = 0
    for file in os.listdir(seal_outdir):
        if file.endswith('seal.fasta'):
            if progenitor_fastas:
                subgenomeName = 'Subgenome_' + progenitor_labels[file.replace('out_','').replace('.seal.fasta','')]
            else:
                subgenomeName = 'Subgenome_' + chr(65+count)
            subgenomes.append(file)
            Fasta(seal_outdir+file)
            if original:
                with open(seal_outdir + file + '.fai','r') as f, open(outputfname,'a') as f2:
                    f2.write('\n'.join(['\t'.join([line.strip('\n').split('\t')[0],'0',genomeDict[line.strip('\n').split('\t')[0]]] + [subgenomeName]) for line in f if line])+'\n')
            else:
                with open(seal_outdir + file + '.fai','r') as f, open(outputfname,'a') as f2:
                    f2.write('\n'.join(['\t'.join(['_'.join(line.strip('\n').split('\t')[0].split('_')[0:-2])] + line.strip('\n').split('\t')[0].split('_')[-2:] + [subgenomeName]) for line in f if line])+'\n')
            count += 1
    if progenitor_fastas:
        for progenitor_label in progenitor_labels.values():
            subprocess.call('grep Subgenome_%s progenitors.bed | bedtools sort | bedtools merge > progenitor_%s.bed'%(progenitor_label,progenitor_label),shell=True)
        if gff_file:
            gff = BedTool(gff_file)
            for progenitor_label in progenitor_labels.values():
                progenitor_bed = BedTool('progenitor_%s.bed'%progenitor_label)
                progenitor_gff = 'progenitor_%s.gff3'%progenitor_label
                gff.intersect(progenitor_bed,wa=True).sort().saveas(progenitor_gff)
                with open('progenitor_%s.bed'%progenitor_label,'w') as f:
                    for line in str(progenitor_bed).splitlines():
                        if line:
                            f.write(line + '\t%s\n'%('_'.join(line.split())))
                subprocess.call('python -m jcvi.formats.gff bed --type=mRNA --key=gene_name %s > progenitor%s.bed'%(progenitor_gff,progenitor_label),shell=True)
                if original_genome:
                    subprocess.call('samtools faidx '+original_genome,shell = True)
                    subprocess.call('python -m jcvi.formats.gff load %s %s --parents=mRNA --children=CDS -o progenitor%s.cds'%(progenitor_gff,original_genome,progenitor_label),shell=True)
            if original_genome and gff_file:
                for proj1, proj2 in combinations(progenitor_labels.values(), 2):
                    subprocess.call('python -m jcvi.compara.catalog ortholog progenitor%s progenitor%s'%(proj1, proj2),shell=True)
                    ctx.invoke(anchor2bed,anchor_file='protenitor%s.progenitor%s.lifted.anchors'%(proj1,proj2),qbed='progenitor%s.bed'%proj1, sbed='progenitor%s.bed'%proj2)
                    #subprocess.call('python -m jcvi.assembly.syntenypath bed %s --switch --scale=10000 --qbed=progenitor%s.bed --sbed=progenitor%s.bed -o synteny.%s.%s.bed'%(proj1+'_'+proj2+'.bed',proj1,proj2,proj1,proj2),shell=True)


@polycracker.command()
@click.option('-a', '--anchor_file', help = 'Lifted anchor file generated from basic synteny run using jcvi tools.', type=click.Path(exists=False))
@click.option('-q', '--qbed', help='First bed file.', type=click.Path(exists=False))
@click.option('-s', '--sbed', help='Second bed file.', type=click.Path(exists=False))
def anchor2bed(anchor_file, qbed, sbed):
    """Convert syntenic blocks of genes to bed coordinates between the two genomes being compared."""
    with open(anchor_file,'r') as f:
        anchors = f.read().split('###')
    with open(qbed,'r') as f:
        qbed = {}
        for line in f:
            if line:
                lineL = line.split()
                qbed[lineL[3]] = [lineL[0]] + map(int,lineL[1:3])
    #print qbed
    with open(sbed,'r') as f:
        sbed = {}
        for line in f:
            if line:
                lineL = line.split()
                sbed[lineL[3]] = [lineL[0]] + map(int,lineL[1:3])
    with open(anchor_file.replace('.lifted.anchors','.bed'),'w') as f:
        for anchor in anchors:
            if anchor:
                #print anchor
                q_coords = []
                s_coords = []
                for line in anchor.splitlines():
                    if line:
                        genes = line.split()[:2]
                        #print genes
                        q_coords.append(qbed[genes[0]])
                        s_coords.append(sbed[genes[1]])
                #print q_coords
                q_coords = pd.DataFrame(np.array(q_coords)).sort_values([0,1]).as_matrix()
                s_coords = pd.DataFrame(np.array(s_coords)).sort_values([0,1]).as_matrix()
                f.write('\t'.join(map(str,[q_coords[0,0],q_coords[:,1:].min(),q_coords[:,1:].max(), s_coords[0,0],s_coords[:,1:].min(),s_coords[:,1:].max()]))+'\n')
    with open(anchor_file.replace('.lifted.anchors','.bed'),'r') as f:
        links = np.array([line.split() for line in f.read().splitlines()])
        colors_set = {color:i+1 for i, color in enumerate(set(links[:,0]))}
        colors = pd.DataFrame(np.vectorize(lambda color: colors_set[color])(links[:,0]),columns=['Color'])
        colors.to_csv('link_colors.csv',index=False)
        links = pd.DataFrame(links,columns=['seg1','start1','end1','seg2','start2','end2'])
        links.to_csv('links.csv',index=False)
        # FIXME, need to grab correct orientation!!!


def compute_correlation(mat):
    rowShape, columnShape = np.shape(mat)
    rowCombos = permutations(range(rowShape),rowShape)
    columnCombos = permutations(range(columnShape),columnShape)
    print mat
    maxR = []
    for idx,combos in enumerate([columnCombos,rowCombos]):
        for combo in combos:
            if idx == 0:
                matNew = mat[:, combo]
            else:
                matNew = mat[combo, :]
            coords = []
            for i in range(rowShape):
                for j in range(columnShape):
                    if matNew[i,j] > 0:
                        for k in range(matNew[i,j]):
                            coords.append((i,j))
            xy = np.array(coords)
            maxR.append(abs(pearsonr(xy[:,0],xy[:,1])[0]))
    return max(maxR)

@polycracker.command(name='compareSubgenomes_progenitors_v_extracted')
@click.option('-s', '--scaffolds_file', default='scaffolds.p', help='Path to scaffolds pickle file.', show_default=True, type=click.Path(exists=False))
@click.option('-b1', '--bed1', default='bootstrap_results.bed', help='Bed file containing bootstrapped results.', show_default=True, type=click.Path(exists=False))
@click.option('-b2', '--bed2', default='progenitors.bed', help='Bed file containing progenitor results. Alternatively, you can include the results from a prior bootstrap.', show_default=True, type=click.Path(exists=False))
@click.option('-od', '--out_dir', default='./', help='Write results to this output directory.', show_default=True, type=click.Path(exists=False))
def compareSubgenomes_progenitors_v_extracted(scaffolds_file, bed1, bed2, out_dir):
    """Compares the results found from the progenitorMapping function to results from polyCRACKER. Outputs CompareSubgenomesToProgenitors* files in the output directory. Final_stats is a better alternative to this function."""
    import seaborn as sns
    if out_dir.endswith('/') == 0:
        out_dir += '/'
    scaffolds = pickle.load(open(scaffolds_file,'rb'))
    scaffoldsDict = {scaffold: '\t'.join(['_'.join(scaffold.split('_')[0:-2])] + scaffold.split('_')[-2:]) for
                     scaffold in scaffolds}
    scaffoldsBed = BedTool('\n'.join(scaffoldsDict.values()), from_string=True)
    subgenomesDicts = []
    for bed_file in [bed1,bed2]:
        featureBed = BedTool(bed_file)
        finalBed = scaffoldsBed.intersect(featureBed, wa=True, wb=True).sort().merge(d=-1, c=7, o='distinct')
        scaffolds_final = defaultdict(list)
        for line in str(finalBed).splitlines():
            lineList = line.strip('\n').split('\t')
            feature = lineList[-1]
            scaffold = '_'.join(lineList[0:-1])
            if ',' not in feature:
                scaffolds_final[feature].append(scaffold)
        for feature in scaffolds_final.keys():
            scaffolds_final[feature] = set(scaffolds_final[feature])
        subgenomesDicts.append(scaffolds_final)
    finalDict = defaultdict(list)
    for key in subgenomesDicts[0]:
        finalDict[key] = {key2: len(subgenomesDicts[0][key].intersection(subgenomesDicts[1][key2])) for key2 in subgenomesDicts[1]}
    df = pd.DataFrame(finalDict)
    correlation = compute_correlation(df.as_matrix())
    df.to_csv(out_dir + 'CompareSubgenomesToProgenitors.csv')
    plt.figure()
    sns_plot = sns.heatmap(df, annot=True)
    plt.title('Extracted Subgenomes v Progenitors, r = %.4f'%(correlation))
    plt.xlabel(bed1 + ', collected %.2f %% scaffolds'%(sum([len(subgenomesDicts[0][key]) for key in subgenomesDicts[0].keys()])/float(len(scaffolds))*100))
    plt.ylabel(bed2 + ', collected %.2f %% scaffolds'%(sum([len(subgenomesDicts[1][key]) for key in subgenomesDicts[1].keys()])/float(len(scaffolds))*100))
    plt.savefig(out_dir + 'CompareSubgenomesToProgenitors.png', dpi=300)
    plt.savefig(out_dir + 'CompareSubgenomesToProgenitors.pdf', dpi=300)



########################################################################################################

###################################### DIFFERENTIAL KMER ANALYSES ######################################

def write_informative_diff_kmers(informative_diff_kmers, work_dir):
    kmer_dir = work_dir+'informative_diff_kmers/'
    try:
        os.makedirs(kmer_dir)
    except:
        pass
    for subgenome in informative_diff_kmers:
        with open(kmer_dir+subgenome+'informative.higher.kmers.fa','w') as f:
            f.write('\n'.join(['>%s\n%s'%(kmer,kmer) for kmer in informative_diff_kmers[subgenome]]))
    return kmer_dir

def jaccard_similarity(sparse_matrix):
    """similarity=(ab)/(aa + bb - ab)"""
    cols_sum = sparse_matrix.getnnz(axis=0)
    ab = sparse_matrix.T * sparse_matrix
    aa = np.repeat(cols_sum, ab.getnnz(axis=0))
    bb = cols_sum[ab.indices]
    similarities = ab.copy()
    similarities.data /= (aa + bb - ab.data)
    return similarities

def output_Dendrogram(distance_matrix_npy, kmers_pickle, out_dir):
    from scipy.cluster.hierarchy import dendrogram, linkage
    from scipy.spatial.distance import squareform
    import plotly.figure_factory as ff
    distance_matrix = np.load(distance_matrix_npy)
    dists = squareform(distance_matrix)
    linkage_mat = linkage(dists, 'single')
    kmers = pickle.load(open(kmers_pickle,'rb'))
    plt.figure()
    dendrogram(linkage_mat,labels=kmers)
    plt.savefig(out_dir+'output_dendrogram.png')
    fig = ff.create_dendrogram(linkage_mat, orientation='left', labels=kmers)
    fig['layout'].update({'width':1200, 'height':1800})
    py.plot(fig, filename=out_dir+'output_dendrogram.html', auto_open=False)

def repeatGFF2Bed(repeat_gff, out_dir, labels = 0):
    if repeat_gff.endswith('.gff') or repeat_gff.endswith('.gff3'):
        output_bed = out_dir+'repeats.bed'
        repeat_class_subclass = []
        repeat_motifs = []
        BedTool(repeat_gff).sort().saveas(repeat_gff)
        #subprocess.call('bedtools sort -i %s > temp.gff3 && mv temp.gff3 > %s'%(repeat_gff,repeat_gff), shell=True)
        with open(repeat_gff,'r') as f:
            repeat_elements = []
            repeat_elements2 = []
            for line in f:
                if line and line.startswith('#') == 0:
                    lineList = line.strip('\n').split()
                    subclass = lineList[-1].strip('"')
                    motif = lineList[-4].strip('"').replace('Motif:','')
                    repeat_class_subclass.append(subclass)
                    repeat_motifs.append(motif)
                    repeat_elements.append('%s\t%d\t%s'%(lineList[0],int(lineList[3])-1,lineList[4]))
                    repeat_elements2.append(motif+'#'+subclass)


        repeat_elements, idxs = np.unique(np.array(repeat_elements),return_index=True)
        repeat_elements2 = np.array(repeat_elements2)[idxs]
        repeat_class_subclass = np.array(repeat_class_subclass)[idxs]
        repeat_motifs = np.array(repeat_motifs)[idxs]

        if labels:
            with open(output_bed, 'w') as f2:
                f2.write('\n'.join(np.vectorize(lambda i: '%s\t%s'%(repeat_elements[i],repeat_elements2[i]))(range(len(repeat_elements)))))
        else:
            with open(output_bed, 'w') as f2:
                f2.write('\n'.join(repeat_elements))

        pickle.dump(repeat_elements2,open(out_dir + 'TE_motif_subclass_raw_list.p','wb'))
        repeat_elements2 = Counter(repeat_elements2)

        repeat_elements = np.vectorize(lambda x: x.replace('\t','_'))(repeat_elements)

        pickle.dump(repeat_elements,open(out_dir + 'repeat_elements.p','wb'))
        pickle.dump(repeat_elements2.keys(),open(out_dir + 'TE_motif_subclass.p','wb'))
        pickle.dump(repeat_elements2,open(out_dir + 'TE_motif_subclass_counter.p','wb'))
        pickle.dump(repeat_motifs,open(out_dir + 'repeat_motifs.p','wb'))
        pickle.dump(repeat_class_subclass,open(out_dir + 'repeat_class_subclass.p','wb'))
        pickle.dump({repeat_elements[i]:repeat_class_subclass[i] for i in range(len(repeat_elements))}, open(out_dir + 'repeat_class_dictionary.p','wb'))
    elif repeat_gff.endswith('.bed'):
        output_bed = repeat_gff
    else:
        output_bed = 'xxx'
    return output_bed

def sam2diffkmer_clusteringmatrix(work_dir,kmers_pickle,blast_path, kernel, repeat_bed, TE_cluster = 0):
    if TE_cluster:
        windows = BedTool(work_dir + 'windows.bed')
        kmers = pickle.load(open(kmers_pickle,'rb'))
        with open(work_dir + 'windows.bed','r') as f:
            scaffolds = np.array([line.replace('\t','_') for line in f.read().splitlines() if line])
        pickle.dump(scaffolds, open(work_dir+'scaffolds_TE_cluster_analysis.p','wb'))
        repeat_masked_TEs = windows.intersect(repeat_bed,wa=True,wb=True).sort()
        TE_repeat_masked = ''
        for line in str(repeat_masked_TEs).splitlines():
            if line:
                lineList = line.strip('\n').split()
                TE_repeat_masked += '\t'.join(['_'.join(lineList[0:3]), '0', str(int(lineList[2]) - int(lineList[1])), lineList[-1]]) + '\n'
        TE_repeat_masked = BedTool(TE_repeat_masked,from_string=True).sort().merge(c=4, o='collapse').sort()
        bedText = []
        for line in str(TE_repeat_masked).splitlines():
            if line:
                lineList = line.strip('\n').split()
                lineList2 = lineList[0].split('_')
                lineList[1:-1] = map(lambda x: str(int(lineList2[-2])+ int(x.strip('\n'))), lineList[1:-1])
                lineList[0] = '_'.join(lineList2[:-2])
                bedText.append('\t'.join(lineList))
        BedTool('\n'.join(bedText),from_string=True).sort().saveas(work_dir+'clustering_TEs.bed')
        build_cluster_matrix = [(scaffolds, work_dir+'clustering_TEs.bed',work_dir+'TEclusteringMatrix.npz',work_dir+'TE_cluster_pca_data.npy')]
    else:
        # turn sam files into clustering matrix by scaffold
        repeat_analysis = 0
        if repeat_bed.endswith('.bed'):
            repeat_folder = work_dir + 'repeat_analysis/'
            repeat_analysis = 1
            repeat_windows = BedTool(repeat_bed)
        kmers = pickle.load(open(kmers_pickle,'rb'))
        with open(work_dir + 'windows.bed','r') as f:
            scaffolds = np.array([line.replace('\t','_') for line in f.read().splitlines() if line])
        pickle.dump(scaffolds, open(work_dir+'scaffolds_diff_kmer_analysis.p','wb'))
        windows = BedTool(work_dir + 'windows.bed')
        kmers_in_windows = []
        kmers_in_repeat_masked = []
        """for file in os.listdir(blast_path):
            if file.endswith('.sam'):
                #subprocess.call("sam2bed < %s | awk -v OFS='\\t' '{print $1, $2, $3, $4}' > %stemp.bed"%(blast_path+file, work_dir),shell=True)
                query = BedTool(work_dir+'temp.bed').sort()
                kmers_in_windows.append(windows.intersect(query,wa=True,wb=True).merge(c=7,o='collapse'))
                if repeat_analysis:
                    kmers_in_repeat_masked.append(repeat_windows.intersect(query,wa=True,wb=True))#.merge(c=7,o='collapse')
        kmers_in_windows[0].cat(*kmers_in_windows[1:],c=4,o='collapse').saveas(work_dir+'clustering.bed')"""
        subprocess.call("cat %s > %stemp.sam && sam2bed < %stemp.sam | awk -v OFS='\\t' '{print $1, $2, $3, $4}' > %stemp.bed"%(' '.join([blast_path+file for file in os.listdir(blast_path) if file.endswith('.sam')]), work_dir, work_dir, work_dir),shell=True)
        query = BedTool(work_dir+'temp.bed').sort()
        windows.intersect(query,wa=True,wb=True).merge(c=7,o='collapse',d=-1).saveas(work_dir+'clustering.bed')
        build_cluster_matrix = [(scaffolds,work_dir+'clustering.bed',work_dir+'diff_kmer_sparse_matrix.npz',work_dir+'transformed_diff_kmer_matrix.npy')]
        if repeat_analysis:
            #repeat_masked_kmers = kmers_in_repeat_masked[0].cat(*kmers_in_repeat_masked[1:],postmerge=False).sort()#,c=4,o='collapse'
            repeat_masked_kmers = repeat_windows.intersect(query,wa=True,wb=True).sort()
            print repeat_masked_kmers.head()
            kmer_repeat_masked = ''
            for line in str(repeat_masked_kmers).splitlines():
                if line:
                    lineList = line.strip('\n').split()
                    kmer_repeat_masked += '\t'.join(['_'.join(lineList[0:3]), '0', str(int(lineList[2]) - int(lineList[1])), lineList[-1]]) + '\n'
            kmer_repeat_masked = BedTool(kmer_repeat_masked,from_string=True).sort().merge(c=4, o='collapse').sort()
            print kmer_repeat_masked.head()
            bedText = []
            for line in str(kmer_repeat_masked).splitlines():
                if line:
                    lineList = line.strip('\n').split()
                    lineList2 = lineList[0].split('_')
                    lineList[1:-1] = map(lambda x: str(int(lineList2[-2])+ int(x.strip('\n'))), lineList[1:-1])
                    lineList[0] = '_'.join(lineList2[:-2])
                    bedText.append('\t'.join(lineList))
            BedTool('\n'.join(bedText),from_string=True).sort().saveas(repeat_folder+'clustering_repeats.bed')
            build_cluster_matrix.append((pickle.load(open(repeat_folder+'repeat_elements.p','rb')), repeat_folder+'clustering_repeats.bed',repeat_folder+'TE_sparse_matrix.npz',repeat_folder+'transformed_TE_matrix.npy'))
    kmer_index = {kmer: i for i, kmer in enumerate(kmers)}
    for scaffolds_new, clusterBed, output_sparse, output_positions in build_cluster_matrix:
        scaffolds_index = {scaffold : i for i, scaffold in enumerate(scaffolds_new)}
        data = sps.dok_matrix((len(scaffolds_new), len(kmers)),dtype=np.float32)
        with open(clusterBed, 'r') as f:
            """
            if clusterBed.endswith('clustering_repeats.bed'):
                for line in f:
                    if line:
                        try:
                            lineL = line.strip('\n').split('\t')
                            data[scaffolds_index['_'.join(lineL[0:3])], kmer_index[lineL[-1]]] += 1.
                        except:
                            pass
            else:
            """
            for line in f:
                if line:
                    listLine = line.rstrip('\n').split('\t')
                    if '_'.join(listLine[0:3]) in scaffolds_new:
                        counts = Counter(listLine[-1].split(','))
                        for key in counts:
                            try:
                                data[scaffolds_index['_'.join(listLine[0:3])], kmer_index[key]] = counts[key]
                            except:
                                pass
                    else: #FIXME test
                        print '_'.join(listLine[0:3])
        data = data.tocsc()
        sps.save_npz(output_sparse,data)
        data = data.tocsr()
        data = StandardScaler(with_mean=False, copy=False).fit_transform(data)
        try:
            if clusterBed.endswith('clustering_repeats.bed') == 0:
                transformed_data = KernelPCA(n_components=3,kernel=kernel, copy_X=False).fit_transform(data)
            else:
                transformed_data = TruncatedSVD(n_components=3).fit_transform(data)
            np.save(output_positions,transformed_data)
        except:
            pass
    del scaffolds_index, kmer_index

@click.pass_context
def estimate_phylogeny(ctx, work_dir, informative_diff_kmers_dict_pickle, informative_kmers_pickle, sparse_diff_kmer_matrix, kernel, n_neighbors_kmers, weights):
    # transpose matrix and estimate phylogeny
    kmer_graph_path = work_dir+'kmer_graph_outputs/'
    informative_diff_kmers = pickle.load(open(informative_diff_kmers_dict_pickle,'rb'))
    kmers = pickle.load(open(informative_kmers_pickle,'rb'))
    data = sps.load_npz(sparse_diff_kmer_matrix)
    try:
        os.makedirs(kmer_graph_path)
    except:
        pass
    kmer_reverse_lookup = defaultdict(list)
    for subgenome in informative_diff_kmers.keys():
        for kmer in informative_diff_kmers[subgenome]:
            kmer_reverse_lookup[kmer] = subgenome
    kmer_labels = np.vectorize(lambda x: kmer_reverse_lookup[x])(kmers)
    #kmer_class = {kmer_label: i for i,kmer_label in enumerate(set(kmer_labels))}
    #kmer_classes = np.vectorize(lambda x: kmer_class[x])(kmer_labels)
    pickle.dump(kmer_labels,open(work_dir+'diff_kmer_labels.p','wb'))
    kmer_matrix_transposed = data.transpose()
    kmer_pca = KernelPCA(n_components=3,kernel=kernel).fit_transform(StandardScaler(with_mean=False).fit_transform(kmer_matrix_transposed))
    np.save(work_dir+'transformed_diff_kmer_matrix_kmers.npy',kmer_pca)
    distance_matrix = pairwise_distances(kmer_pca,metric='euclidean') # change metric??
    distance_matrix = (distance_matrix + distance_matrix.T)/2
    #distance_matrix = pdist(kmer_pca)
    #print distance_matrix[distance_matrix != distance_matrix.T]
    np.save(work_dir+'kmer_pairwise_distances.npy',distance_matrix)
    nn_kmers = NearestNeighbors(n_neighbors=n_neighbors_kmers, metric = 'precomputed')
    nn_kmers.fit(kmer_pca)
    kmers_nn_graph = nn_kmers.kneighbors_graph(distance_matrix, mode = ('distance' if weights else 'connectivity'))
    sps.save_npz(work_dir+'kmers_nn_graph.npz',kmers_nn_graph)
    output_Dendrogram(work_dir+'kmer_pairwise_distances.npy', informative_kmers_pickle, kmer_graph_path)
    ctx.invoke(plotPositions, positions_npy=work_dir+'transformed_diff_kmer_matrix_kmers.npy', labels_pickle= informative_kmers_pickle, colors_pickle= work_dir+'diff_kmer_labels.p', output_fname=kmer_graph_path+'kmer_graph.html', graph_file= work_dir+'kmers_nn_graph.npz', layout= 'standard', iterations=25)
    # estimate phylogeny
    constructor = DistanceTreeConstructor()
    matrix = [row[:i+1] for i,row in enumerate(distance_matrix.tolist())]#[list(distance_matrix[i,0:i+1]) for i in range(distance_matrix.shape[0])]
    if len(set(kmers)) < len(kmers):
        new_kmer_names = []
        kmer_counter = defaultdict(lambda: 0)
        for kmer in kmers:
            kmer_counter[kmer]+=1
            if kmer_counter[kmer] > 1:
                new_kmer_names.append(kmer+'_'+str(kmer_counter[kmer]))
            else:
                new_kmer_names.append(kmer)
        kmers = new_kmer_names
    print kmers
    dm = _DistanceMatrix(names=kmers,matrix=matrix)
    tree = constructor.nj(dm)
    Phylo.write(tree,work_dir+'output_kmer_tree_by_scaffolds.nh','newick')

@click.pass_context
def jaccard_clustering(ctx, work_dir, sparse_diff_kmer_matrix, scaffolds_pickle, n_subgenomes, n_neighbors_scaffolds, weights):
    scaffolds = np.array(pickle.load(open(scaffolds_pickle,'rb')))
    data = sps.load_npz(sparse_diff_kmer_matrix)
    data.data[:] = 1
    data = data.toarray()
    nn_jaccard = NearestNeighbors(n_neighbors=n_neighbors_scaffolds,metric='jaccard')
    nn_jaccard.fit(data)
    jaccard_distance_NN_matrix = nn_jaccard.kneighbors_graph(data, mode = ('distance' if weights else 'connectivity'))
    sps.save_npz(work_dir+'jaccard_nn_graph.npz',jaccard_distance_NN_matrix)
    # FIXME Maybe use spectral clustering
    #agg_cluster = AgglomerativeClustering(n_clusters=n_subgenomes, linkage='average',affinity='precomputed', connectivity=jaccard_distance_NN_matrix)
    #agg_cluster.fit(jaccard_distance_NN_matrix.toarray())
    spec_cluster = SpectralClustering(n_clusters=n_subgenomes, affinity='precomputed')
    spec_cluster.fit(jaccard_distance_NN_matrix)
    try:
        os.makedirs(work_dir+'jaccard_clustering_results')
    except:
        pass
    labels = spec_cluster.labels_
    print len(scaffolds), len(labels)
    for label in set(labels):
        with open(work_dir+'jaccard_clustering_results/'+str(label)+'.txt','w') as f:
            f.write('\n'.join(list(scaffolds[labels==label])))
    cluster_labels = np.vectorize(lambda x: 'Subgenome %d'%x)(labels)
    pickle.dump(cluster_labels,open(work_dir+'jaccard_clustering_labels.p','wb'))
    ctx.invoke(plotPositions,positions_npy=work_dir+'transformed_diff_kmer_matrix.npy', labels_pickle=work_dir+'scaffolds_diff_kmer_analysis.p', colors_pickle=work_dir+'jaccard_clustering_labels.p', output_fname=work_dir+'jaccard_clustering_results/jaccard_plot.html', graph_file=work_dir+'jaccard_nn_graph.npz', layout='standard', iterations=25)

def TE_analysis(repeat_folder, TE_bed, output_subgenomes_bed, TE_sparse_matrix):
    import seaborn as sns
    # intersect TE's with subgenome labeled regions
    TE_bed = BedTool(TE_bed)
    subgenomes = BedTool(output_subgenomes_bed)
    subgenome_TE_bed = TE_bed.intersect(subgenomes, wa = True, wb = True)#.merge(c=7, o='distinct')
    ambiguous_TE_bed = TE_bed.intersect(subgenomes, v=True, wa = True)
    subgenome_bed_text = ''
    for line in str(subgenome_TE_bed).splitlines():
        if line:
            lineList = line.strip('\n').split()
            subgenome_bed_text += '\t'.join(['_'.join(lineList[0:3]), '0', str(int(lineList[2]) - int(lineList[1])), lineList[-1]]) + '\n'
    for line in str(ambiguous_TE_bed).splitlines():
        if line:
            lineList = line.strip('\n').split()
            subgenome_bed_text += '\t'.join(['_'.join(lineList[0:3]), '0', str(int(lineList[2]) - int(lineList[1])), 'ambiguous']) + '\n'
    subgenome_TE_bed = BedTool(subgenome_bed_text,from_string=True).sort().merge(c=4, o='distinct')
    TE_subgenomes = defaultdict(list)
    for line in str(subgenome_TE_bed).splitlines():
        if line:
            lineList = line.strip('\n').split()
            TE_subgenomes[lineList[0]] = (lineList[-1] if ',' not in lineList[-1] else 'ambiguous')
    TE_classes = pickle.load(open(repeat_folder + 'repeat_class_dictionary.p','rb'))

    TE_index = TE_classes.keys()
    data = sps.load_npz(TE_sparse_matrix)
    if 1:
        sum_kmer_counts = np.array(data.sum(axis=1))[:,0]
        print sum_kmer_counts
        plots= []
        for subclass in [0,1]:
            kmer_sums_TE_class = defaultdict(list)
            if subclass:
                for i in range(len(sum_kmer_counts)):
                    kmer_sums_TE_class[TE_classes[TE_index[i]]].append(sum_kmer_counts[i])
            else:
                for i in range(len(sum_kmer_counts)):
                    kmer_sums_TE_class[TE_classes[TE_index[i]].split('/')[0]].append(sum_kmer_counts[i])
            for TE_class in kmer_sums_TE_class:
                if type(kmer_sums_TE_class[TE_class]) != type(list):
                    kmer_sums_TE_class[TE_class] = sum(kmer_sums_TE_class[TE_class])
            plots.append(go.Bar(x=kmer_sums_TE_class.keys(),y=kmer_sums_TE_class.values(),name=('Subclasses' if subclass else 'Classes')))
            class_vs_subgenome = defaultdict(list)
            if subclass:
                 for TE in TE_classes:
                    class_vs_subgenome[TE_classes[TE]].append(TE_subgenomes[TE])
            else:
                for TE in TE_classes:
                    class_vs_subgenome[TE_classes[TE].split('/')[0]].append(TE_subgenomes[TE])
            for TE_class in class_vs_subgenome:
                if type(class_vs_subgenome[TE_class]) != type(list):
                    class_vs_subgenome[TE_class] = Counter(class_vs_subgenome[TE_class])
            df = pd.DataFrame(class_vs_subgenome)
            df.fillna(0, inplace=True)
            indep_test_results = chi2_contingency(df.as_matrix(), correction=True)
            df.to_csv((repeat_folder + 'TE_subclass_vs_subgenome.csv' if subclass else repeat_folder + 'TE_class_vs_subgenome.csv'))
            plt.figure(figsize=(13,10))
            sns_plot = sns.heatmap(df, annot=True)
            plt.title(r'TE %s v Intersected Subgenomes, p=%.2f, ${\chi}^2$=%.2f'%(('Subclasses' if subclass else 'Classes'),indep_test_results[1],indep_test_results[0]))
            plt.xlabel(('TE Subclasses' if subclass else 'TE Classes'))
            plt.ylabel('TE Subgenomes')
            plt.savefig(repeat_folder + ('TE_subclass_vs_subgenome.png' if subclass else 'TE_class_vs_subgenome.png'))
            traces = []
            for TE_class in class_vs_subgenome:
                 if type(class_vs_subgenome[TE_class]) != type(list):
                     traces.append(go.Bar(x=class_vs_subgenome[TE_class].keys(),y=class_vs_subgenome[TE_class].values(),name=TE_class))
            fig = go.Figure(data=traces,layout=go.Layout(barmode='group'))
            py.plot(fig,filename=repeat_folder+('TE_subclass_vs_subgenome.html' if subclass else 'TE_class_vs_subgenome.html'), auto_open=False)
        fig = go.Figure(data=plots,layout=go.Layout(barmode='group'))
        py.plot(fig, filename=repeat_folder+'Top_Differential_Kmer_Counts_By_Class.html', auto_open=False)

    subclasses = np.array(TE_classes.values())
    classes = np.vectorize(lambda x: x.split('/')[0])(subclasses)
    data = data.transpose()
    kmer_class_matrix = []
    for TE_class in set(classes):
        if TE_class != 'Unknown':
            kmer_class_matrix.append(np.array(data[:,classes == TE_class].sum(axis=1))[:,0]) # FIXME!!! and change if 0 back to normal
    print kmer_class_matrix

    classes = list(set(classes) - {'Unknown'})
    kmer_class_matrix = np.vstack(kmer_class_matrix).T
    print kmer_class_matrix
    kmer_classes = Counter(list(np.vectorize(lambda x: classes[x])(np.argmax(kmer_class_matrix,axis=1))))
    pickle.dump(kmer_classes,open(repeat_folder+'TE_kmer_classes.p','wb'))
    kmer_subclass_matrix = []
    for TE_class in set(subclasses):
        if TE_class != 'Unknown':
            kmer_subclass_matrix.append(np.array(data[:,subclasses == TE_class].sum(axis=1))[:,0])
    subclasses = list(set(subclasses) - {'Unknown'})
    kmer_subclass_matrix = np.vstack(kmer_subclass_matrix).T
    kmer_subclasses = Counter(list(np.vectorize(lambda x: subclasses[x])(np.argmax(kmer_subclass_matrix,axis=1))))
    pickle.dump(kmer_classes,open(repeat_folder+'TE_kmer_subclasses.p','wb'))
    plots = []
    for kmer_counts, label in [(kmer_classes,'Classes'),(kmer_subclasses,'Subclasses')]:
        plots.append(go.Bar(x = kmer_counts.keys(),y = kmer_counts.values(), name=label))
    fig = go.Figure(data=plots,layout=go.Layout(barmode='group'))
    py.plot(fig, filename=repeat_folder+'Differential_Kmers_By_Class.html', auto_open=False)
    # FIXME finish!!! ^^^^ can identify individual kmers that belong to each class

    #ctx.invoke(plotPositions,positions_npy=work_dir+'transformed_diff_kmer_matrix.npy', labels_pickle=work_dir+'scaffolds_diff_kmer_analysis.p', colors_pickle=work_dir+'jaccard_clustering_labels.p', output_fname=work_dir+'jaccard_clustering_results/jaccard_plot.html', graph_file=work_dir+'jaccard_nn_graph.npz', layout='positions', iterations=25)

@polycracker.command()
@click.option('-w', '--work_dir', default='./diff_kmer_distances/', show_default=True, help='Work directory where computations for differential kmer analysis is done.', type=click.Path(exists=False))
@click.option('-go', '--original_genome', help='Full path to original polyploid fasta, prechunked.', type=click.Path(exists=False))
def avg_distance_between_diff_kmers(work_dir, original_genome):
    """Report the average distance between iterations of unique differential kmers over any scaffold."""
    import seaborn as sns
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')
    blast_path = work_dir + 'blast_files/'
    bed_path = work_dir + 'bed_alt_files/'
    output_path = work_dir+'outputs_distances/'
    if 1: #FIXME test
        for dir in [work_dir, blast_path, bed_path,output_path]:
            try:
                os.makedirs(dir)
            except:
                pass
    blast2bed3(work_dir, blast_path, bed_path, output_path, original_genome, 1, bedgraph=0, out_kmers = 1)
    subprocess.call('cat %s | bedtools sort > %s'%(' '.join([bed_path+file for file in os.listdir(bed_path) if file.endswith('.bed3')]),work_dir+'diff_kmer_locations.bed'),shell=True)
    fai_file = original_genome+'.fai'
    with open(fai_file,'r') as f:
        distance_dict = {line.split()[0]:defaultdict(list) for line in f}
    with open(work_dir+'diff_kmer_locations.bed','r') as f:
        for line in f:
            ll = line.split()
            distance_dict[ll[0]][ll[-1].strip('\n')].append(int(ll[1]))
    kmer_avg_distances = defaultdict(list)
    for chrom in distance_dict:
        for kmer in distance_dict[chrom].keys():
            if len(distance_dict[chrom][kmer]) >= 2:
                kmer_avg_distances[kmer].extend(np.diff(sorted(distance_dict[chrom][kmer])).tolist())
                del distance_dict[chrom][kmer]
            else:
                del distance_dict[chrom][kmer]
    for kmer in kmer_avg_distances.keys():
        kmer_avg_distances[kmer] = np.mean(kmer_avg_distances[kmer])
    np.save(output_path+'Average_Top_Kmer_Distance.npy',np.array(stats(kmer_avg_distances.values())))
    plt.figure()
    sns.distplot(kmer_avg_distances.values(),kde=False)
    plt.title(' Average Distance Between Particular Top Differential Kmer')
    plt.xlabel('Average Distance Between Particular Top Differential Kmer')
    plt.ylabel('Count')
    plt.savefig(output_path+'Average_Top_Kmer_Distance.png',dpi=300)

@polycracker.command()
@click.option('-w', '--work_dir', default='./diff_kmer_analysis/', show_default=True, help='Work directory where computations for differential kmer analysis is done.', type=click.Path(exists=False))
@click.option('-npz', '--sparse_kmer_matrix', default='clusteringMatrix.npz', help='Original sparse kmer matrix produced from generate_Kmer_Matrix', show_default=True, type=click.Path(exists=False))
@click.option('-p', '--final_output_label_pickle', help='Pickle generated from bootstrap results from subgenomeExtraction. May need to run convert_subgenome_output_to_pickle.', type=click.Path(exists=False))
@click.option('-b', '--final_output_label_bed', help='Bed generated from bootstrap results from subgenomeExtraction. May need to run generate_out_bed.', type=click.Path(exists=False))
@click.option('-s', '--scaffolds_pickle', default='scaffolds.p', help='Scaffolds pickle produced from generate_Kmer_Matrix.', show_default=True, type=click.Path(exists=False))
@click.option('-kp', '--kmers_pickle', default='kmers.p', help='Kmers pickle produced from generate_Kmer_Matrix.', show_default=True, type=click.Path(exists=False))
@click.option('-min', '--min_number_diff_kmers', default=100, help='Minimum number of differential kmers from each subgenome.', show_default=True)
@click.option('-dd', '--diff_kmers_directory', help='Directory containing differential kmers from subgenomeExtraction bootstrap', show_default=True, type=click.Path(exists=False))
@click.option('-go', '--original_genome', help='Filename of original polyploid fasta, prechunked.', type=click.Path(exists=False))
@click.option('-fp', '--fasta_path', default='./fasta_files/', help='Path to original polyploid fasta, prechunked.', type=click.Path(exists=False))
@click.option('-m', '--blast_mem', default='100', help='Amount of memory to use for bbtools run. More memory will speed up processing.', show_default=True)
@click.option('-sl', '--split_length', default=75000, help='Length of intervals in bedgraph files.', show_default=True)
@click.option('-n', '--n_chromosomes', default=10, help='Output unionbed plots of x largest chromosomes.', show_default=True)
@click.option('-s', '--n_subgenomes', default = 2, help='Number of subgenomes for Jaccard clustering.', show_default=True)
@click.option('-nns', '--n_neighbors_scaffolds', default=25, help='Number of nearest neighbors to use when generating nearest neighbor graph with scaffolds as datapoints.', show_default=True)
@click.option('-nnk', '--n_neighbors_kmers', default=15, help='Number of nearest neighbors to use when generating nearest neighbor graph with kmers as datapoints.', show_default=True)
@click.option('-k', '--kernel', default='cosine', help='Kernel for KPCA. Cosine is particularly effective.', type=click.Choice(['linear','poly','rbf','sigmoid','cosine']), show_default=True)
@click.option('-wnn', '--weights', default=0, help='Whether to weight k_neighbors graph for jaccard clustering and kmer graphs.', show_default=True)
@click.option('-r', '--repeat_masked_gff', default='xxx', help='Repeatmasked gff file, in gff or gff3 format. Used for intersecting kmer results with Transposable Elements to find TE classes for kmers and other analyses.', type=click.Path(exists=False))
@click.option('-ndb', '--no_diff_blast', 'no_run_diff', is_flag=True, help='Flag to not run earlier part of differential kmer analysis. Saves time if already done.' )
@click.option('-ns', '--no_sam2matrix', is_flag=True, help='Flag, if on, does not convert sam files into a clustering matrix.')
@click.option('-np', '--no_run_phylogeny', 'no_phylogeny', is_flag=True, help='Flag, if on, does not run phylogeny analysis')
@click.option('-nj', '--no_jaccard_clustering', 'no_jaccard', is_flag=True, help='Flag, if on, does not run jaccard clustering')
@click.pass_context
def diff_kmer_analysis(ctx, work_dir, sparse_kmer_matrix, final_output_label_pickle, final_output_label_bed, scaffolds_pickle, kmers_pickle, min_number_diff_kmers, diff_kmers_directory, original_genome, fasta_path, blast_mem, split_length, n_chromosomes, n_subgenomes, n_neighbors_scaffolds, n_neighbors_kmers, kernel, weights, repeat_masked_gff, no_run_diff, no_sam2matrix, no_phylogeny, no_jaccard):
    """Runs robust differential kmer analysis pipeline. Find highly informative differential kmers, subset of differential kmers found via polyCRACKER,
    generate a matrix of highly informative differential kmer counts versus scaffolds, generate a network graph linking the kmers,
    estimate phylogeny from these kmers, perform clustering using this matrix via a jaccard statistic, and look at the intersection between these kmers and identified repeats."""
    if work_dir.endswith('/') == 0:
        work_dir += '/'
    blast_path = work_dir + 'blast_files/'
    bed_path = work_dir + 'bed_files/'
    sort_path = work_dir + 'sorted_files/'
    output_images = work_dir + 'unionbed_plots/'
    repeat_path = work_dir + 'repeat_analysis/'
    if 1: #FIXME test
        for dir in [work_dir, blast_path, bed_path, sort_path, output_images, repeat_path]:
            try:
                os.makedirs(dir)
            except:
                pass
        # generate dictionaries containing differential kmers
        diff_kmers = defaultdict(list)
        for file in os.listdir(diff_kmers_directory):
            if file.endswith('.higher.kmers.fa'):
                with open(diff_kmers_directory+'/'+file,'r') as f:
                    diff_kmers[file[file.find('_')+1:file.find('.')]] = f.read().splitlines()[1::2]
        # generate labels for kbest selection
        output_labels = pickle.load(open(final_output_label_pickle,'rb'))
        sparse_kmer_matrix = sps.load_npz(sparse_kmer_matrix)
        labels_dict = {label:i for i, label in enumerate(set(output_labels) - {'ambiguous'})}
        sparse_kmer_matrix = sparse_kmer_matrix[output_labels != 'ambiguous']
        encoded_labels = np.vectorize(lambda x: labels_dict[x])(output_labels[output_labels != 'ambiguous'])
        # load all kmers
        kmers = pickle.load(open(kmers_pickle,'rb'))
        # run kbest to score the kmers
        kbest = SelectKBest(chi2,'all')
        kbest.fit(sparse_kmer_matrix,encoded_labels)
        kmers_ordered = np.array(kmers)[kbest.pvalues_.argsort()]
        # find informative differential kmers
        informative_diff_kmers = defaultdict(list)
        for subgenome in diff_kmers:
            if np.mean(np.vectorize(len)(diff_kmers[subgenome])) != np.mean(np.vectorize(len)(kmers_ordered)):
                print 'Not the same length of kmers between initial scaffolding and subgenome Extraction. The kmer sets must have matching lengths'
                quit()
            informative_diff_kmers[subgenome] = [kmer for kmer in kmers_ordered if kmer in diff_kmers[subgenome]][:min_number_diff_kmers]
        pickle.dump(informative_diff_kmers, open(work_dir+'informative_diff_kmers_dict.p','wb'))
        kmers = list(itertools.chain.from_iterable(informative_diff_kmers.values()))
        pickle.dump(kmers, open(work_dir+'informative_diff_kmers_list.p','wb'))

    repeat_bed = repeatGFF2Bed(repeat_masked_gff, repeat_path)

    if no_run_diff == 0:
        kmer_dir = write_informative_diff_kmers(informative_diff_kmers, work_dir)
        writeBlast(original_genome, blast_path, kmer_dir, fasta_path, 1, blast_mem)
        blast2bed3(work_dir, blast_path, bed_path, sort_path, original_genome, 1, bedgraph=0)
        ctx.invoke(generate_unionbed, bed3_directory=bed_path, original=1, split_length=split_length, fai_file=fasta_path+original_genome+'.fai', work_folder=work_dir)
        ctx.invoke(plot_unionbed,unionbed_file=work_dir+'subgenomes.union.bedgraph', number_chromosomes=n_chromosomes, out_folder=output_images)


    # intersect bed3 files with repeat density and generate matrix, feature labels are types of transposons, clustering matrix by known repeat regions
    # turn repeat density into list of scaffolds and corresponding list of features
    if no_sam2matrix == 0:
        sam2diffkmer_clusteringmatrix(work_dir,work_dir+'informative_diff_kmers_list.p',blast_path,kernel, repeat_bed)
    if no_phylogeny == 0:
        estimate_phylogeny(work_dir, work_dir+'informative_diff_kmers_dict.p', work_dir+'informative_diff_kmers_list.p', work_dir+'diff_kmer_sparse_matrix.npz', kernel, n_neighbors_kmers, weights)
    # convert to binary and output binary matrix for jaccard clustering
    if no_jaccard == 0:
        jaccard_clustering(work_dir, work_dir+'diff_kmer_sparse_matrix.npz', work_dir+'scaffolds_diff_kmer_analysis.p', n_subgenomes, n_neighbors_scaffolds, weights)
    if repeat_bed.endswith('.bed'):
        TE_analysis(repeat_path, repeat_bed, final_output_label_bed, repeat_path+'TE_sparse_matrix.npz')


@polycracker.command(name='TE_Cluster_Analysis')
@click.option('-w', '--work_dir', help='Work directory where computations for TE clustering is done.', type=click.Path(exists=False))
@click.option('-rg', '--repeat_gff', help='Full path to repeat TE gff file, output from repeat masker pipeline.', type=click.Path(exists=False))
@click.option('-rp', '--repeat_pickle', help='Full path to repeat TE pickle file, containing TE names, which will be generated in this pipeline.', type=click.Path(exists=False))
@click.option('-sl', '--split_length', default=75000, help='Length of intervals in bedgraph files.', show_default=True)
@click.option('-n', '--n_chromosomes', default=10, help='Output unionbed plots of x largest chromosomes.', show_default=True)
@click.option('-s', '--n_clusters', default = 2, help='Number of clusters for clustering TEs.', show_default=True)
@click.option('-d', '--n_dimensions', default=3, help='Number of dimensions to reduce to.', show_default=True)
@click.option('-k', '--kernel', default='cosine', help='Kernel for KPCA. Cosine is particularly effective.', type=click.Choice(['linear','poly','rbf','sigmoid','cosine']), show_default=True)
@click.option('-m', '--blast_mem', default='100', help='Amount of memory to use for bbtools run. More memory will speed up processing.', show_default=True)
@click.option('-nt', '--n_top_repeats', default=100, help='Number of top TEs in each subgenome to analyze.', show_default=True)
@click.option('-fai', '--fai_file', help='Full path to original, nonchunked fai file.', type=click.Path(exists=False))
@click.option('-dv', '--default_repeat_val', default=2, help='Default value for number of times TE appears in subgenome if value is 0.', show_default=True)
@click.option('-dt', '--diff_repeat_threshold', default=20, help='Threshold specifying that if one TE is differential in one subgenome versus others label that TE by that subgenome.', show_default=True)
@click.option('-bo','--original_subgenomes_bed', default = '', help='Full path to original bed file containing subgenome labelling. Will use this to label TEs by subgenome instead of clustering. Leave blank if deciding labels via clustering.', type=click.Path(exists=False))
@click.pass_context
def TE_Cluster_Analysis(ctx, work_dir, repeat_gff, repeat_pickle, split_length, n_chromosomes, n_clusters, n_dimensions, kernel, blast_mem, n_top_repeats, fai_file,default_repeat_val,diff_repeat_threshold, original_subgenomes_bed):
    """Build clustering matrix (repeat counts vs scaffolds) from repeats and conduct analyses on repeats instead of kmers."""
    if 1:
        if work_dir.endswith('/') == 0:
            work_dir += '/'
        bed_path = work_dir + 'bed3_files/'
        union_path = work_dir + 'unionbed_images/'
        for dir in [work_dir, bed_path, union_path]:
            try:
                os.makedirs(dir)
            except:
                pass
        #subprocess.call("awk '{print $1}' %s > %s/formatted_repeats.fa"%(repeat_fasta, work_dir), shell=True)
        # FIXME ADD ARGUMENTS BELOW
        repeatGFF2Bed(repeat_gff, work_dir, 1)
        with open(work_dir+'repeats.bed','r') as f, open(bed_path+'repeats.bed','w') as f2:
            for line in f:
                lineList = line.split()[0:2]
                f2.write('\t'.join([lineList[0],lineList[1],str(int(lineList[1])+1)])+'\n')
        ctx.invoke(generate_unionbed, bed3_directory=bed_path, original=1, split_length=split_length, fai_file=fai_file, work_folder=work_dir)
        ctx.invoke(plot_unionbed, unionbed_file=work_dir+'subgenomes.union.bedgraph', number_chromosomes=n_chromosomes, out_folder=union_path)
        sam2diffkmer_clusteringmatrix(work_dir,work_dir+'TE_motif_subclass.p',work_dir,kernel, work_dir+'repeats.bed', 1)
    scaffolds_pickle = work_dir+'scaffolds_TE_cluster_analysis.p'
    clustering_matrix = sps.load_npz(work_dir+'TEclusteringMatrix.npz')
    if original_subgenomes_bed:
        label_new_windows(work_dir, work_dir+'windows.bed' , original_subgenomes_bed)
        out_labels = pickle.load(open(work_dir+'new_labels.p','rb'))
        labels_dict = {label:i for i, label in enumerate(sorted(set(out_labels) - {'ambiguous'}))} #FIXME swapping names on accident
        #ctx.invoke(plotPositions,positions_npy=work_dir+'TE_pca.npy', labels_pickle=scaffolds_pickle, colors_pickle=work_dir+'new_labels.p', output_fname=work_dir+'TE_pca_clusters.html', graph_file='xxx', layout='standard', iterations=0)
    else:
        TE_pca = Pipeline([('ss',StandardScaler(with_mean=False)),('kpca',KernelPCA(n_components=n_dimensions, kernel = kernel))]).fit_transform(clustering_matrix)
        np.save(work_dir+'TE_pca.npy', TE_pca)
        ctx.invoke(plotPositions,positions_npy=work_dir+'TE_pca.npy', labels_pickle=scaffolds_pickle, colors_pickle='xxx', output_fname=work_dir+'TE_pca.html', graph_file='xxx', layout='standard', iterations=0)
        bgm = BayesianGaussianMixture(n_components=n_clusters)
        bgm.fit(TE_pca)
        labels = bgm.predict(TE_pca)
        pickle.dump(np.vectorize(lambda x: 'Subgenome_%d'%x)(labels),open(work_dir+'TE_subgenome_labels.p','wb'))
        ctx.invoke(plotPositions,positions_npy=work_dir+'TE_pca.npy', labels_pickle=scaffolds_pickle, colors_pickle=work_dir+'TE_subgenome_labels.p', output_fname=work_dir+'TE_pca_clusters.html', graph_file='xxx', layout='standard', iterations=0)

    # load all kmers
    TEs = np.array(pickle.load(open(work_dir+'TE_motif_subclass.p','rb')))
    # run kbest to score the kmers
    kbest = SelectKBest(chi2,'all')
    cm = clustering_matrix
    if original_subgenomes_bed:
        print clustering_matrix.shape
        clustering_matrix = clustering_matrix[out_labels != 'ambiguous']
        labels = np.vectorize(lambda x: labels_dict[x])(out_labels[out_labels != 'ambiguous'])
    kbest.fit(clustering_matrix,labels)
    TEs_ordered = TEs[kbest.pvalues_.argsort()]
    print clustering_matrix.shape
    clustering_matrix = clustering_matrix.transpose()
    subgenomes = ['Subgenome %d'%x for x in sorted(set(labels))]
    TE_subgenome_matrix = []
    for subgenome in set(labels):
        TE_subgenome_matrix.append(np.vectorize(lambda x: x if x else default_repeat_val)(np.array(clustering_matrix[:,labels == subgenome].sum(axis=1))[:,0]))
    TE_subgenome_matrix = np.vstack(TE_subgenome_matrix).T
    #print TE_subgenome_matrix
    #TE_max = np.argmax(TE_subgenome_matrix,axis=1)
    row_function = lambda row: subgenomes[np.argmax(row)] if (row[row!=np.max(row)] and np.all(np.vectorize(lambda x: np.float(np.max(row))/x >= diff_repeat_threshold)(row[row != np.max(row)]))) else 'ambiguous'
    #TE_subgenomes = np.vectorize(lambda x: subgenomes[x])(TE_max)
    #TE_subgenomes = np.apply_along_axis(row_function,1,TE_subgenome_matrix)
    TE_subgenomes = np.array([row_function(row) for row in TE_subgenome_matrix])
    print 'unambiguous=',len(TE_subgenomes[TE_subgenomes != 'ambiguous'])
    TE_subgenome_dict = {subgenome: [TE for TE in TEs_ordered if TE in list(TEs[TE_subgenomes == subgenome])][:n_top_repeats] for subgenome in subgenomes if list(TEs[TE_subgenomes == subgenome])}
    #print TE_subgenome_dict
    TEs_ordered = list(itertools.chain.from_iterable(TE_subgenome_dict.values()))
    #print TEs_ordered
    TE_bool = np.vectorize(lambda TE: TE in TEs_ordered)(TEs)
    TE_subgenome_matrix = np.hstack((TEs[TE_bool][:,None],TE_subgenome_matrix[TE_bool]))
    np.save(work_dir+'subgenome_differential_top_TEs.npy',TE_subgenome_matrix)
    pd.DataFrame(TE_subgenome_matrix,columns=(['TEs']+subgenomes)).to_csv('subgenome_differential_top_TEs.csv',index=False)

    pickle.dump(TE_subgenome_dict, open(work_dir+'informative_subgenome_TE_dict.p','wb'))
    pickle.dump(TEs_ordered, open(work_dir+'informative_subgenome_TE_list.p','wb'))
    if 1:#FIXME RIGHT HERE!! UNDER DEVELOPMENT
        print clustering_matrix.T.shape
        TE_diff_sparse_matrix = cm.T[np.vectorize(lambda TE: TE in TEs_ordered)(TEs)]
        print TE_diff_sparse_matrix.T.shape
        TE_pca = Pipeline([('ss',StandardScaler(with_mean=False)),('kpca',KernelPCA(n_components=n_dimensions, kernel = kernel))]).fit_transform(TE_diff_sparse_matrix.transpose())
        print TE_pca.shape
        np.save(work_dir+'top_TE_pca.npy', TE_pca)
        ctx.invoke(plotPositions,positions_npy=work_dir+'top_TE_pca.npy', labels_pickle=scaffolds_pickle, colors_pickle='xxx', output_fname=work_dir+'top_TE_pca.html', graph_file='xxx', layout='standard', iterations=0)
        bgm = BayesianGaussianMixture(n_components=n_clusters)
        bgm.fit(TE_pca)
        labels = bgm.predict(TE_pca)
        print labels.shape
        pickle.dump(np.vectorize(lambda x: 'Subgenome_%d'%x)(labels),open(work_dir+'top_TE_subgenome_labels.p','wb'))
        ctx.invoke(plotPositions,positions_npy=work_dir+'top_TE_pca.npy', labels_pickle=scaffolds_pickle, colors_pickle=work_dir+'top_TE_subgenome_labels.p', output_fname=work_dir+'top_TE_pca_clusters.html', graph_file='xxx', layout='standard', iterations=0)
        sps.save_npz(work_dir+'TE_diff_subgenomes_matrix.npz', TE_diff_sparse_matrix.transpose()) #FIXME RIGHT HERE!!

        ctx.invoke(estimate_phylogeny, work_dir=work_dir, informative_diff_kmers_dict_pickle=work_dir+'informative_subgenome_TE_dict.p', informative_kmers_pickle=work_dir+'informative_subgenome_TE_list.p', sparse_diff_kmer_matrix=work_dir+'TE_diff_subgenomes_matrix.npz', kernel=kernel, n_neighbors_kmers=15, weights=0) #FIXME RIGHT HERE!!

    try:
        TEs_counter = pickle.load(open(work_dir+'TE_motif_subclass_counter.p','rb'))
        top_TEs_counter = {}
        for TE in TEs_ordered:
            top_TEs_counter[TE] = TEs_counter[TE]
        TE_subclasses = np.vectorize(lambda x: x.split('#')[1])(TEs_ordered)
        TE_classes = np.vectorize(lambda x: x.split('/')[0])(TE_subclasses)
        TE_counts = np.vectorize(lambda x: top_TEs_counter[x])(TEs_ordered)
        n_TEs_subclass = Counter(TE_subclasses)
        n_TEs_class = Counter(TE_classes)
        TE_subclasses = {subclass:sum(TE_counts[TE_subclasses==subclass]) for subclass in set(TE_subclasses)}#Counter(TE_subclasses)
        TE_classes = {upper_class:sum(TE_counts[TE_classes==upper_class]) for upper_class in set(TE_classes)}#Counter(TE_classes)
        for class_name, class_dict in [('Class',TE_classes),('Subclasses',TE_subclasses)]:
            plots = []
            plots.append(go.Bar(x = class_dict.keys(),y = class_dict.values(), name=class_name))
            fig = go.Figure(data=plots,layout=go.Layout(barmode='group'))
            py.plot(fig, filename=work_dir+'TotalCounts_Top_TEs_By_%s.html'%(class_name), auto_open=False)
        for class_name, class_dict in [('Class',n_TEs_class),('Subclasses',n_TEs_subclass)]:
            plots = []
            plots.append(go.Bar(x = class_dict.keys(),y = class_dict.values(), name=class_name))
            fig = go.Figure(data=plots,layout=go.Layout(barmode='group'))
            py.plot(fig, filename=work_dir+'Top_TEs_By_%s.html'%(class_name), auto_open=False)
    except:
        print "Memory usage high. Will try to fix in later edition. Decrease number of top kmers."


@polycracker.command(name='subgenome_extraction_via_repeats')
@click.pass_context
@click.option('-w', '--work_dir', default='./repeat_subgenome_extraction/', show_default=True, help='Work directory for computations of repeat supplied subgenome extraction.', type=click.Path(exists=False))
@click.option('-rc', '--repeat_cluster_analysis_dir', default='./TE_cluster_analysis/', show_default=True, help='Work directory where computations for initial TE clustering was done.', type=click.Path(exists=False))
@click.option('-cm', '--clustering_matrix', default='./TE_cluster_analysis/TEclusteringMatrix.npz', show_default=True, help='Repeats vs scaffolds matrix identified by TE_cluster_analysis.', type=click.Path(exists=False))
@click.option('-s','--scaffolds_pickle', default='./TE_cluster_analysis/scaffolds_TE_cluster_analysis.p', show_default=True, help='Pickle file containing the scaffold names from TE_cluster_analysis.',  type=click.Path(exists=False))
@click.option('-sl','--subgenome_labels_by_kmer_analysis', default = './diff_kmer_analysis/subgenomes.bed', show_default=True, help='Full path to original bed file containing subgenome labelling from polyCRACKER. Will use this to label TEs by subgenome instead of initial clustering. MANDATORY until future development.', type=click.Path(exists=False))
@click.option('-a','--all', is_flag=True, help='Grab all clusters.')
@click.option('-dv', '--default_repeat_val', default=1, help='Default value for number of times TE appears in subgenome if value is 0.', show_default=True)
@click.option('-dt', '--diff_repeat_threshold', default=15, help='Threshold specifying that if one TE is differential in one subgenome versus others label that TE by that subgenome.', show_default=True)
@click.option('-ds', '--differential_sum_ratio', default=7, help='Indicates that if the counts of all repeats in a particular region in any other subgenomes are 0, then the total count in a subgenome must be more than this much be binned as that subgenome.', show_default=True)
@click.option('-dc', '--default_total_count', default=2, help='Indicates that if any of the other subgenome kmer counts for all kmers in a region are greater than 0, then the counts on this subgenome divided by any of the other counts must surpass a value to be binned as that subgenome.', show_default=True)
@click.option('-k', '--kernel', default='cosine', help='Kernel for KPCA. Cosine is particularly effective.', type=click.Choice(['linear','poly','rbf','sigmoid','cosine']), show_default=True)
@click.option('-m', '--metric', default='cosine', help='Distance metric used to compute affinity matrix, used to find nearest neighbors graph for spectral clustering.', type=click.Choice(['cityblock','cosine','euclidean','l1','l2','manhattan','braycurtis','canberra','chebyshev','correlation','dice','hamming','jaccard','kulsinski','mahalanobis','matching','minkowski','rogerstanimoto','russellrao','seuclidean','sokalmichener','sokalsneath','sqeuclidean','yule']), show_default=True)
@click.option('-d', '--n_dimensions', default=3, help='Number of dimensions to reduce to.', show_default=True)
@click.option('-ns', '--n_subgenomes', default = 2, help='Number of subgenomes', show_default=True)
@click.option('-i', '--iterations', default = 3, help='Number of iterations for subgenome extraction bootstrapping.', show_default=True)
@click.option('-nn', '--n_neighbors', default=25, help='Number of nearest neighbors in generation of nearest neighbor graph.', show_default=True)
@click.option('-nt', '--n_top_repeats', default=100, help='Number of top TEs in each subgenome to analyze.', show_default=True)
@click.option('-rf', '--reference_fasta', default='', help='Full path to reference chunked fasta file containing scaffold names.', type=click.Path(exists=False))
def subgenome_extraction_via_repeats(ctx,work_dir, repeat_cluster_analysis_dir, clustering_matrix, scaffolds_pickle, subgenome_labels_by_kmer_analysis, all, default_repeat_val, diff_repeat_threshold, differential_sum_ratio, default_total_count, kernel, metric, n_dimensions, n_subgenomes, iterations, n_neighbors, n_top_repeats, reference_fasta):
    """Extends results of TE_cluster_analysis by performing subgenome extraction via matrix methods. Requires as input the found clustering matrix
    as identified via TE_cluster_analysis, and the subgenome labels from a polyCRACKER run output bed file."""
    import glob
    import matplotlib.pyplot as plt
    import seaborn as sns

    #from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    work_dir += '/'
    repeat_cluster_analysis_dir += '/'
    try:
        os.makedirs(work_dir)
    except:
        pass
    clustering_matrix = sps.load_npz(clustering_matrix)
    scaffolds = pickle.load(open(scaffolds_pickle))
    scaffold_len = lambda scaffold: int(scaffold.split('_')[-1])-int(scaffold.split('_')[-2])
    weights = np.vectorize(scaffold_len)(scaffolds)
    kbest = SelectKBest(chi2,'all')
    cm = clustering_matrix
    TEs = np.arange(cm.shape[1])
    label_new_windows(work_dir, repeat_cluster_analysis_dir+'windows.bed' , subgenome_labels_by_kmer_analysis)
    out_labels = pickle.load(open(work_dir+'new_labels.p','rb'))
    labels_dict = {label:i for i, label in enumerate(sorted(set(out_labels) - {'ambiguous'}))}
    clustering_matrix = clustering_matrix[out_labels != 'ambiguous']
    labels = np.vectorize(lambda x: labels_dict[x])(out_labels[out_labels != 'ambiguous'])
    kbest.fit(clustering_matrix,labels)
    TEs_ordered = TEs[kbest.pvalues_.argsort()]
    clustering_matrix = clustering_matrix.transpose()
    subgenomes = ['Subgenome %d'%x for x in sorted(set(labels))]
    row_function = lambda row: subgenomes[np.argmax(row)] if (row[row!=np.max(row)] and np.all(np.vectorize(lambda x: np.float(np.max(row))/x >= diff_repeat_threshold)(row[row != np.max(row)]))) else 'ambiguous'

    if 0:
        TE_subgenome_matrix = []
        for subgenome in set(labels):
            TE_subgenome_matrix.append(np.vectorize(lambda x: x if x else default_repeat_val)(np.array(clustering_matrix[:,labels == subgenome].sum(axis=1))[:,0]))
        TE_subgenome_matrix = np.vstack(TE_subgenome_matrix).T
        TE_subgenomes = np.array([row_function(row) for row in TE_subgenome_matrix])
        TE_subgenome_dict = {subgenome: [TE for TE in TEs_ordered if TE in list(TEs[TE_subgenomes == subgenome])][:n_top_repeats] for subgenome in subgenomes if list(TEs[TE_subgenomes == subgenome])}
        TEs_ordered = list(itertools.chain.from_iterable(TE_subgenome_dict.values()))
        #print TEs_ordered
        TE_bool = np.vectorize(lambda TE: TE in TEs_ordered)(TEs)
        TE_subgenome_matrix = np.hstack((TEs[TE_bool][:,None],TE_subgenome_matrix[TE_bool]))
        TE_diff_sparse_matrix = cm.T[np.vectorize(lambda TE: TE in TEs_ordered)(TEs)]
        TE_diff_sparse_matrix_T = TE_diff_sparse_matrix.transpose()
        #OSVM = OneClassSVM()
        #OSVM.fit(TE_diff_sparse_matrix_T,sample_weight=weights)
        #inliers_outliers = OSVM.predict(TE_diff_sparse_matrix_T)
        #inliers = inliers_outliers == 1

        #encoded_labels = LabelEncoder().fit_transform(out_labels) StandardScaler(with_mean=False)
        TE_pca = Pipeline([('ss',StandardScaler(with_mean=False)),('kpca',KernelPCA(n_components=n_dimensions,kernel=kernel))]).fit_transform(TE_diff_sparse_matrix_T)#TfidfTransformer(),('tsne',TSNE(n_components=n_dimensions,n_jobs=8)).todense(),encoded_labels)# ('lda', LinearDiscriminantAnalysis(n_components=n_dimensions + 1)) lda based on number of classes fixme go back to kpca,('kpca',KernelPCA(n_components=n_dimensions, kernel = kernel))]).fit_transform(TE_diff_sparse_matrix.transpose()) # 25 ('tsne',TSNE(n_components=n_dimensions,n_jobs=8,metric=kernel if kernel == 'cosine' else 'euclidean',learning_rate=200,perplexity=50,angle=0.5)))#,('kpca',KernelPCA(n_components=n_dimensions, kernel = kernel))]).fit_transform(TE_diff_sparse_matrix.transpose()) # 25 ('tsne',TSNE(n_components=n_dimensions,n_jobs=8,metric=kernel if kernel == 'cosine' else 'euclidean',learning_rate=200,perplexity=50,angle=0.5))
        np.save(work_dir+'TE_pca.npy',TE_pca)
    TE_pca = np.load(work_dir+'TE_pca.npy')
    #TE_pca = TSNE(n_components=3,n_jobs=8).fit_transform(TE_pca)
    #np.save(work_dir+'TE_tsne.npy',TE_pca)
    ctx.invoke(plotPositions,positions_npy=work_dir+'TE_pca.npy', labels_pickle=scaffolds_pickle, colors_pickle=work_dir+'new_labels.p', output_fname=work_dir+'top_TE_pca_polycracker.html', graph_file='xxx', layout='standard', iterations=0)
    #pairwise = pairwise_distances(TE_pca,metric=metric)
    neigh = NearestNeighbors(n_neighbors=n_neighbors, algorithm = 'auto', metric=metric)
    neigh.fit(TE_pca)
    nn_graph = neigh.kneighbors_graph(TE_pca, mode = 'connectivity')
    while sps.csgraph.connected_components(nn_graph)[0] > 1:
        print(n_neighbors, sps.csgraph.connected_components(nn_graph)[0])
        n_neighbors += 5
        neigh = NearestNeighbors(n_neighbors=n_neighbors, algorithm = 'auto', metric=metric)
        neigh.fit(TE_pca)
        nn_graph = neigh.kneighbors_graph(TE_pca, mode = 'connectivity')
    sps.save_npz(work_dir+'repeats_nn_graph.npz',nn_graph)
    fit_data = nn_graph

    """
    fit_data = nn_graph + sps.csgraph.minimum_spanning_tree(_fix_connectivity(TE_pca, nn_graph,  affinity = metric)[0].tocsr())
    fit_data += fit_data.T
    fit_data = (fit_data > 0).astype(np.float)"""
    #fit_data = neigh.kneighbors_graph(TE_pca, mode = 'connectivity')
    #mst = sps.csgraph.minimum_spanning_tree().tocsc()
    #fit_data += mst
    #fit_data += fit_data.T
    #fit_data = (fit_data > 0).astype(np.float)
    """
    G = nx.from_scipy_sparse_matrix(fit_data)
    plt.figure()
    nx.draw_spectral(G,node_color=encoded_labels,arrows=False,node_size=10)
    plt.savefig(work_dir+'spectral_layout.png',dpi=300)"""
    # fixme fix spectral clustering
    spec = SpectralClustering(n_clusters=n_subgenomes + 1 - int(all), affinity='precomputed', n_neighbors=n_neighbors)#'precomputed')
    spec.fit(fit_data)
    labels = spec.labels_

    #bgmm = BayesianGaussianMixture(n_components=n_subgenomes + 1 - int(all))
    #bgmm.fit(TE_pca)#[inliers])
    #labels = inliers_outliers
    #labels[inliers] = bgmm.predict(TE_pca[inliers])
    #labels = bgmm.predict(TE_pca)
    pickle.dump(labels,open(work_dir+'repeat_clusters.p','w'))
    ctx.invoke(plotPositions,positions_npy=work_dir+'TE_pca.npy', labels_pickle=scaffolds_pickle, colors_pickle=work_dir+'repeat_clusters.p', output_fname=work_dir+'top_TE_pca_clusters.html', graph_file='xxx', layout='standard', iterations=0)
    if not all:
        labels[labels == np.argmin(np.linalg.norm(map(lambda x: np.mean(x,axis=0),[TE_pca[labels == label] for label in sorted(set(labels))]),axis=1))] = -1
    try:
        os.makedirs(work_dir+'/preliminary/')
    except:
        pass
    for i in sorted(set(labels) - {-1}):#range(max(labels) + 1):
        output_scaffolds = scaffolds[labels == i]
        with open(work_dir+'/preliminary/subgenome_%d.txt'%i,'w') as f:
            f.write('\n'.join(output_scaffolds))
    cmT = cm.transpose()
    row_function2 = lambda row: np.argmax(row) if (row[row!=np.max(row)] and np.all(np.vectorize(lambda x: np.float(np.max(row))/x >= differential_sum_ratio)(row[row != np.max(row)]))) else -1
    n_repeats_each_extraction_run = []
    n_labelled_extraction_run = []
    for i in range(iterations):
        #try:
        TE_subgenome_matrix = []
        for subgenome in sorted(set(labels) - {-1}):#range(max(labels)+1):
            TE_subgenome_matrix.append(np.vectorize(lambda x: x if x else default_repeat_val)(np.array(cmT[:,labels == subgenome].sum(axis=1))[:,0]))
        TE_subgenome_matrix = np.vstack(TE_subgenome_matrix).T
        differential_TEs = np.array([row_function(row) for row in TE_subgenome_matrix])
        print('a')
        n_repeats_each_extraction_run.append([len(differential_TEs[differential_TEs == label]) for label in subgenomes])
        final_matrix = []
        for subgenome in subgenomes:
            final_matrix.append(np.vectorize(lambda x: x if x else default_total_count)(cm[:,differential_TEs == subgenome].sum(axis=1)))
        final_matrix = np.hstack(final_matrix)#.T
        print(final_matrix)
        labels = np.array([row_function2(row) for row in final_matrix])
        print('b')
        n_labelled_extraction_run.append([len(labels[labels==label]) for label in range(max(labels)+1)])
        #except:
        #    print 'iteration failure at %d, displaying next best results'%i
        #    break
    for run_analysis, outfile in zip([n_repeats_each_extraction_run,n_labelled_extraction_run],[work_dir+'/number_repeats_each_iteration.png',work_dir+'/number_labelled_scaffolds_each_iteration.png']):
        df = pd.DataFrame(run_analysis).reset_index(drop=False)
        print(df)
        df = pd.melt(df.rename(columns={'index':'Iteration'}),id_vars=['Iteration'],value_vars=range(max(labels) + 1)).rename(columns={'variable':'Subgenome','value':'Number_Hits/Labels'})
        print(run_analysis,df)
        plt.figure()
        sns.tsplot(data=df,condition='Subgenome',unit=None,interpolate=True,legend=True,value='Number_Hits/Labels',time='Iteration')
        plt.savefig(outfile,dpi=300)
    try:
        os.makedirs(work_dir+'/output/')
    except:
        pass
    scaffolds = np.array(pickle.load(open(scaffolds_pickle)))
    for i in sorted(set(labels) - {-1}):#range(max(labels) + 1):
        output_scaffolds = scaffolds[labels == i]
        with open(work_dir+'/output/subgenome_%d.txt'%i,'w') as f:
            f.write('\n'.join(output_scaffolds))

    pickle.dump(labels,open(work_dir+'repeat_final_partitions.p','w'))
    ctx.invoke(plotPositions,positions_npy=work_dir+'TE_pca.npy', labels_pickle=scaffolds_pickle, colors_pickle=work_dir+'repeat_final_partitions.p', output_fname=work_dir+'top_TE_pca_final.html', graph_file='xxx', layout='standard', iterations=0)
    if reference_fasta:
        ctx.invoke(txt2fasta,txt_files=','.join(glob.glob(work_dir+'/output/subgenome_*.txt')),reference_fasta=reference_fasta)


def stats(arr):
    return (np.mean(arr), np.std(arr), np.min(arr), np.max(arr))


@polycracker.command(name='differential_TE_histogram')
@click.option('-npy','--differential_repeat_subgenome_matrix','differential_TE_subgenome_matrix',default = './TE_cluster_analysis/subgenome_differential_top_TEs.npy',show_default=True, type=click.Path(exists=False))
def differential_TE_histogram(differential_TE_subgenome_matrix):
    """Compare the ratio of hits of certain highly informative repeats between different found genomes."""
    import seaborn as sns
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')
    diff_matrix = np.load(differential_TE_subgenome_matrix)[:,1:].astype(np.float)
    #print diff_matrix
    row_function = lambda row: np.array([np.argmax(row).astype(np.float),np.mean(np.vectorize(lambda x: np.float(np.max(row))/x)(row[row != np.max(row)]))])
    diff_matrix_differential = np.apply_along_axis(row_function,1,diff_matrix)
    #print diff_matrix_differential
    subgenomes = np.vectorize(lambda x: 'Subgenome %d'%int(x))(diff_matrix_differential[:,0])
    differentials = diff_matrix_differential[:,1]
    stats_diff_TEs = {}
    fig, axs = plt.subplots(1,len(set(subgenomes)),figsize=(7, 7), sharex=False, sharey=False)
    for i,subgenome in enumerate(set(subgenomes)):
        diff = differentials[subgenomes==subgenome]
        stats_diff_TEs[subgenome] = stats(diff)
        plt.axes(axs[i])
        sns.distplot(diff,label=subgenome,ax=axs[i],kde=False)
        plt.xlabel('Differential Score')
        plt.legend()
        if i == 0:
            plt.ylabel('Count')
    pd.DataFrame(stats_diff_TEs,index=['Mean','Standard Deviation', 'Min', 'Max']).to_csv('Differential_TEs_Diff_Score.csv')
    plt.title('How Differential are Differential TEs?')
    plt.savefig("Differential_TEs_Diff_Score.png",dpi=300)


def label_TE_bed(TE_bed, original_subgenomes_bed):
    TE_bed = BedTool(TE_bed).sort()
    subgenomes = BedTool(original_subgenomes_bed)
    subgenome_TE_bed = TE_bed.intersect(subgenomes, wa = True, wb = True).sort()
    ambiguous_TE_bed = TE_bed.intersect(subgenomes, v=True, wa = True).sort()
    subgenome_bed_text = ''
    for line in str(subgenome_TE_bed).splitlines():
        if line:
            lineList = line.strip('\n').split()
            subgenome_bed_text += '\t'.join(['_'.join(lineList[0:3]), '0', str(int(lineList[2]) - int(lineList[1])), lineList[-1]]) + '\n'
    for line in str(ambiguous_TE_bed).splitlines():
        if line:
            lineList = line.strip('\n').split()
            subgenome_bed_text += '\t'.join(['_'.join(lineList[0:3]), '0', str(int(lineList[2]) - int(lineList[1])), 'ambiguous']) + '\n'
    subgenome_TE_bed = BedTool(subgenome_bed_text,from_string=True).sort().merge(c=4, o='distinct')
    TE_subgenomes = defaultdict(list)
    for line in str(subgenome_TE_bed).splitlines():
        if line:
            lineList = line.strip('\n').split()
            TE_subgenomes[lineList[0]] = (lineList[-1] if ',' not in lineList[-1] else 'ambiguous')
    return TE_subgenomes


def label_new_windows(work_dir, windows_bed, original_subgenomes_bed):
    windows_bed = BedTool(windows_bed)
    scaffolds_subgenome_bed = BedTool(original_subgenomes_bed)
    labelled_bed = windows_bed.intersect(scaffolds_subgenome_bed,wa=True,wb=True).sort().merge(d=-1,c=7,o='distinct')
    ambiguous_bed = windows_bed.intersect(scaffolds_subgenome_bed,wa=True,v=True)
    bed_lines = []
    for line in str(ambiguous_bed).splitlines():
        if line:
            bed_lines.append(line.split()+['ambiguous'])
    for line in str(labelled_bed).splitlines():
        if line:
            if ',' in line:
                bed_lines.append(line.split()[:-1]+['ambiguous'])
            else:
                bed_lines.append(line.split())
    a = BedTool(bed_lines).sort()
    a.saveas(work_dir+'relabelled_windows.bed')
    new_labels = np.array([line.split()[-1] for line in str(a).splitlines()])
    pickle.dump(new_labels,open(work_dir+'new_labels.p','wb'))

@polycracker.command(name='repeat_subclass_analysis')
@click.option('-w', '--work_dir', default='./TE_subclass_analysis/', show_default=True, help='Work directory for computations of TE_subclass_analysis.', type=click.Path(exists=False))
@click.option('-go', '--original_fasta', help='Full path to original fasta file, nonchunked.', type=click.Path(exists=False))
@click.option('-rp', '--top_repeat_list_pickle', default='./TE_cluster_analysis/informative_subgenome_TE_list.p', help='Pickle containing list of top informative subgenome differential TEs.', show_default=True, type=click.Path(exists=False))
@click.option('-rd', '--top_repeat_dict_pickle', default='./TE_cluster_analysis/informative_subgenome_TE_dict.p', help='Pickle containing dict of top informative subgenome differential TEs by subgenome.', show_default=True, type=click.Path(exists=False))
@click.option('-r', '--all_family_subclass_pickle', default='./TE_cluster_analysis/TE_motif_subclass.p', help='Pickle containing set of all TEs family, subclasses.', show_default=True, type=click.Path(exists=False))
@click.option('-re', '--all_repeat_elements', default='./TE_cluster_analysis/repeat_elements.p', help='All repeat elements, to be converted to bed format.', show_default=True, type=click.Path(exists=False))
@click.option('-rs', '--class_subclass_pickle', default='./TE_cluster_analysis/repeat_class_subclass.p', help='All repeat classes and subclasses, to use to find indices to extract bed intervals.' ,show_default=True, type=click.Path(exists=False))
@click.option('-bo','--original_subgenomes_bed', default = '', help='Full path to original bed file containing subgenome labelling. Will use this to label TEs by subgenome.', type=click.Path(exists=False))
@click.option('-rf', '--repeat_fasta', default = '', help='Full path to repeat fasta file, output from repeat masker pipeline.', type=click.Path(exists=False))
@click.option('-bt','--bootstrap', is_flag=True, help='Bootstrap subclass trees generation.')
def repeat_subclass_analysis(work_dir, original_fasta, top_repeat_list_pickle, top_repeat_dict_pickle, all_family_subclass_pickle, all_repeat_elements, class_subclass_pickle, original_subgenomes_bed, repeat_fasta, bootstrap):
    """Input repeat_fasta and find phylogenies of TE subclasses within. In development: Better analysis may be https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2912890/."""
    #from Bio import AlignIO
    from ete3 import Tree, TreeStyle, TextFace #FIXME can't import treestyle, reset anaconda environment
    from xvfbwrapper import Xvfb
    if work_dir.endswith('/') == 0:
        work_dir += '/'
    try:
        os.makedirs(work_dir)
    except:
        pass
    colors = ["red","green","blue","orange","purple","pink","yellow"]
    if repeat_fasta:
        subprocess.call("awk '{print $1}' %s > %s && dedupe.sh overwrite=true in=%s out=%s ac=f && rm %s"%(repeat_fasta, work_dir+'temp.fa',work_dir+'temp.fa',work_dir+'repeats.fa',work_dir+'temp.fa'), shell=True)
    ### Subclass analysis
    all_TEs = np.array(pickle.load(open(all_family_subclass_pickle,'rb')))
    top_TEs = np.array(pickle.load(open(top_repeat_list_pickle,'rb')))
    all_TEs_subclasses = Counter(np.vectorize(lambda x: x.split('#')[1])(list(set(all_TEs))))
    subclasses = set(all_TEs_subclasses.keys())
    top_TEs_subclasses = Counter(np.vectorize(lambda x: x.split('#')[1])(list(set(top_TEs))))
    for subclass in subclasses:
        if subclass not in top_TEs_subclasses:
            del all_TEs_subclasses[subclass]
    all_TEs_subclasses = OrderedDict(sorted(all_TEs_subclasses.items()))
    top_TEs_subclasses = OrderedDict(sorted(top_TEs_subclasses.items()))
    plots = []
    plots.append(go.Bar(x = all_TEs_subclasses.keys(),y = all_TEs_subclasses.values(), name='All TEs'))
    plots.append(go.Bar(x = top_TEs_subclasses.keys(),y = top_TEs_subclasses.values(), name='Top TEs'))
    all_repeat_subclasses = np.array(all_TEs_subclasses.values())
    observed = np.array(top_TEs_subclasses.values())
    expected = np.array(all_TEs_subclasses.values())/float(sum(all_TEs_subclasses.values()))*sum(top_TEs_subclasses.values())
    plots.append(go.Bar(x = top_TEs_subclasses.keys(),y = expected, name='Expected TEs'))
    chisq = (observed-expected)**2/expected
    df = pd.DataFrame([all_repeat_subclasses,observed,expected,chisq],index=['all_repeat_subclasses','observed','expected','chisq'],columns=top_TEs_subclasses.keys())
    print df
    df.to_csv(work_dir+'/chi-sq-breakdown-subclasses.csv')
    top_chisq = np.argsort(chisq)[::-1]
    top_subclass = top_TEs_subclasses.keys()[top_chisq[0]]
    fig = go.Figure(data=plots,layout=go.Layout(barmode='group',title=r'All vs Top Differential TEs, by Subclass; Top Subclass: %s, chi^2=$%.2f'%(top_subclass,chisq[top_chisq[0]])))
    py.plot(fig, filename=work_dir+'Subclass_Division_Top_vs_All_TEs.html', auto_open=False)
    class_subclass = np.array(pickle.load(open(class_subclass_pickle,'rb')))
    all_repeats = np.array(pickle.load(open(all_repeat_elements,'rb')))
    repeats_bed = work_dir+'TE_elements.bed'
    with open(repeats_bed,'w') as f:
        for repeat in all_repeats:
            rlist = repeat.split('_')
            f.write('\t'.join(['_'.join(rlist[0:-2])]+rlist[-2:])+'\n')
    TE_labels = label_TE_bed(repeats_bed,original_subgenomes_bed)
    subgenomes_color = {subgenome: colors[i] for i, subgenome in enumerate(set(TE_labels.values()))}
    TE_colors = {TE: subgenomes_color[subgenome] for TE,subgenome in TE_labels.items()}
    top_repeat_dict = pickle.load(open(top_repeat_dict_pickle,'rb'))
    subgenomes_repeat_subclasses = {subgenome:defaultdict(lambda: 0) for subgenome in set(TE_labels.values())}
    for i,top_subclass in enumerate(np.array(top_TEs_subclasses.keys())[top_chisq]):
        top_subclass_repeats = all_repeats[class_subclass==top_subclass]
        top_subclass_fname = top_subclass.replace('/','-')
        if len(top_subclass_repeats) >= 2:
            Subgenome_type_counts = defaultdict(lambda: 0)
            for label in TE_labels:
                Subgenome_type_counts[TE_labels[label]] += 1
            plots = []
            plots.append(go.Bar(x = Subgenome_type_counts.keys(),y = Subgenome_type_counts.values(), name='Subgenomes'))
            fig = go.Figure(data=plots,layout=go.Layout(title='Subgenome Breakdown of All TEs Matching the %s most informative and interesting subclass # %d'%(top_subclass,i)))
            py.plot(fig, filename=work_dir+'Breakdown_All_subclass_%s_%d.html'%(top_subclass_fname,i), auto_open=False)
            #print TE_labels
            print list(set(TE_labels.values()))
            subclass_bed = work_dir+'subclass_%s.bed'%top_subclass_fname

            #### APPROACH 1
            if repeat_fasta:
                Subgenome_type_counts = defaultdict(lambda: 0)
                subclass_colors = defaultdict(list)
                for subgenome in top_repeat_dict:
                    subgenome_name = (subgenome[:1].lower() + ('_'.join(subgenome[1:].split())) if subgenome != 'ambiguous' else 'ambiguous')
                    for element in top_repeat_dict[subgenome]:
                        if element.split('#')[1] == top_subclass:
                            subclass_colors[element] = subgenomes_color[subgenome_name]
                            Subgenome_type_counts[subgenome_name] += 1
                for subgenome in subgenomes_repeat_subclasses:
                    try:
                        subgenomes_repeat_subclasses[subgenome][top_subclass] = Subgenome_type_counts[subgenome]
                    except:
                        subgenomes_repeat_subclasses[subgenome][top_subclass] = 0
                print subclass_colors
                plots = []
                plots.append(go.Bar(x = Subgenome_type_counts.keys(),y = Subgenome_type_counts.values(), name='Subgenomes'))
                fig = go.Figure(data=plots,layout=go.Layout(title='Subgenome Breakdown of Top TEs Matching the %s most informative and interesting subclass #%d'%(top_subclass,i)))
                py.plot(fig, filename=work_dir+'Breakdown_Top_subclass_%s_%d.html'%(top_subclass_fname,i), auto_open=False)
                top_subclass_elements = np.array(subclass_colors.keys())#top_TEs[np.vectorize(lambda x: x.split('#')[1] == top_subclass )(list(set(top_TEs)))]
                print len(top_TEs), top_subclass, len(top_subclass_elements)
                if len(top_subclass_elements) >= 2:# and top_subclass not in ['Unknown','Simple_repeat']:# and top_subclass != 'Simple_repeat':
                    subclass_fasta = work_dir+top_subclass_fname+'.fa'
                    print subclass_fasta
                    with open(subclass_fasta.replace('.fa','.intermediate.fa'),'w') as f2:
                        if top_subclass_fname != 'Simple_repeat':
                            with Fasta(work_dir+'repeats.fa') as f:
                                print top_subclass_elements
                                f2.write('\n'.join(['>%s\n%s'%(element,str(f[element][:])) for element in top_subclass_elements]))
                        else:
                            f2.write('\n'.join(['>%s\n%s'%(element,element[element.find('(')+1:element.find(')')]) if len(element.strip(')(')) != len(element) else '>%s\n%s'%(element,str(f[element][:])) for element in top_subclass_elements ]))
                    subprocess.call('reformat.sh overwrite=true in=%s out=%s fastawrap=60'%(subclass_fasta.replace('.fa','.intermediate.fa'),subclass_fasta),shell=True) # "export _JAVA_OPTIONS='-Xms5G -Xmx15G' && "+
                    #subprocess.call('samtools faidx %s %s > %s'%(work_dir+'repeats.fa', ' '.join(top_subclass_elements), subclass_fasta), shell=True)
                    vdisplay = Xvfb()
                    vdisplay.start()
                    subprocess.call('rm %stree_%s_output -r'%(work_dir,top_subclass_fname) if work_dir.strip(' ') != './' and '*' not in work_dir else 'echo change_work_dir',shell=True)
                    subprocess.call('ete3 build --cpu 2 -w %s -n %s -o %stree_%s_output --clearall'%('standard_phyml_bootstrap' if bootstrap else 'standard_fasttree',subclass_fasta,work_dir,top_subclass_fname),shell=True) # standard_phyml_bootstrap
                    tree = work_dir+'tree_%s_output/clustalo_default-none-none-%s/%s.final_tree.nw'%(top_subclass_fname,'phyml_default_bootstrap' if bootstrap else 'fasttree_full','%s.fa'%top_subclass_fname) #
                    print 'Still Running'
                    t = Tree(tree)
                    #t.link_to_alignment(alignment=subclass_fasta, alg_format="fasta")
                    for leaf in t:
                        leaf.img_style['size'] = 0
                        if leaf.is_leaf():
                            color=subclass_colors.get(leaf.name, None)
                            if color:
                                name_face = TextFace(leaf.name,fgcolor=color)
                                leaf.add_face(name_face,column=0,position='branch-right')
                    ts = TreeStyle()
                    #ts.mode = "c" # draw tree in circular mode
                    #ts.scale = 20
                    ts.show_leaf_name = False
                    t.render(work_dir+"subclass_%s_%d_tree.png"%(top_subclass_fname,i), dpi=300, w=1000, tree_style=ts)
                    print 'Debug Test'
                    vdisplay.stop()
    if repeat_fasta:
        plots = []
        for subgenome in subgenomes_repeat_subclasses:
            plots.append(go.Bar(x=subgenomes_repeat_subclasses[subgenome].keys(),y=subgenomes_repeat_subclasses[subgenome].values(),label=subgenome))
        fig = go.Figure(data=plots,layout=go.Layout(title='Subgenome/Subclass Breakdown of Top Repeats',barmode='stack'))
        py.plot(fig, filename=work_dir+'Breakdown_Subgenome_Subclass_Top.html', auto_open=False)
    else:
        print 'Breakdown No Print'
    #### APPROACH 2
    # find most commonly occurring top_subclass
    if 0:
        with open(subclass_bed,'w') as f:
            for repeat in top_subclass_repeats:
                rlist = repeat.split('_')
                f.write('\t'.join(['_'.join(rlist[0:-2])]+rlist[-2:] + [repeat])+'\n')
        subclass_fasta = subclass_bed.replace('.bed','.fasta')
        subprocess.call('bedtools getfasta -name -fi %s -bed %s -fo %s'%(original_fasta,subclass_bed,subclass_fasta),shell=True)
        subprocess.call('ete3 build --cpu 4 -w standard_fasttree -n %s  -o %stree_output --clearall'%(subclass_fasta,work_dir),shell=True)
        tree = work_dir+'tree_output/clustalo_default-none-none-fasttree_full/%s.final_tree.nw'%('subclass_%s.fasta'%top_subclass)
        t = Tree(tree)
        for leaf in t:
            leaf.add_features(color=TE_colors.get(leaf.name, "none"))
        ts = TreeStyle()
        ts.mode = "c" # draw tree in circular mode
        ts.scale = 20
        t.render("subclass_%s_tree.png"%top_subclass, w=183, units="mm", tree_style=ts)
        #subprocess.call('fftns %s > %s'%(work_dir+family+'.fa',work_dir+family+'_aligned.fasta'),shell=True)  mafft_ginsi-none-none-fasttree_default
        #subprocess.call('fasttree -nt -gtr < %s > %s'%(work_dir+family+'_aligned.phy',work_dir+family+'_tree.txt'), shell=True)
    ### FAMILY ANALYSIS, SKIP FOR NOW
    if 0:
        # format fasta file toupper()
        repeat_fasta = 'NULL, FIXME'
        subprocess.call("awk '{print $1}' %s > %s && dedupe.sh overwrite=true in=%s out=%s ac=f && rm %s"%(repeat_fasta, work_dir+'temp.fa',work_dir+'temp.fa',work_dir+'repeats.fa',work_dir+'temp.fa'), shell=True)

        # grab TE names
        TEs = Fasta(work_dir+'repeats.fa')
        #TE_names = np.array(TEs.keys())
        TE_names = np.array(pickle.load(open(top_repeat_list_pickle,'rb'))) #FIXME above is important, or do this by subgenome
        TE_families = np.vectorize(lambda x: x.split('_')[0] if x.endswith('rich') == 0 else x.split('#')[0])(TE_names)
        TE_families_set = set(TE_families)
        for family in TE_families_set:
            TEs_from_family = TE_names[TE_families==family]
            if len(TEs_from_family) >= 2:
                subprocess.call('samtools faidx %s %s > %s'%(work_dir+'repeats.fa', ' '.join(TEs_from_family), work_dir+family+'.fa'), shell=True)
                subprocess.call('fftns %s > %s'%(work_dir+family+'.fa',work_dir+family+'_aligned.fasta'),shell=True)
                subprocess.call('fasttree -nt -gtr < %s > %s'%(work_dir+family+'_aligned.phy',work_dir+family+'_tree.txt'), shell=True)
                #aln = AlignIO.read(open(work_dir+family+'_aligned.fasta','r'),'fasta')
                #AlignIO.write(aln,open(work_dir+family+'_aligned.phy','w'),'phylip-relaxed')
                #subprocess.call('raxmlHPC -s %s -n %s -m %s -f a -x 123 -N autoMRE -p 456 -q %s'%(work_dir+family+'_aligned.phy',work_dir+family+'_tree.txt','GTRCAT',work_dir+'bootstrap.'+family+'.txt'),shell=True)
        """MAYBE TRY mafft-qinsi"""


@polycracker.command(name='send_repeats')
@click.option('-rf','--subclass_repeat_fasta',default='./TE_subclass_analysis/Unknown.fa',show_default=True,help='Full path to subclass repeat fasta.', type=click.Path(exists=False))
def send_repeats(subclass_repeat_fasta):
    """Use bbSketch to send fasta file containing repeats to check it against different databases for sequence similarity. Uses minhash to check relative abundance of species.
    Where do these repeats come from and what is the parasitic DNA source."""
    subprocess.call('sendsketch.sh in=%s nt overwrite=True'%(subclass_repeat_fasta),shell=True)#,subclass_repeat_fasta[:subclass_repeat_fasta.rfind('/')]),shell=True) # refseq mode=single
    subprocess.call('sendsketch.sh in=%s refseq overwrite=True'%(subclass_repeat_fasta),shell=True)#,subclass_repeat_fasta[:subclass_repeat_fasta.rfind('/')]),shell=True) # refseq mode=single


@polycracker.command(name='run_iqtree')
@click.option('-f','--fasta_in',default='./TE_subclass_analysis/Unknown.fa',show_default=True,help='Full path to subclass repeat fasta. To be aligned via muscle.', type=click.Path(exists=False))
@click.option('-m','--model',default='MF',show_default=True,help='Model selection for iqtree. See http://www.iqtree.org/doc/Substitution-Models.')
@click.option('-nt','--n_threads',default='AUTO',show_default=True,help='Number of threads for parallel computation.')
@click.option('-b','--bootstrap',default=25,show_default=True,help='Bootstrap support.')
def run_iqtree(fasta_in,model,n_threads,bootstrap):
    """Perform multiple sequence alignment on multi-fasta and run iqtree to find phylogeny between each sequence."""
    import sys
    iqtree_line = next(path for path in sys.path if 'conda/' in path and '/lib/' in path).split('/lib/')[0]+'/bin/ete3_apps/bin/iqtree'
    muscle_line = next(path for path in sys.path if 'conda/' in path and '/lib/' in path).split('/lib/')[0]+'/bin/ete3_apps/bin/muscle'

    subprocess.call(muscle_line + ' -in %s -out %s'%(fasta_in,fasta_in.replace('.fasta','.muscle.fasta').replace('.fa','.muscle.fa')),shell=True)
    subprocess.call('rm %s.ckp.gz'%fasta_in.replace('.fasta','.muscle.fasta').replace('.fa','.muscle.fa'),shell=True)
    subprocess.call(iqtree_line + ' -s %s -m %s -nt %s %s'%(fasta_in.replace('.fasta','.muscle.fasta').replace('.fa','.muscle.fa'),model,n_threads,'-b %d'%bootstrap if bootstrap > 1 and model != 'MF' else ''), shell=True)


@polycracker.command(name='color_trees')
@click.option('-w', '--work_dir', default='./TE_subclass_analysis/', show_default=True, help='Work directory for computations of Trees.', type=click.Path(exists=False))
@click.option('-n', '--newick_in', default='./x.treefile', help='Input tree, newick format.', show_default=True, type=click.Path(exists=False))
@click.option('-rd', '--top_repeat_dict_pickle', default='./TE_cluster_analysis/informative_subgenome_TE_dict.p', help='Pickle containing dict of top informative subgenome differential TEs by subgenome.', show_default=True, type=click.Path(exists=False))
def color_trees(work_dir,newick_in,top_repeat_dict_pickle):
    """Color phylogenetic trees by progenitor of origin."""
    from ete3 import Tree, TreeStyle, TextFace
    #from xvfbwrapper import Xvfb
    work_dir+='/'
    ts = TreeStyle()
    tree =  Tree(newick_in)
    colors  = ["red","green","blue","orange","purple","pink","yellow"]
    subgenomes_repeat_dict = pickle.load(open(top_repeat_dict_pickle,'r'))
    subgenomes = subgenomes_repeat_dict.keys()
    subgenome_colors = dict(zip(subgenomes,colors[:len(subgenomes)]))
    repeat_color_dict = { repeat:subgenome_colors[s] for s,repeat in reduce(lambda x,y: x+y,[map(lambda x: (subgenome,x),subgenomes_repeat_dict[subgenome]) for subgenome in subgenomes_repeat_dict])}
    for leaf in tree:
        leaf.img_style['size'] = 0
        if leaf.is_leaf():
            name = leaf.name
            if 'Simple_repeat' in name and 'n' in name:
                name = '(' + name.split('_')[1] + ')n#'+'Simple_repeat'
            else:
                name = name.rsplit('-',1)[0]+'-'+'#'.join(name.rsplit('-',1)[1].split('_',1)).replace('_','/')
            print name
            color=repeat_color_dict.get(name, None)
            #print color
            if color:
                name_face = TextFace(name,fgcolor=color)
                leaf.add_face(name_face,column=0,position='branch-right')
    ts.show_leaf_name = False
    ts.show_branch_support = True
    R = tree.get_midpoint_outgroup()
    tree.set_outgroup(R)
    tree.render(work_dir+"subclass_%s_tree.png"%(newick_in[newick_in.rfind('/')+1:newick_in.rfind('.')]), dpi=300, w=1000, tree_style=ts)
    tree.render(work_dir+"subclass_%s_tree.pdf"%(newick_in[newick_in.rfind('/')+1:newick_in.rfind('.')]), dpi=300, w=1000, tree_style=ts)


@polycracker.command(name='find_denovo_repeats')
@click.option('-sp', '--input_species', help='Input species for naming of repeat database.', type=click.Path(exists=False))
@click.option('-fi', '--input_fasta', help='Full path to original fasta file, nonchunked.', type=click.Path(exists=False))
@click.option('-od', '--out_dir', default='./denovo_repeats/', show_default=True, help='Work directory for computations of denovo repeats.', type=click.Path(exists=False))
@click.option('-rd','--recover_dir', default='',show_default=True,help='Recover directory when using RepeatModeler',type=click.Path(exists=False))
def find_denovo_repeats(input_species,input_fasta, out_dir,recover_dir):
    """Wrapper for repeat modeler. Runs repeatmodeler and repeat masker to ID repeats."""
    print 'In development'
    if out_dir.endswith('/') == 0:
        out_dir += '/'
    try:
        os.makedirs(out_dir)
    except:
        pass
    recover_dir = (os.path.abspath(recover_dir) if recover_dir else '')
    if recover_dir:
        try:
            os.makedirs(recover_dir)
        except:
            pass
    input_fasta = os.path.abspath(input_fasta)
    import multiprocessing
    n_cpus = multiprocessing.cpu_count()
    subprocess.call('BuildDatabase -name %s %s'%(input_species,input_fasta),shell=True)
    print 'nohup RepeatModeler %s -pa %d -database %s >& db.out'%('-recoverDir '+recover_dir if recover_dir else '',n_cpus-1,input_species)
    subprocess.call('nohup RepeatModeler %s -pa %d -database %s >& db.out'%('-recoverDir '+recover_dir if recover_dir else '',n_cpus-1,input_species),shell=True)
    print 'RepeatMasker -gff -dir %s -pa %d -lib %s-families.fa %s'%(out_dir,n_cpus-1,input_species,input_fasta)
    subprocess.call('RepeatMasker -gff -dir %s -pa %d -lib %s-families.fa %s'%(out_dir,n_cpus-1,input_species,input_fasta),shell=True)
    print 'Masker Done'
    # RUN TO THIS AND CONVERT TO GFF/BED
    # ADD GFF HERE
    # AND CHECK AGAINST NCBI
    #subprocess.call('sendsketch.sh in=%s nt mode=sequence out=%s/sketches.out',shell=True)
    # FIXME ADD INFO TO ABOVE


##################################################################################################

###################################### POLYPLOID COMPARISON ######################################

def kmer_set(k,kmers):
    final_kmer_set = []
    for kmer in kmers:
        if len(kmer) == k:
            final_kmer_set.append(kmer)
        else:
            final_kmer_set.extend(set([kmer[i:i+k] for i in xrange(len(kmer) - k)]))
    return set(final_kmer_set)


@polycracker.command(name='polyploid_diff_kmer_comparison')
@click.option('-p', '--analysis_path', default='./polyploid_comparison/', help='Work directory where computations for polyploid comparison is done.', type=click.Path(exists=False), show_default=True)
@click.option('-l', '--kmer_list_path', default='./polyploid_comparison/diff_kmer_lists/', help='Directory containing list of informative differential kmers for each polyploid, pickle files.', type=click.Path(exists=False), show_default=True)
@click.option('-t', '--kmer_type_path', default='./polyploid_comparison/diff_kmer_types/', help='Directory containing dictionaries of distributions of kmer class/subclass type for each polyploid, pickle files.', type=click.Path(exists=False), show_default=True)
def polyploid_diff_kmer_comparison(analysis_path, kmer_list_path, kmer_type_path):
    """Compare highly informative differential kmers between many different polyCRACKER runs/polyploids. Find intersections between them.
    In development: May be better to modify bio_hyp_class pipeline to handle this problem."""
    import venn
    # create output directory
    try:
        os.makedirs(analysis_path)
    except:
        pass
    if kmer_list_path.endswith('/') == 0:
        kmer_list_path += '/'
    if kmer_type_path.endswith('/') == 0:
        kmer_type_path += '/'
    if analysis_path.endswith('/') == 0:
        analysis_path += '/'
    polyploid_top_kmers = defaultdict(list)
    polyploid_top_subgenome_share_rate = defaultdict(list)
    for kmer_pickle in os.listdir(kmer_list_path):
        if kmer_pickle.endswith('.p'):
            polyploid_top_kmers[kmer_pickle.split('.')[0]] = pickle.load(open(kmer_list_path+kmer_pickle,'rb'))
    lowest_kmer_size = len(min(polyploid_top_kmers[min(polyploid_top_kmers.keys(), key=lambda x: len(min(polyploid_top_kmers[x], key=len)))], key = len))
    #print lowest_kmer_size
    for polyploid in polyploid_top_kmers:
        polyploid_top_subgenome_share_rate[polyploid] = 1. - len(set(polyploid_top_kmers[polyploid]))/float(len(polyploid_top_kmers[polyploid]))
        polyploid_top_kmers[polyploid] = kmer_set(lowest_kmer_size, polyploid_top_kmers[polyploid])
    py.plot(go.Figure(layout=go.Layout(title='Top Differential Kmer Share Rate Between Polyploid Subgenomes'),
                      data=[go.Bar(x=polyploid_top_subgenome_share_rate.keys(),y=polyploid_top_subgenome_share_rate.values(),name=polyploid)]),
            filename=analysis_path+'polyploid_subgenome_top_kmer_share.html', auto_open=False)
    #pickle.dump(polyploid_top_kmers,open('top_kmers.p','wb'))
    #print polyploid_top_kmers
    n_polyploids = len(polyploid_top_kmers.keys())
    labels = venn.get_labels(polyploid_top_kmers.values(), fill=['number', 'logic'])
    if n_polyploids == 2:
        fig, ax = venn.venn2(labels, names=polyploid_top_kmers.keys())
    elif n_polyploids == 3:
        fig, ax = venn.venn3(labels, names=polyploid_top_kmers.keys())
    elif n_polyploids == 4:
        fig, ax = venn.venn4(labels, names=polyploid_top_kmers.keys())
    elif n_polyploids == 5:
        fig, ax = venn.venn5(labels, names=polyploid_top_kmers.keys())
    elif n_polyploids == 6:
        fig, ax = venn.venn6(labels, names=polyploid_top_kmers.keys())
    else:
        print 'Invalid number of polyploids'
    if n_polyploids in range(2,7):
        fig.savefig(analysis_path+'polyploid_comparison_top_differential_kmers.png')
    try:
        for class_label in ['class', 'subclass']:
            polyploid_top_kmer_types = defaultdict(list)
            for kmer_pickle in os.listdir(kmer_type_path):
                if kmer_pickle.endswith(class_label+'.p'):
                    polyploid_top_kmer_types[kmer_pickle.split('.')[0]] = pickle.load(open(kmer_type_path+kmer_pickle,'rb'))
            plots = []
            for polyploid in polyploid_top_kmer_types:
                plots.append(go.Bar(x=polyploid_top_kmer_types.keys(),y=polyploid_top_kmer_types.values(),name=polyploid))
            df = pd.DataFrame(polyploid_top_kmer_types)
            df.fillna(0, inplace=True)
            df.to_csv(analysis_path+'Polyploid_Comparison_Differential_Kmers_By_%s.csv'%class_label)
            indep_test_results = chi2_contingency(df.as_matrix(), correction=True)
            fig = go.Figure(data=plots,layout=go.Layout(title='X**2=%.2f, p=%.2f'%indep_test_results[0:2],barmode='group'))
            py.plot(fig, filename=analysis_path+'Polyploid_Comparison_Differential_Kmers_By_%s.html'%class_label, auto_open=False)
    except:
        pass
    """I remember that.  I guess the questions I want to answer are:  can we define particular repeats ("full length"
    rather than just the kmers) that are marking our subgenomes?  What are they (type/class/family)?

    take repeats fasta file and bbmap it against main fasta file... Find clustering matrix and see if separates.

    then see which class TE helps separate it and find top TEs
    """


@polycracker.command()
@click.option('-s','--subclass_dir',default='./',show_default=True,help='')
def compare_subclasses(subclass_dir):
    """In development: Grab abundance of top classes and subclasses of TEs in each subgenome and compare vs progenitors. Useful to use pairwise similarity function of all consensus repeats."""
    print 'In development'


@polycracker.command()
@click.pass_context
@click.option('-i','--input_dict',default='subgenome_1:./fasta_files/subgenome_1.fa,SpeciesA:./SpeciesA.fasta',show_default=True, help='MANDATORY: Comma delimited mapping of all subgenome names to their subgenome fasta files.', type=click.Path(exists=False))
@click.option('-f', '--folder_delimiter', default='./folder/,_,4', show_default=True, help='OPTIONA: Comma delimited list of folder containing genomes, delimiters from which to construct short names, and number of characters to use for short name. Save fastas as AAAA_xxx_v0.fa format. Supercedes -i option, unless default value not modified.', type=click.Path(exists=False))
@click.option('-kv', '--default_kcount_value', default = 1, help='If kmer hits in subgenome is 0, this value will replace it.', show_default = True)
@click.option('-dk', '--ratio_threshold', default=20, help='Value indicates that if the counts of a particular kmer in a subgenome divided by any of the counts in other subgenomes are greater than this value, then the kmer is differential.', show_default=True)
@click.option('-w', '--work_dir', default='./', show_default=True, help='Work directory where computations for biological hypothesis testing is done.', type=click.Path(exists=False))
@click.option('-m', '--blast_mem', default='100', help='Amount of memory to use for bbtools run. More memory will speed up processing.', show_default=True)
@click.option('-l', '--kmer_length', default=23, help='Length of kmers to find.', show_default=True)
@click.option('-ft', '--fast_tree', is_flag=True, help='Make quick estimated phylogenetic tree out of kmer matrix.')
@click.option('-min', '--min_count', default = 3, show_default=True, help='Minimum count for kmer counting.')
@click.option('-sk', '--skip_kcount', is_flag=True, help='Skip generation of kcount files. kcount files must be named by the following convention: subgenome_1 used in input dict -> subgenome_1.kcount')
@click.option('-max', '--max_val', default = 100, show_default=True, help='Minimum count for maximum count of kmer between subgenomes.')
def bio_hyp_class(ctx,input_dict, folder_delimiter, default_kcount_value, ratio_threshold, work_dir, blast_mem, kmer_length, fast_tree, min_count, skip_kcount, max_val):
    """Generate count matrix of kmers versus genomes. Optionally can transpose this matrix and find kmer guide tree / approximated phylogeny based on differential kmer counts. Changing settings to include all kmers can generate a more accurate guide tree."""
    #from sklearn.feature_extraction import DictVectorizer
    from sklearn.preprocessing import LabelEncoder
    #from scipy.stats import chisquare
    if not work_dir.endswith('/'):
        work_dir += '/'
    try:
        os.makedirs(work_dir)
    except:
        pass
    blast_memStr = "export _JAVA_OPTIONS='-Xms5G -Xmx%sG'"%(blast_mem)

    if folder_delimiter != './folder/,_,4':
        folder, delimiter, n_chars = tuple(folder_delimiter.split(','))
        if n_chars == 'n':
            n_char = False
        else:
            n_chars = int(n_chars)
        fastas = [fasta for fasta in os.listdir(folder) if fasta.endswith('.fa') or fasta.endswith('.fasta')]
        short_names = map(lambda x: x[:n_chars] + x[x.find(delimiter)+1:x.rfind(delimiter)] if n_char else x.split('.')[0],fastas)
        subgenome_labels = dict(zip(short_names,map(lambda x: folder+'/'+x,fastas)))
    else:
        subgenome_labels = {subgenome_name:subgenome_fasta for subgenome_name,subgenome_fasta in sorted([tuple(mapping.split(':')) for mapping in input_dict.split(',')])}
    kmer_matrix = []
    # FIXME GENERATE MATRIX HERE
    #def return_kcounts(subgenome_name):
    #kmer_counts = pd.read_table(work_dir+subgenome_name+'.kcount',sep=None)
    #return dict(zip(kmer_counts[0],kmer_counts[1]))
    #    return dict(zip(os.popen("awk '{ print $1 }' %s"%(work_dir+subgenome_name+'.kcount')).read().splitlines(),map(int,os.popen("awk '{ print $2 }' %s"%(work_dir+subgenome_name+'.kcount')).read().splitlines())))
    return_kcounts = lambda s_name: dict(itertools.izip(os.popen("awk '{ print $1 }' %s"%(work_dir+s_name+'.kcount')).read().splitlines(),map(int,os.popen("awk '{ print $2 }' %s"%(work_dir+s_name+'.kcount')).read().splitlines())))
    for subgenome_name in subgenome_labels:
        click.echo(subgenome_name)
        if not skip_kcount:
            if kmer_length <= 31:
                subprocess.call(blast_memStr+' && kmercountexact.sh mincount=%d overwrite=true fastadump=f in=%s out=%s k=%d'%(min_count,subgenome_labels[subgenome_name],work_dir+subgenome_name+'.kcount',kmer_length),shell=True)
            else:
                subprocess.call('jellyfish count -L %d -m %d -s %d -t 15 -C -o %s/mer_counts.jf %s && jellyfish dump %s/mer_counts.jf -c > %s/%s'%(min_count,kmer_length,os.stat(subgenome_labels[subgenome_name]).st_size,work_dir,subgenome_labels[subgenome_name],work_dir,work_dir,subgenome_name+'.kcount'))
        kmer_matrix.append(return_kcounts(subgenome_name))#dict(zip(kmer_counts[0],kmer_counts[1])))
    print subgenome_labels.keys()
    #dv = DictVectorizer(sparse=True)
    click.echo('fitting')
    #dv.fit(kmer_matrix)
    kmers = list(set().union(*map(dict.keys,kmer_matrix)))#reduce(set.union, map(set, map(dict.keys,kmer_matrix)))
    print kmers[0:10]
    kmer_mapping = LabelEncoder()
    kmer_mapping.fit(kmers)
    subgenomes = np.array(subgenome_labels.keys())
    data = sps.dok_matrix((len(subgenomes),len(kmers)),dtype=np.int)
    for i,d in enumerate(kmer_matrix):
        print i
        data[i,kmer_mapping.transform(d.keys())] = np.array(d.values())
    del kmer_matrix
    # FIXME I can use above to speed up other algorithms, kmer matrix generation
    data=data.tocsr()
    pickle.dump(subgenomes,open(work_dir+'subgenomes_all.p','wb'))
    if fast_tree: #FIXME visualize results?
        pca_data = Pipeline([('scaler',StandardScaler(with_mean=False)),('kpca',KernelPCA(n_components=3))]).fit_transform(data)
        np.save(work_dir+'kmer_pca_results.npy',pca_data)
        d_matrix = pairwise_distances(pca_data)
        d_matrix = (d_matrix + d_matrix.T)/2
        pd.DataFrame(d_matrix,index=subgenome_labels.keys(),columns=subgenome_labels.keys()).to_csv(work_dir+'kmer_distance_matrix.csv')
        matrix = [row[:i+1] for i,row in enumerate(d_matrix.tolist())]#[list(distance_matrix[i,0:i+1]) for i in range(distance_matrix.shape[0])]
        dm = _DistanceMatrix(names=subgenome_labels.keys(),matrix=matrix)
        constructor = DistanceTreeConstructor()
        tree = constructor.nj(dm)
        Phylo.write(tree,work_dir+'kmer_guide_tree.nh','newick')
        ctx.invoke(plotPositions,positions_npy=work_dir+'kmer_pca_results.npy',labels_pickle=work_dir+'subgenomes_all.p',colors_pickle='',output_fname=work_dir+'subgenome_bio_pca.html')
    data = data.T
    #kmers = np.array(dv.feature_names_)
    #kmer_matrix = dv.transform(kmer_matrix).T
    #row_function = lambda l: np.max(l)/float(np.min(l)) >= ratio_threshold
    #threshold_bool_array = []
    #for i in range(data.shape[0]): #FIXME here is where the slowdown occurs
    #    threshold_bool_array.append(row_function(np.clip(data[i,:].toarray()[0],default_kcount_value,None)))
    print 'pretransform'
    #print data.max(axis=1).toarray()[:,0][0:10]
    #print np.clip(data.min(axis=1).toarray(),default_kcount_value,None)[:,0][0:10]
    max_array = data.max(axis=1).toarray()[:,0]
    print sum(max_array >= max_val)
    threshold_bool_array = np.logical_and(np.vectorize(lambda x: x >= ratio_threshold)(max_array/np.clip(data.min(axis=1).toarray()[:,0],default_kcount_value,None)), max_array >= max_val)
    print 'post threshold'
    click.echo('check')
    #threshold_bool_array = np.array(threshold_bool_array)
    print threshold_bool_array
    kmers = kmer_mapping.inverse_transform(np.arange(data.shape[0]))[threshold_bool_array]#np.array(kmers)[kmer_mapping.transform(kmers)[threshold_bool_array]] # FIXME
    data = data[threshold_bool_array]
    pickle.dump(kmers,open(work_dir+'kmers_union.p','wb'))
    sps.save_npz(work_dir+'union_kmer_matrix.npz',data)
    df = pd.SparseDataFrame(data,default_fill_value=0,index=kmers,columns=subgenomes).to_dense()
    df.to_csv(work_dir+'kmer_master_count_matrix.csv')
    #np.apply_along_axis(row_function,1,[np.clip(kmer_matrix[i,:].toarray()[0],default_value,None) for i in range(kmer_matrix.shape[0])])
    #for i in range(kmer_matrix.shape[0]):
    #    row = np.clip(kmer_matrix[i,:].toarray(),default_value,None)
    # FIXME can now filter array and store as pandas to excel


@polycracker.command() # fixme future for polyCRACKER/metacracker, can use ubiquitous kmers between many lines, on non ubiquitous, rated via tfidf to definte kmers used for polycracker pipeline, automatic dimensionality reduction via abundance in different lines
@click.pass_context
@click.option('-w', '--work_dir', default='./', show_default=True, help='Work directory where computations for plotting kmer count matrix is done.', type=click.Path(exists=False))
@click.option('-csv', '--kmer_count_matrix', default='./kmer_master_count_matrix.csv', show_default=True, help='Kmer count matrix.', type=click.Path(exists=False))
@click.option('-r', '--reduction_method', default='tsne', show_default=True, help='Type of dimensionality reduction technique to use.', type=click.Choice(['tsne','kpca', 'spectral', 'nmf', 'feature']))
@click.option('-d', '--n_dimensions', default=3, help='Number of dimensions to reduce to.', show_default=True)
@click.option('-k', '--kernel', default='cosine', help='Kernel for KPCA. Cosine is particularly effective.', type=click.Choice(['linear','poly','rbf','sigmoid','cosine']), show_default=True)
@click.option('-m', '--metric', default='cosine', help='Distance metric used to compute distance matrix.', type=click.Choice(['cityblock','cosine','euclidean','l1','l2','manhattan','braycurtis','canberra','chebyshev','dice','hamming','haversine','infinity','jaccard','kulsinski','mahalanobis','matching','minkowski','rogerstanimoto','russellrao','seuclidean','sokalmichener','sokalsneath','wminkowski','ectd']), show_default=True)
@click.option('-min_c', '--min_cluster_size', default = 300, show_default=True, help='Minimum cluster size for hdbscan algorithm.')
@click.option('-min_s', '--min_samples', default = 150, show_default=True, help='Minimum number samples for hdbscan algorithm.')
@click.option('-nn', '--n_neighbors', default=10, help='Number of nearest neighbors in generation of nearest neighbor graph.', show_default=True)
@click.option('-scan','--hyperparameter_scan', is_flag=True, help='Whether to conduct hyperparameter scan of best clustering parameters.')
@click.option('-min_n', '--min_number_clusters', default = 3, show_default=True, help='Minimum number of clusters to find if doing hyperparameter scan. Parameters that produce fewer clusters face heavy penalization.')
@click.option('-low', '--low_counts', default='5,5,5', show_default=True, help='Comma delimited list of low bound on min_cluster_size, min_samples, and nearest neighbors respectively for hyperparameter scan.')
@click.option('-j', '--n_jobs', default=1, help='Number of jobs for TSNE transform.', show_default=True)
@click.option('-s', '--silhouette', is_flag=True, help='Use mean silhouette coefficient with mahalanobis distance as scoring metric for GA hyperparameter scan.')
@click.option('-v', '--validity', is_flag=True, help='Use hdbscan validity metric for clustering score. Takes precedent over silhouette score.')
def explore_kmers(ctx,work_dir,kmer_count_matrix,reduction_method,n_dimensions, kernel, metric, min_cluster_size,min_samples, n_neighbors, hyperparameter_scan, min_number_clusters, low_counts, n_jobs, silhouette, validity):
    """Perform dimensionality reduction on matrix of kmer counts versus genomes and cluster using a combination of genetic algorithm + density based clustering (hdbscan). Uncovers kmer conservation patterns/rules across different lines."""
    import hdbscan
    from sklearn.manifold import SpectralEmbedding#, TSNE
    from MulticoreTSNE import MulticoreTSNE as TSNE
    from sklearn.cluster import FeatureAgglomeration
    from sklearn.metrics import calinski_harabaz_score, silhouette_score
    from evolutionary_search import maximize
    import seaborn as sns
    # FIXME mahalanobis arguments to pass V, debug distance metrics
    # FIXME add ECTD as a distance metric? Feed as precomputed into hdbscan?
    hdbscan_metric = (metric if metric not in ['ectd','cosine','mahalanobis'] else 'precomputed')
    optional_arguments = dict()

    def cluster_data(t_data,min_cluster_size, min_samples, cluster_selection_method= 'eom'): # , n_neighbors = n_neighbors
        #print min_cluster_size, min_samples, kernel, n_neighbors
        labels = hdbscan.HDBSCAN(min_cluster_size = min_cluster_size, min_samples= min_samples, cluster_selection_method=cluster_selection_method, metric = hdbscan_metric, alpha = 1.0).fit_predict(t_data)
        #lp = LabelPropagation(kernel=kernel, n_neighbors = n_neighbors) # FIXME Try decision trees next, maybe just use highest chi square valued ones for training
        #lp.fit(t_data,labels) #kmer_count_matrix
        #labels = np.array(lp.predict(t_data))
        return labels
    scoring_method = lambda X, y: hdbscan.validity.validity_index(X,y,metric=hdbscan_metric) if validity else (silhouette_score(X,y,metric='precomputed' if metric =='mahalanobis' else 'mahalanobis',V=(np.cov(X,rowvar=False) if metric != 'mahalanobis' else '')) if silhouette else calinski_harabaz_score(X,y))

    def return_cluster_score(t_data,min_cluster_size, min_samples, cluster_selection_method): # , n_neighbors
        click.echo(' '.join(map(str,[min_cluster_size, min_samples, cluster_selection_method]))) # , n_neighbors
        labels = cluster_data(t_data,min_cluster_size, min_samples, cluster_selection_method) # , n_neighbors
        n_clusters = labels.max() + 1
        X = t_data if validity else t_data[labels != -1,:]
        y = labels if validity else labels[labels != -1]
        return scoring_method(X,y)/((1. if n_clusters >= min_number_clusters else float(min_number_clusters - n_clusters + 1))*(1.+len(labels[labels == -1])/float(len(labels)))) #FIXME maybe change t_data[labels != -1,:], labels[labels != -1] and (1.+len(labels[labels == -1])/float(len(labels)))

    def ectd_graph(t_data):
        paired = pairwise_distances(t_data)
        neigh = NearestNeighbors(n_neighbors=n_neighbors,metric='precomputed')
        neigh.fit(t_data)
        fit_data = neigh.kneighbors_graph(paired, mode='distance')
        fit_data = ( fit_data + fit_data.T )/2.
        min_span_tree = sps.csgraph.minimum_spanning_tree(paired).to_csc()
        min_span_tree = ( min_span_tree + min_span_tree.T )/2.
        return fit_data + min_span_tree

    sns.set(style="ticks")
    low_counts = map(int,low_counts.split(','))
    kmer_count_matrix = pd.read_csv(kmer_count_matrix,index_col = ['Unnamed: 0'])
    subgenome_names = list(kmer_count_matrix)
    labels_text = []
    for index, row in kmer_count_matrix.iterrows():
        labels_text.append(index+'<br>'+'<br>'.join(['%s: %s'%(subgenome,val) for subgenome,val in zip(subgenome_names,row.as_matrix().astype(str).tolist())]))#+'-'+','.join(subgenome_names+row.as_matrix().astype(str).tolist())) fixme ' ' ', '
    pickle.dump(np.array(labels_text),open(work_dir+'kmer_labels_coordinates.p','wb'))
    pickle.dump(kmer_count_matrix.idxmax(axis=1).as_matrix(),open(work_dir+'kmer_labels.p','wb'))
    transform_dict = {'kpca':KernelPCA(n_components=n_dimensions, kernel=kernel),'spectral':SpectralEmbedding(n_components=n_dimensions),'nmf':NMF(n_components=n_dimensions),'tsne':TSNE(n_components=n_dimensions,n_jobs=n_jobs), 'feature': FeatureAgglomeration(n_clusters=n_dimensions)}
    t_data = Pipeline([('scaler',StandardScaler(with_mean=False)),(reduction_method,transform_dict[reduction_method])]).fit_transform(kmer_count_matrix) # ,('spectral_induced',SpectralEmbedding(n_components=3))
    np.save(work_dir+'kmer_counts_pca_results.npy',t_data)
    if metric == 'ectd':
        t_data = ectd_graph(t_data)
    elif metric == 'cosine':
        t_data = pairwise_distances(t_data,metric='cosine')
    elif metric == 'mahalanobis':
        t_data = pairwise_distances(t_data,metric='mahalanobis',V=np.cov(t_data,rowvar=True))
    ctx.invoke(plotPositions,positions_npy=work_dir+'kmer_counts_pca_results.npy',labels_pickle=work_dir+'kmer_labels_coordinates.p',colors_pickle=work_dir+'kmer_labels.p',output_fname=work_dir+'subgenome_bio_rules_kmers.html')
    if hyperparameter_scan: # FIXME Test hyperparameter_scan, add ability to use label propagation, or scan for it or iterations of label propagation
        best_params, best_score, score_results, hist, log = maximize(return_cluster_score, dict(min_cluster_size = np.unique(np.linspace(low_counts[0],min_cluster_size,10).astype(int)).tolist(), min_samples = np.unique(np.linspace(low_counts[1],min_samples, 10).astype(int)).tolist(), cluster_selection_method= ['eom', 'leaf'] ), dict(t_data=t_data), verbose=True, n_jobs = 1, generations_number=8, gene_mutation_prob=0.45, gene_crossover_prob = 0.45) # n_neighbors = np.unique(np.linspace(low_counts[2], n_neighbors, 10).astype(int)).tolist()),
        labels = cluster_data(t_data,min_cluster_size=best_params['min_cluster_size'], min_samples=best_params['min_samples'], cluster_selection_method= best_params['cluster_selection_method']) # , n_neighbors = best_params['n_neighbors']
        print best_params, best_score, score_results, hist, log
    else:
        labels = cluster_data(t_data,min_cluster_size, min_samples)
    rules_orig = np.vectorize(lambda x: 'rule %d'%x)(labels)
    pickle.dump(rules_orig,open(work_dir+'rules.p','wb'))
    ctx.invoke(plotPositions,positions_npy=work_dir+'kmer_counts_pca_results.npy',labels_pickle=work_dir+'kmer_labels_coordinates.p',colors_pickle=work_dir+'rules.p',output_fname=work_dir+'subgenome_bio_rules_propagated_kmers.html')
    observed = kmer_count_matrix.as_matrix()
    print observed
    rules = np.array([rules_orig[idx] for idx in sorted(np.unique(rules_orig,return_index=True)[1])])
    rules_mean = [observed[rules_orig==rule,:]/observed[rules_orig==rule,:].sum(axis=1).astype(float)[:,None] for rule in rules]
    print rules_mean
    """
    for i, rule in enumerate(rules_mean):
        rule_name = rules[i].replace(' ','')
        rule = pd.DataFrame(rule,columns=subgenome_names).melt(id_vars = None, var_name='Genome Name', value_name='Normalized Counts')
        plt.figure()
        sns.boxplot(x='Normalized Counts',y='Genome Name', data=rule, palette="vlag") #whis=np.inf,
        sns.swarmplot(x='Normalized Counts', y='Genome Name', data=rule,
              size=2, color=".3", linewidth=0)
        sns.despine(trim=True, left=True)
        plt.savefig(work_dir+rule_name+'_genome_dominance.png',dpi=300)
    """ # FIXME use this to combine rules if they have matching normalized distributions, pairwise chi-square clustering of rules
    pd.DataFrame([rule.mean(axis=0) for rule in rules_mean],index=rules,columns=subgenome_names).to_csv(work_dir+'kmers_unsupervised_rules.csv')

    n_subgenomes = len(subgenome_names)
    #sum_count = kmer_count_matrix.as_matrix().sum(axis=1)
    print n_subgenomes
    expected = np.ones(observed.shape) * np.sum(observed,axis=0)/np.sum(observed,axis=0).sum() * observed.sum(axis=1)[:,np.newaxis] #np.ones(kmer_count_matrix.shape)/float(n_subgenomes) * kmer_count_matrix.as_matrix().sum(axis=1)[:,None]
    print expected
    chi2_arr = (observed - expected)**2/expected#np.apply_along_axis(lambda x: (x-expected*np.sum(x))**2/(expected*np.sum(x)),1,kmer_count_matrix.as_matrix())
    chi2_sum = chi2_arr.sum(axis=1)
    df2 = pd.DataFrame(chi2_arr,index=kmer_count_matrix.index.values,columns=[name+'-chi2' for name in subgenome_names])
    df3 = pd.concat([kmer_count_matrix,df2],axis=1,join='outer')
    df2['Sum'] = chi2_sum
    print df2, df3
    kmer_count_matrix['Rules'] = rules_orig
    #kmer_count_matrix = kmer_count_matrix.set_index(['Unnamed: 0'])
    kmer_count_matrix.to_csv(work_dir + 'kmer_master_matrix_rules.csv')
    for folder in ['rules_plots/','rules_plots_chi2/']:
        try:
            os.makedirs(work_dir+folder)
        except:
            pass
    ctx.invoke(plot_rules,work_dir=work_dir+'rules_plots/',rule_csv=work_dir + 'kmer_master_matrix_rules.csv')
    df2.to_csv(work_dir+'kmer_master_chi2_matrix.csv')
    df3.to_csv(work_dir+'kmer_master_count_chi2_matrix.csv')
    t_data = Pipeline([('scaler',StandardScaler(with_mean=False)),(reduction_method,transform_dict[reduction_method])]).fit_transform(df3)
    print t_data
    np.save(work_dir+'kmer_counts_pca_chi2_results.npy',t_data)
    if metric == 'ectd':
        t_data = ectd_graph(t_data)
    elif metric == 'cosine':
        t_data = pairwise_distances(t_data,metric='cosine')
    elif metric == 'mahalanobis':
        t_data = pairwise_distances(t_data,metric='mahalanobis',V=np.cov(t_data,rowvar=True))
    if hyperparameter_scan: # FIXME Test hyperparameter_scan, add ability to use label propagation, or scan for it or iterations of label propagation
        best_params, best_score, score_results, hist, log = maximize(return_cluster_score, dict(min_cluster_size = np.unique(np.linspace(low_counts[0],min_cluster_size,10).astype(int)).tolist(), min_samples = np.unique(np.linspace(low_counts[1],min_samples, 10).astype(int)).tolist(), cluster_selection_method= ['eom', 'leaf'] ), dict(t_data=t_data), verbose=True, n_jobs = 1, generations_number=8, gene_mutation_prob=0.45, gene_crossover_prob = 0.45) # n_neighbors = np.unique(np.linspace(low_counts[2], n_neighbors, 10).astype(int)).tolist()),
        labels = cluster_data(t_data,min_cluster_size=best_params['min_cluster_size'], min_samples=best_params['min_samples'], cluster_selection_method= best_params['cluster_selection_method']) # , n_neighbors = best_params['n_neighbors']
        print best_params, best_score, score_results, hist, log
    else:
        labels = cluster_data(t_data,min_cluster_size, min_samples)
    rules = np.vectorize(lambda x: 'rule %d'%x)(labels)
    df3['Rules'] = rules
    pickle.dump(rules,open(work_dir+'rules_chi2.p','wb'))
    ctx.invoke(plotPositions,positions_npy=work_dir+'kmer_counts_pca_chi2_results.npy',labels_pickle=work_dir+'kmer_labels_coordinates.p',colors_pickle=work_dir+'rules_chi2.p',output_fname=work_dir+'subgenome_bio_rules_kmers_chi2.html')
    df3.to_csv(work_dir+'kmer_master_count_chi2_matrix_rules.csv')
    ctx.invoke(plot_rules,work_dir=work_dir+'rules_plots_chi2/',rule_csv=work_dir + 'kmer_master_count_chi2_matrix_rules.csv')
    X = [observed[labels==label,:]/observed[labels==label,:] for label in range(labels.max()+1)]
    X_mean = np.vstack([x_s.mean(axis=0) for x_s in X])
    X_std = np.vstack([x_s.std(axis=0) for x_s in X])
    pd.DataFrame(X_mean,index=['rule_%d'%label for label in range(labels.max()+1)],columns=subgenome_names).to_csv(work_dir+'kmers_unsupervised_rules_chi2.csv')
    pd.DataFrame(X_std,index=['rule_%d'%label for label in range(labels.max()+1)],columns=subgenome_names).to_csv(work_dir+'kmers_unsupervised_rules_chi2_uncertainty.csv')
    # FIXME function: turn above into merging and splitting clusters based on heterogeneity (maybe use local PCA?), though no order, but maybe find way to order based on x-y-z
    # FIXME function: add ability to input consensus sequences and start to find rule and subclass breakdown, maybe subclass breakdown for each rule
    # FIXME fix above merging clusters method
    # FIXME add function to use user input for rule discovery, hypotheses user is looking for can also help with dimensionality breakdown and initial clustering, as well as postprocessing
    # FIXME comment and clean, also maybe make more command groups
    # FIXME check out penalization for genetic algorithm
    # FIXME add rule finding http://skope-rules.readthedocs.io/en/latest/auto_examples/plot_skope_rules.html#sphx-glr-auto-examples-plot-skope-rules-py , way to display rules http://skope-rules.readthedocs.io/en/latest/skope_rules.html
    # FIXME Euclidean commute time as distance metric, -> clustering via random walks
    # FIXME SVD + DQC instead of TSNE + HDBSCAN ?


@polycracker.command()
@click.option('-w', '--work_dir', default='./', show_default=True, help='Work directory where computations for plotting kmer count matrix is done.', type=click.Path(exists=False))
def find_rules(work_dir):
    """In development: Elucidate underlying rules of certain kmer conservation patterns."""
    import Orange
    from sklearn import tree
    df = pd.read_csv(work_dir+'kmer_master_count_chi2_matrix_rules.csv')
    X , y = df.iloc[:,1:-1].as_matrix(), df.iloc[:,-1].as_matrix()
    n_col = X.shape[1]
    print n_col
    X1 = X[:,:n_col/2]
    #print X1
    X1 /= X1.sum(axis=1).astype(float)[:, np.newaxis]
    X[:,:n_col/2] = X1
    #t_data = FeatureAgglomeration(n_clusters=n_col/2)
    clf = tree.DecisionTreeClassifier()
    clf.fit(X[df['Rules'].as_matrix() != 'rule -1'], y[df['Rules'].as_matrix() != 'rule -1'])
    tree.export_graphviz(clf, out_file=work_dir+'rules_graph.dot',
                         feature_names=list(df)[1:-1],
                         class_names=np.unique(y[df['Rules'].as_matrix() != 'rule -1']),
                         filled=True, rounded=True,
                         special_characters=True)
    subprocess.call('dot -Tpng %s -o %s'%(work_dir+'rules_graph.dot',work_dir+'rules_graph.png'),shell=True)
    df = df.rename(columns=dict(zip(list(df),['i#k-mer']+['C#'+ val for val in df.columns.values[1:-1]]+['cD#'+df.columns.values[-1]])))
    #print X1, df.iloc[:,1:n_col/2+1]
    df.iloc[:,1:n_col/2+1] = X1
    print df
    df.to_csv(work_dir+'orange_input_rules.csv',index=False, sep='\t')
    subprocess.call("grep -v 'rule -1' %s > %s"%(work_dir+'orange_input_rules.csv',work_dir+'orange_input_rules_no_out.csv'),shell=True)
    data = Orange.data.Table(work_dir+'orange_input_rules_no_out.csv')
    print data
    cn2_classifier = Orange.classification.rules.CN2Learner(data)
    with open(work_dir+'rules.txt','w') as f:
        for r in cn2_classifier.rules:
            f.write(Orange.classification.rules.rule_to_string(r)+'\n')


@polycracker.command()
@click.option('-w', '--work_dir', default='./', show_default=True, help='Work directory where computations for plotting kmer count matrix is done.', type=click.Path(exists=False))
@click.option('-n', '-n_rules', default = 10, show_default=True, help='Number of rules to find.')
def find_rules2(work_dir, n_rules):
    """In development: Elucidate underlying rules of certain kmer conservation patterns."""
    from skrules import SkopeRules
    rng = np.random.RandomState(42)
    df = pd.read_csv(work_dir+'kmer_master_count_chi2_matrix_rules.csv')
    clf = SkopeRules(feature_names = df.columns.values[:-1],random_state=rng, n_estimators=10, max_samples = 1)
    X , y = df.iloc[:,:-1].as_matrix(), df.iloc[:,-1].as_matrix()
    clf.fit(X[df['Rules'] != 'rule -1'],y[df['Rules'] != 'rule -1'])
    labels=clf.predict(X)
    for rule in clf.rules_[:n_rules]:
        print(rule[0])

@polycracker.command()
@click.option('-w', '--work_dir', default='./', show_default=True, help='Work directory where computations for plotting kmer count matrix is done.', type=click.Path(exists=False))
@click.option('-csv', '--rule_csv', default = './kmer_master_count_chi2_matrix_rules.csv', show_default = True, help='Kmer count matrix with appended rule labels. Default includes chi-squared values.', type=click.Path(exists=False))
def plot_rules(work_dir,rule_csv):
    """Plots normalized frequency distribution of select kmers across multiple genomes of certain rules/patterns."""
    df = pd.read_csv(rule_csv)
    X , y = df.iloc[:,1:-1].as_matrix(), df.iloc[:,-1].as_matrix()
    if 'kmer_master_count_chi2_matrix_rules.csv' in rule_csv:
        n_col = X.shape[1]
        X1 = X[:,:n_col/2]
        X1 /= X1.sum(axis=1).astype(float)[:, np.newaxis]
        #X[:,:n_col/2] = X1
    else:
        X1 = X / X.sum(axis=1)[:, np.newaxis].astype(float)
    col_names = list(df)[1:-1]
    for rule in set(y) - {'rule -1'}:
        plots = []
        x = X1[y == rule,:]
        for i, col in enumerate(col_names):
            plots.append(go.Box(y=x[:,i],name=col,boxpoints='all'))
        py.plot(go.Figure(data=plots),filename=work_dir+rule.replace(' ','_')+'.html',auto_open=False)

@polycracker.command()
def build_pairwise_align_similarity_structure(fasta_in):
    """Take consensus repeats, generate graph structure from sequence similarity, and cluster. Can be useful to find homologous repeats from different genomes."""
    from pyfaidx import Fasta
    from Bio import pairwise2
    f = Fasta(fasta_in)
    repeat_names = f.keys()
    similarity_mat = np.ones((len(repeat_names),)*2,dtype=np.float)
    diagonal_elements = zip(range(len(repeat_names)),range(len(repeat_names)))
    for i,j in list(combinations(range(len(repeat_names)),2)) + diagonal_elements:
        similarity_mat[i,j] = pairwise2.align.globalxx(str(f[repeat_names[i]][:]),str(f[repeat_names[j]][:]),score_only=True)
        if i != j:
            similarity_mat[j,i] = similarity_mat[i,j]
    for i,j in list(combinations(repeat_names,2)):# + diagonal_elements:
        similarity_mat[i,j] = similarity_mat[i,j]/np.sqrt(similarity_mat[i,i]*similarity_mat[j,j])
        if i != j:
            similarity_mat[j,i] = similarity_mat[i,j]
    #dissimilarity_matrix = 1. - similarity_mat
    #nn = NearestNeighbors(n_neighbors= 10,metric='precomputed').fit(dissimilarity_matrix)
    spec = SpectralClustering(n_clusters = 8, affinity='precomputed')
    labels = spec.fit_predict(similarity_mat)
    return repeat_names , similarity_mat, labels

@polycracker.command()
@click.pass_context
@click.option('-w', '--work_dir', default='./', show_default=True, help='Work directory where computations for merging of clusters is done.', type=click.Path(exists=False))
@click.option('-rf', '--repeat_fasta', default = '', help='Full path to repeat fasta file, output from repeat masker pipeline.', type=click.Path(exists=False))
@click.option('-m', '--blast_mem', default='100', help='Amount of memory to use for bbtools run. More memory will speed up processing.', show_default=True)
@click.option('-l', '--kmer_length', default=23, help='Length of kmers to find.', show_default=True)
@click.option('-r', '--rules_kmers', default = './kmer_master_matrix_rules.csv', show_default=True,help='Kmer count matrix with appended rule labels.', type=click.Path(exists=False))
@click.option('-gff', '--repeat_gff', default='', show_default=True, help='If repeat gff is submitted here, repeat fasta must be original genome, and non-consensus repeat sequences will be considered.', type=click.Path(exists=False))
@click.option('-motif', '--grab_motif', is_flag=True, help='Grab unique consensus repeat identifiers.')
@click.option('-dash', '--output_dash', is_flag=True, help='Output csv file for dash.')
def categorize_repeats(ctx,work_dir,repeat_fasta,blast_mem,kmer_length, rules_kmers, repeat_gff, grab_motif, output_dash):
    """Take outputs from denovo repeat finding/modeling and intersect kmers of particular conservation patterns with these repeats,
    either all iterations of a consensus repeat or consensus repeats themselves, and crosstabulate rule distribution with repeats/subclass."""
    from sklearn.preprocessing import LabelEncoder
    from pyfaidx import Fasta
    from sklearn.feature_extraction import DictVectorizer
    #from scipy.stats.contingency import expected_freq
    from sklearn.preprocessing import Normalizer
    import seaborn as sns

    try:
        os.makedirs(work_dir)
    except:
        pass

    def count_append(arr):
        d = defaultdict(lambda: 0)
        final_arr = []
        for element in arr.tolist():
            d[element] += 1
            final_arr.append(str(d[element])+'#'+element)
        return np.array(final_arr)

    def kmer_dict_gen(list_tuples):
        d = defaultdict(list)
        for key, val in list_tuples:
            d[key].append(val)
        return d

    def combine_dicts(d1,d2):
        return dict((k, d1.get(k,[]) + d2.get(k,[])) for k in set(d1).union(d2))

    # step one: classify repeats by kmer distribution to ID additional repeats belonging to subclass
    # step two: label these repeats by their kmers and find distribution of kmer rules for each subclass
    # FIXME reason why
    if repeat_gff:
        # extract sequences from original genome fasta and make new fasta file, call that one the repeat fasta
        subclass_motif = 'ID' if grab_motif else 'Subclass'
        df = pd.read_table(repeat_gff,sep='\t',skiprows=3,header=None,names=['Chr','xi','xf',subclass_motif],dtype={'Chr':str,'xi':float,'xf':str,subclass_motif:str},usecols=[0,3,4,8])#,columns=['Chr']+['x']*2+['xi','xf']+['x']*7+['Subclass'])
        #print df
        #df['xi':'xf'] = df['xi':'xf'].astype(int)
        df = df[np.isfinite(df['xi'])]
        df['xi'] = np.vectorize(lambda x: int(x)-1)(df['xi'])
        if grab_motif:
            df['ID'] = count_append(np.vectorize(lambda x: ':'.join(np.array(x.split())[[1,-1]]).replace('"','').replace('Motif:',''))(df['ID']))
        else:
            df['Subclass'] = count_append(np.vectorize(lambda x: x.split()[-1].replace('"',''))(df['Subclass']))
        #print df
        #df = df[['Chr','xi','xf','Subclass']]
        df.to_csv(work_dir+'repeat_extract.bed',sep='\t',index=False, header = False)
        subprocess.call('samtools faidx %s && bedtools getfasta -fi %s -fo %s -bed %s -name'%(repeat_fasta,repeat_fasta,work_dir+'extracted_repeats.fa',work_dir+'repeat_extract.bed'),shell=True)
        repeat_fasta = work_dir+'extracted_repeats.fa'
        repeat_names = df[subclass_motif].as_matrix()

    fasta = Fasta(repeat_fasta)
    if not repeat_gff:
        repeat_names = np.array(fasta.keys())
    blast_memStr = "export _JAVA_OPTIONS='-Xms5G -Xmx%sG'"%(blast_mem)
    if repeat_gff:
        df = pd.read_csv(rules_kmers,index_col=0)
        kmers = list(df.index)
        rule_mapping = zip(kmers,np.vectorize(lambda x: x.replace(' ','_'))(df['Rules']))
        with open(work_dir+repeat_fasta[repeat_fasta.rfind('/')+1:]+'.kcount.fa','w') as f:
            f.write('\n'.join(['>%s\n%s'%(rule+'@'+kmer,kmer) for kmer,rule in rule_mapping]))
    else:
        subprocess.call(blast_memStr + '&& kmercountexact.sh overwrite=true fastadump=f in=%s out=%s.kcount k=%d -Xmx100g'%(repeat_fasta,repeat_fasta,kmer_length),shell=True)
        subprocess.call("awk '{print $1}' %s > %s && dedupe.sh overwrite=true in=%s out=%s ac=f && rm %s"%(repeat_fasta, work_dir+'temp.fa',work_dir+'temp.fa',work_dir+'repeats.fa',work_dir+'temp.fa'), shell=True)

        #FIXME WIP below, also add splitting cluster ability
        ctx.invoke(kmer2Fasta,kmercount_path=work_dir, kmer_low_count=0, high_bool=0, kmer_high_count=100000000, sampling_sensitivity=1)
    ctx.invoke(blast_kmers,blast_mem=blast_mem,reference_genome=repeat_fasta,kmer_fasta=work_dir+repeat_fasta[repeat_fasta.rfind('/')+1:]+'.kcount.fa', output_file=work_dir+'repeat_blasted.sam')
    if output_dash:
        subprocess.call("awk -v OFS='\\t' '{split($6, a, "+'"="'+"); print $3, $4, $4 + a[1], $1 }' %s > %s"%(work_dir+'repeat_blasted.sam',work_dir+'repeat_blasted_dash.bed'),shell=True)
        repeat_lengths = dict(zip(os.popen("awk '{print $1}' %s"%repeat_fasta+'.fai').read().splitlines(),map(float,os.popen("awk '{print $2}' %s"%repeat_fasta+'.fai').read().splitlines())))
        df = pd.read_table(work_dir+'repeat_blasted_dash.bed',header=None,names=['Repeat','xi','xf','rule_kmer'],dtype=dict(Repeat=str,xi=float,xf=float,rule_kmer=str))
        df['length'] = np.vectorize(lambda x: repeat_lengths[x])(df['Repeat'])
        df['xm'] = (df['xi'] + df['xf']) / 2.
        df['rule'] = np.vectorize(lambda x: x.split('@')[0])(df['rule_kmer'])
        df['kmer'] = np.vectorize(lambda x: x.split('@')[1])(df['rule_kmer'])
        df['iteration'] = np.vectorize(lambda x: int(x.split('#')[0]))(df['Repeat'])
        df['Repeat'] = np.vectorize(lambda x: x.split('#')[1])(df['Repeat'])
        df['Subclass'] = np.vectorize(lambda x: x.split(':')[-1])(df['Repeat'])
        df['xm_length'] = df['xm']/df['length']
        df = df.drop(['xi','xf','rule_kmer'],axis=1).reindex(columns=['Subclass','Repeat','iteration','xm','length','xm_length','rule','kmer'])
        df.to_csv(work_dir+'dash_repeat_kmer_content.csv')
    else:
        ctx.invoke(blast2bed,blast_file=work_dir+'repeat_blasted.sam', bb=1 , low_memory=0, output_bed_file=work_dir+'repeat_blasted.bed', output_merged_bed_file=work_dir+'repeat_blasted_merged.bed', external_call=True)
        if not repeat_gff:
            kmers = np.array(os.popen("awk '{ print $1 }' %s"%(work_dir+repeat_fasta[repeat_fasta.rfind('/')+1:]+'.kcount')).read().splitlines())
            df = pd.read_csv(rules_kmers,index_col=0)
            excluded_kmers = set(kmers) - set(list(df.index))
            rule_mapping = dict(zip(list(df.index),df['Rules'])+zip(excluded_kmers,['rule -1']*len(excluded_kmers)))
            del df
        print repeat_names
        repeat_mapping = LabelEncoder()
        repeat_mapping.fit(repeat_names)
        if repeat_gff:
            subclasses = np.vectorize(lambda x: x.split('#')[1])(np.array(os.popen("awk '{ print $1 }' %s"%work_dir+'repeat_blasted_merged.bed').read().splitlines()))
            v = DictVectorizer(sparse=False,dtype=np.int)
            rule_encoding_info = [map(lambda x: tuple(x.split('@')),line.split(',')) for line in os.popen("awk '{ print $4 }' %s"%work_dir+'repeat_blasted_merged.bed').read().splitlines()]
            X = v.fit_transform([Counter(map(lambda x: x[0],line_info)) for line_info in rule_encoding_info])
            print X
            rule_set = v.get_feature_names()
            print rule_set
            subclass_set = set(subclasses)
            print subclass_set
            kmer_dicts = defaultdict(list)
            for i, list_tuples in enumerate(rule_encoding_info):
                kmer_dicts[subclasses[i]].append(kmer_dict_gen(list_tuples))
            for subclass in kmer_dicts:
                kmer_dicts[subclass] = { k:'\n'.join(['%s:%d'%(kmer,kcount) for kmer,kcount in Counter(v).items()]) for k,v in reduce(lambda x,y: combine_dicts(x,y),kmer_dicts[subclass]).items() }
            df_final2 = pd.DataFrame(kmer_dicts).transpose()
            df_final = pd.DataFrame(np.vstack(tuple([np.sum(X[subclasses == subclass,:],axis=0) for subclass in subclass_set])),index=list(subclass_set),columns=rule_set)
            df_final2 = df_final2.reindex(index=list(df_final.index.values),columns=list(df_final))
            subclass_counter = Counter(subclasses)
            df_final2['Element_Count'] = np.vectorize(lambda x: subclass_counter[x])(list(df_final2.index.values))
            df_final2 = df_final2.drop(['rule_-1'],axis=1)
            df_final2.to_csv(work_dir+'kmers_in_repeat_rule.csv')
        else:
            repeats_idx_bed = repeat_mapping.transform(np.array(os.popen("awk '{ print $1 }' %s"%work_dir+'repeat_blasted_merged.bed').read().splitlines()))
            subclasses = np.vectorize(lambda x: x.split('#')[1])(repeat_names)
            kmer_mapping = LabelEncoder()
            kmer_mapping.fit(kmers)
            data = sps.dok_matrix((len(repeat_names),len(kmers)),dtype=np.int)
            with open(work_dir+'repeat_blasted_merged.bed','r') as f:
                for i, line in enumerate(f):
                    ll = line.strip('\n').split()
                    d = Counter(ll[-1].split(','))
                    data[repeats_idx_bed[i],kmer_mapping.transform(d.keys())] = np.array(d.values())
            data = data.tocsr()
            rules = np.vectorize(lambda x: rule_mapping[x])(kmer_mapping.inverse_transform(range(len(kmers))))
            sparse_df = pd.SparseDataFrame(data,index=subclasses,columns=rules,default_fill_value=0)
            #print sparse_df
            df_final = sparse_df.groupby(sparse_df.columns, axis=1).sum().groupby(sparse_df.index).sum().to_dense().fillna(0)
        df_final = df_final.drop(['rule_-1'],axis=1)
        df_final.to_csv(work_dir+('repeat_rule_cross_tab.csv' if grab_motif and repeat_gff else 'subclass_rule_cross_tab.csv'))
        observed = df_final.as_matrix()
        pickle.dump(np.array(list(df_final)),open(work_dir+'rules.p','wb'))
        pickle.dump(np.array(list(df_final.index.values)),open(work_dir+'subclass.p','wb'))
        if not grab_motif:
            chi_sq, p, dof, expected = chi2_contingency(observed)
            plt.figure()
            sns.heatmap(observed/observed.sum(axis=1)[:,np.newaxis])
            plt.title('Chi-sq = %f, p=%f'%(chi_sq,p))
            plt.savefig(work_dir+'subclass_rule_cross_tab.png',dpi=300)
            plt.figure()
            ch2 = (observed-expected)**2/expected
            heat_plt = sns.heatmap(ch2)
            heat_plt.set(xticklabels=list(df_final),yticklabels=list(df_final.index.values))
            plt.title('Chi-sq = %f, p=%f'%(chi_sq,p))
            plt.savefig(work_dir+'subclass_rule_cross_tab_chi2.png',dpi=300)
            t_data = Pipeline([('norm',Normalizer()),('kpca',KernelPCA(n_components=3))]).fit_transform(observed)
            np.save(work_dir+'subclass_rules.npy',t_data)
            t_data = Pipeline([('norm',Normalizer()),('kpca',KernelPCA(n_components=3))]).fit_transform(observed.T)
            np.save(work_dir+'rules_subclass.npy',t_data)
            ctx.invoke(plotPositions,positions_npy=work_dir+'subclass_rules.npy',labels_pickle=work_dir+'subclass.p',colors_pickle='',output_fname=work_dir+'subclass_rules.html')
            ctx.invoke(plotPositions,positions_npy=work_dir+'rules_subclass.npy',labels_pickle=work_dir+'rules.p',colors_pickle='',output_fname=work_dir+'rules_subclass.html')
            #chi_sq, p, dof, expected = chi2_contingency(df_final.as_matrix()[:,1:])
            df_final.iloc[:,:] = expected#expected_freq(df_final.as_matrix()[:,1:])
            df_final.to_csv(work_dir+'subclass_rule_cross_tab_exp.csv')
            df_final.iloc[:,:] = ch2
            df_final.to_csv(work_dir+'subclass_rule_cross_tab_chi2.csv')
        elif grab_motif and repeat_gff:
            t_data = Pipeline([('norm',Normalizer()),('kpca',KernelPCA(n_components=3))]).fit_transform(observed)
            np.save(work_dir+'repeat_rules.npy',t_data)
            t_data = Pipeline([('norm',Normalizer()),('kpca',KernelPCA(n_components=3))]).fit_transform(observed.T)
            np.save(work_dir+'rules_repeat.npy',t_data)
            ctx.invoke(plotPositions,positions_npy=work_dir+'repeat_rules.npy',labels_pickle=work_dir+'subclass.p',colors_pickle='',output_fname=work_dir+'repeat_rules.html')
            ctx.invoke(plotPositions,positions_npy=work_dir+'rules_repeat.npy',labels_pickle=work_dir+'rules.p',colors_pickle='',output_fname=work_dir+'rules_repeat.html')
        # FIXME #1 maybe first establish voting system for consensus repeats, assign rules to consensus repeats
        # FIXME look at all consensus repeat types, find phylogeny, see if there are clade specific patterns in consensus repeats, maybe color top consensus repeats by rules, but this should favor certain rules over others
        # FIXME calculate chi-square for each distribution and see if it is different than sum of columns / expected frequency
        # FIXME could just be that there are more kmers that dominate a certain rule.. More kmers originally ID'd for a rule so blasted would yield more... Look at number of kmers for each rule, maybe normalize that way, and compare to overall distribution
        # FIXME do this for each genome and create function to compare distributions


@polycracker.command(name='plot_rules_chromosomes')
@click.pass_context
@click.option('-w', '--work_dir', default='./', show_default=True, help='Work directory for computations of spatial plotting of kmer rules.', type=click.Path(exists=False))
@click.option('-go', '--original_genome', help='Complete path to original, prechunked genome fasta', type=click.Path(exists=False))
@click.option('-csv', '--kmer_rule_matrix', default = './kmer_master_count_chi2_matrix_rules.csv', show_default = True, help='Kmer count matrix with appended rule labels. Default includes chi-squared values.', type=click.Path(exists=False))
@click.option('-m', '--blast_mem', default='100', help='Amount of memory to use for bbtools run. More memory will speed up processing.', show_default=True)
@click.option('-sl', '--split_length', default=75000, help='Length of intervals, bed files.', show_default=True)
def plot_rules_chromosomes(ctx,work_dir, original_genome, kmer_rule_matrix, blast_mem, split_length):
    """Plot distribution of rules/conservation pattern kmers across the chromosomes."""
    import seaborn as sns
    from sklearn.preprocessing import LabelEncoder
    # subset out kmers by rules >rule\nkmer
    original_genome = os.path.abspath(original_genome)
    subprocess.call('samtools faidx %s'%original_genome,shell=True)
    original_genome = original_genome.rsplit('/',1)
    if original_genome[0:-1]:
        fasta_path = original_genome[0] +'/'
    else:
        fasta_path = './'
    original_genome = original_genome[-1]
    work_dir += '/' if work_dir.endswith('/') else ''
    blast_path, bed_path, sort_path = tuple([work_dir+path for path in ['rule_blast/','rule_bed/', 'rule_sort/']])
    for path in [work_dir,blast_path, bed_path, sort_path]:
        try:
            os.makedirs(path)
        except:
            pass
    df = pd.read_csv(kmer_rule_matrix,index_col=0)
    kmers = list(df.index)
    if 1:
        rule_mapping = zip(kmers,np.vectorize(lambda x: x.replace(' ','_'))(df['Rules']))
        with open(blast_path+'kmer_rules.higher.kmers.fa','w') as f:
            f.write('\n'.join(['>%s\n%s'%(rule,kmer) for kmer,rule in rule_mapping if rule != 'rule_-1']))
        # blast these kmers across genome
        writeBlast(original_genome, blast_path, blast_path, fasta_path, 1, blast_mem)
        #ctx.invoke(blast2bed,blast_file=blast_path+'kmer_rules.higher.kmers.sam', bb=1 , low_memory=0, output_bed_file=work_dir+bed_path+'kmer_rules.bed', output_merged_bed_file=work_dir+bed_path+'kmer_rules_merged.bed', external_call=1)
        subprocess.call("awk -v OFS='\\t' '{ print $3, $4, $4 + 1, $1 }' %s > %s"%(blast_path+'kmer_rules.higher.kmers.sam',bed_path+'kmer_rules.bed'),shell=True)
        subprocess.call('cut -f 1-2 %s.fai > %s.genome'%(fasta_path+original_genome,work_dir + '/genome'),shell=True)
        subprocess.call('bedtools makewindows -g %sgenome.genome -w %d > %swindows.bed'%(work_dir,split_length,work_dir),shell=True)
        BedTool('%swindows.bed'%work_dir).sort().intersect(BedTool(bed_path+'kmer_rules.bed').sort(),wa=True,wb=True).sort().merge(c=7,o='collapse',d=-1).saveas(bed_path+'kmer_rules_merged.bed')
    # FIXME intersect with windows bed and merge with d=-1
    # FIXME then read last column and encode labels into matrix, to append to dataframe
    #FIXME create windows bed
    #blast2bed3(work_dir, blast_path, bed_path, sort_path, original_genome, 1, bedgraph=0)
    #ctx.invoke(generate_unionbed, bed3_directory=bed_path, original=1, split_length=split_length, fai_file=fasta_path+original_genome+'.fai', work_folder=work_dir)
    # plot results, one chromosome at time
    le = LabelEncoder()
    rules = [rule.replace(' ','_') for rule in sorted(df['Rules'].unique().tolist()) if rule != 'rule -1']
    #print rules
    le.fit(rules)
    df = pd.read_table(bed_path+'kmer_rules_merged.bed', names = ['chr','xi','xf','rule'], dtype = {'chr':str,'xi':np.int,'xf':np.int,'rule':str})
    #print df
    rule_count_mat = sps.dok_matrix((df.shape[0],len(rules)),dtype=np.int)
    for i,rule_dist in enumerate(df['rule']):
        d = Counter(rule_dist.split(','))
        rule_count_mat[i,le.transform(d.keys())] = np.array(d.values())

    df['xi'] = (df['xi'] + df['xf'])/2
    df = df.drop(['xf','rule'],axis=1)
    df = pd.concat([df,pd.SparseDataFrame(rule_count_mat,columns=rules,default_fill_value=0).to_dense()],axis=1)

    """
    df = pd.read_table(work_dir+'subgenomes.union.bedgraph', names = ['chr','xi','xf']+[rule for rule in rules if rule != 'rule -1'])
    #df = df.rename(columns=['chr','xi','xf']+[rule for rule in df['Rules'].unique.as_matrix().tolist() if rule != 'rule -1'])
    df.iloc[:,0:3] = np.array(map(lambda x: x.rsplit('_',2), df['chr'].as_matrix().tolist()))
    df.iloc[:,1:] = df.iloc[:,1:].as_matrix().astype(np.int)
    df['xi'] = (df['xi'] + df['xf'])/2
    df = df.drop(['xf'],axis=1)

    df = df.sort_values(['chr','xi'])
    # melt the dataframe and then use sns tsplot to plot all of these values"""
    #print df
    df = pd.melt(df, id_vars=['chr','xi'], value_vars=rules)#[rule for rule in rules if rule != 'rule -1'])
    #print df
    df = df.rename(columns = {'variable':'Rule','value':'Number_Hits','xi':'x_mean'})
    df['subject'] = 0
    #print df
    for chromosome in set(df['chr'].as_matrix()):
        print df[df['chr'].as_matrix()==chromosome]
        plt.figure()
        sns.tsplot(data=df[df['chr']==chromosome],condition='Rule',unit='subject',interpolate=True,legend=True,value='Number_Hits',time='x_mean')
        plt.savefig(work_dir+chromosome+'.png',dpi=300)


@polycracker.command(name='merge_split_kmer_clusters')
@click.pass_context
@click.option('-w', '--work_dir', default='./', show_default=True, help='Work directory where computations for merging of clusters is done.', type=click.Path(exists=False))
@click.option('-c', '--estimated_clusters', default=-1, show_default=True, help='Estimated number of clusters based on prior rule discovery. If set to -1, bases number of cluster selection on number already discovered.')
@click.option('-d', '--n_dimensions', default=3, help='Number of dimensions to reduce to.', show_default=True)
def merge_split_kmer_clusters(ctx,work_dir,estimated_clusters,n_dimensions):
    """In development: working on merging and splitting clusters of particular kmer conservation patterns acros multiple genomes."""
    import statsmodels.api as sm
    from scipy.stats import pearsonr
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

    def linear_test(x, y, s_x, s_y):
        # must have high positive r value, reduced chi-square close to one to merge
        # expected equation is y=x for clusters to be similar, find if slope = 1 and intercept = 0
        print x,y,s_x,s_y
        R_mat = np.ones((2,2))/np.sqrt(2)
        R_mat[1,0] = -R_mat[1,0]
        X = np.vstack((x,y))
        sX = np.vstack((s_x,s_y))
        X = np.dot(R_mat,X)
        sX = np.dot(R_mat,sX)
        results_y = sm.WLS(X[1,:],sm.add_constant(X[0,:]),weights=1./sX[1,:]).fit()
        results_x = sm.WLS(X[0,:],sm.add_constant(X[1,:]),weights=1./sX[0,:]).fit()
        print(results_x.summary())
        print(results_y.summary())
        #f1 = np.polyval(np.polyfit(x,y,deg=1),x) # s_y
        #f2 = np.polyval(np.polyfit(y,x,deg=1),y) # s_x
        #chi2_y_reduced = (f1-y)**2/s_y/(len(y) - 2)
        #chi2_x_reduced = (f2-x)**2/s_x/(len(x) - 2)
        conditional = np.all(np.hstack((results_y.pvalues,results_x.pvalues)) > 0.05)
        print conditional
        return conditional
    rules_df = pd.read_csv(work_dir+'kmer_master_count_chi2_matrix_rules.csv', index_col=0)
    df = rules_df.iloc[:,:-1]
    df_train = df.iloc[rules_df['Rules'] != 'rule -1',:]
    df_test = df.iloc[rules_df['Rules'] == 'rule -1',:]
    rules_mean = pd.read_csv(work_dir+'kmers_unsupervised_rules_chi2.csv')
    rules_std = pd.read_csv(work_dir+'kmers_unsupervised_rules_chi2_uncertainty.csv')
    X_mean = rules_mean.to_matrix()
    X_std = rules_std.to_matrix()
    model = Pipeline([('scaler',StandardScaler()),('lda',LDA(n_components=n_dimensions))])
    model.fit(df_train)
    t_data = model.transform(df)
    np.save(work_dir+'LDA_kmers.npy',t_data)
    ctx.invoke(plotPositions,positions_npy=work_dir+'LDA_kmers.npy',labels_pickle=work_dir+'kmer_labels_coordinates.p',colors_pickle=work_dir+'rules_chi2.p',output_fname=work_dir+'subgenome_bio_rules_kmers_chi2.html')
    # combine rules
    merged_clusters = []
    for i,j in combinations(range(len(set(rules_df['Rules'].to_matrix()))), 2): # labels.max()+1
        if pearsonr(X_mean[i,:],X_mean[j,:]) > 0.7 and linear_test(X_mean[i,:], X_mean[j,:], X_std[i,:], X_std[j,:]):
            merged_clusters.append((i,j))
    #labels = BayesianGaussianMixture(n_components=(len(set(rules_df['Rules'].to_matrix())) if estimated_clusters == -1 else estimated_clusters))
    print 'MERGED: ', merged_clusters

##################################################################################

###################################### DASH ######################################


@polycracker.command(name='return_dash_data_structures')
@click.pass_context
@click.option('-m', '--blast_mem', default='100', help='Amount of memory to use for bbtools run. More memory will speed up processing.', show_default=True)
@click.option('-r', '--reference_genome', help='Genome to blast against.', type=click.Path(exists=False))
@click.option('-o', '--output_dir', default='./', show_default=True, help='Work directory for computations and outputs.', type=click.Path(exists=False))
@click.option('-sl', '--split_length', default=75000, help='Length of intervals in bedgraph files.', show_default=True)
@click.option('-npy', '--kmer_pca_data', default='./kmer_counts_pca_results.npy', show_default=True, help='Location of pca of kmer count matrix.', type=click.Path(exists=False))
@click.option('-kl', '--kmer_pca_labels', default='./kmer_labels_coordinates.p', show_default=True, help='Location of kmer labels pickle for each pca datapoint, eg. ATTTCGGCGAT Bd: 10, Bs: 20, ABRD: 40.', type=click.Path(exists=False))
@click.option('-kr', '--kmer_rules_pickle', default='./rules.p', show_default=True, help='Location of kmer rules pickle for each pca datapoint, eg.rule 3.', type=click.Path(exists=False))
@click.option('-csv', '--kmer_rule_matrix', default = './kmer_master_count_chi2_matrix_rules.csv', show_default = True, help='Kmer count matrix with appended rule labels. Default includes chi-squared values.', type=click.Path(exists=False))
def return_dash_data_structures(ctx,blast_mem,reference_genome,output_dir,split_length,kmer_pca_data,kmer_pca_labels,kmer_rules_pickle,kmer_rule_matrix):
    """Return dash data structures needed to run dash app. Copy them over to a directory to be referenced by app or uploaded to Heroku for dash app deployment."""
    from sklearn.preprocessing import LabelEncoder
    output_dir +='/'
    final_output_dir = output_dir + 'final_outputs/'
    if reference_genome != 'no_test':
        reference_genome = os.path.abspath(reference_genome)
    else:
        reference_genome = ''
    for path in [output_dir,final_output_dir]:
        try:
            os.makedirs(path)
        except:
            pass
    df = pd.read_csv(kmer_rule_matrix,index_col=0)
    df.to_csv(final_output_dir+kmer_rule_matrix.rsplit('/',1)[-1])
    kmers = list(df.index)
    #FIXME concatenate/stack below
    t_data = np.load(kmer_pca_data)
    if t_data.shape[1] > 3:
        t_data = KernelPCA(n_components=3).fit_transform(t_data)
    #print map(lambda x: np.array(x).shape,[list(df.index),pickle.load(open(kmer_pca_labels,'rb')),pickle.load(open(kmer_rules_pickle,'rb')),np.load(kmer_pca_data)])
    pca_data_df = pd.DataFrame(np.hstack([np.array(list(df.index))[:,np.newaxis],np.array(pickle.load(open(kmer_pca_labels,'rb')))[:,np.newaxis],np.array(pickle.load(open(kmer_rules_pickle,'rb')))[:,np.newaxis],t_data]),columns=['kmers','label','rule','x','y','z'])
    print pca_data_df
    pca_data_df.to_csv(final_output_dir+'pca_data.csv')
    if reference_genome:
        if 1:
            rule_mapping = zip(kmers,pca_data_df['rule'].as_matrix().tolist())
            with open(output_dir+'kmer_rules.fa','w') as f:
                f.write('\n'.join(['>%s\n%s'%(kmer,kmer) for kmer,rule in rule_mapping if rule != 'rule_-1']))
            subprocess.call('samtools faidx %s'%(reference_genome),shell=True)
            ctx.invoke(blast_kmers,blast_mem=blast_mem,reference_genome=reference_genome,kmer_fasta=output_dir+'kmer_rules.fa', output_file=output_dir+'kmer_rules.sam')
            subprocess.call("awk -v OFS='\\t' '{ print $3, $4, $4 + 1, $1 }' %s > %s"%(output_dir+'kmer_rules.sam',output_dir+'kmer_rules.bed'),shell=True)
            subprocess.call('samtools faidx %s && cut -f 1-2 %s.fai > %s.genome'%(reference_genome,reference_genome,output_dir + '/genome'),shell=True)
            subprocess.call('bedtools makewindows -g %sgenome.genome -w %d > %swindows.bed'%(output_dir,split_length,output_dir),shell=True)
            BedTool('%swindows.bed'%output_dir).sort().intersect(BedTool(output_dir+'kmer_rules.bed').sort(),wa=True,wb=True).sort().merge(c=7,o='collapse',d=-1).saveas(output_dir+'kmer_rules_merged.bed')
        le = LabelEncoder()
        le.fit(kmers)
        df = pd.read_table(output_dir+'kmer_rules_merged.bed', names = ['chr','xi','xf','kmers'], dtype = {'chr':str,'xi':np.int,'xf':np.int,'rule':str})
        if os.path.exists(final_output_dir+'kmer.count.npz'):
            rule_count_mat = sps.load_npz(final_output_dir+'kmer.count.npz')
            print rule_count_mat
        else:
            rule_count_mat = sps.dok_matrix((df.shape[0],len(kmers)),dtype=np.int)
            for i,rule_dist in enumerate(df['kmers']):
                d = Counter(rule_dist.split(','))
                rule_count_mat[i,le.transform(d.keys())] = np.array(d.values())
            rule_count_mat = rule_count_mat.tocsr()
            print rule_count_mat
            sps.save_npz(final_output_dir+'kmer.count.npz',rule_count_mat)
        df['xi'] = (df['xi'] + df['xf'])/2
        df = df.drop(['xf','kmers'],axis=1)
        df.to_csv(final_output_dir+'kmer.count.coords.csv')
        df2 = pd.SparseDataFrame(rule_count_mat,columns=kmers,default_fill_value=0)#pd.SparseDataFrame(sps.hstack([sps.csr_matrix(df['xi'].as_matrix()).T,rule_count_mat]),index=df['chr'].as_matrix().tolist(),columns=['xi']+list(kmers),default_fill_value=0).reset_index().rename(columns={'index':'chr'})
        df2.insert(0,'chr',df['chr'].as_matrix())
        df2.insert(1,'xi',df['xi'].as_matrix())
        df2.to_pickle(final_output_dir+'sparse_kmer_count_matrix.p')


@polycracker.command()
@click.option('-w', '--work_dir', default='./', show_default=True, help='Work directory where computations for plotting kmer count matrix is done.', type=click.Path(exists=False))
@click.option('-csv', '--kmer_count_matrix', default='./kmer_master_count_matrix.csv', show_default=True, help='Kmer count matrix.', type=click.Path(exists=False))
@click.option('-r', '--reduction_method', default='tsne', show_default=True, help='Type of dimensionality reduction technique to use.', type=click.Choice(['tsne','kpca', 'spectral', 'nmf', 'feature']))
@click.option('-d', '--n_dimensions', default=3, help='Number of dimensions to reduce to.', show_default=True)
@click.option('-k', '--kernel', default='cosine', help='Kernel for KPCA. Cosine is particularly effective.', type=click.Choice(['linear','poly','rbf','sigmoid','cosine']), show_default=True)
@click.option('-m', '--metric', default='cosine', help='Distance metric used to compute distance matrix.', type=click.Choice(['cityblock','cosine','euclidean','l1','l2','manhattan','braycurtis','canberra','chebyshev','dice','hamming','haversine','infinity','jaccard','kulsinski','mahalanobis','matching','minkowski','rogerstanimoto','russellrao','seuclidean','sokalmichener','sokalsneath','wminkowski','ectd']), show_default=True)
@click.option('-min_c', '--min_cluster_size', default = 300, show_default=True, help='Minimum cluster size for hdbscan algorithm.')
@click.option('-min_s', '--min_samples', default = 150, show_default=True, help='Minimum number samples for hdbscan algorithm.')
@click.option('-nn', '--n_neighbors', default=10, help='Number of nearest neighbors in generation of nearest neighbor graph.', show_default=True)
@click.option('-scan','--hyperparameter_scan', is_flag=True, help='Whether to conduct hyperparameter scan of best clustering parameters.')
@click.option('-min_n', '--min_number_clusters', default = 3, show_default=True, help='Minimum number of clusters to find if doing hyperparameter scan. Parameters that produce fewer clusters face heavy penalization.')
@click.option('-low', '--low_counts', default='5,5,5', show_default=True, help='Comma delimited list of low bound on min_cluster_size, min_samples, and nearest neighbors respectively for hyperparameter scan.')
@click.option('-j', '--n_jobs', default=1, help='Number of jobs for TSNE transform.', show_default=True)
@click.option('-s', '--silhouette', is_flag=True, help='Use mean silhouette coefficient with mahalanobis distance as scoring metric for GA hyperparameter scan.')
@click.option('-v', '--validity', is_flag=True, help='Use hdbscan validity metric for clustering score. Takes precedent over silhouette score.')
def dash_genetic_algorithm_hdbscan_test(work_dir,kmer_count_matrix,reduction_method,n_dimensions,kernel,metric,min_cluster_size,min_samples,n_neighbors,hyperparameter_scan,min_number_clusters,low_counts,n_jobs,silhouette,validity):
    """Save labels of all hdbscan runs, generate distance matrix for input into dash app. Output distance matrix, dataframe of parameters and score, and matrix of labels that produce distance matrix, referenced by parameters"""
    import hdbscan
    from sklearn.manifold import SpectralEmbedding#, TSNE
    from MulticoreTSNE import MulticoreTSNE as TSNE
    from sklearn.cluster import FeatureAgglomeration
    from sklearn.metrics import calinski_harabaz_score, silhouette_score
    from evolutionary_search import maximize
    import seaborn as sns
    from sklearn.metrics import adjusted_mutual_info_score as AMI
    # FIXME mahalanobis arguments to pass V, debug distance metrics
    # FIXME add ECTD as a distance metric? Feed as precomputed into hdbscan?
    hdbscan_metric = (metric if metric not in ['ectd','cosine','mahalanobis'] else 'precomputed')
    all_labels = defaultdict(list)
    global count
    count = 0

    def cluster_data(t_data,min_cluster_size, min_samples, cluster_selection_method= 'eom'): # , n_neighbors = n_neighbors
        #print min_cluster_size, min_samples, kernel, n_neighbors
        labels = hdbscan.HDBSCAN(min_cluster_size = min_cluster_size, min_samples= min_samples, cluster_selection_method=cluster_selection_method, metric = hdbscan_metric, alpha = 1.0).fit_predict(t_data)
        #lp = LabelPropagation(kernel=kernel, n_neighbors = n_neighbors) # FIXME Try decision trees next, maybe just use highest chi square valued ones for training
        #lp.fit(t_data,labels) #kmer_count_matrix
        #labels = np.array(lp.predict(t_data))
        return labels

    scoring_method = lambda X, y: hdbscan.validity.validity_index(X,y,metric=hdbscan_metric) if validity else (silhouette_score(X,y,metric='precomputed' if metric =='mahalanobis' else 'mahalanobis',V=(np.cov(X,rowvar=False) if metric != 'mahalanobis' else '')) if silhouette else calinski_harabaz_score(X,y))

    def return_cluster_score(t_data,min_cluster_size, min_samples, cluster_selection_method): # , n_neighbors
        global count
        click.echo(' '.join(map(str,[min_cluster_size, min_samples, cluster_selection_method]))) # , n_neighbors
        labels = cluster_data(t_data,min_cluster_size, min_samples, cluster_selection_method) # , n_neighbors
        n_clusters = labels.max() + 1
        X = t_data if validity else t_data[labels != -1,:]
        y = labels if validity else labels[labels != -1]
        score = scoring_method(X,y)/((1. if n_clusters >= min_number_clusters else float(min_number_clusters - n_clusters + 1))*(1.+len(labels[labels == -1])/float(len(labels)))) #FIXME maybe change t_data[labels != -1,:], labels[labels != -1] and (1.+len(labels[labels == -1])/float(len(labels)))
        all_labels['%d_%d_%d_%s'%(count,min_cluster_size, min_samples, cluster_selection_method)]=[labels,score]
        count += 1
        return score

    def ectd_graph(t_data):
        paired = pairwise_distances(t_data)
        neigh = NearestNeighbors(n_neighbors=n_neighbors,metric='precomputed')
        neigh.fit(t_data)
        fit_data = neigh.kneighbors_graph(paired, mode='distance')
        fit_data = ( fit_data + fit_data.T )/2.
        min_span_tree = sps.csgraph.minimum_spanning_tree(paired).to_csc()
        min_span_tree = ( min_span_tree + min_span_tree.T )/2.
        return fit_data + min_span_tree

    sns.set(style="ticks")
    low_counts = map(int,low_counts.split(','))
    kmer_count_matrix = pd.read_csv(kmer_count_matrix,index_col = ['Unnamed: 0'])
    subgenome_names = list(kmer_count_matrix)
    labels_text = []
    for index, row in kmer_count_matrix.iterrows():
        labels_text.append(index+'<br>'+'<br>'.join(['%s: %s'%(subgenome,val) for subgenome,val in zip(subgenome_names,row.as_matrix().astype(str).tolist())]))#+'-'+','.join(subgenome_names+row.as_matrix().astype(str).tolist())) fixme ' ' ', '
    pickle.dump(np.array(labels_text),open(work_dir+'kmer_labels_coordinates.p','wb'))
    pickle.dump(kmer_count_matrix.idxmax(axis=1).as_matrix(),open(work_dir+'kmer_labels.p','wb'))
    transform_dict = {'kpca':KernelPCA(n_components=n_dimensions, kernel=kernel),'spectral':SpectralEmbedding(n_components=n_dimensions),'nmf':NMF(n_components=n_dimensions),'tsne':TSNE(n_components=n_dimensions,n_jobs=n_jobs), 'feature': FeatureAgglomeration(n_clusters=n_dimensions)}
    t_data = Pipeline([('scaler',StandardScaler(with_mean=False)),(reduction_method,transform_dict[reduction_method])]).fit_transform(kmer_count_matrix) # ,('spectral_induced',SpectralEmbedding(n_components=3))
    #np.save(work_dir+'kmer_counts_pca_results.npy',KernelPCA(n_components=3).fit_transform(t_data) if t_data.shape[1] > 3 else t_data)
    pd.DataFrame(np.hstack((np.array(labels_text)[:,np.newaxis],KernelPCA(n_components=3).fit_transform(t_data) if t_data.shape[1] > 3 else t_data)),columns = ['labels','x','y','z']).to_csv(work_dir+'pca_output.csv')
    if metric == 'ectd':
        t_data = ectd_graph(t_data)
    elif metric == 'cosine':
        t_data = pairwise_distances(t_data,metric='cosine')
    elif metric == 'mahalanobis':
        t_data = pairwise_distances(t_data,metric='mahalanobis',V=np.cov(t_data,rowvar=True))
    if 1: # FIXME Test hyperparameter_scan, add ability to use label propagation, or scan for it or iterations of label propagation
        best_params, best_score, score_results, hist, log = maximize(return_cluster_score, dict(min_cluster_size = np.unique(np.linspace(low_counts[0],min_cluster_size,25).astype(int)).tolist(), min_samples = np.unique(np.linspace(low_counts[1],min_samples, 25).astype(int)).tolist(), cluster_selection_method= ['eom', 'leaf'] ), dict(t_data=t_data), verbose=True, n_jobs = 1, population_size=15, generations_number=7, gene_mutation_prob=0.3, gene_crossover_prob = 0.3)#15 7 fixme <--add these back, also begin to implement dash app, note: back up all final poly runs to disk... # n_neighbors = np.unique(np.linspace(low_counts[2], n_neighbors, 10).astype(int)).tolist()),
        labels = cluster_data(t_data,min_cluster_size=best_params['min_cluster_size'], min_samples=best_params['min_samples'], cluster_selection_method= best_params['cluster_selection_method']) # , n_neighbors = best_params['n_neighbors']
        print best_params, best_score, score_results, hist, log
    else:
        labels = cluster_data(t_data,min_cluster_size, min_samples)
    rules_orig = np.vectorize(lambda x: 'rule %d'%x)(labels)
    pickle.dump(rules_orig,open(work_dir+'rules.p','wb'))
    gen = defaultdict(list)
    indivs = np.array(all_labels.keys())
    indivs_vals = np.vectorize(lambda x: int(x[:x.find('_')]))(indivs)
    indivs = indivs[np.argsort(indivs_vals)]
    indivs_vals = indivs_vals[np.argsort(indivs_vals)]
    count = 0
    print list(enumerate(log))
    for i,generation in enumerate(log):
        print count
        gen[i] = indivs[count:count+generation['nevals']]#np.intersect1d(indivs_vals,np.arange(count,count+generation['nevals']))]
        count += generation['nevals']
    # FIXME generate dataframe
    # FIXME df = pd.DataFrame([[generation,int(parameters[:parameters.find('_')]),parameters,all_labels[parameters][1]]+parameters.split('_')[1:] for parameters in gen[generation] for generation in gen],columns = ['generation','individual','parameters','score','min_cluster_size', 'min_samples', 'cluster_selection_method'])
    # FIXME TypeError: unhashable type: 'dict'
    #print gen
    #print [gen[generation] for generation in gen]
    #print [all_labels[gen[generation][0]] for generation in gen]
    #print gen[0]
    #print all_labels
    #print [all_labels[parameters][1] for parameters in gen[0].tolist()]
    #print [all_labels[parameters][1] for parameters in gen[0]]
    generation_data = []
    for generation in gen:
        for parameters in gen[generation]:
            generation_data.append([generation,int(parameters[:parameters.find('_')]),parameters,all_labels[parameters][1]]+parameters.split('_')[1:])
    # [[generation,int(parameters[:parameters.find('_')]),parameters,all_labels[parameters][1]]+parameters.split('_')[1:] for parameters in gen[generation] for generation in gen]
    df = pd.DataFrame(generation_data,columns = ['generation','individual','parameters','score','min_cluster_size', 'min_samples', 'cluster_selection_method'])
    print df
    #pickle.dump(all_labels,open(work_dir+'all_labels.p','wb'))
    all_labels = pd.DataFrame(np.array([all_labels[indiv][0] for indiv in indivs]).T,columns = indivs)
    df.to_csv(work_dir+'generations.csv')
    all_labels.to_csv(work_dir+'db_labels.csv')
    distance_mat = pd.DataFrame(np.zeros((len(indivs),len(indivs))),index=indivs,columns=indivs)
    for i,j in list(combinations(indivs,2)):
        distance_mat.loc[i,j] = 1.-AMI(all_labels[i],all_labels[j])
        distance_mat.loc[j,i] = distance_mat.loc[i,j]
    distance_mat.to_csv(work_dir+'distance_mat.csv')
    #distance_mat = similarity_mat
    #distance_mat.iloc[:,:] = 1. - distance_mat.as_matrix()
    # FIXME feed distance matrix, generations, db_labels matrix, and pca matrix into dash app, subset by generation, score, etc... also kmer coordinate labels


@polycracker.command(name='dash_genome_quality_assessment')
@click.pass_context
@click.option('-w', '--work_dir', default='./', show_default=True, help='Work directory where computations for finding array of kmers versus prescaffolded genomes with unassigned sequences.', type=click.Path(exists=False))
@click.option('-csv', '--kmer_rule_matrix', default = './kmer_master_matrix_rules.csv', show_default = True, help='Kmer count matrix with appended rule labels.', type=click.Path(exists=False))
@click.option('-g','--pre_scaffolded_genomes', default = 'genome1:./path/genome_1_fname.fa,genome2:./path/genome_2_fname.fa,genome3:./path/genome_3_fname.fa',show_default=True,help="Comma delimited dictionary of genome names and corresponding genomes. Genomes should be assemblies prior to polyCRACKER/bbtools binning and scaffolding. Can input './path/*.fa[sta]' to input all genomes in path.",type=click.Path(exists=False))
@click.option('-m', '--blast_mem', default='100', help='Amount of memory to use for bbtools run. More memory will speed up processing.', show_default=True)
def dash_genome_quality_assessment(ctx,work_dir,kmer_rule_matrix,pre_scaffolded_genomes,blast_mem):
    """Input pre chromosome level scaffolded genomes, before split by ploidy, and outputs frequency distribution of select kmers.
    Used to compare this distribution of kmers to that found from comparing post-scaffolded polyploid subgenomes.
    The scaffolding, if reference based, may be biased and missing key repeat information, so comparing to prescaffolded genomes may show whether repeat info was lost during scaffolding for important words."""
    import glob
    work_dir += '/'
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    df = pd.read_csv(kmer_rule_matrix, index_col = 0)
    genomes = dict(map(lambda x: tuple(x.split(':')),pre_scaffolded_genomes.split(','))) if '*' not in pre_scaffolded_genomes else {genome.rsplit('/')[-1]:genome for genome in glob.glob(pre_scaffolded_genomes)}
    print genomes
    kmers = list(df.index)
    with open(work_dir+'kmer_fasta.fa','w') as f:
        f.write('\n'.join(['>%s\n%s'%(kmer,kmer) for kmer in kmers]))
    genomes_dict = {k:{kmer:0 for kmer in kmers} for k in genomes.keys()}
    df2 = pd.DataFrame(df['Rules'],index=kmers,columns=['Rules'])
    #for genome in genomes_dict:
    #    df2[genome] = 0
    kmer_length = int(np.mean(map(len,kmers)))
    blast_memStr = "export _JAVA_OPTIONS='-Xms5G -Xmx%sG'"%(blast_mem)
    for genome in genomes:
        subprocess.call(blast_memStr+' && kmercountexact.sh mincount=%d overwrite=true fastadump=f in=%s out=%s k=%d'%(5,genomes[genome],work_dir+genome+'.kcount',kmer_length),shell=True)
        # fixme kmers found from bbmap are different than ones found in kmercountexact
        #ctx.invoke(blast_kmers,blast_mem=blast_mem,reference_genome=genomes[genome],kmer_fasta=work_dir+'kmer_fasta.fa', output_file=work_dir+genome+'_blasted.sam',kmer_length=8)
        #genomes_dict[genome].update(Counter(os.popen("awk '{ print $1 }' %s"%(work_dir+genome+'_blasted.sam')).read().splitlines()))
        genomes_dict[genome].update(dict(zip(os.popen("awk '{ print $1 }' %s"%work_dir+genome+'.kcount').read().splitlines(),os.popen("awk '{ print $2 }' %s"%work_dir+genome+'.kcount').read().splitlines())))
        df2[genome] = pd.DataFrame.from_dict(genomes_dict[genome],orient='index',dtype=np.int).reindex(index=kmers)
    df2.to_csv(work_dir+'genome_quality_check.csv')


@polycracker.command(name='correct_kappa')
@click.pass_context
@click.option('-dict','--comparisons_dict', default='subgenome_1:progenitorA,subgenome_2:progenitorB,subgenome_3:speciesA' , show_default=True, help='MANDATORY: Comma delimited mapping of inferred subgenome names output from polycracker to Progenitor/Species labels.', type=click.Path(exists=False))
@click.option('-p0','--scaffolds_pickle', default='scaffolds_stats.p', show_default=True, help='Pickle file containing the original scaffold names.',  type=click.Path(exists=False))
@click.option('-p1','--polycracker_pickle', default='scaffolds_stats.poly.labels.p', show_default=True, help='Pickle file generated from final_stats. These are polycracker results.',  type=click.Path(exists=False))
@click.option('-p2','--progenitors_pickle', default='scaffolds_stats.progenitors.labels.p', show_default=True, help='Pickle file generated from final_stats. These are progenitor mapping results.',  type=click.Path(exists=False))
@click.option('-r', '--from_repeat', is_flag=True, help='From repeat subgenome extraction.')
@click.option('-w','--work_dir', default='./', show_default=True, help='Work directory.',  type=click.Path(exists=False))
def correct_kappa(ctx,comparisons_dict,scaffolds_pickle,polycracker_pickle,progenitors_pickle,from_repeat, work_dir):
    """Find corrected cohen's kappa score. Used to test final_stats."""
    from sklearn.metrics import cohen_kappa_score
    scaffold_len = lambda scaffold: int(scaffold.split('_')[-1])-int(scaffold.split('_')[-2])
    load = lambda f: pickle.load(open(f,'rb'))
    scaffolds = load(scaffolds_pickle)
    weights = np.vectorize(scaffold_len)(scaffolds)
    weights_new = weights / float(np.sum(weights))
    polycracker2ProgSpec = {subgenome:progenitor_species for subgenome,progenitor_species in [tuple(mapping.split(':')) for mapping in comparisons_dict.split(',')]+[('ambiguous','ambiguous')]}
    if from_repeat:
        ctx.invoke(convert_subgenome_output_to_pickle,input_dir=polycracker_pickle, scaffolds_pickle=scaffolds_pickle, output_pickle=work_dir+'/scaffolds.repeats.labels.p')
        ctx.invoke(convert_subgenome_output_to_pickle,input_dir=progenitors_pickle, scaffolds_pickle=scaffolds_pickle, output_pickle=work_dir+'/progenitors.scaffolds.repeats.labels.p')
        polycracker_pickle = work_dir+'/scaffolds.repeats.labels.p'
        progenitors_pickle = work_dir+'/progenitors.scaffolds.repeats.labels.p'
    y_polycracker = np.vectorize(lambda x: polycracker2ProgSpec[x])(load(polycracker_pickle))
    y_progenitors = load(progenitors_pickle)
    a = y_progenitors != 'ambiguous'
    b = y_polycracker != 'ambiguous'
    sequence_in_common = (a & b)
    labels = np.unique(np.union1d(np.unique(y_progenitors),np.unique(y_polycracker)))
    cohen = cohen_kappa_score(y_progenitors[sequence_in_common],y_polycracker[sequence_in_common], sample_weight = weights_new[sequence_in_common])#,labels = labels[labels != 'ambiguous'])
    cohen2 = cohen_kappa_score(y_progenitors,y_polycracker,sample_weight = weights_new,labels = labels, weights=None)
    print classification_report(y_progenitors, y_polycracker, sample_weight=weights_new)
    print(weights[sequence_in_common].sum(),weights_new[sequence_in_common])
    print 'cohen unambig',cohen,'cohen all', cohen2


@polycracker.command()
@click.pass_context
@click.option('-p','--scaffolds_pickle', default='scaffolds_stats.p', show_default=True, help='Pickle file generated from final_stats. Contains all scaffolds.',  type=click.Path(exists=False))
@click.option('-f', '--fasta_results', default='./cluster-0.fa,./cluster-1.fa',show_default=True, help= "Fasta files of clusters output from scimm/metabat. Write './*.fa' or 'folder/*.fasta' if specifying multiple files.",  type=click.Path(exists=False))
@click.option('-p1','--scimm_metabat_pickle', default='scaffolds_stats.scimm.metabat.labels.p', show_default=True, help='Pickle file generated from final_stats. These are polycracker results.',  type=click.Path(exists=False))
@click.option('-p2','--progenitors_pickle', default='scaffolds_stats.progenitors.labels.p', show_default=True, help='Pickle file generated from final_stats. These are progenitor mapping results.',  type=click.Path(exists=False))
@click.option('-w', '--work_dir', default='./', show_default=True, help='Work directory where computations for scimm/metabat comparison is done. Make sure only text files are subgenome outputs in folder.', type=click.Path(exists=False))
def compare_scimm_metabat(ctx,scaffolds_pickle,fasta_results,scimm_metabat_pickle, progenitors_pickle, work_dir):
    from sklearn.metrics import cohen_kappa_score, homogeneity_completeness_v_measure
    from sklearn.preprocessing import LabelEncoder
    import glob
    work_dir += '/'
    #print fasta_results
    def cohen_max(y_true,y_pred,weights):
        y_range = range(y_pred.max()+1)
        y_pred_permutations = permutations(y_range)
        cohens = []
        for perm in y_pred_permutations:
            d = dict(zip(y_range,perm))
            y_p = np.vectorize(lambda x: d[x])(y_pred)
            cohen = cohen_kappa_score(y_true,y_p, sample_weight = weights)
            print cohen
            cohens.append(cohen)
        return max(cohens)
    scaffold_len = lambda scaffold: int(scaffold.split('_')[-1])-int(scaffold.split('_')[-2])
    try:
        os.makedirs(work_dir)
    except:
        pass
    try:
        os.makedirs(work_dir+'results_compare/')
    except:
        pass
    if fasta_results.endswith('*.fa') or fasta_results.endswith('*.fasta'):
        fasta_results = glob.glob(fasta_results)
    else:
        fasta_results=fasta_results.split(',')
    for i,fasta in enumerate(fasta_results): #fixme throw in some metabat
        f1 = Fasta(fasta)
        with open(work_dir+'subgenome_%d.txt'%i,'w') as f:
            f.write('\n'.join(f1.keys()))
    ctx.invoke(convert_subgenome_output_to_pickle,input_dir=work_dir,scaffolds_pickle=scaffolds_pickle,output_pickle=scimm_metabat_pickle)
    weights = np.vectorize(scaffold_len)(pickle.load(open(scaffolds_pickle,'rb')))
    scimm_metabat_labels = pickle.load(open(scimm_metabat_pickle,'rb'))
    progenitor_labels = pickle.load(open(progenitors_pickle,'rb'))
    progenitor_labels = LabelEncoder().fit_transform(progenitor_labels)
    scimm_metabat_labels = LabelEncoder().fit_transform(scimm_metabat_labels)
    w = weights.tolist()
    weights_mode = max(w, key = w.count)
    output_dict = dict(cohen_kappa_score=cohen_max(progenitor_labels,scimm_metabat_labels,weights),homogeneity_completeness_v_measure=homogeneity_completeness_v_measure(progenitor_labels,scimm_metabat_labels),weights_len = weights[weights==weights_mode].sum()/float(sum(weights))) #fixme permute labels here!, add weights, etc))
    with open(work_dir+'results_compare/results.txt','w') as f:
        f.write(str(output_dict))


@polycracker.command(name='final_stats')
@click.option('-p/-s','--progenitors/--species',default=False, help='If running final_stats with progenitors without known subgenomes labelling, will compare progenitor results to polyCRACKER without ground truth. If separating species from sample or you already know subgenome labelling, --species will compare to ground truth.')
@click.option('-dict','--comparisons_dict', default='subgenome_1:progenitorA,subgenome_2:progenitorB,subgenome_3:speciesA' , show_default=True, help='MANDATORY: Comma delimited mapping of inferred subgenome names output from polycracker to Progenitor/Species labels.', type=click.Path(exists=False))
@click.option('-cbed','--correspondence_bed', default='correspondence.bed', show_default=True, help='Bed file containing the original scaffold names. Please check if this bed file contains all scaffolds, else generate file from splitFasta.',  type=click.Path(exists=False))
@click.option('-pbed','--polycracker_bed', default='subgenomes.bed', show_default=True, help='Bootstrap/cluster run results bed generated from outputgenerate_out_bed after running polycracker. These are polycracker results.',  type=click.Path(exists=False))
@click.option('-sbed','--progenitors_species_bed', default='progenitors.bed', show_default=True, help='Progenitors bed output from progenitorMapping or species bed output.',  type=click.Path(exists=False))
@click.option('-c','--cluster_analysis', is_flag=True, help='Whether to perform analyses on clustering results. Classification analysis will be disabled for this run if this option is selected, but you may need to add data from the above options.')
@click.option('-cs','--cluster_scaffold', default = 'scaffolds.p', help='Scaffolds pickle file used for cluster analysis.', show_default=True, type=click.Path(exists=False))
@click.option('-npy','--positions_npy',default='',help='Positions npy file if choosing to do clustering analysis. Will assess the validity of the clusters with a euclidean metric, so may not be as valid for non-convex sets. Leave blank if not running analysis.',type=click.Path(exists=False))
@click.option('-op','--original_progenitors',default='',help='Dictionary of original progenitor names to their fasta files. Eg. progenitorA:./progenitors/progenitorA.fasta,progenitorR:./progenitorsR.fasta')
@click.option('-n','--note',default='',help='Note to self that can be put into report.',type=click.Path(exists=False))
@click.pass_context
def final_stats(ctx,progenitors, comparisons_dict, correspondence_bed, polycracker_bed, progenitors_species_bed,cluster_analysis,cluster_scaffold,positions_npy,original_progenitors,note):
    """Analyzes the accuracy and agreement between polyCRACKER and ground truth species labels or progenitor mapped labels. Also compares polyCRACKER output to sizes of known progenitors. In future, may attempt to find similarity etween polyCRACKER sequences and progenitors through mash/bbsketch."""
    import seaborn as sns
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')
    from sklearn.metrics import cohen_kappa_score,fowlkes_mallows_score,calinski_harabaz_score
    scaffold_len = lambda scaffold: int(scaffold.split('_')[-1])-int(scaffold.split('_')[-2])
    total_len = lambda scaffolds_list: sum([scaffold_len(scaffold) for scaffold in scaffolds_list if scaffold])
    if cluster_analysis == 0:
        # grab total length of all sequences
        total_length = int(os.popen("awk '{s+=($3-$2)} END {printf \"%%.0f\", s}' %s"%correspondence_bed).read())
        all_sequences = np.array(os.popen("awk '{print $1 \"_\" $2 \"_\" $3}' %s"%correspondence_bed).read().splitlines())
        pickle.dump(all_sequences,open('scaffolds_stats.p','wb'))
        polycracker2ProgSpec = {subgenome:progenitor_species for subgenome,progenitor_species in [tuple(mapping.split(':')) for mapping in comparisons_dict.split(',')]}
        weights = np.vectorize(scaffold_len)(all_sequences)
        weights_new = weights / float(np.sum(weights))
        ctx.invoke(convert_subgenome_output_to_pickle,input_dir=polycracker_bed, scaffolds_pickle='scaffolds_stats.p', output_pickle='scaffolds_stats.poly.labels.p')
        y_polycracker = pickle.load(open('scaffolds_stats.poly.labels.p','rb'))
        polycracker_unambiguous_total_len = sum(weights[y_polycracker != 'ambiguous'])
        polycracker_unambiguous_total_len_percent = float(polycracker_unambiguous_total_len)/total_length
        print(np.unique(polycracker2ProgSpec.keys()))
        print(polycracker2ProgSpec)
        print(y_polycracker)
        y_polycracker = np.vectorize(lambda x: polycracker2ProgSpec[x] if x in np.unique(polycracker2ProgSpec.keys()) else 'ambiguous')(y_polycracker)
        measures = {'Length: Total Genome':total_length,'Length: Total Poly': polycracker_unambiguous_total_len,'Ratio: [Total Poly]/[Total Genome]': polycracker_unambiguous_total_len_percent}
        if progenitors:
            ctx.invoke(convert_subgenome_output_to_pickle,input_dir=progenitors_species_bed, scaffolds_pickle='scaffolds_stats.p', output_pickle='scaffolds_stats.progenitors.labels.p')
            y_progenitors = pickle.load(open('scaffolds_stats.progenitors.labels.p','rb'))
            progenitor_unambiguous_total_len = sum(weights[y_progenitors != 'ambiguous'])
            progenitor_unambiguous_total_len_percent = float(progenitor_unambiguous_total_len)/total_length
            union = np.unique(np.union1d(np.unique(y_progenitors),np.unique(y_polycracker)))
            if 'ambiguous' in union:
                c_matrix_labels = np.hstack((np.setdiff1d(union,['ambiguous']),['ambiguous']))
            else:
                c_matrix_labels = union
            c_matrix = confusion_matrix(y_progenitors,y_polycracker,sample_weight=weights,labels=c_matrix_labels)
            sequence_agreement = (np.trace(c_matrix[:-1,:-1]) if 'ambiguous' in c_matrix_labels else np.trace(c_matrix))
            sequence_disagreement_n_ambiguous = total_length - sequence_agreement
            percent_agreement = float(sequence_agreement)/total_length
            percent_disagreement = float(sequence_disagreement_n_ambiguous)/total_length
            # other metrics, when both have nonambiguous sequences
            a = y_progenitors != 'ambiguous'
            b = y_polycracker != 'ambiguous'
            sequence_in_common = (a & b)
            cohen = cohen_kappa_score(y_progenitors[sequence_in_common],y_polycracker[sequence_in_common], sample_weight = weights_new[sequence_in_common],labels = np.setdiff1d(c_matrix_labels,['ambiguous']))
            cohen2 = cohen_kappa_score(y_progenitors,y_polycracker,sample_weight = weights_new,labels = c_matrix_labels)
            measures.update({'Length: Total Prog Map': progenitor_unambiguous_total_len,'Ratio: [Total Prog Map]/[Total Genome]': progenitor_unambiguous_total_len_percent,
                      'Length: Total Poly-Prog_Map Agreement':sequence_agreement, 'Ratio: [Poly-Prog_Map Agreement]/[Total Genome]':percent_agreement,
                      "Metric: Cohen's Kappa Unambiguous": cohen, "Metric: Cohen's Kappa All": cohen2, 'Metric: Jaccard Similarity Unambiguous':jaccard_similarity_score(y_progenitors[sequence_in_common],y_polycracker[sequence_in_common],normalize=True)})
            # FIXME ADD MORE AND PLOT C_MATRIX, send report to csv 'Ambiguous and Disagreement Sequence': sequence_disagreement_n_ambiguous,'Percent Disagreement over Total':percent_disagreement,
            if original_progenitors:
                progenitors_dict = {progenitor:original_progenitor for progenitor,original_progenitor in [tuple(mapping.split(':')) for mapping in original_progenitors.split(',')]}
                original_progenitor_lengths = {}
                for progenitor,original_progenitor in progenitors_dict.items():
                    subprocess.call('samtools faidx %s'%original_progenitor,shell=True)
                    original_progenitor_lengths[progenitor]=int(os.popen("awk '{s+=($2)} END {printf \"%%.0f\", s}' %s"%original_progenitor+'.fai').read())
                    measures['Length: Actual Prog %s'%progenitor] = original_progenitor_lengths[progenitor]
                for i in range((len(c_matrix_labels)-1 if 'ambiguous' in c_matrix_labels else len(c_matrix_labels))):
                    progenitor = c_matrix_labels[i]
                    measures['Length: %s Poly-Prog_Map Agreement'%progenitor]=c_matrix[i,i]
                    prog_sum = np.sum(c_matrix[i,:])
                    poly_sum = np.sum(c_matrix[:,i])
                    measures.update({'Length: %s Prog Map'%progenitor:prog_sum,'Length: %s Poly'%progenitor:poly_sum,
                                     'Ratio: [%s Prog Map]/[%s Actual Prog]'%(progenitor,progenitor):float(prog_sum)/original_progenitor_lengths[progenitor],
                                     'Ratio: [%s Poly]/[%s Actual Prog]'%(progenitor,progenitor):float(poly_sum)/original_progenitor_lengths[progenitor],
                                     'Ratio: [%s Poly]/[%s Prog Map]'%(progenitor,progenitor):float(poly_sum)/float(prog_sum)})
                measures.update({'Ratio: [Total Poly]/[Total Actual Prog]':float(polycracker_unambiguous_total_len)/sum(original_progenitor_lengths.values()),
                                 'Ratio: [Total Prog Map]/[Total Actual Prog]':float(progenitor_unambiguous_total_len)/sum(original_progenitor_lengths.values()),
                                 'Ratio: [Total Poly]/[Total Prog Map]':float(polycracker_unambiguous_total_len)/float(progenitor_unambiguous_total_len)})
            plot_labels = ('Classification Comparison','Progenitors','PolyCRACKER',c_matrix_labels)
        else:
            ctx.invoke(species_comparison_scaffold2colors,scaffolds_pickle='scaffolds_stats.p',output_pickle='scaffolds_stats.species.labels.p')
            y_species = pickle.load(open('scaffolds_stats.species.labels.p','rb')) # no ambiguous sequences here
            c_matrix_labels = np.unique(y_species)
            c_matrix = confusion_matrix(y_species,y_polycracker,sample_weight=weights,labels=c_matrix_labels)
            sequence_correctly_classified = np.trace(c_matrix)
            percent_correct = float(sequence_correctly_classified)/total_length
            # incorrect sequence is also ambiguous
            sequence_incorrectly_classified = total_length - sequence_correctly_classified
            percent_incorrect = float(sequence_incorrectly_classified)/total_length
            species_lengths = {species:sum(weights[y_species==species]) for species in np.unique(y_species)}
            polycracker_lengths = {species:sum(weights[y_polycracker==species]) for species in np.unique(y_species)}
            for species in np.unique(y_species):
                measures['Length: %s Original'%species] = species_lengths[species]
                measures['Length: %s Poly'%species] = polycracker_lengths[species]
                measures['Ratio: [%s Poly]/[%s Original]'%(species,species)] = float(polycracker_lengths[species])/species_lengths[species]
            for i in range(len(c_matrix_labels)):
                species = c_matrix_labels[i]
                measures['Length: %s Poly Correct'%species]=c_matrix[i,i]
                measures['Ratio: [%s Poly Correct]/[%s Original]'%(species,species)] = float(c_matrix[i,i])/species_lengths[c_matrix_labels[i]]
            if c_matrix.shape == (2,2):
                tn, fp, fn, tp = c_matrix.ravel()
                measures.update({'Metric: TN':tn,'Metric: FP':fp,'Metric: FN':fn,'Metric: TP':tp})
            class_report = classification_report(y_species, y_polycracker, sample_weight=weights_new, output_dict=True)
            if 0:
                class_report_rows = []
                class_report_data = []
                for line in class_report.splitlines()[2:-1]:
                    if line:
                        ll = line.split()
                        class_report_rows.append(ll[0])
                        class_report_data.append(ll[1:-1])
                line = class_report.splitlines()[-1]
                ll = line.split()
                class_report_rows.append(''.join(ll[0:3]))
                class_report_data.append(ll[3:-1])
                class_report_data = np.array(class_report_data).astype(float)
            class_report_df = pd.DataFrame(class_report)#,index=class_report_rows,columns=['Precision','Recall','F1-score'])
            class_report_df.to_csv('polycracker.classification.report.csv')
            plt.figure()
            sns.heatmap(class_report_df,annot=True)
            plt.savefig('polycracker.classification.report.png',dpi=300)
            measures.update({'Length: Total Poly Correct':sequence_correctly_classified,'Ratio: [Total Poly Correct]/[Total Genomes]':percent_correct,
                             'Metric: Jaccard Similarity':jaccard_similarity_score(y_species,y_polycracker,normalize=True),
                             'Metric: Classification Report Summary Avgs':class_report})
                             #'Metric: Classification Report Summary Avgs':['Precision: %f'%class_report_data[-1,0],'Recall: %f'%class_report_data[-1,1],'F1-Score: %f'%class_report_data[-1,2]]})
            #'Sequence incorrectly classified':sequence_incorrectly_classified, 'Percent of all, incorrect':percent_incorrect,
            # other metrics                              'brier score loss':'xxx',#[brier_score_loss(y_species, y_polycracker, sample_weight=weights,pos_label=species) for species in np.unique(y_species)],
            """'hamming loss':hamming_loss(y_species,y_polycracker,labels=np.unique(y_species),sample_weight=weights),
                             'zero one loss':zero_one_loss(y_species, y_polycracker, sample_weight=weights),
                             'Accuracy':accuracy_score(y_species, y_polycracker, sample_weight=weights)
                             'f1':f1_score(y_species,y_polycracker,average='weighted',sample_weight=weights),
                             'Precision and Recall, Fscore Support':precision_recall_fscore_support(y_species,y_polycracker,average='weighted',sample_weight=weights),"""
            # FIXME ADD MORE METRICS AND PLOT C_MATRIX
            plot_labels = ('Classification Confusion Matrix','Species','PolyCRACKER',c_matrix_labels)
    else:
        if cluster_scaffold.endswith('.bed'):
            all_sequences = np.array(os.popen("awk '{print $1 \"_\" $2 \"_\" $3}' %s"%cluster_scaffold).read().splitlines())
            scaffolds = all_sequences
            cluster_scaffold = 'new_scaffolds.p'
            pickle.dump(all_sequences,open(cluster_scaffold,'wb'))
        else:
            all_sequences = pickle.load(open(cluster_scaffold,'rb'))
            scaffolds = np.array(pickle.load(open(cluster_scaffold,'rb')))
        weights = np.vectorize(scaffold_len)(all_sequences)
        ctx.invoke(convert_subgenome_output_to_pickle,input_dir=polycracker_bed, scaffolds_pickle=cluster_scaffold, output_pickle='scaffolds_stats.poly.labels.p')
        y_pred = pickle.load(open('scaffolds_stats.poly.labels.p','rb'))
        measures = {}
        total_length = int(os.popen("awk '{s+=($3-$2)} END {printf \"%%.0f\", s}' %s"%correspondence_bed).read())
        measures.update({'Length: Total Genome':total_length,'Length: Total Poly':total_len(scaffolds)})
        for cluster in np.unique(y_pred):
            measures['Length: %s Poly'%cluster] = total_len(scaffolds[y_pred==cluster])
        if progenitors_species_bed and os.path.exists(progenitors_species_bed) and os.stat(progenitors_species_bed).st_size > 0:
            # PROGENITORS VS SPECIES
            if progenitors:
                ctx.invoke(convert_subgenome_output_to_pickle,input_dir=progenitors_species_bed, scaffolds_pickle=cluster_scaffold, output_pickle='scaffolds_stats.progenitors.labels.p')
                y_true = pickle.load(open('scaffolds_stats.progenitors.labels.p','rb'))
                plot_labels = ('Clustering Comparison','Progenitors','PolyCRACKER')
                measures.update({'Metric: AMI':adjusted_mutual_info_score(y_true,y_pred)})
                for progenitor in np.unique(y_true):
                    measures['Length: %s Prog Map from Poly Selected'%progenitor] = total_len(scaffolds[y_true==progenitor])
            else:
                ctx.invoke(species_comparison_scaffold2colors,scaffolds_pickle=cluster_scaffold,output_pickle='scaffolds_stats.species.labels.p')
                y_true = pickle.load(open('scaffolds_stats.species.labels.p','rb'))
                plot_labels = ('Clustering Comparison','Species','PolyCRACKER')
                measures.update({'Metric: V_measure':homogeneity_completeness_v_measure(y_true,y_pred)})
                for species in np.unique(y_true):
                    measures['Length: %s Original from Poly Selected'%species] = total_len(scaffolds[y_true==species])
            # metrics
            measures.update({'Metric: Fowlkes Mallows Score':fowlkes_mallows_score(y_true,y_pred),'Metric: ARI':adjusted_rand_score(y_true,y_pred)})
            # 'homogeneity':homogeneity_score(y_true,y_pred),Completeness':completeness_score(y_true,y_pred) 'ARI':adjusted_rand_score(y_true,y_pred),
            c_matrix = pd.crosstab(y_true,y_pred,values=weights,aggfunc=sum)
        if positions_npy:
            X = np.load(positions_npy)
            measures.update({'Metric: Silhouette Score':silhouette_score(X,y_pred,metric='euclidean'),'Metric: Calinski Harabaz':calinski_harabaz_score(X,y_pred)})
    plt.figure(figsize=(7,7))
    if cluster_analysis == 0:
        classes = plot_labels[3]
        c_matrix = pd.DataFrame(c_matrix,classes,['PolyCRACKER:' + cls for cls in classes])
        #tick_marks = np.arange(len(classes))
        #plt.xticks(tick_marks, classes)
        #plt.yticks(tick_marks, classes)
        plt.title(plot_labels[0])
        plt.xlabel(plot_labels[2])
        plt.ylabel(plot_labels[1])
    try:
        sns.heatmap(c_matrix)
    except:
        pass
    plt.xticks(rotation=45)
    if note:
        measures['Note'] = note
    for measure in measures:
        if type(measures[measure]) != type([]) or type(measures[measure]) != type(tuple([])):
            measures[measure] = [measures[measure]]
    measures = OrderedDict(sorted(measures.items()))
    print(measures)
    pd.DataFrame(measures).T.to_csv('polycracker.stats.analysis.csv',index=True)
    try:
        c_matrix.to_csv('polycracker.stats.confusion.matrix.csv',index=True)
        plt.savefig('polycracker.stats.confusion.matrix.pdf',dpi=300)
    except:
        pass

##################################################################################

###################################### MASH ######################################


@polycracker.command()
@click.option('-i', '--input_files', default = "genomes/*.fa", show_default=True, help="Input fasta files. Put input in quotations if specifying multiple files. Eg. 'genomes/*.fasta'", type=click.Path(exists=False))
@click.option('-kl', '--kmer_length', default = 23, show_default=True, help='Default kmer length for signature.')
@click.option('-o', '--output_file_prefix', default = 'output', show_default=True, help='Output file prefix, default outputs output.cmp.dnd and output.sig.', type=click.Path(exists=False) )
@click.option('-mf', '--multi_fasta', is_flag=True, help='Instead of using multiple fasta files, generate signatures based on sequences in a multifasta file.')
@click.option('-s','--scaled', default = 10000, show_default=True, help='Scale factor for sourmash.')
def generate_genome_signatures(input_files, kmer_length, output_file_prefix,multi_fasta,scaled):
    """Wrapper for sourmash. Generate genome signatures and corresponding distance matrices for scaffolds/fasta files."""
    subprocess.call('sourmash compute -f --scaled %d %s -o %s.sig -k %d %s'%(scaled,input_files,output_file_prefix,kmer_length,'--singleton' if multi_fasta else ''),shell=True)
    subprocess.call('sourmash compare %s.sig --csv %s.cmp.csv'%(output_file_prefix,output_file_prefix),shell=True)


@polycracker.command()
@click.option('-csv','--dist_mat', default= 'output.cmp.csv', help='Input distance matrix from sourmash or can use feature matrix kmer_master_count_matrix.csv with option -f T.', type=click.Path(exists=False))
@click.option('-t','--transform_algorithm', default='mds', help='Dimensionality reduction technique to use.', type=click.Choice(['mds','tsne','spectral']))
@click.option('-o', '--output_file_prefix', default = 'output', show_default=True, help='Output file prefix, default outputs output.heatmap.png and output.[transform_algorithm].html.', type=click.Path(exists=False) )
@click.option('-j', '--n_jobs', default=1, help='Number of jobs for distance matrix transformation.', show_default=True)
@click.option('-f','--feature_space', default='n', help='Matrix is in feature space (n_samples x n_features or vice versa); y transforms via assuming matrix is n_samples x n_features and T assumes matrix is n_features x n_samples.', type=click.Choice(['n','y','T']))
@click.option('-k', '--kmeans_clusters', default = 0, help= 'If number of chosen clusters is greater than 0, runs kmeans clustering with chosen number of clusters, and choose most representative samples of clusters.', show_default=True)
def plot_distance_matrix(dist_mat,transform_algorithm,output_file_prefix,n_jobs,feature_space,kmeans_clusters):
    """Perform dimensionality reduction on sourmash distance matrix or feature space matrix and plot samples in lower dimensional space and cluster."""
    from MulticoreTSNE import MulticoreTSNE as TSNE
    from sklearn.manifold import MDS
    import seaborn as sns
    from sklearn.cluster import KMeans
    df = pd.read_csv(dist_mat,index_col=(None if feature_space == 'n' else 0))
    sample_names = np.array(list(df))
    if feature_space == 'T':
        df = df.transpose()
    if feature_space == 'y' or feature_space == 'T':
        sample_names = np.array(list(df.index))
        df = pairwise_distances(df,metric='manhattan') # euclidean fixme high dimensions
    else:
        df.iloc[:,:] = 1.-df.as_matrix()
    plt.figure()
    sns.heatmap(df,xticklabels=False, yticklabels=False)
    plt.savefig(output_file_prefix+'.heatmap.png',dpi=300)
    transform_dict = {'spectral':SpectralEmbedding(n_components=3,n_jobs=n_jobs,affinity='precomputed'),'tsne':TSNE(n_components=3,n_jobs=n_jobs,metric='precomputed'), 'mds':MDS(n_components=3,n_jobs=n_jobs,dissimilarity='precomputed')}
    if transform_algorithm == 'spectral':
        nn = NearestNeighbors(n_neighbors=5,metric='precomputed')
        nn.fit(df)
        df = nn.kneighbors_graph(df).todense()
    t_data = transform_dict[transform_algorithm].fit_transform(df)
    py.plot(go.Figure(data=[go.Scatter3d(x=t_data[:,0],y=t_data[:,1],z=t_data[:,2],mode='markers',marker=dict(size=3),text=sample_names)]),filename='%s.%s.html'%(output_file_prefix,transform_algorithm),auto_open=False)
    if kmeans_clusters > 0:
        km = KMeans(n_clusters=kmeans_clusters)
        km.fit(t_data)
        centers = km.cluster_centers_
        df = pd.DataFrame(t_data,index=sample_names,columns=['x','y','z'])
        df['labels'] = km.labels_
        df['distance_from_center'] = np.linalg.norm(df.loc[:,['x','y','z']].as_matrix() - np.array([centers[label] for label in df['labels'].as_matrix()]),axis=1)
        plots = []
        representative_points = []
        for label in df['labels'].unique():
            dff = df[df['labels'] == label]
            representative_points.append(dff['distance_from_center'].argmin())
            plots.append(go.Scatter3d(x=dff['x'],y=dff['y'],z=dff['z'],name='Cluster %d'%label,text=list(dff.index),mode='markers',marker=dict(size=3)))
        plots.append(go.Scatter3d(x=centers[:,0],y=centers[:,1],z=centers[:,2],name='Cluster Centers',text=['Cluster %d'%label for label in df['labels'].unique()],mode='markers',marker=dict(size=6,opacity=0.5,color='purple')))
        with open('representative_points.txt','w') as f:
            f.write(','.join(representative_points)+'\nCopy Commands:\nscp '+ ' '.join(representative_points+['folder_of_choice']))
        py.plot(plots,auto_open=False,filename='%s.%s.clusters.html'%(output_file_prefix,transform_algorithm))


@polycracker.command() # FIXME mash, sourmash, kWIP, bbsketch
def mash_test(split_fasta):
    """Sourmash integration in development."""
    print 'Under development'


##################################################################################

###################################### TEST ######################################

@polycracker.command()
def run_tests():
    """Run basic polyCRACKER tests to see if working properly."""
    subprocess.call('pytest -q test_polycracker.py',shell=True)

##################################################################################

###################################### MAIN ######################################

if __name__ == '__main__':
    polycracker()
