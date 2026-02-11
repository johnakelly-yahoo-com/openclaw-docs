---
summary: "25. OpenClaw (macOS ilovasi) uchun birinchi ishga tushirishdagi onboarding oqimi"
read_when:
  - 26. macOS onboarding yordamchisini loyihalash
  - 27. Auth yoki identifikatsiya sozlamalarini amalga oshirish
title: "28. Onboarding (macOS ilovasi)"
sidebarTitle: "29. Onboarding: macOS ilovasi"
---

# 30. Onboarding (macOS ilovasi)

31. Ushbu hujjat **joriy** birinchi ishga tushirishdagi onboarding oqimini tasvirlaydi. 32. Maqsad — silliq “day 0” tajribasi: Gateway qayerda ishlashini tanlash, auth ulash, ustani ishga tushirish va agentning o‘zini o‘zi boshlashiga imkon berish.

<Steps>
<Step title="Approve macOS warning">33. 
<Frame><img src="/assets/macos-onboarding/01-macos-warning.jpeg" alt="" />34. 
</Frame></Step>
<Step title="Approve find local networks">35. 
<Frame><img src="/assets/macos-onboarding/02-local-networks.jpeg" alt="" />36. 
</Frame></Step>
<Step title="Welcome and security notice">37. 
<Frame caption="Ko‘rsatilgan xavfsizlik ogohlantirishini o‘qing va shunga muvofiq qaror qabul qiling"><img src="/assets/macos-onboarding/03-security-notice.png" alt="" />38. 
</Frame></Step>
<Step title="Local vs Remote">39. 
<Frame><img src="/assets/macos-onboarding/04-choose-gateway.png" alt="" />
</Frame>

40. **Gateway** qayerda ishlaydi?

- 41. **Ushbu Mac (faqat lokal):** onboarding OAuth oqimlarini ishga tushirishi va hisob maʼlumotlarini lokal ravishda yozishi mumkin.
- 42. **Masofaviy (SSH/Tailnet orqali):** onboarding OAuthʼni lokal ravishda ishga tushirmaydi; hisob maʼlumotlari gateway xostida mavjud bo‘lishi kerak.
- 43. **Keyinroq sozlash:** sozlashni o‘tkazib yuborish va ilovani sozlanmagan holda qoldirish.

<Tip>
44. **Gateway auth bo‘yicha maslahat:**
- Endi usta loopback uchun ham **token** yaratadi, shuning uchun lokal WS mijozlari autentifikatsiyadan o‘tishi kerak.
45. - Agar auth’ni o‘chirsangiz, istalgan lokal jarayon ulanadi; buni faqat to‘liq ishonchli mashinalarda ishlating.
46. - Ko‘p mashinali kirish yoki loopback bo‘lmagan bog‘lanishlar uchun **token**dan foydalaning.
</Tip>
</Step>
<Step title="Permissions">48. 
<Frame caption="OpenClawʼga qaysi ruxsatlarni berishni xohlayotganingizni tanlang"><img src="/assets/macos-onboarding/05-permissions.png" alt="" />
</Frame>

49. Onboarding quyidagilar uchun zarur bo‘lgan TCC ruxsatlarini so‘raydi:

- 50. Avtomatlashtirish (AppleScript)
- Notifications
- Accessibility
- Screen Recording
- Microphone
- Speech Recognition
- Camera
- Location

</Step>
<Step title="CLI">
  <Info>This step is optional</Info>
  The app can install the global `openclaw` CLI via npm/pnpm so terminal
  workflows and launchd tasks work out of the box.
</Step>
<Step title="Onboarding Chat (dedicated session)">
  After setup, the app opens a dedicated onboarding chat session so the agent can
  introduce itself and guide next steps. This keeps first‑run guidance separate
  from your normal conversation. See [Bootstrapping](/start/bootstrapping) for
  what happens on the gateway host during the first agent run.
</Step>
</Steps>
