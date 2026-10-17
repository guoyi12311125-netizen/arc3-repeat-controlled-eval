# Model provenance

Every experiment in this release served the same checkpoint, from the same Kaggle
mount, through the same serving build. Values below are read from the run artifacts
(`serve.log` server arguments, `shared-serving-config.json`, and the kernel notebooks),
not from memory.

| item | value |
| --- | --- |
| model path (Kaggle input) | `/kaggle/input/models/dfranzen/intel-qwen3.8-flash-next-w4a16-autoround/transformers/default/1` |
| dataset version | `default/1` in the path above |
| quantization | AutoRound W4A16 (name and `quantization: auto-round` in server args) |
| speculative decoding | MTP draft model, EAGLE algorithm, 3 steps, 4 draft tokens |
| serving build | SGLang `Pennyroyal v2.5.3`, wheels from the Kaggle dataset `pennyroyal-v253` |
| runtime image | Kaggle `python-3.12` image, offline |
| context length | 147,456 configured at the server; harness window 131,072 |
| output cap | 12,288 tokens per request |
| KV cache | FP8 E4M3 |
| concurrent streams | 10 |
| weights redistributed here | no |

**Licensing.** The checkpoint is published on Kaggle Models; its license terms are
those published there by its authors. The mount we served from carried no license tag we
could read, so we do not restate a license name here. This release does not redistribute weights,
tokenizer files, or serving wheels; it references the Kaggle input paths above.

**Checksums.** We did not hash the mounted model directory; it is immutable per Kaggle
dataset version and the path above pins the version. Nothing in our analysis depends on
weight bytes, only on the requests the served model produced, which are in the logs.
