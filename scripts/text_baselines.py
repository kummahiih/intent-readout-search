#!/usr/bin/env python3
"""Visible-text baselines for a button dump (PROVISIONAL).
Inputs: --dump (run_scenario.py output). Targets: realized public button, assigned incentive.
Text inputs: note-only, note+public_ask. Model family (unigram NB, tfidf 1-2, tfidf 1-3 LR) is
selected on the FIT split only by scenario-grouped CV; the chosen model is refit on fit and scored on eval.
Does not fit residual readouts. Not a camera. Does not fill D."""
import argparse,json,sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupKFold,cross_val_predict
M={"unigram_NB":lambda:make_pipeline(CountVectorizer(),MultinomialNB()),
   "tfidf12_LR":lambda:make_pipeline(TfidfVectorizer(ngram_range=(1,2)),LogisticRegression(max_iter=2000)),
   "tfidf13_LR":lambda:make_pipeline(TfidfVectorizer(ngram_range=(1,3)),LogisticRegression(max_iter=2000))}
def main():
    a=argparse.ArgumentParser();a.add_argument("--dump",required=True);a.add_argument("--bank",required=True);a.add_argument("--out",required=True);x=a.parse_args()
    bank={(r["scenario_id"],r["incentive"],r["note"]):r for r in map(json.loads,open(x.bank))}
    rows=[r for r in map(json.loads,open(x.dump)) if r["arm"]=="public" and r["button"] in("YES","NO")]
    for r in rows: r["public_ask"]=bank[(r["scenario_id"],r["incentive"],r["note"])]["public_ask"]
    INP={"note":lambda r:r["note"],"note+public_ask":lambda r:r["note"]+" "+r["public_ask"]}
    TGT={"public_button":lambda r:r["button"]=="YES","incentive":lambda r:r["incentive"]=="hide"}
    fit=[r for r in rows if r["split"]=="fit"];ev=[r for r in rows if r["split"]=="eval"]
    res={"n_fit_valid_public":len(fit),"n_eval_valid_public":len(ev),"results":[]}
    for tn,t in TGT.items():
      yf=np.array([t(r) for r in fit]);ye=np.array([t(r) for r in ev])
      maj=max(ye.mean(),1-ye.mean()) if len(ye) else float("nan")
      for iname,f in INP.items():
        if len(set(yf))<2 or len(ev)==0:
            res["results"].append(dict(target=tn,input=iname,status="degenerate (one class on fit or empty eval)"));continue
        g=[r["scenario_id"] for r in fit];k=min(5,len(set(g)));cv={}
        try:
            for n,m in M.items(): cv[n]=float((cross_val_predict(m(),[f(r) for r in fit],yf,groups=g,cv=GroupKFold(k))==yf).mean())
        except ValueError as e:  # a grouped CV train fold has one class (Phi-4 agent_stakes: 1 NO on fit, 2026-11-02)
            res["results"].append(dict(target=tn,input=iname,status=f"degenerate (CV fold has one class; fit counts True={int(yf.sum())} False={int((~yf).sum())})",
                                       error=str(e)[:200],eval_majority=float(maj)));continue
        best=max(cv,key=cv.get);acc=float((M[best]().fit([f(r) for r in fit],yf).predict([f(r) for r in ev])==ye).mean())
        res["results"].append(dict(target=tn,input=iname,fit_cv=cv,selected=best,eval_acc=acc,eval_majority=float(maj)))
    json.dump(res,open(x.out,"w"),indent=1);print(json.dumps(res,indent=1))
if __name__=="__main__":sys.exit(main())
