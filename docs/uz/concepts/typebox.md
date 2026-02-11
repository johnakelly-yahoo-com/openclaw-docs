---
summary: "9. Gateway protokoli uchun yagona haqiqat manbai sifatida TypeBox sxemalari"
read_when:
  - 10. Protokol sxemalarini yoki codegenni yangilash
title: "11. TypeBox"
---

# 12. Protokol uchun haqiqatning yagona manbai sifatida TypeBox

13. Oxirgi yangilanish: 2026-01-10

14. TypeBox — TypeScript-ga yo‘naltirilgan sxema kutubxonasi. 15. Biz undan **Gateway WebSocket protokoli**ni (handshake, so‘rov/javob, server hodisalari) aniqlash uchun foydalanamiz. 16. Ushbu sxemalar **ishga tushirish vaqtidagi tekshiruv**, **JSON Schema eksporti** va macOS ilovasi uchun **Swift codegen**ni ta’minlaydi. 17. Yagona haqiqat manbai; qolgan hammasi generatsiya qilinadi.

18. Yuqori darajadagi protokol konteksti uchun [Gateway architecture](/concepts/architecture) dan boshlang.

## 19. Aqliy model (30 soniya)

20. Har bir Gateway WS xabari uchta freymdan biriga tegishli:

- 21. **So‘rov (Request)**: `{ type: "req", id, method, params }`
- 22. **Javob (Response)**: `{ type: "res", id, ok, payload | error }`
- 23. **Hodisa (Event)**: \`{ type: "event", event, payload, seq?, stateVersion?
  24. }`25. Birinchi freym **majburiy ravishda**`connect\` so‘rovi bo‘lishi kerak.

26. Shundan so‘ng mijozlar metodlarni (masalan, `health`, `send`, `chat.send`) chaqirishi va hodisalarga (masalan, `presence`, `tick`, `agent`) obuna bo‘lishi mumkin. 27. Ulanish oqimi (minimal):

28. Client                    Gateway
    \|---- req:connect -------->|
    |<---- res:hello-ok --------|
    |<---- event:tick ----------|
    \|---- req:health ---------->|
    |<---- res:health ----------|

```
29. Umumiy metodlar + hodisalar:
```

30. Kategoriya

| Doimiy ofset uchun aniq IANA vaqt zonasidan foydalaning (masalan, `"Europe/Vienna"`). | 32. Eslatmalar                                                 | 33. Yadro (Core)                |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| 34. `connect`, `health`, `status`                                                                 | 35. `connect` birinchi bo‘lishi shart                          | 36. Xabar almashish (Messaging) |
| Kategoriya                                                                                                               | 38. yon ta’sirlar uchun `idempotencyKey` kerak                 | 39. Chat                                           |
| 40. `chat.history`, `chat.send`, `chat.abort`, `chat.inject`                                      | 41. WebChat bularni ishlatadi                                  | 42. Sessiyalar                                     |
| 43. `sessions.list`, `sessions.patch`, `sessions.delete`                                          | 44. sessiya administratsiyasi                                  | 45. Tugunlar (Nodes)            |
| 46. `node.list`, `node.invoke`, `node.pair.*`                                                     | 47. Gateway WS + tugun amallari                                | 48. Hodisalar                                      |
| 49. `tick`, `presence`, `agent`, `chat`, `health`, `shutdown`                                     | 50. server tomonidan yuborish (server push) | server push                                                               |

1. Avtoritativ roʻyxat `src/gateway/server.ts` (`METHODS`, `EVENTS`) faylida joylashgan.

## 2. Sxemalar qayerda joylashgan

- Xabar almashish
- 4. Ish vaqtidagi validatorlar (AJV): `src/gateway/protocol/index.ts`
- 5. Server qoʻl siqish (handshake) va metodlarni yoʻnaltirish: `src/gateway/server.ts`
- 6. Node mijozi: `src/gateway/client.ts`
- 7. Generatsiya qilingan JSON Schema: `dist/protocol.schema.json`
- 8. Generatsiya qilingan Swift modellari: `apps/macos/Sources/OpenClawProtocol/GatewayModels.swift`

## 9. Joriy pipeline

- 10. `pnpm protocol:gen`
  - 11. JSON Schema (draft‑07) ni `dist/protocol.schema.json` fayliga yozadi
- 12. `pnpm protocol:gen:swift`
  - 13. Swift gateway modellari generatsiya qilinadi
- Manba: `src/gateway/protocol/schema.ts`
  - 15. Ikkala generatorni ham ishga tushiradi va chiqish commit qilinganini tekshiradi

## 16. Sxemalar ish vaqtida qanday ishlatiladi

- 17. **Server tomoni**: har bir kiruvchi frame AJV yordamida tekshiriladi. 18. Qoʻl siqish faqat parametrlari `ConnectParams` ga mos keladigan `connect` soʻrovini qabul qiladi.
- 19. **Mijoz tomoni**: JS mijozi event va javob freymlarini ishlatishdan oldin tekshiradi.
- 20. **Metodlar yuzasi**: Gateway `hello-ok` ichida qoʻllab-quvvatlanadigan `methods` va `events` ni eʼlon qiladi.

## 21. Frame misollari

22. Connect (birinchi xabar):

```json
23. {
  "type": "req",
  "id": "c1",
  "method": "connect",
  "params": {
    "minProtocol": 2,
    "maxProtocol": 2,
    "client": {
      "id": "openclaw-macos",
      "displayName": "macos",
      "version": "1.0.0",
      "platform": "macos 15.1",
      "mode": "ui",
      "instanceId": "A1B2"
    }
  }
}
```

24. Hello-ok javobi:

```json
25. {
  "type": "res",
  "id": "c1",
  "ok": true,
  "payload": {
    "type": "hello-ok",
    "protocol": 2,
    "server": { "version": "dev", "connId": "ws-1" },
    "features": { "methods": ["health"], "events": ["tick"] },
    "snapshot": {
      "presence": [],
      "health": {},
      "stateVersion": { "presence": 0, "health": 0 },
      "uptimeMs": 0
    },
    "policy": { "maxPayload": 1048576, "maxBufferedBytes": 1048576, "tickIntervalMs": 30000 }
  }
}
```

26. Soʻrov + javob:

```json
27. { "type": "req", "id": "r1", "method": "health" }
```

```json
28. { "type": "res", "id": "r1", "ok": true, "payload": { "ok": true } }
```

29. Hodisa (event):

```json
30. { "type": "event", "event": "tick", "payload": { "ts": 1730000000 }, "seq": 12 }
```

## 31. Minimal mijoz (Node.js)

32. Eng kichik foydali oqim: connect + health.

```ts
33. import { WebSocket } from "ws";

