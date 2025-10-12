# AWS Bedrock Model IDs Reference

## Current Configuration (2025)

**Active Model:** Claude 3.5 Sonnet v2
**Model ID:** `us.anthropic.claude-3-5-sonnet-20241022-v2:0`
**Region:** us-west-2
**Throughput:** On-demand (via US inference profile)

---

## Claude 3.5 Sonnet (October 2024 - v2)

### ✅ CURRENT - With On-Demand Support

**US Inference Profile (Recommended):**
```
us.anthropic.claude-3-5-sonnet-20241022-v2:0
```
- Routes across us-west-2, us-east-1, us-east-2
- **Supports on-demand throughput**
- 200K context window

**EU Inference Profile:**
```
eu.anthropic.claude-3-5-sonnet-20241022-v2:0
```

**Direct Model ID (Regional - NO on-demand):**
```
anthropic.claude-3-5-sonnet-20241022-v2:0
```
⚠️ Does NOT support on-demand throughput - use inference profile instead

---

## Claude 3.5 Sonnet (June 2024 - v1)

**Model ID:**
```
anthropic.claude-3-5-sonnet-20240620-v1:0
```
- Supports on-demand throughput directly (no inference profile needed)
- 200K context window
- Older version, consider upgrading to v2

---

## Claude Sonnet 4 (May 2025)

**Model ID:**
```
anthropic.claude-sonnet-4-20250514-v1:0
```

**Inference Profile IDs:**
```
us.anthropic.claude-sonnet-4-20250514-v1:0     # US regions
eu.anthropic.claude-sonnet-4-20250514-v1:0     # EU regions
apac.anthropic.claude-sonnet-4-20250514-v1:0   # APAC regions
```

⚠️ **Important:** Claude 4 models do NOT support on-demand throughput
- Must use inference profiles
- Requires provisioned throughput or cross-region inference

**Why We're Not Using Claude 4:**
- On-demand throughput not supported
- Would require provisioned capacity (higher cost)
- Claude 3.5 Sonnet v2 with inference profile works well for our use case

---

## Claude Sonnet 4.5 (September 2025)

**Model ID:**
```
anthropic.claude-sonnet-4-5-20250929-v1:0
```
- Newest model from Anthropic
- Best for coding and complex agents
- Also requires inference profiles (no direct on-demand)

---

## Error: "Invocation of model ID with on-demand throughput isn't supported"

**Cause:** Using direct model ID instead of inference profile for models that require it

**Solution:** Use inference profile ID format:
- ✅ `us.anthropic.claude-3-5-sonnet-20241022-v2:0`
- ❌ `anthropic.claude-3-5-sonnet-20241022-v2:0`

---

## Configuration Files

### base_agent.py
```python
MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
REGION = "us-west-2"
```

### .env
```bash
BEDROCK_MODEL_ID=us.anthropic.claude-3-5-sonnet-20241022-v2:0
AWS_DEFAULT_REGION=us-west-2
```

**Both files MUST match to avoid runtime errors!**

---

## References

- [AWS Bedrock Supported Models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- [Anthropic Models Overview](https://docs.anthropic.com/en/docs/about-claude/models)
- [Amazon Bedrock API - Claude Docs](https://docs.claude.com/en/api/claude-on-amazon-bedrock)

---

**Last Updated:** 2025-01-11
**Current Model:** Claude 3.5 Sonnet v2 with US inference profile
