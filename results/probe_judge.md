# Probe judge

Not a camera. Not `handoverPass`. Do not fill *D*.

A clear is above the note-text baseline with no interval overlap. Overlap is not a pass. A missing cache is not 0.

| Model | Probe | Score | Baseline | Clear |
| --- | --- | --- | --- | --- |
| qwen | prebutton | 50/55 = 0.909 [0.804, 0.961] | 0.709 | yes |
| qwen | noteonly | 33/55 = 0.600 [0.468, 0.719] | 0.709 | no |
| qwen | endnote | 30/55 = 0.545 [0.415, 0.670] | 0.709 | no |
| qwen | swap | 42/55 = 0.764 [0.637, 0.856] | 0.709 | no |
| qwen | askonly | 23/55 = 0.418 [0.297, 0.550] | 0.709 | no |
| qwen | note_mid | 37/55 = 0.673 [0.541, 0.782] | 0.709 | no |
| qwen | combine | 52/55 = 0.945 [0.851, 0.981] | 0.709 | yes |
| mistral | prebutton | 48/55 = 0.873 [0.760, 0.937] | 0.855 | no |
| mistral | noteonly | 43/55 = 0.782 [0.656, 0.871] | 0.855 | no |
| mistral | endnote | 43/55 = 0.782 [0.656, 0.871] | 0.855 | no |
| mistral | swap | 37/55 = 0.673 [0.541, 0.782] | 0.855 | no |
| mistral | askonly | 38/55 = 0.691 [0.560, 0.797] | 0.855 | no |
| mistral | note_mid | 38/55 = 0.691 [0.560, 0.797] | 0.855 | no |
| mistral | combine | 53/55 = 0.964 [0.877, 0.990] | 0.855 | yes |
| aya | prebutton | 55/55 = 1.000 [0.935, 1.000] | 0.836 | yes |
| aya | noteonly | 45/55 = 0.818 [0.697, 0.898] | 0.836 | no |
| aya | endnote | 48/55 = 0.873 [0.760, 0.937] | 0.836 | no |
| aya | swap | 44/55 = 0.800 [0.676, 0.884] | 0.836 | no |
| aya | askonly | 23/55 = 0.418 [0.297, 0.550] | 0.836 | no |
| aya | note_mid | 35/55 = 0.636 [0.504, 0.751] | 0.836 | no |
| aya | combine | 54/55 = 0.982 [0.904, 0.997] | 0.836 | yes |
| gemma | prebutton | 48/53 = 0.906 [0.797, 0.959] | 0.792 | yes |
| gemma | noteonly | 37/53 = 0.698 [0.565, 0.805] | 0.792 | no |
| gemma | endnote | 40/53 = 0.755 [0.624, 0.851] | 0.792 | no |
| gemma | swap | 35/53 = 0.660 [0.526, 0.773] | 0.792 | no |
| gemma | askonly | 35/53 = 0.660 [0.526, 0.773] | 0.792 | no |
| gemma | note_mid | 26/53 = 0.491 [0.361, 0.621] | 0.792 | no |
| gemma | combine | 52/53 = 0.981 [0.901, 0.997] | 0.792 | yes |
| falcon | prebutton | 53/55 = 0.964 [0.877, 0.990] | 0.818 | yes |
| falcon | noteonly | 42/55 = 0.764 [0.637, 0.856] | 0.818 | no |
| falcon | endnote | 43/55 = 0.782 [0.656, 0.871] | 0.818 | no |
| falcon | swap | 48/55 = 0.873 [0.760, 0.937] | 0.818 | no |
| falcon | askonly | 13/55 = 0.236 [0.144, 0.363] | 0.818 | no |
| falcon | note_mid | 34/55 = 0.618 [0.486, 0.735] | 0.818 | no |
| falcon | combine | 49/55 = 0.891 [0.782, 0.949] | 0.818 | no |

The pre-button and combine rows see the ask. Note-only, end-of-note, swap, and ask-only do not clear the bar. Not a plan readout.
