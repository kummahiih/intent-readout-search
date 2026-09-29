mkdir -p datasets

hf download skyai798/DeceptionBench \
  --repo-type dataset \
  --local-dir datasets/DeceptionBench

hf download ai-safety-institute/lie-detection-rollouts \
  --repo-type dataset \
  --local-dir datasets/lie-detection-rollouts

hf download difraud/difraud \
  --repo-type dataset \
  --local-dir datasets/difraud


hf download xycoord/deception-probes-activations \
  --repo-type dataset \
  --local-dir datasets/deception-probes-activations