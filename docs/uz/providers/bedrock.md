---
summary: "OpenClaw bilan Amazon Bedrock (Converse API) modellaridan foydalaning"
read_when:
  - Siz OpenClaw bilan Amazon Bedrock modellaridan foydalanmoqchisiz
  - Model chaqiruvlari uchun AWS credential/region sozlamalari talab etiladi
title: "Amazon Bedrock"
---

# Amazon Bedrock

OpenClaw **Amazon Bedrock** modellaridan pi‑ai’ning **Bedrock Converse** oqimli provayderi orqali foydalanishi mumkin. Bedrock autentifikatsiyasi API kaliti emas, balki **AWS SDK standart credential chain** dan foydalanadi.

## pi‑ai nimalarni qo‘llab-quvvatlaydi

- Provayder: `amazon-bedrock`
- API: `bedrock-converse-stream`
- Auth: AWS credentiallari (env o‘zgaruvchilari, shared config yoki instance roli)
- Mintaqa: `AWS_REGION` yoki `AWS_DEFAULT_REGION` (standart: `us-east-1`)

## Avtomatik model aniqlash

Agar AWS credentiallari aniqlansa, OpenClaw **streaming** va **text output** ni qo‘llab‑quvvatlaydigan Bedrock modellarini avtomatik aniqlashi mumkin. Aniqlash `bedrock:ListFoundationModels` dan foydalanadi va keshda saqlanadi (standart: 1 soat).

Konfiguratsiya opsiyalari `models.bedrockDiscovery` ostida joylashgan:

```json5
{
  models: {
    bedrockDiscovery: {
      enabled: true,
      region: "us-east-1",
      providerFilter: ["anthropic", "amazon"],
      refreshInterval: 3600,
      defaultContextWindow: 32000,
      defaultMaxTokens: 4096,
    },
  },
}
```

Eslatmalar:

- `enabled` AWS credentiallari mavjud bo‘lsa, standart holatda `true` bo‘ladi.
- `region` avval `AWS_REGION` yoki `AWS_DEFAULT_REGION`, so‘ng `us-east-1` ga o‘rnatiladi.
- `providerFilter` Bedrock provayder nomlariga mos keladi (masalan `anthropic`).
- `refreshInterval` soniyalarda; keshlashni o‘chirish uchun `0` ga o‘rnating.
- `defaultContextWindow` (standart: `32000`) va `defaultMaxTokens` (standart: `4096`) aniqlangan modellar uchun ishlatiladi (agar model limitlarini bilsangiz, o‘zgartiring).

## Sozlash (qo‘lda)

1. **Gateway host** da AWS credentiallari mavjudligini ta’minlang:

```bash
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="us-east-1"
# Optional:
export AWS_SESSION_TOKEN="..."
export AWS_PROFILE="your-profile"
# Optional (Bedrock API key/bearer token):
export AWS_BEARER_TOKEN_BEDROCK="..."
```

2. Konfiguratsiyangizga Bedrock provayderi va modelini qo‘shing (`apiKey` talab qilinmaydi):

```json5
{
  models: {
    providers: {
      "amazon-bedrock": {
        baseUrl: "https://bedrock-runtime.us-east-1.amazonaws.com",
        api: "bedrock-converse-stream",
        auth: "aws-sdk",
        models: [
          {
            id: "us.anthropic.claude-opus-4-6-v1:0",
            name: "Claude Opus 4.6 (Bedrock)",
            reasoning: true,
            input: ["text", "image"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "amazon-bedrock/us.anthropic.claude-opus-4-6-v1:0" },
    },
  },
}
```

## EC2 Instance Rollari

Agar OpenClaw IAM roli biriktirilgan EC2 instansiyasida ishga tushirilsa, AWS SDK autentifikatsiya uchun avtomatik ravishda instance metadata service (IMDS) dan foydalanadi.
Biroq, OpenClaw’ning credential aniqlashi hozirda faqat environment o‘zgaruvchilarini tekshiradi, IMDS credentiallarini emas.

**Yechim:** AWS credentiallari mavjudligini bildirish uchun `AWS_PROFILE=default` ni o‘rnating. Haqiqiy autentifikatsiya baribir IMDS orqali instance roli yordamida amalga oshiriladi.

```bash
# ~/.bashrc yoki shell profilingizga qo‘shing
export AWS_PROFILE=default
export AWS_REGION=us-east-1
```

EC2 instance roli uchun **talab qilinadigan IAM ruxsatlari**:

- `bedrock:InvokeModel`
- `bedrock:InvokeModelWithResponseStream`
- `bedrock:ListFoundationModels` (avtomatik aniqlash uchun)

Yoki boshqariladigan `AmazonBedrockFullAccess` siyosatini biriktiring.

**Tezkor sozlash:**

```bash
# 1. IAM roli va instance profilini yarating
aws iam create-role --role-name EC2-Bedrock-Access \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy --role-name EC2-Bedrock-Access \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

aws iam create-instance-profile --instance-profile-name EC2-Bedrock-Access
aws iam add-role-to-instance-profile \
  --instance-profile-name EC2-Bedrock-Access \
  --role-name EC2-Bedrock-Access

# 2. EC2 instansiyangizga biriktiring
aws ec2 associate-iam-instance-profile \
  --instance-id i-xxxxx \
  --iam-instance-profile Name=EC2-Bedrock-Access

# 3. EC2 instansiyada aniqlashni yoqing
openclaw config set models.bedrockDiscovery.enabled true
openclaw config set models.bedrockDiscovery.region us-east-1

# 4. Yechim uchun env o‘zgaruvchilarini o‘rnating
echo 'export AWS_PROFILE=default' >> ~/.bashrc
echo 'export AWS_REGION=us-east-1' >> ~/.bashrc
source ~/.bashrc

# 5. Modellar aniqlanganini tekshiring
openclaw models list
```

## Eslatmalar

- Bedrock AWS akkauntingiz/mintaqangizda **model access** yoqilgan bo‘lishini talab qiladi.
- Avtomatik aniqlash uchun `bedrock:ListFoundationModels` ruxsati kerak.
- Agar profillardan foydalansangiz, gateway host da `AWS_PROFILE` ni o‘rnating.
- OpenClaw credential manbasini quyidagi tartibda aniqlaydi: `AWS_BEARER_TOKEN_BEDROCK`, so‘ng `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`, so‘ng `AWS_PROFILE`, so‘ng standart AWS SDK chain.
- Reasoning qo‘llab‑quvvatlashi modelga bog‘liq; joriy imkoniyatlar uchun Bedrock model kartasini tekshiring.
- Agar boshqariladigan kalit oqimini afzal ko‘rsangiz, Bedrock oldiga OpenAI‑mos proksini qo‘yib, uni OpenAI provayderi sifatida sozlashingiz ham mumkin.
