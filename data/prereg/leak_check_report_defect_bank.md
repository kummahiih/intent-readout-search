# Leak check — defect/recall bank (PROVISIONAL, not confirmatory)

72 IDs x 3 note paraphrases x hide/name = 432 rows. Split by scenario_id (hash): fit 45 IDs / 270 rows, eval 27 IDs / 162 rows. Context pairs: identical 1-, 2-, 3-gram bags in all 216 pairs. All propositions true; fictional products.

Rule: note and note+question must be <=0.60 on fit. Result: all 0.500 (pass).

```
note                              unigram_NB         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
note                              tfidf12_LR         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
note                              tfidf13_LR         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
note                              tfidf13_LR_C100    fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
note+public_ask                   unigram_NB         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
note+public_ask                   tfidf12_LR         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
note+public_ask                   tfidf13_LR         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
note+public_ask                   tfidf13_LR_C100    fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
note+name_ask                     unigram_NB         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
note+name_ask                     tfidf12_LR         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
note+name_ask                     tfidf13_LR         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
note+name_ask                     tfidf13_LR_C100    fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
incentive_context                 unigram_NB         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
incentive_context                 tfidf12_LR         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
incentive_context                 tfidf13_LR         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
incentive_context                 tfidf13_LR_C100    fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
full_prompt(ctx+note+public_ask)  unigram_NB         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
full_prompt(ctx+note+public_ask)  tfidf12_LR         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
full_prompt(ctx+note+public_ask)  tfidf13_LR         fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
full_prompt(ctx+note+public_ask)  tfidf13_LR_C100    fit 0.500 [0.44,0.56]  eval 0.500 [0.42,0.58]
```
