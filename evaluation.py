import csv
from typing import Dict

from matching_and_ranking import Matching_and_ranking

def __get_queries_corpus(dataset_name: str) -> Dict[str, str]:
    queries_corpus = {}
    if dataset_name == "wiki":
        with open("C:/Users/lenovo/Desktop/wikIR1k/wikIR1k/validation/queries.csv", mode='r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                query_id = row['id_left']
                query_text = row['text_left']
                queries_corpus[query_id] = query_text
    return queries_corpus

def _get_qrels(file_path: str):
    qrels = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()  # أو استخدم split(',') للفصل بالفواصل
            qrels.append(parts)
    return qrels

def compute_metrics(ranked_docs, qrels, k=None):
    metrics = {}
    ap_sum = 0
    mrr_sum = 0
    p10_sum = 0
    overall_precision = 0
    overall_recall = 0
    overall_f1_score = 0
    for query_id in ranked_docs.keys():
        ranked_list = ranked_docs[query_id]
        relevant_docs = [doc_id for doc_id, score in qrels[query_id].items() if score > 0]
        if k is not None:
            ranked_list = {key: value for key, value in list(ranked_list.items())[:k]}
        tp = len(set(ranked_list).intersection(set(relevant_docs)))
        precision = tp / len(ranked_list) if len(ranked_list) > 0 else 0
        recall = tp / len(relevant_docs) if len(relevant_docs) > 0 else 0
        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        overall_precision += precision
        overall_recall += recall
        overall_f1_score += f1_score
        ap = 0
        relevant_docs_seen = set()
        for i, doc_id in enumerate(ranked_list):
            if doc_id in relevant_docs and doc_id not in relevant_docs_seen:
                ap += (len(relevant_docs_seen) + 1) / (i + 1)
                relevant_docs_seen.add(doc_id)
                if len(relevant_docs_seen) == 1:
                    mrr_sum += 1 / (i + 1)
                if len(relevant_docs_seen) == len(relevant_docs):
                    break
        ap /= len(relevant_docs) if len(relevant_docs) > 0 else 1
        ap_sum += ap
        p10 = len(set(list(tuple(ranked_list))[:10]).intersection(set(relevant_docs)))
        p10_sum += p10 / 10
        metrics[query_id] = {
            'recall': recall,
            'ap': ap,
            'p10': p10
        }
    overall_precision = overall_precision / len(ranked_docs)
    overall_recall = overall_recall / len(ranked_docs)
    overall_f1_score = overall_f1_score / len(ranked_docs)
    overall_ap = ap_sum / len(ranked_docs)
    overall_mrr = mrr_sum / len(ranked_docs)
    overall_p10 = p10_sum / len(ranked_docs)
    metrics['overall'] = {
        'recall': overall_recall,
        'map': overall_ap,
        'mrr': overall_mrr,
        'p10': overall_p10
    }
    # return metrics
    return metrics["overall"]



def evaluate(file_path: str, dataset_name: str, k=None):
    qrelsMap = dict()
    qrels = _get_qrels(file_path)
    
    for qrel_parts in qrels:
        query_id, _, doc_id, relevance = qrel_parts
        if query_id in qrelsMap:
            qrelsMap[query_id].update({doc_id: int(relevance)})
        else:
            qrelsMap[query_id] = {doc_id: int(relevance)}

    ranked_docs = {}
    queries = {}
    if dataset_name == "wiki":
        with open("C:/Users/lenovo/Desktop/wikIR1k/wikIR1k/validation/queries.csv", mode='r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                query_id = row['id_left']
                query_text = row['text_left']
                queries[query_id] = query_text
    i = 0
    for query_id in queries.keys():
        file_path='C:/Users/lenovo/Desktop/wiki.csv'
        with open(file_path,'r')as file:
            results = Matching_and_ranking(queries[query_id], file)
            ranked_docs[query_id] = results
#             print(f"currently ranking {query_id}")
            i = i + 1
            if i == 3000:
                break
    evaluation = compute_metrics(qrelsMap,ranked_docs, k)
    print(evaluation)