const ws = new WebSocket("ws://127.0.0.1:18789");

ws.on("open", () => {
  ws.send(
    JSON.stringify({
      type: "req",
      id: "c1",
      method: "connect",
      params: {
        minProtocol: 3,
        maxProtocol: 3,
        client: {
          id: "cli",
          displayName: "example",
          version: "dev",
          platform: "node",
          mode: "cli",
        },
      },
    }),
  );
});

ws.on("message", (data) => {
  const msg = JSON.parse(String(data));
  if (msg.type === "res" && msg.id === "c1" && msg.ok) {
    ws.send(JSON.stringify({ type: "req", id: "h1", method: "health" }));
  }
  if (msg.type === "res" && msg.id === "h1") {
    console.log("health:", msg.payload);
    ws.close();
  }
});
```

## 34. Ishlagan misol: metodni boshidan oxirigacha qoʻshish

35. Misol: `{ ok: true, text }` qaytaradigan yangi `system.echo` soʻrovini qoʻshish.

1. 36. **Sxema (haqiqatning yagona manbai)**

37) `src/gateway/protocol/schema.ts` ga qoʻshing:

```ts
38. export const SystemEchoParamsSchema = Type.Object(
  { text: NonEmptyString },
  { additionalProperties: false },
);

export const SystemEchoResultSchema = Type.Object(
  { ok: Type.Boolean(), text: NonEmptyString },
  { additionalProperties: false },
);
```

39. Ikkalasini ham `ProtocolSchemas` ga qoʻshing va turlarni eksport qiling:

```ts
40.   SystemEchoParams: SystemEchoParamsSchema,
  SystemEchoResult: SystemEchoResultSchema,
```

```ts
41. export type SystemEchoParams = Static<typeof SystemEchoParamsSchema>;
export type SystemEchoResult = Static<typeof SystemEchoResultSchema>;
```

2. 42. **Validatsiya**

43) `src/gateway/protocol/index.ts` da AJV validatorini eksport qiling:

```ts
44. export const validateSystemEchoParams = ajv.compile<SystemEchoParams>(SystemEchoParamsSchema);
```

3. 45. **Server xatti-harakati**

46) `src/gateway/server-methods/system.ts` ga handler qoʻshing:

```ts
47. export const systemHandlers: GatewayRequestHandlers = {
  "system.echo": ({ params, respond }) => {
    const text = String(params.text ?? "");
    respond(true, { ok: true, text });
  },
};
```

48. Uni `src/gateway/server-methods.ts` da roʻyxatdan oʻtkazing (u allaqachon `systemHandlers` ni birlashtiradi), soʻng `src/gateway/server.ts` dagi `METHODS` ga `"system.echo"` ni qoʻshing.

4. 49. **Qayta generatsiya qilish**

```bash
50. pnpm protocol:check
```

5. **Testlar + hujjatlar**

`src/gateway/server.*.test.ts` ichida server testi qo‘shing va usulni hujjatlarda qayd eting.

## Swift codegen xatti-harakati

`pnpm protocol:check`

- `req`, `res`, `event` va `unknown` holatlariga ega `GatewayFrame` enum
- Kuchli tiplashtirilgan payload struct/enumlar
- `ErrorCode` qiymatlari va `GATEWAY_PROTOCOL_VERSION`

Oldinga moslik uchun noma’lum frame turlari xom payload sifatida saqlanadi.

## Versiyalash + moslik

- `PROTOCOL_VERSION` `src/gateway/protocol/schema.ts` da joylashgan.
- Mijozlar `minProtocol` + `maxProtocol` yuboradi; server nomosliklarni rad etadi.
- Swift modellari eski mijozlarni buzmaslik uchun noma’lum frame turlarini saqlab qoladi.

## Schema naqshlari va konvensiyalari

- Aksariyat obyektlar qat’iy payloadlar uchun `additionalProperties: false` dan foydalanadi.
- `NonEmptyString` IDlar va metod/event nomlari uchun sukut bo‘yicha ishlatiladi.
- Yuqori darajadagi `GatewayFrame` `type` bo‘yicha **discriminator** dan foydalanadi.
- Yon ta’sirli metodlar odatda parametrlarda `idempotencyKey` talab qiladi
  (misol: `send`, `poll`, `agent`, `chat.send`).

## Jonli schema JSON

Yaratilgan JSON Schema repoda `dist/protocol.schema.json` da joylashgan. E’lon qilingan xom fayl odatda bu manzilda mavjud:

- https://raw.githubusercontent.com/openclaw/openclaw/main/dist/protocol.schema.json

## Schema’larni o‘zgartirganda

1. TypeBox schema’larini yangilang.
2. `pnpm protocol:check` ni ishga tushiring.
3. Qayta yaratilgan schema va Swift modellari bilan commit qiling.
