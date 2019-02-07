import csv
import os


def generate_report(genes_count, report_path='output/report.tsv'):
    print('Generating report: {}'.format(report_path))

    header = ["gene", "count"]
    with open(report_path, 'w') as csvfile:
        report_csv = csv.writer(csvfile, delimiter='\t')
        report_csv.writerow(header)
        for gene in sorted(genes_count.keys()):
            report_csv.writerow([gene, genes_count[gene]])

def generate_mutliple_reports(genes_counts, output_path="output"):
    for sample in genes_counts.keys():
        generate_report(genes_counts[sample], report_path=os.path.join(output_path, sample+"_report.tsv"))