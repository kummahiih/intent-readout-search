#!/usr/bin/env python3
"""Visible-text baselines for a button dump (PROVISIONAL).
Inputs: --dump (run_scenario.py output). Targets: realized public button, assigned incentive.
Text inputs: note-only, note+public_ask, incentive_context, note+incentive_context, and the full visible
prompt (system + user text as run_scenario.py renders it, frame inferred from the bank row or set by
--role-frame / --incentive-in-user; added 2026-11-03, see results/audit_2026-11-03.md). Model family (unigram NB, tfidf 1-2, tfidf 1-3 LR, and the order-sensitive word 1-5 gram / char_wb 3-6 gram LR
added in the second review) is
selected on the FIT split only by scenario-grouped CV; the chosen model is refit on fit and scored on eval.
Does not fit residual readouts. Not a camera. Does not fill D."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from prompt_text import visible_text
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupKFold,cross_val_predict
M={"unigram_NB":lambda:make_pipeline(CountVectorizer(),MultinomialNB()),
   "tfidf12_LR":lambda:make_pipeline(TfidfVectorizer(ngram_range=(1,2)),LogisticRegression(max_iter=2000)),
   "tfidf13_LR":lambda:make_pipeline(TfidfVectorizer(ngram_range=(1,3)),LogisticRegression(max_iter=2000)),
   # order-sensitive (second review 2026-11-03): word 1-5 grams and char_wb 3-6 grams
   "tfidf15_LR":lambda:make_pipeline(TfidfVectorizer(ngram_range=(1,5),sublinear_tf=True),LogisticRegression(max_iter=4000,C=10.0)),
   "charwb36_LR":lambda:make_pipeline(TfidfVectorizer(analyzer="char_wb",ngram_range=(3,6),sublinear_tf=True),LogisticRegression(max_iter=4000,C=10.0))}
ORDER_SENSITIVE=("tfidf15_LR","charwb36_LR")
def main():
    a=argparse.ArgumentParser();a.add_argument("--dump",required=True);a.add_argument("--bank",required=True);a.add_argument("--out",required=True);a.add_argument("--role-frame",default=None,choices=["","user-says","agent-stakes"]);a.add_argument("--incentive-in-user",action="store_true");x=a.parse_args()
    bank={(r["scenario_id"],r["incentive"],r["note"]):r for r in map(json.loads,open(x.bank))}
    raw=[json.loads(l) for l in open(x.dump) if l.strip()]
    if not raw or "arm" not in raw[0]:
        print(f"SKIP {x.dump}: not a button dump (no arm field)")
        json.dump({"status":"skipped","reason":"not a button dump"},open(x.out,"w"),indent=1)
        return 0
    rows=[r for r in raw if r.get("arm")=="public" and r.get("button") in("YES","NO")]
    for r in rows:
        b=bank[(r["scenario_id"],r["incentive"],r["note"])];r["public_ask"]=b["public_ask"];r["incentive_context"]=b.get("incentive_context") or ""
        rf=x.role_frame if x.role_frame is not None else (b.get("framing") or "")
        iiu=x.incentive_in_user or b.get("incentive_position")=="user"
        r["full_prompt"]=visible_text(b,b["public_ask"],iiu,rf)
    INP={"note":lambda r:r["note"],"note+public_ask":lambda r:r["note"]+" "+r["public_ask"],
         "incentive_context":lambda r:r["incentive_context"] or "_empty_",
         "note+incentive_context":lambda r:r["note"]+" "+r["incentive_context"],
         "full_prompt":lambda r:r["full_prompt"]}
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
        except ValueError as e:
            res["results"].append(dict(target=tn,input=iname,status=f"degenerate (CV fold has one class; fit counts True={int(yf.sum())} False={int((~yf).sum())})",
                                       error=str(e)[:200],eval_majority=float(maj)));continue
        best=max(cv,key=cv.get);acc=float((M[best]().fit([f(r) for r in fit],yf).predict([f(r) for r in ev])==ye).mean())
        osb=max(ORDER_SENSITIVE,key=cv.get);acc_os=acc if best==osb else float((M[osb]().fit([f(r) for r in fit],yf).predict([f(r) for r in ev])==ye).mean())
        res["results"].append(dict(target=tn,input=iname,fit_cv=cv,selected=best,eval_acc=acc,eval_majority=float(maj),
                                   order_sensitive_selected=osb,order_sensitive_eval_acc=acc_os))
    json.dump(res,open(x.out,"w"),indent=1);print(json.dumps(res,indent=1))
if __name__=="__main__":sys.exit(main())
